# Guion de exposición y defensa técnica

Fuente auditada: `774dacd80e6410ca43299f63f19d9744a31929c0`. Capturas offline; datos sintéticos. Investigación y verificación nuevas realizadas por Codex.

Las notas están en primera persona para facilitar el ensayo. No atribuyen al candidato las verificaciones de esta misión. Duraciones estimadas a 140 palabras por minuto; practicar en voz alta.

## 01. Elegir a quién investigar primero

**Tipo:** Demostrado · sintético · **Duración orientativa:** 59 s

### Discurso

Presento ConectaPyME, un prototipo para decidir qué pequeñas empresas conviene investigar primero cuando un equipo comercial tiene tiempo limitado. El grafo representa empresas y sus relaciones económicas. Mi punto de partida es una pregunta sencilla: ¿conocer las relaciones entre negocios cambia la lista que revisaríamos? En este proyecto sí cambia. Con los mismos datos disponibles y cinco lugares, tres empresas son distintas al agregar relaciones confirmadas. Ese es el resultado técnico que voy a mostrar. Todavía no puedo decir que esas empresas compren más o que el proyecto genere ganancias. Para eso faltan resultados comerciales y una comparación controlada. Durante esta revisión, Codex volvió a ejecutar el código y las pruebas, y obtuvo las capturas que veremos. Yo puedo usar esa evidencia para explicar el funcionamiento, sin presentar el trabajo de esta revisión como una experiencia personal mía.

### Qué señalar

Señala tres lugares distintos de cinco y la etiqueta de datos sintéticos.

### Pregunta del evaluador

¿Qué resultado concreto demuestra el proyecto?

**Respuesta sencilla:** Que agregar relaciones confirmadas cambia la priorización. Todavía no demuestra más ventas.

**Si profundiza:** Se comparan dos políticas deterministas sobre la misma cohorte, corte y capacidad K=5; se reproducen tres entradas y tres salidas del Top 5.

**Verificar en:** src/economic_graph/rankings.py:145–233; app/control_tower.py:283–313

**Reproducción:** `uv run python scripts/rank_companies.py --as-of T2 --format markdown`

**Límite:** Los datos son ficticios. Cambiar una selección no mide su calidad comercial.

## 02. Hay más cuentas que tiempo

**Tipo:** Hipótesis de negocio · **Duración orientativa:** 54 s

### Discurso

La idea es bastante sencilla: un equipo no puede investigar todas las cuentas al mismo tiempo. Necesita una lista con razones claras para empezar por algunas. En este ejercicio uso cinco lugares, y comparo dos maneras de llenarlos. La primera utiliza información individual de las empresas. La segunda agrega relaciones económicas confirmadas. Mantengo el mismo grupo y el mismo cupo para que la diferencia venga de la regla de prioridad. No estoy afirmando que este sea el principal problema actual de Totalplay; esa parte necesitaría entrevistas y datos del negocio. Tampoco significa que las cinco seleccionadas ya estén listas para recibir una llamada. Todavía faltaría comprobar cobertura, identidad, producto y permiso de contacto. Por ahora la decisión es a quién investigar, no a quién venderle automáticamente.

### Qué señalar

Marca el cupo de cinco y las dos listas comparables.

### Pregunta del evaluador

¿Por qué elegiste cinco cuentas?

**Respuesta sencilla:** Es la capacidad aprobada para esta demostración. No viene de una medición del equipo de ventas.

**Si profundiza:** POLICY fija capacity=5. El filtro de servicio activo es una elegibilidad sintética mínima, distinta de la elegibilidad operativa propuesta para un piloto.

**Verificar en:** docs/01-product-brief.md:1–87; src/economic_graph/rankings.py:12–22; src/economic_graph/tower_read_model.py:99–115

**Reproducción:** `uv run python scripts/rank_companies.py --as-of T2`

**Límite:** El problema comercial y los pesos necesitan validarse con personas y datos reales.

## 03. Solo usamos lo que ya se sabía

**Tipo:** Demostrado · sintético · **Duración orientativa:** 54 s

### Discurso

En el diseño sintético existen treinta empresas, pero el sistema no conoce a todas desde el principio. En enero conoce doce; en mayo, diecisiete; y en septiembre, veintitrés. Las observaciones acumuladas son veintiocho, cincuenta y cuatro y ochenta y tres. La regla importante usa available_at, que significa cuándo estuvo disponible cada dato. No basta con que un hecho haya ocurrido antes: si todavía no se había registrado y puesto a disposición, no debe aparecer en un ranking histórico. Cada corte usa un instante exacto, con zona horaria. Esto me permite volver a una fecha y explicar con qué información se tomó la decisión. Las treinta empresas son una referencia del diseño, mientras que la interfaz solo trabaja con las que realmente conoce dentro de la simulación.

### Qué señalar

Recorre los tres cortes; distingue universo de diseño y conocimiento observable.

### Pregunta del evaluador

¿Por qué no usas solamente la fecha del hecho?

**Respuesta sencilla:** Porque un hecho pudo ocurrir antes y conocerse después. Para evitar usar información futura, filtro por disponibilidad.

**Si profundiza:** visible_observations valida el contrato y aplica parse_time(available_at) <= parse_time(as_of), ordena y devuelve una copia. Los cortes son a las 12:00 UTC, equivalentes a las 06:00 de Ciudad de México.

**Verificar en:** src/economic_graph/contracts.py:5–9; src/economic_graph/observable.py:38–45; src/economic_graph/observable.py:82–176; tests/test_observable.py:23–49

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** Los tres cortes no son tres experimentos ni mediciones independientes de ventas.

## 04. Cada dato conserva su respaldo

**Tipo:** Demostrado · sintético · **Duración orientativa:** 54 s

### Discurso

