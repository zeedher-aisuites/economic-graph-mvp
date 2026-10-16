"""Control Tower local: presentación de evidencia observable y escenarios educativos."""

import json
from decimal import Decimal
from pathlib import Path

import streamlit as st

from economic_graph.contracts import CUTS, parse_time
from economic_graph.finance import financial_report, load_financial_config
from economic_graph.observable import load_observations
from economic_graph.tower_read_model import (
    STATES,
    TYPES,
    account_detail,
    atlas_context,
    build_context,
    funnel,
    network_data,
    network_spec,
    ranking_table,
    sector,
    segment_ids,
)

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/observable/observations.json"
FINANCE = ROOT / "config/financial_assumptions.json"
PAGES = ["Resumen", "Graph Health", "AI Performance", "Business Funnel", "Economic Impact"]
SCENARIOS = {
    "conservative": "Conservador",
    "base": "Base",
    "optimistic": "Optimista",
    "null": "Nulo",
}


def table(rows: list[dict]) -> None:
    if rows:
        st.dataframe(rows, hide_index=True, width="stretch", row_height=32)
    else:
        st.info("Sin registros para esta selección.")


def money(value: str) -> str:
    return f"${Decimal(value):,.2f} MXN"


def signed_money(value: str) -> str:
    amount = Decimal(value)
    return f"{'−' if amount < 0 else '+' if amount > 0 else ''}${abs(amount):,.0f}"


def scenario_cards(report: dict, scope: str) -> None:
    rows = [row for row in report["results"] if row["scope"] == scope]
    for column, row in zip(st.columns(len(rows)), rows, strict=True):
        with column.container(border=True):
            st.markdown(f"**{SCENARIOS[row['scenario']]}**")
            st.markdown(f"### {signed_money(row['net_present_value_mxn'])}")
            st.caption("Saldo neto hipotético · MXN")
            st.caption(f"Reserva: {money(row['reserve_mxn'])}")
            st.write(f"Tras reserva: **{signed_money(row['net_after_reserve_mxn'])}**")


def selection_headline(context: dict) -> None:
    report = context["ranking"]
    changed = len(report["comparison"]["entered_graph"])
    capacity = report["policy"]["capacity"]
    st.markdown(f"### El grafo modifica {changed} de las {capacity} selecciones comerciales")
    st.caption(
        "Misma cohorte y capacidad. Cambiar la selección no demuestra mayores ventas "
        "ni autoriza contactos."
    )


def reset_segment() -> None:
    st.session_state["company"] = None
    st.session_state["industry"] = "Todas"


