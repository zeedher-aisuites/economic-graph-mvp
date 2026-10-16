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

## Alcance vigente — misión 002B

- La restricción de generación de misión 001 es histórica. El usuario aprobó los paquetes de `docs/06` a `docs/09` y los insumos de `design-data/restricted/` para materializar únicamente construcción, trazabilidad y observabilidad. Conservar datos e IDs aprobados; documentar cualquier desviación en `docs/10-design-validation.md` sin corregir hechos arbitrariamente.
- El universo privado tiene 30 empresas, 48 relaciones verdaderas, 3 afirmaciones falsas y 3 referencias. El plan tiene 83 observaciones, 12/17/23 empresas conocidas y cortes a las 12:00 UTC de 2026-01-15/05-15/09-15. Usar siempre `available_at <= as_of` con zona explícita.
- La interfaz comercial solo puede leer el ledger de `data/observable/` o la colección pública dedicada. No importar `simulator` en consultas comerciales ni acceder al catálogo para completar atributos. Eliminar campos privados y diagnósticos de verdad en texto; no exponer empresas nunca descubiertas ni IDs que revelen la clase verdadera/falsa de una afirmación.
- Mantener alias como candidatos y conflictos sin arbitraje automático. No inventar evidencia de fusión, caducidad o transición para completar ejemplos ausentes; ver DV-002 y DV-003. Los eventos comerciales siguen como contrato pendiente.
- Los diagnósticos no escriben. La carga es dry-run por defecto y solo puede aplicar en `conectapyme_mvp_observable`, con confirmación explícita, propiedad de colecciones comprobada y sin operaciones destructivas. Las credenciales del operador no deben entregarse al consumidor comercial.
- Detener la misión al publicar la implementación revisable: no implementar scoring, ventas, ML, economía, causalidad ni Control Tower; no integrar automáticamente en `main`.

## Alcance vigente — misión 003A

- La prohibición de scoring anterior describe el cierre histórico de 002B. El usuario autorizó dos rankings comparables y aprobó expresamente la política conservadora, elegibilidad y K=5, registrados en `docs/12-commercial-ranking.md` y DEC-009. Mantener esa versión; cambios de prioridades comerciales requieren aprobación explícita.
- Calcular exclusivamente desde el ledger observable o su lectura MongoDB temporal; mismo baseline, cohorte y capacidad para ambas políticas. Conservar evidencia, incertidumbre, conflictos, candidatos y empates. No editar el ledger ni consultar el oráculo para puntuar.
- La CLI de rankings es de solo lectura. No ejecutar cargas ni la prueba opcional de integración que escribe en Atlas durante esta misión; verificar paridad mediante dobles offline. No presentar 002C como validación real de los nuevos rankings.
- Conservar las tablas reproducibles y la trazabilidad. Cambiar una selección no acredita intención de compra, conversiones ni incremento causal. No implementar ventas simuladas, evaluación causal, ML, agentes ni Control Tower; publicar mediante PR sin integrar automáticamente en `main`.

## Alcance histórico — misión 003B, fase de diseño

- El usuario autorizó únicamente auditoría, fórmulas, variables, escenarios propuestos y diseño experimental, publicados como documentación en PR borrador desde `main` actualizado. No implementar todavía el simulador financiero ni el experimento.
- `docs/14-incremental-economic-case.md` y `docs/15-incrementality-experiment.md` separan evidencia, supuestos y resultados medibles futuros. ECO-01 a ECO-06 requieren revisión y aprobación expresa; no inferirla del PR ni de la aprobación de rankings 003A.
- Conservar políticas, código, pruebas, dependencias, ledger y Atlas. No consultar el oráculo para decidir resultados económicos ni transformar cambios de ranking en conversiones, ingresos o ROI causal. Mantener DEC-004/010 como propuestas hasta la aprobación correspondiente.

## Alcance vigente — misión 003B, calculador educativo

- El usuario aprobó provisionalmente ECO-01 a ECO-06, exclusivamente como metodología PoC, y autorizó calculador determinista, escenarios, sensibilidad y equilibrio. Se actualiza el PR #5 para revisión, sin integrarlo automáticamente. Registrar límites en `docs/14-incremental-economic-case.md` y DEC-004/010.
- Mantener separados cinco plazas de demostración, 500 plazas hipotéticas y protocolo experimental futuro. Mostrar deterioro, efecto nulo obligatorio, casos positivos y referencia de saldo cero sin ajustar parámetros para favorecer al grafo. No generar ventas por empresa ni atribuir resultados a las 30 PyMEs o a Totalplay.
- Etiquetar supuestos no calibrados, validar unidades/valoración temporal y evitar duplicar costos/reserva. Conservar rankings, ledger, oráculo, Atlas y dependencias. Probar matemáticas y CLI offline, incluido UTF-8 en Windows; no ejecutar integración que escribe en Atlas.
- La aprobación es metodológica, no validación financiera ni autorización de datos reales, contactos, presupuesto, piloto operativo o despliegue. El experimento es solo diseño: no calcular muestra sin varianza/ICC ni afirmar inferencia causal si faltan bolsas independientes suficientes.

## Alcance histórico — misión 004A, diseño de Control Tower

- El usuario autorizó auditoría y propuesta documental de arquitectura visual/técnica, páginas, indicadores, filtros, fuentes y aceptación en PR borrador desde `main` actualizado. No implementar interfaz, instalar Streamlit ni modificar código, pruebas, dependencias o lockfile en esta fase.
- Mantener CT-01 a CT-05 de `docs/17-control-tower-design.md` como propuestas hasta aprobación explícita. La Control Tower es obligatoria por el reto; eso no aprueba todavía su tecnología o diseño visual.
- Reutilizar como fuentes autorizadas los módulos de observabilidad, rankings y finanzas, sin reinterpretar reglas ni alterar ledger, políticas, supuestos u operaciones Atlas. Filtros no redefinen cohortes, posiciones o finanzas. No observar una venta no equivale a venta cero.
- Separar sintético observable, evidencia técnica con procedencia, hipótesis educativa y experimento futuro. Offline por defecto; Atlas solo diseño de lectura opcional. No avanzar a programar antes de revisar las decisiones CT.

## Alcance vigente — misión 004B, Control Tower local

- El usuario aprobó CT-01 a CT-05 y amplió CT-02 con red interactiva sencilla dentro de Graph Health. Implementar en la rama existente del PR #6, sin integrar en `main`. Streamlit en grupo opcional `ui`; usar Vega-Lite integrado y selector sincronizado, sin motor gráfico adicional ni nuevas fórmulas.
- Mantener cinco vistas, Resumen/T2/Offline por defecto. Distinguir afirmaciones y confirmaciones, referencias, conflictos, candidatos no fusionados y nodos sin evidencia. Filtros de inspección conservan puntuaciones, posiciones, top-5 y supuestos agregados. No escribir en Atlas ni ejecutar integración histórica que carga datos.
- Probar adaptador y UI con `uv run --group ui pytest`, además de Ruff y formato; mantener CLI base independiente. Registrar diferencias entre validación Linux, regresiones de codificación Windows y ejecución nativa Windows pendiente. Actualizar diseño, guía de demo, decisiones y trazabilidad con evidencia real.
