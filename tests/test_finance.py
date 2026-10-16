"""Identidades financieras y casos adversos sobre supuestos agregados, nunca empresas."""

from copy import deepcopy
from decimal import Decimal, localcontext
from pathlib import Path
from unittest.mock import Mock

import pytest

from economic_graph.finance import evaluate_scenario, financial_report, load_financial_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def assumptions():
    return load_financial_config(ROOT / "config/financial_assumptions.json")


def base(config):
    return next(case for case in config["scenarios"] if case["name"] == "base")


def set_amount(case, key, value):
    case[key]["value"] = str(value)


@pytest.mark.parametrize(
    "pools,expected",
    [
        (1, {"conservative": "-33900", "base": "-15450", "optimistic": "-5125", "null": "-16250"}),
        (
            100,
            {"conservative": "-123000", "base": "39000", "optimistic": "279500", "null": "-41000"},
        ),
    ],
)
def test_manual_arithmetic_regression_all_scenarios(assumptions, pools, expected):
    report = financial_report(assumptions)
    cases = [row for row in report["results"] if row["pools"] == pools]
    assert {row["scenario"]: row["net_present_value_mxn"] for row in cases} == expected
    assert all(row["slots"] == pools * 5 and not row["operational_authorization"] for row in cases)


def test_accounting_identity_no_double_cost_or_reserve(assumptions):
    result = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    assert result["baseline_selected_margin_mxn"] == "400000"
    assert result["graph_selected_margin_mxn"] == "480000"
    assert result["baseline_commercial_cost_mxn"] == "150000"
    assert result["graph_commercial_cost_mxn"] == "175000"
    assert result["commercial_cost_increment_mxn"] == "25000"
    assert result["net_present_value_mxn"] == "39000"
    assert result["reserve_mxn"] == "3200"
    assert result["net_after_reserve_mxn"] == "35800"
    assert result["maximum_fixed_and_operating_budget_mxn"] == "55000"


def test_shared_commercial_cost_cancels(assumptions):
    before = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    set_amount(base(assumptions), "baseline_commercial_cost_per_slot", 1300)
    after = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    assert after["net_present_value_mxn"] == before["net_present_value_mxn"]
    assert after["commercial_cost_increment_mxn"] == before["commercial_cost_increment_mxn"]


def test_unique_cost_splitting_preserves_totals(assumptions):
    case = base(assumptions)
    expected = evaluate_scenario(case, assumptions["settings"])
    extra = deepcopy(case["costs"][0])
    extra.update(cost_id="second_implementation_part")
    extra["amount"]["value"] = "4000"
    case["costs"][0]["amount"]["value"] = "6000"
    case["costs"].append(extra)
    assert evaluate_scenario(case, assumptions["settings"]) == expected


def test_reserve_not_expensed_twice(assumptions):
    normal = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    assumptions["settings"]["reserve_rate"] = "0.50"
    increased = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    assert normal["net_present_value_mxn"] == increased["net_present_value_mxn"]
    assert increased["reserve_mxn"] == "8000"
    assert increased["net_after_reserve_mxn"] == "31000"


@pytest.mark.parametrize(
    "pools,root,required", [(1, "0.40625", "0.48625"), (100, "0.01025", "0.01105")]
)
def test_break_even_and_strict_reserve_boundary(assumptions, pools, root, required):
    case, settings = base(assumptions), assumptions["settings"]
    report = evaluate_scenario(case, settings, pools)
    assert report["break_even"]["delta_rate"] == root
    assert report["required_with_reserve"]["delta_rate"] == required
    case["activation_rate_increment"] = root
    at_zero = evaluate_scenario(case, settings, pools)
    assert at_zero["net_present_value_mxn"] == "0" and at_zero["balance_status"] == "ZERO"
    case["activation_rate_increment"] = required
    at_reserve = evaluate_scenario(case, settings, pools)
    assert at_reserve["net_after_reserve_mxn"] == "0"
    assert not at_reserve["clears_reserve_mathematically"]
    case["activation_rate_increment"] = str(Decimal(required) + Decimal("0.00001"))
    assert evaluate_scenario(case, settings, pools)["clears_reserve_mathematically"]


def test_negative_zero_positive_without_cherry_picking(assumptions):
    case = base(assumptions)
    for delta, status in [("0", "NEGATIVE"), ("0.01025", "ZERO"), ("0.02", "POSITIVE")]:
        case["activation_rate_increment"] = delta
        result = evaluate_scenario(case, assumptions["settings"], 100)
        assert result["balance_status"] == status and not result["operational_authorization"]


