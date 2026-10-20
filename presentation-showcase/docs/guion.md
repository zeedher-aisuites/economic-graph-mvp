# Guion de exposición y defensa técnica

Versión anterior · ConectaPyME: caso de negocio B2B con evidencias opcionales. Implementación de respaldo: `774dacd80e6410ca43299f63f19d9744a31929c0`. Capturas offline y datos sintéticos de la primera revisión, conservados.

El relato de alcance, hipótesis y decisiones corresponde a la declaración del candidato. La programación fue asistida por ChatGPT/GPT, Gemini y Codex según esa declaración. Las pruebas, capturas y el experimento de depuración de V1 fueron producidos por Codex y conservan su origen; no acreditan ejecución manual personal. Duraciones a 140 palabras por minuto; ensayar en voz alta.

## 01. ConectaPyME: caso de negocio B2B

**Tipo:** El reto · mi punto de partida · **Duración orientativa:** 59 s

### Discurso

Cuando recibí el reto, entendí que no se trataba solamente de dibujar conexiones o elegir una base de datos. La pregunta era cómo construir un Economic Graph de pequeñas empresas para una Telco y cómo demostrar que genera valor económico incremental. Para mí, eso significa conectar información con una decisión comercial y después medir si esa decisión deja un beneficio adicional frente a una referencia. ConectaPyME es mi respuesta a esa pregunta. El grafo representa empresas y sus relaciones económicas. Preparé una prueba de concepto pequeña, con datos sintéticos, para explorar una parte del problema. En esta presentación voy a explicar cómo elegí el alcance, cómo trabajé con asistencia de IA, qué hace el prototipo y qué resultados puedo defender. También voy a separar lo que funciona técnicamente de lo que todavía necesitaría medir con datos reales.

### Qué señalar

Señala la pregunta completa y la cadena información → decisión → valor medible.

### Pregunta del evaluador

¿Qué decisión de negocio intenta mejorar ConectaPyME?

**Respuesta sencilla:** Conectar datos y relaciones con una decisión comercial y explicar cómo mediría un beneficio económico adicional. La arquitectura es parte del soporte.

**Si profundiza:** Las diapositivas 4 y 5 del reto fijan la pregunta y su intención; 10 y 12 establecen Control Tower y seis entregables.

**Verificar en:** presentation-showcase/docs/reto-original.md:1–190; presentation-showcase/docs/origen-y-alcance.md:1–59

**Reproducción:** `Consultar el contexto técnico, diapositivas 4, 5, 10 y 12; extracción completa en docs/reto-original.md.`

**Límite:** El prototipo no acredita ventas, ROI ni un efecto económico real; las cifras ilustrativas del reto no son resultados de ConectaPyME.

## 02. Primero definí qué decisión quería mejorar

**Tipo:** Mi elección · caso ficticio · **Duración orientativa:** 56 s

### Discurso

Antes de elegir tecnologías, me hice varias preguntas. ¿Qué empresa usaría el grafo? ¿Qué decisión necesitaba mejorar? ¿Qué información tendría disponible? ¿Y cómo sabría si las conexiones servían para algo? El reto ofrecía varias posibilidades y elegí adquisición de clientes empresariales: investigar pequeñas empresas similares o conectadas con clientes actuales. Para aterrizarlo definí una Telco ficticia, ConectaPyME, y una decisión concreta: a quién investigar primero cuando hay más cuentas que tiempo. En la demostración uso cinco lugares. Eso me permite comparar dos listas sin cambiar la capacidad comercial. La empresa, su territorio y su contexto operativo son una simulación. No estoy describiendo ni diagnosticando los procesos reales de una empresa. Tampoco significa que las seleccionadas ya estén listas para recibir una llamada; todavía faltaría validar cobertura, identidad y permiso de contacto.

### Qué señalar

Muestra el caso B2B Acquisition del reto y la decisión acotada de cinco lugares.

### Pregunta del evaluador

¿Estás afirmando que este problema existe en una empresa real?

**Respuesta sencilla:** No. Elegí una posibilidad del reto y la desarrollé en una Telco ficticia. Tendría que validar el problema y el proceso real con la empresa.

**Si profundiza:** La intención de adquisición está en la diapositiva 7 del reto. K=5 pertenece a la política de la PoC, no a una capacidad comercial medida.

**Verificar en:** presentation-showcase/docs/reto-original.md:1–190; presentation-showcase/docs/origen-y-alcance.md:1–59; src/economic_graph/rankings.py:12–22

**Reproducción:** `uv run python scripts/rank_companies.py --as-of T2`

**Límite:** El caso de uso elegido no implica que ya se haya implementado similitud aprendida o una política especial para vecinos de clientes actuales.

## 03. Mi hipótesis: las relaciones podrían ayudar

**Tipo:** Hipótesis · todavía por validar · **Duración orientativa:** 56 s

### Discurso

