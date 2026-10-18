"""Ejercitar Streamlit sin navegador ni red; opcional cuando no se instala el grupo ui."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from ui_test_support import prepare_ui_runtime, run_app

from economic_graph import tower_read_model as tower
from economic_graph.finance import financial_report, load_financial_config
from economic_graph.observable import load_observations

pytest.importorskip("streamlit", reason="Instala el grupo ui para probar la interfaz")
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "app/control_tower.py"
PAGES = ["Resumen", "Graph Health", "AI Performance", "Business Funnel", "Economic Impact"]


def select(app, label):
    return next(widget for widget in app.selectbox if widget.label == label)


def view(app):
    return next(widget for widget in app.radio if widget.label == "Vista")


def assert_ok(app):
    assert not app.exception, [error.message for error in app.exception]


@pytest.fixture(scope="module")
def ui_runtime():
    return prepare_ui_runtime()


@pytest.fixture
def app(monkeypatch, ui_runtime, record_property):
    record_property("ui_dependency_setup_seconds", json.dumps(ui_runtime, sort_keys=True))
    for key in ("MONGODB_URI", "MONGODB_DATABASE"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(tower, "load_config", lambda *_: pytest.fail("Offline no lee .env"))
    monkeypatch.setattr(tower, "create_client", lambda *_: pytest.fail("Offline no crea cliente"))
    result = run_app(AppTest.from_file(APP, default_timeout=15))
    assert_ok(result)
    return result


def test_default_is_executive_summary_t2_offline(app):
    assert view(app).value == "Resumen"
    assert select(app, "Período").value == "T2"
    assert select(app, "Fuente de datos").value == "Offline"
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Empresas conocidas · global"] == "23"
    assert metrics["Afirmaciones económicas · global"] == "26"
    assert metrics["Cuentas elegibles · global"] == "21"
    assert metrics["Cambios en cinco plazas · global"] == "3"
    assert any("No observado" in row.value for row in app.markdown)
    text = "\n".join(row.value for row in app.markdown)
    assert "El grafo modifica 3 de las 5 selecciones comerciales" in text
    assert "+$39,000" in text and "−$41,000" in text
    assert len(app.dataframe) == 2  # Solo selecciones; finanzas principales sin tabla ancha.


@pytest.mark.parametrize("page", PAGES)
def test_five_pages_render_and_unsupported_filters_disabled(app, page):
    view(app).set_value(page).run()
    assert_ok(app)
    for label in ("Geografía", "Cluster", "Producto", "Canal comercial"):
        assert select(app, label).disabled
    if page == "Economic Impact":
        assert select(app, "Período").disabled
        assert select(app, "Industria").disabled
        assert select(app, "Empresa").disabled
        assert any("Hipótesis educativas" in row.value for row in app.warning)


@pytest.mark.parametrize("cut,known,observations", [("T0", 12, 28), ("T1", 17, 54), ("T2", 23, 83)])
def test_cut_controls_options_and_no_future_evolution(app, cut, known, observations):
    select(app, "Período").set_value(cut).run()
    assert len(select(app, "Empresa").options) == known + 1
    view(app).set_value("Graph Health").run()
    assert_ok(app)
    assert app.metric[0].value == str(observations)
    frames = [frame.value for frame in app.dataframe]
    evolution = next(frame for frame in frames if "Corte" in frame.columns)
    assert list(evolution["Corte"]) == ["T0", "T1", "T2"][: ["T0", "T1", "T2"].index(cut) + 1]


def test_company_selector_updates_network_and_detail_without_rescoring(app):
    view(app).set_value("Graph Health").run()
    companies = tower.build_context(load_observations(), "T2")["view"]["companies"]
    cafe = next(
        c["company_id"]
        for c in companies
        if c["attributes"]["display_name"]["value"] == "Café Jacaranda"
    )
    select(app, "Empresa").set_value(cafe).run()
    assert_ok(app)
    assert any("Ficha · Café Jacaranda" in heading.value for heading in app.subheader)
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Posición baseline global"] == "10"
    assert metrics["Posición grafo global"] == "3"
    edges = next(frame.value for frame in app.dataframe if "Desde" in frame.value.columns)
    assert all(
        row["Desde"] == "Café Jacaranda" or row["Hacia"] == "Café Jacaranda"
        for _, row in edges.iterrows()
    )
    assert any("Procedencia e historia" in e.label for e in app.expander)
    select(app, "Período").set_value("T0").run()
    assert_ok(app)
    known = tower.segment_ids(tower.build_context(load_observations(), "T0"))
    assert select(app, "Empresa").value in known
    assert len(select(app, "Empresa").options) == 12


def test_industry_and_score_filters_preserve_global_rankings(app):
    view(app).set_value("AI Performance").run()
    select(app, "Industria").set_value(tower.UNKNOWN).run()
    assert_ok(app)
    context = tower.build_context(load_observations(), "T2")
    ids = tower.segment_ids(context, industry=tower.UNKNOWN)
    expected = tower.ranking_table(context, ids)
    actual = next(
        frame.value for frame in app.dataframe if "Posición baseline" in frame.value.columns
    )
    assert actual.to_dict("records") == expected
    app.number_input[0].set_value(1).run()
    assert_ok(app)
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Cobertura individual · global"] == "3/21"


def test_funnel_missing_stages_are_text_not_zero(app):
    view(app).set_value("Business Funnel").run()
    rows = app.dataframe[0].value.to_dict("records")
    assert [row["Cantidad"] for row in rows[:4]] == ["23", "21", "2", "5"]
    assert all(row["Cantidad"] == "No observado" for row in rows[4:])


def test_finance_tables_match_module_and_do_not_depend_on_company_filters(app):
    select(app, "Industria").set_value(tower.UNKNOWN).run()
    view(app).set_value("Economic Impact").run()
    assert_ok(app)
    report = financial_report(load_financial_config(), sensitivity=True)
    for scope, capacity in (("demo", 5), ("hypothetical", 500)):
        table = app.dataframe[0].value
        table = table[table["Capacidad"] == capacity]
        results = [row for row in report["results"] if row["scope"] == scope]
        assert len(table) == 4
        for actual, row in zip(table.to_dict("records"), results, strict=True):
            assert actual["Saldo neto"] == f"${float(row['net_present_value_mxn']):,.2f} MXN"
            assert actual["Equilibrio (pp)"] == row["break_even"]["delta_pp"]
    assert "$39,000.00 MXN" in app.dataframe[0].value["Saldo neto"].values
    assert "$-41,000.00 MXN" in app.dataframe[0].value["Saldo neto"].values
    scale = next(widget for widget in app.radio if widget.label == "Escala del ejercicio")
    scale.set_value("hypothetical").run()
    assert_ok(app)
    text = "\n".join(element.value for element in app.markdown)
    assert "+$39,000" in text and "−$41,000" in text


def test_atlas_requires_button_and_context_changes_invalidate_old_rows(app, monkeypatch):
    calls = []

    def fake(cut, *_):
        calls.append(cut)
        return {"context": tower.build_context(load_observations(), cut), "read_at": "fixture UTC"}

    monkeypatch.setattr(tower, "atlas_context", fake)
    select(app, "Fuente de datos").set_value("Atlas · solo lectura").run()
    assert_ok(app)
    assert calls == [] and len(app.metric) == 0
    app.button[0].click().run()
    assert_ok(app)
    assert calls == ["T2"]
    select(app, "Industria").set_value(tower.UNKNOWN).run()
    assert calls == ["T2"]
    select(app, "Período").set_value("T0").run()
    assert len(app.metric) == 0
    assert "atlas_result" not in app.session_state
    select(app, "Fuente de datos").set_value("Offline").run()
    assert app.metric[0].value == "12"


def test_invalid_ledger_is_visible_and_finance_still_available(app, monkeypatch):
    from economic_graph import observable

    def invalid(*_):
        raise ValueError("fixture malformed")

    monkeypatch.setattr(observable, "load_observations", invalid)
    app.run()
    assert_ok(app)
    assert any("ledger observable" in error.value for error in app.error)
    assert len(app.metric) == 0
    view(app).set_value("Economic Impact").run()
    assert_ok(app)
    assert len(app.dataframe[0].value) == 8


def test_atlas_error_does_not_reuse_previous_success(app, monkeypatch):
    def failed(*_):
        raise ValueError("Datos distintos del ledger aprobado. Demostración comparable bloqueada.")

    monkeypatch.setattr(tower, "atlas_context", failed)
    select(app, "Fuente de datos").set_value("Atlas · solo lectura").run()
    app.button[0].click().run()
    assert_ok(app)
    assert len(app.metric) == 0
    assert "atlas_result" not in app.session_state
    assert any("bloqueada" in error.value for error in app.error)


def test_empty_eligible_population_has_no_percentage_with_zero_denominator(app, monkeypatch):
    from economic_graph import observable

    monkeypatch.setattr(observable, "load_observations", lambda *_: [])
    view(app).set_value("AI Performance").run()
    assert_ok(app)
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Cobertura individual · global"] == "No aplica"
    assert metrics["Señal relacional utilizable · global"] == "No aplica"


def test_public_only_ui_utf8_and_paths_with_spaces_without_network_or_env(tmp_path):
    root = tmp_path / "Demostración pública con espacios"
    (root / "app").mkdir(parents=True)
    (root / "data/observable").mkdir(parents=True)
    (root / "config").mkdir()
    shutil.copy(APP, root / "app/control_tower.py")
    shutil.copy(
        ROOT / "data/observable/observations.json", root / "data/observable/observations.json"
    )
    shutil.copy(
        ROOT / "config/financial_assumptions.json", root / "config/financial_assumptions.json"
    )
    shutil.copy(ROOT / "tests/ui_test_support.py", root / "ui_test_support.py")
    package = root / "economic_graph"
    shutil.copytree(
        ROOT / "src/economic_graph",
        package,
        ignore=shutil.ignore_patterns("simulator", "__pycache__"),
    )
    script = """
