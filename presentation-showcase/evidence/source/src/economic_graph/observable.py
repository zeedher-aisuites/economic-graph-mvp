"""Lectura comercial: solo ledger observable y consultas as-of, sin módulos del simulador."""

import json
import unicodedata
from copy import deepcopy
from datetime import datetime
from pathlib import Path

from economic_graph.contracts import (
    COMPANY_ATTRIBUTES,
    iso_time,
    parse_time,
    validate_observations,
)


def load_observations(path: Path = Path("data/observable/observations.json")) -> list[dict]:
    """Rechazar archivos de diseño: la interfaz solo admite el contrato público."""
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        raise ValueError(
            "No se puede leer el ledger observable. Ejecuta primero build_observable.py."
        ) from None
    if (
        not isinstance(document, dict)
        or set(document) != {"schema_version", "observations"}
        or document["schema_version"] != "1.0"
    ):
        raise ValueError("El archivo no cumple el contrato observable 1.0.")
    rows = document["observations"]
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError("El ledger debe contener una lista de observaciones.")
    validate_observations(rows)
    return rows


def visible_observations(rows: list[dict], as_of: str | datetime) -> list[dict]:
    """Filtrar por disponibilidad, no por phase ni fecha del hecho."""
    validate_observations(rows)
    cut = parse_time(as_of)
    visible = [row for row in rows if parse_time(row["available_at"]) <= cut]
    return deepcopy(
        sorted(visible, key=lambda row: (parse_time(row["available_at"]), row["observation_id"]))
    )


def attribute_history(
    rows: list[dict], company_id: str, attribute: str, as_of: str | datetime
) -> list[dict]:
    """Preservar alternativas y procedencia; una consulta desconocida devuelve lista vacía."""
    return [
        row
        for row in visible_observations(rows, as_of)
        if row["subject_type"] == "COMPANY"
        and row["subject_id"] == company_id
        and row["attribute"] == attribute
    ]


def _attribute(evidence: list[dict]) -> dict:
    if not evidence:
        return {"value": None, "status": "UNKNOWN", "observation_ids": []}
    values = {json.dumps(row["value"], sort_keys=True, ensure_ascii=False) for row in evidence}
    # Sin regla aprobada de arbitraje, ni la recencia ni una fuente ganan por defecto.
    return {
        "value": evidence[-1]["value"] if len(values) == 1 else None,
        "status": "OBSERVED" if len(values) == 1 else "CONFLICTED",
        "observation_ids": [row["observation_id"] for row in evidence],
    }


def _name_key(value: str) -> set[str]:
    normalized = "".join(
        char
        for char in unicodedata.normalize("NFKD", value.casefold())
        if not unicodedata.combining(char)
    )
    return set(normalized.split()) - {"de", "del", "la", "el"}


def snapshot(rows: list[dict], as_of: str | datetime) -> dict:
    """Reconstruir conocimiento, conflictos e identidades sin consultar el universo privado."""
    visible = visible_observations(rows, as_of)
    company_ids = sorted(
        {
            row["subject_id"]
            for row in visible
            if row["subject_type"] == "COMPANY" and row["attribute"] == "display_name"
        }
    )
    companies, conflicts = [], []
    for company_id in company_ids:
        evidence = [
            row
            for row in visible
            if row["subject_type"] == "COMPANY" and row["subject_id"] == company_id
        ]
        attributes = {
            attribute: _attribute([row for row in evidence if row["attribute"] == attribute])
            for attribute in sorted(COMPANY_ATTRIBUTES)
        }
        companies.append(
            {
                "company_id": company_id,
                "first_known_at": min(
                    row["available_at"] for row in evidence if row["attribute"] == "display_name"
                ),
                "identity_status": "NEEDS_REVIEW",
                "attributes": attributes,
            }
        )
        for attribute, value in attributes.items():
            if value["status"] == "CONFLICTED":
                conflicts.append(
                    {
                        "company_id": company_id,
                        "attribute": attribute,
                        "observations": [row for row in evidence if row["attribute"] == attribute],
                    }
                )
    relationships = []
    relation_ids = sorted(
        {row["subject_id"] for row in visible if row["subject_type"] == "RELATIONSHIP"}
    )
    for relationship_id in relation_ids:
        history = [
            row
            for row in visible
            if row["subject_id"] == relationship_id and row["subject_type"] == "RELATIONSHIP"
        ]
        latest = history[-1]
        latest_states = {
            row["verification_status"]
            for row in history
            if row["available_at"] == latest["available_at"]
        }
        state = latest["verification_status"] if len(latest_states) == 1 else "CONFLICTED"
        relationships.append(
            {
                "relationship_id": relationship_id,
                **latest["value"],
                "verification_status": state,
                "active_claim": state not in {"DISCARDED", "CONFLICTED"},
                "first_known_at": history[0]["available_at"],
                "status_history": history,
            }
        )
    identities = []
    for row in visible:
        if row["subject_type"] != "SOURCE_RECORD":
            continue
        candidates = [
            company["company_id"]
            for company in companies
            if isinstance(company["attributes"]["display_name"]["value"], str)
            and _name_key(company["attributes"]["display_name"]["value"]) == _name_key(row["value"])
        ]
        identities.append(
            {
                "source_record_id": row["subject_id"],
                "name": row["value"],
                "identity_status": "NEEDS_REVIEW",
                "candidate_company_ids": candidates,
                "rule": "Nombre normalizado: solo candidato, sin fusión ni ID fuerte.",
                "observation_ids": [row["observation_id"]],
            }
        )
    return {
        "as_of": iso_time(as_of),
        "companies": companies,
        "relationships": relationships,
        "observations": visible,
        "identities": identities,
        "conflicts": conflicts,
    }


def summarize(view: dict) -> dict:
    """Conteos comerciales: no clasificar afirmaciones como verdaderas o falsas."""
    relationships = view["relationships"]
    referrals = sum(row["relationship_type"] == "REFERS_TO" for row in relationships)
    return {
        "as_of": view["as_of"],
        "companies": len(view["companies"]),
        "relationship_claims": len(relationships) - referrals,
        "referrals": referrals,
        "observations": len(view["observations"]),
        "identity_candidates": len(view["identities"]),
        "conflicted_attributes": len(view["conflicts"]),
    }
