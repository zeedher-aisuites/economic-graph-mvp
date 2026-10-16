"""Adaptación descriptiva de fuentes públicas; sin nuevas reglas comerciales ni UI."""

import math
import textwrap
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from pymongo.errors import PyMongoError

from economic_graph.config import load_config
from economic_graph.contracts import CUTS, parse_time
from economic_graph.database import create_client
from economic_graph.mongo_observable import MVP_DATABASE, read_observations
from economic_graph.observable import load_observations, snapshot, summarize
from economic_graph.rankings import compare_rankings

UNKNOWN = "Desconocida"
CONFLICTED = "En conflicto"
TYPES = {
    "SUPPLIES_TO": "Suministra a",
    "PARTNERS_WITH": "Alianza",
    "REFERS_TO": "Referencia (no puntúa)",
}
STATES = {
    "CONFIRMED": "Confirmada",
    "REPORTED": "Reportada",
    "INFERRED": "Inferida",
    "DISCARDED": "Descartada",
    "CONFLICTED": "En conflicto",
}


def sector(company: dict) -> str:
    attribute = company["attributes"]["sector"]
    if attribute["status"] == "CONFLICTED":
        return CONFLICTED
    return attribute["value"] if attribute["status"] == "OBSERVED" else UNKNOWN


def build_context(rows: list[dict], cut: str) -> dict:
    """Calcular siempre sobre la entrada completa al corte, antes de filtros visuales."""
    view = snapshot(rows, cut)
    ranking = compare_rankings(rows, cut)
    eligible = ranking["companies"]
    return {
        "view": view,
        "summary": summarize(view),
        "ranking": ranking,
        "evolution": [
            {"Corte": label, **summarize(snapshot(rows, instant))}
            for label, instant in CUTS.items()
            if parse_time(instant) <= parse_time(cut)
        ],
        "sources": dict(Counter(row["source_type"] for row in view["observations"])),
        "states": dict(Counter(row["verification_status"] for row in view["relationships"])),
        "coverage": {
            "branches": sum(
                row["features"]["additional_branches"]["status"] == "OBSERVED" for row in eligible
            ),
            "neighbors": sum(
                row["features"]["confirmed_neighbors"]["value"] > 0 for row in eligible
            ),
            "denominator": len(eligible),
        },
    }


def segment_ids(context: dict, industry: str | None = None, company_id: str | None = None) -> set:
    return {
        company["company_id"]
        for company in context["view"]["companies"]
        if (industry is None or sector(company) == industry)
        and (company_id is None or company["company_id"] == company_id)
    }


def ranking_table(context: dict, ids: set | None = None) -> list[dict]:
    """Copiar puntuaciones/posiciones globales; nunca rellenar el top-5 del segmento."""
    return [
        {
            "ID": row["company_id"],
            "Empresa": row["display_name"] or row["company_id"],
            "Posición baseline": row["baseline_position"],
            "Posición grafo": row["graph_position"],
            "Cambio de posición": row["position_change"],
            "Score baseline": row["baseline_score"],
            "Score grafo": row["graph_score"],
            "Aporte individual": row["features"]["additional_branches"]["contribution"],
            "Aporte relacional": row["features"]["confirmed_neighbors"]["contribution"],
            "Top-5 baseline": row["baseline_selected"],
            "Top-5 grafo": row["graph_selected"],
        }
        for row in context["ranking"]["companies"]
        if ids is None or row["company_id"] in ids
    ]


def funnel(context: dict, ids: set, policy: str) -> list[dict]:
    report = context["ranking"]
    eligible = {row["company_id"] for row in report["companies"]}
    excluded = {row["company_id"] for row in report["excluded"]}
    measured = [
        ("Conocidas", len(ids)),
        ("Elegibles para ranking", len(ids & eligible)),
        ("Excluidas (rama aparte)", len(ids & excluded)),
        ("Priorizadas del top-5 global", len(ids & set(report["top_k"][policy]))),
    ]
    return [
        {"Etapa": name, "Cantidad": count, "Estado": "Sintético observable"}
        for name, count in measured
    ] + [
        {"Etapa": name, "Cantidad": None, "Estado": "No observado"}
        for name in ("Contactos", "Contactos activados", "Oportunidades", "Activaciones", "Ventas")
    ]


def account_detail(context: dict, company_id: str) -> dict | None:
    view, report = context["view"], context["ranking"]
    company = next((c for c in view["companies"] if c["company_id"] == company_id), None)
    if company is None:
        return None
    ranking = next(
        c for c in report["companies"] + report["excluded"] if c["company_id"] == company_id
    )
    relationships = [
        claim
        for claim in report["relationship_context"]
        if any(
            company_id in (row["value"]["from_company_id"], row["value"]["to_company_id"])
            for row in claim["evidence"]
        )
    ]
    candidates = [row for row in view["identities"] if company_id in row["candidate_company_ids"]]
    subjects = (
        {company_id}
        | {row["relationship_id"] for row in relationships}
        | {row["source_record_id"] for row in candidates}
    )
    return {
        "company": company,
        "ranking": ranking,
        "relationships": relationships,
        "candidates": candidates,
        "observations": [row for row in view["observations"] if row["subject_id"] in subjects],
    }


