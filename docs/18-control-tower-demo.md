# Control Tower ejecutiva — uso y demostración 004B

**Estado:** aplicación local implementada para revisión del PR #6; CT-01 a CT-05 aprobadas expresamente por el usuario, con red interactiva sencilla añadida a CT-02. No integrada automáticamente en `main`. Datos sintéticos, escenarios no calibrados y experimento futuro conservan etiquetas distintas. No hay operaciones comerciales ni resultados causales.

## Instalar y ejecutar

Desde la raíz del checkout, en Windows PowerShell:

```powershell
git fetch origin
git switch mision-004a-control-tower-design
git pull --ff-only origin mision-004a-control-tower-design
uv sync --locked --group ui
uv run --group ui streamlit run app/control_tower.py
```

Si tienes cambios propios, consérvalos antes de cambiar de rama; no uses reset o force push. Requisitos base y cómo instalar uv están en el [README](../README.md). La instalación inicial requiere paquetes descargados o caché; después el modo offline no utiliza red externa, credenciales o `.env`. El servicio escucha solo en `127.0.0.1`; abre su dirección en el navegador de esa misma laptop. Para detenerlo, `Ctrl+C`. No es un despliegue ni una aplicación multiusuario protegida.

La dependencia directa nueva es **Streamlit 1.66.0**, fijada en el grupo opcional `ui` con `uv.lock`; incluye transitivas como pandas, NumPy, PyArrow, Altair y PyDeck. No se añade biblioteca directa de grafos ni se ejecuta Graphviz. No se usan mapas, CDN, HTML arbitrario, agentes o APIs. Telemetría desactivada en `.streamlit/config.toml`. Las CLI base siguen ejecutándose con `uv sync --locked` sin el grupo UI; sus pruebas omiten las de interfaz si no está Streamlit instalado.

## Cómo leer las cinco vistas

| Vista | Interpretación ejecutiva |
|---|---|
| Resumen | Inicia en T2, global: 23 conocidas, 26 afirmaciones económicas, 21 elegibles, tres sustituciones en cinco plazas. Muestra ambas selecciones, escenarios y qué falta medir |
| Graph Health | 83 observaciones, dos atributos en conflicto, dos registros candidatos; red y tabla por procedencia, evolución sin cortes futuros, historial y estado de identidad |
| AI Performance | Reglas explicables, no modelo entrenado: scores, posiciones, contribuciones, top-5, cobertura y empates; no precision/recall/lift sin etiquetas |
| Business Funnel | Conocidas = elegibles + excluidas; cinco priorizadas por política. Contactos, contactos activados, oportunidades, activaciones y ventas: **No observado**, sin barras o tasas falsas |
| Economic Impact | Cinco y 500 plazas separadas, cuatro escenarios completos incluido nulo, componentes, reserva, sensibilidad y equilibrio; **hipótesis educativas no calibradas** |

El score no es una probabilidad y una plaza no es un contacto. Identidad NEEDS_REVIEW no equivale a empresa resuelta. Conflictos y repeticiones se conservan; no se arbitran por conveniencia de visualización. Indicadores y denominadores detallados: [diseño](17-control-tower-design.md), sin una segunda definición de reglas.

### Explorar la red y una cuenta

En Graph Health, el selector lateral **Empresa** sincroniza red y ficha. La red muestra vínculos incidentes y vecinos directos, incluyendo contexto fuera de la industria seleccionada si ya es conocido al corte. Pasa el cursor para nombres, sector, estado y procedencia; la tabla preserva dirección Desde/Hacia, fuentes, LINK-ID y OBS-ID. Los puntos no admiten edición ni arrastre; la selección se hace con el control lateral.

- Color de líneas: suministro, alianza o referencia. Línea continua: confirmada; trazos: reportada; puntos: inferida. Descartes y conflictos tienen patrones distintos y texto en tabla.
- Formas de nodos: círculo con vínculo confirmado utilizable; rombo sin vínculo confirmado utilizable; cuadrado sin vínculo económico observado. Es evidencia al corte, no existencia o inexistencia en el mundo. Referencias se separan y nunca aportan puntos.
- Posiciones circulares deterministas: decorativas, no distancias comerciales, comunidades o potencial de venta. Más de diez nodos ocultan etiquetas superpuestas; nombres completos permanecen en hover/tablas. No se dibujan aristas ocultas ni se completan datos del catálogo.
- La ficha muestra elegibilidad, posiciones/scores globales y aportes con reglas. Las cuentas excluidas muestran motivo sin score artificial. Historial incluye fuente, estado, evidencia y observed_at/recorded_at/available_at; identidades candidatas permanecen sin fusión.

### Filtros sin cambiar la política

Período usa las 12:00 UTC exactas de T0/T1/T2. Cambiar corte limpia selección/lectura anterior; ninguna opción o evolución revela futuro. Industria y empresa intersectan las salidas globales: una selección sectorial puede mostrar menos de cinco priorizadas, sin rellenar plazas ni cambiar posiciones. Vecinos fuera del segmento aparecen como contexto.

Fuente, tipo y verificación inspeccionan tablas de vínculos; no eliminan evidencia para recalcular puntos. Score mínimo inspecciona la tabla de rankings. Tarjetas y cobertura globales llevan su alcance; el funnel indica segmento/total. Geografía, cluster, producto y canal comercial quedan deshabilitados por ausencia de datos.

Economic Impact deshabilita filtros empresariales: usa solo supuestos agregados aprobados, sin pesos editables ni importación de archivos. Saldo positivo, superar reserva o equilibrio algebraico no autorizan invertir. Todas las cifras financieras están en valor presente al horizonte definido, no flujo observado por empresa.

