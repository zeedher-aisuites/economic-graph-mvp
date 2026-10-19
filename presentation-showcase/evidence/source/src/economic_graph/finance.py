"""Aritmética financiera educativa: supuestos agregados, sin empresas, red ni resultados reales."""

import hashlib
import json
from copy import deepcopy
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, localcontext
from pathlib import Path

VERSION = "003b-finance-v1"
STATUS = "educational_uncalibrated"
DEFAULT_CONFIG = Path("config/financial_assumptions.json")
SCENARIOS = ("conservative", "base", "optimistic")
WARNING = (
    "Ejercicio hipotético no calibrado, exclusivamente para la PoC educativa. "
    "No representa datos observados de Totalplay ni de las 30 PyMEs. "
    "Un saldo positivo no valida causalidad ni autoriza inversión, contactos, piloto o despliegue."
)


def _fields(value: object, fields: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != fields:
        raise ValueError(f"{label}: campos incompletos o desconocidos.")


def _decimal(value: object, label: str) -> Decimal:
    # Exigir cadenas evita introducir redondeo binario desde números JSON float.
    if not isinstance(value, str):
        raise ValueError(f"{label}: usa una cadena decimal, por ejemplo '0.02', sin símbolo %.")
    try:
        result = Decimal(value)
        if not result.is_finite():
            raise InvalidOperation
    except InvalidOperation:
        raise ValueError(f"{label}: decimal finito inválido.") from None
    return result


def _positive_integer(value: object, label: str) -> int:
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label}: debe ser un entero positivo.")
    return value


def _settings(settings: dict) -> dict:
    _fields(
        settings,
        {
            "currency",
            "capacity_per_pool",
            "activation_window_days",
            "horizon_months",
            "monthly_discount_rate",
            "reserve_rate",
        },
        "settings",
    )
    if settings["currency"] != "MXN" or settings["capacity_per_pool"] != 5:
        raise ValueError("La PoC requiere MXN y capacidad de cinco plazas por bolsa.")
    result = deepcopy(settings)
    for key in ("capacity_per_pool", "activation_window_days", "horizon_months"):
        _positive_integer(result[key], key)
    for key in ("monthly_discount_rate", "reserve_rate"):
        result[key] = _decimal(result[key], key)
        if not 0 <= result[key] <= 1:
            raise ValueError(f"{key}: usa una fracción entre 0 y 1, no puntos porcentuales.")
    return result


def _money(spec: dict, unit: str, settings: dict) -> Decimal:
    if not isinstance(spec, dict) or spec.get("unit") != unit:
        raise ValueError(f"Importe: se requiere unidad {unit}.")
    if spec.get("basis") == "present_value":
        _fields(spec, {"unit", "basis", "value", "horizon_months", "monthly_discount_rate"}, unit)
        if (
            type(spec["horizon_months"]) is not int
            or spec["horizon_months"] != settings["horizon_months"]
            or _decimal(spec["monthly_discount_rate"], unit) != settings["monthly_discount_rate"]
        ):
            raise ValueError(
                "Valor presente incompatible con horizonte/descuento; revalora los importes."
            )
        # Ya descontado: volver a descontar aquí duplicaría el efecto financiero.
        return _decimal(spec["value"], unit)
    if spec.get("basis") == "monthly_cashflows":
        _fields(spec, {"unit", "basis", "values"}, unit)
        values = spec["values"]
        if not isinstance(values, list) or len(values) != settings["horizon_months"] + 1:
            raise ValueError("Flujos mensuales: incluye exactamente mes 0 hasta H, sin truncarlos.")
        return sum(
            (
                _decimal(value, unit) / (1 + settings["monthly_discount_rate"]) ** month
                for month, value in enumerate(values)
            ),
            Decimal(0),
        )
    raise ValueError("Importe: basis debe ser present_value o monthly_cashflows.")


