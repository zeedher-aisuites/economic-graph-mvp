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
        st.dataframe(rows, hide_index=True, width="stretch")
    else:
        st.info("Sin registros para esta selección.")


def money(value: str) -> str:
    return f"${Decimal(value):,.2f} MXN"


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
    st.caption(f"{selected} · {sector(company)} · Identidad NEEDS_REVIEW: sin resolución fuerte")
    st.write("**Elegibilidad:** " + rank["eligibility"]["status"])
    if rank["eligibility"]["eligible"]:
        a, b, c, d = st.columns(4)
        a.metric("Score baseline", rank["baseline_score"])
        b.metric("Score grafo", rank["graph_score"])
        c.metric("Posición baseline global", rank["baseline_position"])
        d.metric("Posición grafo global", rank["graph_position"])
        table(
            [
                {
                    "Señal": name,
                    "Estado": feature["status"],
                    "Valor utilizable": feature["value"],
                    "Aporte": feature["contribution"],
                    "Peso": feature["weight"],
                    "Tope": feature["cap"],
                    "Regla": feature["rule"],
                }
                for name, feature in rank["features"].items()
            ]
        )
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
    a, b, c, d = st.columns(4)
    a.metric("Empresas conocidas · global", summary["companies"])
    b.metric("Afirmaciones económicas · global", summary["relationship_claims"])
    c.metric("Cuentas elegibles · global", report["eligible_companies"])
    d.metric("Cambios en cinco plazas · global", len(report["comparison"]["entered_graph"]))
    st.caption(
        "Sintético observable · Afirmaciones no equivale a relaciones confirmadas. "
        f"Referencias separadas: {summary['referrals']}. Capacidad: cinco cuentas por investigar, "
        "sin autorización de contacto."
    )
    top_tables(context, ids)
    st.info(
        "El grafo añade vecinos económicos confirmados a las mismas señales individuales. "
        "Cambiar la selección no demuestra más ventas; los empates y la escasez de evidencia "
        "limitan la interpretación."
    )
    st.subheader("¿Qué beneficio podría cubrir el costo?")
    if finance:
        rows = [row for row in finance["results"] if row["scope"] == "hypothetical"]
        table(
            [
                {
                    "Hipótesis · 500 plazas": SCENARIOS[row["scenario"]],
                    "Saldo incremental": money(row["net_present_value_mxn"]),
                    "Saldo tras reserva": money(row["net_after_reserve_mxn"]),
                }
                for row in rows
            ]
        )
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
    network = network_data(context, ids)
    if network["nodes"]:
        st.vega_lite_chart(
            spec=network_spec(network),
            width="stretch",
            alt="Red observable: empresas, vínculos y estados; detalle tabular debajo.",
        )
    else:
        st.info("Sin empresas en el segmento.")
    st.caption(
        "Explora con el selector Empresa y pasa el cursor sobre nodos/líneas. "
        "Línea continua: confirmada; trazos: reportada; puntos: inferida. "
        "Con más de diez nodos, los nombres aparecen al pasar el cursor o en las tablas; "
        "Color: tipo de vínculo. Referencias no puntúan. Posición circular decorativa, "
        "sin distancia comercial. Dirección y diagnósticos en la tabla; "
        "vecinos de contexto pueden estar fuera del sector."
    )
    source = st.selectbox(
        "Fuente de evidencia · solo inspección", ["Todas", *sorted(context["sources"])]
    )
    relation_type = st.selectbox("Tipo de vínculo · solo inspección", ["Todos", *TYPES.values()])
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
    company_detail(context, selected)