Un dato no es solamente un valor. También necesito saber de qué fuente vino, cuándo lo conocí y si está confirmado. Por eso cada observación conserva su identificador, fuente, fechas y estado. En Hornos del Centro hay valores distintos para el número de sucursales. El código conserva las alternativas y no elige una por ser más reciente. Para el ranking, esa señal en conflicto aporta cero puntos. Eso no significa que la empresa tenga cero sucursales; significa que no tengo una señal utilizable con esa regla. Con los nombres pasa algo parecido: una coincidencia genera un candidato de identidad, pero no fusiona negocios automáticamente. En T2 se conservan dos atributos en conflicto y dos registros candidatos. Así puedo reconocer una duda sin convertirla en una certeza inventada.

### Qué señalar

Señala las observaciones OBS-028, OBS-047 y OBS-075 y su contribución cero por conflicto.

### Pregunta del evaluador

¿Por qué no gana automáticamente el dato más nuevo?

**Respuesta sencilla:** Porque no hay una regla aprobada para resolver ese conflicto. Prefiero conservar las opciones y revisarlas.

**Si profundiza:** _attribute marca CONFLICTED si hay valores distintos en el historial visible. Las relaciones conservan historia de estados; las candidaturas usan normalización de nombres, sin identificación fuerte.

**Verificar en:** src/economic_graph/contracts.py:22–36; src/economic_graph/observable.py:61–70; src/economic_graph/observable.py:82–176; tests/test_tower_read_model.py:105–120

**Reproducción:** `uv run pytest tests/test_observable.py tests/test_tower_read_model.py -q`

**Límite:** CONFLICTED y UNKNOWN no significan que se haya demostrado un valor cero.

## 05. Dos reglas que puedo explicar

**Tipo:** Demostrado · reglas · **Duración orientativa:** 60 s

### Discurso

Para esta primera versión uso reglas, no un modelo entrenado. El baseline, que es la regla de referencia, da diez puntos por cada sucursal adicional válida, hasta cinco sucursales adicionales. La política con grafo conserva esos puntos y suma cinco por cada vecino económico confirmado y distinto, hasta cuatro vecinos. Aquí llamo vecino a otra empresa conectada por suministro o alianza. Si dos observaciones hablan del mismo vecino, no cuento dos vecinos. Tampoco sumo puntos por una referencia comercial, una inferencia o una relación solamente reportada. Elegir reglas permite seguir el cálculo hasta sus evidencias. Con datos sintéticos y sin resultados de conversión, no tendría una evaluación honesta de un modelo predictivo. Los puntos sirven para ordenar cuentas: diez puntos no significan diez por ciento de probabilidad de compra. Los pesos siguen siendo exploratorios y necesitarían evaluación con datos reales.

### Qué señalar

Explica cada sumando y los dos topes; aclara que son puntos.

### Pregunta del evaluador

¿Dónde está el machine learning?

**Respuesta sencilla:** Todavía no hay un modelo entrenado. El enfoque actual es una referencia explicable para comparar después, cuando existan etiquetas reales.

**Si profundiza:** Vecinos distintos en SUPPLIES_TO y PARTNERS_WITH CONFIRMED utilizables; REFERS_TO se marca NOT_ECONOMIC. Empates por score descendente e ID público ascendente.

**Verificar en:** src/economic_graph/rankings.py:42–56; src/economic_graph/rankings.py:97–129; src/economic_graph/rankings.py:145–233

**Reproducción:** `uv run pytest tests/test_rankings.py -q`

**Límite:** Los pesos no están calibrados con intención de compra ni ventas.

## 06. Cambian tres de las cinco cuentas

**Tipo:** Demostrado · T2 · **Duración orientativa:** 53 s

### Discurso

Aquí comparo las listas completas de cinco lugares. Dos cuentas se mantienen en ambas: Panificadora Valle Claro y Carga Urbana del Centro. Con el grafo entran Café Jacaranda, Hornos del Centro y Papelería Horizonte. Salen Comedor del Andén, Mesa de Barrio y Mapa Digital Studio. Esto se obtiene con las mismas veintiuna empresas elegibles del corte T2. La capacidad no crece y no agrego empresas que el sistema todavía desconoce. También hay empates, por eso el código usa el identificador público como desempate y los declara en la auditoría. Puedo afirmar que las relaciones modifican la priorización, pero todavía no que la lista nueva sea mejor para vender. Esa diferencia tendría que medirse con resultados de negocio y un grupo de comparación válido.

### Qué señalar

Sigue las tres entradas y tres salidas; evita interpretar tres cambios como tres ventas.

### Pregunta del evaluador

¿Tres sustituciones son una mejora del 60%?

**Respuesta sencilla:** No. Es un cambio en tres de cinco lugares. No mide una mejora en conversión o ingresos.

**Si profundiza:** comparison calcula intersección, entered_graph y left_baseline. Las posiciones se asignan a todos los elegibles antes de seleccionar las primeras cinco.

**Verificar en:** src/economic_graph/rankings.py:145–233; tests/test_rankings.py:1–456; docs/13-ranking-comparison.md:1–117

**Reproducción:** `uv run python scripts/rank_companies.py --all-cuts --format markdown`

**Límite:** Los empates y la baja cobertura de atributos pueden influir en el orden.

## 07. Café Jacaranda: del lugar 10 al 3

**Tipo:** Demostrado · T2 · **Duración orientativa:** 54 s

### Discurso

Café Jacaranda es el ejemplo que usaría para explicar una cuenta sin quedarme en cifras generales. En el baseline tiene cero puntos y aparece en el lugar diez. Con el grafo suma diez puntos y queda en el tercero. Los diez puntos vienen de dos vecinos confirmados utilizables: Hornos del Centro y Enlace Punto POS. En la captura real las líneas gruesas señalan ese respaldo. Las otras conexiones se conservan como contexto, pero no todas suman puntos. Si quiero revisar el origen puedo llegar a las observaciones OBS-026 y OBS-063, ambas del CRM sintético. No estoy infiriendo que Jacaranda quiera contratar ni que esos vecinos le hayan recomendado el servicio. Estoy mostrando cómo una regla explícita usa evidencia disponible para cambiar su posición de investigación.

### Qué señalar

Amplía la captura; señala líneas gruesas y las dos observaciones que sí puntúan.

### Pregunta del evaluador

¿Todas las líneas del dibujo dan puntos?

