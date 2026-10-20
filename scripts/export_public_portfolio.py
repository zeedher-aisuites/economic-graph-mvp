"""Prepare a clean, non-publishing copy of the approved public package."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

INCLUDE = ("README.md", "pyproject.toml", "uv.lock", ".python-version", ".env.example", "src", "app", "scripts", "tests", "config", "data/observable", "briefs", "case-studies/telcomx", "presentation-showcase", "docs/04-architecture-overview.md", "docs/12-commercial-ranking.md", "docs/14-incremental-economic-case.md", "docs/16-financial-calculation.md", "docs/18-control-tower-demo.md", "docs/release/public-export-manifest.md")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"Refusing to overwrite non-empty directory: {output}")
    for item in INCLUDE:
        source = root / item
        if not source.exists():
            print(f"SKIP missing: {item}")
            continue
        print(f"COPY {item}")
        if args.apply:
            target = output / item
            target.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, target, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".env", ".git", "__pycache__"))
            else:
                shutil.copy2(source, target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
