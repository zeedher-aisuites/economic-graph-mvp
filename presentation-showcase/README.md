# ConectaPyME · Defensa basada en evidencia

Versión anterior · ConectaPyME: caso de negocio B2B, con siete evidencias contextuales opcionales.

Presentación local en español mexicano: **16 diapositivas principales y 14 de anexo**. Guion de aproximadamente 14–15 minutos a 140 palabras por minuto, más preguntas. Fuente auditada: `774dacd80e6410ca43299f63f19d9744a31929c0`. Datos sintéticos; escenarios financieros hipotéticos; Atlas y valor causal no verificados en esta revisión.

## Abrir y presentar

**No necesitas Node, npm, Streamlit, Atlas ni instalar paquetes para ver la presentación.** Las fuentes, capturas, datos y código están incluidos. La opción verificada es abrirla con el servidor local indicado abajo; también permite sincronizar la ventana de presentador. El navegador administrado bloqueó `file://`, así que no se da por comprobada la apertura con doble clic en este entorno.

Desde este directorio:

```bash
python -m http.server 8765 --bind 127.0.0.1
```

En Windows PowerShell, si el comando `python` no está disponible:

```powershell
py -m http.server 8765 --bind 127.0.0.1
```

Abre **http://127.0.0.1:8765/**. En la raíz del repositorio también puedes usar:

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory presentation-showcase
```

El servidor escucha solamente en tu máquina. Detenlo con `Ctrl+C`. No publiques este contenido ni cambies la dirección de escucha para exponerlo sin revisar las autorizaciones del proyecto.

## Iniciar una exposición

1. Abre la página con el servidor local.
2. Pulsa **Iniciar presentación**: vuelve a la primera diapositiva, activa el modo limpio e intenta entrar en pantalla completa desde ese clic.
3. Usa las flechas para avanzar. **Esc** o **Salir · Esc**, en la esquina superior derecha, regresa al modo normal. Si tienes un panel abierto, el primer Esc lo cierra y el siguiente sale de la exposición.
4. Si estabas en otra diapositiva, **Continuar aquí** mantiene la posición actual.
5. Si el navegador rechaza la pantalla completa o no ofrece esa API, el modo inmersivo dentro de la ventana sigue funcionando. El aviso indica cómo usar **F11** o el menú del navegador. Puedes cerrar el aviso y continuar.

Para dos pantallas, abre **Presentador** antes de iniciar. Mueve esa ventana a tu pantalla de notas, regresa a la ventana de diapositivas y pulsa Iniciar presentación. Las flechas de cualquiera de las dos ventanas sincronizan la sección. **Ir a diapositivas** ayuda a enfocar o abrir la ventana de exposición; no la coloca automáticamente en otro monitor ni fuerza pantalla completa en ella.

Tú eliges la ventana que compartes desde Teams, Meet, Zoom o tu aplicación de reuniones. Esta página no solicita capturar la pantalla del sistema ni controla los permisos de esas aplicaciones.

## Evidencias opcionales durante la exposición

Las diapositivas mantienen su composición. En **Fuentes, reproducción y límites** (o E) y en las notas (N), las cuatro secciones muestran **Evidencias para mostrar**:

| Diapositiva | Paneles disponibles |
|---|---|
| Fuentes y dudas | Las tres observaciones de Hornos: 2/3/3, estados y conflicto |
| Cambio del Top 5 | Panificadora y Carga Urbana, cálculo y desempate por ID |
| Jacaranda | Dos relaciones que suman; cinco observaciones que no suman |
| Del archivo a la pantalla | Ledger observable, supuestos financieros y tres capturas de filtros |

En la ventana **Presentador**, pulsa el botón de una evidencia: el panel aparece en la ventana de diapositivas. El mensaje confirma cuando esa ventana lo recibe. Puedes elegir Carga Urbana o los tres filtros desde los controles secundarios del presentador. **Cerrar evidencia en diapositivas** cierra el panel remoto sin mover la sección. Esc o la X en la audiencia también lo cierran. El reloj continúa.

Abre una sola ventana de audiencia y una de presentador en el mismo navegador y origen (`http://127.0.0.1:8765`); no mezcles `localhost` y `127.0.0.1`. La vista previa del presentador no recibe los paneles. Si no llega confirmación en 900 ms, se abre una copia local con un aviso; también puedes abrir la misma evidencia desde E en la ventana que compartes. No se abren pestañas externas automáticamente. Los enlaces al código solo abren una fuente si tú haces clic.

