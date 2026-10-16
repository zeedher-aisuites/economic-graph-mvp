"""Regresiones del adaptador público: paridad, tiempo, red y lectura remota segura."""

import json
import os
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from economic_graph import tower_read_model as tower
from economic_graph.contracts import CUTS, assert_no_private_fields, parse_time
from economic_graph.mongo_observable import MVP_DATABASE, OBSERVATIONS
from economic_graph.observable import load_observations, snapshot, summarize
from economic_graph.rankings import compare_rankings

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/observable/observations.json"


@pytest.fixture
def public_rows():
    return load_observations(LEDGER)


@pytest.mark.parametrize(
    "cut,companies,observations,edges",
    [
        ("T0", 12, 28, 2),
        ("T1", 17, 54, 15),
        ("T2", 23, 83, 29),
    ],
)
def test_context_and_network_match_public_api(public_rows, cut, companies, observations, edges):
    context = tower.build_context(public_rows, cut)
    assert context["ranking"] == compare_rankings(public_rows, cut)
    assert context["summary"] == summarize(snapshot(public_rows, cut))
    assert context["summary"]["companies"] == companies
    assert context["summary"]["observations"] == observations
    network = tower.network_data(context, tower.segment_ids(context))
    assert len(network["nodes"]) == companies
    assert len(network["edges"]) == edges
    node_ids = {node["id"] for node in network["nodes"]}
    assert all(edge["from"] in node_ids and edge["to"] in node_ids for edge in network["edges"])
    assert len({edge["id"] for edge in network["edges"]}) == edges
    assert_no_private_fields({"context": context, "network": network})
    text = json.dumps({"context": context, "network": network}, ensure_ascii=False)
    assert "EMP-" not in text


@pytest.mark.parametrize("cut", ["T0", "T1"])
def test_no_future_nodes_edges_options_or_evolution(public_rows, cut):
    prefix = [r for r in public_rows if parse_time(r["available_at"]) <= parse_time(cut)]
    context = tower.build_context(public_rows, cut)
    assert context == tower.build_context(prefix, cut)
    assert all(parse_time(row["as_of"]) <= parse_time(cut) for row in context["evolution"])
    assert len(context["evolution"]) == list(CUTS).index(cut) + 1
    future_ids = tower.segment_ids(tower.build_context(public_rows, "T2")) - tower.segment_ids(
        context
    )
    for key in future_ids:
        assert tower.account_detail(context, key) is None
    with pytest.raises(ValueError, match="no conocida"):
        tower.network_data(context, {next(iter(future_ids))})


def test_selecting_company_keeps_global_scores_and_adds_only_known_direct_neighbors(public_rows):
    context = tower.build_context(public_rows, "T2")
    before = deepcopy(context)
    cafe = next(
        c
        for c in context["view"]["companies"]
        if c["attributes"]["display_name"]["value"] == "Café Jacaranda"
    )
    key = cafe["company_id"]
    ids = tower.segment_ids(context, company_id=key)
    detail = tower.account_detail(context, key)
    assert (detail["ranking"]["baseline_position"], detail["ranking"]["graph_position"]) == (10, 3)
    assert detail["ranking"]["graph_score"] == 10
    assert tower.ranking_table(context, ids)[0]["Posición grafo"] == 3
    network = tower.network_data(context, ids)
    assert all(key in (edge["from"], edge["to"]) for edge in network["edges"])
    assert any(node["scope"] == "Vecino de contexto" for node in network["nodes"])
    assert set(tower.segment_ids(context)) >= {node["id"] for node in network["nodes"]}
    assert context == before


def test_referrals_reported_inferred_and_isolated_are_not_presented_as_confirmed(public_rows):
    context = tower.build_context(public_rows, "T2")
    network = tower.network_data(context, tower.segment_ids(context))
    assert {edge["status"] for edge in network["edges"]} == {"Confirmada", "Reportada", "Inferida"}
    referrals = [edge for edge in network["edges"] if edge["type"] == tower.TYPES["REFERS_TO"]]
    assert len(referrals) == 3
    assert all(edge["scoring_status"] == "NOT_ECONOMIC" for edge in referrals)
    early = tower.build_context(public_rows, "T0")
    early_network = tower.network_data(early, tower.segment_ids(early))
    assert any(
        node["state"] == "Sin vínculo económico observado" for node in early_network["nodes"]
    )
    assert any(node["state"] == "Sin vínculo confirmado utilizable" for node in network["nodes"])
    assert all(node["identity"] == "NEEDS_REVIEW" for node in network["nodes"])


