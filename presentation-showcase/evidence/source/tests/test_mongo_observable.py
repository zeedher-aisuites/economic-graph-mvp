"""Dobles mínimos de MongoDB para probar idempotencia y protección de datos ajenos."""

from copy import deepcopy
from types import SimpleNamespace

import pytest

from economic_graph.contracts import parse_time
from economic_graph.mongo_observable import (
    METADATA,
    MVP_DATABASE,
    OBSERVATIONS,
    OWNER,
    load_observable,
    read_observations,
)
from economic_graph.observable import snapshot, summarize


class MemoryCollection:
    """Doble inmutable: solo implementa las operaciones permitidas por el cargador."""

    def __init__(self):
        self.documents = {}
        self.indexes = {}
        self.created = False
        self.writes = 0
        self.queries = []

    def find_one(self, query):
        return deepcopy(self.documents.get(query["_id"]))

    def update_one(self, query, update, upsert):
        assert upsert and set(update) == {"$setOnInsert"}
        self.created = True
        key = query["_id"]
        inserted = key not in self.documents
        if inserted:
            self.documents[key] = deepcopy(update["$setOnInsert"])
            self.writes += 1
        return SimpleNamespace(upserted_id=key if inserted else None)

    def create_index(self, keys, name):
        self.created = True
        self.indexes[name] = keys

    def find(self, query):
        self.queries.append(deepcopy(query))
        cut = query["available_at"]["$lte"]
        return [
            deepcopy(doc)
            for doc in self.documents.values()
            if parse_time(doc["available_at"]) <= cut
            and ("subject_id" not in query or doc["subject_id"] == query["subject_id"])
        ]


class MemoryDatabase:
    def __init__(self, name=MVP_DATABASE):
        self.name = name
        self.collections = {}

    def __getitem__(self, name):
        return self.collections.setdefault(name, MemoryCollection())

    def list_collection_names(self):
        return [name for name, collection in self.collections.items() if collection.created]


def test_repeated_load_is_idempotent_for_observations_companies_and_edges(projection):
    rows, _ = projection
    database = MemoryDatabase()
    assert load_observable(database, rows) == {
        "observations_checked": 83,
        "inserted": 83,
        "unchanged": 0,
    }
    before = deepcopy(database[OBSERVATIONS].documents)
    assert load_observable(database, rows) == {
        "observations_checked": 83,
        "inserted": 0,
        "unchanged": 83,
    }
    assert database[OBSERVATIONS].documents == before
    assert len(before) == 83
    for cut, companies, claims in [("T0", 12, 2), ("T1", 17, 13), ("T2", 23, 26)]:
        summary = summarize(snapshot(read_observations(database, cut), cut))
        assert summary["companies"] == companies
        assert summary["relationship_claims"] == claims
    assert database[OBSERVATIONS].queries[-1] == {"available_at": {"$lte": parse_time("T2")}}
    assert database[METADATA].find_one({"_id": OWNER["_id"]}) == OWNER


@pytest.mark.parametrize(
    "name", ["production", "conectapyme", "admin", "conectapyme_mvp_observable_backup"]
)
def test_wrong_database_is_rejected_before_any_access(projection, name):
    database = MemoryDatabase(name)
    with pytest.raises(ValueError, match="base dedicada"):
        load_observable(database, projection[0])
    assert database.collections == {}
    with pytest.raises(ValueError, match="base dedicada"):
        read_observations(database, "T0")
    assert database.collections == {}


@pytest.mark.parametrize("collection", ["customers", OBSERVATIONS, METADATA])
def test_unowned_collections_are_left_untouched(projection, collection):
    database = MemoryDatabase()
    database[collection].created = True
    database[collection].documents["foreign"] = {"_id": "foreign", "content": "conservar"}
    before = deepcopy(database[collection].documents)
    with pytest.raises(ValueError, match="ajenas|propiedad"):
        load_observable(database, projection[0])
    assert database[collection].documents == before
    assert sum(item.writes for item in database.collections.values()) == 0


def test_changed_existing_document_is_rejected_before_any_new_write(projection):
    rows, _ = projection
    database = MemoryDatabase()
    load_observable(database, rows)
    before_writes = sum(item.writes for item in database.collections.values())
    last_id = rows[-1]["observation_id"]
    database[OBSERVATIONS].documents[last_id]["evidence_note"] = "Nota cambiada por otra operación"
    before = deepcopy(database[OBSERVATIONS].documents)
    with pytest.raises(ValueError, match=last_id):
        load_observable(database, rows)
    assert database[OBSERVATIONS].documents == before
    assert sum(item.writes for item in database.collections.values()) == before_writes


def test_naive_bson_utc_dates_are_normalized_on_read(projection):
    database = MemoryDatabase()
    load_observable(database, projection[0])
    for doc in database[OBSERVATIONS].documents.values():
        for field in ("observed_at", "recorded_at", "available_at"):
            doc[field] = doc[field].replace(tzinfo=None)
    # El doble emula la comparación de instantes BSON del servidor.
    collection = database[OBSERVATIONS]
    collection.find = lambda query: [
        deepcopy(doc)
        for doc in collection.documents.values()
        if doc["available_at"] <= query["available_at"]["$lte"].replace(tzinfo=None)
    ]
    assert len(snapshot(read_observations(database, "T0"), "T0")["companies"]) == 12


def test_company_history_filters_by_subject_and_availability_in_mongo(projection):
    rows, private = projection
    database = MemoryDatabase()
    load_observable(database, rows)
    company_id = private["companies"]["EMP-002"]
    history = read_observations(database, "T1", company_id=company_id)
    assert {row["subject_id"] for row in history} == {company_id}
    assert {row["observation_id"] for row in history} == {
        "OBS-003",
        "OBS-004",
        "OBS-028",
        "OBS-047",
    }
    assert database[OBSERVATIONS].queries[-1] == {
        "subject_id": company_id,
        "available_at": {"$lte": parse_time("T1")},
    }
