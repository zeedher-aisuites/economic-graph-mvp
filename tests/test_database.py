"""Dobles de PyMongo: ping, errores, tiempos de espera y cierre del cliente."""

from unittest.mock import MagicMock, call

import pytest
from pymongo.errors import (
    ConfigurationError,
    InvalidURI,
    OperationFailure,
    PyMongoError,
    ServerSelectionTimeoutError,
)

from economic_graph import database


@pytest.fixture
def client_factory(monkeypatch):
    factory = MagicMock()
    client = factory.return_value
    client.__enter__.return_value = client
    client.__getitem__.return_value.command.return_value = {"ok": 1.0}
    monkeypatch.setattr(database, "MongoClient", factory)
    return factory


def test_client_is_lazy_and_has_bounded_timeouts(client_factory):
    client = database.create_client("mongodb://localhost")

    assert client is client_factory.return_value
    client_factory.assert_called_once_with(
        "mongodb://localhost",
        serverSelectionTimeoutMS=5_000,
        connectTimeoutMS=5_000,
        socketTimeoutMS=5_000,
        timeoutMS=5_000,
        connect=False,
    )


def test_ping_targets_selected_database_without_writing(client_factory):
    database.check_connection("mongodb://localhost", "conectapyme")

    client = client_factory.return_value
    assert client.mock_calls == [
        call.__enter__(),
        call.__getitem__("conectapyme"),
        call.__getitem__().command("ping"),
        call.__exit__(None, None, None),
    ]


@pytest.mark.parametrize("response", [{"ok": 0}, {}])
def test_rejects_unconfirmed_ping_and_releases_client(client_factory, response):
    client = client_factory.return_value
    client.__getitem__.return_value.command.return_value = response

    with pytest.raises(ConnectionError, match="no confirmó"):
        database.check_connection("mongodb://localhost", "conectapyme")

    client.__exit__.assert_called_once()


@pytest.mark.parametrize(
    ("driver_error", "expected_message"),
    [
        (ServerSelectionTimeoutError("URI con secreto"), "tiempo límite"),
        (OperationFailure("URI con secreto", code=18), "autenticación"),
        (OperationFailure("URI con secreto", code=13), "permisos"),
        (OperationFailure("URI con secreto", code=2), "rechazó ping"),
        (PyMongoError("URI con secreto"), "No se pudo comprobar"),
        (ValueError("URI con secreto"), "No se pudo comprobar"),
    ],
)
def test_driver_errors_are_sanitized_and_client_released(
    client_factory, driver_error, expected_message
):
    client = client_factory.return_value
    client.__getitem__.return_value.command.side_effect = driver_error

    with pytest.raises(ConnectionError, match=expected_message) as error:
        database.check_connection("mongodb://usuario:secreto@localhost", "conectapyme")

    assert "secreto" not in str(error.value)
    assert error.value.__suppress_context__
    client.__exit__.assert_called_once()


@pytest.mark.parametrize("error_type", [InvalidURI, ConfigurationError, ValueError])
def test_client_creation_errors_do_not_expose_uri(client_factory, error_type):
    client_factory.side_effect = error_type("mongodb://usuario:secreto@localhost")

    with pytest.raises(ConnectionError, match="crear el cliente") as error:
        database.check_connection("mongodb://usuario:secreto@localhost", "conectapyme")

    assert "secreto" not in str(error.value)
    assert error.value.__suppress_context__