def _scenario(scenario: dict, settings: dict) -> dict:
    money_units = {
        "contract_margin_per_activation": "MXN_per_activation",
        "baseline_commercial_cost_per_slot": "MXN_per_slot",
        "incremental_commercial_cost_per_slot": "MXN_per_slot",
        "unselected_margin_increment": "MXN_total",
    }
    _fields(
        scenario,
        set(money_units)
        | {
            "name",
            "activation_window_days",
            "baseline_activation_rate",
            "activation_rate_increment",
            "contract_margin_scope",
            "commercial_cost_scope",
            "costs",
        },
        "scenario",
    )
    if scenario["name"] not in (*SCENARIOS, "null"):
        raise ValueError("Escenario desconocido.")
    if (
        type(scenario["activation_window_days"]) is not int
        or scenario["activation_window_days"] != settings["activation_window_days"]
    ):
        raise ValueError("La ventana de las tasas/márgenes no coincide con settings.")
    if (
        scenario["contract_margin_scope"] != "net_of_service_installation_commission"
        or scenario["commercial_cost_scope"] != "prospecting_only"
    ):
        raise ValueError("Separar margen neto de servicio/alta/comisión y costo de prospección.")
    result = {key: _money(scenario[key], unit, settings) for key, unit in money_units.items()}
    result["name"] = scenario["name"]
    p = _decimal(scenario["baseline_activation_rate"], "baseline_activation_rate")
    delta = _decimal(scenario["activation_rate_increment"], "activation_rate_increment")
    if not 0 <= p <= 1 or not 0 <= p + delta <= 1:
        raise ValueError("Las probabilidades baseline y grafo deben estar entre 0 y 1.")
    result.update(baseline_activation_rate=p, activation_rate_increment=delta)
    if scenario["name"] == "null" and (delta != 0 or result["unselected_margin_increment"] != 0):
        raise ValueError("El escenario nulo requiere Δp=0 y ΔU=0.")
    if (
        result["baseline_commercial_cost_per_slot"] < 0
        or result["baseline_commercial_cost_per_slot"]
        + result["incremental_commercial_cost_per_slot"]
        < 0
    ):
        raise ValueError("El costo comercial total por plaza no puede ser negativo.")
    result.update(fixed_incremental_cost=Decimal(0), operating_incremental_cost=Decimal(0))
    seen, categories = set(), set()
    if not isinstance(scenario["costs"], list):
        raise ValueError("costs debe ser una lista con costos fijos y operativos explícitos.")
    for cost in scenario["costs"]:
        _fields(cost, {"cost_id", "category", "amount"}, "cost")
        identifier, category = cost["cost_id"], cost["category"]
        if not isinstance(identifier, str) or not identifier.strip() or identifier in seen:
            raise ValueError("cost_id vacío o duplicado: evitar doble contabilización.")
        if category not in ("fixed", "operating"):
            raise ValueError(
                "Solo costos incrementales fixed/operating; prospección se cuenta aparte."
            )
        amount = _money(cost["amount"], "MXN_total", settings)
        if amount < 0:
            raise ValueError(
                "Los costos fijos y operativos de esta versión deben ser no negativos."
            )
        seen.add(identifier)
        categories.add(category)
        result[f"{category}_incremental_cost"] += amount
    if categories != {"fixed", "operating"}:
        raise ValueError("Declarar costos fixed y operating, incluso cuando sean cero.")
    return result


def _threshold(cost: Decimal, slots: int, margin: Decimal, p: Decimal) -> dict:
    if margin <= 0:
        return {"delta_rate": None, "delta_pp": None, "feasibility": "NON_POSITIVE_MARGIN"}
    rate = cost / (slots * margin)
    feasibility = "ATTAINABLE"
    if rate > 1 - p:
        feasibility = "UNATTAINABLE"
    elif rate < -p:
        feasibility = "BELOW_MINIMUM_RATE"
    return {"delta_rate": rate, "delta_pp": rate * 100, "feasibility": feasibility}