## Atlas opcional y exclusivamente de lectura

Offline no carga configuración ni crea clientes MongoDB. Para Atlas, configura localmente variables como en README, con base `conectapyme_mvp_observable`, idealmente credencial de solo lectura de `m002b_observations`; no se publica su URI. Elige **Atlas · solo lectura** y pulsa **Leer Atlas al corte**. No basta elegir el modo ni tener variables presentes.

Se valida la base antes de crear cliente y solo se llama a `read_observations`/`find` con filtro temporal; cierra el cliente. No hay ping, metadata, índices, cargas o escrituras. El hash visible debe coincidir con el ledger aprobado al mismo corte; discrepancia bloquea la demo comparable. Errores no muestran mensajes crudos del driver, credenciales ni cifras locales como si fueran Atlas. Volver a Offline requiere selección explícita.

El estado de lectura y su instante UTC se conservan en sesión, sin URI. Cambiar corte/fuente invalida la lectura. No se verificó una nueva integración real en 004B: la evidencia Windows de [002C](11-atlas-integration-validation.md) sigue siendo reporte del usuario y no acredita funcionamiento actual de esta UI en Atlas.

## Guion ejecutivo de aproximadamente cinco minutos

1. **0:00–0:45 · Resumen/T2.** «Conocemos 23 empresas a partir de 83 observaciones ficticias. Tenemos 26 afirmaciones económicas, no 26 vínculos confirmados. Podemos investigar cinco cuentas. Las políticas comparten dos selecciones y cambian tres; eso aún no es venta». Mostrar las dos tablas.
2. **0:45–2:00 · Graph Health.** Seleccionar Café Jacaranda. Mostrar red directa, tipos/estados y vecinos conocidos. Abrir ficha: baseline posición10/score0, grafo posición3/score10, dos vecinos confirmados utilizables. Abrir evidencia con fechas. Seleccionar Hornos del Centro para explicar sucursales en conflicto y cero aporte individual, sin afirmar cero sucursales.
3. **2:00–2:45 · Tiempo y comparación.** Volver a Todas y cambiar a T0: solo 12 conocidas/28 observaciones. Nada futuro aparece. Volver a T2/AI Performance: empates y cobertura 3/21 individual, 5/21 relacional. Pesos exploratorios, sin modelo entrenado, probabilidades ni superioridad comercial medida.
4. **2:45–3:20 · Business Funnel.** Mostrar 23 conocidas, 21 elegibles, dos excluidas y cinco priorizadas. Industria filtra el segmento sin rehacer el ranking. «Contactos y ventas no están observados; no los contamos como cero». Ninguna cuenta está autorizada para contacto real.
5. **3:20–4:30 · Economic Impact.** Mostrar pérdidas con cinco plazas y resultados hipotéticos de 500: base +39 000 MXN antes de reserva; nulo −41 000 MXN. Mostrar conservador/optimista juntos y sensibilidad. «Son supuestos educativos, independientes de estas empresas; no hemos ganado ese dinero». Explicar equilibrio como mejora mínima que cubriría costos, no efecto probado.
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

Pruebas nuevas: `test_tower_read_model.py` y `test_control_tower.py`. Comprueban paridad con módulos públicos, cortes/opciones/evolución, red y estados, alias/conflictos, filtros sin reordenar, funnel sin ventas inventadas, finanzas intactas, Atlas mediante doble `find` sin escrituras, fallos y ejecución aislada pública sin red/env/simulador. Esquema Vega-Lite validado con la transitiva Altair; navegador local Linux comprueba dibujo real. No hay pruebas de escala, inferencia o performance de producción.

La regresión aislada usa rutas con espacios/acentos y cp1252 estricto, sin forzar UTF-8 en el proceso hijo; Streamlit serializa la UI Unicode sin depender de stdout regional. Es una simulación de esa condición en Linux, **no ejecución nativa Windows11**. Antes de integrar, el usuario debe ejecutar en Windows los comandos del README, explorar las cinco vistas, seleccionar cuentas, comprobar acentos y contrastar tablas con las CLI. La revisión visual local y lectura real opcional de Atlas quedan pendientes de ese equipo; no se presentan como verificadas por Codex Cloud.

Resultados reales en Codex Cloud/Linux, Python 3.12.14:

| Comando/comprobación | Resultado |
|---|---|
| `uv sync --locked` y `RUN_MONGODB_INTEGRATION=0 uv run pytest`, sin grupo UI | 252 aprobadas, 3 omisiones: módulo UI, validación Vega opcional e integración real Atlas |
| `uv sync --locked --group ui` | Correcto; CLI y UI instaladas con lockfile |
| `RUN_MONGODB_INTEGRATION=0 uv run --group ui pytest` | **271 aprobadas, 1 integración real Atlas omitida**; 38 pruebas nuevas de adaptador/UI |
| `uv run --group ui ruff check .` | Correcto |
| `uv run --group ui ruff format --check .` | Correcto, 59 archivos formateados |
| Chromium local, laptop virtual 1366×900 | Cinco vistas y selección Café Jacaranda correctas; red dibujada, 0 errores JavaScript y 0 peticiones externas durante el recorrido |
| `git diff --check`, enlaces Markdown y comparación de archivos protegidos | Correctos; ledger, diseños, configuración financiera y módulos de dominio intactos |

La única instalación adicional directa fue Streamlit; el navegador usado para inspección ya existía en el entorno, sin añadirlo al manifiesto. Los tiempos de la prueba Linux no son una medición de rendimiento del equipo Windows ni un SLA. Cronometrar arranque/refresco en la laptop de presentación y registrar esa evidencia durante la revisión pendiente.
