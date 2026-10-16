"""Materializar únicamente las observaciones aprobadas; nunca fabricar datos aleatorios."""

import argparse
import json
import sys
from pathlib import Path

from economic_graph.simulator.design import audit_design, load_design
from economic_graph.simulator.project import project_observations, write_projection


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="Validar y proyectar sin escribir archivos."
    )
    parser.add_argument("--output", type=Path, default=Path("data/observable"))
    args = parser.parse_args()
    try:
        data = load_design()
        audit = audit_design(data)
        if audit["errors"]:
            print(json.dumps(audit, ensure_ascii=False, indent=2), file=sys.stderr)
            return 1
        rows, reconciliation = project_observations(data["observations"])
        if not args.dry_run:
            write_projection(rows, reconciliation, args.output)
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {"mode": "dry-run" if args.dry_run else "materialized", "observations": len(rows)},
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
