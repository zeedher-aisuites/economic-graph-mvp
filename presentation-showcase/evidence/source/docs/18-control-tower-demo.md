# Control Tower ejecutiva — uso y demostración 004B/004C

**Estado actual:** aplicación local 004B/004C integrada en `main` mediante el PR #6, commit `c9194ed8425cc1f62eaac6174656a658810e6597`. CT-01 a CT-05 aprobadas expresamente por el usuario, con red interactiva sencilla añadida a CT-02. Datos sintéticos, escenarios no calibrados y experimento futuro conservan etiquetas distintas. No hay operaciones comerciales ni resultados causales.

**Validación posterior al merge reportada por el usuario:** Windows 11 / PowerShell / VS Code, `main` en `c9194ed`, árbol limpio; instalación correcta, 284 pruebas aprobadas y una integración excluida, Ruff sin errores y 60 archivos con formato correcto. Confirmó las cinco vistas y reportó ping, lectura T2 y captura de la Control Tower en Atlas de solo lectura. Son ejecuciones locales suyas, no de Codex Cloud; detalle y límites en [validación Atlas](11-atlas-integration-validation.md). Las 271 pruebas de 004B son un antecedente histórico, superado por este reporte.

## Instalar y ejecutar

Desde la raíz del checkout, en Windows PowerShell:

```powershell
git fetch origin
git switch main
git pull --ff-only origin main
uv sync --locked --group ui
uv run --group ui streamlit run app/control_tower.py
```

Si tienes cambios propios, consérvalos antes de cambiar de rama; no uses reset o force push. Requisitos base y cómo instalar uv están en el [README](../README.md). La instalación inicial requiere paquetes descargados o caché; después el modo offline no utiliza red externa, credenciales o `.env`. El servicio escucha solo en `127.0.0.1`; abre su dirección en el navegador de esa misma laptop. Para detenerlo, `Ctrl+C`. No es un despliegue ni una aplicación multiusuario protegida.

La dependencia directa UI es **Streamlit 1.66.0**, fijada en el grupo opcional `ui` con `uv.lock`; incluye transitivas como pandas, NumPy, PyArrow, Altair y PyDeck. 004C no añade dependencias ni modifica lockfile. No se añade biblioteca directa de grafos ni se ejecuta Graphviz. No se usan mapas, CDN, HTML procedente de datos, agentes o APIs. Solo se aplica una regla CSS estática para reducir el margen superior. Telemetría desactivada en `.streamlit/config.toml`. Las CLI base siguen ejecutándose con `uv sync --locked` sin el grupo UI; sus pruebas omiten las de interfaz si no está Streamlit instalado.

## Cómo leer las cinco vistas

| Vista | Interpretación ejecutiva |
|---|---|
| Resumen | Hallazgo «El grafo modifica 3 de las 5 selecciones» → indicadores → ambas selecciones → cuatro tarjetas financieras hipotéticas con signo. Inicia T2/global/offline |
| Graph Health | Inicia en una empresa conocida y sus vecinos directos; red completa como opción secundaria. Vínculos que respaldan la señal se resaltan sin promover incertidumbre |
| AI Performance | Dos cuentas compartidas y tres sustituciones; matriz baseline/grafo con posiciones y puntos, caso Café Jacaranda. Reglas explicables, no IA predictiva |
| Business Funnel | Global T2: 23 → 21 → 5, exclusiones como rama separada. Contactos, contactos activados, oportunidades, activaciones y ventas: **No observado** |
| Economic Impact | Selector de cinco o 500 plazas, cuatro escenarios completos en tarjetas, umbral base hipotético visible. Sensibilidad y datos técnicos contraídos por defecto |

El score no es una probabilidad y una plaza no es un contacto. Identidad NEEDS_REVIEW no equivale a empresa resuelta. Conflictos y repeticiones se conservan; no se arbitran por conveniencia de visualización. Indicadores y denominadores detallados: [diseño](17-control-tower-design.md), sin una segunda definición de reglas.

### Explorar la red y una cuenta

Graph Health abre en **Empresa y vecinos**. El selector **Empresa** sincroniza red, ficha y observaciones: propone Café Jacaranda solo si es conocida en la industria/corte actuales; de lo contrario toma la primera opción pública ordenada. Es una elección de demostración, sin prioridad comercial nueva. Cambiar corte nunca conserva una cuenta desconocida en él. La red muestra vínculos incidentes y vecinos conocidos, incluyendo contexto fuera de la industria. La opción **Red completa del segmento** libera la selección de cuenta, la deshabilita y muestra todas las empresas de la industria al corte; vuelve al modo centrado para abrir una ficha.

