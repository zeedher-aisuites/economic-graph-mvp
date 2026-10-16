"""Persistencia del ledger público en una base dedicada; sin acceso al diseño privado."""

from copy import deepcopy
from datetime import UTC, datetime

from economic_graph.contracts import iso_time, parse_time, validate_observations

MVP_DATABASE = "conectapyme_mvp_observable"
OBSERVATIONS = "m002b_observations"
METADATA = "m002b_metadata"
OWNER = {"_id": "mission-002b", "owner": "conectapyme-m002b", "schema_version": "1.0"}


def require_dedicated_database(database) -> None:
    if database.name != MVP_DATABASE:
        raise ValueError(f"Operación detenida: solo se permite la base dedicada {MVP_DATABASE}.")


def _to_document(row: dict) -> dict:
    result = deepcopy(row)
    for field in ("observed_at", "recorded_at", "available_at"):
        result[field] = parse_time(result[field])
    result["_id"] = result["observation_id"]
    return result


def _from_document(document: dict) -> dict:
    result = deepcopy(document)
    result.pop("_id", None)
    for field in ("observed_at", "recorded_at", "available_at"):
        value = result[field]
        # BSON conserva instantes UTC; PyMongo sin codec tz_aware los devuelve sin tzinfo.
        if isinstance(value, datetime) and value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        result[field] = iso_time(value)
    return result


def load_observable(database, rows: list[dict]) -> dict:
    """Agregar registros inmutables idempotentemente; jamás borrar ni reemplazar documentos."""
    require_dedicated_database(database)
    validate_observations(rows)
    names = set(database.list_collection_names())
    if names - {OBSERVATIONS, METADATA}:
        raise ValueError("La base contiene colecciones ajenas; no se escribirá en ella.")
    owner = database[METADATA].find_one({"_id": OWNER["_id"]})
    if owner != OWNER and (owner is not None or OBSERVATIONS in names or METADATA in names):
        raise ValueError("Las colecciones existentes no tienen una marca de propiedad compatible.")
    collection = database[OBSERVATIONS]
    # Revisar TODAS las colisiones antes de comenzar; no sobrescribir una versión distinta.
    documents = [_to_document(row) for row in rows]
    for document in documents:
        existing = collection.find_one({"_id": document["_id"]})
        if existing is not None and _from_document(existing) != _from_document(document):
            raise ValueError(
                f"{document['_id']}: existe otro contenido; carga detenida sin reemplazarlo."
            )
    database[METADATA].update_one({"_id": OWNER["_id"]}, {"$setOnInsert": OWNER}, upsert=True)
    collection.create_index([("available_at", 1)], name="available_at")
    collection.create_index([("subject_id", 1), ("available_at", 1)], name="subject_available")
    inserted = 0
    for document in documents:
        result = collection.update_one(
            {"_id": document["_id"]}, {"$setOnInsert": document}, upsert=True
        )
        inserted += result.upserted_id is not None
        if _from_document(collection.find_one({"_id": document["_id"]})) != _from_document(
            document
        ):
            raise ValueError("Colisión concurrente detectada; no se reemplazó ningún documento.")
    return {
        "observations_checked": len(rows),
        "inserted": inserted,
        "unchanged": len(rows) - inserted,
    }


def read_observations(database, as_of: str, company_id: str | None = None) -> list[dict]:
    """Solo lectura sobre la colección pública; el filtro temporal se ejecuta en MongoDB."""
    require_dedicated_database(database)
    query = {"available_at": {"$lte": parse_time(as_of)}}
    if company_id is not None:
        if not isinstance(company_id, str) or not company_id.startswith("CO-"):
            raise ValueError("La consulta de historial requiere una identidad observable CO-.")
        query["subject_id"] = company_id
    cursor = database[OBSERVATIONS].find(query)
    rows = [_from_document(document) for document in cursor]
    validate_observations(rows)
    return rows