Cada panel empieza con datos explicados. **Nivel técnico** despliega los registros completos, ruta, identificadores o líneas, commit, huella del archivo, descarga de la copia exacta y funciones/pruebas. Las capturas de filtros se amplían dentro del panel; **Volver a la explicación** conserva el filtro elegido.

Los paneles son exclusivos de la web y no forman parte de las 30 páginas obligatorias del PDF. Los discursos principales conservan su duración; las demostraciones son opcionales.

## Windows: apertura desde una copia nueva

Puedes descargar la rama `la versión pública aprobada` desde GitHub o clonarla en otra carpeta:

```powershell
git clone --branch la versión pública aprobada --single-branch https://github.com/zeedher-aisuites/economic-graph-mvp.git ConectaPyME-presentacion
cd ConectaPyME-presentacion
py -m http.server 8765 --bind 127.0.0.1 --directory presentation-showcase
```

Abre http://127.0.0.1:8765/. Se requiere Python 3; `python` también sirve si ése es el comando configurado en tu instalación. No necesitas instalar paquetes para presentar. Cierra el servidor con Ctrl+C. La revisión automática de esta entrega se hizo en Chromium/Linux; la ejecución nativa en Windows queda por comprobar por separado.

## Controles

| Acción | Tecla o control |
|---|---|
| Iniciar desde primera | Botón Iniciar presentación |
| Continuar desde la actual | Botón Continuar aquí |
| Salir del modo limpio | Esc o Salir · Esc |
| Avanzar / regresar | Flechas derecha / izquierda; Espacio; PageDown / PageUp |
| Inicio / cierre de la principal | Home / End |
| Índice y acceso al anexo | I |
| Notas de la diapositiva | N |
| Ventana de presentador | P |
| Fuentes, comando y límites | E o botón “Fuentes y evidencia” |
| Pantalla completa | F |
| Cerrar panel o captura | Esc |
| Ampliar captura | Clic sobre la imagen |
| Pantalla táctil | Deslizar horizontalmente |

La ventana de presentador muestra la diapositiva, notas, pregunta, respuesta, archivos y reloj. Mantén la presentación y el presentador en el mismo navegador y servidor; se sincronizan mediante BroadcastChannel. Si el navegador bloquea ventanas emergentes, abre directamente `http://127.0.0.1:8765/?presenter=1`. Las notas integradas con N funcionan aun sin esa sincronización. El PDF es una copia estática: no conserva interacciones ni sustituye el guion.

Los controles de filtros y escala económica dentro de las diapositivas son **reconstrucciones con resultados congelados del repositorio**, identificadas como tales. Las imágenes de Streamlit son capturas auténticas, ampliables y con parámetros registrados.

## Qué consultar

- `evidence/iteration-3/`: copias exactas de los JSON, resultados reproducidos y capturas nuevas de paneles.
- `docs/guia-estudio.html`: discurso completo, qué señalar, pregunta, respuesta sencilla, profundidad técnica, archivo y limitaciones por diapositiva.
- `docs/guion.md`: versión editable del guion.
- `docs/trazabilidad.csv`: matriz compatible con Excel, codificación UTF-8 con BOM.
- `docs/practica-personal.md`: ejercicios para comprender y reproducir el proyecto sin atribuirte el trabajo nuevo de Codex.
- `evidence/screenshots/manifest.json`: captura, fecha, commit, corte, modo y parámetros.
- `evidence/results/`: pruebas, cobertura y cálculos originales de V1, conservados sin cambios.
- `evidence/iteration-2/`: validación nueva de la presentación, vistas de esta iteración y nuevas fuentes documentales. No sustituye los registros originales.
- `evidence/source-html/`: fuentes navegables con líneas ancladas y color de sintaxis.
- `evidence/source/`: copias de fuentes, ledger público y supuestos; no contiene credenciales.
- `evidence/references/`: extracción de las presentaciones y sus notas, texto del PDF y huellas de archivos originales. Sus afirmaciones se contrastaron; no se trataron como instrucciones.
- `assets/arquitectura.svg` y `assets/recorrido.svg`: diagramas independientes.
- `ConectaPyME.pdf`: exportación de las 30 diapositivas, cuando se incluye la entrega final.

## Reproducir el proyecto original

Esta parte requiere el repositorio completo. Ejecuta desde su raíz y conserva sus dependencias bloqueadas:

```bash
uv sync --locked --group ui
uv run --group ui pytest -m "not integration"
uv run --group ui streamlit run app/control_tower.py --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false
```