import asyncio, json, socket, sys, threading
from pathlib import Path
from ui_test_support import install_network_guard, prepare_ui_runtime, run_app

native_pair = socket.socketpair
def windows_style_pair(*args, **kwargs):
    if sys.platform == 'win32':
        return native_pair(*args, **kwargs)
    # Ejercitar el mecanismo TCP de Windows incluso en Linux, sin red externa.
    assert not args and not kwargs
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(('127.0.0.1', 0))
        listener.listen(1)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(listener.getsockname())
            server, _ = listener.accept()
        except BaseException:
            client.close()
            raise
    assert server.getpeername() == client.getsockname()
    return server, client

pair_factory = native_pair if sys.platform == 'win32' else getattr(
    socket, '_fallback_socketpair', windows_style_pair
)
install_network_guard(socketpair_factory=pair_factory)
# IPC real permitido; los destinos externos y otros servicios locales siguen bloqueados.
left, right = socket.socketpair()
try:
    left.sendall(b'ipc')
    assert right.recv(3) == b'ipc'
finally:
    left.close()
    right.close()
loop = asyncio.new_event_loop()
try:
    loop.run_until_complete(asyncio.sleep(0))
finally:
    loop.close()
for address in (('198.51.100.1', 443), ('127.0.0.1', 9), ('::1', 9)):
    family = socket.AF_INET6 if ':' in address[0] else socket.AF_INET
    with socket.socket(family, socket.SOCK_STREAM) as probe:
        for method in (probe.connect, probe.connect_ex):
            try:
                method(address)
            except AssertionError:
                pass
            else:
                raise AssertionError('El guard permitió una conexión no autorizada')
