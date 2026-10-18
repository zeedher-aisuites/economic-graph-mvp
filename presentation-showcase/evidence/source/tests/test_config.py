"""Configuración obligatoria, precedencia del entorno y validaciones sin secretos."""

import os

import pytest

from economic_graph.config import load_config


@pytest.fixture(autouse=True)
def clean_mongodb_environment(monkeypatch):
    for name in ("MONGODB_URI", "MONGODB_DATABASE"):
        monkeypatch.delenv(name, raising=False)


def test_loads_dotenv_without_modifying_process_environment(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "MONGODB_URI=mongodb://localhost:27017\nMONGODB_DATABASE=conectapyme\n",
        encoding="utf-8",
    )

    assert load_config(env_file) == ("mongodb://localhost:27017", "conectapyme")
    assert "MONGODB_URI" not in os.environ
    assert "MONGODB_DATABASE" not in os.environ


def test_process_environment_takes_precedence(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "MONGODB_URI=mongodb://archivo:27017\nMONGODB_DATABASE=archivo\n", encoding="utf-8"
    )
    monkeypatch.setenv("MONGODB_URI", "mongodb://proceso:27017")
    monkeypatch.setenv("MONGODB_DATABASE", "proceso")

    assert load_config(env_file) == ("mongodb://proceso:27017", "proceso")


def test_empty_environment_value_does_not_fall_back_to_file(monkeypatch, tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "MONGODB_URI=mongodb://localhost\nMONGODB_DATABASE=conectapyme\n", encoding="utf-8"
    )
    monkeypatch.setenv("MONGODB_DATABASE", "")

    with pytest.raises(ValueError, match="MONGODB_DATABASE"):
        load_config(env_file)


@pytest.mark.parametrize("missing_name", ["MONGODB_URI", "MONGODB_DATABASE"])
@pytest.mark.parametrize("missing_value", [None, "", "   "])
def test_rejects_missing_configuration(monkeypatch, tmp_path, missing_name, missing_value):
    monkeypatch.setenv("MONGODB_URI", "mongodb://usuario:secreto@example.invalid")
    monkeypatch.setenv("MONGODB_DATABASE", "conectapyme")
    if missing_value is None:
        monkeypatch.delenv(missing_name)
    else:
        monkeypatch.setenv(missing_name, missing_value)

    with pytest.raises(ValueError, match=missing_name) as error:
        load_config(tmp_path / "archivo-ausente")

    assert "secreto" not in str(error.value)
    assert "example.invalid" not in str(error.value)


@pytest.mark.parametrize(
    "uri", ["https://usuario:secreto@example.invalid", "mongodb://host con espacio"]
)
def test_rejects_invalid_uri_without_echoing_it(monkeypatch, tmp_path, uri):
    monkeypatch.setenv("MONGODB_URI", uri)
    monkeypatch.setenv("MONGODB_DATABASE", "conectapyme")

    with pytest.raises(ValueError, match="MONGODB_URI") as error:
        load_config(tmp_path / "archivo-ausente")

    assert uri not in str(error.value)


@pytest.mark.parametrize(
    "database", ["con espacio", "base.nombre", "base/otra", "a" * 64, "é" * 32]
)
def test_rejects_invalid_database_names(monkeypatch, tmp_path, database):
    monkeypatch.setenv("MONGODB_URI", "mongodb://localhost")
    monkeypatch.setenv("MONGODB_DATABASE", database)

    with pytest.raises(ValueError, match="MONGODB_DATABASE"):
        load_config(tmp_path / "archivo-ausente")


def test_preserves_literal_credentials_without_interpolation(tmp_path):
    env_file = tmp_path / ".env"
    uri = "mongodb://usuario:${NO_EXPANDIR}@localhost"
    env_file.write_text(f"MONGODB_URI='{uri}'\nMONGODB_DATABASE=conectapyme\n", encoding="utf-8")

    assert load_config(env_file) == (uri, "conectapyme")


def test_accepts_srv_without_making_a_dns_request(monkeypatch, tmp_path):
    monkeypatch.setenv("MONGODB_URI", "mongodb+srv://usuario:ejemplo@cluster.example.invalid")
    monkeypatch.setenv("MONGODB_DATABASE", "conectapyme")

    assert load_config(tmp_path / "archivo-ausente")[1] == "conectapyme"


def test_reports_unreadable_encoding_without_exposing_contents(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_bytes(b"MONGODB_URI=secreto\xff")

    with pytest.raises(ValueError, match="UTF-8") as error:
        load_config(env_file)

    assert "secreto" not in str(error.value)
    assert error.value.__suppress_context__
