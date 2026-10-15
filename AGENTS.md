# Instrucciones para Codex y colaboradores

**Proyecto:** ConectaPyME Economic Intelligence / SME Economic Graph\
**Objetivo prioritario:** responder al reto laboral: **«¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?»**\
**Plazo:** 3 días de ejecución del MVP.\
**Idioma de documentación:** español claro, comprensible para desarrolladores junior.

## 1. Orden de prioridad

1. Atender los seis apartados del reto laboral y ofrecer una defensa técnica, económica y experimental rigurosa.
2. Construir una prueba de concepto (PoC) pequeña y reproducible que aporte evidencias a esa defensa.
3. Reutilizar el caso en ICEméxico y apoyar el aprendizaje de análisis, arquitectura de datos y gestión de producto, solo si no compite con el objetivo principal.
4. Evaluar agentes de IA **después** de la entrega. No implementar ahora.

**Antes de programar una funcionalidad**, identificar qué requisito de `docs/02-challenge-traceability.md` cubre. Si no tiene relación, advertirlo y pedir decisión antes de añadirla.

## 2. Restricciones aprobadas

- Telco ficticia: **ConectaPyME Telecom**; escenario sintético: **Distrito Centro**, localidad de **Villa Conecta**.
- Inicialmente **30 PyMEs** ficticias y un historial comercial sintético que puede cubrir hasta 12 meses.
- Uso directo por personas: analistas comerciales y gerentes. **Sin agentes, LangGraph, LangChain, LLM, automatización autónoma ni integraciones con sistemas reales**.
- Preferir Python, MongoDB/PyMongo y análisis sencillo del grafo. Visualización solo si aporta evidencia; Streamlit es una **opción**, no una obligación.
- El MVP debe ser defendible con tablas, consultas y diagramas; evitar gastar tiempo en estética de la interfaz.
- No afirmar mejoras causales, precisión predictiva generalizable ni ROI comprobado a partir de 30 empresas sintéticas.

## 3. Forma de trabajar

- Inspeccionar archivos existentes antes de cambiarlos. Hacer cambios pequeños y delimitados.
- Mantener código simple, con funciones de nombres explícitos, responsabilidad única y tipado cuando mejore la comprensión.
- Evitar arquitecturas de múltiples capas, interfaces abstractas, patrones complejos y dependencias «para el futuro».
- Separar, cuando sea necesario, acceso a datos, lógica de negocio y presentación. **No** construir infraestructura para agentes futuros.
- Usar datos y semillas reproducibles; preservar procedencia y fechas.
- Distinguir **verdad sintética del simulador** de **datos observables por la Telco**. No introducir conocimiento privilegiado ni eventos futuros en rankings históricos.
- Diferenciar *observado*, *inferido*, *estimado* y *simulado* en datos, gráficos y reportes.
- Si hay dudas técnicas, documentar opciones y escoger la solución mínima suficiente. No presentar elecciones por conveniencia como estándares oficiales de MongoDB.

## 4. Seguridad y calidad

- Nunca subir contraseñas, URIs privadas ni claves. Usar `.env` local ignorado por Git y `.env.example` sin secretos.
- Añadir pruebas automatizadas de funciones críticas que no requieran conexión real a Atlas; aislar las pruebas de integración.
- Ejecutar las pruebas/linter disponibles y **reportar resultados reales**; no declarar verificaciones que no se ejecutaron.
- Mensajes de error claros y sin revelar credenciales.
- Actualizar documentación cuando cambie una decisión, un campo o el modo de ejecutar el proyecto.
- Documentar comandos para **Windows PowerShell**. Se propone `uv`; verificar compatibilidad con el entorno real.

## 5. Fuentes y rigor

- El reto laboral es la fuente prioritaria: contrastar los seis apartados con el archivo original cuando esté disponible.
- **No atribuir reglas al curso de MongoDB University sin revisar el material correspondiente.**
- Separar lo implementado de lo propuesto para producción. Un esquema conceptual no es un esquema de colecciones aprobado.
- En la evaluación económica, separar supuestos, ejemplos numéricos, resultados observados y diseño experimental futuro.
- Para atribución causal, plantear control, aleatorización cuando sea viable, ventana de medición, unidad de asignación, contaminación entre grupos y costo incremental.

## 6. Documentos de referencia

