"""Contrato del comando: códigos de salida y mensajes, sin conexión de red."""

import runpy
from pathlib import Path
from unittest.mock import Mock

import pytest

from economic_graph import config, database

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_connection.py"


def test_command_reports_success_after_ping(monkeypatch, capsys):
    monkeypatch.setattr(config, "load_config", lambda: ("mongodb://localhost", "conectapyme"))
    ping = Mock()
    monkeypatch.setattr(database, "check_connection", ping)

    with pytest.raises(SystemExit) as result:
        runpy.run_path(str(SCRIPT), run_name="__main__")

    assert result.value.code == 0
    ping.assert_called_once_with("mongodb://localhost", "conectapyme")
    captured = capsys.readouterr()
    assert "MongoDB respondió a ping" in captured.out
    assert captured.err == ""


@pytest.mark.parametrize("stage", ["config", "database"])
def test_command_reports_controlled_failure_without_traceback(monkeypatch, capsys, stage):
    loader = Mock(return_value=("mongodb://usuario:secreto@localhost", "conectapyme"))
    ping = Mock()
    if stage == "config":
        loader.side_effect = ValueError("Falta configuración obligatoria: MONGODB_DATABASE.")
    else:
        ping.side_effect = ConnectionError("No se pudo contactar con MongoDB.")
    monkeypatch.setattr(config, "load_config", loader)
    monkeypatch.setattr(database, "check_connection", ping)

    with pytest.raises(SystemExit) as result:
        runpy.run_path(str(SCRIPT), run_name="__main__")

    assert result.value.code == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err.startswith("Error: ")
    assert "secreto" not in captured.err
    assert "mongodb://" not in captured.err
    assert "Traceback" not in captured.err
    if stage == "config":
        ping.assert_not_called()
