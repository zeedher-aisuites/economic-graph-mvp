"""Auditoría de los archivos aprobados y rechazo de desviaciones de diseño."""

import shutil
from collections import Counter
from copy import deepcopy
from pathlib import Path

import pytest

from economic_graph.simulator.design import audit_design, load_design


def test_approved_sources_are_structurally_consistent(approved_design):
    report = audit_design(approved_design)
    assert report["errors"] == []
    assert len(report["warnings"]) == 5
    assert approved_design["csv_errors"] == []
    assert approved_design["integrity_errors"] == []


def test_exact_world_counts_and_ids(approved_design):
    assert {row["company_id"] for row in approved_design["companies"]} == {
        f"EMP-{i:03}" for i in range(1, 31)
    }
    assert len({row["relationship_id"] for row in approved_design["relationships"]}) == 48
    assert all(row["truth_exists"] for row in approved_design["relationships"])
    assert Counter(row["relationship_type"] for row in approved_design["relationships"]) == {
        "SUPPLIES_TO": 41,
        "PARTNERS_WITH": 7,
    }
    assert len(approved_design["claims"]) == len(approved_design["referrals"]) == 3
    assert {row["truth_status"] for row in approved_design["claims"]} == {"FALSE"}


def test_observations_sources_and_closed_world_coverage(approved_design):
    observations = approved_design["observations"]
    assert len({row["observation_id"] for row in observations}) == 83
    assert Counter(row["phase"] for row in observations) == {"T0": 28, "T1": 26, "T2": 29}
    assert Counter(row["source_type"] for row in observations) == {
        "CRM": 37,
        "PUBLIC_PROFILE": 16,
        "REFERRAL": 15,
        "DIRECTORY": 13,
        "TELCO_INTERNAL": 2,
    }
    counts = audit_design(approved_design)["counts"]
    assert counts["cuts"] == {
        "T0": {"companies": 12, "planned_true_relationships": 2},
        "T1": {"companies": 17, "planned_true_relationships": 11},
        "T2": {"companies": 23, "planned_true_relationships": 23},
    }
    assert counts["unknown_companies_t2"] == 7
    assert counts["unknown_true_relationships_t2"] == 25


@pytest.mark.parametrize(
    "mutation, expected",
    [
        ("orphan", "huérfano"),
        ("self", "auto-relación"),
        ("unknown_type", "tipo económico"),
        ("duplicate", "únicos"),
        ("bad_date", "fecha inválida"),
        ("missing", "campos obligatorios"),
        ("future_endpoint", "no identificable"),
        ("altered_referral", "referencia comercial"),
        ("alias_merged", "fusionado sin evidencia"),
    ],
)
def test_audit_reports_bad_data_without_repairing_it(approved_design, mutation, expected):
    data = deepcopy(approved_design)
    if mutation == "orphan":
        data["relationships"][0]["from_company_id"] = "EMP-999"
    elif mutation == "self":
        data["relationships"][0]["from_company_id"] = data["relationships"][0]["to_company_id"]
    elif mutation == "unknown_type":
        data["relationships"][0]["relationship_type"] = "SAME_BUSINESS_AS"
    elif mutation == "duplicate":
        data["observations"][1]["observation_id"] = data["observations"][0]["observation_id"]
    elif mutation == "bad_date":
        data["observations"][0]["available_at"] = "2026-99-15"
    elif mutation == "missing":
        data["observations"][0].pop("evidence_note")
    elif mutation == "future_endpoint":
        data["observations"][33]["value"]["from_company_id"] = "EMP-030"
    elif mutation == "altered_referral":
        data["referrals"][0]["referred_company_id"] = "EMP-029"
    else:
        data["aliases"][0]["resolution"] = "RESOLVED"
    before = deepcopy(data)
    assert any(expected in error for error in audit_design(data)["errors"])
    assert data == before


def test_missing_input_identifies_file(tmp_path):
    with pytest.raises(ValueError, match="companies_world_design.json"):
        load_design(tmp_path)


def test_modified_csv_and_fingerprint_are_detected(tmp_path):
    original = Path(__file__).resolve().parents[1] / "design-data"
    shutil.copytree(original, tmp_path / "design-data")
    target = tmp_path / "design-data/restricted/companies_world_design.csv"
    target.write_text(
        target.read_text(encoding="utf-8-sig").replace("La Espiga del Barrio", "Nombre alterado"),
        encoding="utf-8",
    )
    data = load_design(target.parent)
    assert data["csv_errors"]
    assert any(target.name in error for error in data["integrity_errors"])
