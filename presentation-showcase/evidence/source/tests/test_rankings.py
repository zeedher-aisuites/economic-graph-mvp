"""Políticas aprobadas: fixtures públicos y casos adversos, sin oráculo ni red."""

import json
from copy import deepcopy
from datetime import timedelta
from pathlib import Path
from unittest.mock import Mock

import pytest

from economic_graph.contracts import CUTS, assert_no_private_fields, parse_time
from economic_graph.observable import load_observations, snapshot
from economic_graph.rankings import compare_rankings, render_comparison

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def public_ledger():
    return load_observations(ROOT / "data/observable/observations.json")


def observation(
    identifier, subject, attribute, value, *, kind="COMPANY", status="REPORTED", cut="T0"
):
    instant = CUTS.get(cut, cut)
    return {
        "observation_id": identifier,
        "subject_type": kind,
        "subject_id": subject,
        "attribute": attribute,
        "value": value,
        "source_type": "CRM",
        "source_record_id": f"TEST-SRC-{identifier}",
        "verification_status": status,
        "observed_at": instant,
        "recorded_at": instant,
        "available_at": instant,
        "evidence_note": "Fixture de prueba; no amplía el ledger aprobado.",
        "conflict_group": None,
    }


def claim(
    identifier="TEST-LINK",
    subject="LINK-A",
    left="CO-A",
    right="CO-B",
    kind="SUPPLIES_TO",
    status="CONFIRMED",
    cut="T0",
):
    return observation(
        identifier,
        subject,
        "relationship_claim",
        {
            "from_company_id": left,
            "to_company_id": right,
            "relationship_type": kind,
        },
        kind="RELATIONSHIP",
        status=status,
        cut=cut,
    )


@pytest.fixture
def small_ledger():
    return [
        observation(f"TEST-NAME-{key}", f"CO-{key}", "display_name", f"Cuenta {key}")
        for key in "ABC"
    ]


def company(report, key="CO-A"):
    return next(row for row in report["companies"] if row["company_id"] == key)


@pytest.mark.parametrize(
    "cut,known,eligible,observations",
    [
        ("T0", 12, 12, 28),
        ("T1", 17, 17, 54),
        ("T2", 23, 21, 83),
    ],
)
def test_same_cohort_capacity_and_explanations(public_ledger, cut, known, eligible, observations):
    report = compare_rankings(public_ledger, cut)
    assert (
        report["known_companies"],
        report["eligible_companies"],
        report["visible_observations"],
    ) == (known, eligible, observations)
    assert report["policy"]["version"] == "003a-conservative-v1"
    assert report["policy"]["capacity"] == 5
    assert len(report["top_k"]["baseline"]) == len(report["top_k"]["graph"]) == 5
    assert sorted(row["baseline_position"] for row in report["companies"]) == list(
        range(1, eligible + 1)
    )
    assert sorted(row["graph_position"] for row in report["companies"]) == list(
        range(1, eligible + 1)
    )
    for row in report["companies"]:
        branches, neighbors = row["features"].values()
        assert row["baseline_score"] == branches["contribution"]
        assert row["graph_score"] == row["baseline_score"] + neighbors["contribution"]
        assert row["position_change"] == row["baseline_position"] - row["graph_position"]
        assert branches["weight"] == 10 and neighbors["weight"] == 5
        assert branches["rule"] and neighbors["rule"]
        for feature in (branches, neighbors):
            for evidence in feature["evidence"]:
                assert evidence["source_record_id"] and evidence["evidence_note"]
                for date in ("observed_at", "recorded_at", "available_at"):
                    assert parse_time(evidence[date]) <= parse_time(cut)
    assert_no_private_fields(report)
    assert len(report["comparison"]["entered_graph"]) == 3
    assert len(report["comparison"]["left_baseline"]) == 3


@pytest.mark.parametrize(
    "cut,baseline,graph",
    [
        (
            "T0",
            [
                "Hornos del Centro",
                "Comedor del Andén",
                "Ruta Corta Mensajería",
                "Papelería Horizonte",
                "Ferretería Cinco Calles",
            ],
            [
                "Hornos del Centro",
                "Papelería Horizonte",
                "Café Jacaranda",
                "Enlace Punto POS",
                "Nodo Azul Soporte TI",
            ],
        ),
        (
            "T1",
            [
                "Panificadora Valle Claro",
                "Carga Urbana del Centro",
                "Comedor del Andén",
                "Mesa de Barrio",
                "Ruta Corta Mensajería",
            ],
            [
                "Panificadora Valle Claro",
                "Carga Urbana del Centro",
                "Papelería Horizonte",
                "Café Jacaranda",
                "Enlace Punto POS",
            ],
        ),
        (
            "T2",
            [
                "Panificadora Valle Claro",
                "Carga Urbana del Centro",
                "Comedor del Andén",
                "Mesa de Barrio",
                "Mapa Digital Studio",
            ],
            [
                "Panificadora Valle Claro",
                "Carga Urbana del Centro",
                "Café Jacaranda",
                "Hornos del Centro",
                "Papelería Horizonte",
            ],
        ),
    ],
)
def test_regression_approved_policy_top_five(public_ledger, cut, baseline, graph):
    report = compare_rankings(public_ledger, cut)
    names = {row["company_id"]: row["display_name"] for row in report["companies"]}
    assert [names[key] for key in report["top_k"]["baseline"]] == baseline
    assert [names[key] for key in report["top_k"]["graph"]] == graph