Pasa el cursor para nombres, sector, estado y procedencia. La tabla legible muestra vínculo/verificación; el panel **Auditar vínculos y filtrar evidencia** conserva dirección Desde/Hacia, fuentes, LINK-ID y OBS-ID. La ficha y su historial están en **Ficha de cuenta y respaldo completo**, contraído inicialmente. No hay edición, arrastre ni nuevas inferencias.

- Color de líneas: suministro, alianza o referencia. Línea continua: confirmada; trazos: reportada; puntos: inferida. Descartes y conflictos tienen patrones distintos y texto en tabla.
- En modo centrado, línea gruesa = LINK-ID ya presente en la evidencia de vecinos de la feature aprobada de esa cuenta; línea fina = contexto sin aporte a su score. No se suman puntos por arista: deduplicación, conflictos, topes y exclusiones siguen gobernados por 003A. Una cuenta excluida no recibe un score visual nuevo.
- Formas de nodos: círculo con vínculo confirmado utilizable; rombo sin vínculo confirmado utilizable; cuadrado sin vínculo económico observado. Es evidencia al corte, no existencia o inexistencia en el mundo. Referencias se separan y nunca aportan puntos.
- Cuenta enfocada en el centro y vecinos alrededor; red completa en círculo. Posiciones deterministas decorativas, no distancias comerciales, comunidades o potencial de venta. Nombres de vecinos en varias líneas; más de diez nodos usan hover/tablas. No se dibujan aristas ocultas ni se completan datos del catálogo.
- La ficha muestra elegibilidad, posiciones/scores globales y aportes con reglas. Las cuentas excluidas muestran motivo sin score artificial. Historial incluye fuente, estado, evidencia y observed_at/recorded_at/available_at; identidades candidatas permanecen sin fusión.

### Filtros sin cambiar la política

Período usa las 12:00 UTC exactas de T0/T1/T2. Cambiar corte limpia selección/lectura anterior; ninguna opción o evolución revela futuro. Industria y empresa intersectan las salidas globales: una selección sectorial puede mostrar menos de cinco priorizadas, sin rellenar plazas ni cambiar posiciones. Vecinos fuera del segmento aparecen como contexto.

Fuente, tipo y verificación inspeccionan tablas de vínculos; no eliminan evidencia para recalcular puntos. Score mínimo inspecciona la tabla de rankings. Tarjetas y cobertura globales llevan su alcance; el funnel indica segmento/total. Geografía, cluster, producto y canal comercial quedan deshabilitados por ausencia de datos.

Después de explorar una cuenta, usa **Mostrar todas las empresas** en Resumen/AI/Funnel para restablecer explícitamente industria y empresa, sin tocar corte, fuente o políticas. Con una cuenta/industria filtrada, la comparación y el funnel describen ese segmento y pueden mostrar menos de cinco; no interpretar 1 → 1 → 1 de una cuenta como el total global. Las tarjetas globales de coincidencias/cambios siempre se rotulan como tales.

Economic Impact deshabilita filtros empresariales: usa solo supuestos agregados aprobados, sin pesos editables ni importación de archivos. Saldo positivo, superar reserva o equilibrio algebraico no autorizan invertir. Todas las cifras financieras están en valor presente al horizonte definido, no flujo observado por empresa.

## Atlas opcional y exclusivamente de lectura

Offline no carga configuración ni crea clientes MongoDB. Para Atlas, configura localmente variables como en README, con base `conectapyme_mvp_observable`, idealmente credencial de solo lectura de `m002b_observations`; no se publica su URI. Elige **Atlas · solo lectura** y pulsa **Leer Atlas al corte**. No basta elegir el modo ni tener variables presentes.

Se valida la base antes de crear cliente y solo se llama a `read_observations`/`find` con filtro temporal; cierra el cliente. No hay ping, metadata, índices, cargas o escrituras. El hash visible debe coincidir con el ledger aprobado al mismo corte; discrepancia bloquea la demo comparable. Errores no muestran mensajes crudos del driver, credenciales ni cifras locales como si fueran Atlas. Volver a Offline requiere selección explícita.

El estado de lectura y su instante UTC se conservan en sesión, sin URI. Cambiar corte/fuente invalida la lectura. Tras el merge, el usuario reportó ping exitoso, consulta T2 (23 empresas, 26 afirmaciones económicas, tres referencias, 83 observaciones, dos candidatos y dos atributos en conflicto) y una captura de la UI en Atlas de solo lectura con indicadores/rankings esperados. La [validación Atlas](11-atlas-integration-validation.md) registra esa procedencia local y la distingue del cierre histórico 002C. No es una lectura nueva de Codex, una ejecución independiente de la CLI de rankings en Atlas ni la suite de integración completa.