def _evaluate(scenario: dict, settings: dict, pools: int) -> dict:
    pools = _positive_integer(pools, "pools")
    slots = pools * settings["capacity_per_pool"]
    p, delta = scenario["baseline_activation_rate"], scenario["activation_rate_increment"]
    margin = scenario["contract_margin_per_activation"]
    commercial_base = slots * scenario["baseline_commercial_cost_per_slot"]
    commercial_graph = commercial_base + slots * scenario["incremental_commercial_cost_per_slot"]
    fixed, operating = scenario["fixed_incremental_cost"], scenario["operating_incremental_cost"]
    commercial_delta = commercial_graph - commercial_base
    unselected = scenario["unselected_margin_increment"]
    selected_delta = slots * delta * margin
    net = selected_delta - commercial_delta + unselected - fixed - operating
    reserve = settings["reserve_rate"] * (fixed + operating)
    threshold_cost = commercial_delta + fixed + operating - unselected
    return {
        "scenario": scenario["name"],
        "pools": pools,
        "capacity_per_pool": 5,
        "slots": slots,
        "baseline_activation_rate": p,
        "graph_activation_rate": p + delta,
        "activation_rate_increment": delta,
        "contract_margin_per_activation_mxn": margin,
        "baseline_selected_margin_mxn": slots * p * margin,
        "graph_selected_margin_mxn": slots * (p + delta) * margin,
        "selected_margin_increment_mxn": selected_delta,
        "baseline_commercial_cost_mxn": commercial_base,
        "graph_commercial_cost_mxn": commercial_graph,
        "commercial_cost_increment_mxn": commercial_delta,
        "unselected_margin_increment_mxn": unselected,
        "fixed_incremental_cost_mxn": fixed,
        "operating_incremental_cost_mxn": operating,
        "net_present_value_mxn": net,
        "balance_status": "POSITIVE" if net > 0 else "NEGATIVE" if net < 0 else "ZERO",
        "reserve_mxn": reserve,
        "net_after_reserve_mxn": net - reserve,
        "clears_reserve_mathematically": net > reserve,
        "break_even": _threshold(threshold_cost, slots, margin, p),
        "required_with_reserve": _threshold(threshold_cost + reserve, slots, margin, p),
        "maximum_fixed_and_operating_budget_mxn": selected_delta - commercial_delta + unselected,
        "operational_authorization": False,
    }


def _plain(value):
    if isinstance(value, Decimal):
        if value == 0:
            return "0"
        text = format(value, "f")
        return text.rstrip("0").rstrip(".") if "." in text else text
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_plain(item) for item in value]
    return value


def evaluate_scenario(scenario: dict, settings: dict, pools: int = 1) -> dict:
    """Una campaña agregada; cadenas decimales y precisión interna de 50 cifras."""
    with localcontext() as context:
        context.prec, context.rounding = 50, ROUND_HALF_EVEN
        validated = _settings(settings)
        return _plain(_evaluate(_scenario(scenario, validated), validated, pools))


def load_financial_config(path: Path = DEFAULT_CONFIG) -> dict:
    def unique_fields(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Clave JSON duplicada.")
            result[key] = value
        return result

    try:
        return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_fields)
    except (OSError, ValueError):
        raise ValueError(
            "No se puede leer la configuración financiera JSON UTF-8; revisa ruta, sintaxis "
            "y claves duplicadas."
        ) from None


def _sensitivity(base: dict, settings: dict, pools: int) -> dict:
    ranges = {
        "activation_rate_increment": ["-0.02", "0", "0.01", "0.02", "0.05"],
        "contract_margin_per_activation": ["4000", "8000", "12000"],
        "incremental_commercial_cost_per_slot": ["25", "50", "100"],
        "fixed_incremental_cost": ["5000", "10000", "20000"],
        "operating_incremental_cost": ["3000", "6000", "12000"],
        "unselected_margin_increment": ["-1000", "0", "1000"],
        "reserve_rate": ["0", "0.20", "0.50"],
        "pools": [1, 10, 100],
    }
    one_way, rate_margin, volume_cost = [], [], []
    for parameter, values in ranges.items():
        for value in values:
            case, case_settings, volume = deepcopy(base), deepcopy(settings), pools
            if parameter == "pools":
                volume = value
            elif parameter == "reserve_rate":
                case_settings[parameter] = Decimal(value)
            else:
                case[parameter] = Decimal(value)
            # Conservar como inválidas las variaciones que excedan probabilidades posibles.
            p = case["baseline_activation_rate"] + case["activation_rate_increment"]
            if not 0 <= p <= 1:
                one_way.append({"parameter": parameter, "value": value, "status": "INVALID_RATE"})
                continue
            one_way.append(
                {
                    "parameter": parameter,
                    "value": value,
                    "result": _evaluate(case, case_settings, volume),
                }
            )
    for rate in ranges["activation_rate_increment"]:
        for margin in ranges["contract_margin_per_activation"]:
            case = {
                **base,
                "activation_rate_increment": Decimal(rate),
                "contract_margin_per_activation": Decimal(margin),
            }
            if 0 <= case["baseline_activation_rate"] + case["activation_rate_increment"] <= 1:
                rate_margin.append(_evaluate(case, settings, pools))
            else:
                rate_margin.append(
                    {
                        "activation_rate_increment": rate,
                        "contract_margin_per_activation_mxn": margin,
                        "status": "INVALID_RATE",
                    }
                )
    for volume in ranges["pools"]:
        for factor in (Decimal("0.5"), Decimal(1), Decimal(2)):
            case = {
                **base,
                "fixed_incremental_cost": base["fixed_incremental_cost"] * factor,
                "operating_incremental_cost": base["operating_incremental_cost"] * factor,
            }
            volume_cost.append({"cost_factor": factor, "result": _evaluate(case, settings, volume)})
    return {
        "one_way": one_way,
        "rate_by_margin": rate_margin,
        "volume_by_cost": volume_cost,
        "warning": "Rangos exploratorios, no intervalos de confianza. Al variar volumen, costos "
        "constantes solo aíslan su efecto; no son cotizaciones a escala. H y descuento "
        "requieren revalorar los importes o aportar flujos mensuales compatibles.",
    }


