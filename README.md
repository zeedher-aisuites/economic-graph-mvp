# ConectaPyME Economic Intelligence

**Pregunta central del reto de Totalplay:** ¿cómo construir un Economic Graph de PyMEs para una Telco y demostrar que genera valor económico incremental?

Este repositorio prepara una PoC pequeña, operada por personas, para explorar adquisición B2B y defender sus decisiones arquitectónicas, económicas y experimentales. ConectaPyME Telecom, Distrito Centro y Villa Conecta son ficticios. No contiene datos de clientes reales ni resultados económicos comprobados.

## Estado de las misiones

Implementado y verificado offline: ingesta del diseño aprobado, auditoría de 30 empresas/48 relaciones/83 observaciones, proyección física e interfaces separadas, consultas a fecha de corte, historial, conflictos e identidad como candidatos. Las empresas conocidas son 12/17/23 en T0/T1/T2; no se exponen las 7 nunca descubiertas ni se completan perfiles desde el catálogo. La carga PyMongo está preparada con dry-run, protección de base dedicada e idempotencia probada con dobles.

La infraestructura de misión 001 se conserva: configuración, cliente y ping sin escrituras, uv, pytest y Ruff. **Cierre 002C:** el usuario reportó validación real de Atlas desde Windows con VS Code: ping exitoso, carga de 83 observaciones, segunda carga con 0 inserciones/83 sin cambios y consultas T0/T1/T2 con los conteos esperados. La evidencia y su procedencia están en [validación Atlas](docs/11-atlas-integration-validation.md); no son ejecuciones realizadas por Codex Cloud y su conectividad sigue sin verificarse. No hay modelos ML, eventos comerciales, ventas, conversiones, cálculo económico ni Control Tower implementados. La Control Tower sigue siendo un entregable obligatorio del reto para otra misión.

**Misión 003A:** rankings baseline y con grafo deterministas, con reglas aprobadas por el usuario, capacidad fija de cinco cuentas, cortes temporales, contribuciones y evidencia. La [auditoría y política](docs/12-commercial-ranking.md) explica señales y sesgos; la [comparación T0/T1/T2](docs/13-ranking-comparison.md) muestra selecciones reproducibles. No demuestra mayor conversión ni valor económico incremental.

**Misión 003B, diseño para revisión:** [caso económico incremental](docs/14-incremental-economic-case.md) y [protocolo A/B](docs/15-incrementality-experiment.md). Incluyen variables, fórmulas, escenarios hipotéticos, sensibilidad, umbral y decisiones ECO-01 a ECO-06 pendientes de aprobación. No hay simulador financiero ni resultados comerciales nuevos; la entrega es exclusivamente documental.

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

Usa tu acceso GitHub habitual para repositorios privados. Para revisar la misión 003A antes de su integración, ejecuta `git switch mision-003a-comparable-rankings` después del clone. No vuelvas a clonar si ya estás en el checkout de Codex.

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

## Validar e inspeccionar el modelo aprobado

Ejecuta desde la raíz. Estos pasos no requieren Atlas, red ni `.env`:

```powershell
uv sync --locked
uv run python scripts/validate_design.py
uv run python scripts/build_observable.py --dry-run
uv run python scripts/build_observable.py
uv run python scripts/inspect_graph.py --as-of T0 --summary
uv run python scripts/inspect_graph.py --as-of T1 --summary
uv run python scripts/inspect_graph.py --as-of T2 --summary
```

`validate_design.py` es una herramienta de auditoría restringida: muestra cantidades de verdad sintética para el desarrollador. Lee los 11 CSV/JSON aprobados, sus huellas y referencias; no escribe. No edites esos datos para hacer pasar una validación: registra la desviación en [la auditoría](docs/10-design-validation.md) y solicita aprobación si cambiaría hechos.

