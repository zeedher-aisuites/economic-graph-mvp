"""Inspeccionar conocimiento disponible sin leer fuentes restringidas ni escribir datos."""

import argparse
import json
import sys

from pymongo.errors import PyMongoError

from economic_graph.config import load_config
from economic_graph.database import create_client
from economic_graph.mongo_observable import read_observations
from economic_graph.observable import attribute_history, load_observations, snapshot, summarize


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--as-of", required=True, help="T0/T1/T2 o instante ISO 8601 con zona.")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument(
        "--company", help="ID CO-... observable para consultar la historia de un atributo."
    )
    parser.add_argument("--attribute", help="Atributo cuya procedencia se quiere inspeccionar.")
    parser.add_argument(
        "--mongo", action="store_true", help="Leer MongoDB en lugar del ledger local."
    )
    args = parser.parse_args()
    if bool(args.company) != bool(args.attribute):
        parser.error("--company y --attribute deben usarse juntos.")
    try:
        if args.mongo:
            uri, name = load_config()
            with create_client(uri) as client:
                rows = read_observations(client[name], args.as_of, company_id=args.company)
        else:
            rows = load_observations()
        if args.company:
            result = attribute_history(rows, args.company, args.attribute, args.as_of)
        else:
            result = snapshot(rows, args.as_of)
            if args.summary:
                result = summarize(result)
    except (ValueError, ConnectionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except PyMongoError:
        print("Error: no se pudo leer MongoDB. Revisa acceso, red y TLS.", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
