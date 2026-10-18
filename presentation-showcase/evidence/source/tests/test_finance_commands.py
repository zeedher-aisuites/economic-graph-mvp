"""CLI financiera educativa: Unicode, aislamiento y errores sin datos de conexión."""

import json
import os
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from economic_graph.finance import financial_report, load_financial_config, render_financial_report

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/calculate_finance.py"


def run(monkeypatch, arguments):
    monkeypatch.chdir(ROOT)
    monkeypatch.setattr(sys, "argv", ["calculate_finance.py", *arguments])
    with pytest.raises(SystemExit) as result:
        runpy.run_path(str(SCRIPT), run_name="__main__")
    return result.value.code


@pytest.mark.parametrize("scope,count", [("demo", 4), ("hypothetical", 4), ("both", 8)])
def test_scope_keeps_three_cases_and_null_separate_from_experiment(
    monkeypatch, capsys, scope, count
):
    assert run(monkeypatch, ["--scope", scope]) == 0
    report = json.loads(capsys.readouterr().out)
    assert len(report["results"]) == count
    assert report["assumption_status"] == "educational_uncalibrated"
    assert report["future_experiment"]["sample_size"] is None
    assert all(not row["operational_authorization"] for row in report["results"])


def test_sensitivity_command_has_all_matrices(monkeypatch, capsys):
    assert run(monkeypatch, ["--sensitivity"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert set(result["sensitivity"]) == {"demo", "hypothetical"}
    assert len(result["sensitivity"]["demo"]["one_way"]) == 26
    assert len(result["sensitivity"]["hypothetical"]["rate_by_margin"]) == 15


def test_markdown_example_reproducible_and_shows_infeasibility(monkeypatch, capsys):
    assert run(monkeypatch, ["--format", "markdown"]) == 0
    text = capsys.readouterr().out
    config = load_financial_config(ROOT / "config/financial_assumptions.json")
    assert text == render_financial_report(financial_report(config))
    assert "167.500000 (inviable)" in text
    assert "Referencia base de saldo nulo" in text
    assert "No representa datos observados" in text
    assert (ROOT / "docs/16-financial-calculation.md").read_text(encoding="utf-8").endswith(text)


@pytest.mark.parametrize("encoding", ["utf-8", "cp1252"])
@pytest.mark.parametrize("output_format", ["json", "markdown"])
def test_finance_only_public_module_config_and_no_mongo(tmp_path, encoding, output_format):
    directory = tmp_path / "calculador público con espacios"
    package = directory / "economic_graph"
    package.mkdir(parents=True)
    for name in ("__init__", "finance"):
        shutil.copyfile(ROOT / f"src/economic_graph/{name}.py", package / f"{name}.py")
    shutil.copyfile(SCRIPT, directory / "calculate_finance.py")
    shutil.copyfile(ROOT / "config/financial_assumptions.json", directory / "supuestos.json")
    environment = {
        key: value for key, value in os.environ.items() if not key.upper().startswith("MONGODB_")
    }
    environment.update(
        PYTHONPATH=str(directory), PYTHONUTF8="0", PYTHONIOENCODING=f"{encoding}:strict"
    )
    result = subprocess.run(
        [
            sys.executable,
            str(directory / "calculate_finance.py"),
            "--config",
            "supuestos.json",
            "--format",
            output_format,
        ],
        cwd=directory,
        env=environment,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode != 0:
        pytest.fail(
            f"CLI financiera: código {result.returncode}. "
            f"stderr: {result.stderr.decode('utf-8', errors='backslashreplace')}",
            pytrace=False,
        )
    output = result.stdout.decode("utf-8")
    if output_format == "json":
        assert len(json.loads(output)["results"]) == 8
    else:
        assert "Δ conversión" in output and "Escenario hipotético: 500 plazas" in output
    assert not (package / "simulator").exists()
    assert not (package / "database.py").exists()
    assert not (directory / "data").exists()


def test_missing_config_is_an_error_without_fallback(monkeypatch, capsys, tmp_path):
    assert run(monkeypatch, ["--config", str(tmp_path / "missing.json")]) == 1
    assert "No se puede leer la configuración" in capsys.readouterr().err


def test_bad_config_does_not_echo_sensitive_value(monkeypatch, capsys, tmp_path):
    config = load_financial_config(ROOT / "config/financial_assumptions.json")
    config["scenarios"][0]["contract_margin_per_activation"]["value"] = (
        "mongodb://fake-user:fake-secret@invalid"
    )
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    assert run(monkeypatch, ["--config", str(path)]) == 1
    error = capsys.readouterr().err
    assert "inválido" in error and "fake-secret" not in error and "mongodb://" not in error


def test_utf8_bom_config_accepted(tmp_path):
    source = ROOT / "config/financial_assumptions.json"
    path = tmp_path / "supuestos.json"
    path.write_text(source.read_text(encoding="utf-8"), encoding="utf-8-sig")
    assert financial_report(load_financial_config(path)) == financial_report(
        load_financial_config(source)
    )


def test_duplicate_json_keys_not_silently_overwritten(tmp_path):
    path = tmp_path / "duplicate.json"
    path.write_text('{"scenarios": [], "scenarios": []}', encoding="utf-8")
    with pytest.raises(ValueError, match="claves duplicadas"):
        load_financial_config(path)


def test_deterministic_config_key_order_and_input_hash():
    config = load_financial_config(ROOT / "config/financial_assumptions.json")
    reordered = dict(reversed(list(config.items())))
    assert financial_report(config, sensitivity=True) == financial_report(
        reordered, sensitivity=True
    )
