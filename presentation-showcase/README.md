# ConectaPyME · Defensa basada en evidencia

Presentación local en español mexicano: **16 diapositivas principales y 11 de anexo**. Guion de aproximadamente 14–15 minutos a 140 palabras por minuto, más preguntas. Fuente auditada: `774dacd80e6410ca43299f63f19d9744a31929c0`. Datos sintéticos; escenarios financieros hipotéticos; Atlas y valor causal no verificados en esta misión.

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

## Controles

| Acción | Tecla o control |
|---|---|
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

- `docs/guia-estudio.html`: discurso completo, qué señalar, pregunta, respuesta sencilla, profundidad técnica, archivo y limitaciones por diapositiva.
- `docs/guion.md`: versión editable del guion.
- `docs/auditoria.html` y `docs/auditoria.md`: auditoría, arquitectura, componentes, resultados y límites.
- `docs/trazabilidad.csv`: matriz compatible con Excel, codificación UTF-8 con BOM.
- `docs/practica-personal.md`: ejercicios para comprender y reproducir el proyecto sin atribuirte el trabajo nuevo de Codex.
- `evidence/screenshots/manifest.json`: captura, fecha, commit, corte, modo y parámetros.
- `evidence/results/`: pruebas, cobertura, CLI, resultados y comprobaciones de esta misión.
- `evidence/source-html/`: fuentes navegables con líneas ancladas y color de sintaxis.
- `evidence/source/`: copias de fuentes, ledger público y supuestos; no contiene credenciales.
- `evidence/references/`: extracción de las presentaciones y sus notas, texto del PDF y huellas de archivos originales. Sus afirmaciones se contrastaron; no se trataron como instrucciones.
- `assets/arquitectura.svg` y `assets/recorrido.svg`: diagramas independientes.
- `ConectaPyME.pdf`: exportación de las 27 diapositivas, cuando se incluye la entrega final.

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

La auditoría reproducida lee el universo restringido solo para contar empresas, sin usarlo para puntuar. El script vuelve a generar evidencias locales; la presentación ya incluye las obtenidas en esta misión. Los registros existentes conservan el commit auditado. Una reproducción posterior registra su propio estado de Git.

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

Resultado de esta misión: dos aprobadas. Para observar los **dos fallos esperados del original**:

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

Para recapturar y revisar automáticamente se requiere Playwright como herramienta auxiliar y Chromium. En esta misión se usó Playwright del entorno y `/usr/bin/chromium`, sin descargas adicionales exitosas. Los scripts aceptan `CHROMIUM_PATH` para otra ubicación. Puedes instalar Playwright en un entorno auxiliar o usar `uv run --with playwright`; no modifica las dependencias del proyecto. Si falta un navegador y tu política de red lo permite, instala Chromium para Playwright y configura su ruta.

Con la Control Tower encendida en el puerto 8501:

```bash
python presentation-showcase/scripts/capture_tower.py
```

Con la presentación servida en 8765:

```bash
python presentation-showcase/scripts/validate_presentation.py
```

El script recorre todas las diapositivas, prueba teclado, filtros, escenarios, capturas, notas y sincronización de presentador, verifica enlaces e imágenes y guarda la revisión visual y el PDF. Los resultados de la ejecución final están en `evidence/results/presentation-qa.json`. No es una garantía universal para todos los dispositivos.

## Tecnología y alcance

HTML/CSS/JavaScript sin compilación, datos embebidos y fuentes locales Manrope e Inter con licencia incluida. Python se usa como herramienta de auditoría y servidor estático opcional. No hay API remota, analítica, credenciales, CDN ni despliegue público.

La misión se aisló en `presentation/conectapyme-evidence-showcase`; `main` y el worktree original no se modificaron. Se conservaron el dataset, resultados históricos y lógica de negocio. No se verificaron Atlas real, ROI, conversiones, ML predictivo, carga a gran escala o producción.