def test_conflicts_candidates_and_duplicate_evidence_survive(public_rows):
    context = tower.build_context(public_rows, "T2")
    assert len(context["view"]["conflicts"]) == 2
    assert len(context["view"]["identities"]) == 2
    horno = next(
        c for c in context["ranking"]["companies"] if c["display_name"] == "Hornos del Centro"
    )
    detail = tower.account_detail(context, horno["company_id"])
    feature = detail["ranking"]["features"]["additional_branches"]
    assert feature["status"] == "CONFLICTED" and feature["contribution"] == 0
    assert len(feature["evidence"]) > 1
    assert set(o["observation_id"] for o in feature["evidence"]) <= set(
        o["observation_id"] for o in detail["observations"]
    )
    assert len(tower.network_data(context, tower.segment_ids(context))["nodes"]) == 23
    assert sum(context["sources"].values()) == 83


def test_industry_filters_do_not_refill_funnel_or_rankings(public_rows):
    context = tower.build_context(public_rows, "T2")
    ids = tower.segment_ids(context, industry=tower.UNKNOWN)
    assert len(ids) == 10
    rows = tower.funnel(context, ids, "graph")
    eligible = {c["company_id"] for c in context["ranking"]["companies"]}
    assert rows[0]["Cantidad"] == rows[1]["Cantidad"] + rows[2]["Cantidad"]
    assert rows[1]["Cantidad"] == len(ids & eligible)
    assert rows[3]["Cantidad"] == len(ids & set(context["ranking"]["top_k"]["graph"]))
    assert all(row["Cantidad"] is None and row["Estado"] == "No observado" for row in rows[4:])
    assert tower.ranking_table(context, ids) == [
        row for row in tower.ranking_table(context) if row["ID"] in ids
    ]
    assert tower.segment_ids(context, industry="Sector inexistente") == set()


def test_empty_context_has_no_fabricated_coverage_or_stages():
    context = tower.build_context([], "T0")
    assert context["coverage"] == {"branches": 0, "neighbors": 0, "denominator": 0}
    assert tower.network_data(context, set()) == {"nodes": [], "edges": []}
    assert tower.account_detail(context, "CO-unknown") is None
    assert all(row["Cantidad"] is None for row in tower.funnel(context, set(), "graph")[4:])


def test_network_preserves_simultaneous_verification_conflict(public_rows):
    # Fixture de prueba explícito; no modifica el ledger ni inventa un hecho de la demo.
    original = next(
        row
        for row in public_rows
        if row["subject_type"] == "RELATIONSHIP" and row["verification_status"] == "CONFIRMED"
    )
    opposition = {
        **deepcopy(original),
        "observation_id": "OBS-TEST-CONFLICT",
        "verification_status": "DISCARDED",
    }
    context = tower.build_context([*public_rows, opposition], "T2")
    edge = next(
        row
        for row in tower.network_data(context, tower.segment_ids(context))["edges"]
        if row["id"] == original["subject_id"]
    )
    assert edge["status"] == "En conflicto"
    assert edge["scoring_status"] == "CONFLICTED"
    assert "OBS-TEST-CONFLICT" in edge["evidence"]


def test_discarded_link_is_visible_as_discarded_not_confirmed(public_rows):
    rows = deepcopy(public_rows)
    original = next(
        row
        for row in rows
        if row["subject_type"] == "RELATIONSHIP" and row["verification_status"] == "CONFIRMED"
    )
    original["verification_status"] = "DISCARDED"
    context = tower.build_context(rows, "T2")
    edge = next(
        row
        for row in tower.network_data(context, tower.segment_ids(context))["edges"]
        if row["id"] == original["subject_id"]
    )
    assert edge["status"] == "Descartada"
    assert edge["scoring_status"] == "DISCARDED"


def test_vega_spec_uses_embedded_data_no_remote_resources(public_rows):
    altair = pytest.importorskip("altair", reason="Grupo ui opcional no instalado")
    context = tower.build_context(public_rows, "T1")
    network = tower.network_data(context, tower.segment_ids(context))
    spec = tower.network_spec(network)
    altair.LayerChart.from_dict(spec, validate=True)
    assert spec["layer"][0]["data"]["values"] == network["edges"]
    assert spec["layer"][1]["data"]["values"] == network["nodes"]
    assert "url" not in json.dumps(spec)
    encoding = spec["layer"][0]["encoding"]
    assert encoding["color"]["field"] == "type"
    assert encoding["strokeDash"]["field"] == "status"


