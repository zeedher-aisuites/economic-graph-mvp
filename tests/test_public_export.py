from pathlib import Path
import subprocess
import sys


SCRIPT = Path(__file__).parents[1] / "scripts" / "export_public_portfolio.py"


def run_export(destination: Path, *extra: str):
    return subprocess.run([sys.executable, str(SCRIPT), str(destination), *extra], capture_output=True, text=True)


def test_export_dry_run_and_manifest(tmp_path):
    result = run_export(tmp_path / "package")
    assert result.returncode == 0, result.stderr
    assert 'conectapyme-public-export-v1' in result.stdout


def test_export_rejects_repository_destination():
    result = run_export(SCRIPT.parents[1])
    assert result.returncode != 0
    assert "outside the repository" in result.stderr or "outside the repository" in result.stdout


def test_export_rejects_nonempty_destination(tmp_path):
    destination = tmp_path / "package"
    destination.mkdir()
    (destination / "existing.txt").write_text("keep", encoding="utf-8")
    result = run_export(destination)
    assert result.returncode != 0
    assert "non-empty" in result.stderr or "non-empty" in result.stdout
