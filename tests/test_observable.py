"""Cortes, aislamiento, conflictos y candidatos de identidad sobre evidencia observable."""

import json
from copy import deepcopy
from datetime import timedelta
from pathlib import Path

import pytest

from economic_graph.contracts import assert_no_private_fields, parse_time, validate_observations
from economic_graph.observable import attribute_history, load_observations, snapshot, summarize
from economic_graph.simulator.project import project_observations, write_projection


@pytest.mark.parametrize(
    "cut, companies, claims, referrals, observations",
    [
        ("T0", 12, 2, 0, 28),
        ("T1", 17, 13, 2, 54),
        ("T2", 23, 26, 3, 83),
    ],
)
def test_cut_coverage_and_truth_only_reconciliation(
    projection, approved_design, cut, companies, claims, referrals, observations
):
    rows, private = projection
    view = snapshot(rows, cut)
    summary = summarize(view)
    assert (
        summary["companies"],
        summary["relationship_claims"],
        summary["referrals"],
        summary["observations"],
    ) == (companies, claims, referrals, observations)
    known = {row["company_id"] for row in view["companies"]}
    expected = {
        row["company_id"]
        for row in approved_design["discoveries"]
        if row["first_known_phase"] != "NEVER"
        and parse_time(row["first_known_phase"]) <= parse_time(cut)
    }
    assert known == {private["companies"][key] for key in expected}
    true_ids = {
        private["subjects"][row["relationship_id"]]
        for row in approved_design["relationships"]
        if row["relationship_id"] in private["subjects"]
    }
    expected_true = {"T0": 2, "T1": 11, "T2": 23}[cut]
    assert sum(row["relationship_id"] in true_ids for row in view["relationships"]) == expected_true


@pytest.mark.parametrize("phase, previous_companies", [("T0", 0), ("T1", 12), ("T2", 17)])
def test_exact_boundary_and_observed_date_do_not_leak_future(projection, phase, previous_companies):
    rows, _ = projection
    before = parse_time(phase) - timedelta(microseconds=1)
    assert len(snapshot(rows, before)["companies"]) == previous_companies
    assert all(
        parse_time(row["available_at"]) <= before for row in snapshot(rows, before)["observations"]
    )


@pytest.mark.parametrize(
    "value", ["2026-01-15", "2026-01-15T12:00:00", "2026-99-15T12:00:00Z", "T3"]
)
def test_ambiguous_or_invalid_cut_rejected(value):
    with pytest.raises(ValueError, match="zona horaria"):
        parse_time(value)


def test_explicit_timezone_is_equivalent(projection):
    assert snapshot(projection[0], "2026-05-15T06:00:00-06:00") == snapshot(projection[0], "T1")


def test_all_commercial_outputs_exclude_private_fields_names_and_ids(projection, approved_design):
    rows, _ = projection
    for phase in ("T0", "T1", "T2"):
        view = snapshot(rows, phase)
        assert_no_private_fields(view)
        text = json.dumps(view, ensure_ascii=False)
        assert not any(token in text for token in ("EMP-", "CLM-", "REL-", "truth", "NEVER"))
        for company in approved_design["discoveries"]:
            if company["first_known_phase"] == "NEVER":
                assert company["company_name"] not in text
    for identifier in ("OBS-043", "OBS-044", "OBS-073"):
        note = next(row["evidence_note"] for row in rows if row["observation_id"] == identifier)
        assert not any(
            word in note.lower() for word in ("incorrecta", "confunde", "falsa", "no constituye")
        )


def test_profile_is_not_enriched_from_catalog_and_conflicts_survive(projection):
    rows, private = projection
    view = snapshot(rows, "T2")
    company = next(
        row for row in view["companies"] if row["company_id"] == private["companies"]["EMP-003"]
    )
    assert company["attributes"]["sector"] == {
        "value": None,
        "status": "UNKNOWN",
        "observation_ids": [],
    }
    assert company["attributes"]["size"]["status"] == "UNKNOWN"
    company_id = private["companies"]["EMP-002"]
    assert [row["value"] for row in attribute_history(rows, company_id, "branch_count", "T2")] == [
        2,
        3,
        3,
    ]
    assert [row["value"] for row in attribute_history(rows, company_id, "branch_count", "T0")] == [
        2
    ]
    assert len(view["conflicts"]) == 2
    assert {group["attribute"] for group in view["conflicts"]} == {"branch_count", "size"}
    assert attribute_history(rows, "EMP-011", "display_name", "T2") == []


def test_aliases_stay_candidates_without_using_private_mapping(projection):
    view = snapshot(projection[0], "T2")
    assert len(view["companies"]) == 23
    assert len(view["identities"]) == 2
    assert all(
        row["identity_status"] == "NEEDS_REVIEW" and len(row["candidate_company_ids"]) == 1
        for row in view["identities"]
    )
    assert all("company_id" not in row for row in view["identities"])


