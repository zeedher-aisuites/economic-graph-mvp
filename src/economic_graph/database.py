"""Cliente MongoDB y comprobación de conectividad sin operaciones de escritura."""

from typing import Any

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, PyMongoError

TIMEOUT_MS = 5_000


def create_client(uri: str) -> MongoClient[dict[str, Any]]:
    """Crear un cliente con tiempos acotados; no equivale a verificar la conexión."""
    try:
        return MongoClient(
            uri,
            serverSelectionTimeoutMS=TIMEOUT_MS,
            connectTimeoutMS=TIMEOUT_MS,
            socketTimeoutMS=TIMEOUT_MS,
            timeoutMS=TIMEOUT_MS,
            connect=False,
        )
    except (PyMongoError, ValueError):
        # Los mensajes del driver pueden incluir la URI. No propagar esos detalles.
        raise ConnectionError(
            "No se pudo crear el cliente MongoDB. Revisa la URI y sus opciones."
        ) from None


def check_connection(uri: str, database_name: str) -> None:
    """Ejecutar ping en la base indicada y cerrar el cliente incluso si falla."""
    try:
        with create_client(uri) as client:
            response = client[database_name].command("ping")
            if response.get("ok") != 1:
                raise ConnectionError("MongoDB no confirmó correctamente la respuesta a ping.")
    except OperationFailure as error:
        if error.code in (13, 18):
            raise ConnectionError(
                "MongoDB rechazó la autenticación o los permisos. Revisa el usuario y sus accesos."
            ) from None
        raise ConnectionError(
            "MongoDB rechazó ping. Revisa la configuración del servidor."
        ) from None
    except ConnectionFailure:
        raise ConnectionError(
            "No se pudo contactar con MongoDB dentro del tiempo límite. "
            "Revisa el servidor, DNS, red y configuración TLS."
        ) from None
    except (PyMongoError, ValueError):
        raise ConnectionError(
            "No se pudo comprobar MongoDB. Revisa la URI, la base y la configuración TLS."
        ) from None
