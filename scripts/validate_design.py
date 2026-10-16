"""Auditar insumos aprobados; diagnóstico de solo lectura y uso restringido."""

import json
import sys

from economic_graph.simulator.design import audit_design, load_design


def main() -> int:
    try:
        report = audit_design(load_design())
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