def network_data(context: dict, ids: set, focus_id: str | None = None) -> dict:
    """Red incidente al segmento; extremos externos conocidos permanecen como contexto."""
    view, report = context["view"], context["ranking"]
    known = {row["company_id"]: row for row in view["companies"]}
    if not ids <= known.keys():
        raise ValueError("La selección contiene una empresa no conocida al corte.")
    if focus_id is not None and ids != {focus_id}:
        raise ValueError("El foco debe corresponder a la única empresa seleccionada.")
    claims = [
        row for row in view["relationships"] if ids & {row["from_company_id"], row["to_company_id"]}
    ]
    diagnostics = {row["relationship_id"]: row for row in report["relationship_context"]}
    shown = ids | {row[key] for row in claims for key in ("from_company_id", "to_company_id")}
    if not shown <= known.keys():
        raise ValueError("La red contiene un extremo no identificable al corte.")
    ordered = sorted(shown - {focus_id}) if focus_id else sorted(known)
    # Layout circular determinista: posición decorativa, sin distancia comercial implícita.
    positions = {
        key: (math.cos(2 * math.pi * i / len(ordered)), math.sin(2 * math.pi * i / len(ordered)))
        for i, key in enumerate(ordered)
    }
    if focus_id:
        positions[focus_id] = (0, 0)
    ranked = {row["company_id"]: row for row in report["companies"]}
    focus = ranked.get(focus_id, {})
    support_ids = {
        identifier
        for neighbor in focus.get("features", {})
        .get("confirmed_neighbors", {})
        .get("neighbors", [])
        for identifier in neighbor["relationship_ids"]
    }
    nodes = []
    for key in sorted(shown):
        company = known[key]
        incident = [
            row
            for row in view["relationships"]
            if key in (row["from_company_id"], row["to_company_id"])
            and row["relationship_type"] != "REFERS_TO"
        ]
        usable = any(
            diagnostics[row["relationship_id"]]["scoring_status"] == "CONFIRMED" for row in incident
        )
        state = (
            ("Con vínculo confirmado utilizable" if usable else "Sin vínculo confirmado utilizable")
            if incident
            else "Sin vínculo económico observado"
        )
        rank = ranked.get(key, {})
        nodes.append(
            {
                "id": key,
                "name": company["attributes"]["display_name"]["value"] or key,
                "label": textwrap.fill(company["attributes"]["display_name"]["value"] or key, 18)
                if len(shown) <= 10
                else "",
                "sector": sector(company),
                "x": positions[key][0],
                "y": positions[key][1],
                "label_x": positions[key][0] * 1.22,
                "label_y": positions[key][1] * 1.22 if key != focus_id else -0.22,
                "size": 650 if key == focus_id else 180,
                "scope": "Selección" if key in ids else "Vecino de contexto",
                "state": state,
                "identity": company["identity_status"],
                "baseline_score": rank.get("baseline_score"),
                "graph_score": rank.get("graph_score"),
            }
        )
    edges = []
    for row in claims:
        left, right = row["from_company_id"], row["to_company_id"]
        edges.append(
            {
                "id": row["relationship_id"],
                "from": left,
                "to": right,
                "from_name": known[left]["attributes"]["display_name"]["value"] or left,
                "to_name": known[right]["attributes"]["display_name"]["value"] or right,
                "type": TYPES[row["relationship_type"]],
                "status": STATES[row["verification_status"]],
                "scoring_status": diagnostics[row["relationship_id"]]["scoring_status"],
                "supports_focus": row["relationship_id"] in support_ids,
                "emphasis": 4 if row["relationship_id"] in support_ids else 1.5,
                "opacity": 1 if row["relationship_id"] in support_ids else 0.5,
                "source": ", ".join(sorted({r["source_type"] for r in row["status_history"]})),
                "evidence": ", ".join(r["observation_id"] for r in row["status_history"]),
                "x": positions[left][0],
                "y": positions[left][1],
                "x2": positions[right][0],
                "y2": positions[right][1],
            }
        )
    return {"nodes": nodes, "edges": edges}


