"""CLI reproducible: lectura pública offline y MongoDB simulado sin escritura."""

import json
import os
import runpy
import shutil
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock

import pytest
from pymongo.errors import OperationFailure

from economic_graph import config, database
from economic_graph.contracts import CUTS, parse_time
from economic_graph.mongo_observable import MVP_DATABASE, OBSERVATIONS
from economic_graph.observable import load_observations
from economic_graph.rankings import compare_rankings, render_comparison

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/rank_companies.py"


def run(monkeypatch, arguments):
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(sys, "argv", ["rank_companies.py", *arguments])
    with pytest.raises(SystemExit) as result:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    return result.value.code


def test_offline_never_loads_credentials_or_connects(monkeypatch, capsys):
    loader = Mock(side_effect=AssertionError("Sin .env"))
    factory = Mock(side_effect=AssertionError("Sin MongoDB"))
    monkeypatch.setattr(config, "load_config", loader)
    monkeypatch.setattr(database, "create_client", factory)
    assert run(monkeypatch, ["--all-cuts"]) == 0
    reports = json.loads(capsys.readouterr().out)
    assert [report["eligible_companies"] for report in reports] == [12, 17, 21]
    loader.assert_not_called()
    factory.assert_not_called()


def test_markdown_is_reproducible(monkeypatch, capsys):
    rows = load_observations(ROOT / "data/observable/observations.json")
    assert run(monkeypatch, ["--all-cuts", "--format", "markdown"]) == 0
    expected = "\n".join(render_comparison(compare_rankings(rows, cut)) for cut in CUTS)
    assert capsys.readouterr().out == expected
    assert (ROOT / "docs/13-ranking-comparison.md").read_text(encoding="utf-8").endswith(expected)


def test_cli_runs_with_only_public_package_and_ledger(tmp_path):
    # No existe el simulador en el paquete copiado, ni diseños ni .env en el cwd aislado.
    package = tmp_path / "economic_graph"
    package.mkdir()
    for name in (
        "__init__",
        "rankings",
        "observable",
        "contracts",
        "config",
        "database",
        "mongo_observable",
    ):
        shutil.copyfile(ROOT / f"src/economic_graph/{name}.py", package / f"{name}.py")
    shutil.copyfile(SCRIPT, tmp_path / "rank_companies.py")
    shutil.copyfile(ROOT / "data/observable/observations.json", tmp_path / "ledger.json")
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("MONGODB_")
    }
    environment["PYTHONPATH"] = str(tmp_path)
    result = subprocess.run(
        [
            sys.executable,
            str(tmp_path / "rank_companies.py"),
            "--as-of",
            "T2",
            "--ledger",
            "ledger.json",
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        check=True,
    )
    assert json.loads(result.stdout)["eligible_companies"] == 21
    assert not (package / "simulator").exists()


def test_mongo_read_only_parity_and_server_time_filters(monkeypatch, capsys):
    rows = load_observations(ROOT / "data/observable/observations.json")
    queries = []

    class ReadOnlyCollection:
        def find(self, query):
            queries.append(query)
            cut = query["available_at"]["$lte"]
            return [row for row in rows if parse_time(row["available_at"]) <= cut]

    class ReadOnlyDatabase:
        name = MVP_DATABASE

        def __getitem__(self, collection):
            assert collection == OBSERVATIONS
            return ReadOnlyCollection()

    # El doble solo implementa find: escribir, crear índices o leer metadata haría fallar.
    client = MagicMock()
    client.__enter__.return_value = client
    client.__getitem__.return_value = ReadOnlyDatabase()
    monkeypatch.setattr(config, "load_config", lambda: ("mongodb://test.invalid", MVP_DATABASE))
    monkeypatch.setattr(database, "create_client", lambda uri: client)
    assert run(monkeypatch, ["--all-cuts", "--mongo"]) == 0
    reports = json.loads(capsys.readouterr().out)
    assert reports == [compare_rankings(rows, cut) for cut in CUTS]
    assert queries == [{"available_at": {"$lte": parse_time(cut)}} for cut in CUTS]
    client.__exit__.assert_called_once()


def test_wrong_database_rejected_before_connecting(monkeypatch, capsys):
    monkeypatch.setattr(config, "load_config", lambda: ("mongodb://user:secret@test", "production"))
    factory = Mock(side_effect=AssertionError("No conectar"))
    monkeypatch.setattr(database, "create_client", factory)
    assert run(monkeypatch, ["--as-of", "T0", "--mongo"]) == 1
    assert "base dedicada" in capsys.readouterr().err
    factory.assert_not_called()


def test_mongo_driver_error_does_not_leak_credentials(monkeypatch, capsys):
    monkeypatch.setattr(config, "load_config", lambda: ("mongodb://user:secret@test", MVP_DATABASE))
    factory = Mock(side_effect=OperationFailure("mongodb://user:secret@test", code=13))
    monkeypatch.setattr(database, "create_client", factory)
    assert run(monkeypatch, ["--as-of", "T0", "--mongo"]) == 1
    error = capsys.readouterr().err
    assert "no se pudo leer MongoDB" in error
    assert "secret" not in error and "mongodb://" not in error


def test_invalid_cut_rejected_before_network(monkeypatch, capsys):
    loader = Mock(side_effect=AssertionError("Fecha inválida: no leer credenciales"))
    monkeypatch.setattr(config, "load_config", loader)
    assert run(monkeypatch, ["--as-of", "2026-01-15", "--mongo"]) == 1
    assert "zona horaria" in capsys.readouterr().err
    loader.assert_not_called()


def test_raw_design_contract_rejected_without_loading_private_files(monkeypatch, capsys, tmp_path):
    path = tmp_path / "not-a-ledger.json"
    path.write_text(json.dumps([{"company_id_truth": "TEST-PRIVATE"}]), encoding="utf-8")
    assert run(monkeypatch, ["--as-of", "T0", "--ledger", str(path)]) == 1
    assert "contrato observable" in capsys.readouterr().err


def test_missing_input_does_not_silently_build_from_simulator(monkeypatch, capsys, tmp_path):
    assert run(monkeypatch, ["--as-of", "T0", "--ledger", str(tmp_path / "missing.json")]) == 1
    assert "No se puede leer el ledger observable" in capsys.readouterr().err
