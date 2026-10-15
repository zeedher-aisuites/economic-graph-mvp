# ConectaPyME Economic Intelligence

**Pregunta central del reto de Totalplay:** ¿cómo construir un Economic Graph de PyMEs para una Telco y demostrar que genera valor económico incremental?

Este repositorio prepara una PoC pequeña, operada por personas, para explorar adquisición B2B y defender sus decisiones arquitectónicas, económicas y experimentales. ConectaPyME Telecom, Distrito Centro y Villa Conecta son ficticios. No contiene datos de clientes reales ni resultados económicos comprobados.

## Estado de la misión 001

Implementado: paquete Python, lectura y validación de configuración, cliente PyMongo, comprobación explícita mediante `ping`, pruebas sin servidor y herramientas de calidad. Incluye contexto, matriz de trazabilidad y estructura de una presentación ejecutiva de 12 diapositivas.

Todavía no implementado: las 30 empresas sintéticas, relaciones, colecciones, Economic Graph, consultas analíticas, baseline, scoring, ML, Control Tower y evaluación económica. La Control Tower es un entregable obligatorio del reto como dashboard o prototipo, que se atenderá en otra misión. No hay agentes, LLM, API, dashboard ni Docker.

## Requisitos

- Windows con PowerShell y Git; también puede usarse Linux con comandos equivalentes.
- Acceso al repositorio existente: <https://github.com/zeedher-aisuites/economic-graph-mvp>.
- `uv` y Python 3.11 o superior. Se usa **Python 3.12** en `.python-version`; uv puede instalarlo.
- Solo para comprobar una conexión real: un servidor MongoDB ya disponible, local o administrado, y autorización de red y usuario si corresponde. Este proyecto no instala el servidor. Las pruebas unitarias no lo necesitan.

## Instalación desde Windows PowerShell

### 1. Obtener el repositorio

```powershell
git clone https://github.com/zeedher-aisuites/economic-graph-mvp.git
Set-Location economic-graph-mvp
```

Usa tu acceso GitHub habitual para repositorios privados. Si revisas una rama aún no integrada, ejecuta `git switch mision-001-inicializacion` después del clone. No vuelvas a clonar si ya estás en el checkout de Codex.

### 2. Instalar uv y Python

Con Windows Package Manager:

```powershell
winget install --id astral-sh.uv --exact
```

Abre otra terminal si `uv` todavía no aparece en el PATH. Alternativas oficiales: <https://docs.astral.sh/uv/getting-started/installation/>.

```powershell
uv --version
uv python install 3.12
uv sync --locked
```

`uv sync` instala el paquete local y las herramientas de desarrollo en `.venv`. `--locked` exige que `uv.lock` coincida con `pyproject.toml`; no regenera dependencias accidentalmente. No hace falta activar el entorno: `uv run` lo utiliza. Para actualizar dependencias deliberadamente, modifica y revisa el lockfile en una tarea separada.

En Codex Linux, la caché predeterminada puede estar en una ruta de solo lectura. Si ocurre, configura antes `export UV_CACHE_DIR=/workspace/.cache/uv`. No hace falta ese ajuste en un equipo Windows con caché escribible.

### 3. Configurar `.env`

Desde la raíz del repositorio, copia el ejemplo solo si no existe una configuración local:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

El ejemplo contiene una dirección local sin credenciales:

```dotenv
MONGODB_URI=mongodb://localhost:27017
MONGODB_DATABASE=conectapyme
```

Esto **no inicia MongoDB**. Sustituye la URI por la que corresponda a tu servidor si no tienes una instancia local. Para Atlas usa su cadena `mongodb+srv://`, conserva la verificación TLS y configura los permisos y el acceso de red necesarios. Codifica en porcentaje los caracteres reservados de usuario/contraseña según la cadena de conexión de MongoDB. Nunca publiques la URI ni la pegues en reportes.

