# ConectaPyME Economic Intelligence

**Pregunta central del reto de Totalplay:** ¿cómo construir un Economic Graph de PyMEs para una Telco y demostrar que genera valor económico incremental?

PoC educativa de adquisición B2B, operada por personas, con Python, PyMongo y una Control Tower local en Streamlit. ConectaPyME Telecom, Distrito Centro y Villa Conecta son ficticios. Los datos son sintéticos; los escenarios financieros son supuestos no calibrados. **Cambiar la selección comercial no demuestra mayores ventas ni valor económico incremental.**

## Estado actual y seis entregables

La Control Tower de las misiones 004B/004C **ya está integrada en `main`** mediante el PR #6, commit `c9194ed8425cc1f62eaac6174656a658810e6597`. La versión principal se ejecuta desde `main`; no requiere volver a la rama de diseño.

| Entregable del reto | Implementación o evidencia disponible | Límite principal |
|---|---|---|
| Business Framing | [Problema e hipótesis B2B](docs/01-product-brief.md) | Sin validación con clientes reales |
| Economic Graph | [Diseño](docs/06-economic-graph-design.md), [auditoría](docs/10-design-validation.md), ledger y consultas temporales | Conocimiento sintético parcial; identidad candidata sin fusión fuerte |
| AI/ML Approach | [Reglas explicables](docs/12-commercial-ranking.md) y [comparación T0/T1/T2](docs/13-ranking-comparison.md) | Sin modelo entrenado ni superioridad comercial medida |
| Architecture | [Arquitectura PoC y propuesta de producción](docs/04-architecture-overview.md), módulos públicos y adaptador UI | Producción, roles y escala no demostrados; consultar el estado vigente en la matriz |
| Economic Case | [Caso financiero](docs/14-incremental-economic-case.md), [calculador](docs/16-financial-calculation.md) y [experimento futuro](docs/15-incrementality-experiment.md) | Escenarios hipotéticos; sin A/B ejecutado ni ROI real |
| Control Tower | Cinco vistas, red observable, filtros y trazabilidad; [guía de demostración](docs/18-control-tower-demo.md) | Herramienta local, sin acciones comerciales ni despliegue productivo |

La [matriz de trazabilidad](docs/02-challenge-traceability.md) es la referencia del alcance y del estado actual. Algunos documentos de diseño conservan estados de misiones anteriores; los hallazgos pendientes de actualización se registran en esa matriz.

## Ruta rápida para evaluadores — Windows PowerShell

### 1. Requisitos y obtener `main`

Necesitas Git, acceso al repositorio y uv. Python debe ser 3.11 o superior; el proyecto fija **3.12** en `.python-version`. Si falta uv:

```powershell
winget install --id astral-sh.uv --exact
```

