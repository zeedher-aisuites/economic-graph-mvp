"""Calcular escenarios educativos, sensibilidad y equilibrio sin leer empresas ni Atlas."""

import argparse
import json
import sys
from pathlib import Path

from economic_graph.finance import financial_report, load_financial_config, render_financial_report


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, help="JSON UTF-8 de supuestos, no ledger ni oráculo."
    )
    parser.add_argument("--scope", choices=("demo", "hypothetical", "both"), default="both")
    parser.add_argument("--sensitivity", action="store_true", help="Barridos y cruces de la base.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    try:
        config = load_financial_config(args.config) if args.config else load_financial_config()
        report = financial_report(config, args.scope, args.sensitivity)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if args.format == "markdown":
        print(render_financial_report(report), end="")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