Mi hipótesis fue que una empresa puede ser más interesante para investigar cuando entiendo cómo se relaciona con otros negocios, y no solamente sus atributos individuales. Por ejemplo, conocer un vínculo económico confirmado podría agregar contexto a una cuenta con poca información propia. Eso podría ayudar a seleccionar prospectos más útiles y, bajo ciertas condiciones, mejorar la adquisición y el margen. Pero no lo doy por hecho. Primero necesitaría datos confiables y autorizados, relaciones relevantes y bien verificadas, una comparación justa contra una referencia, un equipo que pueda actuar y resultados reales para medir. Por eso dividí la pregunta en dos partes. Con la PoC puedo comprobar si el grafo cambia la selección y explicar por qué. Para saber si ese cambio ayuda a vender mejor necesitaría una evaluación comercial posterior.

### Qué señalar

Sigue la cadena de hipótesis y las cinco condiciones; separa cambio de lista de mejora comercial.

### Pregunta del evaluador

¿Qué parte de tu hipótesis comprobaste?

**Respuesta sencilla:** Que las relaciones confirmadas cambian la selección bajo las reglas del prototipo. Que esa selección genere mayor margen sigue pendiente.

**Si profundiza:** El ranking compara atributos individuales frente a los mismos atributos más vecinos económicos confirmados; no estima probabilidades ni un efecto causal.

**Verificar en:** presentation-showcase/docs/reto-original.md:1–190; presentation-showcase/docs/origen-y-alcance.md:1–59

**Reproducción:** `Consultar docs/reto-original.md y docs/origen-y-alcance.md.`

**Límite:** Una señal relevante para describir una relación no necesariamente predice una compra.

## 04. Dirigí una PoC con apoyo de IA

**Tipo:** Mi forma de trabajo · asistencia de IA · **Duración orientativa:** 56 s

### Discurso

Con el plazo del reto y sin datos reales de una Telco, decidí construir una prueba de concepto controlada. Utilicé ChatGPT o GPT, Gemini y Codex para avanzar más rápido en investigación, programación y documentación. Mi participación fue plantear el alcance y las hipótesis, revisar propuestas y avances, decidir qué tenía sentido y solicitar o autorizar cambios. No quiero presentar todo el código como si lo hubiera escrito manualmente. También distingo dirigir el desarrollo, comprender el resultado y ejecutar personalmente una validación: son cosas diferentes. Las pruebas y capturas automatizadas tienen sus registros y su origen en la trazabilidad. Durante la exposición me apoyaré en esa evidencia sin atribuirme ejecuciones que no hice. Mi responsabilidad es poder explicar la solución, reconocer sus límites y practicar cómo reproducir sus partes importantes.

### Qué señalar

Señala tu papel, el apoyo de GPT/Gemini/Codex y la diferencia entre dirigir, comprender y validar.

### Pregunta del evaluador

¿Qué hiciste tú y qué hicieron las herramientas?

**Respuesta sencilla:** Yo definí el enfoque, revisé avances y tomé decisiones. Usé IA para apoyar investigación, implementación y documentación. Los registros identifican las comprobaciones automatizadas; no las presento como ejecuciones manuales mías.

**Si profundiza:** El uso de las tres herramientas y el papel de dirección corresponden a la declaración del candidato. No hay base para atribuir un porcentaje de código o una tarea específica a cada herramienta. Las evidencias nuevas de V1 fueron producidas por Codex.

**Verificar en:** presentation-showcase/docs/reto-original.md:1–190; presentation-showcase/docs/origen-y-alcance.md:1–59

**Reproducción:** `Consultar docs/reto-original.md y docs/origen-y-alcance.md.`

**Límite:** El apoyo de IA no acredita por sí solo que yo domine cada archivo o haya ejecutado todas las validaciones.

## 05. Construí un laboratorio de 30 PyMEs

**Tipo:** Demostrado · sintético · **Duración orientativa:** 54 s

### Discurso

Para poner a prueba la idea sin inventar datos de una Telco real, decidí trabajar con treinta empresas sintéticas, sus atributos y sus relaciones. Pero no quería que el sistema conociera todo desde el principio. Separé el universo completo del simulador de la información que estaría disponible para una decisión. En enero, T0, se conocen doce empresas; en mayo, T1, diecisiete; y en septiembre, T2, veintitrés. Las observaciones acumuladas son veintiocho, cincuenta y cuatro y ochenta y tres. Las otras siete empresas siguen fuera de la información observable al último corte. Esto me permite explorar una idea sencilla: una decisión histórica debe usar lo que se sabía en ese momento. No completo el ranking con información del universo privado solo porque el simulador conoce la respuesta.

### Qué señalar

Distingue las 30 del diseño de las 12/17/23 conocidas; señala las siete que siguen fuera.

### Pregunta del evaluador

¿Por qué no usas solamente la fecha del hecho?

**Respuesta sencilla:** Porque un hecho pudo ocurrir antes y conocerse después. Para evitar usar información futura, filtro por disponibilidad.