def comparison_chart(context: dict, ids: set) -> None:
    report = context["ranking"]
    top = report["top_k"]
    shown = (set(top["baseline"]) | set(top["graph"])) & ids
    companies = [row for row in report["companies"] if row["company_id"] in shown]
    companies.sort(
        key=lambda row: (min(row["baseline_position"], row["graph_position"]), row["company_id"])
    )
    if not companies:
        st.info("El segmento no contiene cuentas de los top-5 globales.")
        return
    data = []
    names = {row["company_id"]: row["display_name"] or row["company_id"] for row in companies}
    for row in companies:
        shared = row["company_id"] in report["comparison"]["shared"]
        for policy, label in (("baseline", "Baseline"), ("graph", "Con grafo")):
            selected = row["company_id"] in top[policy]
            data.append(
                {
                    "ID": row["company_id"],
                    "Empresa": names[row["company_id"]],
                    "Política": label,
                    "Selección": "Compartida"
                    if shared
                    else ("Entra con grafo" if policy == "graph" else "Solo baseline")
                    if selected
                    else "Fuera del top-5",
                    "Etiqueta": f"#{row[f'{policy}_position']} · {row[f'{policy}_score']} puntos"
                    if selected
                    else "—",
                }
            )
    st.vega_lite_chart(
        spec={
            "data": {"values": data},
            "height": len(companies) * 34,
            "encoding": {
                "y": {
                    "field": "ID",
                    "type": "nominal",
                    "sort": list(names),
                    "title": None,
                    "axis": {
                        "labelExpr": f"({json.dumps(names)})[datum.label]",
                        "labelLimit": 230,
                        "labelFontSize": 13,
                        "labelOverlap": False,
                    },
                },
                "x": {
                    "field": "Política",
                    "type": "nominal",
                    "sort": ["Baseline", "Con grafo"],
                    "title": None,
                    "axis": {"orient": "top", "labelAngle": 0},
                },
            },
            "layer": [
                {
                    "mark": {
                        "type": "rect",
                        "cornerRadius": 4,
                        "stroke": "white",
                        "strokeWidth": 3,
                    },
                    "encoding": {
                        "color": {
                            "field": "Selección",
                            "type": "nominal",
                            "scale": {
                                "domain": [
                                    "Compartida",
                                    "Solo baseline",
                                    "Entra con grafo",
                                    "Fuera del top-5",
                                ],
                                "range": ["#dbeafe", "#e2e8f0", "#ccfbf1", "#f8fafc"],
                            },
                            "legend": {"orient": "bottom", "title": None},
                        }
                    },
                },
                {
                    "mark": {"type": "text", "color": "#0f172a", "fontSize": 13},
                    "encoding": {
                        "text": {"field": "Etiqueta"},
                        "tooltip": [
                            {"field": field}
                            for field in ("Empresa", "Política", "Selección", "Etiqueta")
                        ],
                    },
                },
            ],
            "config": {"view": {"stroke": None}},
        },
        width="stretch",
        alt="Selección baseline frente a grafo: compartidas, entradas y salidas.",
    )


def evidence_table(rows: list[dict]) -> None:
    table(
        [
            {**row, "value": json.dumps(row["value"], ensure_ascii=False, sort_keys=True)}
            for row in rows
        ]
    )


def company_detail(context: dict, selected: str | None) -> None:
    if selected is None:
        st.caption("Selecciona una empresa en la barra lateral para abrir su ficha y conexiones.")
        return
    detail = account_detail(context, selected)
    if detail is None:
        st.info("No conocida al corte.")
        return
    company, rank = detail["company"], detail["ranking"]
    st.subheader(f"Ficha · {company['attributes']['display_name']['value'] or selected}")
    st.caption(f"{sector(company)} · Identidad pendiente de revisión, sin fusión automática")
    st.write(
        "**Elegibilidad:** "
        + (
            "Por validar comercialmente"
            if rank["eligibility"]["eligible"]
            else "Excluida: servicio activo confirmado"
        )
    )
    if rank["eligibility"]["eligible"]:
        a, b, c, d = st.columns(4)
        a.metric("Score baseline", rank["baseline_score"])
        b.metric("Score grafo", rank["graph_score"])
        c.metric("Posición baseline global", rank["baseline_position"])
        d.metric("Posición grafo global", rank["graph_position"])
        table(
            [
                {
                    "Señal": "Sucursales adicionales"
                    if name == "additional_branches"
                    else "Vecinos confirmados",
                    "Estado": feature["status"],
                    "Aporte": feature["contribution"],
                }
                for name, feature in rank["features"].items()
            ]
        )
        with st.expander("Auditar contribuciones, reglas y evidencias"):
            st.json(rank)
    else:
        st.info(
            "Servicio activo confirmado: excluida del ranking de adquisición. Score no aplicable."
        )
    with st.expander("Atributos y conflictos sin arbitraje"):
        table(
            [
                {
                    "Atributo": name,
                    "Estado": attribute["status"],
                    "Valor": json.dumps(attribute["value"], ensure_ascii=False),
                    "Observaciones": ", ".join(attribute["observation_ids"]),
                }
                for name, attribute in company["attributes"].items()
            ]
        )
    with st.expander("Identidades candidatas · sin fusión"):
        table(detail["candidates"])
    with st.expander("Procedencia e historia de la cuenta y sus vínculos"):
        st.caption(
            "Conserva repeticiones, conflictos, estados y las tres fechas de cada observación."
        )
        evidence_table(detail["observations"])