**Respuesta sencilla:** No. Solo los vecinos económicos confirmados utilizables. Las demás líneas dan contexto.

**Si profundiza:** La red es una vista del resultado, no el motor del score. network_data resalta relationship_ids ya elegidos por _neighbor_feature. El acomodo circular no tiene significado comercial.

**Verificar en:** src/economic_graph/tower_read_model.py:118–146; src/economic_graph/rankings.py:97–129; tests/test_control_tower.py:95–119

**Reproducción:** `uv run --group ui pytest tests/test_control_tower.py -k company_selector -q`

**Límite:** El dibujo no demuestra centralidad comercial, intención de compra ni causalidad.

## 08. Así llega la información a la pantalla

**Tipo:** Demostrado · implementación · **Duración orientativa:** 54 s

### Discurso

Esta es la organización que encontré en el código. La aplicación lee observations.json y valida su contrato con load_observations. Después build_context prepara lo que mostrarán las vistas. Dentro de esa función hay dos llamadas separadas: snapshot reconstruye lo que se sabe y compare_rankings calcula las dos políticas. A su vez, compare_rankings llama a snapshot para reconstruir su propia vista. Por eso no lo dibujo como si el resultado de snapshot se pasara directamente al ranking. Build_context también calcula resúmenes y evolución histórica. Al final, la interfaz aplica filtros para inspeccionar resultados. El cálculo financiero entra por otra ruta, desde su archivo de supuestos. Esa separación explica por qué cambiar una empresa en pantalla no debería modificar un escenario económico agregado ni las posiciones generales del ranking.

### Qué señalar

Recorre las dos ramas de build_context y la fuente financiera separada.

### Pregunta del evaluador

¿build_context pasa su snapshot a compare_rankings?

**Respuesta sencilla:** No. Les pasa las mismas observaciones y el corte. Cada función construye su vista por su propio camino.

**Si profundiza:** En T2 hay cinco llamadas a snapshot durante build_context: una directa, una interna en compare_rankings y tres para evolution. No se midió su rendimiento a escala.

**Verificar en:** app/control_tower.py:706–841; src/economic_graph/tower_read_model.py:41–66; src/economic_graph/rankings.py:145–233; src/economic_graph/finance.py:337–405

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** La separación de módulos no acredita una arquitectura de producción ni aislamiento por roles.

## 09. Filtrar no cambia el lugar global

**Tipo:** Demostrado · reconstrucción interactiva · **Duración orientativa:** 54 s

### Discurso

Esta función prepara primero el ranking general. Después puedo filtrar por industria o por empresa sin volver a calcular sus posiciones. Si Café Jacaranda estaba en el tercer lugar general, debe seguir mostrando tres aunque sea la única fila visible. En esta demostración puedo cambiar entre todas las cuentas, restaurantes y cafeterías, o solo Jacaranda. Los datos vienen de la ejecución del repositorio; este pequeño control es una reconstrucción para explicar el resultado, no una captura de Streamlit. También guardé capturas de la aplicación original con esos filtros. La razón de conservar el lugar es poder comparar sin cambiar silenciosamente la pregunta. Un filtro para inspeccionar no es una nueva competencia entre las cuentas visibles. Tampoco lleno los cinco lugares con otras empresas del sector.

### Qué señalar

Activa los tres filtros y observa que #10 y #3 permanecen iguales.

### Pregunta del evaluador

¿Por qué no aparece como lugar uno cuando solo queda una empresa?

**Respuesta sencilla:** Porque muestro su posición en el ranking completo. La selección de pantalla solo decide qué filas ver.

**Si profundiza:** segment_ids devuelve IDs del contexto; ranking_table copia baseline_position, graph_position y banderas selected ya calculadas. Las pruebas comparan las filas filtradas con el subconjunto original.

**Verificar en:** src/economic_graph/tower_read_model.py:41–66; src/economic_graph/tower_read_model.py:69–75; src/economic_graph/tower_read_model.py:78–96; tests/test_control_tower.py:122–136; tests/test_tower_read_model.py:123–136

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** La interacción de esta diapositiva usa resultados congelados; la captura y el script permiten verificar la aplicación original.

## 10. Cinco vistas para revisar la misma evidencia

**Tipo:** Demostrado · navegador offline · **Duración orientativa:** 52 s

### Discurso

La Control Tower permite revisar el proyecto sin depender de una explicación del código en cada momento. Resumen muestra la selección; Graph Health permite revisar fuentes, conflictos y conexiones; AI Performance compara las reglas; Business Funnel separa conocidas, elegibles y priorizadas; Economic Impact muestra escenarios hipotéticos. Durante esta misión, Codex abrió la aplicación real en Chromium, recorrió las cinco vistas y cambió períodos, industria, empresa, política y escala económica. Las imágenes son capturas de esa ejecución offline. Puedo ampliarlas para revisar el estado y consultar sus parámetros. No necesito una conexión a Atlas para mostrar esta evidencia. Sin embargo, que las pantallas funcionen con estos datos no significa que la aplicación esté lista para producción o que ya hayamos validado ventas.

### Qué señalar

Cambia entre las cinco capturas; amplía una y muestra sus parámetros.

### Pregunta del evaluador

¿Son diseños de ejemplo o capturas reales?

**Respuesta sencilla:** Son capturas de Streamlit ejecutado en modo offline. Cada archivo registra fecha, commit y filtros.

**Si profundiza:** La automatización usa Playwright y Chromium del sistema. Conserva estados, texto visible, capturas originales y metadatos; no cambia la UI ni sus fuentes.

**Verificar en:** app/control_tower.py:706–841; app/control_tower.py:316–462; app/control_tower.py:465–538; app/control_tower.py:596–703

**Reproducción:** `python presentation-showcase/scripts/capture_tower.py`

**Límite:** La revisión se hizo en Linux; no sustituye una revisión nativa en Windows ni una prueba de carga.

## 11. Cada prueba responde algo distinto

**Tipo:** Demostrado · ejecución de Codex · **Duración orientativa:** 54 s

### Discurso

