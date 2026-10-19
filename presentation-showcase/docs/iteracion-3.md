# Misión 3 · Evidencias que puedo abrir durante la exposición

Esta iteración añade siete paneles opcionales a cuatro diapositivas. Conserva las 16 diapositivas principales, los 14 anexos y el discurso principal de la versión anterior. Preparación y comprobación de esta misión realizadas por Codex; no se atribuyen al candidato como ejecuciones personales.

Rama: `presentation/conectapyme-contextual-evidence`, desde `23a8efac164f8631dae57e9c9e8e3bcf9efe66ae`. El PR apunta a `presentation/conectapyme-junior-pov`, sin fusionar. Los cambios se limitan a `presentation-showcase/`. No se modifica el motor ni las ramas anteriores.

## Cómo los muestro

1. Abro la presentación y su ventana **Presentador** en el mismo navegador y dirección local. Uso una sola ventana de audiencia.
2. En una de las cuatro diapositivas, elijo un botón de **Evidencias para mostrar**. El panel aparece en la ventana de diapositivas; un mensaje confirma su recepción.
3. Explico primero la tabla y el razonamiento. Si me preguntan por el origen, despliego **Nivel técnico**: JSON completo, ruta, IDs o líneas, commit, huella, descarga y funciones/pruebas.
4. Cierro con **Cerrar evidencia en diapositivas** desde mis notas, o con Esc o la X en la audiencia. Regreso a la misma diapositiva y el reloj continúa.

Los mismos paneles están en **Fuentes, reproducción y límites** (E) y en las notas (N). No se abren pestañas externas automáticamente. Solo los enlaces al código abren una fuente cuando se solicitan. En filtros, puedo ampliar la captura dentro del panel y volver a la explicación con el mismo filtro.

La comunicación usa BroadcastChannel. La vista previa del presentador queda excluida. Si no se recibe confirmación en 900 ms, aparece una copia local con un aviso; la alternativa es abrir el mismo panel con E en la ventana que comparto. Esto no prueba que una ventana esté visible en un monitor físico. La selección de pantalla para una videollamada sigue siendo manual.

## Qué demuestra cada panel

| Diapositiva / panel | Datos que puedo señalar | Límite que debo reconocer |
|---|---|---|
| `procedencia` / `hornos` | OBS-028: 2, REPORTED; OBS-047: 3, REPORTED; OBS-075: 3, CONFIRMED. Las tres conservan CG-001. | La mayoría y la última confirmación no resuelven los valores distintos. Cero puntos por sucursales no significa cero sucursales. Una coincidencia de nombre no demuestra identidad. |
| `cambio` / `leaders` | Panificadora: OBS-048/076, seis sucursales, 50 puntos y #1. Carga Urbana: OBS-053, dos sucursales, 10 puntos y #2. Cero vecinos confirmados utilizables en ambas. | Las sucursales admiten evidencia reportada o confirmada sin conflicto; las relaciones exigen confirmación. Carga comparte 10 puntos con Jacaranda y Hornos: se ordenan por ID público, sin significado comercial. |
| `cafe` / `confirmed` | OBS-026 y OBS-063: suministro confirmado desde Enlace Punto POS y Hornos hacia Jacaranda. Dos vecinos × cinco puntos = diez; #10/0 → #3/10. | El cálculo cuenta vecinos distintos con tope de cuatro. La dirección se conserva; la regla considera ambos extremos. No demuestra intención de compra. |
| `cafe` / `context` | OBS-044 inferida; OBS-037/045/043/072 reportadas. Se conservan las cinco afirmaciones y sus tipos. Todas aportan cero a Jacaranda. | Ruta Corta tiene dos afirmaciones distintas. REFERRAL es una fuente; REFERS_TO es un tipo no económico. Papelería tiene otra evidencia que respalda su propio score; su relación inferida con Jacaranda no suma. |
| `arquitectura` / `ledger` | 83 observaciones; campos, procedencia y disponibilidad; ejemplos de nombre, sucursales y suministro leídos del archivo. | Son datos sintéticos observables y locales. No son 83 empresas ni una consulta en vivo a Atlas. |
| `arquitectura` / `finance` | Tres escenarios de configuración, cinco plazas por bolsa, tasas supuestas, margen, costos, 90 días, 12 meses, descuento mensual de 1% y reserva de 20%. | El código deriva el escenario nulo y las 100 bolsas/500 plazas. La ruta financiera no usa empresas ni scores; no acredita ventas reales. |
| `arquitectura` / `filters` | Capturas originales 08/09/10, sus parámetros y fechas. Tablas reproducidas con #10/#3 en global, industria y empresa. | `build_context()` calcula antes; `segment_ids()` selecciona IDs; `ranking_table()` conserva posiciones. No se rellena el Top 5. Capturas históricas de Streamlit, no sesión en vivo. |

