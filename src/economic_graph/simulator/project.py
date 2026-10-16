"""Proyección unidireccional de observaciones; no utiliza perfiles ni vínculos del mundo."""

import json
from copy import deepcopy
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from economic_graph.contracts import iso_time, validate_observations

# Estas notas son diagnósticos del diseñador, no evidencia accesible a un comercial.
EVIDENCE_PROJECTION = {
    "OBS-043": (
        "Afirmación de suministro recibida por referencia comercial; pendiente de verificación."
    ),
    "OBS-044": "Hipótesis de colaboración basada solo en coincidencia geográfica; no confirmada.",
    "OBS-073": (
        "Afirmación de suministro registrada en una nota comercial; pendiente de verificación."
    ),
}


def public_id(prefix: str, observation_id: str) -> str:
    """Asignar identidad estable desde evidencia, independiente del ordinal EMP o CLM."""
    return f"{prefix}-{uuid5(NAMESPACE_URL, 'conectapyme/1.0/' + observation_id).hex}"


def project_observations(plan: list[dict]) -> tuple[list[dict], dict]:
    """Devolver ledger público y conciliación privada; ninguna decisión usa la verdad."""
    company_map = {
        row["subject_id"]: public_id("CO", row["observation_id"])
        for row in plan
        if row["subject_type"] == "COMPANY" and row["attribute"] == "display_name"
    }
    subjects = {}
    for row in sorted(
        plan, key=lambda item: (iso_time(item["available_at"]), item["observation_id"])
    ):
        kind = row["subject_type"]
        prefix = "REC" if kind == "COMPANY_ALIAS" else "LINK"
        if kind != "COMPANY":
            subjects.setdefault(row["subject_id"], public_id(prefix, row["observation_id"]))
    result = []
    for original in sorted(plan, key=lambda item: item["observation_id"]):
        identifier = original["observation_id"]
        kind = original["subject_type"]
        row = {
            key: deepcopy(original[key])
            for key in (
                "observation_id",
                "attribute",
                "value",
                "source_type",
                "verification_status",
                "observed_at",
                "recorded_at",
                "available_at",
                "evidence_note",
                "conflict_group",
            )
        }
        row["source_record_id"] = f"SRC-{original['source_type']}-{identifier}"
        row["subject_type"] = {"REFERRAL": "RELATIONSHIP", "COMPANY_ALIAS": "SOURCE_RECORD"}.get(
            kind, kind
        )
        row["subject_id"] = (
            company_map[original["subject_id"]]
            if kind == "COMPANY"
            else subjects[original["subject_id"]]
        )
        if kind in {"RELATIONSHIP", "REFERRAL"}:
            value = original["value"]
            left_key, right_key = (
                ("referrer_company_id", "referred_company_id")
                if kind == "REFERRAL"
                else ("from_company_id", "to_company_id")
            )
            try:
                left, right = company_map[value[left_key]], company_map[value[right_key]]
            except KeyError:
                raise ValueError(
                    f"{identifier}: extremo sin descubrimiento; proyección detenida."
                ) from None
            relationship_type = "REFERS_TO" if kind == "REFERRAL" else value["relationship_type"]
            if relationship_type == "PARTNERS_WITH":
                left, right = sorted((left, right))
            row["attribute"] = "relationship_claim"
            row["value"] = {
                "from_company_id": left,
                "to_company_id": right,
                "relationship_type": relationship_type,
            }
        row["evidence_note"] = EVIDENCE_PROJECTION.get(identifier, row["evidence_note"])
        for field in ("observed_at", "recorded_at", "available_at"):
            row[field] = iso_time(row[field])
        result.append(row)
    validate_observations(result)
    return result, {"companies": company_map, "subjects": subjects}


def write_projection(
    rows: list[dict], reconciliation: dict, output: Path = Path("data/observable")
) -> None:
    """Escribir únicamente los dos artefactos propios; no borrar archivos del usuario."""
    validate_observations(rows)
    output.mkdir(parents=True, exist_ok=True)
    content = (
        json.dumps({"schema_version": "1.0", "observations": rows}, ensure_ascii=False, indent=2)
        + "\n"
    )
    target = output / "observations.json"
    if not target.exists() or target.read_text(encoding="utf-8") != content:
        target.write_text(content, encoding="utf-8")
    private = Path("data/synthetic/restricted")
    private.mkdir(parents=True, exist_ok=True)
    private.chmod(0o700)
    target = private / "reconciliation.json"
    target.write_text(
        json.dumps(reconciliation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    target.chmod(0o600)