`build_observable.py` transforma únicamente las 83 observaciones aprobadas. Su dry-run no escribe; el modo normal genera `data/observable/observations.json` y una conciliación privada ignorada por Git. No agrega aleatoriedad ni necesita semilla. No edites directamente el ledger generado. Al repetir el comando produce los mismos bytes. La vista comercial no lee `design-data/restricted/`.

Los resúmenes comerciales muestran empresas **12/17/23**, observaciones **28/54/83**, afirmaciones económicas **2/13/26** y referencias **0/2/3**. No etiquetan qué afirmaciones son falsas ni suman referencias como suministro. La auditoría restringida comprueba, por separado, las **2/11/23 relaciones verdaderas observadas**.

Los cortes son exactamente `2026-01-15T12:00:00Z`, `2026-05-15T12:00:00Z` y `2026-09-15T12:00:00Z`. También puedes consultar un instante con zona, nunca una fecha sin hora:

```powershell
uv run python scripts/inspect_graph.py --as-of "2026-05-15T11:59:59Z" --summary
uv run python scripts/inspect_graph.py --as-of T2
```

La salida completa muestra empresas con atributos conocidos/desconocidos, observaciones, relaciones con historia, conflictos y alias candidatos. Usa un `company_id` CO-... devuelto por esa salida para pedir procedencia:

```powershell
$vista = uv run python scripts/inspect_graph.py --as-of T2 | ConvertFrom-Json
$empresa = $vista.companies | Where-Object { $_.attributes.display_name.value -eq "Hornos del Centro" }
uv run python scripts/inspect_graph.py --as-of T2 --company $empresa.company_id --attribute branch_count
```

Tamaño, sector u otros atributos ausentes permanecen UNKNOWN; valores distintos sin arbitraje quedan CONFLICTED. Nombre parecido solo sugiere un candidato, no fusiona empresas. Las tres notas que revelaban diagnósticos del oráculo se conservan en los originales y se proyectan con texto comercial neutral. Ver IDs y límites en `docs/10-design-validation.md`.

## Comparar rankings sin Atlas

Desde la raíz, sin red, MongoDB ni `.env`:

```powershell
uv run python scripts/rank_companies.py --as-of T0 --format markdown
uv run python scripts/rank_companies.py --all-cuts --format markdown
uv run python scripts/rank_companies.py --as-of T2
```

La política `003a-conservative-v1` compara las mismas cuentas elegibles con cinco plazas por corte. Baseline: 10 puntos por sucursal adicional observada, máximo 50. Con grafo: misma base más 5 por vecino económico distinto confirmado, máximo 20 adicionales. Se excluyen únicamente cuentas con servicio activo confirmado y sin conflicto; el resto requiere validación comercial, sin asumir que sean no-clientes. Incertidumbre y conflictos no se completan desde el catálogo. Los pesos son exploratorios, sin significado probabilístico.

Markdown muestra posiciones, puntos, diferencia, selección y empates en el límite. JSON es la salida predeterminada e incluye reglas, fuentes, fechas y evidencia por característica. Por ejemplo:

El CLI emite **UTF-8** en stdout y stderr, también al capturarlo desde otro proceso. Un consumidor Python debe decodificar ambos como UTF-8, sin depender de la página de códigos de Windows. Si Windows PowerShell 5 interpreta mal los acentos al canalizar la salida a `ConvertFrom-Json`, configura su lector de salida nativa en la sesión actual antes del ejemplo:

```powershell
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
```

```powershell
$ranking = uv run python scripts/rank_companies.py --as-of T2 | ConvertFrom-Json
$ranking.policy
$ranking.comparison
$cafe = $ranking.companies | Where-Object { $_.display_name -eq "Café Jacaranda" }
$cafe.features | ConvertTo-Json -Depth 20
$ranking.excluded | ConvertTo-Json -Depth 20
```

También admite instantes con zona y un ledger público copiado a otra ruta:

```powershell
uv run python scripts/rank_companies.py --as-of "2026-05-15T11:59:59Z" --format markdown
uv run python scripts/rank_companies.py --as-of T2 --ledger data/observable/observations.json
```

No hace falta regenerar el ledger ni ejecutar la carga para comparar. Conceptos de features, scoring, baseline, sesgo y evaluación, así como reglas frente a contradicciones y duplicados, están en [la guía de rankings](docs/12-commercial-ranking.md). Las tablas completas están en [la comparación reproducible](docs/13-ranking-comparison.md). Tres sustituciones del top-5 no significan tres ventas adicionales; muchos empates reflejan escasez de evidencia.

### Lectura opcional desde Atlas

Solo si ya tienes conectividad y acceso de lectura a la base dedicada `conectapyme_mvp_observable`, con las dos variables configuradas de forma privada:

```powershell
uv run python scripts/rank_companies.py --mongo --as-of T2 --format markdown
uv run python scripts/rank_companies.py --mongo --all-cuts
```

Este comando solo consulta `m002b_observations` mediante `find` con filtro de disponibilidad. No carga datos, crea índices ni escribe colecciones. `--mongo` y `--ledger` son alternativas excluyentes; no hay fallback silencioso si falla Atlas. La paridad se probó con un doble de lectura; **integración real de rankings en Atlas no verificada**. La evidencia local de 002C no es una nueva ejecución de este comando.

## Carga MongoDB opcional y explícita — operación de misión 002B

Primero revisa, sin credenciales ni conexión:

```powershell
uv run python scripts/load_observable.py --dry-run
```

Solo un operador autorizado debe usar una instancia no productiva y configurar en `.env` **MONGODB_DATABASE=conectapyme_mvp_observable**, junto con su URI privada. El ejemplo local `conectapyme` de la misión 001 sirve para ping; **no está autorizado para carga**. No copies aquí credenciales.

```powershell
uv run python scripts/load_observable.py --apply --confirm-database conectapyme_mvp_observable
uv run python scripts/load_observable.py --apply --confirm-database conectapyme_mvp_observable
uv run python scripts/inspect_graph.py --mongo --as-of T2 --summary
```

La segunda carga no debe insertar nuevos registros. Se usan solo `m002b_observations` y `m002b_metadata`; se rechazan colecciones ajenas y documentos existentes con contenido diferente. No se borran ni se reemplazan registros. Un fallo puede dejar un lote parcialmente cargado; reintentarlo es seguro por ID. La verificación de red y roles debe realizarla el operador antes de usar Atlas. No se carga la verdad sintética en esa base.

Entrega al usuario comercial solo el directorio observable, o una credencial distinta con acceso de lectura limitado a `m002b_observations`. Un desarrollador con acceso al checkout completo puede leer los diseños; no se afirma aislamiento frente a ese usuario. Los permisos POSIX no sustituyen ACL de Windows ni roles MongoDB. Los diagnósticos `check_connection.py`, `validate_design.py` e `inspect_graph.py` no escriben.

## Pruebas y calidad

Desde la raíz, sin necesidad de MongoDB ni de `.env`:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Las pruebas offline cubren la infraestructura y los invariantes del modelo: conteos, enlaces, fechas, cortes, ausencia de oráculo, desconocidos, evidencia duplicada, conflictos, alias y carga repetida contra un doble de MongoDB. Las pruebas 003A añaden regresiones del top-5, contribuciones, elegibilidad, empates, invariancia ante datos futuros y paridad de lectura con MongoDB simulado. No leen `.env` ni abren Atlas. Un resultado unitario exitoso no verifica conectividad real. La única integración aparece omitida por defecto con su motivo explícito.

Para ejecutar únicamente las pruebas de rankings, o excluir expresamente cualquier integración:

```powershell
uv run pytest tests/test_rankings.py tests/test_ranking_commands.py
uv run pytest -m "not integration"
```

Para formatear cambios locales de código de manera intencional:

```powershell
uv run ruff format .
```

