## Diapositiva 1

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Economic Graph para adquisición B2B
Qué construí, qué cambia en la decisión comercial y qué falta para demostrar valor incremental.
Fuente: reto original, diap. 4 y 12 · PoC sintética · commit principal 774dacd
01
DISEÑO
Una decisión comercial más informada,
no un grafo por el grafo.
Evidencia técnica
Construcción y ranking reproducibles.
Evidencia económica
Todavía requiere un ensayo real.

### Notas originales

Buenas tardes. Soy el candidato que desarrolló ConectaPyME, una prueba de concepto para responder al reto de construir un Economic Graph de pequeñas y medianas empresas para una Telco. Quiero organizar la presentación alrededor de tres preguntas: qué construí, qué decisión comercial modifica el grafo y qué tendríamos que medir para demostrar valor económico incremental. Desde el inicio hago una distinción: el prototipo utiliza datos sintéticos y sus resultados técnicos son reproducibles, pero no tenemos ventas reales ni un efecto causal medido. Mi objetivo fue construir una respuesta que pudiera explicar y auditar, no simplemente mostrar una visualización atractiva.

## Diapositiva 2

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
El reto exige seis entregables
No solo arquitectura: problema, información, decisión, resultado y medición.
Fuente: Reto-AI-Engineering-SME-Economic-Graph.pptx · diapositivas 5, 10–12
02
CONSTRUIDO
01
Business Framing
02
Economic Graph
03
AI/ML Approach
04
Architecture
05
Economic Case
06
Control Tower
La evaluación clave: ¿cómo demostraríamos margen neto incremental, no solo rankings distintos?

### Notas originales

Organicé la respuesta en los seis entregables que solicita el reto: planteamiento del problema, diseño del grafo económico, enfoque analítico o de inteligencia artificial, arquitectura, caso económico y Control Tower. Para mí, estos componentes forman una sola historia. Primero definimos qué decisión necesita tomar el negocio; luego reunimos evidencia sobre empresas y sus conexiones; utilizamos esa información para generar una priorización; y finalmente planteamos cómo comprobar si cambiar la priorización realmente mejora el margen. La parte más importante no es producir una lista distinta, sino proponer una forma defendible de medir su impacto.

## Diapositiva 3

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Problema de negocio: priorización B2B
Capacidad comercial limitada frente a múltiples cuentas posibles: decidir a quién investigar primero.
Fuente: docs/01-product-brief.md · docs/02-challenge-traceability.md
03
HIPÓTESIS
Situación
Las señales de cada PyME pueden ser incompletas y cambiar con el tiempo.
Decisión
Ordenar cuentas con un baseline y otra política enriquecida con relaciones.
Resultado esperado
Mejor uso de la capacidad comercial y margen neto potencial.
FALTA: línea base, costos, restricciones y validación del problema en una Telco real.

### Notas originales

El problema que elegí es la adquisición B2B cuando la capacidad del equipo comercial es limitada. Supongamos que hay más cuentas por explorar que tiempo para analizarlas. La decisión inmediata es cuáles investigar primero y por qué. El supuesto de esta prueba es que las relaciones económicas entre empresas podrían aportar señales útiles que no aparecen en los atributos individuales. Lo planteo como una hipótesis, no como un problema que ya haya medido en Totalplay. Para demostrar su relevancia comercial necesitaríamos conocer el proceso vigente, los costos, los recursos disponibles y la línea base real de conversiones.

## Diapositiva 4

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Dos laboratorios, una misma pregunta empresarial
El diagnóstico operativo y el grafo son simulaciones distintas; sus empresas y cifras no se mezclan.
Fuentes: presentación integrada anterior · docs/02-challenge-traceability.md
04
DISEÑO
Contexto consultivo · CRM simulado
240 leads ficticios; 181 contactos; 103 calificados; 44 propuestas; 16 cierres.
No son datos observados de Totalplay.
PoC técnica · Economic Graph
30 PyMEs ficticias en el simulador; 83 observaciones; cortes temporales; ranking de cinco cuentas.
No contiene resultados comerciales.
DECISIÓN EDITORIAL: este diagnóstico puede pasar a anexo o desaparecer del brief.

