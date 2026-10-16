"""Los comandos comerciales son de solo lectura y la carga es opt-in."""

import json
import runpy
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from economic_graph import config, database
from economic_graph.mongo_observable import MVP_DATABASE

ROOT = Path(__file__).resolve().parents[1]


def run_script(monkeypatch, name, arguments):
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(sys, "argv", [name, *arguments])
    with pytest.raises(SystemExit) as result:
        runpy.run_path(str(ROOT / "scripts" / name), run_name="__main__")
    return result.value.code


def test_default_and_explicit_dry_run_never_read_credentials_or_create_client(monkeypatch, capsys):
    loader = Mock(side_effect=AssertionError("No debe leer .env"))
    factory = Mock(side_effect=AssertionError("No debe abrir MongoDB"))
    monkeypatch.setattr(config, "load_config", loader)
    monkeypatch.setattr(database, "create_client", factory)
    for arguments in ([], ["--dry-run"]):
        assert run_script(monkeypatch, "load_observable.py", arguments) == 0
        report = json.loads(capsys.readouterr().out)
        assert report["mode"] == "dry-run" and report["observations"] == 83
    loader.assert_not_called()
    factory.assert_not_called()


def test_apply_requires_literal_database_confirmation(monkeypatch, capsys):
    assert run_script(monkeypatch, "load_observable.py", ["--apply"]) == 2
    assert "--confirm-database" in capsys.readouterr().err


def test_apply_rejects_wrong_environment_database_before_connecting(monkeypatch, capsys):
    monkeypatch.setattr(
        config, "load_config", lambda: ("mongodb://usuario:secreto@localhost", "production")
    )
    factory = Mock(side_effect=AssertionError("No debe abrir MongoDB"))
    monkeypatch.setattr(database, "create_client", factory)
    assert (
        run_script(
            monkeypatch, "load_observable.py", ["--apply", "--confirm-database", MVP_DATABASE]
        )
        == 1
    )
    message = capsys.readouterr().err
    assert "base dedicada" in message and "secreto" not in message
    factory.assert_not_called()


@pytest.mark.parametrize("cut, count", [("T0", 12), ("T1", 17), ("T2", 23)])
def test_inspection_command_runs_without_design_access_or_mongo(monkeypatch, capsys, cut, count):
    factory = Mock(side_effect=AssertionError("Sin MongoDB"))
    monkeypatch.setattr(database, "create_client", factory)
    assert run_script(monkeypatch, "inspect_graph.py", ["--as-of", cut, "--summary"]) == 0
    assert json.loads(capsys.readouterr().out)["companies"] == count
    factory.assert_not_called()


def test_inspection_rejects_date_without_time_or_timezone(monkeypatch, capsys):
    assert run_script(monkeypatch, "inspect_graph.py", ["--as-of", "2026-01-15"]) == 1
    assert "zona horaria" in capsys.readouterr().err


def test_build_dry_run_does_not_invoke_writer(monkeypatch, capsys):
    from economic_graph.simulator import project

    writer = Mock(side_effect=AssertionError("Dry-run no puede escribir"))
    monkeypatch.setattr(project, "write_projection", writer)
    assert run_script(monkeypatch, "build_observable.py", ["--dry-run"]) == 0
    assert json.loads(capsys.readouterr().out) == {"mode": "dry-run", "observations": 83}
    writer.assert_not_called()