def network_spec(network: dict) -> dict:
    """Vega-Lite integrado en Streamlit: sin bibliotecas de red, CDN o HTML propio."""
    axes = {"type": "quantitative", "axis": None, "scale": {"domain": [-1.45, 1.45]}}
    return {
        "height": 350,
        "layer": [
            {
                "data": {"values": network["edges"]},
                "mark": {"type": "rule"},
                "encoding": {
                    "x": {"field": "x", **axes},
                    "y": {"field": "y", **axes},
                    "x2": {"field": "x2"},
                    "y2": {"field": "y2"},
                    "strokeWidth": {
                        "field": "emphasis",
                        "type": "quantitative",
                        "scale": None,
                        "legend": None,
                    },
                    "opacity": {
                        "field": "opacity",
                        "type": "quantitative",
                        "scale": None,
                        "legend": None,
                    },
                    "color": {
                        "field": "type",
                        "type": "nominal",
                        "title": "Vínculo",
                        "scale": {
                            "domain": list(TYPES.values()),
                            "range": ["#2563eb", "#0d9488", "#b45309"],
                        },
                    },
                    "strokeDash": {
                        "field": "status",
                        "type": "nominal",
                        "title": "Verificación",
                        "scale": {
                            "domain": list(STATES.values()),
                            "range": [[1, 0], [7, 4], [2, 4], [10, 6, 2, 6], [4, 3, 1, 3]],
                        },
                    },
                    "tooltip": [
                        {"field": field, "type": "nominal", "title": title}
                        for field, title in (
                            ("from_name", "Desde"),
                            ("to_name", "Hacia"),
                            ("type", "Tipo"),
                            ("status", "Estado"),
                            ("scoring_status", "Diagnóstico scoring"),
                            ("supports_focus", "Respalda señal de la cuenta"),
                            ("source", "Fuentes"),
                            ("evidence", "Observaciones"),
                        )
                    ],
                },
            },
            {
                "data": {"values": network["nodes"]},
                "mark": {"type": "point", "filled": True, "stroke": "white"},
                "encoding": {
                    "x": {"field": "x", **axes},
                    "y": {"field": "y", **axes},
                    "size": {
                        "field": "size",
                        "type": "quantitative",
                        "scale": None,
                        "legend": None,
                    },
                    "color": {
                        "field": "scope",
                        "type": "nominal",
                        "title": "Cuenta",
                        "scale": {
                            "domain": ["Selección", "Vecino de contexto"],
                            "range": ["#172554", "#94a3b8"],
                        },
                    },
                    "shape": {
                        "field": "state",
                        "type": "nominal",
                        "title": "Evidencia económica",
                        "legend": None,
                        "scale": {
                            "domain": [
                                "Con vínculo confirmado utilizable",
                                "Sin vínculo confirmado utilizable",
                                "Sin vínculo económico observado",
                            ],
                            "range": ["circle", "diamond", "square"],
                        },
                    },
                    "tooltip": [
                        {"field": field, "type": "nominal", "title": title}
                        for field, title in (
                            ("name", "Empresa"),
                            ("sector", "Sector"),
                            ("state", "Evidencia"),
                            ("identity", "Identidad"),
                            ("baseline_score", "Score baseline"),
                            ("graph_score", "Score grafo"),
                        )
                    ],
                },
            },
            {
                "data": {"values": network["nodes"]},
                "mark": {
                    "type": "text",
                    "fontSize": 12,
                    "lineHeight": 14,
                    "lineBreak": "\n",
                    "limit": 160,
                },
                "encoding": {
                    "x": {"field": "label_x", **axes},
                    "y": {"field": "label_y", **axes},
                    "text": {"field": "label", "type": "nominal"},
                },
            },
        ],
        "resolve": {"scale": {"color": "independent"}},
        "config": {"view": {"stroke": None}, "legend": {"orient": "bottom", "columns": 2}},
    }


def atlas_context(cut: str, ledger_path: Path, env_file: Path) -> dict:
    """Lectura explícita, base dedicada y paridad; errores deliberadamente sin detalle remoto."""
    try:
        local = build_context(load_observations(ledger_path), cut)
        uri, database = load_config(env_file)
        if database != MVP_DATABASE:
            raise ValueError("Base no autorizada")
        with create_client(uri) as client:
            rows = read_observations(client[database], cut)
        context = build_context(rows, cut)
    except (
        ValueError,
        ConnectionError,
        OSError,
        TypeError,
        KeyError,
        AttributeError,
        PyMongoError,
    ):
        raise ValueError(
            "No se pudo leer Atlas. Revisa configuración local, base dedicada, DNS, red, "
            "TLS y permisos de lectura. No se cargaron cifras de respaldo."
        ) from None
    if context["ranking"]["visible_input_sha256"] != local["ranking"]["visible_input_sha256"]:
        raise ValueError(
            "Datos distintos del ledger aprobado. Demostración comparable bloqueada; "
            "investiga la diferencia sin modificar Atlas."
        )
    return {"context": context, "read_at": datetime.now(UTC).isoformat()}