@pytest.mark.parametrize("cut", CUTS)
def test_future_data_cannot_change_any_historical_output(public_ledger, cut):
    visible = [row for row in public_ledger if parse_time(row["available_at"]) <= parse_time(cut)]
    report = compare_rankings(public_ledger, cut)
    assert report == compare_rankings(visible, cut)
    future = [
        observation(
            "TEST-FUTURE-NAME",
            "CO-future",
            "display_name",
            "Cuenta futura",
            cut="2027-01-01T12:00:00Z",
        ),
        observation(
            "TEST-FUTURE-SIZE", "CO-future", "branch_count", 100, cut="2027-01-01T12:00:00Z"
        ),
    ]
    future[1]["observed_at"] = CUTS["T0"]
    assert report == compare_rankings([*public_ledger, *future], cut)
    assert "Cuenta futura" not in json.dumps(report, ensure_ascii=False)


@pytest.mark.parametrize("cut,prior_known", [("T0", 0), ("T1", 12), ("T2", 17)])
def test_exact_boundary_and_timezone(public_ledger, cut, prior_known):
    before = parse_time(cut) - timedelta(microseconds=1)
    assert compare_rankings(public_ledger, before)["known_companies"] == prior_known
    offset = parse_time(cut).isoformat().replace("+00:00", "Z")
    assert compare_rankings(public_ledger, cut) == compare_rankings(public_ledger, offset)


def test_input_not_mutated_and_order_not_significant(public_ledger):
    original = deepcopy(public_ledger)
    expected = compare_rankings(public_ledger, "T2")
    assert public_ledger == original
    assert compare_rankings(list(reversed(public_ledger)), "T2") == expected
    assert compare_rankings(public_ledger, "2026-09-15T06:00:00-06:00") == expected


def test_missing_not_zero_and_single_branch_not_missing(small_ledger):
    unknown = company(compare_rankings(small_ledger, "T0"))["features"]["additional_branches"]
    assert unknown["value"] is None and unknown["status"] == "UNKNOWN"
    small_ledger.append(observation("TEST-BRANCH", "CO-A", "branch_count", 1))
    known = company(compare_rankings(small_ledger, "T0"))["features"]["additional_branches"]
    assert known["value"] == 0 and known["status"] == "OBSERVED"
    assert unknown["contribution"] == known["contribution"] == 0


def test_caps_and_distinct_neighbors():
    rows = [observation(f"TEST-N-{n}", f"CO-{n}", "display_name", f"Cuenta {n}") for n in range(7)]
    rows += [observation("TEST-B", "CO-0", "branch_count", 100)]
    rows += [claim(f"TEST-R-{n}", f"LINK-{n}", "CO-0", f"CO-{n}") for n in range(1, 7)]
    result = company(compare_rankings(rows, "T0"), "CO-0")
    assert result["baseline_score"] == 50 and result["graph_score"] == 70
    assert result["features"]["confirmed_neighbors"]["value"] == 6


def test_conflicting_branches_remain_unscored_even_after_confirmation(small_ledger):
    small_ledger += [
        observation("TEST-B1", "CO-A", "branch_count", 2),
        observation("TEST-B2", "CO-A", "branch_count", 3, status="CONFIRMED", cut="T1"),
    ]
    assert company(compare_rankings(small_ledger, "T0"))["baseline_score"] == 10
    result = company(compare_rankings(small_ledger, "T1"))
    feature = result["features"]["additional_branches"]
    assert result["baseline_score"] == 0
    assert feature["status"] == "CONFLICTED" and feature["value"] is None
    assert [row["value"] for row in feature["evidence"]] == [2, 3]


