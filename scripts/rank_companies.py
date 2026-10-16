"""Comparar políticas aprobadas offline o mediante lectura MongoDB, sin escrituras."""

import argparse
import json
import sys
from pathlib import Path

from pymongo.errors import PyMongoError

from economic_graph.config import load_config
from economic_graph.contracts import CUTS, parse_time
from economic_graph.database import create_client
from economic_graph.mongo_observable import MVP_DATABASE, read_observations
from economic_graph.observable import load_observations
from economic_graph.rankings import compare_rankings, render_comparison


def main() -> int:
    # En Windows, las tuberías pueden usar cp1252 aunque la consola admita Unicode.
    # El contrato de salida es UTF-8 tanto en terminal como con redirección/captura.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    cuts = parser.add_mutually_exclusive_group(required=True)
    cuts.add_argument("--as-of", help="T0/T1/T2 o instante ISO 8601 con zona.")
    cuts.add_argument("--all-cuts", action="store_true", help="Comparar T0, T1 y T2.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--ledger", type=Path, help="Ruta a un ledger observable 1.0.")
    source.add_argument("--mongo", action="store_true", help="Solo lectura en la base dedicada.")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    try:
        instants = list(CUTS) if args.all_cuts else [args.as_of]
        for instant in instants:
            parse_time(instant)
        if args.mongo:
            uri, name = load_config()
            if name != MVP_DATABASE:
                raise ValueError(f"Solo se permite la base dedicada {MVP_DATABASE}.")
            with create_client(uri) as client:
                reports = [
                    compare_rankings(read_observations(client[name], cut), cut) for cut in instants
                ]
        else:
            rows = load_observations(args.ledger) if args.ledger else load_observations()
            reports = [compare_rankings(rows, cut) for cut in instants]
    except (ValueError, ConnectionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except PyMongoError:
        print("Error: no se pudo leer MongoDB. Revisa acceso, red y TLS.", file=sys.stderr)
        return 1
    if args.format == "markdown":
        print("\n".join(render_comparison(report) for report in reports), end="")
    else:
        print(json.dumps(reports if args.all_cuts else reports[0], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