1. `docs/00-project-context.md` — motivación y preguntas centrales.
2. `docs/01-product-brief.md` — usuarios, flujo, funcionalidades y aceptación.
3. `docs/02-challenge-traceability.md` — trazabilidad de los seis entregables.
4. `docs/03-scope-and-decisions.md` — alcance, restricciones y decisiones pendientes.
5. `docs/04-architecture-overview.md` — arquitectura **propuesta**, no implementación confirmada.

## 7. Entrega de cada tarea

Explicar brevemente: **qué cambió**, **por qué**, **cómo ejecutarlo**, **qué pruebas se realizaron** y **qué quedó pendiente**. No crear documentos extensos ni funciones ajenas al alcance de la tarea.

## Comunicación ejecutiva y justificación de decisiones

El proyecto debe ser técnicamente defendible y comprensible para un CEO o director comercial de una empresa de telecomunicaciones.

Para cada decisión arquitectónica, analítica o económica importante:

1. Explicar qué problema resuelve.
2. Identificar las alternativas razonables consideradas.
3. Justificar la opción elegida.
4. Describir beneficios esperados, costos, riesgos y limitaciones.
5. Indicar cómo se comprobaría que la decisión fue correcta.
6. Registrar la decisión en `docs/03-scope-and-decisions.md` o en el registro de decisiones correspondiente.
7. Actualizar la presentación ejecutiva cuando la decisión afecte el argumento central del reto.

### Reglas para presentaciones

- Utilizar lenguaje claro y comprensible para directivos no técnicos.
- Cada diapositiva debe comunicar una idea principal.
- Preferir conclusiones y argumentos sobre descripciones de herramientas.
- Utilizar diagramas sencillos, comparaciones y visualizaciones cuando aporten claridad.
- No inventar estadísticas, mejoras de conversión, ingresos ni ahorros.
- Diferenciar resultados comprobados, datos sintéticos, escenarios hipotéticos y beneficios pendientes de validación.
- Mostrar supuestos y limitaciones de cualquier estimación económica.
- Conectar las decisiones importantes con la pregunta central: cómo generar y medir valor económico incremental.
- Mantener referencias internas que permitan rastrear las afirmaciones ejecutivas hasta la documentación o el código.

### Entregables de comunicación

Mantener `presentations/executive-deck.md` como fuente de la presentación ejecutiva.

No generar automáticamente nuevos archivos PowerPoint por cada modificación. Generar una versión exportable cuando se solicite o al preparar un hito de entrega.

No crear una diapositiva por cada decisión menor de implementación.

Priorizar la calidad del argumento empresarial sobre la cantidad de diapositivas.

## Reglas operativas desde la misión 001

- Trabajar sobre el repositorio existente `zeedher-aisuites/economic-graph-mvp` y revisar `git status` y el historial antes de editar. Usar ramas descriptivas, commits delimitados y push verificado por SHA remoto; abrir PR cuando el acceso lo permita. Nunca usar force push ni eliminar trabajo ajeno.
- Conservar `uv.lock`; reproducir con `uv sync --locked`. Antes de publicar, ejecutar `uv run pytest`, `uv run ruff check .` y `uv run ruff format --check .`. Las pruebas unitarias deben funcionar sin MongoDB ni credenciales.
- Mantener `.env` ignorado y `.env.example` sin secretos. No registrar valores de configuración ni errores crudos del driver. Una conexión real solo está verificada si respondió a `ping`; los dobles de prueba no la sustituyen.
- La matriz `docs/02-challenge-traceability.md` gobierna los seis entregables. La fuente original exige Control Tower como dashboard o prototipo y un brief final de 2–3 páginas. No confundir una interfaz opcional con un entregable opcional.
- Registrar decisiones importantes en `presentations/decision-log.md` y actualizar alcance, arquitectura y la única presentación principal cuando corresponda. Conservar los estados **aprobada**, **propuesta** y **descartada**; nunca convertir pendientes en aprobaciones implícitas.
- Separar archivos sintéticos de cualquier dato real. No almacenar datos reales en `data/synthetic/`; incorporar datos reales requerirá autorización y controles de privacidad. Identificar procedencia, temporalidad y naturaleza de cualquier resultado.
- La misión 001 termina en infraestructura, documentación, pruebas y publicación. No generar las 30 empresas, relaciones, scoring, ML, dashboard ni Economic Graph en esta misión. No inventar métricas, resultados económicos ni operaciones Git exitosas.
