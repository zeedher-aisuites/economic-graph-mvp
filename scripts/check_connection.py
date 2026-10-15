"""Comprobar MongoDB sin imprimir secretos, crear colecciones ni insertar datos."""

import sys

from economic_graph.config import load_config
from economic_graph.database import check_connection


def main() -> int:
    """Informar el resultado; devolver 0 en éxito y 1 ante un error controlado."""
    try:
        uri, database_name = load_config()
        check_connection(uri, database_name)
    except (ValueError, ConnectionError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Conexión verificada: MongoDB respondió a ping. No se escribieron datos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
