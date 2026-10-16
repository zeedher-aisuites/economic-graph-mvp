"""Políticas comparables: solo evidencia observable al corte, sin acceso al simulador."""

import hashlib
import json
from collections import defaultdict
from copy import deepcopy
from datetime import datetime

from economic_graph.contracts import parse_time
from economic_graph.observable import snapshot

POLICY = {
    "version": "003a-conservative-v1",
    "capacity": 5,
    "additional_branches": {"weight": 10, "cap": 5},
    "confirmed_neighbors": {"weight": 5, "cap": 4},
    "baseline_rule": "10 × min(max(branch_count − 1, 0), 5)",
    "graph_rule": "baseline + 5 × min(distinct_confirmed_economic_neighbors, 4)",
    "eligibility_rule": "Conocidas salvo servicio activo confirmado sin conflicto.",
    "tie_break": "Puntuación descendente, company_id público ascendente.",
    "interpretation": "Puntos exploratorios; no probabilidades ni efecto económico medido.",
}
ACCEPTED_ATTRIBUTES = {"REPORTED", "CONFIRMED"}
ECONOMIC_TYPES = {"SUPPLIES_TO", "PARTNERS_WITH"}


def _latest(evidence: list[dict]) -> list[dict]:
    instant = max(parse_time(row["available_at"]) for row in evidence)
    return [row for row in evidence if parse_time(row["available_at"]) == instant]


def _attribute_status(attribute: dict, evidence: list[dict]) -> str:
    """No arbitrar valores distintos; tampoco usar una última evidencia descartada."""
    if attribute["status"] != "OBSERVED":
        return attribute["status"]
    states = {row["verification_status"] for row in _latest(evidence)}
    if len(states) > 1:
        return "VERIFICATION_CONFLICTED"
    return "OBSERVED" if states <= ACCEPTED_ATTRIBUTES else "INSUFFICIENT_EVIDENCE"


def _branch_feature(attribute: dict, evidence: list[dict]) -> dict:
    status = _attribute_status(attribute, evidence)
    value = max(attribute["value"] - 1, 0) if status == "OBSERVED" else None
    parameters = POLICY["additional_branches"]
    return {
        "status": status,
        "observed_branch_count": attribute["value"],
        "value": value,
        **parameters,
        "contribution": min(value, parameters["cap"]) * parameters["weight"]
        if value is not None
        else 0,
        "rule": POLICY["baseline_rule"],
        "evidence": evidence,
    }


def _relationship_context(relationships: list[dict]) -> list[dict]:
    """Evaluar estados al corte; duplicados no multiplican vecinos ni ocultan conflictos."""
    claims, by_signature = [], defaultdict(list)
    for relationship in relationships:
        evidence = relationship["status_history"]
        values = {
            (
                row["value"]["relationship_type"],
                row["value"]["from_company_id"],
                row["value"]["to_company_id"],
            )
            for row in evidence
        }
        latest = _latest(evidence)
        states = {row["verification_status"] for row in latest}
        state = next(iter(states)) if len(states) == 1 and len(values) == 1 else "CONFLICTED"
        claim = {
            "relationship_id": relationship["relationship_id"],
            **latest[0]["value"],
            "verification_status": state,
            "scoring_status": state,
            "evidence": evidence,
        }
        if claim["relationship_type"] not in ECONOMIC_TYPES:
            claim["scoring_status"] = "NOT_ECONOMIC"
        claims.append(claim)
        # Conservar IDs e historia; agrupar hechos equivalentes solo para detectar oposición.
        for signature in values:
            by_signature[signature].append(claim)
    for group in by_signature.values():
        states = {claim["verification_status"] for claim in group}
        if "CONFIRMED" in states and states & {"DISCARDED", "CONFLICTED"}:
            for claim in group:
                if claim["relationship_type"] in ECONOMIC_TYPES:
                    claim["scoring_status"] = "CONFLICTED"
    return claims


