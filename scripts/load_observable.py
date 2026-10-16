"""Carga explícita e idempotente del ledger público, solo en la base dedicada del MVP."""

import argparse
import json
import sys

from pymongo.errors import PyMongoError

from economic_graph.config import load_config
from economic_graph.database import create_client
from economic_graph.mongo_observable import MVP_DATABASE, load_observable
from economic_graph.observable import load_observations, snapshot, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--dry-run", action="store_true", help="Modo predeterminado; no accede a MongoDB."
    )
    modes.add_argument(
        "--apply", action="store_true", help="Aplicar únicamente después de revisar el dry-run."
    )
    parser.add_argument(
        "--confirm-database", help=f"Para aplicar debe ser exactamente {MVP_DATABASE}."
    )
    args = parser.parse_args()
    if args.apply and args.confirm_database != MVP_DATABASE:
        parser.error(f"--apply requiere --confirm-database {MVP_DATABASE}.")
    try:
        rows = load_observations()
        if not args.apply:
            report = {"mode": "dry-run", **summarize(snapshot(rows, "T2"))}
        else:
            uri, name = load_config()
            if name != MVP_DATABASE:
                raise ValueError(f"MONGODB_DATABASE debe ser la base dedicada {MVP_DATABASE}.")
            with create_client(uri) as client:
                report = {"mode": "applied", **load_observable(client[name], rows)}
    except (ValueError, ConnectionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except PyMongoError:
        print(
            "Error: la carga MongoDB no se completó. Revisa acceso, red y TLS; puede reintentarse.",
            file=sys.stderr,
        )
        return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