No todas las pruebas demuestran lo mismo. Las pruebas de funciones revisan reglas, fechas y cálculos. Los dobles de MongoDB guardan documentos en memoria para comprobar consultas, idempotencia y protecciones sin conectarse a Atlas. AppTest ejecuta Streamlit y permite cambiar controles y revisar tablas, pero no dibuja la página en un navegador real. Por eso la revisión también incluyó Chromium para observar las pantallas. La suite original pasó doscientas ochenta y cuatro pruebas y una integración remota quedó excluida. La medición de cobertura se limita al paquete economic_graph: no incluye toda la interfaz ni los scripts. Estos resultados los ejecutó Codex en esta misión. No los presento como pruebas realizadas personalmente por mí, ni como una conexión real a Atlas o una garantía de ausencia de errores.

### Qué señalar

Distingue funciones, dobles, AppTest, navegador e integración real.

### Pregunta del evaluador

¿Pasar las pruebas de MongoDB significa que Atlas funciona?

**Respuesta sencilla:** No. Los dobles prueban nuestra lógica. Atlas requiere una conexión y una lectura reales verificadas aparte.

**Si profundiza:** Cobertura con pytest-cov y ramas: 904/943 líneas y 362/396 ramas. El 94.55% combinado no debe confundirse con cobertura de líneas. Se excluyó integration porque su roundtrip carga datos.

**Verificar en:** tests/test_mongo_observable.py:20–55; tests/test_mongo_observable.py:58–67; tests/test_control_tower.py:43–51; src/economic_graph/tower_read_model.py:374–402

**Reproducción:** `uv run --group ui pytest -m 'not integration'`

**Límite:** Cobertura alta no mide calidad comercial, producción, seguridad integral ni corrección de todos los casos.

## 12. Un caso límite al comparar fechas

**Tipo:** Demostrado · caso aislado · **Duración orientativa:** 54 s

### Discurso

Quiero mostrar también una limitación concreta. En la auditoría, Codex construyó un caso aislado con dos observaciones opuestas que llegaron en el mismo instante. Una fecha terminaba en Z y la otra en más cero cero dos puntos cero cero. Ambas representan la misma hora. El ranking las interpreta como un conflicto, pero snapshot compara el texto de las fechas y puede mostrar solamente descartada. La causa está en esa comparación, no en MongoDB. La corrección experimental compara instantes ya convertidos, y las dos pruebas de regresión pasan. El motor original no fue modificado. Este problema no aparece en el ledger aprobado, cuyas fechas están normalizadas. Puedo explicar cómo se reproduce y cómo lo investigaría, pero el hallazgo y el cambio experimental fueron realizados por Codex.

### Qué señalar

Señala mismo instante, resultado distinto y comparación propuesta; reconoce el origen del trabajo.

### Pregunta del evaluador

¿Encontraste un error en los resultados presentados?

**Respuesta sencilla:** No en el ledger aprobado. Es un defecto reproducible con una entrada válida aislada que usa otra forma de escribir la misma hora.

**Si profundiza:** snapshot agrupa latest_states con igualdad de cadenas; _latest en rankings usa parse_time. La prueba introduce una observación DISCARDED simultánea y válida. El original falla dos veces y la copia modificada en memoria pasa dos veces.

**Verificar en:** src/economic_graph/observable.py:82–176; src/economic_graph/rankings.py:27–29; presentation-showcase/experiments/test_timezone_conflict.py:1–55

**Reproducción:** `uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q`

**Límite:** La corrección es experimental; no se integró al proyecto ni se atribuye como competencia personal ya demostrada.

## 13. Priorizar todavía no es vender

**Tipo:** Demostrado · sintético · **Duración orientativa:** 53 s

### Discurso

El embudo ayuda a ver exactamente dónde termina la evidencia. En T2 hay veintitrés empresas conocidas. Dos quedan fuera por servicio activo confirmado y veintiuna participan en el ranking. De ahí selecciono cinco para investigar. Las dos exclusiones son una rama aparte, no una etapa que se reste después de priorizar. Más adelante la pantalla dice no observado para contactos, oportunidades, activaciones y ventas. Es distinto de poner cero. No tengo eventos que permitan saber cuántos intentos hubo o cuántos contratos se activaron. Tampoco sumaría las dos listas de cinco como si fueran diez contactos, porque son políticas alternativas y comparten cuentas. Esta separación me permite presentar lo construido sin convertir una decisión de prioridad en un resultado comercial que todavía no existe.

### Qué señalar

Recorre 23 → 21 → 5 y detente antes de contactos.

### Pregunta del evaluador

¿Cuál fue tu tasa de conversión?

**Respuesta sencilla:** No puedo calcularla: no hay contactos y activaciones verificadas en este conjunto de datos.

**Si profundiza:** funnel devuelve None y Estado=No observado para etapas sin datos. Las pruebas exigen texto explícito y evitan reemplazar faltantes por ceros.

**Verificar en:** src/economic_graph/tower_read_model.py:99–115; tests/test_control_tower.py:139–143; app/control_tower.py:541–593

**Reproducción:** `uv run --group ui pytest tests/test_control_tower.py -k funnel -q`

**Límite:** Sin eventos comerciales no hay tasas observadas de conversión ni embudo comercial completo.

## 14. El saldo depende de lo que supongamos

**Tipo:** Hipótesis · cálculo reproducido · **Duración orientativa:** 52 s

### Discurso

El calculador responde qué tendría que pasar para cubrir los costos, no cuánto dinero gané. En el caso base de quinientas plazas supongo que la activación pasa de diez a doce por ciento: dos puntos porcentuales más. Con ocho mil pesos de margen por activación y los costos declarados, el saldo es más treinta y nueve mil pesos antes de reserva. Si mantengo los costos pero quito esa mejora, el escenario nulo pierde cuarenta y un mil. Con solo cinco plazas, incluso el caso base pierde quince mil cuatrocientos cincuenta. Puedo cambiar la escala para mostrarlo. Las cifras se reproducen con el código, pero los supuestos no están calibrados. Quinientas plazas tampoco significa quinientas empresas observadas ni una muestra experimental ya definida.

### Qué señalar