### Notas originales

Aquí quiero aclarar una separación importante. Durante la preparación también exploré un diagnóstico comercial con un CRM ficticio de 240 prospectos. Esa simulación sirve para ilustrar fricciones operativas en ventas y marketing. Pero no es la misma muestra ni la fuente de datos del Economic Graph: el grafo parte de un universo sintético de 30 empresas y observaciones propias. No mezclé sus cifras para producir rankings, ingresos o conclusiones. Incluí esta comparación porque refleja dos maneras distintas de analizar adquisición B2B: mejorar el proceso comercial, por un lado, y enriquecer la información para priorizar, por otro. En un brief final, esta sección puede reducirse o trasladarse a un anexo.

## Diapositiva 5

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Qué aprendemos del diagnóstico CRM sintético
Hay señales de fricción operativa que conviene investigar antes de prometer impacto de un grafo.
Fuente: ConectaPyME_Defensa_Integral_Lista_Para_Presentar.pptx, slides 7–24
05
HIPÓTESIS
240
Leads simulados
100/181
Contactos después de 24 h
16
Cierres simulados
Lectura ejecutiva
Diagnóstico de procesos ≠ causalidad del Economic Graph; no se atribuyen pérdidas a demoras sin medirlas.

### Notas originales

En el ejercicio independiente de CRM aparecen 240 leads ficticios, de los que 181 están marcados como contactados y 16 como cierres. Además, 100 de esos 181 contactos ocurrieron después de 24 horas, según las reglas de generación de la simulación. Es tentador concluir que la demora causó oportunidades perdidas, pero esos datos no permiten establecerlo. Lo que sí muestran es qué preguntas formularía en un diagnóstico real: tiempos de atención, responsable, capacidad y calidad del registro. Mantengo este caso separado porque no quiero utilizar una simulación operativa como supuesta prueba de que el Economic Graph funciona mejor.

## Diapositiva 6

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Qué es nuestro Economic Graph
No es una lista de empresas: añade vínculos económicos con dirección, procedencia y fecha.
Fuente: docs/06-economic-graph-design.md · docs/10-design-validation.md
06
DEMOSTRADO
Nodos
PyMEs conocidas y atributos observados por corte.
Aristas
SUPPLIES_TO, PARTNERS_WITH y vínculos de referencia diferenciados.
Evidencia
Confirmada, reportada, inferida o descartada, con fuente y fechas.
La verdad completa del simulador permanece separada del conocimiento observable.

### Notas originales

Para mí, un Economic Graph no es solamente un conjunto de nombres unido por líneas. Cada nodo representa una PyME conocida y cada vínculo representa una afirmación económica con significado, dirección, fuente y fecha. Por ejemplo, una empresa puede suministrar a otra, colaborar con ella o referirla. También importa el nivel de verificación: una afirmación reportada no equivale a una relación confirmada. En la simulación mantuve separada la verdad completa del mundo ficticio de lo que un analista habría podido observar. Esa separación es esencial para no construir una demostración que ya conoce de antemano todas las respuestas.

## Diapositiva 7

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
El conocimiento crece, pero nunca debe viajar al futuro
T0, T1 y T2 reconstruyen qué información estaba disponible en cada fecha de corte.
Fuente: docs/09-observability-plan.md · docs/02-challenge-traceability.md
07
DEMOSTRADO
T0 · Ene
12
T1 · May
17
T2 · Sep
23
Observaciones acumuladas: 28 → 54 → 83     |     Afirmaciones económicas: 2 → 13 → 26
Solo se consultan datos cuyo available_at es anterior o igual al corte; siete PyMEs nunca se descubren.

### Notas originales

Este gráfico resume una decisión técnica central: evitar la fuga de información del futuro. Definí tres fechas de corte, T0 en enero, T1 en mayo y T2 en septiembre de 2026. Al principio solo se conocen 12 empresas; después 17 y finalmente 23. Las observaciones acumuladas crecen de 28 a 54 y luego a 83. El sistema consulta únicamente información que ya estaba disponible en cada fecha. Por eso, aunque el simulador conoce 30 empresas, siete permanecen desconocidas al último corte. Esta es una prueba de consistencia temporal, no una afirmación sobre cuántas empresas conocería una Telco real.