**Si profundiza:** visible_observations valida el contrato y aplica parse_time(available_at) <= parse_time(as_of), ordena y devuelve una copia. Los cortes son a las 12:00 UTC, equivalentes a las 06:00 de Ciudad de México.

**Verificar en:** src/economic_graph/contracts.py:5–9; src/economic_graph/observable.py:38–45; src/economic_graph/observable.py:82–176; tests/test_observable.py:23–49

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** Los tres cortes no son tres experimentos ni mediciones independientes de ventas.

## 06. Quise conservar las fuentes y las dudas

**Tipo:** Demostrado · sintético · **Duración orientativa:** 55 s

### Discurso

Al trabajar con información incompleta me pareció importante conservar de dónde viene cada dato y cuándo puedo usarlo. El prototipo guarda observaciones con fuente, fechas y estado de verificación. Utiliza available_at, que indica desde cuándo estuvo disponible el dato, para evitar usar información del futuro. También conserva dudas. En Hornos del Centro hay registros que dicen dos sucursales y otros que dicen tres. No quise elegir una versión solo porque era más reciente sin una regla válida para resolverlo. El código mantiene el conflicto y esa señal aporta cero puntos. Eso no significa que la empresa tenga cero sucursales. Con los nombres pasa algo parecido: una coincidencia produce un candidato de identidad, pero no fusiona negocios. Así puedo explicar qué sé, qué no sé y qué tendría que revisar.

### Qué señalar

Señala las observaciones OBS-028, OBS-047 y OBS-075 y su contribución cero por conflicto.

### Pregunta del evaluador

¿Por qué no gana automáticamente el dato más nuevo?

**Respuesta sencilla:** Porque no hay una regla aprobada para resolver ese conflicto. Prefiero conservar las opciones y revisarlas.

**Si profundiza:** _attribute marca CONFLICTED si hay valores distintos en el historial visible. Las relaciones conservan historia de estados; las candidaturas usan normalización de nombres, sin identificación fuerte.

**Verificar en:** src/economic_graph/contracts.py:22–36; src/economic_graph/observable.py:61–70; src/economic_graph/observable.py:82–176; tests/test_tower_read_model.py:105–120; src/economic_graph/observable.py:38–45

**Reproducción:** `uv run pytest tests/test_observable.py tests/test_tower_read_model.py -q`

**Límite:** CONFLICTED y UNKNOWN no significan que se haya demostrado un valor cero.

### Evidencias para mostrar (opcionales)

Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. Este apoyo es opcional y no forma parte del tiempo del discurso principal.

- Ver las 3 observaciones originales · `hornos`

## 07. Empecé con reglas que pudiera explicar

**Tipo:** Demostrado · reglas · **Duración orientativa:** 56 s

### Discurso

No quise empezar entrenando un modelo complejo. Primero necesitaba entender los datos y tener una referencia que pudiera comprobar. Por eso comparé dos políticas. El baseline, o regla de referencia, usa información individual: diez puntos por cada sucursal adicional válida, con un tope de cinco adicionales. La segunda política conserva esa base y suma cinco puntos por vecino económico confirmado y distinto, hasta cuatro vecinos. Aquí vecino significa otra empresa conectada por suministro o alianza. Las referencias comerciales y las relaciones solamente reportadas o inferidas no suman puntos. Tampoco cuento dos veces al mismo vecino. Así puedo explicar de dónde sale cada cambio. Son reglas exploratorias, no probabilidades de compra. Más adelante evaluaría un modelo aprendido solo si tengo información real y una forma de comprobar que mejora esta referencia.

### Qué señalar

Explica cada sumando y los dos topes; aclara que son puntos.

### Pregunta del evaluador

¿Dónde está el machine learning?

**Respuesta sencilla:** Todavía no hay un modelo entrenado. El enfoque actual es una referencia explicable para comparar después, cuando existan etiquetas reales.

**Si profundiza:** Vecinos distintos en SUPPLIES_TO y PARTNERS_WITH CONFIRMED utilizables; REFERS_TO se marca NOT_ECONOMIC. Empates por score descendente e ID público ascendente.

**Verificar en:** src/economic_graph/rankings.py:42–56; src/economic_graph/rankings.py:97–129; src/economic_graph/rankings.py:145–233

**Reproducción:** `uv run pytest tests/test_rankings.py -q`

**Límite:** Los pesos no están calibrados con intención de compra ni ventas.

## 08. Las relaciones cambian tres de cinco lugares

**Tipo:** Demostrado · T2 · **Duración orientativa:** 54 s

### Discurso

Con las dos políticas definidas, el resultado técnico que puedo mostrar es un cambio en tres de las cinco cuentas priorizadas. En T2 ambas usan las mismas veintiuna empresas elegibles y el mismo cupo. Panificadora Valle Claro y Carga Urbana del Centro permanecen en ambas listas. Con el grafo entran Café Jacaranda, Hornos del Centro y Papelería Horizonte. Salen Comedor del Andén, Mesa de Barrio y Mapa Digital Studio. El ranking completo, sus puntos y sus evidencias están registrados para poder reproducirlos. También hay empates y el código los resuelve de manera estable por identificador público. Lo que defiendo aquí es que agregar relaciones sí modifica la selección. Todavía no puedo decir que las nuevas cuentas sean mejores clientes ni que tres sustituciones equivalgan a tres ventas.