## Guion ejecutivo de aproximadamente cinco minutos

1. **0:00–0:45 · Resumen/T2.** Empezar por «El grafo modifica tres de las cinco selecciones». Mostrar 23 conocidas, 26 afirmaciones económicas (no todas confirmadas), 21 elegibles y ambas selecciones. Las tarjetas financieras tienen signos, pero son hipótesis: «Cambiar la selección no demuestra mayores ventas».
2. **0:45–2:00 · Graph Health.** Ya abre en Café Jacaranda y sus vecinos. Señalar líneas gruesas que respaldan su señal y trazos de evidencia incierta. Abrir la ficha: baseline posición 10/score 0 → grafo posición 3/score 10, por **dos vecinos económicos distintos confirmados utilizables**. El score no representa probabilidad de conversión. Abrir observaciones de respaldo con sus fechas y cerrar los paneles. Opcional: Hornos para explicar sucursales en conflicto, o red completa para contexto, sin interpretarla como potencial comercial.
3. **2:00–2:45 · Tiempo y comparación.** Cambiar a T0: solo 12 conocidas/28 observaciones, sin futuro. Volver a T2 y AI Performance; pulsar **Mostrar todas las empresas**. La matriz muestra dos compartidas, tres entradas y tres salidas, con posiciones globales. Caso Café y empates auditables; pesos exploratorios, sin modelo entrenado ni probabilidades.
4. **2:45–3:20 · Business Funnel.** Sin filtros, señalar la progresión 23 → 21 → 5 y la rama de dos exclusiones. Las etapas posteriores dicen No observado. «No son cero ventas: todavía no existen eventos que permitan medirlas». No hay autorización de contacto.
5. **3:20–4:30 · Economic Impact.** Inicia en cinco plazas, con pérdidas en los cuatro escenarios. Cambiar explícitamente a 500 plazas hipotéticas: base +39 000 MXN antes de reserva y nulo −41 000 MXN, junto a conservador y optimista. El equilibrio base de 1.025 pp es mejora requerida, no obtenida. Abrir sensibilidad solo si preguntan; no asociar cifras a las PyMEs ni a Totalplay.
6. **4:30–5:00 · Cierre.** «Construcción y trazabilidad sí son demostrables. Para decidir inversión faltan datos autorizados, identidad/cobertura/permisos, costos reales y un experimento por bolsas independientes con ITT. Si no hay suficientes bolsas, ese diseño no permite inferencia causal». No prometer despliegue.

## Respaldo por CLI

Si Streamlit no está disponible, las mismas fuentes/calculadores funcionan sin grupo UI. Ejecutar desde la raíz:

```powershell
$env:PYTHONUTF8 = "1"
uv sync --locked
uv run python scripts/inspect_graph.py --as-of T2 --summary
uv run python scripts/rank_companies.py --all-cuts --format markdown
uv run python scripts/calculate_finance.py --format markdown
uv run python scripts/calculate_finance.py --sensitivity
```

Son consultas/cálculos offline; no ejecutar cargas o pruebas de integración para la demo. `docs/13-ranking-comparison.md` y `docs/16-financial-calculation.md` son respaldos legibles. Para recuperar UI usa de nuevo `uv sync --locked --group ui` y `uv run --group ui streamlit run app/control_tower.py`.

## Validación y límites

Pruebas nuevas: `test_tower_read_model.py` y `test_control_tower.py`. Comprueban paridad con módulos públicos, cortes/opciones/evolución, red y estados, alias/conflictos, filtros sin reordenar, funnel sin ventas inventadas, finanzas intactas, Atlas mediante doble `find` sin escrituras, fallos y ejecución aislada pública sin red/env/simulador. Esquema Vega-Lite validado con la transitiva Altair; las revisiones históricas 004B/004C en navegador local Linux comprobaron el dibujo real. No hay pruebas de escala, inferencia o performance de producción.

La regresión aislada usa rutas con espacios/acentos y cp1252 estricto, sin forzar UTF-8 en el proceso hijo; Streamlit serializa la UI Unicode sin depender de stdout regional. Es una simulación en Linux, **no ejecución nativa Windows de Codex**. El usuario confirmó después del merge las cinco vistas en Windows y 284 pruebas aprobadas, con una integración excluida. También reportó la lectura real Atlas T2 y la UI en modo solo lectura. Ninguna evidencia local suya se atribuye a Codex Cloud. En 005C no hubo una nueva revisión de navegador, ejecución Windows o consulta Atlas de Codex; la validación offline no sustituye estas evidencias locales.