Ambas variables son obligatorias. Las variables ya definidas en el proceso tienen prioridad sobre `.env`; un valor vacío se considera un error, no activa un fallback al archivo. No se expanden expresiones `${VARIABLE}` dentro del archivo. El nombre de base debe ser válido en Windows y Linux y ocupar como máximo 63 bytes UTF-8.

`.env` está ignorado por Git. `.env.example` debe permanecer sin credenciales. Para comprobarlo:

```powershell
git check-ignore .env
```

### 4. Comprobar MongoDB

```powershell
uv run python scripts/check_connection.py
$LASTEXITCODE
```

Un resultado exitoso imprime «Conexión verificada: MongoDB respondió a ping. No se escribieron datos.» y devuelve código `0`. Un error devuelve `1` con un mensaje sin la URI ni los detalles sensibles del driver.

La operación usa `ping` en la base configurada, con tiempos de espera de cinco segundos para selección, conexión, socket y operación. La resolución DNS de una URI SRV y otros pasos previos del sistema pueden añadir tiempo. El cliente se cierra al terminar. No se crean colecciones ni se insertan datos; seleccionar una base inexistente y hacer `ping` no la materializa. El éxito no verifica permisos de lectura/escritura ni ninguna funcionalidad del Economic Graph.

Si falla: comprueba primero que ambas variables estén definidas; después revisa el servidor, host/DNS, reglas de red, TLS y permisos. No desactives la validación de certificados ni publiques el error crudo del driver. No atribuyas el fallo automáticamente a una contraseña incorrecta.

## Pruebas y calidad

Desde la raíz, sin necesidad de MongoDB ni de `.env`:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Las pruebas configuran entornos temporales y sustituyen el cliente MongoDB. Verifican precedencia, campos obligatorios, nombres válidos, errores sanitizados, `ping`, ausencia de escrituras y liberación del cliente. Un resultado unitario exitoso no verifica la conectividad real.

Para formatear cambios locales de código de manera intencional:

```powershell
uv run ruff format .
```

## Organización

| Ruta | Responsabilidad |
|---|---|
| `src/economic_graph/config.py` | Leer y validar las dos variables sin modificar el entorno |
| `src/economic_graph/database.py` | Crear el cliente y verificar mediante `ping` |
| `scripts/check_connection.py` | Comando de comprobación con salida y código de estado claros |
| `tests/` | Pruebas unitarias independientes de MongoDB |
| `data/synthetic/` | Reservada para una misión futura; actualmente solo `.gitkeep` |
| `docs/00` a `docs/04` | Contexto recibido, alcance, trazabilidad y arquitectura propuesta |
| `docs/05-executive-communication.md` | Reglas para comunicar decisiones e impacto potencial |
| `presentations/executive-deck.md` | Única presentación ejecutiva principal, todavía inicial |
| `presentations/decision-log.md` | Decisiones relevantes con estado, riesgos y evidencia |
| `presentations/references/` | Presentación original del reto, conservada como referencia |
| `AGENTS.md` | Reglas para colaboradores y futuras misiones |

## Alcance, evidencia y siguiente misión

La referencia del alcance es [la matriz de los seis entregables](docs/02-challenge-traceability.md). El original del reto y sus notas se revisaron para corregir la obligatoriedad de la Control Tower e identificar el brief final de 2–3 páginas. Las discrepancias y los pendientes están registrados allí y en [alcance y decisiones](docs/03-scope-and-decisions.md).

Las pruebas ejecutadas y la publicación de cada entrega deben reportarse con su SHA y resultados reales. Los comandos de PowerShell son instrucciones para Windows; su ejecución en Windows no queda demostrada por las pruebas de Linux. La conexión real requiere configuración válida y un servidor disponible; nunca se deduce de los mocks.

Próxima misión propuesta: revisar y aprobar modelo conceptual, fuentes observables, identidad y temporalidad (P-001 a P-003) antes de generar empresas. Los datos sintéticos ilustrarán viabilidad y no probarán ROI ni uplift causal. La evaluación económica futura deberá usar un contrafactual y descontar costos incrementales.