### Qué señalar

Sigue las tres entradas y tres salidas; evita interpretar tres cambios como tres ventas.

### Pregunta del evaluador

¿Tres sustituciones son una mejora del 60%?

**Respuesta sencilla:** No. Es un cambio en tres de cinco lugares. No mide una mejora en conversión o ingresos.

**Si profundiza:** comparison calcula intersección, entered_graph y left_baseline. Las posiciones se asignan a todos los elegibles antes de seleccionar las primeras cinco.

**Verificar en:** src/economic_graph/rankings.py:145–233; tests/test_rankings.py:1–456; docs/13-ranking-comparison.md:1–117

**Reproducción:** `uv run python scripts/rank_companies.py --all-cuts --format markdown`

**Límite:** Los empates y la baja cobertura de atributos pueden influir en el orden.

### Evidencias para mostrar (opcionales)

Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. Este apoyo es opcional y no forma parte del tiempo del discurso principal.

- ¿Por qué se mantienen las primeras dos empresas? · `leaders`

## 09. Jacaranda me permite explicar el cambio

**Tipo:** Demostrado · T2 · **Duración orientativa:** 54 s

### Discurso

Para explicar el resultado usaría Café Jacaranda, porque permite seguir una cuenta de principio a fin. Con la regla individual tiene cero puntos y está en el lugar diez. Al agregar relaciones confirmadas obtiene diez puntos y pasa al tercer lugar. Esos puntos vienen de dos vecinos utilizables: Hornos del Centro y Enlace Punto POS. En la captura real las líneas gruesas señalan ese respaldo. Las otras conexiones permanecen como contexto, pero no todas suman. Puedo seguir las dos que sí cuentan hasta las observaciones OBS-026 y OBS-063 del CRM sintético. Eso me permite explicar por qué cambió su prioridad. No significa que Jacaranda tenga intención de comprar o que esos negocios hayan recomendado contratar. La evidencia respalda la regla de investigación, no una venta.

### Qué señalar

Amplía la captura; señala líneas gruesas y las dos observaciones que sí puntúan.

### Pregunta del evaluador

¿Todas las líneas del dibujo dan puntos?

**Respuesta sencilla:** No. Solo los vecinos económicos confirmados utilizables. Las demás líneas dan contexto.

**Si profundiza:** La red es una vista del resultado, no el motor del score. network_data resalta relationship_ids ya elegidos por _neighbor_feature. El acomodo circular no tiene significado comercial.

**Verificar en:** src/economic_graph/tower_read_model.py:118–146; src/economic_graph/rankings.py:97–129; tests/test_control_tower.py:95–119

**Reproducción:** `uv run --group ui pytest tests/test_control_tower.py -k company_selector -q`

**Límite:** El dibujo no demuestra centralidad comercial, intención de compra ni causalidad.

### Evidencias para mostrar (opcionales)

Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. Este apoyo es opcional y no forma parte del tiempo del discurso principal.

- Ver las 2 relaciones confirmadas (+10 puntos) · `confirmed`
- Ver las 5 observaciones de contexto (0 puntos) · `context`

## 10. Así pasa mi información del archivo a la pantalla

**Tipo:** Demostrado · implementación · **Duración orientativa:** 54 s

### Discurso

Para entender el funcionamiento sigo la ruta desde observations.json. Load_observations lee ese registro y valida sus campos. Después build_context prepara la información de las vistas. Dentro hace dos llamadas separadas: snapshot reconstruye lo que se sabe al corte y compare_rankings calcula las dos políticas. Esta segunda función llama a su propio snapshot; no recibe la primera vista como entrada. También se reconstruyen los cortes pasados para mostrar la evolución. Al final puedo filtrar industria o empresa sin recalcular posiciones: si Jacaranda es tercera en el ranking general, sigue siendo tercera aunque vea una sola fila. El cálculo financiero tiene una entrada distinta, el archivo de supuestos, y no lee las empresas para inventar ventas. Esta separación me ayuda a explicar qué responsabilidad tiene cada parte.

### Qué señalar

Recorre las dos ramas de build_context y la fuente financiera separada.

### Pregunta del evaluador

¿build_context pasa su snapshot a compare_rankings?

**Respuesta sencilla:** No. Les pasa las mismas observaciones y el corte. Cada función construye su vista por su propio camino.

**Si profundiza:** En T2 hay cinco llamadas a snapshot durante build_context: una directa, una interna en compare_rankings y tres para evolution. No se midió su rendimiento a escala.