@pytest.mark.parametrize("status", ["INFERRED", "DISCARDED"])
def test_unusable_branch_verification_does_not_score(small_ledger, status):
    small_ledger.append(observation("TEST-B1", "CO-A", "branch_count", 4, status=status))
    result = company(compare_rankings(small_ledger, "T0"))
    assert result["baseline_score"] == 0
    assert result["features"]["additional_branches"]["status"] == "INSUFFICIENT_EVIDENCE"


def test_later_discarded_branch_does_not_reuse_earlier_report(small_ledger):
    small_ledger += [
        observation("TEST-B1", "CO-A", "branch_count", 4),
        observation("TEST-B2", "CO-A", "branch_count", 4, status="DISCARDED", cut="T1"),
    ]
    assert company(compare_rankings(small_ledger, "T0"))["baseline_score"] == 30
    assert company(compare_rankings(small_ledger, "T1"))["baseline_score"] == 0


def test_simultaneous_attribute_verification_conflict(small_ledger):
    small_ledger += [
        observation("TEST-B1", "CO-A", "branch_count", 4),
        observation("TEST-B2", "CO-A", "branch_count", 4, status="DISCARDED"),
    ]
    feature = company(compare_rankings(small_ledger, "T0"))["features"]["additional_branches"]
    assert feature["status"] == "VERIFICATION_CONFLICTED" and feature["contribution"] == 0


@pytest.mark.parametrize(
    "status,expected",
    [
        ("CONFIRMED", 5),
        ("REPORTED", 0),
        ("INFERRED", 0),
        ("DISCARDED", 0),
    ],
)
def test_relationship_states_preserved_not_promoted(small_ledger, status, expected):
    small_ledger.append(claim(status=status))
    report = compare_rankings(small_ledger, "T0")
    assert company(report)["graph_score"] == expected
    assert report["relationship_context"][0]["verification_status"] == status
    assert report["relationship_context"][0]["evidence"][0]["verification_status"] == status


def test_referral_is_context_even_when_confirmed(small_ledger):
    small_ledger.append(claim(kind="REFERS_TO"))
    report = compare_rankings(small_ledger, "T0")
    assert company(report)["graph_score"] == 0
    assert report["relationship_context"][0]["scoring_status"] == "NOT_ECONOMIC"


def test_discarded_relationship_only_changes_available_cut(small_ledger):
    small_ledger += [claim(), claim("TEST-DISCARD", status="DISCARDED", cut="T1")]
    assert company(compare_rankings(small_ledger, "T0"))["graph_score"] == 5
    report = compare_rankings(small_ledger, "T1")
    assert company(report)["graph_score"] == 0
    assert len(report["relationship_context"][0]["evidence"]) == 2


@pytest.mark.parametrize("separate_id", [False, True])
def test_contradictory_relationships_not_arbitrarily_chosen(small_ledger, separate_id):
    negative = claim(
        "TEST-NEGATIVE", subject="LINK-B" if separate_id else "LINK-A", status="DISCARDED"
    )
    # Mismo instante expresado con otra zona: debe seguir siendo una contradicción simultánea.
    negative["available_at"] = "2026-01-15T06:00:00-06:00"
    small_ledger += [claim(), negative]
    report = compare_rankings(small_ledger, "T0")
    assert company(report)["graph_score"] == 0
    assert all(row["scoring_status"] == "CONFLICTED" for row in report["relationship_context"])


def test_relationship_endpoint_change_is_not_arbitrated(small_ledger):
    small_ledger += [claim(), claim("TEST-CHANGED", right="CO-C", cut="T1")]
    report = compare_rankings(small_ledger, "T1")
    assert all(row["graph_score"] == 0 for row in report["companies"])
    assert report["relationship_context"][0]["verification_status"] == "CONFLICTED"


def test_duplicate_claims_and_directions_do_not_inflate_neighbors(small_ledger):
    small_ledger += [
        claim(),
        claim("TEST-REPEAT"),
        claim("TEST-DUPLICATE", subject="LINK-B"),
        claim("TEST-REVERSE", subject="LINK-C", left="CO-B", right="CO-A"),
        claim("TEST-PARTNER", subject="LINK-D", kind="PARTNERS_WITH"),
    ]
    report = compare_rankings(small_ledger, "T0")
    feature = company(report)["features"]["confirmed_neighbors"]
    assert feature["value"] == 1 and feature["contribution"] == 5
    assert len(feature["evidence"]) == 5
    assert len(report["relationship_context"]) == 4


def test_alias_candidates_not_fused_or_added_to_cohort(small_ledger):
    initial = compare_rankings(small_ledger, "T0")
    small_ledger += [
        observation("TEST-ALIAS", "REC-candidate", "alias_name", "Cuenta A", kind="SOURCE_RECORD")
    ]
    result = compare_rankings(small_ledger, "T0")
    assert result["companies"] == initial["companies"]
    assert result["top_k"] == initial["top_k"]
    assert result["identity_candidates"][0]["candidate_company_ids"] == ["CO-A"]
    assert result["identity_candidates"][0]["identity_status"] == "NEEDS_REVIEW"