## Diapositiva 8

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
La incertidumbre no se esconde
Una relación mencionada no equivale a una relación confirmada.
Fuente: docs/10-design-validation.md · docs/17-control-tower-design.md
08
DEMOSTRADO
26
Afirmaciones económicas T2
2
Identidades candidatas
2
Atributos en conflicto
Regla de confiabilidad
Se conservan fuentes, conflictos y candidatos; no se fuerzan fusiones ni se inventa certeza.

### Notas originales

En datos comerciales reales es común encontrar fuentes incompletas o contradictorias. No quise resolver artificialmente esos problemas para hacer más atractivo el resultado. En el corte T2 hay 26 afirmaciones económicas observables, dos posibles identidades equivalentes pendientes de revisión y dos atributos en conflicto. La aplicación conserva esas situaciones, junto con su procedencia, en lugar de convertirlas automáticamente en datos confirmados. Esta postura también tiene un costo: a veces sabemos menos y asignamos menos puntos. Me parece preferible a introducir certeza que no podemos justificar, especialmente si después una persona tomará una decisión de ventas a partir de esa información.

## Diapositiva 9

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
De la evidencia al ranking comercial
Misma cohorte elegible, la misma capacidad y dos políticas explícitas.
Fuente: docs/12-commercial-ranking.md · docs/13-ranking-comparison.md
09
DEMOSTRADO
BASELINE
10 puntos por sucursal adicional observable sin conflicto; máximo cinco sucursales adicionales.
CON GRAFO
Baseline + 5 puntos por vecino económico confirmado distinto, máximo cuatro vecinos.
K = 5 por corte. Reportadas, inferidas y referencias no suman. Score ≠ probabilidad.

### Notas originales

Una vez construido el conocimiento observable, comparé dos políticas sobre la misma cohorte y con una capacidad fija de cinco cuentas. El baseline asigna diez puntos por cada sucursal adicional observada sin conflicto, hasta un límite. La política enriquecida conserva esa misma base y suma cinco puntos por cada vecino económico distinto y confirmado que cumple los criterios, también con un límite. Las relaciones reportadas, inferidas o de referencia no aumentan el score. Elegí reglas deliberadamente simples para hacer visible qué aportó el grafo. El puntaje es un criterio de ordenamiento exploratorio, no una probabilidad de compra.

## Diapositiva 10

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Resultado demostrable: tres cuentas cambian
La señal relacional cambia a quién investigaríamos primero; no demuestra mayor conversión.
Fuente: docs/13-ranking-comparison.md · T2; reglas exploratorias aprobadas
10
DEMOSTRADO
5
Plazas disponibles
2
Cuentas coincidentes
3
Sustituciones en el top-5
Conclusión permitida
La política con grafo produce una selección distinta usando información relacional confirmada.

### Notas originales

Éste es uno de los principales resultados que sí puedo demostrar. En el corte T2, ambas políticas tienen cinco plazas disponibles. Coinciden en dos cuentas, pero las otras tres cambian cuando añadimos relaciones económicas confirmadas. Eso demuestra que el grafo altera la selección bajo las reglas establecidas. Lo que todavía no demuestra es que las tres cuentas nuevas sean mejores clientes, que vayan a comprar o que generen mayor margen. Precisamente por esa diferencia separé el resultado técnico de la hipótesis económica: cambiar una decisión es una condición que podemos observar, pero su valor requiere medir consecuencias comerciales.

## Diapositiva 11

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Caso auditable: Café Jacaranda
Un ejemplo de por qué cambió la decisión, sustentado por dos relaciones confirmadas.
Fuente: docs/13-ranking-comparison.md · docs/18-control-tower-demo.md
11
DEMOSTRADO
Sin grafo
Posición 10
Puntuación 0
Con grafo
Posición 3
Puntuación 10
Dos vecinos económicos confirmados utilizables; no representan intención de compra.

### Notas originales