def top_tables(context: dict, ids: set) -> None:
    rows = ranking_table(context, ids)
    for column, policy, title in zip(
        st.columns(2),
        ("baseline", "graph"),
        ("Selección tradicional · baseline", "Selección con grafo"),
        strict=True,
    ):
        with column:
            st.markdown(f"**{title}**")
            label = "baseline" if policy == "baseline" else "grafo"
            selected = set(context["ranking"]["top_k"][policy])
            table(
                sorted(
                    [
                        {
                            "Empresa": row["Empresa"],
                            "Posición global": row[f"Posición {label}"],
                            "Puntos": row[f"Score {label}"],
                        }
                        for row in rows
                        if row["ID"] in selected
                    ],
                    key=lambda row: row["Posición global"],
                )
            )
    st.caption("Top-5 global intersectado con el segmento; no se rellenan plazas al filtrar.")


def summary_page(context: dict, ids: set, finance: dict | None) -> None:
    summary, report = context["summary"], context["ranking"]
    selection_headline(context)
    a, b, c, d = st.columns(4)
    a.metric("Empresas conocidas · global", summary["companies"])
    b.metric("Afirmaciones económicas · global", summary["relationship_claims"])
    c.metric("Cuentas elegibles · global", report["eligible_companies"])
    d.metric("Cambios en cinco plazas · global", len(report["comparison"]["entered_graph"]))
    st.caption(
        "Sintético observable · Afirmaciones no implica confirmación. "
        f"Referencias separadas: {summary['referrals']}; cinco cuentas por investigar."
    )
    top_tables(context, ids)
    st.subheader("Potencial hipotético · 500 plazas")
    if finance:
        scenario_cards(finance, "hypothetical")
        st.caption(
            "Hipótesis educativas no calibradas, independientes del corte y segmento. "
            "Cinco plazas y sus pérdidas se muestran en Economic Impact. "
            "Ningún saldo autoriza invertir."
        )
    else:
        st.warning("Caso económico no disponible: revisa su archivo de supuestos aprobado.")
    st.subheader("Qué falta comprobar")
    st.write(
        "Contactos, oportunidades, activaciones y ventas: **No observado**. "
        "Faltan cobertura, identidad fuerte, permiso de contacto, costos y márgenes reales. "
        "El experimento futuro deberá medir margen neto por cuenta asignada, con control y "
        "bolsas independientes suficientes. No se ha ejecutado."
    )
    company_detail(context, next(iter(ids)) if len(ids) == 1 else None)


