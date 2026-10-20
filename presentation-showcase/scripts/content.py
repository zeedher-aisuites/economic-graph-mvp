# ruff: noqa: E501
FINANCE_STORY_SPEECHES = [
    "Para evaluar si esta idea podr\u00eda ser rentable, primero establec\u00ed algunos supuestos. Imagin\u00e9 una inversi\u00f3n de diez mil pesos para implementar la soluci\u00f3n, seis mil para operarla y cincuenta pesos adicionales por cada plaza comercial.\n\nTambi\u00e9n supuse que, con el m\u00e9todo tradicional, contratar\u00eda el diez por ciento de las empresas, mientras que con el grafo podr\u00eda llegar al doce por ciento.\n\nEsa mejora todav\u00eda no est\u00e1 demostrada. Es justamente lo que necesitar\u00edamos validar.",
    "Ahora imaginemos que aplicamos la soluci\u00f3n a quinientas plazas comerciales.\n\nSi el grafo consiguiera mejorar las activaciones del diez al doce por ciento, tendr\u00edamos diez clientes adicionales en promedio.\n\nSuponiendo ocho mil pesos de margen por cada uno, obtendr\u00edamos ochenta mil pesos de beneficio adicional.\n\nDespu\u00e9s restar\u00eda veinticinco mil pesos de esfuerzo comercial, diez mil de implementaci\u00f3n y seis mil de operaci\u00f3n.\n\nEl resultado ser\u00eda de treinta y nueve mil pesos positivos, antes de considerar una reserva adicional de tres mil doscientos pesos. Es un escenario hipot\u00e9tico, no una ganancia que ya conseguimos.",
    "Pero tambi\u00e9n me pregunt\u00e9 qu\u00e9 suceder\u00eda si mis supuestos no se cumplen.\n\nPor eso prepar\u00e9 cuatro escenarios: conservador, base, optimista y nulo.\n\nEl escenario nulo es especialmente importante: si trabajamos con quinientas plazas y el grafo no consigue mejorar las activaciones, tendr\u00edamos un resultado negativo de cuarenta y un mil pesos antes de reserva.\n\nEsto me permite explicar que el proyecto podr\u00eda ser econ\u00f3micamente atractivo, pero no basta con desarrollar la tecnolog\u00eda. Necesitamos demostrar que realmente mejora los resultados comerciales.",
]
"""Fuente de verdad de la defensa en primera persona: versión anterior, perspectiva del candidato."""

