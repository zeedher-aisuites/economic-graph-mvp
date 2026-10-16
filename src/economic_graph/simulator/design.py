"""Auditoría de insumos aprobados. Este módulo tiene acceso al universo restringido."""

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

from economic_graph.contracts import CUTS, SOURCES, STATUSES, parse_time

FILES = {
    "companies": "companies_world_design.json",
    "relationships": "world_relationships_design.json",
    "claims": "false_claims_design.json",
    "referrals": "referrals_design.json",
    "aliases": "identity_alias_plan.json",
    "discoveries": "company_discovery_plan.json",
    "visibility": "relationship_visibility_plan.json",
    "observations": "observation_plan.json",
}
DEFAULT_DESIGN = Path("design-data/restricted")
SCHEMAS = {
    "companies": (
        "company_id sector display_name size_truth employee_count_truth branch_count_truth "
        "microzone_truth business_operation_truth digital_maturity_truth "
        "connectivity_use_case_truth commercial_constraint_truth seed_crm_t0"
    ),
    "relationships": (
        "relationship_id from_company_id from_company_name to_company_id to_company_name "
        "relationship_type truth_exists plausibility_rationale first_observed_phase planned_source "
        "planned_initial_status observation_caveat"
    ),
    "claims": (
        "claim_id from_company_id to_company_id relationship_type phase source reported_status "
        "truth_status purpose"
    ),
    "referrals": "referral_id referrer_company_id referred_company_id phase source meaning",
    "aliases": "alias_id company_id_truth source_record_name phase source resolution note",
    "discoveries": "company_id company_name first_known_phase first_known_source",
    "visibility": (
        "relationship_id first_observed_phase source status from_company_id to_company_id"
    ),
    "observations": (
        "observation_id phase subject_type subject_id attribute value source_type "
        "verification_status observed_at recorded_at available_at evidence_note "
        "truth_reference conflict_group"
    ),
}


def load_design(directory: Path = DEFAULT_DESIGN) -> dict:
    """Leer todos los archivos, sin completar contenido ausente ni consultar MongoDB."""
    result = {}
    for key, name in FILES.items():
        try:
            rows = json.loads((directory / name).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            raise ValueError(f"No se puede leer el insumo aprobado {name}.") from None
        if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
            raise ValueError(f"{name}: se esperaba una lista de objetos.")
        result[key] = rows
    result["csv_errors"] = []
    for key in ("companies", "relationships", "observations"):
        name = FILES[key].replace(".json", ".csv")
        try:
            with (directory / name).open(encoding="utf-8-sig", newline="") as stream:
                csv_rows = list(csv.DictReader(stream))
        except (OSError, ValueError):
            raise ValueError(f"No se puede leer el insumo aprobado {name}.") from None
        json_rows = result[key]
        if len(csv_rows) != len(json_rows):
            result["csv_errors"].append(f"{name}: cantidad distinta del JSON.")
        for csv_row, json_row in zip(csv_rows, json_rows, strict=False):
            if set(csv_row) != set(json_row):
                result["csv_errors"].append(f"{name}: columnas distintas del JSON.")
                continue
            for field, expected in json_row.items():
                raw = csv_row[field]
                # Los CSV aprobados usan True/False; JSON usa true/false.
                if isinstance(expected, bool):
                    equal = raw.lower() == str(expected).lower()
                elif isinstance(expected, (dict, list)):
                    try:
                        equal = json.loads(raw) == expected
                    except ValueError:
                        equal = False
                else:
                    equal = raw == str(expected)
                if not equal:
                    result["csv_errors"].append(f"{name}: diferencia en {field}.")
    manifest_path = directory.parent / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError("Falta design-data/manifest.json con la procedencia de los insumos.")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    result["integrity_errors"] = []
    for item in manifest["files"]:
        if item["kind"] == "data":
            path = directory / item["name"]
            if (
                not path.is_file()
                or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]
            ):
                result["integrity_errors"].append(f"{item['name']}: SHA-256 distinto del aprobado.")
    return result


