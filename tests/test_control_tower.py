"""Ejercitar Streamlit sin navegador ni red; opcional cuando no se instala el grupo ui."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

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


def assert_ok(app):
    assert not app.exception, [error.message for error in app.exception]


@pytest.fixture
def app(monkeypatch):
    for key in ("MONGODB_URI", "MONGODB_DATABASE"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(tower, "load_config", lambda *_: pytest.fail("Offline no lee .env"))
    monkeypatch.setattr(tower, "create_client", lambda *_: pytest.fail("Offline no crea cliente"))
    result = AppTest.from_file(APP, default_timeout=15).run()
    assert_ok(result)
    return result


def test_default_is_executive_summary_t2_offline(app):
    assert app.radio[0].value == "Resumen"
    assert select(app, "Período").value == "T2"
    assert select(app, "Fuente de datos").value == "Offline"
    metrics = {metric.label: metric.value for metric in app.metric}
    assert metrics["Empresas conocidas · global"] == "23"
    assert metrics["Afirmaciones económicas · global"] == "26"
    assert metrics["Cuentas elegibles · global"] == "21"
    assert metrics["Cambios en cinco plazas · global"] == "3"
    assert any("No observado" in row.value for row in app.markdown)


@pytest.mark.parametrize("page", PAGES)
def test_five_pages_render_and_unsupported_filters_disabled(app, page):
    app.radio[0].set_value(page).run()
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
    app.radio[0].set_value("Graph Health").run()
    assert_ok(app)
    assert app.metric[0].value == str(observations)
    frames = [frame.value for frame in app.dataframe]
    evolution = next(frame for frame in frames if "Corte" in frame.columns)
    assert list(evolution["Corte"]) == ["T0", "T1", "T2"][: ["T0", "T1", "T2"].index(cut) + 1]


def test_company_selector_updates_network_and_detail_without_rescoring(app):
    app.radio[0].set_value("Graph Health").run()
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
    assert select(app, "Empresa").value is None
    assert len(select(app, "Empresa").options) == 13


def test_industry_and_score_filters_preserve_global_rankings(app):
    app.radio[0].set_value("AI Performance").run()
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
    app.radio[0].set_value("Business Funnel").run()
    rows = app.dataframe[0].value.to_dict("records")
    assert [row["Cantidad"] for row in rows[:4]] == ["23", "21", "2", "5"]
    assert all(row["Cantidad"] == "No observado" for row in rows[4:])


def test_finance_tables_match_module_and_do_not_depend_on_company_filters(app):
    select(app, "Industria").set_value(tower.UNKNOWN).run()
    app.radio[0].set_value("Economic Impact").run()
    assert_ok(app)
    report = financial_report(load_financial_config(), sensitivity=True)
    for index, scope in enumerate(("demo", "hypothetical")):
        table = app.dataframe[index].value
        results = [row for row in report["results"] if row["scope"] == scope]
        assert len(table) == 4
        for actual, row in zip(table.to_dict("records"), results, strict=True):
            assert actual["Saldo neto"] == f"${float(row['net_present_value_mxn']):,.2f} MXN"
            assert actual["Equilibrio (pp)"] == row["break_even"]["delta_pp"]
    assert "$39,000.00 MXN" in app.dataframe[1].value["Saldo neto"].values
    assert "$-41,000.00 MXN" in app.dataframe[1].value["Saldo neto"].values


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
    app.radio[0].set_value("Economic Impact").run()
    assert_ok(app)
    assert len(app.dataframe[0].value) == 4


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
    app.radio[0].set_value("AI Performance").run()
    assert_ok(app)
    assert [metric.value for metric in app.metric] == ["No aplica", "No aplica"]


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
    package = root / "economic_graph"
    shutil.copytree(
        ROOT / "src/economic_graph",
        package,
        ignore=shutil.ignore_patterns("simulator", "__pycache__"),
    )
    script = """
import json, socket, sys
from pathlib import Path
from streamlit.testing.v1 import AppTest
def blocked(*args, **kwargs):
    raise AssertionError('Red no autorizada en modo offline')
socket.socket.connect = blocked
socket.create_connection = blocked
app = AppTest.from_file('app/control_tower.py', default_timeout=20).run()
for page in app.radio[0].options:
    app.radio[0].set_value(page).run()
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
