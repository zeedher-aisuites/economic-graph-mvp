"""Contrato público: fechas explícitas, tipos y validación sin acceso al simulador."""

from datetime import UTC, datetime

CUTS = {
    "T0": "2026-01-15T12:00:00Z",
    "T1": "2026-05-15T12:00:00Z",
    "T2": "2026-09-15T12:00:00Z",
}
SOURCES = {"CRM", "TELCO_INTERNAL", "DIRECTORY", "PUBLIC_PROFILE", "REFERRAL"}
STATUSES = {"CONFIRMED", "REPORTED", "INFERRED", "DISCARDED"}
RELATION_TYPES = {"SUPPLIES_TO", "PARTNERS_WITH", "REFERS_TO"}
COMPANY_ATTRIBUTES = {
    "display_name",
    "sector",
    "size",
    "branch_count",
    "public_rating",
    "review_count",
    "service_active",
}
OBSERVATION_FIELDS = {
    "observation_id",
    "subject_type",
    "subject_id",
    "attribute",
    "value",
    "source_type",
    "source_record_id",
    "verification_status",
    "observed_at",
    "recorded_at",
    "available_at",
    "evidence_note",
    "conflict_group",
}


def parse_time(value: str | datetime) -> datetime:
    """Aceptar un corte nombrado o un instante con zona; nunca suponer fin de día."""
    try:
        instant = (
            value
            if isinstance(value, datetime)
            else datetime.fromisoformat(CUTS.get(value, value).replace("Z", "+00:00"))
        )
        if instant.tzinfo is None or instant.utcoffset() is None:
            raise ValueError
        return instant.astimezone(UTC)
    except (ValueError, TypeError, AttributeError):
        raise ValueError(
            "La fecha debe ser T0/T1/T2 o un instante ISO 8601 con zona horaria."
        ) from None


def iso_time(value: str | datetime) -> str:
    return parse_time(value).isoformat().replace("+00:00", "Z")


def assert_no_private_fields(value: object) -> None:
    """Rechazar metadatos del oráculo incluso dentro de listas y objetos anidados."""
    if isinstance(value, dict):
        for key, item in value.items():
            if "truth" in key.lower() or key in {"seed_crm_t0", "first_observed_phase"}:
                raise ValueError(
                    "El registro observable contiene campos restringidos del simulador."
                )
            assert_no_private_fields(item)
    elif isinstance(value, list):
        for item in value:
            assert_no_private_fields(item)


def validate_observations(rows: list[dict]) -> None:
    """Validar el ledger observable antes de consultarlo o enviarlo a MongoDB."""
    seen = set()
    for row in rows:
        identifier = row.get("observation_id", "sin ID")
        assert_no_private_fields(row)
        if set(row) != OBSERVATION_FIELDS:
            raise ValueError(f"{identifier}: campos observables incompletos o desconocidos.")
        if not isinstance(identifier, str) or not identifier or identifier in seen:
            raise ValueError(f"{identifier}: ID de observación vacío o duplicado.")
        seen.add(identifier)
        if row["source_type"] not in SOURCES or row["verification_status"] not in STATUSES:
            raise ValueError(f"{identifier}: fuente o estado desconocido.")
        for field in ("subject_id", "source_record_id", "evidence_note"):
            if not isinstance(row[field], str) or not row[field].strip():
                raise ValueError(f"{identifier}: falta {field}.")
        dates = [parse_time(row[field]) for field in ("observed_at", "recorded_at", "available_at")]
        if not dates[0] <= dates[1] <= dates[2]:
            raise ValueError(f"{identifier}: fechas fuera de orden.")
        kind, attribute, value = row["subject_type"], row["attribute"], row["value"]
        if kind == "COMPANY":
            if attribute not in COMPANY_ATTRIBUTES or not row["subject_id"].startswith("CO-"):
                raise ValueError(f"{identifier}: atributo o identidad de empresa inválido.")
            if attribute in {"display_name", "sector", "size"}:
                valid = isinstance(value, str) and bool(value.strip())
            elif attribute == "service_active":
                valid = isinstance(value, bool)
            elif attribute in {"branch_count", "review_count"}:
                valid = type(value) is int and value >= (1 if attribute == "branch_count" else 0)
            else:
                valid = type(value) in (int, float) and 0 <= value <= 5
            if not valid:
                raise ValueError(f"{identifier}: valor incompatible con {attribute}.")
        elif kind == "RELATIONSHIP":
            required = {"from_company_id", "to_company_id", "relationship_type"}
            if (
                attribute != "relationship_claim"
                or not isinstance(value, dict)
                or set(value) != required
            ):
                raise ValueError(f"{identifier}: contrato de relación inválido.")
            if value["relationship_type"] not in RELATION_TYPES:
                raise ValueError(f"{identifier}: tipo de relación desconocido.")
            left, right = value["from_company_id"], value["to_company_id"]
            if left == right or not all(
                isinstance(v, str) and v.startswith("CO-") for v in (left, right)
            ):
                raise ValueError(f"{identifier}: extremos de relación inválidos o auto-relación.")
            if value["relationship_type"] == "PARTNERS_WITH" and left > right:
                raise ValueError(f"{identifier}: alianza sin orientación canónica.")
            if not row["subject_id"].startswith("LINK-"):
                raise ValueError(f"{identifier}: identidad de relación inválida.")
        elif kind == "SOURCE_RECORD":
            if attribute != "alias_name" or not isinstance(value, str) or not value.strip():
                raise ValueError(f"{identifier}: contrato de alias inválido.")
            if not row["subject_id"].startswith("REC-"):
                raise ValueError(f"{identifier}: identidad de registro inválida.")
        else:
            raise ValueError(f"{identifier}: tipo de sujeto desconocido.")

    first_known = {}
    for row in rows:
        if row["subject_type"] == "COMPANY" and row["attribute"] == "display_name":
            key = row["subject_id"]
            first_known[key] = min(
                first_known.get(key, parse_time(row["available_at"])),
                parse_time(row["available_at"]),
            )
    for row in rows:
        endpoints = []
        if row["subject_type"] == "COMPANY":
            endpoints = [row["subject_id"]]
        elif row["subject_type"] == "RELATIONSHIP":
            endpoints = [row["value"][key] for key in ("from_company_id", "to_company_id")]
        if any(
            key not in first_known or first_known[key] > parse_time(row["available_at"])
            for key in endpoints
        ):
            raise ValueError(
                f"{row['observation_id']}: empresa huérfana o no identificable al conocer el dato."
            )
