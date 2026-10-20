"""Create a verified, non-publishing copy of the approved public package."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import re
from pathlib import Path

REQUIRED = ("README.md", "pyproject.toml", "uv.lock", ".python-version", ".env.example", "src", "app", "scripts", "tests", "config", "data/observable", "briefs", "case-studies/telcomx", "docs/04-architecture-overview.md", "docs/12-commercial-ranking.md", "docs/14-incremental-economic-case.md", "docs/16-financial-calculation.md", "docs/18-control-tower-demo.md", "docs/release/public-export-manifest.md")
PRESENTATION_REQUIRED = ("presentation-showcase/index.html", "presentation-showcase/app.js", "presentation-showcase/data.js", "presentation-showcase/content.json", "presentation-showcase/evidence-panels.js", "presentation-showcase/style.css", "presentation-showcase/README.md", "presentation-showcase/ConectaPyME.pdf", "presentation-showcase/assets", "presentation-showcase/evidence/iteration-3/data", "presentation-showcase/evidence/iteration-3/panels", "presentation-showcase/docs/guion.md", "presentation-showcase/docs/guia-estudio.html", "presentation-showcase/docs/trazabilidad.csv")
FORBIDDEN_NAMES = {".git", ".env", ".env.local", ".env.production", "__pycache__"}
FORBIDDEN_TEXT = ("ghp_", "github_pat_", "BEGIN PRIVATE KEY")


def files_under(path: Path):
    return [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"]


def broken_links(source: Path, root: Path) -> list[str]:
    if source.suffix.lower() not in {".html", ".md"}:
        return []
    text = source.read_text(encoding="utf-8", errors="strict")
    links = re.findall(r"(?:href|\]\()=['\"]?([^'\" )>]+)", text)
    result = []
    for link in links:
        if link.startswith(("http:", "https:", "mailto:", "#", "data:")):
            continue
        target = (source.parent / link.split("#", 1)[0].split("?", 1)[0]).resolve()
        if not target.exists():
            result.append(f"broken link: {source.relative_to(root)} -> {link}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    if output == root or root in output.parents:
        raise SystemExit("Destination must be outside the repository")
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty destination: {output}")
    missing = [item for item in REQUIRED + PRESENTATION_REQUIRED if not (root / item).exists()]
    if missing:
        raise SystemExit("Missing required export paths: " + ", ".join(missing))
    selected = []
    for item in REQUIRED + PRESENTATION_REQUIRED:
        selected.extend(files_under(root / item))
    violations = []
    for source in selected:
        relative = source.relative_to(root)
        if any(part in FORBIDDEN_NAMES for part in relative.parts):
            violations.append(f"forbidden path: {relative}")
        elif source.suffix.lower() in {".html", ".md", ".json", ".py", ".js", ".css", ".csv", ".txt"}:
            data = source.read_bytes()
            if source.name != "export_public_portfolio.py" and any(token.encode() in data for token in FORBIDDEN_TEXT):
                violations.append(f"sensitive text: {relative}")
        violations.extend(broken_links(source, root))
    if violations:
        raise SystemExit("Export validation failed:\n" + "\n".join(violations))
    records = []
    for source in sorted(set(selected)):
        relative = source.relative_to(root)
        records.append({"path": relative.as_posix(), "sha256": hashlib.sha256(source.read_bytes()).hexdigest(), "bytes": source.stat().st_size})
        print(f"COPY {relative}")
        if args.apply:
            target = output / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    manifest = {"schema": "conectapyme-public-export-v1", "files": records}
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if args.apply:
        (output / "PUBLIC-EXPORT-MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