**Verificar en:** app/control_tower.py:706–841; src/economic_graph/tower_read_model.py:41–66; src/economic_graph/rankings.py:145–233; src/economic_graph/finance.py:337–405

**Reproducción:** `uv run python presentation-showcase/scripts/reproduce.py`

**Límite:** La separación de módulos no acredita una arquitectura de producción ni aislamiento por roles.

### Evidencias para mostrar (opcionales)

Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. Este apoyo es opcional y no forma parte del tiempo del discurso principal.

- Ver datos de observations.json · `ledger`
- Ver supuestos financieros · `finance`
- Ver filtros reales de Streamlit · `filters`

## 11. La Control Tower reúne lo que puedo revisar

**Tipo:** Demostrado · navegador offline · **Duración orientativa:** 54 s

### Discurso

La Control Tower es la forma de recorrer el prototipo sin abrir todos los archivos durante la exposición. Resumen muestra la selección general. Graph Health permite revisar conexiones, fuentes y conflictos. AI Performance compara las dos reglas, aunque el nombre de la vista no significa que haya un modelo entrenado. Business Funnel muestra conocidas, elegibles y priorizadas. Economic Impact reúne los escenarios financieros. Estas capturas corresponden a la aplicación real en modo offline y conservan sus parámetros para revisar cada estado. Puedo ampliar una imagen o consultar su respaldo. Después de priorizar, contactos, oportunidades, activaciones y ventas aparecen como no observados. Quise mantener visible ese límite: el tablero reúne evidencia y supuestos, pero no ejecuta campañas ni convierte por sí mismo una recomendación en un resultado comercial.

### Qué señalar

Cambia entre las cinco capturas; amplía una y muestra sus parámetros.

### Pregunta del evaluador

¿Son diseños de ejemplo o capturas reales?

**Respuesta sencilla:** Son capturas de Streamlit ejecutado en modo offline. Cada archivo registra fecha, commit y filtros.

**Si profundiza:** La automatización usa Playwright y Chromium del sistema. Conserva estados, texto visible, capturas originales y metadatos; no cambia la UI ni sus fuentes.

**Verificar en:** app/control_tower.py:706–841; app/control_tower.py:316–462; app/control_tower.py:465–538; app/control_tower.py:596–703

**Reproducción:** `python presentation-showcase/scripts/capture_tower.py`

**Límite:** La revisión se hizo en Linux; no sustituye una revisión nativa en Windows ni una prueba de carga.

### Evidencias para mostrar (opcionales)

Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. Este apoyo es opcional y no forma parte del tiempo del discurso principal.

- ¿Cómo calculé estos escenarios? · `finance-story`

## 12. Cómo organicé y comprobé el desarrollo

**Tipo:** Evidencia técnica · registros conservados · **Duración orientativa:** 51 s

### Discurso

Para organizar el proyecto utilicé GitHub. Ahí fui manteniendo el código, la documentación y sus diferentes versiones. El repositorio es privado, pero puedo compartirlo si necesitan revisar cómo está construido. También trabajé con MongoDB Atlas desde mi cuenta personal, aunque para esta demostración estoy usando la versión offline y no presento la integración remota como verificada. Durante el desarrollo y la revisión se hicieron comprobaciones para los datos, los rankings, los cálculos y la interfaz. Codex ejecutó parte de las pruebas automatizadas que conservo; yo tomé las decisiones de alcance, revisé los resultados y preparé la forma de explicarlos. Mi intención fue mantener una prueba de concepto organizada y revisable, aunque todavía no sea un sistema listo para producción.

### Qué señalar

Distingue funciones, dobles, AppTest, navegador e integración real.

### Pregunta del evaluador

¿Tú ejecutaste personalmente todas estas pruebas y la depuración?

**Respuesta sencilla:** Las ejecuciones automatizadas de la primera revisión fueron realizadas por Codex y conservan sus registros. Yo dirigí y revisé el desarrollo; no atribuyo esas ejecuciones a una validación manual mía. Puedo preparar y demostrar mi reproducción por separado.

**Si profundiza:** Cobertura con pytest-cov y ramas: 904/943 líneas y 362/396 ramas. El 94.55% combinado no debe confundirse con cobertura de líneas. Se excluyó integration porque su roundtrip carga datos. Los resultados originales se conservan sin volver a etiquetarlos como ejecuciones de esta iteración.

**Verificar en:** tests/test_mongo_observable.py:20–55; tests/test_mongo_observable.py:58–67; tests/test_control_tower.py:43–51; src/economic_graph/tower_read_model.py:374–402

**Reproducción:** `uv run --group ui pytest -m 'not integration'`

**Límite:** Cobertura alta no mide calidad comercial, producción, seguridad integral ni corrección de todos los casos.

## 13. ¿Cuántas empresas necesitaría para que la idea valga la pena?

**Tipo:** Hipótesis · cálculo reproducido · **Duración orientativa:** 55 s

### Discurso