Para no quedarme en una comparación abstracta, preparé un caso auditable: Café Jacaranda. Con el baseline ocupa la posición diez y obtiene cero puntos; al incorporar información relacional confirmada sube a la posición tres con diez puntos. Ese cambio proviene de dos vecinos económicos distintos que cumplen la regla aprobada y cuyas observaciones pueden inspeccionarse en la Control Tower. Puedo mostrar de dónde provienen, cuándo estuvieron disponibles y por qué sumaron puntos. Esto permite explicar el resultado sin decir que el negocio tiene intención de comprar. La trazabilidad explica la decisión del algoritmo, no anticipa una venta.

## Diapositiva 12

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Por qué reglas antes que machine learning
Sin etiquetas de conversión, entrenar ML puede aparentar precisión que aún no podemos verificar.
Fuente: docs/12-commercial-ranking.md · reto, diapositiva 9
12
DISEÑO
Lo implementado
Reglas interpretables, pesos exploratorios, desempates, no fuga temporal y pruebas de regresión.
Lo que exigiría ML
Etiquetas, resultados comerciales, división temporal, evaluación predictiva, monitoreo y comparación válida.
No hay GNN, link prediction entrenado, precision@K comercial ni lift predictivo observado.

### Notas originales

Podría haber intentado entrenar un modelo de machine learning o incluso una red neuronal de grafos, pero no habría sido una elección sólida con estos datos. No contamos con etiquetas reales de conversión o margen, y una muestra sintética tan pequeña no permite validar capacidad predictiva. Por eso elegí un baseline y reglas explícitas que se pueden probar, comparar y auditar. Si el caso avanzara, entonces sí propondría reunir resultados comerciales con fechas, evitar fuga temporal, definir métricas predictivas apropiadas y comparar un modelo entrenado contra esta referencia. No digo que las reglas sean superiores al machine learning; digo que son la opción más justificable en esta etapa.

## Diapositiva 13

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Arquitectura: pequeña pero auditable
El código separa simulación, conocimiento observable, lógica comercial y presentación.
Fuente: docs/04-architecture-overview.md · README · src/economic_graph/
13
DEMOSTRADO
01
Diseño sintético
→
02
Ledger observable
→
03
Python + reglas
→
04
Atlas opcional
→
05
Streamlit
No se presenta como arquitectura productiva ni como un sistema autónomo de ventas.

### Notas originales

La arquitectura responde a esa necesidad de trazabilidad sin presentarse como lista para producción. Separé el diseño sintético restringido del registro observable, la lógica de consultas temporales, las políticas de ranking, el cálculo financiero y la presentación. MongoDB Atlas funciona como persistencia opcional de las observaciones; el prototipo también opera offline para que un evaluador pueda reproducirlo sin credenciales. En Python mantuve funciones relativamente pequeñas y pruebas sobre los invariantes principales. No afirmo haber resuelto aquí autenticación empresarial, escalamiento, alta disponibilidad ni gobierno de datos de una Telco: esos puntos pertenecerían a una fase posterior.

## Diapositiva 14

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Conocía el camino mínimo: decidí explorar más
La complejidad adicional fue una decisión de aprendizaje y trazabilidad, no un requisito comercial.
Fuente: reflexión metodológica del autor · alcance real verificado en README y docs/
14
DISEÑO
Camino mínimo
CSV + Python + reporte HTML
Grafo pequeño, dos rankings y fórmula económica. Menor costo y entrega rápida.
Camino elegido · ConectaPyME
Python + MongoDB + Streamlit
Procedencia, incertidumbre, cortes temporales, pruebas y auditoría de decisiones.
Para un piloto real, elegiría la solución más simple que permita medir bien el impacto.

### Notas originales

Quiero detenerme un momento en una decisión personal de ingeniería. Era posible contestar este reto con una solución mucho más simple: unos CSV, un script de Python, dos rankings y un HTML. Eso habría sido razonable para validar la idea básica. Yo elegí ampliar el prototipo para explorar problemas que me interesan especialmente: fuentes que se contradicen, datos que aparecen en momentos distintos, decisiones que deben justificarse y pruebas que permitan repetir el resultado. Esa forma de trabajar —construir, experimentar, documentar y mejorar— es la que disfruto. No creo que más complejidad sea siempre mejor; si mañana iniciara un piloto comercial, comenzaría con la solución más pequeña que permita medir bien el efecto.