Alterna cinco y 500; compara base con nulo y señala que la reserva va aparte.

### Pregunta del evaluador

¿Los 39 mil pesos prueban ROI positivo?

**Respuesta sencilla:** No. Son el resultado de supuestos de activación, margen y costos que todavía no medimos.

**Si profundiza:** ΔV = plazas×Δp×margen − plazas×Δc + ΔU − F − ΔO. Base 500: 80,000−25,000−10,000−6,000=39,000. Nulo: −25,000−10,000−6,000=−41,000. Reserva 3,200 separada; base tras reserva=35,800.

**Verificar en:** src/economic_graph/finance.py:186–227; src/economic_graph/finance.py:337–405; config/financial_assumptions.json:1–194; tests/test_finance.py:113–127

**Reproducción:** `uv run python scripts/calculate_finance.py --sensitivity --format markdown`

**Límite:** No interpretar tasas supuestas, sensibilidad o equilibrio como efectos alcanzados ni intervalos de confianza.

## 15. Cómo comprobaríamos si genera valor

**Tipo:** Diseño · no ejecutado · **Duración orientativa:** 54 s

### Discurso

Para medir valor real necesitaría un experimento distinto del calculador. La propuesta agrupa cuentas y equipos en bolsas que reduzcan el intercambio de información entre grupos. Asignaría al azar bolsas completas: unas usan baseline y otras el ranking con grafo, con esfuerzo y capacidad comparables. Mediría margen neto por todas las cuentas elegibles asignadas, incluso las que nadie contactó. Eso evita evaluar solamente los éxitos. El seguimiento propuesto considera noventa días para activar y doce meses desde la asignación para margen y costos. Todavía faltan datos autorizados, costos reales y suficientes bolsas independientes. Sin conocer la variación del margen y qué tan parecidas son las cuentas dentro de cada bolsa, no puedo dar un tamaño de muestra serio. Es un diseño futuro, no un experimento realizado.

### Qué señalar

Señala que se asignan bolsas antes de seleccionar, y el denominador incluye todas las cuentas.

### Pregunta del evaluador

¿Por qué no comparas directamente los dos Top 5?

**Respuesta sencilla:** Porque no fueron asignados al azar, comparten cuentas y tienen señales distintas. Eso no separa el efecto de usar el grafo.

**Si profundiza:** ITT conserva la asignación original. Inferencia por bolsa y bloques; objetivo IC bilateral 95% y potencia 80%, sin muestra calculada. Registrar contaminación, faltantes y costos sin duplicar plataforma en el KPI y en inversión.

**Verificar en:** docs/15-incrementality-experiment.md:1–88; docs/14-incremental-economic-case.md:1–178; src/economic_graph/finance.py:337–405

**Reproducción:** `Lectura: docs/15-incrementality-experiment.md; no existe un ensayo ejecutado.`

**Límite:** Si no hay suficientes bolsas independientes, este diseño no permite atribuir causalidad.

## 16. El ranking cambia. El valor falta medirlo.

**Tipo:** Conclusión con límites · **Duración orientativa:** 55 s

### Discurso

Lo que puedo defender es un prototipo que conserva fuentes y fechas, mantiene visibles las dudas y compara dos formas de priorizar. Las relaciones confirmadas cambian tres de cinco lugares, y puedo seguir el caso de Café Jacaranda hasta sus observaciones. La Control Tower permite revisar esos resultados, y hay pruebas y capturas nuevas de la ejecución offline. Al mismo tiempo, no puedo afirmar que mejoró la conversión, que hubo ventas adicionales o que se recuperó una inversión. La lectura real de Atlas quedó pendiente en esta misión, y tampoco medimos escala o preparación para producción. Mi siguiente paso sería comprender y practicar esta defensa, revisar los casos del anexo y después conseguir los datos y permisos para una evaluación real. Prefiero reconocer esos límites y explicar cómo comprobarlos.

### Qué señalar

Cierra con lo demostrado, lo pendiente y el siguiente paso; abre anexo si preguntan.

### Pregunta del evaluador

¿Qué harías después?

**Respuesta sencilla:** Primero practicaría la reproducción del código y la depuración. Para negocio validaría datos, permisos, costos y viabilidad de un piloto controlado.

**Si profundiza:** Los seis entregables están mapeados en el anexo y la matriz. La auditoría nueva es trabajo de Codex; no sustituye que el candidato explique y modifique el código por sí mismo.

**Verificar en:** docs/02-challenge-traceability.md:1–226; src/economic_graph/rankings.py:145–233; docs/15-incrementality-experiment.md:1–88

**Reproducción:** `Consultar evidence/results y docs/auditoria.md de esta entrega.`

**Límite:** No presentar este MVP como sistema productivo o caso de éxito comercial.

## 17. build_context(): las llamadas reales

**Tipo:** Demostrado · código · **Duración orientativa:** 51 s

### Discurso

Si me preguntan por build_context, lo explicaría como una preparación de datos para las pantallas. Recibe observaciones y un corte. Llama directamente a snapshot y, por separado, a compare_rankings. Esta última vuelve a llamar a snapshot dentro de su implementación. Además, build_context reconstruye un resumen por cada corte pasado para la evolución. En T2 eso da cinco llamadas a snapshot: dos para la vista y el ranking y tres para la historia. No existe una cadena donde el primer snapshot sea la entrada del ranking. Esta repetición es aceptable para explicar el prototipo pequeño, pero no tengo una medición para decir qué tan bien escala. Antes de optimizar, mediría tiempos y comprobaría que los resultados siguen siendo iguales.

### Qué señalar

Señala las líneas 43, 44 y 51 y la llamada interna del ranking.

### Pregunta del evaluador

¿Puedes dibujar la relación exacta sin leer un README?

**Respuesta sencilla:** Sí: build_context tiene ramas separadas para snapshot, compare_rankings y evolución; compare_rankings hace su propio snapshot.

**Si profundiza:** summary=summarize(view), sources y states derivan de view; coverage deriva de ranking.companies. Ningún filtro de industria entra a build_context.

