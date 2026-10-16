"""Integración opcional y explícita; nunca modificar una base ajena o de producción."""

import os

import pytest

from economic_graph.config import load_config
from economic_graph.database import create_client
from economic_graph.mongo_observable import MVP_DATABASE, load_observable, read_observations
from economic_graph.observable import load_observations, snapshot, summarize


@pytest.mark.integration
@pytest.mark.skipif(
    os.environ.get("RUN_MONGODB_INTEGRATION") != "1"
    or os.environ.get("MONGODB_INTEGRATION_DATABASE_CONFIRM") != MVP_DATABASE,
    reason="Integración real no verificada: requiere activación explícita y base dedicada.",
)
def test_dedicated_database_roundtrip():
    uri, name = load_config()
    assert name == MVP_DATABASE, "La prueba no puede escribir fuera de la base dedicada."
    rows = load_observations()
    with create_client(uri) as client:
        database = client[name]
        database.command("ping")
        load_observable(database, rows)
        repeated = load_observable(database, rows)
        assert repeated["inserted"] == 0
        assert repeated["unchanged"] == 83
        for cut, companies, observations in [("T0", 12, 28), ("T1", 17, 54), ("T2", 23, 83)]:
            summary = summarize(snapshot(read_observations(database, cut), cut))
            assert summary["companies"] == companies
            assert summary["observations"] == observations