## Diapositiva 15

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Control Tower: una cadena visible, no una promesa de ventas
La herramienta conecta datos → ranking → priorización → hipótesis económica.
Fuente: docs/17-control-tower-design.md · docs/18-control-tower-demo.md
15
DEMOSTRADO
Graph Health
Calidad y fuentes
AI Performance
Dos rankings
Business Funnel
23 → 21 → 5
Economic Impact
Escenarios
Más una quinta vista de Resumen. No se ejecutan contactos ni campañas.

### Notas originales

La Control Tower es la manera de recorrer todo el análisis sin abrir scripts durante una presentación. Incluye cinco vistas: un resumen ejecutivo y cuatro dimensiones principales. Graph Health muestra qué información existe y qué tan respaldada está; AI Performance compara las dos políticas; Business Funnel muestra la selección comercial disponible; y Economic Impact permite examinar escenarios financieros. La interfaz no ejecuta campañas, no contacta clientes ni convierte las hipótesis en ventas. Su propósito es reunir el razonamiento y permitir inspeccionar la evidencia detrás de cada cifra y de cada decisión.

## Diapositiva 16

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Business Funnel: hasta dónde llega la evidencia
Priorizadas no significa contactadas; los resultados comerciales posteriores no existen en el dataset.
Fuente: docs/18-control-tower-demo.md · T2 global
16
DEMOSTRADO
23
Conocidas
21
Elegibles
5
Priorizadas
Contactos · oportunidades · activaciones · ventas: NO OBSERVADO
Dos exclusiones se muestran aparte; el filtro comercial no altera las posiciones globales.

### Notas originales

Este embudo ilustra con mucha claridad el alcance real de la prueba. En T2 hay 23 empresas conocidas, 21 elegibles con la política definida y cinco priorizadas. Las dos exclusiones se muestran aparte. Después de ese punto, el tablero no inventa conversiones: contactos, oportunidades, activaciones y ventas aparecen como no observados. Esa expresión importa, porque no equivale a decir que hubo cero ventas; simplemente no existe un registro comercial con el cual medirlas. La utilidad de este módulo es hacer visible dónde termina el prototipo de priorización y dónde tendría que comenzar el sistema comercial y la recolección de resultados.

## Diapositiva 17

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Validación técnica: qué sí funciona
Pruebas offline y conexión Atlas comprobada desde la versión integrada.
Fuente: reporte local de usuario · docs/11-atlas-integration-validation.md
17
DEMOSTRADO
284
Pruebas seleccionadas aprobadas
83
Observaciones leídas en Atlas T2
5
Vistas Streamlit funcionales
Límite de prueba
Una integración se excluyó de pytest; ping/lectura Atlas y UI son verificaciones locales separadas.

### Notas originales

También quise comprobar que la implementación funciona de forma repetible. Sobre la versión integrada se ejecutaron 284 pruebas automatizadas seleccionadas, sin fallos, y las comprobaciones de estilo terminaron correctamente. Una prueba de integración quedó excluida de esa suite. De manera separada, desde mi entorno Windows confirmé que MongoDB Atlas respondía al ping, que podía leer 83 observaciones en T2 y que las cinco vistas funcionaban, incluida la lectura de Atlas en modo solo lectura. Es evidencia de funcionamiento técnico local. No debe confundirse con pruebas de rendimiento a escala, producción o validación de resultados de negocio.

## Diapositiva 18

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
El valor económico se decide en el contrafactual
No basta con que el grafo produzca una lista distinta: debe superar al baseline después de costos.
Fuente: docs/14-incremental-economic-case.md · docs/15-incrementality-experiment.md
18
DISEÑO
Margen incremental neto = beneficio adicional atribuible − costos incrementales de construir y operar el grafo
Sin contrafactual real, el caso financiero es un ejercicio de umbrales, no una medición de ROI.

### Notas originales