@pytest.mark.parametrize(
    "value,status,excluded",
    [
        (True, "CONFIRMED", True),
        (True, "REPORTED", False),
        (True, "INFERRED", False),
        (True, "DISCARDED", False),
        (False, "CONFIRMED", False),
    ],
)
def test_service_eligibility_is_same_for_both_policies(small_ledger, value, status, excluded):
    small_ledger.append(observation("TEST-SERVICE", "CO-A", "service_active", value, status=status))
    report = compare_rankings(small_ledger, "T0")
    assert (len(report["excluded"]) == 1) is excluded
    for policy in ("baseline", "graph"):
        assert ("CO-A" not in report["top_k"][policy]) is excluded


def test_conflicting_service_does_not_claim_known_noncustomer(small_ledger):
    small_ledger += [
        observation("TEST-S1", "CO-A", "service_active", True, status="CONFIRMED"),
        observation("TEST-S2", "CO-A", "service_active", False, status="CONFIRMED"),
    ]
    report = compare_rankings(small_ledger, "T0")
    eligibility = company(report)["eligibility"]
    assert not report["excluded"]
    assert eligibility["status"] == "PENDING_COMMERCIAL_VALIDATION"
    assert eligibility["service_status"] == "CONFLICTED"


def test_excluded_clients_remain_known_neighbor_context(public_ledger):
    report = compare_rankings(public_ledger, "T2")
    excluded = {row["company_id"] for row in report["excluded"]}
    cafe = next(row for row in report["companies"] if row["display_name"] == "Café Jacaranda")
    assert any(
        row["company_id"] in excluded
        for row in cafe["features"]["confirmed_neighbors"]["neighbors"]
    )
    assert cafe["graph_score"] == 10


def test_ties_empty_and_insufficient_cohort(small_ledger):
    report = compare_rankings(small_ledger, "T0")
    assert report["top_k"]["baseline"] == ["CO-A", "CO-B", "CO-C"]
    assert report["comparison"]["unfilled_capacity"] == 2
    assert not report["comparison"]["baseline_boundary"]["crosses_tie"]
    empty = compare_rankings([], "T0")
    assert empty["comparison"]["unfilled_capacity"] == 5
    assert empty["top_k"] == {"baseline": [], "graph": []}
    assert "Ninguna" in render_comparison(empty)


def test_cutoff_tie_is_explicit(small_ledger):
    small_ledger += [
        observation(f"TEST-N-{key}", f"CO-{key}", "display_name", f"Cuenta {key}") for key in "DEF"
    ]
    report = compare_rankings(small_ledger, "T0")
    assert report["top_k"]["baseline"] == [f"CO-{key}" for key in "ABCDE"]
    assert report["comparison"]["baseline_boundary"]["crosses_tie"]
    assert len(report["comparison"]["baseline_boundary"]["tied_company_ids"]) == 6


def test_calculation_has_no_filesystem_access(public_ledger, monkeypatch):
    forbidden = Mock(side_effect=AssertionError("El scoring no debe abrir ningún archivo"))
    monkeypatch.setattr("builtins.open", forbidden)
    monkeypatch.setattr(Path, "open", forbidden)
    report = compare_rankings(public_ledger, "T2")
    assert report["eligible_companies"] == 21
    forbidden.assert_not_called()


@pytest.mark.parametrize("cut", CUTS)
def test_all_output_ids_are_known_at_cut_and_no_private_metadata(public_ledger, cut):
    known = {row["company_id"] for row in snapshot(public_ledger, cut)["companies"]}
    report = compare_rankings(public_ledger, cut)
    assert_no_private_fields(report)
    encoded = json.dumps(report)
    assert not any(token in encoded for token in ("EMP-", "REL-", "CLM-", "truth_reference"))

    def check(value):
        if isinstance(value, dict):
            for item in value.values():
                check(item)
        elif isinstance(value, list):
            for item in value:
                check(item)
        elif isinstance(value, str) and value.startswith("CO-"):
            assert value in known

    check(report)


def test_restricted_fields_and_duplicate_observation_ids_rejected(small_ledger):
    malformed = deepcopy(small_ledger)
    malformed[0]["truth_exists"] = True
    with pytest.raises(ValueError, match="restringidos"):
        compare_rankings(malformed, "T0")
    with pytest.raises(ValueError, match="duplicado"):
        compare_rankings([*small_ledger, small_ledger[0]], "T0")