def _neighbor_feature(company_id: str, claims: list[dict]) -> dict:
    related = [
        claim
        for claim in claims
        if any(
            company_id in (row["value"]["from_company_id"], row["value"]["to_company_id"])
            for row in claim["evidence"]
        )
    ]
    neighbors = defaultdict(list)
    for claim in related:
        if claim["scoring_status"] == "CONFIRMED":
            other = (
                claim["to_company_id"]
                if claim["from_company_id"] == company_id
                else (claim["from_company_id"])
            )
            neighbors[other].append(claim["relationship_id"])
    value = len(neighbors)
    parameters = POLICY["confirmed_neighbors"]
    return {
        "status": "OBSERVED" if value else "INSUFFICIENT_EVIDENCE",
        "value": value,
        **parameters,
        "contribution": min(value, parameters["cap"]) * parameters["weight"],
        "rule": "Vecinos distintos en SUPPLIES_TO/PARTNERS_WITH CONFIRMED; sin fusión de alias.",
        "neighbors": [
            {"company_id": key, "relationship_ids": sorted(neighbors[key])}
            for key in sorted(neighbors)
        ],
        "relationship_ids": [claim["relationship_id"] for claim in related],
        "evidence": [row for claim in related for row in claim["evidence"]],
    }


def _boundary(ordered: list[dict], score_key: str) -> dict:
    capacity = POLICY["capacity"]
    if not ordered:
        return {"crosses_tie": False, "score": None, "tied_company_ids": []}
    index = min(capacity, len(ordered)) - 1
    score = ordered[index][score_key]
    return {
        "crosses_tie": len(ordered) > capacity and ordered[capacity][score_key] == score,
        "score": score,
        "tied_company_ids": [row["company_id"] for row in ordered if row[score_key] == score],
    }