def health_page(context: dict, ids: set, selected: str | None) -> None:
    summary = context["summary"]
    a, b, c = st.columns(3)
    a.metric("Observaciones · global", summary["observations"])
    b.metric("Atributos en conflicto · global", summary["conflicted_attributes"])
    c.metric("Registros candidatos · global", summary["identity_candidates"])
    st.caption(
        "Sintético observable · Los candidatos no son duplicados confirmados ni se fusionan."
    )
    st.subheader("Red económica al corte")
    network = network_data(context, ids, focus_id=selected)
    if network["nodes"]:
        st.vega_lite_chart(
            spec=network_spec(network),
            width="stretch",
            alt="Red observable: empresas, vínculos y estados; detalle tabular debajo.",
        )
    else:
        st.info("Sin empresas en el segmento.")
    st.caption(
        "Gruesa: respalda vecinos confirmados de la cuenta; fina: evidencia de contexto. "
        "Continua: confirmada; trazos: reportada; puntos: inferida. Referencias no puntúan."
        if selected
        else "Red completa del segmento. Selecciona Empresa y vecinos para "
        "ver qué vínculos respaldan el score de una cuenta."
    )
    with st.expander("Cómo interpretar la red"):
        st.write(
            "Los vecinos se deduplican y los topes de la política siguen vigentes. "
            "Color indica tipo de vínculo; círculo: confirmado utilizable, rombo: sin "
            "confirmado utilizable, cuadrado: sin vínculo económico observado. "
            "Layout decorativo sin distancia comercial; los vecinos de contexto pueden "
            "estar fuera del sector. Más de diez nodos usan nombres en hover/tablas."
        )
    if network["edges"]:
        connections = [
            {
                "Empresa vinculada": row["to_name"]
                if row["from"] == selected
                else row["from_name"]
                if selected
                else f"{row['from_name']} → {row['to_name']}",
                "Vínculo · verificación": f"{row['type']} · {row['status']}",
                "Señal de la cuenta": "Respalda vecinos confirmados"
                if row["supports_focus"]
                else "Contexto · no suma puntos"
                if selected
                else "Ver ficha de cuenta",
            }
            for row in network["edges"]
        ]
        if selected:
            st.table(connections)
        else:
            with st.expander("Conexiones observadas de la red completa"):
                st.table(connections)
    else:
        st.info("Sin conexiones observadas en esta selección.")
    with st.expander("Ficha de cuenta y respaldo completo"):
        company_detail(context, selected)
    with st.expander("Auditar vínculos y filtrar evidencia"):
        source = st.selectbox(
            "Fuente de evidencia · solo inspección", ["Todas", *sorted(context["sources"])]
        )
        relation_type = st.selectbox(
            "Tipo de vínculo · solo inspección", ["Todos", *TYPES.values()]
        )
        status = st.selectbox("Verificación · solo inspección", ["Todas", *STATES.values()])
        inspected = [
            row
            for row in network["edges"]
            if (relation_type == "Todos" or row["type"] == relation_type)
            and (status == "Todas" or row["status"] == status)
        ]
        if source != "Todas":
            inspected = [row for row in inspected if source in row["source"].split(", ")]
        st.caption(
            "Estos tres controles inspeccionan tablas, "
            "sin ocultar evidencia de entrada al grafo o score."
        )
        table(
            [
                {
                    "Desde": row["from_name"],
                    "Hacia": row["to_name"],
                    "Tipo": row["type"],
                    "Verificación": row["status"],
                    "Diagnóstico scoring": row["scoring_status"],
                    "Fuentes": row["source"],
                    "Observaciones": row["evidence"],
                    "Vínculo": row["id"],
                }
                for row in inspected
            ]
        )
    with st.expander("Nodos aislados y evidencia insuficiente"):
        table(
            [
                {
                    "Empresa": node["name"],
                    "Sector": node["sector"],
                    "Estado": node["state"],
                    "Alcance": node["scope"],
                }
                for node in network["nodes"]
                if node["state"] != "Con vínculo confirmado utilizable"
            ]
        )
    with st.expander("Evolución global al corte"):
        st.subheader("Evolución global · solo cortes ya disponibles")
        evolution = [
            {
                "Corte": row["Corte"],
                "Empresas": row["companies"],
                "Observaciones": row["observations"],
                "Afirmaciones económicas": row["relationship_claims"],
            }
            for row in context["evolution"]
        ]
        table(evolution)
        st.bar_chart(evolution, x="Corte", y=["Empresas", "Afirmaciones económicas"], stack=False)
    with st.expander("Estados, fuentes y frescura globales"):
        table(
            [
                {"Estado de afirmación": key, "Cantidad": value}
                for key, value in context["states"].items()
            ]
        )
        table(
            [{"Fuente": key, "Observaciones": value} for key, value in context["sources"].items()]
        )
        ages = sorted(
            (parse_time(context["view"]["as_of"]) - parse_time(row["observed_at"])).total_seconds()
            / 86400
            for row in context["view"]["observations"]
        )
        if ages:
            from statistics import median

            st.write(
                f"Edad mediana desde observed_at: {median(ages):.1f} días; "
                f"n={len(ages)}. Sin SLA aprobado."
            )
    with st.expander("Conflictos e identidades candidatas · global"):
        st.json(
            {"conflicts": context["view"]["conflicts"], "identities": context["view"]["identities"]}
        )


