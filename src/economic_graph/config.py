"""Lectura de configuración local sin registrar credenciales ni modificar el entorno."""

import os
from pathlib import Path

from dotenv import dotenv_values


def load_config(env_file: str | Path = ".env") -> tuple[str, str]:
    """Devolver URI y base; las variables del proceso prevalecen sobre el archivo."""
    try:
        file_values = dotenv_values(env_file, interpolate=False)
    except (OSError, UnicodeError):
        raise ValueError("No se pudo leer el archivo de configuración como texto UTF-8.") from None

    values = {
        name: os.environ.get(name, file_values.get(name))
        for name in ("MONGODB_URI", "MONGODB_DATABASE")
    }
    missing = [name for name, value in values.items() if not value or not value.strip()]
    if missing:
        raise ValueError("Falta configuración obligatoria: " + ", ".join(missing) + ".")

    uri = values["MONGODB_URI"].strip()
    database = values["MONGODB_DATABASE"]
    if not uri.startswith(("mongodb://", "mongodb+srv://")):
        raise ValueError("MONGODB_URI debe usar el esquema mongodb:// o mongodb+srv://.")
    if any(character.isspace() for character in uri):
        raise ValueError("MONGODB_URI no puede contener espacios sin codificar.")

    # Usar nombres portables entre Windows y Linux; el límite se mide en bytes.
    forbidden = set('/\\. "$*<>:|?\x00')
    if any(character in forbidden for character in database) or len(database.encode("utf-8")) > 63:
        raise ValueError("MONGODB_DATABASE debe ser un nombre válido de MongoDB de hasta 63 bytes.")

    return uri, database