Abre otra terminal si uv no aparece en el PATH. Consulta las [alternativas oficiales de instalación](https://docs.astral.sh/uv/getting-started/installation/).

```powershell
git clone https://github.com/zeedher-aisuites/economic-graph-mvp.git
Set-Location economic-graph-mvp
git switch main
git pull --ff-only origin main
uv --version
uv python install 3.12
```

Si ya tienes el repositorio, omite el clon y conserva tus cambios antes de cambiar de rama. No uses reset ni force push para actualizarlo. Los comandos restantes se ejecutan desde su raíz y no dependen de rutas personales.

### 2. Instalar dependencias bloqueadas

```powershell
uv sync --locked --group ui
```

Se instalan el paquete, pytest, Ruff y el grupo opcional `ui` con Streamlit 1.66.0 en `.venv`. `--locked` exige coherencia entre manifiesto y lockfile; no actualiza dependencias. No hace falta activar el entorno. Mantén `--group ui` al usar uv: sin él puede retirar las dependencias opcionales de la interfaz.

La descarga inicial requiere internet o una caché disponible. **Después de instalar, la demostración offline no requiere MongoDB, credenciales ni `.env`**. El navegador solo se comunica con la aplicación local.

### 3. Ejecutar las pruebas offline y calidad

```powershell
$env:RUN_MONGODB_INTEGRATION = "0"
uv run --group ui pytest -m "not integration"
uv run --group ui ruff check .
uv run --group ui ruff format --check .
```

El marcador excluye la prueba de integración real: no se conecta a Atlas ni carga datos. Con el grupo UI se incluyen las pruebas de las cinco vistas. La prueba aislada conserva bloqueo de conexiones externas y acceso restringido al paquete público, ledger y configuración financiera. Detalles de compatibilidad Windows: [guía de la suite](docs/18-control-tower-demo.md#corrección-de-la-suite-tras-el-reporte-windows).

### 4. Iniciar la Control Tower y explorar sus cinco vistas

```powershell
uv run --group ui streamlit run app/control_tower.py
```

Abre la dirección local indicada por Streamlit. Inicia en **Resumen / T2 / Offline**. El servidor escucha en loopback; no es un despliegue multiusuario. Para detenerlo, pulsa `Ctrl+C`.

1. **Resumen:** 23 empresas conocidas, 21 elegibles y cinco priorizadas; dos selecciones compartidas y tres sustituciones entre políticas.
2. **Graph Health:** evolución T0/T1/T2, conexiones, estados, fuentes, conflictos e identidades candidatas. Empieza por Café Jacaranda y sus vecinos.
3. **AI Performance:** posiciones, contribuciones y empates. Café Jacaranda en T2 pasa de posición baseline 10/score 0 a posición grafo 3/score 10 por dos vecinos confirmados utilizables; el score no es una probabilidad.
4. **Business Funnel:** 23 → 21 → 5 y dos exclusiones aparte. Contactos, oportunidades, activaciones y ventas: **No observado**, nunca cero.
5. **Economic Impact:** cuatro escenarios para cinco y 500 plazas, reserva, sensibilidad y equilibrio. Todo resultado es hipotético, sin ventas atribuibles a las 30 PyMEs.

Industria y empresa filtran la presentación sin recalcular posiciones, scores ni top-5 globales. Usa **Mostrar todas las empresas** después de explorar una cuenta para recuperar el segmento global. Geografía, cluster, producto y canal no tienen soporte y se muestran deshabilitados. La economía agregada no se segmenta por empresa, industria o corte.

La [guía y guion de cinco minutos](docs/18-control-tower-demo.md) conecta la selección con su evidencia y con lo que faltaría medir realmente.

### 5. Reproducir el grafo y los rankings

Para mostrar acentos correctamente, también en las tuberías de PowerShell:

```powershell
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
uv run --group ui python scripts/inspect_graph.py --as-of T0 --summary
uv run --group ui python scripts/inspect_graph.py --as-of T1 --summary
uv run --group ui python scripts/inspect_graph.py --as-of T2 --summary
uv run --group ui python scripts/rank_companies.py --all-cuts --format markdown
uv run --group ui python scripts/rank_companies.py --as-of T2
```

Se consulta el ledger ya incluido, `data/observable/observations.json`. No hace falta regenerarlo, cargar datos ni consultar el oráculo. Los cortes son exactamente T0 `2026-01-15T12:00:00Z`, T1 `2026-05-15T12:00:00Z` y T2 `2026-09-15T12:00:00Z`; las consultas usan `available_at <= as_of`, no el final del día.

| Corte | Empresas conocidas | Observaciones | Afirmaciones económicas | Referencias |
|---|---:|---:|---:|---:|
| T0 | 12 | 28 | 2 | 0 |
| T1 | 17 | 54 | 13 | 2 |
| T2 | 23 | 83 | 26 | 3 |

Las afirmaciones no son todas relaciones confirmadas. Las referencias no cuentan como suministro ni aportan puntos. El universo de diseño restringido tiene 30 empresas y 48 relaciones verdaderas, pero las consultas comerciales no revelan las siete empresas nunca descubiertas ni completan atributos desde ese universo.

La política aprobada `003a-conservative-v1` usa cinco plazas y la misma cohorte para ambas alternativas. Baseline: 10 puntos por sucursal adicional observable sin conflicto, con máximo de 50. Grafo: misma base más 5 por vecino económico distinto confirmado utilizable, con máximo de 20 adicionales. Se excluye servicio activo confirmado sin conflicto; las demás cuentas quedan pendientes de validar comercialmente. Los empates por ID y las señales escasas se declaran explícitamente.

JSON conserva reglas, contribuciones, fuentes y fechas. Para inspeccionar Café Jacaranda:

```powershell
$ranking = uv run --group ui python scripts/rank_companies.py --as-of T2 | ConvertFrom-Json
$cafe = $ranking.companies | Where-Object { $_.display_name -eq "Café Jacaranda" }
$cafe.features | ConvertTo-Json -Depth 20
$ranking.comparison | ConvertTo-Json -Depth 20
```

Para procedencia de un atributo, toma un ID público CO-... de la vista completa:

```powershell
$vista = uv run --group ui python scripts/inspect_graph.py --as-of T2 | ConvertFrom-Json
$empresa = $vista.companies | Where-Object { $_.attributes.display_name.value -eq "Hornos del Centro" }
uv run --group ui python scripts/inspect_graph.py --as-of T2 --company $empresa.company_id --attribute branch_count
```

Atributos ausentes siguen desconocidos, conflictos sin arbitraje y alias sin fusión automática. La [auditoría de diseño](docs/10-design-validation.md) conserva las cinco advertencias conocidas y los límites de identidad, transición y caducidad.

### 6. Reproducir escenarios financieros

```powershell
uv run --group ui python scripts/calculate_finance.py --format markdown
uv run --group ui python scripts/calculate_finance.py --scope demo --format markdown
uv run --group ui python scripts/calculate_finance.py --scope hypothetical --format markdown
uv run --group ui python scripts/calculate_finance.py --sensitivity
```

El calculador `003b-finance-v1` lee exclusivamente [supuestos versionados](config/financial_assumptions.json), sin empresas, ledger ni Atlas. ECO-01 a ECO-06 fueron aprobadas provisionalmente solo como metodología educativa: MXN nominales, activación en 90 días, horizonte de doce meses, descuento mensual del 1% y reserva del 20%. No son datos financieros de Totalplay.

Se muestran conservador, base, optimista y nulo con incremento de conversión cero y costos conservados. Con cinco plazas los cuatro saldos son negativos. Con 500 plazas hipotéticas, el saldo base es +39 000 MXN y el nulo −41 000 MXN, antes de reserva. El equilibrio base de 1.025 puntos porcentuales es un **umbral requerido bajo supuestos**, no un efecto conseguido. La reserva se muestra aparte para evitar contabilizarla como gasto dos veces.

Cinco plazas de demostración, 500 hipotéticas y el experimento futuro son niveles distintos. No se generan ventas por empresa, muestras A/B, intervalos de un efecto real ni ROI causal. Un saldo positivo no autoriza invertir ni operar; fórmulas, unidades y límites en [el caso económico](docs/14-incremental-economic-case.md) y [sus resultados reproducibles](docs/16-financial-calculation.md).

## Atlas — alternativa opcional de solo lectura

Omite esta sección para la demostración offline. Requiere conectividad, autorización y datos ya cargados en la base dedicada `conectapyme_mvp_observable`. El proyecto no instala MongoDB ni modifica seguridad de Atlas.

Si no existe configuración privada local:

```powershell
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
notepad .env
```

Configura `MONGODB_URI` y `MONGODB_DATABASE` sin publicar sus valores. El ejemplo genérico sirve para ping; para consultar este MVP el nombre debe ser la base dedicada anterior. Usa credenciales con acceso de lectura autorizado, conserva TLS y nunca pegues la URI en capturas, reportes o terminales compartidas. Las variables del proceso tienen prioridad sobre `.env`; un valor vacío es un error. `.env` está ignorado por Git:

```powershell
git check-ignore .env
uv run --group ui python scripts/check_connection.py
uv run --group ui python scripts/inspect_graph.py --as-of T2 --summary --mongo
```

El ping exitoso devuelve código 0 y «Conexión verificada: MongoDB respondió a ping. No se escribieron datos.». No crea colecciones ni acredita permisos de escritura. Si falla, revisa presencia de variables, DNS, red, TLS y permisos sin revelar mensajes crudos del driver ni desactivar certificados. Los timeouts de cliente son de cinco segundos; DNS/SRV puede añadir tiempo.

En la UI elige **Atlas · solo lectura** y pulsa **Leer Atlas al corte**. Solo se realiza lectura temporal mediante `find`; se exige paridad con el ledger aprobado, no hay carga, índices ni fallback silencioso. Cambiar fuente/corte invalida la lectura anterior. También existe la CLI de rankings:

```powershell
uv run --group ui python scripts/rank_companies.py --mongo --as-of T2 --format markdown
```

El usuario reportó ping, consulta T2 y Control Tower en Atlas de solo lectura desde Windows sobre `main`/`c9194ed`. Esto no es acceso de Codex Cloud ni una ejecución reportada de la CLI de rankings `--mongo`. La [validación Atlas](docs/11-atlas-integration-validation.md) separa cada evidencia y sus límites.

## Evidencia de validación y procedencia

| Entorno y versión | Evidencia | Límite |
|---|---|---|
| Windows 11 / PowerShell / VS Code, `main` en `c9194ed`, reportado por el usuario | Instalación UI correcta; 284 pruebas aprobadas, una integración excluida; Ruff correcto, 60 archivos con formato correcto; cinco vistas funcionales; ping y lectura Atlas T2 | Reporte local, no ejecución Windows o Atlas de Codex; la suite de integración Atlas no fue ejecutada |
| Codex Cloud / Linux, Python 3.12.14, auditoría 005C sobre esa base | Instalación UI con lockfile; 284 aprobadas, una integración excluida; Ruff y formato correctos, 60 archivos; CLI offline de resúmenes, rankings y finanzas | Sin nueva ejecución nativa Windows, consulta Atlas ni revisión visual de navegador en 005C |

El detalle histórico de carga e idempotencia 002C y la evidencia posterior al merge están en [validación Atlas](docs/11-atlas-integration-validation.md). Las comprobaciones de interfaz y su historial están en [la guía de demo](docs/18-control-tower-demo.md). Los mocks no sustituyen respuestas del servidor.

## Organización y límites de entrega

| Ruta | Responsabilidad |
|---|---|
| `data/observable/observations.json` | Ledger público, única entrada empresarial offline para consultas y ranking |
| `src/economic_graph/observable.py` | Vista temporal, historia, conflictos e identidad candidata |
| `src/economic_graph/rankings.py`, `scripts/rank_companies.py` | Políticas aprobadas y CLI con explicaciones |
| `src/economic_graph/finance.py`, `scripts/calculate_finance.py`, `config/financial_assumptions.json` | Cálculo financiero puro, CLI y supuestos educativos |
| `app/control_tower.py`, `src/economic_graph/tower_read_model.py` | Cinco vistas y adaptación de cálculos existentes |
| `src/economic_graph/config.py`, `database.py`, `mongo_observable.py` | Configuración segura, ping, lectura temporal y carga protegida separada |
| `design-data/restricted/`, `src/economic_graph/simulator/` | Diseño aprobado y herramientas restringidas; nunca entrada de scoring o UI |
| `data/synthetic/restricted/` | Conciliación privada generada, ignorada por Git |
| `tests/` | Pruebas offline; integración real separada y opcional |
| `docs/` | Alcance, trazabilidad, auditorías, arquitectura, reglas y guías |
| `presentations/executive-deck.md`, `presentations/decision-log.md` | Presentación principal y decisiones; revisar hallazgos de estado en la matriz |
| `presentations/references/` | Reto original conservado como referencia |
| `AGENTS.md` | Reglas de colaboración y contexto de misiones anteriores |

Las herramientas de desarrollo `validate_design.py` y `build_observable.py --dry-run` auditan el diseño restringido. La generación normal del ledger y `load_observable.py --apply` **escriben** y no forman parte de esta ruta de evaluación. El procedimiento histórico y las protecciones están en [la auditoría de diseño](docs/10-design-validation.md). La prueba marcada `integration` también puede cargar datos: no se necesita ni se activa para esta entrega de solo lectura.

Sin UI, las CLI funcionan con `uv sync --locked` y `uv run python ...`; las pruebas de interfaz se omiten si Streamlit no está instalado. Para verificar toda la suite offline anterior usa el grupo `ui`. En entornos cloud con caché no escribible puede usarse `UV_CACHE_DIR` apuntando a una ruta permitida; Windows normalmente no necesita ese ajuste.

No existen modelo predictivo, agentes, campañas, eventos de contacto, ventas o experimento A/B ejecutado. La arquitectura productiva, roles operativos, escala y validación con clientes son propuestas. El laboratorio CRM independiente de 240 prospectos no pertenece a este repositorio ni a las 30 empresas del Economic Graph; `CRM` aquí es uno de los cinco tipos de fuente sintética.

Para la entrega final quedan consolidar el brief de 2–3 páginas y revisar los documentos fuera del alcance de esta auditoría que mantienen estados antiguos. La siguiente fase de evidencia económica requeriría datos autorizados, costos calibrados y un experimento defendible por bolsas independientes, con ITT y sin inferencia causal si faltan unidades suficientes. La aprobación metodológica de la PoC no autoriza contactos, presupuesto, piloto ni despliegue.