**Verificar en:** src/economic_graph/tower_read_model.py:41–66; src/economic_graph/rankings.py:145–233; src/economic_graph/observable.py:82–176

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** No se midió latencia ni costo de estas reconstrucciones con miles de empresas.

## 18. Datos, conflictos e identidades

**Tipo:** Demostrado · código · **Duración orientativa:** 52 s

### Discurso

El archivo observable es la frontera de entrada de la aplicación. Su contrato revisa campos, tipos, identificadores y que las fechas tengan zona y un orden válido. También comprueba que una relación no mencione una empresa que todavía no era identificable cuando se conoció el dato. El diseño privado sirve para construir y auditar la simulación; no se consulta para completar atributos o puntuar. Los IDs públicos se generan desde observaciones, sin revelar los nombres internos del diseño. Para conflictos de atributos se conservan los valores distintos. Para alias se normaliza el nombre y solo se sugieren candidatos. Esto ayuda a explicar la incertidumbre, pero no reemplaza un proceso real de verificación de identidad, con fuentes autorizadas y revisión de casos ambiguos.

### Qué señalar

Distingue el diseño restringido de observations.json y explica UNKNOWN frente a CONFLICTED.

### Pregunta del evaluador

¿Cómo evitas completar una empresa con información privilegiada?

**Respuesta sencilla:** La ruta comercial lee solo observaciones y sus módulos no importan el simulador para enriquecerlas.

**Si profundiza:** assert_no_private_fields rechaza metadatos de verdad. La prueba public_only_ui ejecuta una copia sin simulator ni design-data y bloquea red y credenciales.

**Verificar en:** src/economic_graph/contracts.py:74–154; src/economic_graph/observable.py:61–70; src/economic_graph/observable.py:73–79; src/economic_graph/simulator/project.py:27–97

**Reproducción:** `uv run pytest tests/test_observable.py -q`

**Límite:** La revisión no es una auditoría integral de privacidad ni una prueba de identidad empresarial fuerte.

## 19. Elegibilidad, topes y empates

**Tipo:** Demostrado · política 003a · **Duración orientativa:** 52 s

### Discurso

La elegibilidad de esta PoC es conservadora en lo que afirma, aunque todavía es mínima para una operación real. Solo excluye una cuenta si tiene servicio activo confirmado y sin conflicto. Que el servicio sea desconocido no prueba que no sea cliente: queda pendiente de validación comercial. Después se calculan ambas reglas para todas las elegibles. Los puntos se ordenan de mayor a menor y, si empatan, gana el identificador público menor. Esa decisión es reproducible, pero no agrega evidencia comercial. Por eso el reporte muestra si el empate cruza la quinta plaza. También se limitan las contribuciones y se deduplican vecinos. Con pocos atributos observados, varios lugares pueden depender del desempate; es una limitación que debo mencionar al interpretar la lista.

### Qué señalar

Muestra cobertura 3/21 individual y 5/21 relacional; explica por qué cero puntos puede significar falta de evidencia.

### Pregunta del evaluador

¿Por qué es elegible una empresa cuyo servicio no conoces?

**Respuesta sencilla:** Es la regla de demostración aprobada. Para un piloto necesitaría comprobar que no es cliente y otras condiciones antes de contactar.

**Si profundiza:** La última evidencia debe ser CONFIRMED y el valor True, con atributo OBSERVED. _relationship_context bloquea oposición confirmada/descartada y conflictos antes de contar vecinos.

**Verificar en:** src/economic_graph/rankings.py:145–233; src/economic_graph/rankings.py:32–39; src/economic_graph/rankings.py:59–94; src/economic_graph/rankings.py:132–142

**Reproducción:** `uv run pytest tests/test_rankings.py -q`

**Límite:** ID ascendente es un desempate técnico; no es señal de valor ni regla comercial calibrada.

## 20. MongoDB en memoria no es Atlas

**Tipo:** Demostrado · pruebas offline · **Duración orientativa:** 51 s

### Discurso

MemoryCollection y MemoryDatabase son objetos de Python que imitan solo las operaciones que necesita el código. Guardan documentos en diccionarios, registran consultas y usan copias para evitar cambios accidentales. La primera carga inserta ochenta y tres observaciones; la segunda no agrega ninguna. Eso prueba idempotencia: repetir la misma operación no duplica los datos. También hay pruebas que rechazan otra base, colecciones sin propiedad compatible y cambios en documentos existentes antes de escribir. En esta misión esas escrituras ocurrieron únicamente en memoria, no en Atlas. El doble ayuda a probar rápido y sin credenciales, pero no reproduce todos los tipos BSON, índices, permisos, concurrencia o comportamiento del servidor. Para afirmar integración necesito otra comprobación contra una instancia real autorizada.

### Qué señalar

Señala 83 insertadas en memoria → 0 nuevas y el diccionario de consultas.

### Pregunta del evaluador

¿Qué no reproduce MemoryCollection?

**Respuesta sencilla:** No es un servidor completo: no prueba red, autenticación, rendimiento, concurrencia real ni todos los detalles de MongoDB.

**Si profundiza:** update_one exige únicamente $setOnInsert con upsert; find aplica available_at y subject_id. Los tests verifican protección previa a escrituras e historial temporal.

**Verificar en:** tests/test_mongo_observable.py:20–55; tests/test_mongo_observable.py:58–67; tests/test_mongo_observable.py:70–91; src/economic_graph/mongo_observable.py:39–75

**Reproducción:** `uv run pytest tests/test_mongo_observable.py -q`

**Límite:** Una carga idempotente con dobles no acredita una carga real exitosa en Atlas.

## 21. AppTest comprueba lógica; Chromium, la pantalla

**Tipo:** Demostrado · Linux · **Duración orientativa:** 52 s

### Discurso

AppTest carga el script de Streamlit y permite mover controles como si fuera una prueba de la aplicación. Puedo seleccionar un período, revisar opciones y comprobar que Café Jacaranda conserva sus posiciones. También comprueba que una lectura fallida no reutilice cifras anteriores y que las etapas sin eventos sigan diciendo no observado. En las pruebas offline, el cliente MongoDB y la carga de configuración están bloqueados. Eso es útil para demostrar que esa ruta no necesita credenciales. Lo que AppTest no muestra es el dibujo final del navegador: no puedo usarlo para asegurar que una tabla cabe o que un texto se lee bien. Para eso se capturaron las cinco vistas con Chromium. Las dos verificaciones responden preguntas diferentes y se complementan.