Para activar la integración **solo en la base dedicada autorizada**, después de configurar el servidor:

```powershell
$env:RUN_MONGODB_INTEGRATION = "1"
$env:MONGODB_INTEGRATION_DATABASE_CONFIRM = "conectapyme_mvp_observable"
uv run pytest -m integration
Remove-Item Env:RUN_MONGODB_INTEGRATION
Remove-Item Env:MONGODB_INTEGRATION_DATABASE_CONFIRM
```

La prueba hace ping, carga idempotente y lecturas observacionales T0/T1/T2. Conserva los registros de la PoC; no borra colecciones para limpiar.

## Organización

| Ruta | Responsabilidad |
|---|---|
| `src/economic_graph/config.py` | Leer y validar las dos variables sin modificar el entorno |
| `src/economic_graph/database.py` | Crear el cliente y verificar mediante `ping` |
| `scripts/check_connection.py` | Comando de comprobación con salida y código de estado claros |
| `tests/` | Pruebas unitarias independientes de MongoDB |
| `data/synthetic/restricted/` | Conciliación privada generada, ignorada por Git |
| `design-data/restricted/` | Insumos aprobados intactos; solo ingesta y auditoría |
| `design-data/README.md` y `manifest.json` | README adjunto, origen, versión y huellas |
| `data/observable/` | Ledger público materializado |
| `src/economic_graph/simulator/` | Ingesta, auditoría y proyección restringida |
| `src/economic_graph/observable.py` | Consultas públicas a fecha de corte |
| `src/economic_graph/mongo_observable.py` | Carga protegida y lectura temporal MongoDB |
| `src/economic_graph/rankings.py` | Dos políticas versionadas, comparación y explicaciones sin I/O |
| `scripts/rank_companies.py` | CLI de rankings offline o lectura MongoDB, JSON y Markdown |
| `docs/06` a `docs/10` | Diseño aprobado y auditoría de implementación |
| `docs/11` a `docs/13` | Evidencia Atlas local, política de rankings y tablas comparativas |
| `docs/00` a `docs/04` | Contexto recibido, alcance, trazabilidad y arquitectura propuesta |
| `docs/05-executive-communication.md` | Reglas para comunicar decisiones e impacto potencial |
| `presentations/executive-deck.md` | Única presentación ejecutiva principal, todavía inicial |
| `presentations/decision-log.md` | Decisiones relevantes con estado, riesgos y evidencia |
| `presentations/references/` | Presentación original del reto, conservada como referencia |
| `AGENTS.md` | Reglas para colaboradores y futuras misiones |

## Alcance, evidencia y siguiente misión

La referencia del alcance es [la matriz de los seis entregables](docs/02-challenge-traceability.md). El original del reto y sus notas se revisaron para corregir la obligatoriedad de la Control Tower e identificar el brief final de 2–3 páginas. Las discrepancias y los pendientes están registrados allí y en [alcance y decisiones](docs/03-scope-and-decisions.md).

Las pruebas ejecutadas y la publicación de cada entrega deben reportarse con su SHA y resultados reales. Los comandos de PowerShell son instrucciones para Windows; su ejecución en Windows no queda demostrada por las pruebas de Linux. La conexión real requiere configuración válida y un servidor disponible; nunca se deduce de los mocks.

El diseño conceptual, catálogo, relaciones y observabilidad ya fueron aprobados y materializados en misión 002B. Las limitaciones documentadas de fusión, transiciones y caducidad requieren nueva evidencia aprobada si se desea ampliar esos ejemplos. La misión 003A añade comparación de políticas, sin cambiar el ledger ni escribir en Atlas. La primera fase de 003B propone el caso económico y el experimento; su implementación, simulaciones de ventas y Control Tower siguen sin autorizarse. Los datos sintéticos no prueban ROI ni uplift causal. La medición futura deberá usar un contrafactual y descontar costos incrementales.