SLIDES = [
    {
        "id": "inicio",
        "title": "ConectaPyME: caso de negocio B2B",
        "chapter": "El caso de negocio B2B",
        "kind": "challenge",
        "status": "El reto · mi punto de partida",
        "refs": [
            "presentation-showcase/docs/reto-original.md",
            "presentation-showcase/docs/origen-y-alcance.md",
        ],
        "claims": [
            (
                "El reto pide construir un Economic Graph y demostrar valor económico incremental.",
                "diseño",
            )
        ],
        "capture": None,
        "command": "Consultar el contexto técnico, diapositivas 4, 5, 10 y 12; extracción completa en "
        "docs/reto-original.md.",
        "speech": "Cuando recibí el reto, entendí que no se trataba solamente de dibujar conexiones o elegir una "
        "base de datos. La pregunta era cómo construir un Economic Graph de pequeñas empresas para una "
        "Telco y cómo demostrar que genera valor económico incremental. Para mí, eso significa conectar "
        "información con una decisión comercial y después medir si esa decisión deja un beneficio "
        "adicional frente a una referencia. ConectaPyME es mi respuesta a esa pregunta. El grafo "
        "representa empresas y sus relaciones económicas. Preparé una prueba de concepto pequeña, con "
        "datos sintéticos, para explorar una parte del problema. En esta presentación voy a explicar "
        "cómo elegí el alcance, cómo trabajé con asistencia de IA, qué hace el prototipo y qué "
        "resultados puedo defender. También voy a separar lo que funciona técnicamente de lo que todavía "
        "necesitaría medir con datos reales.",
        "point": "Señala la pregunta completa y la cadena información → decisión → valor medible.",
        "question": "¿Qué decisión de negocio intenta mejorar ConectaPyME?",
        "answer": "Conectar datos y relaciones con una decisión comercial y explicar cómo mediría un beneficio "
        "económico adicional. La arquitectura es parte del soporte.",
        "deep": "Las diapositivas 4 y 5 del reto fijan la pregunta y su intención; 10 y 12 establecen Control "
        "Tower y seis entregables.",
        "warning": "El prototipo no acredita ventas, ROI ni un efecto económico real; las cifras ilustrativas del "
        "reto no son resultados de ConectaPyME.",
        "origin": "Contexto de negocio y enfoque declarado para el portafolio.",
    },
    {
        "id": "problema",
        "title": "Primero definí qué decisión quería mejorar",
        "chapter": "01 · Cómo lo interpreté",
        "kind": "approach",
        "status": "Mi elección · caso ficticio",
        "refs": [
            "presentation-showcase/docs/reto-original.md",
            "presentation-showcase/docs/origen-y-alcance.md",
            "src/economic_graph/rankings.py:POLICY",
        ],
        "claims": [
            (
                "Elegí adquisición B2B como caso de uso y una Telco ficticia para acotar el ejercicio.",
                "diseño",
            ),
            ("El ranking implementado conserva capacidad K=5.", "demostrado"),
        ],
        "command": "uv run python scripts/rank_companies.py --as-of T2",
        "speech": "Antes de elegir tecnologías, me hice varias preguntas. ¿Qué empresa usaría el grafo? ¿Qué "
        "decisión necesitaba mejorar? ¿Qué información tendría disponible? ¿Y cómo sabría si las "
        "conexiones servían para algo? El reto ofrecía varias posibilidades y elegí adquisición de "
        "clientes empresariales: investigar pequeñas empresas similares o conectadas con clientes "
        "actuales. Para aterrizarlo definí una Telco ficticia, ConectaPyME, y una decisión concreta: a "
        "quién investigar primero cuando hay más cuentas que tiempo. En la demostración uso cinco "
        "lugares. Eso me permite comparar dos listas sin cambiar la capacidad comercial. La empresa, su "
        "territorio y su contexto operativo son una simulación. No estoy describiendo ni diagnosticando "
        "los procesos reales de una empresa. Tampoco significa que las seleccionadas ya estén listas para "
        "recibir una llamada; todavía faltaría validar cobertura, identidad y permiso de contacto.",
        "point": "Muestra el caso B2B Acquisition del reto y la decisión acotada de cinco lugares.",
        "question": "¿Estás afirmando que este problema existe en una empresa real?",
        "answer": "No. Elegí una posibilidad del reto y la desarrollé en una Telco ficticia. Tendría que validar "
        "el problema y el proceso real con la empresa.",
        "deep": "La intención de adquisición está en la diapositiva 7 del reto. K=5 pertenece a la política de la "
        "PoC, no a una capacidad comercial medida.",
        "warning": "El caso de uso elegido no implica que ya se haya implementado similitud aprendida o una "
        "política especial para vecinos de clientes actuales.",
        "capture": None,
        "origin": "Enfoque declarado por el candidato; K respaldado por la implementación.",
    },
    {
        "id": "hipotesis",
        "title": "Mi hipótesis: las relaciones podrían ayudar",
        "kind": "hypothesis",
        "speech": "Mi hipótesis fue que una empresa puede ser más interesante para investigar cuando entiendo cómo "
        "se relaciona con otros negocios, y no solamente sus atributos individuales. Por ejemplo, "
        "conocer un vínculo económico confirmado podría agregar contexto a una cuenta con poca "
        "información propia. Eso podría ayudar a seleccionar prospectos más útiles y, bajo ciertas "
        "condiciones, mejorar la adquisición y el margen. Pero no lo doy por hecho. Primero necesitaría "
        "datos confiables y autorizados, relaciones relevantes y bien verificadas, una comparación justa "
        "contra una referencia, un equipo que pueda actuar y resultados reales para medir. Por eso "
        "dividí la pregunta en dos partes. Con la PoC puedo comprobar si el grafo cambia la selección y "
        "explicar por qué. Para saber si ese cambio ayuda a vender mejor necesitaría una evaluación "
        "comercial posterior.",
        "point": "Sigue la cadena de hipótesis y las cinco condiciones; separa cambio de lista de mejora "
        "comercial.",
        "question": "¿Qué parte de tu hipótesis comprobaste?",
        "answer": "Que las relaciones confirmadas cambian la selección bajo las reglas del prototipo. Que esa "
        "selección genere mayor margen sigue pendiente.",
        "deep": "El ranking compara atributos individuales frente a los mismos atributos más vecinos económicos "
        "confirmados; no estima probabilidades ni un efecto causal.",
        "warning": "Una señal relevante para describir una relación no necesariamente predice una compra.",
        "claims": [
            (
                "Las relaciones económicas podrían mejorar la utilidad comercial de la selección.",
                "hipótesis",
            ),
            (
                "Se requiere una comparación y resultados comerciales para medir ese valor.",
                "diseño",
            ),
        ],
        "status": "Hipótesis · todavía por validar",
        "refs": [
            "presentation-showcase/docs/reto-original.md",
            "presentation-showcase/docs/origen-y-alcance.md",
        ],
        "command": "Consultar docs/reto-original.md y docs/origen-y-alcance.md.",
        "origin": "Declaración del candidato en la versión anterior; formulada con apoyo de IA.",
        "chapter": "02 · La hipótesis comercial",
    },
    {
        "id": "estrategia",
        "title": "Dirigí una PoC con apoyo de IA",
        "kind": "ai-workflow",
        "speech": "Con el plazo del reto y sin datos reales de una Telco, decidí construir una prueba de concepto "
        "controlada. Utilicé ChatGPT o GPT, Gemini y Codex para avanzar más rápido en investigación, "
        "programación y documentación. Mi participación fue plantear el alcance y las hipótesis, revisar "
        "propuestas y avances, decidir qué tenía sentido y solicitar o autorizar cambios. No quiero "
        "presentar todo el código como si lo hubiera escrito manualmente. También distingo dirigir el "
        "desarrollo, comprender el resultado y ejecutar personalmente una validación: son cosas "
        "diferentes. Las pruebas y capturas automatizadas tienen sus registros y su origen en la "
        "trazabilidad. Durante la exposición me apoyaré en esa evidencia sin atribuirme ejecuciones que "
        "no hice. Mi responsabilidad es poder explicar la solución, reconocer sus límites y practicar "
        "cómo reproducir sus partes importantes.",
        "point": "Señala tu papel, el apoyo de GPT/Gemini/Codex y la diferencia entre dirigir, comprender y "
        "validar.",
        "question": "¿Qué hiciste tú y qué hicieron las herramientas?",
        "answer": "Yo definí el enfoque, revisé avances y tomé decisiones. Usé IA para apoyar investigación, "
        "implementación y documentación. Los registros identifican las comprobaciones automatizadas; no "
        "las presento como ejecuciones manuales mías.",
        "deep": "El uso de las tres herramientas y el papel de dirección corresponden a la declaración del "
        "candidato. No hay base para atribuir un porcentaje de código o una tarea específica a cada "
        "herramienta. Las evidencias nuevas de V1 fueron producidas por Codex.",
        "warning": "El apoyo de IA no acredita por sí solo que yo domine cada archivo o haya ejecutado todas las "
        "validaciones.",
        "claims": [
            (
                "El candidato declara uso de ChatGPT/GPT, Gemini y Codex y un papel de alcance, revisión y "
                "decisiones.",
                "diseño",
            )
        ],
        "status": "Mi forma de trabajo · asistencia de IA",
        "refs": [
            "presentation-showcase/docs/reto-original.md",
            "presentation-showcase/docs/origen-y-alcance.md",
        ],
        "command": "Consultar docs/reto-original.md y docs/origen-y-alcance.md.",
        "origin": "Declaración del candidato en la versión anterior; formulada con apoyo de IA.",
        "chapter": "03 · Mi estrategia de trabajo",
    },
    {
        "id": "tiempo",
        "title": "Construí un laboratorio de 30 PyMEs",
        "chapter": "04 · Mi laboratorio sintético",
        "kind": "timeline",
        "status": "Demostrado · sintético",
        "refs": [
            "src/economic_graph/contracts.py:CUTS",
            "src/economic_graph/observable.py:visible_observations",
            "src/economic_graph/observable.py:snapshot",
            "tests/test_observable.py:test_cut_coverage_and_truth_only_reconciliation",
        ],
        "claims": [
            ("T0/T1/T2 contienen 12/17/23 empresas y 28/54/83 observaciones.", "demostrado"),
            ("El diseño restringido contiene 30 empresas; no alimenta el ranking.", "demostrado"),
        ],
        "capture": "05-graph-t0",
        "command": "uv run python presentation-showcase/scripts/reproduce.py",
        "speech": "Para poner a prueba la idea sin inventar datos de una Telco real, decidí trabajar con treinta "
        "empresas sintéticas, sus atributos y sus relaciones. Pero no quería que el sistema conociera "
        "todo desde el principio. Separé el universo completo del simulador de la información que "
        "estaría disponible para una decisión. En enero, T0, se conocen doce empresas; en mayo, T1, "
        "diecisiete; y en septiembre, T2, veintitrés. Las observaciones acumuladas son veintiocho, "
        "cincuenta y cuatro y ochenta y tres. Las otras siete empresas siguen fuera de la información "
        "observable al último corte. Esto me permite explorar una idea sencilla: una decisión histórica "
        "debe usar lo que se sabía en ese momento. No completo el ranking con información del universo "
        "privado solo porque el simulador conoce la respuesta.",
        "point": "Distingue las 30 del diseño de las 12/17/23 conocidas; señala las siete que siguen fuera.",
        "question": "¿Por qué no usas solamente la fecha del hecho?",
        "answer": "Porque un hecho pudo ocurrir antes y conocerse después. Para evitar usar información futura, "
        "filtro por disponibilidad.",
        "deep": "visible_observations valida el contrato y aplica parse_time(available_at) <= parse_time(as_of), "
        "ordena y devuelve una copia. Los cortes son a las 12:00 UTC, equivalentes a las 06:00 de Ciudad "
        "de México.",
        "warning": "Los tres cortes no son tres experimentos ni mediciones independientes de ventas.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "procedencia",
        "title": "Quise conservar las fuentes y las dudas",
        "chapter": "05 · La importancia de los datos",
        "kind": "provenance",
        "status": "Demostrado · sintético",
        "refs": [
            "src/economic_graph/contracts.py:OBSERVATION_FIELDS",
            "src/economic_graph/observable.py:_attribute",
            "src/economic_graph/observable.py:snapshot",
            "tests/test_tower_read_model.py:test_conflicts_candidates_and_duplicate_evidence_survive",
            "src/economic_graph/observable.py:visible_observations",
        ],
        "claims": [
            (
                "En T2 se conservan dos atributos en conflicto y dos registros candidatos.",
                "demostrado",
            ),
            ("Una coincidencia de nombre no fusiona empresas.", "demostrado"),
            (
                "available_at determina desde cuándo se usa una observación en el corte.",
                "demostrado",
            ),
        ],
        "command": "uv run pytest tests/test_observable.py tests/test_tower_read_model.py -q",
        "speech": "Al trabajar con información incompleta me pareció importante conservar de dónde viene cada dato "
        "y cuándo puedo usarlo. El prototipo guarda observaciones con fuente, fechas y estado de "
        "verificación. Utiliza available_at, que indica desde cuándo estuvo disponible el dato, para "
        "evitar usar información del futuro. También conserva dudas. En Hornos del Centro hay registros "
        "que dicen dos sucursales y otros que dicen tres. No quise elegir una versión solo porque era "
        "más reciente sin una regla válida para resolverlo. El código mantiene el conflicto y esa señal "
        "aporta cero puntos. Eso no significa que la empresa tenga cero sucursales. Con los nombres pasa "
        "algo parecido: una coincidencia produce un candidato de identidad, pero no fusiona negocios. "
        "Así puedo explicar qué sé, qué no sé y qué tendría que revisar.",
        "point": "Señala las observaciones OBS-028, OBS-047 y OBS-075 y su contribución cero por conflicto.",
        "question": "¿Por qué no gana automáticamente el dato más nuevo?",
        "answer": "Porque no hay una regla aprobada para resolver ese conflicto. Prefiero conservar las opciones y "
        "revisarlas.",
        "deep": "_attribute marca CONFLICTED si hay valores distintos en el historial visible. Las relaciones "
        "conservan historia de estados; las candidaturas usan normalización de nombres, sin identificación "
        "fuerte.",
        "warning": "CONFLICTED y UNKNOWN no significan que se haya demostrado un valor cero.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "reglas",
        "title": "Empecé con reglas que pudiera explicar",
        "chapter": "06 · Mi primera solución",
        "kind": "rules",
        "status": "Demostrado · reglas",
        "refs": [
            "src/economic_graph/rankings.py:_branch_feature",
            "src/economic_graph/rankings.py:_neighbor_feature",
            "src/economic_graph/rankings.py:compare_rankings",
        ],
        "claims": [
            ("Baseline: 10 puntos por sucursal adicional válida, con tope de cinco.", "demostrado"),
            (
                "Grafo: baseline más 5 puntos por vecino económico confirmado distinto, con tope de cuatro.",
                "demostrado",
            ),
        ],
        "command": "uv run pytest tests/test_rankings.py -q",
        "speech": "No quise empezar entrenando un modelo complejo. Primero necesitaba entender los datos y tener "
        "una referencia que pudiera comprobar. Por eso comparé dos políticas. El baseline, o regla de "
        "referencia, usa información individual: diez puntos por cada sucursal adicional válida, con un "
        "tope de cinco adicionales. La segunda política conserva esa base y suma cinco puntos por vecino "
        "económico confirmado y distinto, hasta cuatro vecinos. Aquí vecino significa otra empresa "
        "conectada por suministro o alianza. Las referencias comerciales y las relaciones solamente "
        "reportadas o inferidas no suman puntos. Tampoco cuento dos veces al mismo vecino. Así puedo "
        "explicar de dónde sale cada cambio. Son reglas exploratorias, no probabilidades de compra. Más "
        "adelante evaluaría un modelo aprendido solo si tengo información real y una forma de comprobar "
        "que mejora esta referencia.",
        "point": "Explica cada sumando y los dos topes; aclara que son puntos.",
        "question": "¿Dónde está el machine learning?",
        "answer": "Todavía no hay un modelo entrenado. El enfoque actual es una referencia explicable para "
        "comparar después, cuando existan etiquetas reales.",
        "deep": "Vecinos distintos en SUPPLIES_TO y PARTNERS_WITH CONFIRMED utilizables; REFERS_TO se marca "
        "NOT_ECONOMIC. Empates por score descendente e ID público ascendente.",
        "warning": "Los pesos no están calibrados con intención de compra ni ventas.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "cambio",
        "title": "Las relaciones cambian tres de cinco lugares",
        "chapter": "07 · Resultado técnico",
        "kind": "ranking",
        "status": "Demostrado · T2",
        "refs": [
            "src/economic_graph/rankings.py:compare_rankings",
            "tests/test_rankings.py",
            "docs/13-ranking-comparison.md",
        ],
        "claims": [("Top 5 comparte dos cuentas y sustituye tres en T2.", "demostrado")],
        "capture": "07-ai-global",
        "command": "uv run python scripts/rank_companies.py --all-cuts --format markdown",
        "speech": "Con las dos políticas definidas, el resultado técnico que puedo mostrar es un cambio en tres de "
        "las cinco cuentas priorizadas. En T2 ambas usan las mismas veintiuna empresas elegibles y el "
        "mismo cupo. Panificadora Valle Claro y Carga Urbana del Centro permanecen en ambas listas. Con "
        "el grafo entran Café Jacaranda, Hornos del Centro y Papelería Horizonte. Salen Comedor del "
        "Andén, Mesa de Barrio y Mapa Digital Studio. El ranking completo, sus puntos y sus evidencias "
        "están registrados para poder reproducirlos. También hay empates y el código los resuelve de "
        "manera estable por identificador público. Lo que defiendo aquí es que agregar relaciones sí "
        "modifica la selección. Todavía no puedo decir que las nuevas cuentas sean mejores clientes ni "
        "que tres sustituciones equivalgan a tres ventas.",
        "point": "Sigue las tres entradas y tres salidas; evita interpretar tres cambios como tres ventas.",
        "question": "¿Tres sustituciones son una mejora del 60%?",
        "answer": "No. Es un cambio en tres de cinco lugares. No mide una mejora en conversión o ingresos.",
        "deep": "comparison calcula intersección, entered_graph y left_baseline. Las posiciones se asignan a todos "
        "los elegibles antes de seleccionar las primeras cinco.",
        "warning": "Los empates y la baja cobertura de atributos pueden influir en el orden.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "cafe",
        "title": "Jacaranda me permite explicar el cambio",
        "chapter": "08 · Un ejemplo entendible",
        "kind": "cafe",
        "status": "Demostrado · T2",
        "refs": [
            "src/economic_graph/tower_read_model.py:account_detail",
            "src/economic_graph/rankings.py:_neighbor_feature",
            "tests/test_control_tower.py:test_company_selector_updates_network_and_detail_without_rescoring",
        ],
        "claims": [
            ("Café Jacaranda pasa de 0 a 10 puntos y de posición 10 a 3.", "demostrado"),
            (
                "Dos vecinos confirmados utilizables respaldan los diez puntos relacionales.",
                "demostrado",
            ),
        ],
        "capture": "02-graph-cafe",
        "command": "uv run --group ui pytest tests/test_control_tower.py -k company_selector -q",
        "speech": "Para explicar el resultado usaría Café Jacaranda, porque permite seguir una cuenta de principio "
        "a fin. Con la regla individual tiene cero puntos y está en el lugar diez. Al agregar relaciones "
        "confirmadas obtiene diez puntos y pasa al tercer lugar. Esos puntos vienen de dos vecinos "
        "utilizables: Hornos del Centro y Enlace Punto POS. En la captura real las líneas gruesas "
        "señalan ese respaldo. Las otras conexiones permanecen como contexto, pero no todas suman. Puedo "
        "seguir las dos que sí cuentan hasta las observaciones OBS-026 y OBS-063 del CRM sintético. Eso "
        "me permite explicar por qué cambió su prioridad. No significa que Jacaranda tenga intención de "
        "comprar o que esos negocios hayan recomendado contratar. La evidencia respalda la regla de "
        "investigación, no una venta.",
        "point": "Amplía la captura; señala líneas gruesas y las dos observaciones que sí puntúan.",
        "question": "¿Todas las líneas del dibujo dan puntos?",
        "answer": "No. Solo los vecinos económicos confirmados utilizables. Las demás líneas dan contexto.",
        "deep": "La red es una vista del resultado, no el motor del score. network_data resalta relationship_ids "
        "ya elegidos por _neighbor_feature. El acomodo circular no tiene significado comercial.",
        "warning": "El dibujo no demuestra centralidad comercial, intención de compra ni causalidad.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "arquitectura",
        "title": "Así pasa mi información del archivo a la pantalla",
        "chapter": "09 · Cómo funciona el código",
        "kind": "architecture",
        "status": "Demostrado · implementación",
        "refs": [
            "app/control_tower.py:main",
            "src/economic_graph/tower_read_model.py:build_context",
            "src/economic_graph/rankings.py:compare_rankings",
            "src/economic_graph/finance.py:financial_report",
        ],
        "claims": [
            (
                "build_context llama por separado a snapshot y compare_rankings; compare_rankings llama a su "
                "propio snapshot.",
                "demostrado",
            ),
            (
                "El calculador financiero tiene una entrada independiente del ledger empresarial.",
                "demostrado",
            ),
        ],
        "command": "uv run python presentation-showcase/scripts/reproduce.py",
        "speech": "Para entender el funcionamiento sigo la ruta desde observations.json. Load_observations lee ese "
        "registro y valida sus campos. Después build_context prepara la información de las vistas. "
        "Dentro hace dos llamadas separadas: snapshot reconstruye lo que se sabe al corte y "
        "compare_rankings calcula las dos políticas. Esta segunda función llama a su propio snapshot; no "
        "recibe la primera vista como entrada. También se reconstruyen los cortes pasados para mostrar "
        "la evolución. Al final puedo filtrar industria o empresa sin recalcular posiciones: si "
        "Jacaranda es tercera en el ranking general, sigue siendo tercera aunque vea una sola fila. El "
        "cálculo financiero tiene una entrada distinta, el archivo de supuestos, y no lee las empresas "
        "para inventar ventas. Esta separación me ayuda a explicar qué responsabilidad tiene cada parte.",
        "point": "Recorre las dos ramas de build_context y la fuente financiera separada.",
        "question": "¿build_context pasa su snapshot a compare_rankings?",
        "answer": "No. Les pasa las mismas observaciones y el corte. Cada función construye su vista por su propio "
        "camino.",
        "deep": "En T2 hay cinco llamadas a snapshot durante build_context: una directa, una interna en "
        "compare_rankings y tres para evolution. No se midió su rendimiento a escala.",
        "warning": "La separación de módulos no acredita una arquitectura de producción ni aislamiento por roles.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "torre",
        "title": "La Control Tower reúne lo que puedo revisar",
        "chapter": "10 · Mi Control Tower",
        "kind": "tower",
        "status": "Demostrado · navegador offline",
        "refs": [
            "app/control_tower.py:main",
            "app/control_tower.py:health_page",
            "app/control_tower.py:performance_page",
            "app/control_tower.py:economic_page",
        ],
        "claims": [
            (
                "Las cinco vistas se recorrieron en Chromium con interacciones y capturas auténticas.",
                "demostrado",
            )
        ],
        "capture": "01-resumen-t2",
        "command": "python presentation-showcase/scripts/capture_tower.py",
        "speech": "La Control Tower es la forma de recorrer el prototipo sin abrir todos los archivos durante la "
        "exposición. Resumen muestra la selección general. Graph Health permite revisar conexiones, "
        "fuentes y conflictos. AI Performance compara las dos reglas, aunque el nombre de la vista no "
        "significa que haya un modelo entrenado. Business Funnel muestra conocidas, elegibles y "
        "priorizadas. Economic Impact reúne los escenarios financieros. Estas capturas corresponden a la "
        "aplicación real en modo offline y conservan sus parámetros para revisar cada estado. Puedo "
        "ampliar una imagen o consultar su respaldo. Después de priorizar, contactos, oportunidades, "
        "activaciones y ventas aparecen como no observados. Quise mantener visible ese límite: el "
        "tablero reúne evidencia y supuestos, pero no ejecuta campañas ni convierte por sí mismo una "
        "recomendación en un resultado comercial.",
        "point": "Cambia entre las cinco capturas; amplía una y muestra sus parámetros.",
        "question": "¿Son diseños de ejemplo o capturas reales?",
        "answer": "Son capturas de Streamlit ejecutado en modo offline. Cada archivo registra fecha, commit y "
        "filtros.",
        "deep": "La automatización usa Playwright y Chromium del sistema. Conserva estados, texto visible, "
        "capturas originales y metadatos; no cambia la UI ni sus fuentes.",
        "warning": "La revisión se hizo en Linux; no sustituye una revisión nativa en Windows ni una prueba de "
        "carga.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "pruebas",
        "title": "Cómo organicé y comprobé el desarrollo",
        "chapter": "11 · Cómo se comprobó",
        "kind": "tests",
        "status": "Evidencia técnica · registros conservados",
        "refs": [
            "tests/test_mongo_observable.py:MemoryCollection",
            "tests/test_mongo_observable.py:MemoryDatabase",
            "tests/test_control_tower.py:app",
            "src/economic_graph/tower_read_model.py:atlas_context",
        ],
        "claims": [
            (
                "La suite original ejecutada pasó 284 pruebas; una integración fue excluida.",
                "demostrado",
            ),
            (
                "Cobertura medida: 95.9% de líneas y 91.4% de ramas de economic_graph, sin app ni scripts.",
                "demostrado",
            ),
            ("Atlas real no se verificó durante esta revisión.", "pendiente"),
        ],
        "command": "uv run --group ui pytest -m 'not integration'",
        "speech": "Para organizar el proyecto utilicé GitHub. Ahí fui manteniendo el código, la documentación y sus diferentes versiones. El repositorio es privado, pero puedo compartirlo si necesitan revisar cómo está construido. También trabajé con MongoDB Atlas desde mi cuenta personal, aunque para esta demostración estoy usando la versión offline y no presento la integración remota como verificada. Durante el desarrollo y la revisión se hicieron comprobaciones para los datos, los rankings, los cálculos y la interfaz. Codex ejecutó parte de las pruebas automatizadas que conservo; yo tomé las decisiones de alcance, revisé los resultados y preparé la forma de explicarlos. Mi intención fue mantener una prueba de concepto organizada y revisable, aunque todavía no sea un sistema listo para producción.",
        "point": "Distingue funciones, dobles, AppTest, navegador e integración real.",
        "question": "¿Tú ejecutaste personalmente todas estas pruebas y la depuración?",
        "answer": "Las ejecuciones automatizadas de la primera revisión fueron realizadas por Codex y conservan "
        "sus registros. Yo dirigí y revisé el desarrollo; no atribuyo esas ejecuciones a una validación "
        "manual mía. Puedo preparar y demostrar mi reproducción por separado.",
        "deep": "Cobertura con pytest-cov y ramas: 904/943 líneas y 362/396 ramas. El 94.55% combinado no debe "
        "confundirse con cobertura de líneas. Se excluyó integration porque su roundtrip carga datos. Los "
        "resultados originales se conservan sin volver a etiquetarlos como ejecuciones de esta iteración.",
        "warning": "Cobertura alta no mide calidad comercial, producción, seguridad integral ni corrección de "
        "todos los casos.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "economia",
        "title": "¿Cuántas empresas necesitaría para que la idea valga la pena?",
        "chapter": "12 · Condiciones económicas",
        "kind": "economics",
        "status": "Hipótesis · cálculo reproducido",
        "refs": [
            "src/economic_graph/finance.py:_evaluate",
            "src/economic_graph/finance.py:financial_report",
            "config/financial_assumptions.json",
            "tests/test_finance.py:test_mandatory_null_preserves_costs_and_is_not_zero_profit",
        ],
        "claims": [
            (
                "Con 500 plazas el caso base da +39,000 y el nulo −41,000 MXN antes de reserva.",
                "hipótesis",
            ),
            (
                "Con cinco plazas el caso base da −15,450 MXN; el equilibrio base requiere 40.625 pp frente a "
                "1.025 pp a 500.",
                "hipótesis",
            ),
        ],
        "capture": "15-economic-500",
        "command": "uv run python scripts/calculate_finance.py --sensitivity --format markdown",
        "speech": "Después de construir el prototipo me pregunté cuánto podría costarle a una empresa utilizar una solución como esta. Primero supuse diez mil pesos de implementación, seis mil de operación y cincuenta pesos más por cada empresa investigada. Después imaginé que, si el sistema ayuda a elegir mejores prospectos, podríamos pasar de una activación del diez al doce por ciento, con un margen supuesto de ocho mil pesos por nueva activación. Con cinco plazas, el posible beneficio no cubre los costos y el resultado es de menos quince mil cuatrocientos cincuenta pesos. Con quinientas plazas, y solamente si conseguimos esa mejora, el cálculo da treinta y nueve mil pesos positivos. Ambas cifras son supuestos, no ingresos observados. La viabilidad depende de conseguir una mejora real, no simplemente de utilizar IA.",
        "point": "Alterna cinco y 500; compara base con nulo y señala que la reserva va aparte.",
        "question": "¿Los 39 mil pesos prueban ROI positivo?",
        "answer": "No. Son el resultado de supuestos de activación, margen y costos que todavía no medimos.",
        "deep": "ΔV = plazas×Δp×margen − plazas×Δc + ΔU − F − ΔO. Base 500: 80,000−25,000−10,000−6,000=39,000. "
        "Nulo: −25,000−10,000−6,000=−41,000. Reserva 3,200 separada; base tras reserva=35,800.",
        "warning": "No interpretar tasas supuestas, sensibilidad o equilibrio como efectos alcanzados ni "
        "intervalos de confianza.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "experimento",
        "title": "Así intentaría medir el valor económico real",
        "chapter": "13 · Cómo mediría valor real",
        "kind": "experiment",
        "status": "Diseño · no ejecutado",
        "refs": [
            "docs/15-incrementality-experiment.md",
            "docs/14-incremental-economic-case.md",
            "src/economic_graph/finance.py:financial_report",
        ],
        "claims": [
            (
                "El protocolo propone asignación 1:1 por bolsas independientes y KPI por toda cuenta elegible "
                "asignada.",
                "diseño",
            ),
            (
                "Faltan datos, varianza, correlación dentro de bolsas y suficientes unidades para fijar "
                "muestra.",
                "pendiente",
            ),
        ],
        "command": "Lectura: docs/15-incrementality-experiment.md; no existe un ensayo ejecutado.",
        "speech": "Para saber si usar el grafo realmente ayuda necesitaría una comparación controlada, distinta "
        "del calculador. La propuesta es agrupar cuentas y equipos en bolsas que reduzcan el intercambio "
        "de información entre grupos. Asignaría al azar bolsas completas: unas usarían el baseline y "
        "otras el ranking con grafo, con capacidad y esfuerzo comparables. Mediría margen neto por todas "
        "las cuentas elegibles asignadas, incluso las que no se contactaron. Esa es la idea de intención "
        "de tratar: no evaluar solamente los éxitos. El seguimiento propuesto considera noventa días "
        "para activar y doce meses desde la asignación para margen y costos. Todavía necesito datos "
        "autorizados y suficientes bolsas independientes. Sin conocer la variación del margen y la "
        "relación entre cuentas de una misma bolsa, no daría un tamaño de muestra preciso. Este "
        "experimento todavía no se ejecuta.",
        "point": "Señala que se asignan bolsas antes de seleccionar, y el denominador incluye todas las cuentas.",
        "question": "¿Por qué no comparas directamente los dos Top 5?",
        "answer": "Porque no fueron asignados al azar, comparten cuentas y tienen señales distintas. Eso no separa "
        "el efecto de usar el grafo.",
        "deep": "ITT conserva la asignación original. Inferencia por bolsa y bloques; objetivo IC bilateral 95% y "
        "potencia 80%, sin muestra calculada. Registrar contaminación, faltantes y costos sin duplicar "
        "plataforma en el KPI y en inversión.",
        "warning": "Si no hay suficientes bolsas independientes, este diseño no permite atribuir causalidad.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "evolucion",
        "title": "Elegiría el modelo después de tener datos",
        "kind": "evolution",
        "speech": "Mi siguiente paso empezaría por datos reales, identidad suficiente, permisos y resultados "
        "comerciales confiables. Después evaluaría qué herramienta responde al objetivo. Si quisiera "
        "estudiar similitud entre empresas y tuviera atributos apropiados, consideraría KNN. Si tuviera "
        "etiquetas reales de activación o conversión, podría comparar clasificación o ranking "
        "supervisado contra las reglas. Las técnicas de grafos podrían servir para estudiar comunidades "
        "o relaciones relevantes. Reinforcement Learning sería otra posibilidad, pero solo ante "
        "decisiones secuenciales, acciones y recompensas observables y una forma adecuada de evaluarlo. "
        "No lo considero equivalente a KNN ni un siguiente paso obligatorio. También podría combinar "
        "reglas y modelos si aporta algo comprobable. La idea que mantendría es empezar por datos y "
        "reglas que entienda, y exigir evidencia antes de añadir complejidad.",
        "point": "Distingue lo utilizado de las opciones consideradas y la condición que necesitaría cada una.",
        "question": "¿KNN o RL serían tus siguientes modelos?",
        "answer": "No necesariamente. KNN podría ayudar con similitud si tengo atributos adecuados. RL requiere "
        "decisiones secuenciales y recompensas observables. Primero definiría el objetivo y cómo "
        "evaluar, y después elegiría.",
        "deep": "No hay KNN, clasificación aprendida, ranking supervisado, comunidades calculadas ni RL "
        "implementados en esta PoC. Un enfoque híbrido debe mejorar una referencia bajo una evaluación "
        "pertinente, sin fuga temporal.",
        "warning": "Mencionar una técnica no equivale a implementarla o demostrar competencia para operarla en "
        "producción.",
        "claims": [
            (
                "KNN, supervisados, comunidades, híbridos y RL son opciones consideradas, no implementadas ni "
                "pasos obligatorios.",
                "diseño",
            ),
            (
                "Faltan datos reales y condiciones de evaluación para decidir si ML aporta una mejora.",
                "pendiente",
            ),
        ],
        "status": "Evolución propuesta · según el objetivo",
        "refs": [
            "presentation-showcase/docs/origen-y-alcance.md",
            "presentation-showcase/docs/reto-original.md",
            "docs/12-commercial-ranking.md",
        ],
        "command": "Consultar docs/reto-original.md y docs/origen-y-alcance.md.",
        "origin": "Declaración del candidato en la versión anterior; formulada con apoyo de IA.",
        "chapter": "14 · Cómo la haría evolucionar",
    },
    {
        "id": "cierre",
        "title": "Construí una PoC; el valor real falta medirlo",
        "chapter": "15 · Mi respuesta y sus límites",
        "kind": "closing",
        "status": "Conclusión con límites",
        "refs": [
            "docs/02-challenge-traceability.md",
            "src/economic_graph/rankings.py:compare_rankings",
            "docs/15-incrementality-experiment.md",
        ],
        "claims": [
            (
                "El proyecto demuestra una priorización sintética reproducible, no un aumento real de ventas o "
                "ROI.",
                "demostrado",
            ),
            (
                "Atlas, escala, producción y valor causal siguen pendientes de validación en esta revisión.",
                "pendiente",
            ),
        ],
        "command": "Consultar evidence/results y docs/auditoria.md de esta entrega.",
        "speech": "Mi respuesta al reto es una PoC controlada que conecta datos disponibles, relaciones, reglas de "
        "priorización y una forma de pensar el valor económico. Elegí adquisición B2B, acoté el problema "
        "a investigar cuentas y utilicé herramientas de IA para construir y documentar más rápido "
        "mientras revisaba y decidía el rumbo. Puedo mostrar treinta empresas en el diseño, tres cortes "
        "de conocimiento, dos políticas explicables y un cambio de tres lugares del Top 5. También puedo "
        "seguir el ejemplo de Jacaranda y revisar la Control Tower con su evidencia. Eso no demuestra "
        "más ventas, ROI o causalidad. La lectura real de Atlas y la escala siguen pendientes en estas "
        "revisiones. Mi siguiente paso sería profundizar mi comprensión del código y validar datos, "
        "operación y un experimento con una empresa real antes de recomendar un despliegue.",
        "point": "Cierra con lo demostrado, lo pendiente y el siguiente paso; abre anexo si preguntan.",
        "question": "¿Qué harías después?",
        "answer": "Primero practicaría la reproducción del código y la depuración. Para negocio validaría datos, "
        "permisos, costos y viabilidad de un piloto controlado.",
        "deep": "Los seis entregables están mapeados en el anexo y la matriz. La auditoría nueva es trabajo de "
        "Codex; no sustituye que el candidato explique y modifique el código por sí mismo.",
        "warning": "No presentar este MVP como sistema productivo o caso de éxito comercial.",
        "origin": "Evidencia técnica conservada de V1, producida por Codex; enfoque narrado por el candidato. Sin "
        "atribución de ejecución manual personal.",
    },
    {
        "id": "a-flujo",
        "title": "build_context(): las llamadas reales",
        "chapter": "Anexo A · Recorrido de ejecución",
        "kind": "calltree",
        "status": "Demostrado · código",
        "annex": True,
        "refs": [
            "src/economic_graph/tower_read_model.py:build_context",
            "src/economic_graph/rankings.py:compare_rankings",
            "src/economic_graph/observable.py:snapshot",
        ],
        "claims": [
            (
                "En T2 build_context invoca snapshot cinco veces por sus ramas y evolución.",
                "demostrado",
            )
        ],
        "command": "uv run python presentation-showcase/scripts/reproduce.py",
        "speech": "Si me preguntan por build_context, lo explicaría como una preparación de datos para las "
        "pantallas. Recibe observaciones y un corte. Llama directamente a snapshot y, por separado, a "
        "compare_rankings. Esta última vuelve a llamar a snapshot dentro de su implementación. Además, "
        "build_context reconstruye un resumen por cada corte pasado para la evolución. En T2 eso da "
        "cinco llamadas a snapshot: dos para la vista y el ranking y tres para la historia. No existe "
        "una cadena donde el primer snapshot sea la entrada del ranking. Esta repetición es aceptable "
        "para explicar el prototipo pequeño, pero no tengo una medición para decir qué tan bien escala. "
        "Antes de optimizar, mediría tiempos y comprobaría que los resultados siguen siendo iguales.",
        "point": "Señala las líneas 43, 44 y 51 y la llamada interna del ranking.",
        "question": "¿Puedes dibujar la relación exacta sin leer un README?",
        "answer": "Sí: build_context tiene ramas separadas para snapshot, compare_rankings y evolución; "
        "compare_rankings hace su propio snapshot.",
        "deep": "summary=summarize(view), sources y states derivan de view; coverage deriva de ranking.companies. "
        "Ningún filtro de industria entra a build_context.",
        "warning": "No se midió latencia ni costo de estas reconstrucciones con miles de empresas.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-datos",
        "title": "Datos, conflictos e identidades",
        "chapter": "Anexo B · Contrato observable",
        "kind": "data-detail",
        "status": "Demostrado · código",
        "annex": True,
        "refs": [
            "src/economic_graph/contracts.py:validate_observations",
            "src/economic_graph/observable.py:_attribute",
            "src/economic_graph/observable.py:_name_key",
            "src/economic_graph/simulator/project.py:project_observations",
        ],
        "claims": [
            (
                "El contrato valida tipos, IDs, fechas ordenadas y extremos conocidos; rechaza campos "
                "privados.",
                "demostrado",
            )
        ],
        "command": "uv run pytest tests/test_observable.py -q",
        "speech": "El archivo observable es la frontera de entrada de la aplicación. Su contrato revisa campos, "
        "tipos, identificadores y que las fechas tengan zona y un orden válido. También comprueba que "
        "una relación no mencione una empresa que todavía no era identificable cuando se conoció el "
        "dato. El diseño privado sirve para construir y auditar la simulación; no se consulta para "
        "completar atributos o puntuar. Los IDs públicos se generan desde observaciones, sin revelar los "
        "nombres internos del diseño. Para conflictos de atributos se conservan los valores distintos. "
        "Para alias se normaliza el nombre y solo se sugieren candidatos. Esto ayuda a explicar la "
        "incertidumbre, pero no reemplaza un proceso real de verificación de identidad, con fuentes "
        "autorizadas y revisión de casos ambiguos.",
        "point": "Distingue el diseño restringido de observations.json y explica UNKNOWN frente a CONFLICTED.",
        "question": "¿Cómo evitas completar una empresa con información privilegiada?",
        "answer": "La ruta comercial lee solo observaciones y sus módulos no importan el simulador para "
        "enriquecerlas.",
        "deep": "assert_no_private_fields rechaza metadatos de verdad. La prueba public_only_ui ejecuta una copia "
        "sin simulator ni design-data y bloquea red y credenciales.",
        "warning": "La revisión no es una auditoría integral de privacidad ni una prueba de identidad empresarial "
        "fuerte.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-politica",
        "title": "Elegibilidad, topes y empates",
        "chapter": "Anexo C · Ranking reproducible",
        "kind": "policy-detail",
        "status": "Demostrado · política 003a",
        "annex": True,
        "refs": [
            "src/economic_graph/rankings.py:compare_rankings",
            "src/economic_graph/rankings.py:_attribute_status",
            "src/economic_graph/rankings.py:_relationship_context",
            "src/economic_graph/rankings.py:_boundary",
        ],
        "claims": [
            (
                "Solo se excluye servicio activo confirmado sin conflicto; desconocido queda por validar.",
                "demostrado",
            ),
            ("Empates se resuelven por ID público y se declaran en la frontera K=5.", "demostrado"),
        ],
        "command": "uv run pytest tests/test_rankings.py -q",
        "speech": "La elegibilidad de esta PoC es conservadora en lo que afirma, aunque todavía es mínima para una "
        "operación real. Solo excluye una cuenta si tiene servicio activo confirmado y sin conflicto. "
        "Que el servicio sea desconocido no prueba que no sea cliente: queda pendiente de validación "
        "comercial. Después se calculan ambas reglas para todas las elegibles. Los puntos se ordenan de "
        "mayor a menor y, si empatan, gana el identificador público menor. Esa decisión es reproducible, "
        "pero no agrega evidencia comercial. Por eso el reporte muestra si el empate cruza la quinta "
        "plaza. También se limitan las contribuciones y se deduplican vecinos. Con pocos atributos "
        "observados, varios lugares pueden depender del desempate; es una limitación que debo mencionar "
        "al interpretar la lista.",
        "point": "Muestra cobertura 3/21 individual y 5/21 relacional; explica por qué cero puntos puede "
        "significar falta de evidencia.",
        "question": "¿Por qué es elegible una empresa cuyo servicio no conoces?",
        "answer": "Es la regla de demostración aprobada. Para un piloto necesitaría comprobar que no es cliente y "
        "otras condiciones antes de contactar.",
        "deep": "La última evidencia debe ser CONFIRMED y el valor True, con atributo OBSERVED. "
        "_relationship_context bloquea oposición confirmada/descartada y conflictos antes de contar "
        "vecinos.",
        "warning": "ID ascendente es un desempate técnico; no es señal de valor ni regla comercial calibrada.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "filtros",
        "title": "Filtrar no cambia el lugar global",
        "chapter": "Anexo D · Ranking global y filtros",
        "kind": "filters",
        "status": "Demostrado · reconstrucción interactiva",
        "refs": [
            "src/economic_graph/tower_read_model.py:build_context",
            "src/economic_graph/tower_read_model.py:segment_ids",
            "src/economic_graph/tower_read_model.py:ranking_table",
            "tests/test_control_tower.py:test_industry_and_score_filters_preserve_global_rankings",
            "tests/test_tower_read_model.py:test_industry_filters_do_not_refill_funnel_or_rankings",
        ],
        "claims": [
            (
                "Al filtrar industria o Café Jacaranda, las posiciones globales 10 y 3 se conservan.",
                "demostrado",
            ),
            ("Los segmentos intersectan el Top 5 global; no rellenan lugares.", "demostrado"),
        ],
        "capture": "10-ranking-cafe",
        "command": "uv run python presentation-showcase/scripts/reproduce.py",
        "speech": "Esta función prepara primero el ranking general. Después puedo filtrar por industria o por "
        "empresa sin volver a calcular sus posiciones. Si Café Jacaranda estaba en el tercer lugar "
        "general, debe seguir mostrando tres aunque sea la única fila visible. En esta demostración "
        "puedo cambiar entre todas las cuentas, restaurantes y cafeterías, o solo Jacaranda. Los datos "
        "vienen de la ejecución del repositorio; este pequeño control es una reconstrucción para "
        "explicar el resultado, no una captura de Streamlit. También guardé capturas de la aplicación "
        "original con esos filtros. La razón de conservar el lugar es poder comparar sin cambiar "
        "silenciosamente la pregunta. Un filtro para inspeccionar no es una nueva competencia entre las "
        "cuentas visibles. Tampoco lleno los cinco lugares con otras empresas del sector.",
        "point": "Activa los tres filtros y observa que #10 y #3 permanecen iguales.",
        "question": "¿Por qué no aparece como lugar uno cuando solo queda una empresa?",
        "answer": "Porque muestro su posición en el ranking completo. La selección de pantalla solo decide qué "
        "filas ver.",
        "deep": "segment_ids devuelve IDs del contexto; ranking_table copia baseline_position, graph_position y "
        "banderas selected ya calculadas. Las pruebas comparan las filas filtradas con el subconjunto "
        "original.",
        "warning": "La interacción de esta diapositiva usa resultados congelados; la captura y el script permiten "
        "verificar la aplicación original.",
        "annex": True,
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-dobles",
        "title": "MongoDB en memoria no es Atlas",
        "chapter": "Anexo E · Pruebas con dobles",
        "kind": "doubles",
        "status": "Demostrado · pruebas offline",
        "annex": True,
        "refs": [
            "tests/test_mongo_observable.py:MemoryCollection",
            "tests/test_mongo_observable.py:MemoryDatabase",
            "tests/test_mongo_observable.py:test_repeated_load_is_idempotent_for_observations_companies_and_edges",
            "src/economic_graph/mongo_observable.py:load_observable",
        ],
        "claims": [
            (
                "El doble reproduce el subconjunto de find/update/index usado por el cargador, no un servidor "
                "MongoDB completo.",
                "demostrado",
            ),
            (
                "Repetir la carga en memoria inserta cero registros nuevos y conserva 83.",
                "demostrado",
            ),
        ],
        "command": "uv run pytest tests/test_mongo_observable.py -q",
        "speech": "MemoryCollection y MemoryDatabase son objetos de Python que imitan solo las operaciones que "
        "necesita el código. Guardan documentos en diccionarios, registran consultas y usan copias para "
        "evitar cambios accidentales. La primera carga inserta ochenta y tres observaciones; la segunda "
        "no agrega ninguna. Eso prueba idempotencia: repetir la misma operación no duplica los datos. "
        "También hay pruebas que rechazan otra base, colecciones sin propiedad compatible y cambios en "
        "documentos existentes antes de escribir. En esta revisión esas escrituras ocurrieron únicamente "
        "en memoria, no en Atlas. El doble ayuda a probar rápido y sin credenciales, pero no reproduce "
        "todos los tipos BSON, índices, permisos, concurrencia o comportamiento del servidor. Para "
        "afirmar integración necesito otra comprobación contra una instancia real autorizada.",
        "point": "Señala 83 insertadas en memoria → 0 nuevas y el diccionario de consultas.",
        "question": "¿Qué no reproduce MemoryCollection?",
        "answer": "No es un servidor completo: no prueba red, autenticación, rendimiento, concurrencia real ni "
        "todos los detalles de MongoDB.",
        "deep": "update_one exige únicamente $setOnInsert con upsert; find aplica available_at y subject_id. Los "
        "tests verifican protección previa a escrituras e historial temporal.",
        "warning": "Una carga idempotente con dobles no acredita una carga real exitosa en Atlas.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-apptest",
        "title": "AppTest comprueba lógica; Chromium, la pantalla",
        "chapter": "Anexo F · Dos verificaciones complementarias",
        "kind": "apptest",
        "status": "Demostrado · Linux",
        "annex": True,
        "refs": [
            "tests/test_control_tower.py:app",
            "tests/test_control_tower.py:test_industry_and_score_filters_preserve_global_rankings",
            "tests/test_control_tower.py:test_invalid_ledger_is_visible_and_finance_still_available",
            "tests/ui_test_support.py:prepare_ui_runtime",
        ],
        "claims": [
            (
                "AppTest verifica controles, métricas, tablas y errores sin navegador; no valida la apariencia "
                "real.",
                "demostrado",
            )
        ],
        "command": "uv run --group ui pytest tests/test_control_tower.py -q",
        "speech": "AppTest carga el script de Streamlit y permite mover controles como si fuera una prueba de la "
        "aplicación. Puedo seleccionar un período, revisar opciones y comprobar que Café Jacaranda "
        "conserva sus posiciones. También comprueba que una lectura fallida no reutilice cifras "
        "anteriores y que las etapas sin eventos sigan diciendo no observado. En las pruebas offline, el "
        "cliente MongoDB y la carga de configuración están bloqueados. Eso es útil para demostrar que "
        "esa ruta no necesita credenciales. Lo que AppTest no muestra es el dibujo final del navegador: "
        "no puedo usarlo para asegurar que una tabla cabe o que un texto se lee bien. Para eso se "
        "capturaron las cinco vistas con Chromium. Las dos verificaciones responden preguntas diferentes "
        "y se complementan.",
        "point": "Contrasta una aserción de la prueba con una captura auténtica.",
        "question": "¿AppTest equivale a una prueba visual de extremo a extremo?",
        "answer": "No. Ejecuta Streamlit y revisa sus elementos. Chromium permite comprobar cómo aparecen y se "
        "usan en la pantalla.",
        "deep": "La preparación importa dependencias nativas antes del timeout funcional de 15 s. Un guard bloquea "
        "red externa y permite IPC local necesario. La simulación de codificación Windows no sustituye "
        "ejecución nativa.",
        "warning": "Las capturas no prueban todas las combinaciones, dispositivos, accesibilidad o ejecución "
        "Windows.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-atlas",
        "title": "La lectura real de Atlas queda pendiente",
        "chapter": "Anexo G · Integración y límites",
        "kind": "atlas",
        "status": "Pendiente · sin conexión intentada",
        "annex": True,
        "refs": [
            "src/economic_graph/tower_read_model.py:atlas_context",
            "src/economic_graph/mongo_observable.py:read_observations",
            "src/economic_graph/database.py:check_connection",
            "tests/integration/test_atlas_observable.py",
        ],
        "claims": [
            (
                "atlas_context valida base dedicada, lee al corte y compara huella con el ledger local; no "
                "ejecuta ping.",
                "demostrado",
            ),
            (
                "No se ejecutaron conexiones, lecturas ni escrituras remotas durante esta revisión.",
                "pendiente",
            ),
        ],
        "command": "No ejecutar la integración que escribe; revisión de código y dobles únicamente.",
        "speech": "La ruta de Atlas existe y puedo explicar su código, pero no la presento como verificada en esta "
        "misión. Primero construye una referencia local, valida que la base sea la dedicada, lee "
        "observaciones disponibles al corte y vuelve a preparar el contexto. Después compara la huella "
        "de la entrada visible con la local. Si son distintas, bloquea la demostración comparable; no "
        "reemplaza datos remotos ni inventa cifras de respaldo. Esa función no hace ping. El proyecto "
        "tiene otra función para comprobar conexión y una prueba de integración que sí hace carga, por "
        "eso quedó excluida. La configuración y la red disponibles no bastaban para esa lectura, y se "
        "acordó trabajar offline. No cambié credenciales ni configuraciones para intentar resolverlo. "
        "Los reportes históricos de Atlas permanecen como antecedentes, no como una ejecución nueva.",
        "point": "Señala base dedicada, filtro temporal y comparación de SHA-256; diferencia ping de lectura.",
        "question": "¿Qué necesitarías para afirmar que Atlas funciona?",
        "answer": "Una comprobación de conexión y una lectura real autorizada, con base y permisos correctos, sin "
        "confundirlas con dobles.",
        "deep": "read_observations envía available_at <= parse_time(as_of) al servidor y convierte BSON UTC sin "
        "zona. atlas_context comprueba visible_input_sha256; maneja errores sin exponer URI y no hace "
        "fallback silencioso.",
        "warning": "Una lectura exitosa no valida escrituras, rendimiento, seguridad completa ni todo el historial "
        "de Atlas.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-finanzas",
        "title": "De dónde salen +$39,000 y −$41,000",
        "chapter": "Anexo H · Aritmética financiera",
        "kind": "finance-detail",
        "status": "Hipótesis · aritmética probada",
        "annex": True,
        "refs": [
            "src/economic_graph/finance.py:_evaluate",
            "src/economic_graph/finance.py:_threshold",
            "config/financial_assumptions.json",
            "tests/test_finance.py:test_accounting_identity_no_double_cost_or_reserve",
        ],
        "claims": [
            ("Base 500: 500×0.02×8,000 − 500×50 − 10,000 − 6,000 = 39,000 MXN.", "hipótesis"),
            (
                "Con Δp=0 se conservan costos y resulta −41,000; reserva de 3,200 se muestra aparte.",
                "hipótesis",
            ),
        ],
        "command": "uv run python scripts/calculate_finance.py --format markdown",
        "speech": "Puedo reconstruir el caso base sin depender de una cifra puesta en la diapositiva. Multiplico "
        "quinientas plazas por dos puntos porcentuales de mejora y ocho mil pesos de margen: son ochenta "
        "mil pesos de margen incremental supuesto. Resto veinticinco mil de costo comercial adicional, "
        "diez mil fijos y seis mil de operación. El saldo es treinta y nueve mil antes de reserva. El "
        "caso nulo conserva esos costos, pero pone la mejora en cero: pierde cuarenta y un mil. La "
        "reserva de tres mil doscientos se muestra aparte; al restarla, el caso base queda en treinta y "
        "cinco mil ochocientos. El código usa Decimal y revisa unidades y valoración temporal para "
        "evitar dobles descuentos. Toda esta precisión comprueba aritmética, no que los supuestos sean "
        "reales.",
        "point": "Recorre cada renglón de la cuenta y distingue saldo antes y después de reserva.",
        "question": "¿Ya descontaste dos veces el margen o los costos?",
        "answer": "Los importes del ejemplo ya son valor presente. El código valida horizonte y descuento y separa "
        "prospección, margen neto y reserva.",
        "deep": "90 días para activación; horizonte 12 meses, tasa mensual 1%. Base y nulo usan margen 8,000, "
        "Δc=50, ΔU=0, F=10,000 y ΔO=6,000. Umbral sin reserva: 41,000/(500×8,000)=1.025 pp; con reserva "
        "1.105 pp.",
        "warning": "Los costos fijos constantes al cambiar escala sirven para explorar; no son cotizaciones reales "
        "a volumen.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "embudo",
        "title": "Priorizar todavía no es vender",
        "chapter": "Anexo I · Límites del embudo",
        "kind": "funnel",
        "status": "Demostrado · sintético",
        "refs": [
            "src/economic_graph/tower_read_model.py:funnel",
            "tests/test_control_tower.py:test_funnel_missing_stages_are_text_not_zero",
            "app/control_tower.py:funnel_page",
        ],
        "claims": [
            (
                "T2 muestra 23 conocidas, 21 elegibles, dos excluidas y cinco priorizadas.",
                "demostrado",
            ),
            ("Contactos, oportunidades, activaciones y ventas no están observados.", "pendiente"),
        ],
        "capture": "12-business-funnel",
        "command": "uv run --group ui pytest tests/test_control_tower.py -k funnel -q",
        "speech": "El embudo ayuda a ver exactamente dónde termina la evidencia. En T2 hay veintitrés empresas "
        "conocidas. Dos quedan fuera por servicio activo confirmado y veintiuna participan en el "
        "ranking. De ahí selecciono cinco para investigar. Las dos exclusiones son una rama aparte, no "
        "una etapa que se reste después de priorizar. Más adelante la pantalla dice no observado para "
        "contactos, oportunidades, activaciones y ventas. Es distinto de poner cero. No tengo eventos "
        "que permitan saber cuántos intentos hubo o cuántos contratos se activaron. Tampoco sumaría las "
        "dos listas de cinco como si fueran diez contactos, porque son políticas alternativas y "
        "comparten cuentas. Esta separación me permite presentar lo construido sin convertir una "
        "decisión de prioridad en un resultado comercial que todavía no existe.",
        "point": "Recorre 23 → 21 → 5 y detente antes de contactos.",
        "question": "¿Cuál fue tu tasa de conversión?",
        "answer": "No puedo calcularla: no hay contactos y activaciones verificadas en este conjunto de datos.",
        "deep": "funnel devuelve None y Estado=No observado para etapas sin datos. Las pruebas exigen texto "
        "explícito y evitan reemplazar faltantes por ceros.",
        "warning": "Sin eventos comerciales no hay tasas observadas de conversión ni embudo comercial completo.",
        "annex": True,
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-causal",
        "title": "Medir a todas las cuentas asignadas",
        "chapter": "Anexo J · Experimento futuro",
        "kind": "causal-detail",
        "status": "Diseño · no ejecutado",
        "annex": True,
        "refs": ["docs/15-incrementality-experiment.md", "docs/14-incremental-economic-case.md"],
        "claims": [
            (
                "El KPI propuesto conserva la asignación original y faltante no equivale a cero.",
                "diseño",
            ),
            (
                "La inferencia debe respetar bolsas y bloques, sin tratar cuentas conectadas como "
                "independientes.",
                "diseño",
            ),
        ],
        "command": "Lectura del protocolo; no hay resultados experimentales que reproducir.",
        "speech": "La parte que más cuidaría del experimento es qué cuentas entran a la evaluación. No mediría "
        "únicamente a las contactadas o a las que siguieron la recomendación. Mantendría todas las "
        "elegibles originalmente asignadas; eso es intención de tratar. Si una cuenta compra por otro "
        "canal también cuenta, porque busco el efecto de la política completa. Si no puedo verificar su "
        "resultado, es faltante, no una venta cero. La asignación ocurre por bolsas para reducir que las "
        "relaciones o los vendedores mezclen los grupos. El análisis debe respetar esa unidad y los "
        "tamaños de las bolsas. Se propone un intervalo de confianza del noventa y cinco por ciento, "
        "pero todavía no existe la información necesaria para calcular muestra, precisión o un efecto "
        "real.",
        "point": "Señala todo el denominador y la contaminación entre bolsas.",
        "question": "¿Por qué no calculaste el tamaño de muestra con 500 plazas?",
        "answer": "Porque las plazas del calculador no son unidades independientes. Faltan variación del margen, "
        "correlación dentro de bolsas y su número y tamaño.",
        "deep": "El protocolo propone estimador de totales ponderados por probabilidad de asignación, expresado "
        "por cuenta elegible; inferencia por aleatorización o clusters preespecificada. Plataforma se "
        "evalúa después, sin restarla dos veces.",
        "warning": "No significancia no prueba equivalencia; un intervalo válido tampoco elimina contaminación o "
        "faltantes.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "depuracion",
        "title": "Un caso límite al comparar fechas",
        "chapter": "Anexo K · Caso aislado de fechas",
        "kind": "debug",
        "status": "Demostrado · caso aislado",
        "refs": [
            "src/economic_graph/observable.py:snapshot",
            "src/economic_graph/rankings.py:_latest",
            "presentation-showcase/experiments/test_timezone_conflict.py",
        ],
        "claims": [
            (
                "El snapshot original compara texto de fechas al detectar estados simultáneos; el ranking "
                "compara instantes.",
                "demostrado",
            ),
            (
                "Dos regresiones fallan en original y pasan con una corrección experimental en memoria.",
                "demostrado",
            ),
        ],
        "command": "uv run pytest presentation-showcase/experiments/test_timezone_conflict.py -q",
        "speech": "Quiero mostrar también una limitación concreta. En la auditoría, Codex construyó un caso "
        "aislado con dos observaciones opuestas que llegaron en el mismo instante. Una fecha terminaba "
        "en Z y la otra en más cero cero dos puntos cero cero. Ambas representan la misma hora. El "
        "ranking las interpreta como un conflicto, pero snapshot compara el texto de las fechas y puede "
        "mostrar solamente descartada. La causa está en esa comparación, no en MongoDB. La corrección "
        "experimental compara instantes ya convertidos, y las dos pruebas de regresión pasan. El motor "
        "original no fue modificado. Este problema no aparece en el ledger aprobado, cuyas fechas están "
        "normalizadas. Puedo explicar cómo se reproduce y cómo lo investigaría, pero el hallazgo y el "
        "cambio experimental fueron realizados por Codex.",
        "point": "Señala mismo instante, resultado distinto y comparación propuesta; reconoce el origen del "
        "trabajo.",
        "question": "¿Encontraste un error en los resultados presentados?",
        "answer": "No en el ledger aprobado. Es un defecto reproducible con una entrada válida aislada que usa "
        "otra forma de escribir la misma hora.",
        "deep": "snapshot agrupa latest_states con igualdad de cadenas; _latest en rankings usa parse_time. La "
        "prueba introduce una observación DISCARDED simultánea y válida. El original falla dos veces y la "
        "copia modificada en memoria pasa dos veces.",
        "warning": "La corrección es experimental; no se integró al proyecto ni se atribuye como competencia "
        "personal ya demostrada.",
        "annex": True,
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-cambio",
        "title": "Un cambio pequeño, con una comprobación clara",
        "chapter": "Anexo L · Práctica de ingeniería",
        "kind": "change-detail",
        "status": "Experimental · realizado por Codex",
        "annex": True,
        "refs": [
            "src/economic_graph/observable.py:snapshot",
            "presentation-showcase/experiments/test_timezone_conflict.py",
        ],
        "claims": [
            (
                "La modificación experimental se aplica solo a una copia en memoria; el ledger y motor "
                "original permanecen iguales.",
                "demostrado",
            ),
            (
                "La competencia personal del candidato para repetir la depuración sigue por demostrar.",
                "pendiente",
            ),
        ],
        "command": "SHOWCASE_SNAPSHOT_VARIANT=original uv run pytest "
        "presentation-showcase/experiments/test_timezone_conflict.py -q",
        "speech": "Para estudiar el código puedo repetir este ejercicio en una copia. Primero leo el contrato y la "
        "función que agrupa los estados. Después creo dos observaciones opuestas válidas con el mismo "
        "instante y distinta representación de zona horaria. La prueba exige que la vista y el ranking "
        "coincidan en conflicto. En el original falla; en la copia experimental pasa al comparar fechas "
        "convertidas. También puedo revisar que los archivos originales conservan sus huellas. Esta es "
        "una demostración práctica preparada por Codex. Yo no debería decir que descubrí o resolví "
        "personalmente ese error hasta poder repetirlo y explicarlo por mi cuenta. Lo usaría como una "
        "práctica guiada: anticipar qué pasará, ejecutar, leer la diferencia y justificar por qué el "
        "cambio corrige ese caso.",
        "point": "Abre el archivo experimental y los dos registros de pruebas.",
        "question": "¿Tú hiciste esta corrección?",
        "answer": "La preparó Codex durante la auditoría. Puedo estudiar y reproducirla, pero no la atribuyo como "
        "experiencia personal ya demostrada.",
        "deep": "El test usa compile/exec en un ModuleType independiente y sustituye una comparación en la cadena "
        "fuente. No altera sys.modules del motor comercial ni escribe en src. Dos variantes: +00:00 y "
        "+0000.",
        "warning": "La práctica aislada no sustituye revisión de una corrección productiva y pruebas más amplias.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-futuro",
        "title": "Cada técnica necesita una pregunta y datos",
        "chapter": "Anexo M · Aprendizaje y evolución",
        "kind": "ml-detail",
        "status": "Consideradas · no implementadas",
        "annex": True,
        "refs": [
            "presentation-showcase/docs/origen-y-alcance.md",
            "presentation-showcase/docs/reto-original.md",
            "docs/12-commercial-ranking.md",
        ],
        "claims": [
            (
                "Las técnicas consideradas tienen objetivos y requisitos distintos; el sistema actual usa "
                "reglas.",
                "diseño",
            )
        ],
        "command": "Sin benchmark ejecutado; propuesta de validación futura.",
        "speech": "Si me preguntan por modelos, empezaría por la pregunta que quiero responder. KNN puede ayudar a "
        "estudiar similitud si tengo atributos adecuados y una distancia razonable. Una clasificación o "
        "un ranking aprendido requieren etiquetas reales y una evaluación que respete el tiempo. Las "
        "comunidades de grafos describen estructura, pero no prueban que un grupo compre mejor. RL "
        "corresponde a decisiones secuenciales con acciones y recompensas observables; necesitaría "
        "condiciones para evaluarlo y no es una continuación obligatoria del prototipo. También puedo "
        "considerar híbridos, pero solo si mejoran una referencia verificable. Hoy lo implementado son "
        "las reglas, el historial observable, el calculador y la interfaz. Las herramientas generativas "
        "que utilicé para desarrollar no son un modelo predictivo incorporado al ranking.",
        "point": "Conecta cada propuesta con una evidencia faltante, sin prometer una escala.",
        "question": "¿Cómo evitarías elegir herramientas solo por estar de moda?",
        "answer": "Definiría la decisión, los datos y la evaluación antes del modelo. Si una técnica no responde "
        "una necesidad comprobable, mantendría la solución más sencilla.",
        "deep": "Similarity, predicción supervisada, estructura de comunidades y control secuencial son objetivos "
        "distintos. El reto ofrece libertad tecnológica y pide justificar las decisiones; no exige GNN, "
        "GraphRAG o RL.",
        "warning": "Las opciones descritas no están implementadas, entrenadas o evaluadas en este proyecto.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
    {
        "id": "a-mapa",
        "title": "Dónde comprobar cada parte del reto",
        "chapter": "Anexo N · Mapa de evidencias",
        "kind": "map",
        "status": "Trazabilidad de la entrega",
        "annex": True,
        "refs": ["docs/02-challenge-traceability.md", "presentation-showcase/docs/auditoria.md"],
        "claims": [
            (
                "Los seis entregables tienen referencias, comandos y límites en la matriz de esta revisión.",
                "demostrado",
            )
        ],
        "command": "Consultar docs/trazabilidad.csv y evidence/source/manifest.json.",
        "speech": "Este mapa me ayuda a responder preguntas sin saturar la exposición principal. El problema y la "
        "capacidad cubren Business Framing. Las observaciones y los cortes cubren Economic Graph. Las "
        "dos reglas y sus límites explican AI/ML Approach. Las funciones y sus dependencias cubren "
        "Architecture. El calculador y el protocolo futuro cubren Economic Case. Las cinco vistas "
        "corresponden a Control Tower. Cada afirmación importante tiene una referencia de código o "
        "documento, un comando cuando se puede reproducir, y una limitación. También puedo consultar el "
        "guion, las preguntas de defensa y el informe de auditoría. Las fuentes originales se conservan "
        "como referencia y las cifras nuevas se sostienen en la ejecución. Si me preguntan algo que no "
        "medimos, mi respuesta debe decirlo y proponer cómo lo comprobaría.",
        "point": "Abre la matriz y muestra una fila con fuente, commit, comando y captura.",
        "question": "¿Cómo sé que una afirmación de la presentación corresponde a este código?",
        "answer": "La matriz enlaza la afirmación con archivo, líneas, commit, resultado o captura y sus límites.",
        "deep": "Se preservan huellas SHA-256 del ledger, supuestos y fuentes auditadas; los anexos incluyen "
        "resultados de pruebas y metadatos de capturas. Las referencias históricas no sustituyen evidencia "
        "nueva.",
        "warning": "Una referencia facilita auditar; no convierte una hipótesis en un resultado observado.",
        "origin": "Evidencia y ejercicio de la primera revisión realizados por Codex; conservados, no atribuidos "
        "al candidato.",
    },
]

# Apoyos opcionales; no añaden tablas ni tiempo obligatorio al discurso principal.
CONTEXTUAL_EVIDENCES = {
    "procedencia": [
        {"id": "hornos", "label": "Ver las 3 observaciones originales"},
    ],
    "cambio": [
        {"id": "leaders", "label": "¿Por qué se mantienen las primeras dos empresas?"},
    ],
    "cafe": [
        {"id": "confirmed", "label": "Ver las 2 relaciones confirmadas (+10 puntos)"},
        {"id": "context", "label": "Ver las 5 observaciones de contexto (0 puntos)"},
    ],
    "arquitectura": [
        {"id": "ledger", "label": "Ver datos de observations.json"},
        {"id": "finance", "label": "Ver supuestos financieros"},
        {"id": "filters", "label": "Ver filtros reales de Streamlit"},
    ],
    "torre": [
        {"id": "finance-story", "label": "¿Cómo calculé estos escenarios?"},
    ],
}
for slide in SLIDES:
    if slide["id"] in CONTEXTUAL_EVIDENCES:
        slide["evidences"] = CONTEXTUAL_EVIDENCES[slide["id"]]
        slide["evidence_note"] = (
            "Si quiero profundizar, aquí puedo mostrar los registros originales y después abrir "
            "su detalle técnico. Desde el presentador envío el panel a la ventana de diapositivas "
            "y puedo cerrarlo sin cambiar de sección. Son datos sintéticos offline y resultados "
            "reproducidos; no demuestran ventas ni una conexión en vivo a Atlas. "
            "Este apoyo es opcional y no forma parte del tiempo del discurso principal."
        )

CONTEXTUAL_CLAIMS = {
    "procedencia": [
        (
            "OBS-028 y OBS-047 son REPORTED; OBS-075 es CONFIRMED. Sus valores 2/3/3 mantienen el conflicto de sucursales.",
            "demostrado",
        ),
    ],
    "cambio": [
        (
            "Panificadora conserva 50 puntos y #1; Carga Urbana conserva 10 y #2. Ambas tienen cero vecinos confirmados utilizables en T2.",
            "demostrado",
        ),
        (
            "El empate de 10 puntos se resuelve por company_id público ascendente, sin interpretación comercial del desempate.",
            "demostrado",
        ),
    ],
    "cafe": [
        (
            "OBS-026 y OBS-063 confirman dos vecinos económicos distintos que aportan 10 puntos a Jacaranda.",
            "demostrado",
        ),
        (
            "OBS-044/037/045/043/072 conservan contexto y aportan cero puntos a Jacaranda; las dos de Ruta Corta son afirmaciones distintas.",
            "demostrado",
        ),
    ],
    "arquitectura": [
        (
            "El JSON observable local tiene 83 registros; alimenta la ruta offline, sin consulta en vivo a Atlas.",
            "demostrado",
        ),
        (
            "La configuración financiera declara cinco plazas por bolsa y tres escenarios; el código deriva la escala de 500 y el escenario nulo.",
            "demostrado",
        ),
    ],
}
for slide in SLIDES:
    slide["claims"].extend(CONTEXTUAL_CLAIMS.get(slide["id"], []))