### Qué señalar

Contrasta una aserción de la prueba con una captura auténtica.

### Pregunta del evaluador

¿AppTest equivale a una prueba visual de extremo a extremo?

**Respuesta sencilla:** No. Ejecuta Streamlit y revisa sus elementos. Chromium permite comprobar cómo aparecen y se usan en la pantalla.

**Si profundiza:** La preparación importa dependencias nativas antes del timeout funcional de 15 s. Un guard bloquea red externa y permite IPC local necesario. La simulación de codificación Windows no sustituye ejecución nativa.

**Verificar en:** tests/test_control_tower.py:43–51; tests/test_control_tower.py:122–136; tests/test_control_tower.py:191–204; tests/ui_test_support.py:11–18

**Reproducción:** `uv run --group ui pytest tests/test_control_tower.py -q`

**Límite:** Las capturas no prueban todas las combinaciones, dispositivos, accesibilidad o ejecución Windows.

## 22. La lectura real de Atlas queda pendiente

**Tipo:** Pendiente · sin conexión intentada · **Duración orientativa:** 57 s

### Discurso

La ruta de Atlas existe y puedo explicar su código, pero no la presento como verificada en esta misión. Primero construye una referencia local, valida que la base sea la dedicada, lee observaciones disponibles al corte y vuelve a preparar el contexto. Después compara la huella de la entrada visible con la local. Si son distintas, bloquea la demostración comparable; no reemplaza datos remotos ni inventa cifras de respaldo. Esa función no hace ping. El proyecto tiene otra función para comprobar conexión y una prueba de integración que sí hace carga, por eso quedó excluida. La configuración y la red disponibles no bastaban para esa lectura, y se acordó trabajar offline. No cambié credenciales ni configuraciones para intentar resolverlo. Los reportes históricos de Atlas permanecen como antecedentes, no como una ejecución nueva.

### Qué señalar

Señala base dedicada, filtro temporal y comparación de SHA-256; diferencia ping de lectura.

### Pregunta del evaluador

¿Qué necesitarías para afirmar que Atlas funciona?

**Respuesta sencilla:** Una comprobación de conexión y una lectura real autorizada, con base y permisos correctos, sin confundirlas con dobles.

**Si profundiza:** read_observations envía available_at <= parse_time(as_of) al servidor y convierte BSON UTC sin zona. atlas_context comprueba visible_input_sha256; maneja errores sin exponer URI y no hace fallback silencioso.

**Verificar en:** src/economic_graph/tower_read_model.py:374–402; src/economic_graph/mongo_observable.py:78–89; src/economic_graph/database.py:29–52; tests/integration/test_atlas_observable.py:1–33

**Reproducción:** `No ejecutar la integración que escribe; revisión de código y dobles únicamente.`

**Límite:** Una lectura exitosa no valida escrituras, rendimiento, seguridad completa ni todo el historial de Atlas.

## 23. De dónde salen +$39,000 y −$41,000

**Tipo:** Hipótesis · aritmética probada · **Duración orientativa:** 54 s

### Discurso

Puedo reconstruir el caso base sin depender de una cifra puesta en la diapositiva. Multiplico quinientas plazas por dos puntos porcentuales de mejora y ocho mil pesos de margen: son ochenta mil pesos de margen incremental supuesto. Resto veinticinco mil de costo comercial adicional, diez mil fijos y seis mil de operación. El saldo es treinta y nueve mil antes de reserva. El caso nulo conserva esos costos, pero pone la mejora en cero: pierde cuarenta y un mil. La reserva de tres mil doscientos se muestra aparte; al restarla, el caso base queda en treinta y cinco mil ochocientos. El código usa Decimal y revisa unidades y valoración temporal para evitar dobles descuentos. Toda esta precisión comprueba aritmética, no que los supuestos sean reales.

### Qué señalar

Recorre cada renglón de la cuenta y distingue saldo antes y después de reserva.

### Pregunta del evaluador

¿Ya descontaste dos veces el margen o los costos?

**Respuesta sencilla:** Los importes del ejemplo ya son valor presente. El código valida horizonte y descuento y separa prospección, margen neto y reserva.

**Si profundiza:** 90 días para activación; horizonte 12 meses, tasa mensual 1%. Base y nulo usan margen 8,000, Δc=50, ΔU=0, F=10,000 y ΔO=6,000. Umbral sin reserva: 41,000/(500×8,000)=1.025 pp; con reserva 1.105 pp.

**Verificar en:** src/economic_graph/finance.py:186–227; src/economic_graph/finance.py:174–183; config/financial_assumptions.json:1–194; tests/test_finance.py:45–55

**Reproducción:** `uv run python scripts/calculate_finance.py --format markdown`

**Límite:** Los costos fijos constantes al cambiar escala sirven para explorar; no son cotizaciones reales a volumen.

## 24. Medir a todas las cuentas asignadas

**Tipo:** Diseño · no ejecutado · **Duración orientativa:** 52 s

### Discurso

La parte que más cuidaría del experimento es qué cuentas entran a la evaluación. No mediría únicamente a las contactadas o a las que siguieron la recomendación. Mantendría todas las elegibles originalmente asignadas; eso es intención de tratar. Si una cuenta compra por otro canal también cuenta, porque busco el efecto de la política completa. Si no puedo verificar su resultado, es faltante, no una venta cero. La asignación ocurre por bolsas para reducir que las relaciones o los vendedores mezclen los grupos. El análisis debe respetar esa unidad y los tamaños de las bolsas. Se propone un intervalo de confianza del noventa y cinco por ciento, pero todavía no existe la información necesaria para calcular muestra, precisión o un efecto real.

### Qué señalar

Señala todo el denominador y la contaminación entre bolsas.

### Pregunta del evaluador