def financial_report(config: dict, scope: str = "both", sensitivity: bool = False) -> dict:
    """Tres escenarios y nulo obligatorio; cinco y 500 plazas separados del experimento."""
    _fields(config, {"schema_version", "assumption_status", "settings", "scenarios"}, "config")
    if config["schema_version"] != VERSION or config["assumption_status"] != STATUS:
        raise ValueError("Contrato financiero o etiqueta educativa no calibrada inválidos.")
    if scope not in {"demo", "hypothetical", "both"}:
        raise ValueError("scope debe ser demo, hypothetical o both.")
    with localcontext() as context:
        context.prec, context.rounding = 50, ROUND_HALF_EVEN
        settings = _settings(config["settings"])
        if not isinstance(config["scenarios"], list):
            raise ValueError("scenarios debe ser una lista.")
        cases = [_scenario(item, settings) for item in config["scenarios"]]
        if len(cases) != 3 or {case["name"] for case in cases} != set(SCENARIOS):
            raise ValueError("Incluir conservative, base y optimistic exactamente una vez.")
        cases = sorted(cases, key=lambda case: SCENARIOS.index(case["name"]))
        base = cases[1]
        cases.append(
            {
                **base,
                "name": "null",
                "activation_rate_increment": Decimal(0),
                "unselected_margin_increment": Decimal(0),
            }
        )
        volumes = {"demo": 1, "hypothetical": 100}
        results = []
        analyses = {}
        for name, pools in volumes.items():
            if scope != "both" and scope != name:
                continue
            results.extend({"scope": name, **_evaluate(case, settings, pools)} for case in cases)
            if sensitivity:
                analyses[name] = _sensitivity(base, settings, pools)
        canonical = json.dumps(config, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return _plain(
            {
                "schema_version": VERSION,
                "assumption_status": STATUS,
                "warning": WARNING,
                "settings": settings,
                "input_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
                "results": results,
                "sensitivity": analyses,
                "zero_balance_reference": [
                    {
                        "scope": row["scope"],
                        "delta_rate": row["break_even"]["delta_rate"],
                        "feasibility": row["break_even"]["feasibility"],
                        "net_present_value_mxn": "0",
                        "definition": "Identidad algebraica ΔV=0; "
                        "no es un efecto observado. Una tasa decimal periódica es aproximada.",
                    }
                    for row in results
                    if row["scenario"] == "base" and row["break_even"]["delta_rate"] is not None
                ],
                "future_experiment": {
                    "status": "future_methodological_design_only",
                    "randomization": "1:1 por bolsas independientes",
                    "capacity_per_pool": 5,
                    "confidence_level": "0.95",
                    "target_power": "0.80",
                    "sample_size": None,
                    "inference": "Inviable sin suficientes bolsas independientes; faltan varianza, "
                    "correlación intrabolsa y datos comerciales.",
                    "operational_authorization": False,
                },
            }
        )


def render_financial_report(report: dict) -> str:
    def money(value) -> str:
        return f"{Decimal(value):.2f}"

    labels = {
        "conservative": "Conservador",
        "base": "Base",
        "optimistic": "Optimista",
        "null": "Nulo",
    }
    lines = [
        "# Calculador financiero educativo — 003B",
        "",
        report["warning"],
        "",
        f"Moneda: MXN nominales; ventana: {report['settings']['activation_window_days']} días; "
        f"H: {report['settings']['horizon_months']} meses; descuento mensual: "
        f"{Decimal(report['settings']['monthly_discount_rate']) * 100}%. "
        "Todos los importes están en valor presente a la asignación.",
        "",
    ]
    for scope, title in (
        ("demo", "Demostración: cinco plazas"),
        ("hypothetical", "Escenario hipotético: 500 plazas"),
    ):
        rows = [row for row in report["results"] if row["scope"] == scope]
        if not rows:
            continue
        lines.extend(
            [
                f"## {title}",
                "",
                "| Escenario | Δ conversión (pp) | Δ margen seleccionado | "
                "Δ costo comercial | Δ margen resto | F + O | Saldo neto | Reserva | "
                "Saldo tras reserva | Equilibrio (pp) |",
                "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for row in rows:
            threshold = row["break_even"]["delta_pp"]
            threshold_label = (
                format(Decimal(threshold), ".6f") if threshold is not None else ("No definido")
            )
            if row["break_even"]["feasibility"] == "UNATTAINABLE":
                threshold_label += " (inviable)"
            total_cost = Decimal(row["fixed_incremental_cost_mxn"]) + Decimal(
                row["operating_incremental_cost_mxn"]
            )
            lines.append(
                f"| {labels[row['scenario']]} | "
                f"{Decimal(row['activation_rate_increment']) * 100} | "
                f"{money(row['selected_margin_increment_mxn'])} | "
                f"{money(row['commercial_cost_increment_mxn'])} | "
                f"{money(row['unselected_margin_increment_mxn'])} | "
                f"{money(total_cost)} | "
                f"{money(row['net_present_value_mxn'])} | {money(row['reserve_mxn'])} | "
                f"{money(row['net_after_reserve_mxn'])} | "
                f"{threshold_label} |"
            )
        reference = next(
            (item for item in report["zero_balance_reference"] if item["scope"] == scope), None
        )
        if reference:
            lines.extend(
                [
                    "",
                    "Referencia base de saldo nulo: ΔV = 0 por definición en "
                    f"Δp = {Decimal(reference['delta_rate']) * 100} pp; "
                    "no es conversión observada.",
                ]
            )
        lines.append("")
    lines.extend(
        [
            "El escenario nulo tiene Δp=0 y ΔU=0, conserva los costos base y puede perder dinero. "
            "La reserva es un colchón, no un gasto adicional del saldo neto. "
            "Los importes de tabla se redondean a centavos; JSON conserva más precisión.",
            "",
        ]
    )
    for scope, analysis in report["sensitivity"].items():
        lines.extend(
            [
                f"## Sensibilidad base — {scope}",
                "",
                analysis["warning"],
                "",
                "| Parámetro | Valor | Plazas | Saldo neto MXN | Saldo tras reserva MXN |",
                "|---|---:|---:|---:|---:|",
            ]
        )
        for item in analysis["one_way"]:
            row = item.get("result")
            lines.append(
                f"| {item['parameter']} | {item['value']} | "
                + (
                    f"{row['slots']} | {money(row['net_present_value_mxn'])} | "
                    f"{money(row['net_after_reserve_mxn'])} |"
                    if row
                    else "— | Tasa inválida | — |"
                )
            )
        lines.extend(["", "Los cruces Δp × margen y volumen × costos están en la salida JSON.", ""])
    lines.extend(
        [
            "## Protocolo experimental futuro",
            "",
            "Diseño 1:1 por bolsas independientes, KPI de margen neto comercial por cuenta "
            "elegible asignada, ITT, IC bilateral 95% y potencia objetivo 80%. Sin muestra "
            "calculada ni experimento ejecutado. Cinco o 500 plazas financieras no acreditan "
            "bolsas suficientes para inferencia causal.",
            "",
            f"Versión: `{VERSION}`; SHA-256 de supuestos: `{report['input_sha256']}`.",
        ]
    )
    return "\n".join(lines) + "\n"