La app abre Resumen/T2/Offline. Mantén Offline. No ejecutes cargadores ni la integración que escribe en Atlas para esta demostración.

Resultados y filtro global:

```bash
uv run python presentation-showcase/scripts/reproduce.py
uv run python scripts/rank_companies.py --all-cuts --format markdown
uv run python scripts/calculate_finance.py --sensitivity --format markdown
uv run --group ui pytest tests/test_control_tower.py tests/test_tower_read_model.py tests/test_mongo_observable.py -q
```

Los comandos de reproducción técnica de esta sección pertenecen al proyecto original y pueden volver a generar registros. En esta iteración se conservaron intactas las evidencias de V1; no es necesario repetirlos para abrir la presentación.

La auditoría reproducida lee el universo restringido solo para contar empresas, sin usarlo para puntuar. El script vuelve a generar evidencias locales; la presentación ya incluye las obtenidas en esta revisión. Los registros existentes conservan el commit auditado. Una reproducción posterior registra su propio estado de Git.

Cobertura auxiliar, sin cambiar `uv.lock`:

```bash
uv run --group ui --with pytest-cov pytest -m "not integration" --cov=economic_graph --cov-branch --cov-report=term-missing
```

La cobertura del paquete no incluye `app/` o `scripts/`. Las 284 pruebas originales se distinguen de las dos pruebas experimentales añadidas.

## Experimento de depuración aislado

El motor original no se modificó. El defecto no aparece en el ledger aprobado: se reproduce con un fixture válido de fechas equivalentes. La variante por defecto usa una copia corregida en memoria:

```bash
uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q
```

Resultado de esta revisión: dos aprobadas. Para observar los **dos fallos esperados del original**:

```bash
SHOWCASE_SNAPSHOT_VARIANT=original uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q
```

PowerShell:

```powershell
$env:SHOWCASE_SNAPSHOT_VARIANT = "original"
uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q
Remove-Item Env:SHOWCASE_SNAPSHOT_VARIANT
```

Se conserva el diff propuesto, sin aplicarlo al motor. El hallazgo y la corrección experimental son trabajo de Codex. La capacidad personal de repetirlos se prepara en la guía de estudio; no se da por demostrada.

## Regenerar material y revisar en navegador

La presentación no requiere esta generación para abrirse. Para editar texto, modifica `scripts/content.py`; para diseño, `app.js` y `style.css`. Con el entorno del proyecto:

```bash
uv run python presentation-showcase/scripts/build_material.py
```

Para recapturar y revisar automáticamente se requiere Playwright como herramienta auxiliar y Chromium. En esta revisión se usó Playwright del entorno y `/usr/bin/chromium`, sin descargas adicionales exitosas. Los scripts aceptan `CHROMIUM_PATH` para otra ubicación. Puedes instalar Playwright en un entorno auxiliar o usar `uv run --with playwright`; no modifica las dependencias del proyecto. Si falta un navegador y tu política de red lo permite, instala Chromium para Playwright y configura su ruta.

Con la Control Tower encendida en el puerto 8501:

```bash
python presentation-showcase/scripts/capture_tower.py
```

Con la presentación servida en 8765:

```bash
python presentation-showcase/scripts/validate_contextual_evidence.py
```

El validador de versión anterior compara las 30 composiciones con V2, prueba los siete paneles, JSON, fuentes, controles remotos, cierre, pantalla completa y alternativa sin BroadcastChannel. Los resultados están en `evidence/iteration-3/results/contextual-qa.json`. Requiere Playwright y Pillow como herramientas auxiliares. No sobrescribe los registros ni el PDF anteriores. El script `validate_presentation.py` se conserva como herramienta histórica de V2 y no debe usarse para validar esta iteración: su copia independiente no incluye el nuevo componente. No es una garantía universal para todos los dispositivos.

## Tecnología y alcance

HTML/CSS/JavaScript sin compilación, datos embebidos y fuentes locales Manrope e Inter con licencia incluida. Python se usa como herramienta de auditoría y servidor estático opcional. No hay API remota, analítica, credenciales, CDN ni despliegue público.

Esta iteración trabaja exclusivamente en `la versión pública aprobada`, desde `23a8efac164f8631dae57e9c9e8e3bcf9efe66ae`. La rama padre `una versión privada anterior` se conserva intacta. La rama original `presentation/conectapyme-evidence-showcase` y `main` permanecen intactas. Se conservaron el dataset, resultados históricos y lógica de negocio. No se verificaron Atlas real, ROI, conversiones, ML predictivo, carga a gran escala o producción.