¿Por qué no calculaste el tamaño de muestra con 500 plazas?

**Respuesta sencilla:** Porque las plazas del calculador no son unidades independientes. Faltan variación del margen, correlación dentro de bolsas y su número y tamaño.

**Si profundiza:** El protocolo propone estimador de totales ponderados por probabilidad de asignación, expresado por cuenta elegible; inferencia por aleatorización o clusters preespecificada. Plataforma se evalúa después, sin restarla dos veces.

**Verificar en:** docs/15-incrementality-experiment.md:1–88; docs/14-incremental-economic-case.md:1–178

**Reproducción:** `Lectura del protocolo; no hay resultados experimentales que reproducir.`

**Límite:** No significancia no prueba equivalencia; un intervalo válido tampoco elimina contaminación o faltantes.

## 25. Un cambio pequeño, con una comprobación clara

**Tipo:** Experimental · realizado por Codex · **Duración orientativa:** 52 s

### Discurso

Para estudiar el código puedo repetir este ejercicio en una copia. Primero leo el contrato y la función que agrupa los estados. Después creo dos observaciones opuestas válidas con el mismo instante y distinta representación de zona horaria. La prueba exige que la vista y el ranking coincidan en conflicto. En el original falla; en la copia experimental pasa al comparar fechas convertidas. También puedo revisar que los archivos originales conservan sus huellas. Esta es una demostración práctica preparada por Codex. Yo no debería decir que descubrí o resolví personalmente ese error hasta poder repetirlo y explicarlo por mi cuenta. Lo usaría como una práctica guiada: anticipar qué pasará, ejecutar, leer la diferencia y justificar por qué el cambio corrige ese caso.

### Qué señalar

Abre el archivo experimental y los dos registros de pruebas.

### Pregunta del evaluador

¿Tú hiciste esta corrección?

**Respuesta sencilla:** La preparó Codex durante la auditoría. Puedo estudiar y reproducirla, pero no la atribuyo como experiencia personal ya demostrada.

**Si profundiza:** El test usa compile/exec en un ModuleType independiente y sustituye una comparación en la cadena fuente. No altera sys.modules del motor comercial ni escribe en src. Dos variantes: +00:00 y +0000.

**Verificar en:** src/economic_graph/observable.py:82–176; presentation-showcase/experiments/test_timezone_conflict.py:1–55

**Reproducción:** `SHOWCASE_SNAPSHOT_VARIANT=original uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q`

**Límite:** La práctica aislada no sustituye revisión de una corrección productiva y pruebas más amplias.

## 26. Qué necesitaría para dar el siguiente paso

**Tipo:** Diseño · pendiente · **Duración orientativa:** 53 s

### Discurso

Separaría el siguiente paso en necesidades concretas. Para datos, hacen falta fuentes autorizadas, identidad suficiente, permisos y eventos comerciales confiables. Para evaluación, necesito un baseline real, costos y márgenes medidos, y un experimento viable. Para ingeniería, mediría tiempos y memoria con datos de prueba aislados antes de prometer miles de empresas. Solo después consideraría un modelo aprendido, con etiquetas reales, separación temporal y comparación contra estas reglas. MongoDB es una opción de persistencia útil para este prototipo, pero no la única; SQL también podría guardar un historial de observaciones. No necesito agregar agentes o tecnología por sí misma. Como candidato junior, mi responsabilidad sería explicar lo que existe, medir lo que falta y pedir revisión cuando la decisión requiera experiencia que todavía estoy desarrollando.

### Qué señalar

Conecta cada propuesta con una evidencia faltante, sin prometer una escala.

### Pregunta del evaluador

¿Por qué MongoDB y no SQL?

**Respuesta sencilla:** Es una elección válida para este prototipo de documentos e historial. No he demostrado que sea superior; SQL también podría resolverlo.

**Si profundiza:** Una comparación exigiría cargas equivalentes, índices, costos, latencias y controles. Graph features y modelos supervisados necesitan etiquetas y evaluación temporal; no hay MLOps implementado.

**Verificar en:** docs/04-architecture-overview.md:1–123; docs/15-incrementality-experiment.md:1–88; docs/12-commercial-ranking.md:1–115

**Reproducción:** `Sin benchmark ejecutado; propuesta de validación futura.`

**Límite:** La hoja de ruta es propuesta, no capacidad actual ni experiencia personal acreditada.

## 27. Dónde comprobar cada parte del reto

**Tipo:** Trazabilidad de la entrega · **Duración orientativa:** 54 s

### Discurso

Este mapa me ayuda a responder preguntas sin saturar la exposición principal. El problema y la capacidad cubren Business Framing. Las observaciones y los cortes cubren Economic Graph. Las dos reglas y sus límites explican AI/ML Approach. Las funciones y sus dependencias cubren Architecture. El calculador y el protocolo futuro cubren Economic Case. Las cinco vistas corresponden a Control Tower. Cada afirmación importante tiene una referencia de código o documento, un comando cuando se puede reproducir, y una limitación. También puedo consultar el guion, las preguntas de defensa y el informe de auditoría. Las fuentes originales se conservan como referencia y las cifras nuevas se sostienen en la ejecución. Si me preguntan algo que no medimos, mi respuesta debe decirlo y proponer cómo lo comprobaría.

### Qué señalar

Abre la matriz y muestra una fila con fuente, commit, comando y captura.

### Pregunta del evaluador

¿Cómo sé que una afirmación de la presentación corresponde a este código?

**Respuesta sencilla:** La matriz enlaza la afirmación con archivo, líneas, commit, resultado o captura y sus límites.

**Si profundiza:** Se preservan huellas SHA-256 del ledger, supuestos y fuentes auditadas; los anexos incluyen resultados de pruebas y metadatos de capturas. Las referencias históricas no sustituyen evidencia nueva.

**Verificar en:** docs/02-challenge-traceability.md:1–226; presentation-showcase/docs/auditoria.md:1–184

**Reproducción:** `Consultar docs/trazabilidad.csv y evidence/source/manifest.json.`

**Límite:** Una referencia facilita auditar; no convierte una hipótesis en un resultado observado.