Después de construir el prototipo me pregunté cuánto podría costarle a una empresa utilizar una solución como esta. Primero supuse diez mil pesos de implementación, seis mil de operación y cincuenta pesos más por cada empresa investigada. Después imaginé que, si el sistema ayuda a elegir mejores prospectos, podríamos pasar de una activación del diez al doce por ciento, con un margen supuesto de ocho mil pesos por nueva activación. Con cinco plazas, el posible beneficio no cubre los costos y el resultado es de menos quince mil cuatrocientos cincuenta pesos. Con quinientas plazas, y solamente si conseguimos esa mejora, el cálculo da treinta y nueve mil pesos positivos. Ambas cifras son supuestos, no ingresos observados. La viabilidad depende de conseguir una mejora real, no simplemente de utilizar IA.

### Qué señalar

Alterna cinco y 500; compara base con nulo y señala que la reserva va aparte.

### Pregunta del evaluador

¿Los 39 mil pesos prueban ROI positivo?

**Respuesta sencilla:** No. Son el resultado de supuestos de activación, margen y costos que todavía no medimos.

**Si profundiza:** ΔV = plazas×Δp×margen − plazas×Δc + ΔU − F − ΔO. Base 500: 80,000−25,000−10,000−6,000=39,000. Nulo: −25,000−10,000−6,000=−41,000. Reserva 3,200 separada; base tras reserva=35,800.

**Verificar en:** src/economic_graph/finance.py:186–227; src/economic_graph/finance.py:337–405; config/financial_assumptions.json:1–194; tests/test_finance.py:113–127

**Reproducción:** `uv run python scripts/calculate_finance.py --sensitivity --format markdown`

**Límite:** No interpretar tasas supuestas, sensibilidad o equilibrio como efectos alcanzados ni intervalos de confianza.

## 14. Así intentaría medir el valor económico real

**Tipo:** Diseño · no ejecutado · **Duración orientativa:** 57 s

### Discurso

Para saber si usar el grafo realmente ayuda necesitaría una comparación controlada, distinta del calculador. La propuesta es agrupar cuentas y equipos en bolsas que reduzcan el intercambio de información entre grupos. Asignaría al azar bolsas completas: unas usarían el baseline y otras el ranking con grafo, con capacidad y esfuerzo comparables. Mediría margen neto por todas las cuentas elegibles asignadas, incluso las que no se contactaron. Esa es la idea de intención de tratar: no evaluar solamente los éxitos. El seguimiento propuesto considera noventa días para activar y doce meses desde la asignación para margen y costos. Todavía necesito datos autorizados y suficientes bolsas independientes. Sin conocer la variación del margen y la relación entre cuentas de una misma bolsa, no daría un tamaño de muestra preciso. Este experimento todavía no se ejecuta.

### Qué señalar

Señala que se asignan bolsas antes de seleccionar, y el denominador incluye todas las cuentas.

### Pregunta del evaluador

¿Por qué no comparas directamente los dos Top 5?

**Respuesta sencilla:** Porque no fueron asignados al azar, comparten cuentas y tienen señales distintas. Eso no separa el efecto de usar el grafo.

**Si profundiza:** ITT conserva la asignación original. Inferencia por bolsa y bloques; objetivo IC bilateral 95% y potencia 80%, sin muestra calculada. Registrar contaminación, faltantes y costos sin duplicar plataforma en el KPI y en inversión.

**Verificar en:** docs/15-incrementality-experiment.md:1–88; docs/14-incremental-economic-case.md:1–178; src/economic_graph/finance.py:337–405

**Reproducción:** `Lectura: docs/15-incrementality-experiment.md; no existe un ensayo ejecutado.`

**Límite:** Si no hay suficientes bolsas independientes, este diseño no permite atribuir causalidad.

## 15. Elegiría el modelo después de tener datos

**Tipo:** Evolución propuesta · según el objetivo · **Duración orientativa:** 52 s

### Discurso

Mi siguiente paso empezaría por datos reales, identidad suficiente, permisos y resultados comerciales confiables. Después evaluaría qué herramienta responde al objetivo. Si quisiera estudiar similitud entre empresas y tuviera atributos apropiados, consideraría KNN. Si tuviera etiquetas reales de activación o conversión, podría comparar clasificación o ranking supervisado contra las reglas. Las técnicas de grafos podrían servir para estudiar comunidades o relaciones relevantes. Reinforcement Learning sería otra posibilidad, pero solo ante decisiones secuenciales, acciones y recompensas observables y una forma adecuada de evaluarlo. No lo considero equivalente a KNN ni un siguiente paso obligatorio. También podría combinar reglas y modelos si aporta algo comprobable. La idea que mantendría es empezar por datos y reglas que entienda, y exigir evidencia antes de añadir complejidad.

### Qué señalar

Distingue lo utilizado de las opciones consideradas y la condición que necesitaría cada una.

### Pregunta del evaluador

¿KNN o RL serían tus siguientes modelos?

