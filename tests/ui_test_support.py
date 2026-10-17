"""Preparación y aislamiento de AppTest; solo infraestructura de pruebas."""

import importlib
import socket
import sys
import threading
from pathlib import Path
from time import perf_counter


def prepare_ui_runtime() -> dict[str, float]:
    """Separar carga de DLL/importaciones de la ejecución funcional de Streamlit."""
    timings = {}
    for name in ("numpy", "pandas", "pyarrow", "altair"):
        start = perf_counter()
        importlib.import_module(name)
        timings[name] = perf_counter() - start
    return timings


def run_app(app):
    """Conservar el timeout, sin reintentos; capturar pila antes de que AppTest cierre el hilo."""
    stacks = []

    def capture():
        for thread in threading.enumerate():
            if "ScriptRunner" not in thread.name:
                continue
            frame = sys._current_frames().get(thread.ident)
            lines = []
            while frame is not None:
                code = frame.f_code
                # Sin código fuente, variables locales, credenciales o configuración.
                lines.append(f"{Path(code.co_filename).name}:{frame.f_lineno} {code.co_name}")
                frame = frame.f_back
            stacks.append("\n".join(lines))

    watchdog = threading.Timer(app.default_timeout * 0.8, capture)
    watchdog.daemon = True
    watchdog.start()
    try:
        return app.run()
    except RuntimeError as error:
        if "script run timed out" not in str(error):
            raise
        detail = "\n\n".join(stacks) or "Sin pila ScriptRunner capturada."
        raise RuntimeError(
            "AppTest excedió su timeout funcional con dependencias ya importadas. "
            "No se reintentó ni amplió el límite. Pila previa al cierre:\n" + detail
        ) from None
    finally:
        watchdog.cancel()
        watchdog.join()


def install_network_guard(socketpair_factory=None) -> None:
    """Bloquear red; solo permitir el par TCP efímero creado dentro de socketpair().

    Windows usa TCP loopback para este IPC. El permiso es local al hilo, temporal
    y limitado al endpoint que acaba de enlazar la fábrica confiable de socketpair.
    No permite conectar a servicios loopback arbitrarios, DNS ni destinos externos.
    """
    original_pair = socketpair_factory or socket.socketpair
    original_bind = socket.socket.bind
    original_connect = socket.socket.connect
    original_listen = socket.socket.listen
    state = threading.local()

    def blocked(*args, **kwargs):
        raise AssertionError("Red no autorizada en modo offline")

    def bind(sock, address):
        if (
            getattr(state, "targets", None) is None
            or sock.family not in (socket.AF_INET, socket.AF_INET6)
            or address[:2] not in (("127.0.0.1", 0), ("::1", 0))
        ):
            return blocked()
        result = original_bind(sock, address)
        state.targets.add(sock.getsockname()[:2])
        return result

    def listen(sock, *args):
        targets = getattr(state, "targets", None)
        if targets is None or sock.getsockname()[:2] not in targets:
            return blocked()
        return original_listen(sock, *args)

    def connect(sock, address):
        targets = getattr(state, "targets", None)
        if (
            targets is None
            or sock.family not in (socket.AF_INET, socket.AF_INET6)
            or address[:2] not in targets
        ):
            return blocked()
        return original_connect(sock, address)

    def pair(*args, **kwargs):
        previous = getattr(state, "targets", None)
        state.targets = set()
        try:
            return original_pair(*args, **kwargs)
        finally:
            state.targets = previous

    socket.socketpair = pair
    socket.socket.bind = bind
    socket.socket.listen = listen
    socket.socket.connect = connect
    socket.socket.connect_ex = blocked
    socket.socket.sendto = blocked
    if hasattr(socket.socket, "sendmsg"):
        socket.socket.sendmsg = blocked
    socket.create_connection = blocked
    socket.getaddrinfo = blocked
    socket.gethostbyname = blocked
    socket.gethostbyname_ex = blocked
    socket.gethostbyaddr = blocked
    socket.getnameinfo = blocked