def performance_page(context: dict, ids: set, selected: str | None) -> None:
    st.info(
        "Comparación de reglas explicables, sin modelo predictivo entrenado. "
        "Puntos ≠ probabilidades."
    )
    report, coverage = context["ranking"], context["coverage"]
    selection_headline(context)
    shared, replaced = st.columns(2)
    shared.metric("Cuentas compartidas · global", len(report["comparison"]["shared"]))
    replaced.metric("Sustituciones · global", len(report["comparison"]["entered_graph"]))
    comparison_chart(context, ids)
    st.caption(
        "Posiciones y puntos globales. El segmento solo intersecta los top-5; no rellena plazas."
    )
    case = next(
        (
            row
            for row in report["companies"]
            if row["company_id"] in ids
            and (
                row["company_id"] == selected
                if selected
                else row["display_name"] == "Café Jacaranda"
            )
        ),
        None,
    )
    if case:
        st.subheader(f"Caso explicable · {case['display_name']}")
        feature = case["features"]["confirmed_neighbors"]
        st.write(
            f"Posición baseline **{case['baseline_position']}** → con grafo "
            f"**{case['graph_position']}**. {feature['value']} vecinos confirmados utilizables "
            f"respaldan **{feature['contribution']} puntos** relacionales. "
            "Sin atribución de ventas."
        )
    denominator = coverage["denominator"]
    a, b = st.columns(2)
    a.metric(
        "Cobertura individual · global",
        f"{coverage['branches']}/{denominator}" if denominator else "No aplica",
    )
    b.metric(
        "Señal relacional utilizable · global",
        f"{coverage['neighbors']}/{denominator}" if denominator else "No aplica",
    )
    st.caption(
        "Denominador: elegibles. Cobertura individual incluye valores observados "
        "de una sucursal con cero puntos."
    )
    with st.expander("Auditar ranking, empates y filtros de score"):
        comparison = report["comparison"]
        st.write(
            f"**Global:** {len(comparison['shared'])} cuentas compartidas; "
            f"{len(comparison['entered_graph'])} entran con grafo y "
            f"{len(comparison['left_baseline'])} salen del baseline."
        )
        for policy, title in (("baseline", "baseline"), ("graph", "grafo")):
            boundary = comparison[f"{policy}_boundary"]
            st.write(
                f"Empate que cruza el límite {title}: "
                f"**{'Sí' if boundary['crosses_tie'] else 'No'}**. "
                f"Desempate por ID público; {len(boundary['tied_company_ids'])} "
                "cuentas con puntos de frontera."
            )
        score_policy = st.selectbox("Score para inspeccionar tabla", ["grafo", "baseline"])
        all_rows = ranking_table(context, ids)
        minimum = st.number_input("Score mínimo · solo tabla", min_value=0, value=0, step=1)
        table([row for row in all_rows if row[f"Score {score_policy}"] >= minimum])
        st.caption(
            "Posiciones y selección globales intactas. No disponibles: precision, recall, lift, "
            "calibración y drift validado; faltan etiquetas."
        )
    company_detail(context, selected)


