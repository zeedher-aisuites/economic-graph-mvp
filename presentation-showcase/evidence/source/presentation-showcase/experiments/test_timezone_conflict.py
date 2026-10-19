# ruff: noqa: E501
"""Regresión creada por Codex: fixture aislado, copia experimental, sin editar el motor."""

import os
import types
from copy import deepcopy
from pathlib import Path

import pytest

from economic_graph.contracts import validate_observations
from economic_graph.observable import load_observations, snapshot
from economic_graph.rankings import compare_rankings

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("equivalent", ["+00:00", "+0000"])
def test_simultaneous_conflict_is_independent_of_timestamp_spelling(equivalent):
    rows = load_observations(ROOT / "data/observable/observations.json")
    original = next(
        r
        for r in rows
        if r["subject_type"] == "RELATIONSHIP" and r["verification_status"] == "CONFIRMED"
    )
    opposition = {
        **deepcopy(original),
        "observation_id": "OBS-ZZ-TIMEZONE-FIXTURE",
        "verification_status": "DISCARDED",
    }
    opposition["available_at"] = opposition["available_at"].replace("Z", equivalent)
    isolated = [*rows, opposition]
    validate_observations(isolated)
    reader = snapshot
    if os.environ.get("SHOWCASE_SNAPSHOT_VARIANT") != "original":
        # Cambio de una sola comparación en memoria; no se sustituye ningún módulo instalado.
        source = (ROOT / "src/economic_graph/observable.py").read_text(encoding="utf-8")
        source = source.replace(
            'if row["available_at"] == latest["available_at"]',
            'if parse_time(row["available_at"]) == parse_time(latest["available_at"])',
        )
        module = types.ModuleType("experimental_observable")
        exec(compile(source, "experimental_observable.py", "exec"), module.__dict__)
        reader = module.snapshot
    view = reader(isolated, "T2")
    displayed = next(
        r for r in view["relationships"] if r["relationship_id"] == original["subject_id"]
    )
    report = compare_rankings(isolated, "T2")
    scored = next(
        r for r in report["relationship_context"] if r["relationship_id"] == original["subject_id"]
    )
    assert scored["scoring_status"] == "CONFLICTED"
    assert displayed["verification_status"] == "CONFLICTED"
    assert displayed["active_claim"] is False