def audit_design(data: dict) -> dict:
    """Acumular errores con IDs concretos y distinguir límites documentales de datos inválidos."""
    errors = [*data.get("csv_errors", []), *data.get("integrity_errors", [])]
    for name, fields in SCHEMAS.items():
        for index, row in enumerate(data[name]):
            if set(row) != set(fields.split()):
                errors.append(f"{name}[{index}]: campos obligatorios incompletos o desconocidos.")
    if any("campos obligatorios" in error for error in errors):
        return {"errors": errors, "warnings": [], "counts": {}}

    def check(condition, identifier, message):
        if not condition:
            errors.append(f"{identifier}: {message}")

    identifiers = {
        "companies": ("company_id", 30),
        "relationships": ("relationship_id", 48),
        "claims": ("claim_id", 3),
        "referrals": ("referral_id", 3),
        "aliases": ("alias_id", 2),
        "observations": ("observation_id", 83),
        "discoveries": ("company_id", 30),
        "visibility": ("relationship_id", 48),
    }
    for name, (field, count) in identifiers.items():
        ids = [row.get(field) for row in data[name]]
        check(
            len(ids) == count and len(set(ids)) == count and None not in ids,
            name,
            f"se requieren {count} registros únicos con {field}.",
        )
    companies = {row.get("company_id"): row for row in data["companies"]}
    expected_ids = {f"EMP-{i:03}" for i in range(1, 31)}
    check(set(companies) == expected_ids, "companies", "IDs distintos de EMP-001 a EMP-030.")
    sectors = Counter(row.get("sector") for row in data["companies"])
    check(
        sectors
        == {
            "Panaderías": 3,
            "Logística": 2,
            "Tecnología": 7,
            "Fintech": 4,
            "Restaurantes y cafeterías": 8,
            "Comercio minorista": 6,
        },
        "companies",
        "distribución sectorial distinta de la aprobada.",
    )
    check(
        sum(row.get("seed_crm_t0", 0) for row in data["companies"]) == 12,
        "companies",
        "CRM T0 debe tener 12 identidades.",
    )
    relationships = {row.get("relationship_id"): row for row in data["relationships"]}
    claims = {row.get("claim_id"): row for row in data["claims"]}
    referrals = {row.get("referral_id"): row for row in data["referrals"]}
    aliases = {row.get("alias_id"): row for row in data["aliases"]}
    discoveries = {row.get("company_id"): row for row in data["discoveries"]}
    check(
        set(discoveries) == set(companies), "discoveries", "catálogo de descubrimientos incompleto."
    )
    check(
        {r["relationship_id"] for r in data["visibility"]} == set(relationships),
        "visibility",
        "plan de relaciones incompleto.",
    )
    edge_keys = set()
    for row in [*data["relationships"], *data["claims"]]:
        key = row.get("relationship_id", row.get("claim_id"))
        left, right, kind = (
            row.get(field) for field in ("from_company_id", "to_company_id", "relationship_type")
        )
        check(left in companies and right in companies, key, "extremo huérfano.")
        check(left != right, key, "auto-relación no justificada.")
        check(kind in {"SUPPLIES_TO", "PARTNERS_WITH"}, key, "tipo económico desconocido.")
        if (
            "relationship_id" in row
            and kind == "PARTNERS_WITH"
            and isinstance(left, str)
            and isinstance(right, str)
        ):
            check(left < right, key, "alianza no canonizada.")
        endpoints = (
            sorted((left, right))
            if kind == "PARTNERS_WITH" and isinstance(left, str) and isinstance(right, str)
            else (left, right)
        )
        edge_key = (kind, *endpoints)
        check(
            edge_key not in edge_keys,
            key,
            "arista duplicada o afirmación falsa incluida como verdadera.",
        )
        edge_keys.add(edge_key)
        if "relationship_id" in row:
            check(
                row.get("truth_exists") is True,
                key,
                "la matriz debe contener solo relaciones verdaderas.",
            )
            check(
                row["from_company_name"] == companies.get(left, {}).get("display_name")
                and row["to_company_name"] == companies.get(right, {}).get("display_name"),
                key,
                "nombre de extremo distinto del catálogo.",
            )
        else:
            check(
                row.get("truth_status") == "FALSE",
                key,
                "afirmación falsa sin etiqueta restringida.",
            )
    for row in data["referrals"]:
        check(
            row.get("referrer_company_id") in companies
            and row.get("referred_company_id") in companies,
            row.get("referral_id"),
            "referencia con empresa huérfana.",
        )
        check(
            row.get("referrer_company_id") != row.get("referred_company_id"),
            row.get("referral_id"),
            "auto-referencia no justificada.",
        )
    for row in data["aliases"]:
        check(
            row.get("company_id_truth") in companies and row.get("resolution") == "CANDIDATE",
            row.get("alias_id"),
            "alias sin identidad de conciliación o fusionado sin evidencia.",
        )

    first_known = {}
    observed_relations = {}
    required = {
        "observation_id",
        "phase",
        "subject_type",
        "subject_id",
        "attribute",
        "value",
        "source_type",
        "verification_status",
        "observed_at",
        "recorded_at",
        "available_at",
        "evidence_note",
        "truth_reference",
        "conflict_group",
    }
    for row in data["observations"]:
        identifier = row.get("observation_id", "sin ID")
        check(set(row) == required, identifier, "campos del plan incompletos o desconocidos.")
        if not required <= row.keys():
            continue
        check(
            row["source_type"] in SOURCES and row["verification_status"] in STATUSES,
            identifier,
            "fuente o estado desconocido.",
        )
        check(row["phase"] in CUTS, identifier, "fase desconocida.")
        try:
            times = [
                parse_time(row[field]) for field in ("observed_at", "recorded_at", "available_at")
            ]
            check(times[0] <= times[1] <= times[2], identifier, "fechas fuera de orden.")
            if row["phase"] in CUTS:
                check(
                    times[2] == parse_time(CUTS[row["phase"]]),
                    identifier,
                    "disponibilidad distinta del corte aprobado.",
                )
        except ValueError:
            errors.append(f"{identifier}: fecha inválida o sin zona horaria.")
            continue
        subject, kind = row["subject_id"], row["subject_type"]
        if kind == "COMPANY":
            check(
                subject in companies and row["truth_reference"] == subject,
                identifier,
                "empresa o conciliación huérfana.",
            )
            if row["attribute"] == "display_name":
                check(subject not in first_known, identifier, "descubrimiento duplicado.")
                first_known[subject] = times[2]
                discovery = discoveries.get(subject, {})
                check(
                    discovery.get("first_known_phase") == row["phase"]
                    and discovery.get("first_known_source") == row["source_type"],
                    identifier,
                    "descubrimiento no coincide con el plan.",
                )
                check(
                    row["value"] == discovery.get("company_name"),
                    identifier,
                    "nombre de descubrimiento distinto del aprobado.",
                )
        elif kind == "RELATIONSHIP":
            reference = relationships.get(subject, claims.get(subject))
            check(
                reference is not None and row["truth_reference"] == subject,
                identifier,
                "relación o afirmación huérfana.",
            )
            if reference:
                expected = {
                    field: reference[field]
                    for field in ("from_company_id", "to_company_id", "relationship_type")
                }
                check(row["value"] == expected, identifier, "extremos/tipo distintos de la matriz.")
                check(
                    row["source_type"] == reference.get("planned_source", reference.get("source"))
                    and row["verification_status"]
                    == reference.get("planned_initial_status", reference.get("reported_status")),
                    identifier,
                    "fuente/estado distintos de la matriz.",
                )
            if subject in relationships:
                observed_relations[subject] = times[2]
        elif kind == "REFERRAL":
            reference = referrals.get(subject, {})
            expected = {
                field: reference.get(field)
                for field in ("referrer_company_id", "referred_company_id")
            }
            check(
                bool(reference) and row["value"] == expected and row["truth_reference"] == subject,
                identifier,
                "referencia comercial huérfana o alterada.",
            )
            check(
                reference.get("phase") == row["phase"]
                and reference.get("source") == row["source_type"]
                and row["verification_status"] == "REPORTED",
                identifier,
                "fase/fuente/estado de referencia distintos del plan.",
            )
        elif kind == "COMPANY_ALIAS":
            reference = aliases.get(subject, {})
            check(
                bool(reference)
                and row["truth_reference"] == reference.get("company_id_truth")
                and row["value"] == reference.get("source_record_name"),
                identifier,
                "alias huérfano o alterado.",
            )
            check(
                reference.get("phase") == row["phase"]
                and reference.get("source") == row["source_type"],
                identifier,
                "fase o fuente del alias distinta del plan.",
            )
        else:
            errors.append(f"{identifier}: tipo de sujeto desconocido.")

    for row in data["observations"]:
        try:
            when = parse_time(row["available_at"])
        except (ValueError, KeyError):
            continue
        endpoints = []
        if row.get("subject_type") == "COMPANY":
            endpoints = [row["subject_id"]]
        elif row.get("subject_type") in {"RELATIONSHIP", "REFERRAL"} and isinstance(
            row.get("value"), dict
        ):
            endpoints = [value for key, value in row["value"].items() if key.endswith("company_id")]
        check(
            all(key in first_known and first_known[key] <= when for key in endpoints),
            row.get("observation_id"),
            "empresa no identificable al estar disponible la observación.",
        )
    for row in data["visibility"]:
        identifier = row["relationship_id"]
        original = relationships.get(identifier, {})
        expected = {
            "first_observed_phase": original.get("first_observed_phase"),
            "source": original.get("planned_source"),
            "status": original.get("planned_initial_status"),
            "from_company_id": original.get("from_company_id"),
            "to_company_id": original.get("to_company_id"),
        }
        check(
            all(row.get(k) == v for k, v in expected.items()),
            identifier,
            "plan de visibilidad distinto de la matriz.",
        )
        phase = row.get("first_observed_phase")
        check(
            phase == "NEVER"
            and identifier not in observed_relations
            or phase in CUTS
            and observed_relations.get(identifier) == parse_time(CUTS[phase]),
            identifier,
            "observaciones no cumplen el plan temporal de la relación.",
        )
    counts = {
        "companies": len(companies),
        "relationships": len(relationships),
        "false_claims": len(claims),
        "referrals": len(referrals),
        "observations": len(data["observations"]),
        "cuts": {},
    }
    for phase, company_count, relation_count in [("T0", 12, 2), ("T1", 17, 11), ("T2", 23, 23)]:
        cut = parse_time(CUTS[phase])
        known = {key for key, when in first_known.items() if when <= cut}
        visible = {key for key, when in observed_relations.items() if when <= cut}
        counts["cuts"][phase] = {
            "companies": len(known),
            "planned_true_relationships": len(visible),
        }
        check(
            len(known) == company_count,
            phase,
            "cantidad de empresas observable distinta de la aprobada.",
        )
        check(
            len(visible) == relation_count,
            phase,
            "cantidad de relaciones verdaderas observadas distinta de la aprobada.",
        )
    check(
        {key for key in first_known if discoveries.get(key, {}).get("first_known_phase") == "T0"}
        == {key for key, row in companies.items() if row.get("seed_crm_t0") == 1},
        "T0",
        "semilla CRM distinta del catálogo.",
    )
    check(
        set(first_known)
        == {key for key, row in discoveries.items() if row.get("first_known_phase") != "NEVER"},
        "discoveries",
        "aparece una empresa no planificada o falta un descubrimiento.",
    )
    counts["unknown_companies_t2"] = len(companies) - len(first_known)
    counts["unknown_true_relationships_t2"] = len(relationships) - len(observed_relations)
    warnings = [
        "DV-001: OBS-043/044/073 contienen diagnósticos del oráculo en texto; "
        "deben proyectarse sin revelar falsedad.",
        "DV-002: ALIAS-001/002 solo tienen evidencia de candidato; no se autoriza ninguna fusión.",
        "DV-003: no hay transiciones ni caducidades de relaciones en las 83 observaciones; "
        "no inventarlas.",
        "DV-004: source_record_id no viene en el plan; "
        "se asigna una clave técnica por observación, sin inventar evidencia.",
        "DV-005: CLM-003 conserva orientación de fuente; PARTNERS_WITH se canoniza solo en la "
        "proyección, por ser simétrica.",
    ]
    return {"errors": errors, "warnings": warnings, "counts": counts}