def test_mandatory_null_preserves_costs_and_is_not_zero_profit(assumptions):
    rows = financial_report(assumptions, "hypothetical")["results"]
    null = next(row for row in rows if row["scenario"] == "null")
    normal = next(row for row in rows if row["scenario"] == "base")
    assert (
        null["activation_rate_increment"] == "0" and null["unselected_margin_increment_mxn"] == "0"
    )
    assert null["net_present_value_mxn"] == "-41000"
    for key in (
        "commercial_cost_increment_mxn",
        "fixed_incremental_cost_mxn",
        "operating_incremental_cost_mxn",
        "reserve_mxn",
    ):
        assert null[key] == normal[key]


@pytest.mark.parametrize("margin", ["0", "-8000"])
def test_nonpositive_margin_has_no_conversion_threshold(assumptions, margin):
    set_amount(base(assumptions), "contract_margin_per_activation", margin)
    result = evaluate_scenario(base(assumptions), assumptions["settings"])
    assert result["break_even"]["delta_rate"] is None
    assert result["break_even"]["feasibility"] == "NON_POSITIVE_MARGIN"


def test_unattainable_threshold_reported_not_clipped(assumptions):
    result = evaluate_scenario(assumptions["scenarios"][0], assumptions["settings"])
    assert result["break_even"]["delta_rate"] == "1.675"
    assert result["break_even"]["feasibility"] == "UNATTAINABLE"


@pytest.mark.parametrize(
    "field,value,match",
    [
        ("currency", "USD", "MXN"),
        ("capacity_per_pool", 10, "cinco"),
        ("capacity_per_pool", 5.0, "entero"),
        ("horizon_months", 0, "positivo"),
        ("horizon_months", True, "entero"),
        ("activation_window_days", -1, "positivo"),
        ("monthly_discount_rate", "1%", "inválido"),
        ("monthly_discount_rate", "NaN", "finito"),
        ("monthly_discount_rate", "-0.01", "fracción"),
        ("reserve_rate", "20", "fracción"),
    ],
)
def test_settings_reject_invalid_units_and_values(assumptions, field, value, match):
    assumptions["settings"][field] = value
    with pytest.raises(ValueError, match=match):
        financial_report(assumptions)


@pytest.mark.parametrize(
    "field,value",
    [
        ("baseline_activation_rate", "10"),
        ("baseline_activation_rate", "-0.1"),
        ("activation_rate_increment", "0.95"),
        ("activation_rate_increment", "-0.2"),
        ("activation_rate_increment", 0.02),
    ],
)
def test_invalid_probabilities_and_float_inputs_rejected(assumptions, field, value):
    base(assumptions)[field] = value
    with pytest.raises(ValueError):
        financial_report(assumptions)


@pytest.mark.parametrize("value", ["NaN", "Infinity", "-Infinity", "abc", "8,000", 8000])
def test_invalid_money_rejected(assumptions, value):
    base(assumptions)["contract_margin_per_activation"]["value"] = value
    with pytest.raises(ValueError):
        financial_report(assumptions)


@pytest.mark.parametrize("value", [0, -1, 1.0, True])
def test_invalid_volumes_cannot_divide_by_zero(assumptions, value):
    with pytest.raises(ValueError, match="entero positivo"):
        evaluate_scenario(base(assumptions), assumptions["settings"], value)


@pytest.mark.parametrize("field,value", [("horizon_months", 6), ("monthly_discount_rate", "0.02")])
def test_prevalued_money_cannot_silently_change_horizon_or_discount(assumptions, field, value):
    assumptions["settings"][field] = value
    with pytest.raises(ValueError, match="revalora"):
        financial_report(assumptions)


def test_activation_window_requires_consistent_source(assumptions):
    assumptions["settings"]["activation_window_days"] = 60
    with pytest.raises(ValueError, match="ventana"):
        financial_report(assumptions)


def test_monetary_unit_cannot_mix_total_and_per_slot(assumptions):
    base(assumptions)["incremental_commercial_cost_per_slot"]["unit"] = "MXN_total"
    with pytest.raises(ValueError, match="MXN_per_slot"):
        financial_report(assumptions)


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate_id",
        "unknown_category",
        "negative_cost",
        "missing_category",
        "commission_in_prospecting",
    ],
)
def test_cost_scope_and_duplicates_fail_closed(assumptions, mutation):
    case = base(assumptions)
    if mutation == "duplicate_id":
        case["costs"][1]["cost_id"] = case["costs"][0]["cost_id"]
    elif mutation == "unknown_category":
        case["costs"][1]["category"] = "commercial"
    elif mutation == "negative_cost":
        case["costs"][0]["amount"]["value"] = "-1"
    elif mutation == "missing_category":
        case["costs"].pop()
    else:
        case["commercial_cost_scope"] = "including_commission"
    with pytest.raises(ValueError):
        financial_report(assumptions)