**Respuesta sencilla:** No necesariamente. KNN podría ayudar con similitud si tengo atributos adecuados. RL requiere decisiones secuenciales y recompensas observables. Primero definiría el objetivo y cómo evaluar, y después elegiría.

**Si profundiza:** No hay KNN, clasificación aprendida, ranking supervisado, comunidades calculadas ni RL implementados en esta PoC. Un enfoque híbrido debe mejorar una referencia bajo una evaluación pertinente, sin fuga temporal.

**Verificar en:** presentation-showcase/docs/origen-y-alcance.md:1–59; presentation-showcase/docs/reto-original.md:1–190; docs/12-commercial-ranking.md:1–115

**Reproducción:** `Consultar docs/reto-original.md y docs/origen-y-alcance.md.`

**Límite:** Mencionar una técnica no equivale a implementarla o demostrar competencia para operarla en producción.

## 16. Construí una PoC; el valor real falta medirlo

**Tipo:** Conclusión con límites · **Duración orientativa:** 57 s

### Discurso

Mi respuesta al reto es una PoC controlada que conecta datos disponibles, relaciones, reglas de priorización y una forma de pensar el valor económico. Elegí adquisición B2B, acoté el problema a investigar cuentas y utilicé herramientas de IA para construir y documentar más rápido mientras revisaba y decidía el rumbo. Puedo mostrar treinta empresas en el diseño, tres cortes de conocimiento, dos políticas explicables y un cambio de tres lugares del Top 5. También puedo seguir el ejemplo de Jacaranda y revisar la Control Tower con su evidencia. Eso no demuestra más ventas, ROI o causalidad. La lectura real de Atlas y la escala siguen pendientes en estas revisiones. Mi siguiente paso sería profundizar mi comprensión del código y validar datos, operación y un experimento con una empresa real antes de recomendar un despliegue.

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

## 20. Filtrar no cambia el lugar global

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

## 21. MongoDB en memoria no es Atlas

**Tipo:** Demostrado · pruebas offline · **Duración orientativa:** 51 s

### Discurso

MemoryCollection y MemoryDatabase son objetos de Python que imitan solo las operaciones que necesita el código. Guardan documentos en diccionarios, registran consultas y usan copias para evitar cambios accidentales. La primera carga inserta ochenta y tres observaciones; la segunda no agrega ninguna. Eso prueba idempotencia: repetir la misma operación no duplica los datos. También hay pruebas que rechazan otra base, colecciones sin propiedad compatible y cambios en documentos existentes antes de escribir. En esta revisión esas escrituras ocurrieron únicamente en memoria, no en Atlas. El doble ayuda a probar rápido y sin credenciales, pero no reproduce todos los tipos BSON, índices, permisos, concurrencia o comportamiento del servidor. Para afirmar integración necesito otra comprobación contra una instancia real autorizada.

### Qué señalar

Señala 83 insertadas en memoria → 0 nuevas y el diccionario de consultas.

### Pregunta del evaluador

¿Qué no reproduce MemoryCollection?

**Respuesta sencilla:** No es un servidor completo: no prueba red, autenticación, rendimiento, concurrencia real ni todos los detalles de MongoDB.

**Si profundiza:** update_one exige únicamente $setOnInsert con upsert; find aplica available_at y subject_id. Los tests verifican protección previa a escrituras e historial temporal.

**Verificar en:** tests/test_mongo_observable.py:20–55; tests/test_mongo_observable.py:58–67; tests/test_mongo_observable.py:70–91; src/economic_graph/mongo_observable.py:39–75

**Reproducción:** `uv run pytest tests/test_mongo_observable.py -q`

**Límite:** Una carga idempotente con dobles no acredita una carga real exitosa en Atlas.

## 22. AppTest comprueba lógica; Chromium, la pantalla

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

## 23. La lectura real de Atlas queda pendiente

**Tipo:** Pendiente · sin conexión intentada · **Duración orientativa:** 57 s

### Discurso

La ruta de Atlas existe y puedo explicar su código, pero no la presento como verificada en esta revisión. Primero construye una referencia local, valida que la base sea la dedicada, lee observaciones disponibles al corte y vuelve a preparar el contexto. Después compara la huella de la entrada visible con la local. Si son distintas, bloquea la demostración comparable; no reemplaza datos remotos ni inventa cifras de respaldo. Esa función no hace ping. El proyecto tiene otra función para comprobar conexión y una prueba de integración que sí hace carga, por eso quedó excluida. La configuración y la red disponibles no bastaban para esa lectura, y se acordó trabajar offline. No cambié credenciales ni configuraciones para intentar resolverlo. Los reportes históricos de Atlas permanecen como antecedentes, no como una ejecución nueva.

### Qué señalar

Señala base dedicada, filtro temporal y comparación de SHA-256; diferencia ping de lectura.

### Pregunta del evaluador

¿Qué necesitarías para afirmar que Atlas funciona?

**Respuesta sencilla:** Una comprobación de conexión y una lectura real autorizada, con base y permisos correctos, sin confundirlas con dobles.