def test_reported_and_inferred_claims_are_not_promoted(projection, approved_design):
    rows, private = projection
    relations = {row["relationship_id"]: row for row in snapshot(rows, "T2")["relationships"]}
    for original in [*approved_design["relationships"], *approved_design["claims"]]:
        key = original.get("relationship_id", original.get("claim_id"))
        if key in private["subjects"]:
            assert relations[private["subjects"][key]]["verification_status"] == original.get(
                "planned_initial_status", original.get("reported_status")
            )
    assert all(
        row["verification_status"] == "REPORTED"
        for row in relations.values()
        if row["relationship_type"] == "REFERS_TO"
    )


def test_duplicate_evidence_and_explicit_status_change_are_preserved_in_test_fixture(projection):
    rows, _ = projection
    original = next(row for row in rows if row["observation_id"] == "OBS-034")
    duplicate = deepcopy(original)
    duplicate["observation_id"] = "TEST-DUPLICATE"
    rows.append(duplicate)
    assert (
        len(
            next(
                r
                for r in snapshot(rows, "T1")["relationships"]
                if r["relationship_id"] == original["subject_id"]
            )["status_history"]
        )
        == 2
    )
    discarded = deepcopy(original)
    discarded.update(
        observation_id="TEST-DISCARDED",
        verification_status="DISCARDED",
        available_at="2026-06-01T12:00:00Z",
        recorded_at="2026-06-01T12:00:00Z",
    )
    rows.append(discarded)
    relation = next(
        r
        for r in snapshot(rows, "T2")["relationships"]
        if r["relationship_id"] == original["subject_id"]
    )
    assert relation["verification_status"] == "DISCARDED"
    assert relation["active_claim"] is False
    assert len(relation["status_history"]) == 3
    assert (
        next(
            r
            for r in snapshot(rows, "T1")["relationships"]
            if r["relationship_id"] == original["subject_id"]
        )["verification_status"]
        == "REPORTED"
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "private_nested",
        "duplicate",
        "orphan",
        "self",
        "unknown_type",
        "source",
        "date",
        "time_order",
        "missing",
        "unknown_attribute",
    ],
)
def test_public_contract_rejects_invalid_records(projection, mutation):
    rows = projection[0]
    relation = next(row for row in rows if row["subject_type"] == "RELATIONSHIP")
    if mutation == "private_nested":
        relation["value"]["metadata"] = {"truth_exists": True}
    elif mutation == "duplicate":
        rows.append(deepcopy(rows[0]))
    elif mutation == "orphan":
        relation["value"]["from_company_id"] = "CO-unknown"
    elif mutation == "self":
        relation["value"]["from_company_id"] = relation["value"]["to_company_id"]
    elif mutation == "unknown_type":
        relation["value"]["relationship_type"] = "SAME_BUSINESS_AS"
    elif mutation == "source":
        rows[0]["source_type"] = "UNKNOWN"
    elif mutation == "date":
        rows[0]["available_at"] = "ayer"
    elif mutation == "time_order":
        rows[0]["recorded_at"] = "2027-01-01T12:00:00Z"
    elif mutation == "missing":
        rows[0].pop("source_record_id")
    else:
        rows[0]["attribute"] = "buying_propensity"
    with pytest.raises(ValueError):
        validate_observations(rows)


def test_projection_is_deterministic_and_reader_works_without_restricted_directory(
    projection, approved_design, tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    rows, private = projection
    assert project_observations(approved_design["observations"]) == projection
    write_projection(rows, private)
    path = Path("data/observable/observations.json")
    before = path.read_bytes()
    write_projection(rows, private)
    assert path.read_bytes() == before
    assert not Path("design-data").exists()
    assert summarize(snapshot(load_observations(path), "T2"))["companies"] == 23


def test_reader_rejects_raw_design_file():
    path = Path(__file__).resolve().parents[1] / "design-data/restricted/observation_plan.json"
    with pytest.raises(ValueError, match="contrato observable"):
        load_observations(path)


def test_committed_ledger_matches_projection_and_has_no_commercial_events(projection):
    path = Path(__file__).resolve().parents[1] / "data/observable/observations.json"
    rows = load_observations(path)
    assert rows == projection[0]
    assert len({row["source_record_id"] for row in rows}) == 83
    assert {row["subject_type"] for row in rows} == {"COMPANY", "RELATIONSHIP", "SOURCE_RECORD"}
    assert not any(
        row["attribute"] in {"conversion", "revenue", "score", "commercial_event"} for row in rows
    )