No hubo contradicciones entre los estados esperados de la solicitud y el ledger. Sí se hace explícita una diferencia que podía confundirse: en Hornos las tres observaciones no están confirmadas. Los supuestos financieros distinguen lo declarado en JSON de lo derivado en código.

## Datos y fuentes de verdad

El origen técnico sigue siendo `774dacd80e6410ca43299f63f19d9744a31929c0`. Las capturas originales conservan su fecha, commit y manifest. No se recapturó ni modificó Streamlit.

`scripts/contextual_data.py` lee y valida `data/observable/observations.json`, ejecuta `build_context()` en T2 y reproduce `financial_report()`. Exige igualdad exacta con los resultados de V1. Resuelve nombres desde el snapshot público; no consulta el universo restringido. Las tablas de filtros usan las funciones originales. El JavaScript solo presenta esos datos congelados.

`evidence/iteration-3/data/observations.json` y `financial_assumptions.json` son copias exactas, byte a byte, de sus archivos de origen. La huella de cada archivo está en `contextual-evidence.json` y en los paneles. El JSON de salida del contexto y las finanzas se guarda por separado y se identifica como **resultado calculado**, no como registro original. Los fragmentos de código se extraen desde sus funciones reales.

La fuente de las notas y botones es `scripts/content.py`. `scripts/build_material.py` regenera datos embebidos, guion, guía y matriz. La matriz incorpora las afirmaciones nuevas y las columnas de paneles/JSON. Los discursos principales no aumentaron: las instrucciones de demostración están separadas como apoyo opcional.

## Validación y límites

La ejecución nueva de `uv run --group ui pytest` dio **284 aprobadas y una integración omitida**, en 19.71 s. El registro se conserva en `evidence/iteration-3/results/pytest.txt`. No se ejecutó Atlas ni se modificaron credenciales.

`scripts/validate_contextual_evidence.py` comprueba:

- Las 30 diapositivas contra las capturas de V2, píxel a píxel, a 1600×1030.
- Los siete paneles a 1600×1030, 1366×768 y 1920×1080; JSON, fuentes, descarga y cierre sin perder la sección.
- Los siete enlaces desde el presentador, selección remota de empresa/filtros, confirmación de apertura y cierre desde ambas ventanas, reloj y navegación.
- Pantalla completa nativa con paneles y un fallo controlado de BroadcastChannel con alternativa local.
- Ampliación de la captura y regreso a la explicación. En esta revisión se corrigió que el clic directo sobre la imagen no llegaba al botón que la contenía.
- Copia independiente con servidor HTTP local, sin Streamlit, Atlas, npm ni paquetes de ejecución.
- Igualdad de los archivos protegidos contra el commit de partida: producto, datos, pruebas, evidencias históricas, diagramas, experimento original y PDF.

El resultado final, las referencias comprobadas y las huellas están en `evidence/iteration-3/results/contextual-qa.json`. Las capturas nuevas de los paneles y sus controles están en `evidence/iteration-3/panels/`. El análisis estático y la sintaxis se registran en `results/final-checks.json`.

Resultado de la revisión en navegador: **PASS**. Se comprobaron 70 referencias, 21 composiciones de panel (siete por tres tamaños) y 329 archivos protegidos sin cambios. Las 30 diapositivas coinciden píxel a píxel con las capturas de V2 en el tamaño comparado. La reapertura inmediata también se prueba: un evento de cierre anterior no debe borrar el estado del panel nuevo. El JSON técnico usa letra más grande y se revisaron las capturas de ambos niveles, los selectores y la alternativa de comunicación.

El PDF original de esta versión se conserva byte a byte: **30 páginas**. Los paneles opcionales son exclusivos de la web; no se convierten en diapositivas obligatorias.

La revisión se hizo en Chromium/Linux. Windows nativo, dos monitores físicos, políticas de otros navegadores, Atlas real y resultados económicos comerciales siguen pendientes. Los paneles largos permiten desplazamiento vertical; el JSON y las funciones tienen áreas de consulta desplazables. No se garantiza legibilidad de tablas completas en teléfonos o en toda configuración de proyector.

## Ejecutar y regenerar

Desde la raíz del repositorio, en Windows:

```powershell
py -m http.server 8765 --bind 127.0.0.1 --directory presentation-showcase
```

Abrir `http://127.0.0.1:8765/`. No se requiere instalar paquetes para presentar. El README explica la clonación de la subrama y el uso de dos ventanas.

Para regenerar desde el repositorio:

```powershell
uv sync --locked --group ui
uv run python presentation-showcase/scripts/build_material.py
```

Con el servidor encendido y Playwright, Pillow y Chromium disponibles como herramientas auxiliares:

```powershell
python presentation-showcase/scripts/validate_contextual_evidence.py
```

El validador usa `/usr/bin/chromium` en el entorno revisado; para otra instalación se puede indicar `CHROMIUM_PATH`. La regeneración no consulta red ni Atlas. No se sobrescriben evidencias de V1/V2 ni su PDF.