def performance_page(context: dict, ids: set, selected: str | None) -> None:
    st.info(
        "Comparación de reglas explicables, sin modelo predictivo entrenado. "
        "Puntos ≠ probabilidades."
    )
    report, coverage = context["ranking"], context["coverage"]
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
    top_tables(context, ids)
    comparison = report["comparison"]
    st.write(
        f"**Global:** {len(comparison['shared'])} cuentas compartidas; "
        f"{len(comparison['entered_graph'])} entran con grafo y "
        f"{len(comparison['left_baseline'])} salen del baseline."
    )
    for policy, title in (("baseline", "baseline"), ("graph", "grafo")):
        boundary = comparison[f"{policy}_boundary"]
        st.write(
            f"Empate que cruza el límite {title}: **{'Sí' if boundary['crosses_tie'] else 'No'}**. "
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
    st.caption(
        f"Sintético observable · Segmento: {len(ids)} / "
        f"{context['summary']['companies']} conocidas globales."
    )
    table(
        [
            {
                **row,
                "Cantidad": str(row["Cantidad"]) if row["Cantidad"] is not None else "No observado",
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
    settings = report["settings"]
    st.caption(
        f"MXN nominales · ventana {settings['activation_window_days']} días · "
        f"horizonte {settings['horizon_months']} meses · "
        f"descuento mensual {Decimal(settings['monthly_discount_rate']) * 100}% · "
        "valores presentes a la asignación."
    )
    for scope, title in (
        ("demo", "Demostración: cinco plazas"),
        ("hypothetical", "Escenario hipotético: 500 plazas"),
    ):
        st.subheader(title)
        rows = [row for row in report["results"] if row["scope"] == scope]
        table(
            [
                {
                    "Escenario": SCENARIOS[row["scenario"]],
                    "Δ conversión hipotética (pp)": str(
                        Decimal(row["activation_rate_increment"]) * 100
                    ),
                    "Saldo neto": money(row["net_present_value_mxn"]),
                    "Reserva": money(row["reserve_mxn"]),
                    "Tras reserva": money(row["net_after_reserve_mxn"]),
                    "Equilibrio (pp)": row["break_even"]["delta_pp"],
                    "Equilibrio con reserva (pp)": row["required_with_reserve"]["delta_pp"],
                    "Factibilidad algebraica": row["break_even"]["feasibility"],
                }
                for row in rows
            ]
        )
        st.bar_chart(
            [
                {
                    "Escenario": SCENARIOS[row["scenario"]],
                    "Saldo neto hipotético MXN": float(row["net_present_value_mxn"]),
                }
                for row in rows
            ],
            x="Escenario",
            y="Saldo neto hipotético MXN",
            color="#64748b",
        )
    st.caption(
        "Nulo: incremento de conversión cero con costos conservados; saldo cero es un umbral "
        "diferente. La reserva es un colchón separado, no se descuenta dos veces. "
        "Los gráficos usan floats solo para dibujar; cálculos del módulo con Decimal."
    )
    with st.expander("Componentes auditables y supuestos de cada escenario"):
        table(
            [
                {
                    "Capacidad": row["slots"],
                    "Escenario": SCENARIOS[row["scenario"]],
                    **{key: value for key, value in row.items() if key.endswith("_mxn")},
                }
                for row in report["results"]
            ]
        )
        st.json(load_financial_config(FINANCE))
    st.subheader("Sensibilidad hipotética · sin editar supuestos")
    scope = st.selectbox(
        "Capacidad de sensibilidad",
        ["demo", "hypothetical"],
        format_func=lambda value: "Cinco plazas" if value == "demo" else "500 plazas hipotéticas",
    )
    sensitivity = report["sensitivity"][scope]
    parameters = list(dict.fromkeys(row["parameter"] for row in sensitivity["one_way"]))
    parameter = st.selectbox("Variable explorada", parameters)
    table(
        [
            {
                "Parámetro": row["parameter"],
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
    with st.expander("Matrices de sensibilidad y referencia algebraica de saldo cero"):
        st.json(
            {
                "rate_by_margin": sensitivity["rate_by_margin"],
                "volume_by_cost": sensitivity["volume_by_cost"],
                "zero_balance_reference": report["zero_balance_reference"],
            }
        )
    st.subheader("Experimento futuro · no ejecutado")
    st.write(
        "Asignación 1:1 por bolsas independientes, KPI de margen neto por cuenta elegible "
        "asignada, ITT, IC bilateral del 95% y potencia objetivo del 80%. Sin varianza, "
        "ICC ni bolsas suficientes no se calcula muestra ni se acredita inferencia causal."
    )
    st.caption(
        "Autorización operativa: false. ROI observado, CAC, LTV, payback y efecto causal: "
        "No disponibles. Sin datos reales, contactos, presupuesto, piloto o despliegue autorizados."
    )
    st.caption(
        f"Versión {report['schema_version']} · SHA-256 de supuestos: {report['input_sha256']}"
    )


def main() -> None:
    st.set_page_config(page_title="ConectaPyME · Control Tower", page_icon="◉", layout="wide")
    st.title("ConectaPyME · Inteligencia comercial")
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
    if st.session_state.get("company") not in company_options:
        st.session_state.pop("company", None)
    selected = st.sidebar.selectbox(
        "Empresa",
        company_options,
        key="company",
        disabled=economic or context is None,
        format_func=lambda value: "Todas" if value is None else names[value],
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
    st.caption(f"{source} · Corte {report['as_of']} · Política {report['policy']['version']}")
    ids = segment_ids(context, None if industry == "Todas" else industry, selected)
    st.caption(
        f"Segmento: {len(ids)} de {context['summary']['companies']} empresas conocidas. "
        "Tarjetas rotuladas Global conservan el total al corte."
    )
    st.header(page)
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