Llegamos a la pregunta más importante del reto: ¿cómo demostrar valor económico incremental? La comparación de rankings, por sí sola, no responde eso. Para atribuir valor necesitamos un contrafactual: qué habría pasado con la misma población y recursos si hubiéramos usado la política sin grafo. El resultado que nos interesa es la diferencia de margen de contribución neto, después de incluir el costo incremental de construir y operar la solución. Los cálculos actuales modelan escenarios para pensar en la decisión de inversión, pero no son un ROI observado ni una estimación causal. Esta distinción guía tanto la simulación financiera como el experimento que propongo.

## Diapositiva 19

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Escenarios: el tamaño cambia la viabilidad
El calculador permite analizar supuestos, incluidas pérdidas; no contiene ventas reales.
Fuente: docs/16-financial-calculation.md · config/financial_assumptions.json
19
HIPÓTESIS
5 plazas · demostración
Caso base neto: −$15,450 MXN
La escala pequeña no cubre los costos fijos.
500 plazas · hipotético
Caso base neto: +$39,000 MXN
Antes de la reserva del escenario.
Escenario nulo a 500 plazas: −$41,000 MXN. Ninguno de los dos es resultado observado.

### Notas originales

Probé el caso económico con dos escalas muy diferentes para evidenciar el peso de los costos fijos. Con solo cinco plazas de demostración, el escenario base arroja una pérdida hipotética de quince mil cuatrocientos cincuenta pesos. Si supongo quinientas plazas, manteniendo los parámetros del escenario base, el saldo calculado pasa a más treinta y nueve mil pesos antes de considerar la reserva por separado. Pero si no hay mejora de activación, el escenario nulo para quinientas plazas es negativo en cuarenta y un mil pesos. Ninguna de estas cantidades proviene de contratos reales: son resultados aritméticos de supuestos declarados que todavía tendrían que calibrarse.

## Diapositiva 20

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
¿Cuánto tendría que mejorar la conversión?
En el escenario base de 500 plazas, el break-even es un requisito económico, no un logro.
Fuente: docs/16-financial-calculation.md · supuesto financiero 003b-finance-v1
20
HIPÓTESIS
1.025 pp
Uplift requerido sin reserva
1.105 pp
Uplift requerido con reserva
2.0 pp
Uplift supuesto en caso base
Para calcular el uplift real faltan conversiones comparables, costos calibrados y seguimiento.

### Notas originales

La pregunta económica se vuelve más útil cuando la transformamos en un umbral. Bajo el escenario base hipotético de quinientas plazas, la mejora absoluta de conversión necesaria para cubrir costos es de 1.025 puntos porcentuales sin reserva, o 1.105 puntos si se considera la reserva. El escenario base supone una mejora de dos puntos porcentuales; no significa que la hayamos conseguido. Para medir esa mejora necesitaríamos activaciones verificables, costos completos, un horizonte de seguimiento y grupos comparables. Utilizo los puntos de equilibrio para mostrar qué tendría que ser cierto para justificar la inversión, no para afirmar que ya se justificó.

## Diapositiva 21

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Cómo demostraríamos causalidad: ensayo por bolsas
Misma capacidad; control baseline vs. tratamiento con grafo; evaluación por intención de tratar.
Fuente: docs/15-incrementality-experiment.md
21
DISEÑO
CONTROL
Cuentas elegibles asignadas a política baseline; misma capacidad comercial.
TRATAMIENTO
Cuentas elegibles asignadas a política con grafo; medir también no contactadas.
KPI: margen neto por cuenta elegible asignada. Bolsa = unidad de aleatorización; ensayo NO ejecutado.

### Notas originales

Mi propuesta para medir ese efecto es un ensayo controlado por bolsas de empresas relacionadas, en lugar de asignar empresas conectadas de manera ingenuamente independiente. Dividiríamos las bolsas entre una política baseline y otra con grafo, manteniendo una capacidad comercial comparable. El indicador principal sería margen neto por cada cuenta elegible originalmente asignada, incluyendo las que nunca se contactaron. Esto se conoce como análisis por intención de tratar y ayuda a evitar que solo evaluemos los éxitos. El ensayo requeriría suficientes bolsas independientes, datos comerciales autorizados, seguimiento temporal y una estimación válida de incertidumbre. No lo ejecuté; presento el diseño para una etapa real de validación.