def test_commercial_savings_cannot_make_total_cost_negative(assumptions):
    set_amount(base(assumptions), "incremental_commercial_cost_per_slot", -301)
    with pytest.raises(ValueError, match="no puede ser negativo"):
        financial_report(assumptions)


def test_flows_revalue_configurable_horizon_discount_and_window(assumptions):
    case, settings = deepcopy(base(assumptions)), deepcopy(assumptions["settings"])
    settings.update(horizon_months=2, activation_window_days=30, monthly_discount_rate="0.10")
    case.update(activation_window_days=30, activation_rate_increment="0.1")
    for key in (
        "contract_margin_per_activation",
        "baseline_commercial_cost_per_slot",
        "incremental_commercial_cost_per_slot",
        "unselected_margin_increment",
    ):
        case[key] = {
            "basis": "monthly_cashflows",
            "unit": case[key]["unit"],
            "values": ["0", "0", "0"],
        }
    case["contract_margin_per_activation"]["values"] = ["0", "110", "121"]
    for cost in case["costs"]:
        cost["amount"] = {"basis": "monthly_cashflows", "unit": "MXN_total", "values": ["0"] * 3}
    result = evaluate_scenario(case, settings)
    # 110/1.1 + 121/1.1² = 200; 5 × 0.1 × 200 = 100.
    assert result["contract_margin_per_activation_mxn"] == "200"
    assert result["net_present_value_mxn"] == "100"
    case["contract_margin_per_activation"]["values"].append("1")
    with pytest.raises(ValueError, match="exactamente mes 0 hasta H"):
        evaluate_scenario(case, settings)


def test_present_values_not_discounted_twice(assumptions):
    result = evaluate_scenario(base(assumptions), assumptions["settings"], 100)
    assert result["contract_margin_per_activation_mxn"] == "8000"
    assert result["operating_incremental_cost_mxn"] == "6000"


def test_precision_independent_of_callers_decimal_context(assumptions):
    expected = financial_report(assumptions, sensitivity=True)
    with localcontext() as context:
        context.prec = 6
        assert financial_report(assumptions, sensitivity=True) == expected


def test_sensitivity_covers_all_ranges_and_keeps_losses(assumptions):
    report = financial_report(assumptions, sensitivity=True)
    for analysis in report["sensitivity"].values():
        assert len(analysis["one_way"]) == 26
        assert len(analysis["rate_by_margin"]) == 15
        assert len(analysis["volume_by_cost"]) == 9
        values = [Decimal(row["result"]["net_present_value_mxn"]) for row in analysis["one_way"]]
        assert min(values) < 0
    assert (
        max(
            Decimal(row["result"]["net_present_value_mxn"])
            for row in report["sensitivity"]["hypothetical"]["one_way"]
        )
        > 0
    )


def test_infeasible_sensitivity_cells_explicit_not_silently_omitted(assumptions):
    base(assumptions)["baseline_activation_rate"] = "0.01"
    analysis = financial_report(assumptions, "demo", True)["sensitivity"]["demo"]
    assert len(analysis["rate_by_margin"]) == 15
    assert any(row.get("status") == "INVALID_RATE" for row in analysis["rate_by_margin"])
    assert any(row.get("status") == "INVALID_RATE" for row in analysis["one_way"])


@pytest.mark.parametrize(
    "mutation",
    ["missing_scenario", "duplicate_scenario", "unknown_field", "wrong_label", "raw_ledger"],
)
def test_contract_requires_all_scenarios_and_hypothetical_label(assumptions, mutation):
    if mutation == "missing_scenario":
        assumptions["scenarios"].pop()
    elif mutation == "duplicate_scenario":
        assumptions["scenarios"][2] = deepcopy(base(assumptions))
    elif mutation == "unknown_field":
        assumptions["actual_sales"] = 10
    elif mutation == "wrong_label":
        assumptions["assumption_status"] = "observed"
    else:
        assumptions = {"schema_version": "1.0", "observations": []}
    with pytest.raises(ValueError):
        financial_report(assumptions)


def test_no_mutation_no_files_no_experiment_claim(assumptions, monkeypatch):
    original = deepcopy(assumptions)
    blocked = Mock(side_effect=AssertionError("El calculador puro no lee datos ni archivos"))
    monkeypatch.setattr("builtins.open", blocked)
    monkeypatch.setattr(Path, "open", blocked)
    report = financial_report(assumptions, sensitivity=True)
    assert assumptions == original
    assert report["future_experiment"]["sample_size"] is None
    assert report["future_experiment"]["status"] == "future_methodological_design_only"
    assert not report["future_experiment"]["operational_authorization"]
    blocked.assert_not_called()