**Si profundiza:** read_observations envía available_at <= parse_time(as_of) al servidor y convierte BSON UTC sin zona. atlas_context comprueba visible_input_sha256; maneja errores sin exponer URI y no hace fallback silencioso.

**Verificar en:** src/economic_graph/tower_read_model.py:374–402; src/economic_graph/mongo_observable.py:78–89; src/economic_graph/database.py:29–52; tests/integration/test_atlas_observable.py:1–33

**Reproducción:** `No ejecutar la integración que escribe; revisión de código y dobles únicamente.`

**Límite:** Una lectura exitosa no valida escrituras, rendimiento, seguridad completa ni todo el historial de Atlas.

## 24. De dónde salen +$39,000 y −$41,000

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

## 25. Priorizar todavía no es vender

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

## 26. Medir a todas las cuentas asignadas

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

## 27. Un caso límite al comparar fechas

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

## 28. Un cambio pequeño, con una comprobación clara

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

## 29. Cada técnica necesita una pregunta y datos

**Tipo:** Consideradas · no implementadas · **Duración orientativa:** 51 s

### Discurso

Si me preguntan por modelos, empezaría por la pregunta que quiero responder. KNN puede ayudar a estudiar similitud si tengo atributos adecuados y una distancia razonable. Una clasificación o un ranking aprendido requieren etiquetas reales y una evaluación que respete el tiempo. Las comunidades de grafos describen estructura, pero no prueban que un grupo compre mejor. RL corresponde a decisiones secuenciales con acciones y recompensas observables; necesitaría condiciones para evaluarlo y no es una continuación obligatoria del prototipo. También puedo considerar híbridos, pero solo si mejoran una referencia verificable. Hoy lo implementado son las reglas, el historial observable, el calculador y la interfaz. Las herramientas generativas que utilicé para desarrollar no son un modelo predictivo incorporado al ranking.

### Qué señalar

Conecta cada propuesta con una evidencia faltante, sin prometer una escala.

### Pregunta del evaluador

¿Cómo evitarías elegir herramientas solo por estar de moda?

**Respuesta sencilla:** Definiría la decisión, los datos y la evaluación antes del modelo. Si una técnica no responde una necesidad comprobable, mantendría la solución más sencilla.

**Si profundiza:** Similarity, predicción supervisada, estructura de comunidades y control secuencial son objetivos distintos. El reto ofrece libertad tecnológica y pide justificar las decisiones; no exige GNN, GraphRAG o RL.

**Verificar en:** presentation-showcase/docs/origen-y-alcance.md:1–59; presentation-showcase/docs/reto-original.md:1–190; docs/12-commercial-ranking.md:1–115

**Reproducción:** `Sin benchmark ejecutado; propuesta de validación futura.`

**Límite:** Las opciones descritas no están implementadas, entrenadas o evaluadas en este proyecto.

## 30. Dónde comprobar cada parte del reto

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

## Evidencia financiera opcional · tres pasos

Estas notas aparecen únicamente en la vista del presentador cuando se abre `finance-story`; la audiencia ve solo la evidencia financiera.

### Paso 1 de 3

Para evaluar si esta idea podría ser rentable, primero establecí algunos supuestos. Imaginé una inversión de diez mil pesos para implementar la solución, seis mil para operarla y cincuenta pesos adicionales por cada plaza comercial.

También supuse que, con el método tradicional, contrataría el diez por ciento de las empresas, mientras que con el grafo podría llegar al doce por ciento.

Esa mejora todavía no está demostrada. Es justamente lo que necesitaríamos validar.

**Duración estimada:** 35–50 segundos

### Paso 2 de 3

Ahora imaginemos que aplicamos la solución a quinientas plazas comerciales.

Si el grafo consiguiera mejorar las activaciones del diez al doce por ciento, tendríamos diez clientes adicionales en promedio.

Suponiendo ocho mil pesos de margen por cada uno, obtendríamos ochenta mil pesos de beneficio adicional.

Después restaría veinticinco mil pesos de esfuerzo comercial, diez mil de implementación y seis mil de operación.

El resultado sería de treinta y nueve mil pesos positivos, antes de considerar una reserva adicional de tres mil doscientos pesos. Es un escenario hipotético, no una ganancia que ya conseguimos.

**Duración estimada:** 35–50 segundos

### Paso 3 de 3

Pero también me pregunté qué sucedería si mis supuestos no se cumplen.

Por eso preparé cuatro escenarios: conservador, base, optimista y nulo.

El escenario nulo es especialmente importante: si trabajamos con quinientas plazas y el grafo no consigue mejorar las activaciones, tendríamos un resultado negativo de cuarenta y un mil pesos antes de reserva.

Esto me permite explicar que el proyecto podría ser económicamente atractivo, pero no basta con desarrollar la tecnología. Necesitamos demostrar que realmente mejora los resultados comerciales.

**Duración estimada:** 35–50 segundos