def funnel_page(context: dict, ids: set, selected: str | None) -> None:
    policy = st.selectbox(
        "Política mostrada",
        ["graph", "baseline"],
        format_func=lambda value: "Con grafo" if value == "graph" else "Baseline",
    )
    rows = funnel(context, ids, policy)
    columns = st.columns([3, 1, 3, 1, 3])
    for column, row in zip(columns[::2], (rows[0], rows[1], rows[3]), strict=True):
        column.metric(row["Etapa"], row["Cantidad"])
    for column in columns[1::2]:
        column.markdown("### →")
    st.info(
        f"Rama separada: {rows[2]['Cantidad']} excluidas por servicio activo confirmado. "
        "No consumen las plazas de adquisición."
    )
    st.subheader("Acción y resultado comercial")
    for column, row in zip(st.columns(5), rows[4:], strict=True):
        with column.container(border=True):
            st.caption(row["Etapa"])
            st.write("**No observado**")
    st.caption(
        f"Sintético observable · Segmento: {len(ids)} / "
        f"{context['summary']['companies']} conocidas globales."
    )
    with st.expander("Auditoría del embudo"):
        table(
            [
                {
                    **row,
                    "Cantidad": str(row["Cantidad"])
                    if row["Cantidad"] is not None
                    else "No observado",
                }
                for row in rows
            ]
        )
        st.bar_chart(
            [row for row in rows[:4] if "Excluidas" not in row["Etapa"]], x="Etapa", y="Cantidad"
        )
    st.info(
        "Excluidas son una rama aparte. No se suman los dos top-5 como contactos; "
        "el grafo no autoriza acciones. Sin eventos no hay tasas de conversión."
    )
    with st.expander("Exclusiones del segmento"):
        table(
            [
                {"Empresa": row["display_name"], "Motivo": row["eligibility"]["status"]}
                for row in context["ranking"]["excluded"]
                if row["company_id"] in ids
            ]
        )
    company_detail(context, selected)


def economic_page(report: dict) -> None:
    st.warning(
        "Hipótesis educativas no calibradas. No son resultados de Totalplay ni de las PyMEs. "
        "Un saldo positivo no autoriza inversión."
    )
    scope = st.radio(
        "Escala del ejercicio",
        ["demo", "hypothetical"],
        horizontal=True,
        format_func=lambda value: (
            "Demostración · cinco plazas"
            if value == "demo"
            else "Escenario hipotético · 500 plazas"
        ),
    )
    st.subheader("Cuatro escenarios · saldo incremental hipotético")
    scenario_cards(report, scope)
    st.caption(
        "MXN nominales en valor presente. El nulo conserva costos con incremento de "
        "conversión cero; la reserva se muestra aparte, sin duplicarla."
    )
    base = next(
        row for row in report["results"] if row["scope"] == scope and row["scenario"] == "base"
    )
    st.subheader("¿Qué mejora tendría que ocurrir para cubrir el costo?")
    a, b = st.columns(2)
    for column, label, threshold in (
        (a, "Equilibrio · supuesto base", base["break_even"]),
        (b, "Umbral con reserva · supuesto base", base["required_with_reserve"]),
    ):
        value = threshold["delta_pp"]
        column.metric(label, f"{Decimal(value):.3f} pp" if value is not None else "No aplica")
    st.caption(
        "pp = puntos porcentuales de incremento absoluto de conversión. Umbral hipotético, "
        "no efecto conseguido; depende de estos costos y márgenes no calibrados. "
        "Factibilidad algebraica base: " + base["break_even"]["feasibility"]
    )
    st.info(
        "Faltan resultados comerciales y un experimento válido para decidir invertir. "
        "ROI, CAC, LTV, payback y efecto causal observados: No disponibles."
    )
    with st.expander("Auditar escenarios, componentes y supuestos"):
        settings = report["settings"]
        st.write(
            f"Ventana: {settings['activation_window_days']} días · "
            f"Horizonte: {settings['horizon_months']} meses · "
            f"Descuento mensual: {Decimal(settings['monthly_discount_rate']) * 100}%"
        )
        table(
            [
                {
                    "Escenario": SCENARIOS[row["scenario"]],
                    "Capacidad": row["slots"],
                    "Saldo neto": money(row["net_present_value_mxn"]),
                    "Reserva": money(row["reserve_mxn"]),
                    "Tras reserva": money(row["net_after_reserve_mxn"]),
                    "Equilibrio (pp)": row["break_even"]["delta_pp"],
                }
                for row in report["results"]
            ]
        )
        st.json(
            {
                "results": report["results"],
                "settings": settings,
                "input_sha256": report["input_sha256"],
                "zero_balance_reference": report["zero_balance_reference"],
            }
        )
        st.json(load_financial_config(FINANCE))
    with st.expander("Explorar sensibilidad · sin editar supuestos"):
        sensitivity = report["sensitivity"][scope]
        parameters = list(dict.fromkeys(row["parameter"] for row in sensitivity["one_way"]))
        parameter = st.selectbox("Variable explorada", parameters)
        table(
            [
                {
                    "Valor supuesto": str(row["value"]),
                    "Saldo neto": money(row["result"]["net_present_value_mxn"])
                    if "result" in row
                    else "Tasa inválida",
                    "Tras reserva": money(row["result"]["net_after_reserve_mxn"])
                    if "result" in row
                    else "No aplica",
                }
                for row in sensitivity["one_way"]
                if row["parameter"] == parameter
            ]
        )
        st.caption(sensitivity["warning"])
        st.json(
            {
                "rate_by_margin": sensitivity["rate_by_margin"],
                "volume_by_cost": sensitivity["volume_by_cost"],
            }
        )
    with st.expander("Experimento futuro y procedencia financiera"):
        st.write(
            "Asignación 1:1 por bolsas independientes, KPI de margen neto por cuenta elegible "
            "asignada, ITT, IC bilateral del 95% y potencia objetivo del 80%. Sin varianza, "
            "ICC y suficientes bolsas independientes no se fija muestra ni se acredita "
            "inferencia causal. Experimento no ejecutado."
        )
        st.caption(
            "Autorización operativa: false. Sin datos reales, contactos, presupuesto, "
            "piloto o despliegue autorizados."
        )
        st.caption(f"Versión {report['schema_version']} · SHA-256: {report['input_sha256']}")