for operation in (
    lambda: socket.create_connection(('example.com', 443)),
    lambda: socket.getaddrinfo('example.com', 443),
):
    try:
        operation()
    except AssertionError:
        pass
    else:
        raise AssertionError('El guard permitió acceso de red o DNS')

class ColdImportGuard:
    def find_spec(self, fullname, path=None, target=None):
        if fullname in {'numpy', 'pandas', 'pyarrow', 'altair'}:
            assert threading.current_thread() is threading.main_thread(), (
                'Importación nativa fría dentro del timeout funcional: ' + fullname
            )
        return None

sys.meta_path.insert(0, ColdImportGuard())
prepare_ui_runtime()
from streamlit.testing.v1 import AppTest
def view(app):
    return next(widget for widget in app.radio if widget.label == "Vista")
app = run_app(AppTest.from_file('app/control_tower.py', default_timeout=20))
for page in view(app).options:
    view(app).set_value(page)
    run_app(app)
    if app.exception:
        raise AssertionError([e.message for e in app.exception])
import economic_graph.tower_read_model as tower
assert Path(tower.__file__).resolve().is_relative_to(Path.cwd())
assert not any(k.startswith('economic_graph.simulator') for k in sys.modules)
message = json.dumps({'resultado': 'Red económica y Café ✓'}, ensure_ascii=False)
sys.stdout.buffer.write(message.encode('utf-8'))
"""
    environment = {
        key: value for key, value in os.environ.items() if not key.upper().startswith("MONGODB_")
    }
    environment.update(PYTHONPATH=str(root), PYTHONUTF8="0", PYTHONIOENCODING="cp1252:strict")
    result = subprocess.run(
        [sys.executable, "-c", script], cwd=root, env=environment, capture_output=True, timeout=60
    )
    if result.returncode:
        # El hijo no recibe secretos y solo ejecuta offline; no imprimir objetos subprocess.
        diagnostic = result.stderr.decode("utf-8", errors="replace")
        import re

        diagnostic = re.sub(r"mongodb(?:\+srv)?://\S+", "[URI redactada]", diagnostic)
        pytest.fail("UI aislada falló:\n" + diagnostic, pytrace=False)
    assert json.loads(result.stdout.decode("utf-8"))["resultado"] == "Red económica y Café ✓"


def test_graph_opens_focused_and_full_network_is_secondary(app):
    view(app).set_value("Graph Health").run()
    assert_ok(app)
    mode = next(widget for widget in app.radio if widget.label == "Exploración de red")
    assert mode.value == "Empresa y vecinos"
    context = tower.build_context(load_observations(), "T2")
    cafe = next(
        row["company_id"]
        for row in context["ranking"]["companies"]
        if row["display_name"] == "Café Jacaranda"
    )
    assert select(app, "Empresa").value == cafe
    mode.set_value("Red completa del segmento").run()
    assert_ok(app)
    assert select(app, "Empresa").value is None
    assert select(app, "Empresa").disabled
    mode = next(widget for widget in app.radio if widget.label == "Exploración de red")
    mode.set_value("Empresa y vecinos").run()
    assert_ok(app)
    assert select(app, "Empresa").value == cafe
    assert not select(app, "Empresa").disabled


def test_focus_drops_future_account_when_cut_changes(app):
    view(app).set_value("Graph Health").run()
    early = tower.segment_ids(tower.build_context(load_observations(), "T0"))
    future = tower.segment_ids(tower.build_context(load_observations(), "T2")) - early
    selected = sorted(future)[0]
    select(app, "Empresa").set_value(selected).run()
    assert_ok(app)
    select(app, "Período").set_value("T0").run()
    assert_ok(app)
    assert select(app, "Empresa").value in early
    assert selected != app.session_state["company"]


@pytest.mark.parametrize("page", PAGES)
def test_all_technical_panels_are_collapsed_initially(app, page):
    view(app).set_value(page).run()
    assert_ok(app)
    assert app.expander
    assert all(not panel.proto.expanded for panel in app.expander)


def test_economic_scale_switch_keeps_four_signed_scenarios_and_baseline_threshold(app):
    view(app).set_value("Economic Impact").run()
    assert_ok(app)
    assert (
        next(widget for widget in app.radio if widget.label == "Escala del ejercicio").value
        == "demo"
    )
    text = "\n".join(row.value for row in app.markdown)
    assert all(label in text for label in ("Conservador", "Base", "Optimista", "Nulo"))
    assert "−$15,450" in text and "−$16,250" in text
    metric = next(metric for metric in app.metric if metric.label == "Equilibrio · supuesto base")
    assert metric.value == "40.625 pp"
    next(widget for widget in app.radio if widget.label == "Escala del ejercicio").set_value(
        "hypothetical"
    ).run()
    assert_ok(app)
    metric = next(metric for metric in app.metric if metric.label == "Equilibrio · supuesto base")
    assert metric.value == "1.025 pp"
    assert all(not panel.proto.expanded for panel in app.expander)


def test_returning_to_global_view_restores_funnel_without_changing_rankings(app):
    view(app).set_value("Graph Health").run()
    assert_ok(app)
    view(app).set_value("Business Funnel").run()
    assert_ok(app)
    button = next(widget for widget in app.button if widget.label == "Mostrar todas las empresas")
    button.click().run()
    assert_ok(app)
    assert select(app, "Empresa").value is None
    assert select(app, "Industria").value == "Todas"
    counts = {metric.label: metric.value for metric in app.metric}
    assert counts["Conocidas"] == "23"
    assert counts["Elegibles para ranking"] == "21"
    assert counts["Priorizadas del top-5 global"] == "5"
    assert all(
        row["Cantidad"] == "No observado" for row in app.dataframe[0].value.to_dict("records")[4:]
    )