Resultados históricos 004B en Codex Cloud/Linux, Python 3.12.14:

| Comando/comprobación | Resultado |
|---|---|
| `uv sync --locked` y `RUN_MONGODB_INTEGRATION=0 uv run pytest`, sin grupo UI | 252 aprobadas, 3 omisiones: módulo UI, validación Vega opcional e integración real Atlas |
| `uv sync --locked --group ui` | Correcto; CLI y UI instaladas con lockfile |
| `RUN_MONGODB_INTEGRATION=0 uv run --group ui pytest` | **271 aprobadas, 1 integración real Atlas omitida**; 38 pruebas nuevas de adaptador/UI |
| `uv run --group ui ruff check .` | Correcto |
| `uv run --group ui ruff format --check .` | Correcto, 59 archivos formateados |
| Chromium local, laptop virtual 1366×900 | Cinco vistas y selección Café Jacaranda correctas; red dibujada, 0 errores JavaScript y 0 peticiones externas durante el recorrido |
| `git diff --check`, enlaces Markdown y comparación de archivos protegidos | Correctos; ledger, diseños, configuración financiera y módulos de dominio intactos |

La única instalación adicional directa fue Streamlit; el navegador usado para inspección ya existía en el entorno, sin añadirlo al manifiesto. Los tiempos de la prueba Linux no son una medición de rendimiento del equipo Windows ni un SLA. No se dispone de tiempos de arranque/refresco de la laptop Windows; medirlos sigue siendo opcional y no condiciona el reporte de funcionamiento confirmado.

### Corrección de la suite tras el reporte Windows

**Antecedente histórico 004B:** el usuario confirmó instalación en Windows 11, Python 3.12.10 y Streamlit 1.66.0 y reportó **269 aprobadas, una fallida, un error y una integración omitida**. Fallaron el primer fixture AppTest por timeout de 15 segundos y el subprocess público porque el bloqueo global de `socket.connect` impedía `socketpair()`. Ese reporte no incluye una pila del hilo en el instante del primer timeout.

**Inicialización de AppTest.** Se inspeccionó Streamlit 1.66.0: crea el bucle de eventos antes del contador del script y lo conserva sin ejecutarlo durante el render. No hay trabajo asíncrono propio de la aplicación. Se instrumentó una ejecución fría Linux: NumPy, PyArrow y pandas se importaron en `ScriptRunner.scriptThread`, dentro del presupuesto funcional; render frío aproximado de 1.90 s y repetido de 0.07 s. La preparación separada de NumPy/pandas/PyArrow/Altair tardó aproximadamente 0.55 s en otra medición y el primer AppTest preparado tardó 0.54 s. Son mediciones puntuales, no comparativa de rendimiento ni evidencia de tiempos Windows.

La prueba mezclaba carga inicial de dependencias nativas con su límite de render. Ahora `ui_test_support.prepare_ui_runtime` importa esas dependencias una vez, en el hilo principal, y registra tiempos por módulo como propiedad pytest. El límite funcional sigue **15 s**; el subprocess conserva 20 s por render y 60 s totales. No hay reintentos ni ampliaciones de timeout. La regresión aislada rechaza una primera importación pesada desde el hilo de script. Un watchdog captura pila antes del cierre si el timeout persiste, mostrando solo archivo/línea/función, sin código fuente, variables o secretos.

No se reprodujeron los 15 s en Linux; sin la pila del Windows original no puede atribuirse con certeza su duración a una DLL, antivirus, CPU o bloqueo concreto. La separación corrige el alcance del timeout y añade diagnóstico para comprobarlo en el equipo afectado; no se afirma que el arranque real de Windows haya sido medido o validado por Codex.