## Diapositiva 22

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
La evidencia que realmente falta
Distinguir vacíos que impiden la medición causal de mejoras cosméticas de la presentación.
Fuente: docs/02-challenge-traceability.md · docs/15-incrementality-experiment.md
22
PENDIENTE
Para validar el negocio
Clientes y permisos; baseline real; activaciones, contratos y costos; suficientes bolsas; variabilidad e ICC.
Para cerrar la candidatura
Brief de 2–3 páginas; depurar estados históricos; revisar deck; guion de cinco minutos.
No corresponde completar estos vacíos fabricando datos o llamando causal a un cambio de ranking.

### Notas originales

Esta diapositiva separa dos clases de pendientes. Para validar el negocio faltan fuentes autorizadas, definición de la política comercial vigente, registros confiables de contratos y activaciones, costos calibrados y suficientes unidades independientes para un experimento. Esas brechas no se resuelven escribiendo más código o inventando ventas. En cambio, para cerrar esta candidatura faltan tareas editoriales: consolidar el brief, limpiar estados históricos de algunos documentos y preparar una defensa breve. Me interesa hacer esta separación porque el prototipo está construido; la evidencia de impacto real solo podrá obtenerse con participación de una organización y una prueba controlada.

## Diapositiva 23

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Qué llevar al brief de 2–3 páginas
La reducción no es resumir todas las diapositivas: es preservar decisiones y evidencia esencial.
Fuente: síntesis editorial basada en el reto y la auditoría 005C
23
DISEÑO
PÁGINA 1
Problema y elección de enfoque.
Economic Graph.
Decisión consciente de diseño.
PÁGINA 2
Qué construimos.
T2: 23/21/5.
Tres cambios y caso Café.
Control Tower.
PÁGINA 3
Valor incremental.
Escenarios y A/B futuro.
Brechas, riesgos y próxima decisión.

### Notas originales

Con toda esta evidencia disponible, mi propuesta es que el brief ejecutivo no intente contener el detalle de cada módulo. En la primera página pondría el problema, la hipótesis y la decisión consciente de enfoque; en la segunda, qué construí y qué resultado técnico obtuve, incluyendo el caso de Café Jacaranda y la Control Tower; y en la tercera, cómo evaluaría el valor incremental, qué dicen los escenarios hipotéticos y qué falta para recomendar una inversión. El código, las pruebas, la arquitectura detallada y los supuestos completos quedarían como anexos reproducibles en GitHub. Así el lector obtiene primero la decisión y luego el respaldo.

## Diapositiva 24

CONECTAPYME   /   EVALUACIÓN AI ENGINEER
Decisión ejecutiva: no desplegar todavía
La ingeniería es verificable; la rentabilidad solo podrá juzgarse con datos y experimento autorizados.
Fuentes: docs/02-challenge-traceability.md · docs/15-incrementality-experiment.md
24
DISEÑO
Sí podemos afirmar
Los cortes, conflictos, rankings, cálculos y vistas son reproducibles.
La política con grafo cambia 3/5 decisiones.
No podemos afirmar
Que aumenten las ventas.
Que haya ROI real.
Que sea un sistema productivo listo para operar.
Siguiente paso: validar datos, costes y factibilidad de un piloto controlado; luego decidir.

### Notas originales

Mi conclusión no es que una Telco deba desplegar hoy este sistema. Lo que sí puedo defender es que construí un Economic Graph sintético auditable, reconstruí lo conocido en fechas distintas, comparé dos reglas de priorización y mostré un cambio de tres de las cinco cuentas seleccionadas. También desarrollé una interfaz funcional y un calculador que hace explícitas las condiciones económicas. Lo que no puedo afirmar son nuevas ventas o ROI real. Mi recomendación sería validar primero la viabilidad de los datos, la operación comercial y un piloto controlado con evaluación de margen neto. Creo que una buena solución de ingeniería también debe indicar con claridad cuándo todavía no tenemos evidencia suficiente para decidir.