def main() -> None:
    st.set_page_config(page_title="ConectaPyME · Control Tower", page_icon="◉", layout="wide")
    # Espaciado fijo de presentación; sin HTML procedente de datos o recursos externos.
    st.html("<style>[data-testid='stMainBlockContainer']{padding-top:2rem}</style>")
    st.title("ConectaPyME · Control Tower")
    st.caption("CONTROL TOWER · PoC educativa · Sintético observable · Sin acciones comerciales")
    page = st.sidebar.radio("Vista", PAGES)
    economic = page == "Economic Impact"
    cut = st.sidebar.selectbox("Período", list(CUTS), index=2, disabled=economic)
    source = st.sidebar.selectbox(
        "Fuente de datos", ["Offline", "Atlas · solo lectura"], disabled=economic
    )
    context = None
    key = (source, cut)
    if st.session_state.get("source_cut") != key:
        for stale in ("atlas_result", "company", "industry"):
            st.session_state.pop(stale, None)
        st.session_state["source_cut"] = key
    if source == "Offline":
        try:
            context = build_context(load_observations(LEDGER), cut)
        except (ValueError, OSError, TypeError, KeyError, AttributeError):
            st.error(
                "No se puede leer el ledger observable aprobado. Revisa su ruta y contrato; "
                "no se reconstruye desde datos restringidos."
            )
    else:
        st.sidebar.caption(
            "Requiere base MVP dedicada y permiso de lectura. No realiza escrituras ni ping."
        )
        if st.sidebar.button("Leer Atlas al corte", disabled=economic):
            st.session_state.pop("atlas_result", None)
            try:
                st.session_state["atlas_result"] = atlas_context(cut, LEDGER, ROOT / ".env")
            except ValueError as error:
                st.error(str(error))
        if "atlas_result" in st.session_state:
            context = st.session_state["atlas_result"]["context"]
            st.caption(
                "Lectura Atlas realizada en esta sesión · "
                + st.session_state["atlas_result"]["read_at"]
            )
        else:
            st.info(
                "Atlas sin lectura verificada en este contexto. Pulsa Leer Atlas o selecciona "
                "Offline; sin respaldo automático."
            )
    try:
        finance = financial_report(load_financial_config(FINANCE), sensitivity=True)
    except (ValueError, OSError):
        finance = None
    companies = context["view"]["companies"] if context else []
    industries = sorted({sector(company) for company in companies})
    industry = st.sidebar.selectbox(
        "Industria", ["Todas", *industries], key="industry", disabled=economic or context is None
    )
    options = [
        company for company in companies if industry == "Todas" or sector(company) == industry
    ]
    names = {
        company["company_id"]: company["attributes"]["display_name"]["value"]
        or company["company_id"]
        for company in options
    }
    company_options = [None, *sorted(names, key=lambda value: (names[value], value))]
    network_mode = None
    if page == "Graph Health":
        network_mode = st.sidebar.radio(
            "Exploración de red", ["Empresa y vecinos", "Red completa del segmento"]
        )
        if network_mode == "Empresa y vecinos" and names:
            company_options = company_options[1:]
            if st.session_state.get("company") not in company_options:
                st.session_state["company"] = next(
                    (key for key, name in names.items() if name == "Café Jacaranda"),
                    company_options[0],
                )
        elif network_mode == "Red completa del segmento":
            st.session_state["company"] = None
    if st.session_state.get("company") not in company_options:
        st.session_state.pop("company", None)
    selected = st.sidebar.selectbox(
        "Empresa",
        company_options,
        key="company",
        disabled=economic or context is None or network_mode == "Red completa del segmento",
        format_func=lambda value: "Todas" if value is None else names[value],
        placeholder="Todas",
    )
    with st.sidebar.expander("Filtros sin soporte real"):
        for label in ("Geografía", "Cluster", "Producto", "Canal comercial"):
            st.selectbox(label, ["Pendiente: sin datos"], disabled=True)
    if economic:
        st.info(
            "Supuestos agregados independientes del corte, empresa e industria. "
            "Filtros empresariales deshabilitados."
        )
        if finance:
            economic_page(finance)
        else:
            st.error("No se puede leer el archivo de supuestos financieros aprobado.")
        return
    if context is None:
        st.warning(
            "No hay datos empresariales cargados. Economic Impact conserva su fuente independiente."
        )
        return
    report = context["ranking"]
    ids = segment_ids(context, None if industry == "Todas" else industry, selected)
    st.caption(
        f"{source} · {cut}: {report['as_of']} · Segmento: "
        f"{len(ids)}/{context['summary']['companies']} conocidas. Totales globales rotulados."
    )
    if page != "Graph Health" and len(ids) < context["summary"]["companies"]:
        st.button("Mostrar todas las empresas", on_click=reset_segment)
    if page != "Resumen":
        st.subheader(page)
    if page == "Resumen":
        summary_page(context, ids, finance)
    elif page == "Graph Health":
        health_page(context, ids, selected)
    elif page == "AI Performance":
        performance_page(context, ids, selected)
    elif page == "Business Funnel":
        funnel_page(context, ids, selected)
    with st.expander("Procedencia técnica y reglas"):
        st.write(
            "Sintético observable; no clientes reales. 002C es validación Windows reportada "
            "por el usuario, no una lectura cloud actual. "
            "Ver docs/11-atlas-integration-validation.md."
        )
        st.code(
            f"Corte: {report['as_of']}\nPolítica: {report['policy']['version']}\n"
            f"SHA-256 visible: {report['visible_input_sha256']}"
        )
        st.json(report["policy"])


if __name__ == "__main__":
    main()