def compare_rankings(rows: list[dict], as_of: str | datetime) -> dict:
    """Calcular ambas políticas sobre la misma cohorte, sin red, escrituras ni etiquetas."""
    view = snapshot(rows, as_of)
    observations = view["observations"]
    claims = _relationship_context(view["relationships"])
    companies, excluded = [], []
    for company in view["companies"]:
        company_id, attributes = company["company_id"], company["attributes"]
        evidence = defaultdict(list)
        for row in observations:
            if row["subject_type"] == "COMPANY" and row["subject_id"] == company_id:
                evidence[row["attribute"]].append(row)
        service = attributes["service_active"]
        service_evidence = evidence["service_active"]
        service_status = _attribute_status(service, service_evidence)
        active = (
            service_status == "OBSERVED"
            and service["value"] is True
            and {row["verification_status"] for row in _latest(service_evidence)} == {"CONFIRMED"}
        )
        result = {
            "company_id": company_id,
            "display_name": attributes["display_name"]["value"],
            "name_evidence": evidence["display_name"],
            "identity_status": company["identity_status"],
            "eligibility": {
                "eligible": not active,
                "status": "ACTIVE_SERVICE_CONFIRMED" if active else "PENDING_COMMERCIAL_VALIDATION",
                "service_status": service_status,
                "observed_service_active": service["value"],
                "evidence": service_evidence,
            },
        }
        if active:
            excluded.append(result)
            continue
        branches = _branch_feature(attributes["branch_count"], evidence["branch_count"])
        neighbors = _neighbor_feature(company_id, claims)
        result.update(
            {
                "features": {"additional_branches": branches, "confirmed_neighbors": neighbors},
                "baseline_score": branches["contribution"],
                "graph_score": branches["contribution"] + neighbors["contribution"],
            }
        )
        companies.append(result)
    baseline = sorted(companies, key=lambda row: (-row["baseline_score"], row["company_id"]))
    graph = sorted(companies, key=lambda row: (-row["graph_score"], row["company_id"]))
    capacity = POLICY["capacity"]
    for policy, ordered in (("baseline", baseline), ("graph", graph)):
        for position, company in enumerate(ordered, start=1):
            company[f"{policy}_position"] = position
            company[f"{policy}_selected"] = position <= capacity
    for company in baseline:
        company["position_change"] = company["baseline_position"] - company["graph_position"]
        company["selection_change"] = (
            "BOTH"
            if company["baseline_selected"] and company["graph_selected"]
            else "GRAPH_ONLY"
            if company["graph_selected"]
            else "BASELINE_ONLY"
            if company["baseline_selected"]
            else "NEITHER"
        )
    baseline_ids = [row["company_id"] for row in baseline[:capacity]]
    graph_ids = [row["company_id"] for row in graph[:capacity]]
    canonical = json.dumps(observations, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return {
        "policy": deepcopy(POLICY),
        "as_of": view["as_of"],
        "visible_input_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "known_companies": len(view["companies"]),
        "eligible_companies": len(companies),
        "visible_observations": len(observations),
        "companies": baseline,
        "excluded": excluded,
        "top_k": {"baseline": baseline_ids, "graph": graph_ids},
        "comparison": {
            "shared": sorted(set(baseline_ids) & set(graph_ids)),
            "entered_graph": [key for key in graph_ids if key not in baseline_ids],
            "left_baseline": [key for key in baseline_ids if key not in graph_ids],
            "baseline_boundary": _boundary(baseline, "baseline_score"),
            "graph_boundary": _boundary(graph, "graph_score"),
            "unfilled_capacity": max(capacity - len(companies), 0),
        },
        "relationship_context": claims,
        "identity_candidates": view["identities"],
        "conflicts": view["conflicts"],
    }


def render_comparison(report: dict) -> str:
    """Tabla resumida; el JSON conserva reglas, evidencias y contribuciones completas."""

    def label(value: object) -> str:
        return " ".join(str(value).split()).replace("|", "\\|")

    names = {
        row["company_id"]: row["display_name"] or row["company_id"] for row in report["companies"]
    }
    comparison = report["comparison"]
    lines = [
        f"## Corte {report['as_of']}",
        "",
        f"Política `{report['policy']['version']}`; capacidad **{report['policy']['capacity']}**. "
        f"Conocidas: {report['known_companies']}; elegibles: {report['eligible_companies']}; "
        f"excluidas: {len(report['excluded'])}; observaciones: {report['visible_observations']}.",
        "",
    ]
    for policy in ("baseline", "graph"):
        selected = ", ".join(label(names[key]) for key in report["top_k"][policy]) or "Ninguna"
        lines.append(f"- Top-5 {policy}: {selected}.")
    lines.extend(
        [
            f"- Coincidencias: {len(comparison['shared'])}; "
            f"entran con grafo: {len(comparison['entered_graph'])}; "
            f"salen: {len(comparison['left_baseline'])}.",
            f"- Empate que atraviesa el límite: baseline "
            f"{'sí' if comparison['baseline_boundary']['crosses_tie'] else 'no'}, grafo "
            f"{'sí' if comparison['graph_boundary']['crosses_tie'] else 'no'}.",
            "",
            "| Cuenta | Pos. baseline | Puntos baseline | Pos. grafo | Puntos grafo | Δ posición | "
            "Extra grafo | Selección |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    selections = {
        "BOTH": "Ambas",
        "GRAPH_ONLY": "Solo grafo",
        "BASELINE_ONLY": "Solo baseline",
        "NEITHER": "Ninguna",
    }
    for company in report["companies"]:
        lines.append(
            f"| {label(company['display_name'] or company['company_id'])} | "
            f"{company['baseline_position']} | {company['baseline_score']} | "
            f"{company['graph_position']} | {company['graph_score']} | "
            f"{company['position_change']:+d} | "
            f"{company['features']['confirmed_neighbors']['contribution']} | "
            f"{selections[company['selection_change']]} |"
        )
    lines.extend(
        [
            "",
            "Δ positivo significa subir respecto al baseline. El desempate por ID "
            "no expresa prioridad comercial. Cero puntos no demuestra falta de potencial.",
        ]
    )
    if report["excluded"]:
        lines.extend(
            [
                "",
                "Excluidas por servicio activo confirmado: "
                + ", ".join(
                    label(row["display_name"] or row["company_id"]) for row in report["excluded"]
                )
                + ".",
            ]
        )
    lines.extend(
        [
            "",
            f"SHA-256 de las observaciones visibles: `{report['visible_input_sha256']}`.",
            "",
            "Datos sintéticos observables; sin conversiones ni efecto económico medido.",
        ]
    )
    return "\n".join(lines) + "\n"