def install_read_only_client(monkeypatch, rows):
    """No ofrece ping, metadata, carga, índices ni métodos de escritura."""
    calls = []

    class Collection:
        def find(self, query):
            calls.append(query)
            return [
                {**r, "_id": r["observation_id"]}
                for r in rows
                if parse_time(r["available_at"]) <= query["available_at"]["$lte"]
            ]

    class Database:
        name = MVP_DATABASE

        def __getitem__(self, name):
            assert name == OBSERVATIONS
            return Collection()

    class Client:
        def __enter__(self):
            calls.append("open")
            return self

        def __exit__(self, *args):
            calls.append("closed")

        def __getitem__(self, name):
            assert name == MVP_DATABASE
            return Database()

    monkeypatch.setattr(tower, "create_client", lambda uri: Client())
    monkeypatch.setattr(tower, "load_config", lambda path: ("mongodb://fake", MVP_DATABASE))
    return calls


def test_atlas_is_find_only_parity_and_closes_client(monkeypatch, public_rows):
    calls = install_read_only_client(monkeypatch, public_rows)
    result = tower.atlas_context("T1", LEDGER, ROOT / ".env")
    assert result["context"] == tower.build_context(public_rows, "T1")
    assert calls == ["open", {"available_at": {"$lte": parse_time("T1")}}, "closed"]
    assert parse_time(result["read_at"])
    assert "mongodb" not in json.dumps(result)


def test_atlas_mismatch_is_blocked_without_fallback(monkeypatch, public_rows):
    changed = deepcopy(public_rows)
    changed[0]["evidence_note"] += " diferente"
    calls = install_read_only_client(monkeypatch, changed)
    with pytest.raises(ValueError, match="Datos distintos"):
        tower.atlas_context("T2", LEDGER, ROOT / ".env")
    assert calls[-1] == "closed"


def test_atlas_invalid_database_rejected_before_client(monkeypatch):
    monkeypatch.setattr(tower, "load_config", lambda path: ("mongodb://fake", "production"))
    monkeypatch.setattr(tower, "create_client", lambda uri: pytest.fail("Conexión no autorizada"))
    with pytest.raises(ValueError, match="No se pudo leer Atlas"):
        tower.atlas_context("T2", LEDGER, ROOT / ".env")


def test_atlas_failure_never_exposes_driver_text(monkeypatch, public_rows):
    install_read_only_client(monkeypatch, public_rows)

    def failed(uri):
        raise ConnectionError("mongodb+srv://fake-user:fake-pass@fake-host/private")

    monkeypatch.setattr(tower, "create_client", failed)
    with pytest.raises(ValueError) as error:
        tower.atlas_context("T2", LEDGER, ROOT / ".env")
    assert "fake-pass" not in str(error.value)
    assert "mongodb" not in str(error.value)


@pytest.mark.parametrize("cut", ["T0", "T1", "T2"])
def test_focused_network_only_highlights_approved_feature_evidence(public_rows, cut):
    context = tower.build_context(public_rows, cut)
    before = deepcopy(context)
    cafe = next(
        row for row in context["ranking"]["companies"] if row["display_name"] == "Café Jacaranda"
    )
    key = cafe["company_id"]
    network = tower.network_data(context, {key}, focus_id=key)
    center = next(node for node in network["nodes"] if node["id"] == key)
    assert (center["x"], center["y"]) == (0, 0)
    expected = {
        identifier
        for neighbor in cafe["features"]["confirmed_neighbors"]["neighbors"]
        for identifier in neighbor["relationship_ids"]
    }
    assert {edge["id"] for edge in network["edges"] if edge["supports_focus"]} == expected
    assert all(
        edge["scoring_status"] == "CONFIRMED" for edge in network["edges"] if edge["supports_focus"]
    )
    assert all(
        not edge["supports_focus"]
        for edge in network["edges"]
        if edge["type"] == tower.TYPES["REFERS_TO"]
    )
    assert len({(node["x"], node["y"]) for node in network["nodes"]}) == len(network["nodes"])
    assert context == before
    assert_no_private_fields(network)


def test_focus_cannot_refer_to_company_outside_selection(public_rows):
    context = tower.build_context(public_rows, "T0")
    with pytest.raises(ValueError, match="única empresa"):
        tower.network_data(context, tower.segment_ids(context), focus_id="CO-unknown")


@pytest.mark.parametrize("cut", ["T0", "T1", "T2"])
def test_context_has_exact_parity_with_ranking_cli(public_rows, cut):
    environment = {
        key: value for key, value in os.environ.items() if not key.upper().startswith("MONGODB_")
    }
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/rank_companies.py"), "--as-of", cut],
        cwd=ROOT,
        env=environment,
        capture_output=True,
        timeout=20,
    )
    assert result.returncode == 0, (
        "El CLI offline falló; ejecutar rank_companies.py para diagnosticar."
    )
    assert tower.build_context(public_rows, cut)["ranking"] == json.loads(
        result.stdout.decode("utf-8")
    )