**Aislamiento de red.** El [fallback de socketpair de CPython 3.12.10](https://github.com/python/cpython/blob/v3.12.10/Lib/socket.py) crea un listener TCP loopback efímero y conecta su otro extremo; `asyncio` lo utiliza como canal interno de señalización. Bloquear cualquier `connect`, incluso el de ese par, rompe la inicialización de AppTest en Windows. El guard nuevo solo admite el endpoint recién enlazado dentro de la llamada confiable a `socketpair`, limitado al mismo hilo y a la duración de esa llamada. No es una excepción general para localhost.

La protección continúa activa antes de importar dependencias y ejecutar la UI: bloquea conexiones directas, `connect_ex`, DNS, `create_connection` y envío de datagramas; servicios de loopback ajenos también se rechazan. La prueba verifica intercambio real por el par local y ejecución de un bucle `asyncio`, seguida de rechazos explícitos a destinos externos y otros puertos locales. En Linux fuerza el fallback TCP de la biblioteca estándar cuando existe, con emulación equivalente como respaldo para versiones que no lo exponen; en Windows usa su implementación real. No se intentan conexiones externas para comprobar esos rechazos.

Se conservan **los 271 casos anteriores**, sin omitir ni borrar los dos casos reportados; las nuevas aserciones de regresión están dentro de la prueba aislada existente. Sigue copiando solo app, módulos públicos, ledger, configuración financiera aprobada y helper de pruebas a una ruta con espacios/acentos, sin simulador ni diseños privados. No cambia código de la aplicación, dependencias, ledger, rankings, finanzas ni Atlas.

Reejecución Linux tras la corrección: **271 aprobadas y una integración Atlas omitida**; Ruff y formato correctos. En aquel cierre se solicitó confirmación nativa Windows; posteriormente el usuario confirmó 271 pruebas y, tras el merge, 284. Para repetir offline y mostrar las fases más lentas desde la raíz:

```powershell
$env:RUN_MONGODB_INTEGRATION = "0"
uv sync --locked --group ui
uv run --group ui pytest -m "not integration" --durations=5
uv run --group ui ruff check .
uv run --group ui ruff format --check .
```

### Evidencia de pulido 004C

El usuario confirmó posteriormente el funcionamiento y las 271 pruebas en Windows. Este pulido conserva esa infraestructura de compatibilidad y añade 13 regresiones de presentación/interacción, sin retirar casos previos: red centrada/completa, foco temporal, resaltado basado en la feature, escalas/signos/umbral, paneles contraídos y regreso explícito al segmento global. El guion de arriba corresponde a la interfaz actual.

| Comprobación histórica 004C, Codex Cloud/Linux | Resultado |
|---|---|
| `uv sync --locked --group ui` | Correcto; manifiesto/lockfile intactos |
| `RUN_MONGODB_INTEGRATION=0 uv run --group ui pytest --durations=5` | **284 aprobadas, una integración real Atlas omitida**, 14.70 s en esta ejecución |
| Ruff / formato / `git diff --check` | Correctos; 60 archivos Python formateados |
| Chromium 1366×900, cinco vistas | Sin errores JavaScript, peticiones externas o desbordamientos horizontales en contenido principal; JSON no visible y paneles cerrados inicialmente |
| Interacciones en navegador | Foco/red completa/restablecimiento de segmento y cambio cinco→500 correctos; +39 000/−41 000 y umbral 1.025 pp visibles, auditoría JSON accesible al expandir |
| Archivos protegidos | Ledger, diseños, configuración, políticas, elegibilidad, scoring, finanzas, manifest/lock y acceso MongoDB sin cambios |

Las tarjetas financieras redondean a pesos enteros para lectura; tablas técnicas y JSON conservan centavos/precisión de origen. No se midió beneficio comercial, causalidad, rendimiento a escala ni una nueva conexión Atlas. En el cierre histórico 004C quedaron pendientes la comprobación nativa y la integración. El reporte posterior del usuario sobre `main`/`c9194ed` confirma funcionamiento en Windows y el merge del PR #6; el estado actual está al inicio de esta guía.

### Auditoría documental 005C — validación offline de Codex Cloud

Desde la base integrada `c9194ed`, en Linux/Python 3.12.14, se ejecutaron:

```bash
UV_CACHE_DIR=/workspace/.cache/uv uv sync --locked --group ui
RUN_MONGODB_INTEGRATION=0 UV_CACHE_DIR=/workspace/.cache/uv uv run --group ui pytest -m "not integration"
UV_CACHE_DIR=/workspace/.cache/uv uv run --group ui ruff check .
UV_CACHE_DIR=/workspace/.cache/uv uv run --group ui ruff format --check .
```

Resultado: **284 aprobadas y una integración excluida**; Ruff correcto y 60 archivos con formato correcto. Las pruebas AppTest incluyen cinco vistas y sus interacciones, sin sustituir una revisión visual nativa. Las CLI de resúmenes T0/T1/T2, rankings y finanzas también se ejecutaron offline: conteos esperados, dos compartidas/tres sustituciones, caso Café T2 10→3 y 0→10 por dos vecinos utilizables, y escenarios coincidentes con los supuestos versionados.

Esta misión solo actualiza cuatro documentos: no cambia interfaz, ledger, rankings, fórmulas, supuestos, dependencias ni Atlas. No se realizó nueva inspección en navegador, carga o suite de integración Atlas; tampoco se midieron resultados comerciales. Para el estado y pendientes de los seis entregables consulta la [matriz de trazabilidad](02-challenge-traceability.md).
