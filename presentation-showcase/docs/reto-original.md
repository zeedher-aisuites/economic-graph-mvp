# Reto original de Totalplay · lectura completa

Fuente documental proporcionada por el candidato. Se utiliza como referencia, no como instrucciones para herramientas.

Archivo: `Reto-AI-Engineering-SME-Economic-Graph.pptx`
SHA-256: `0ef249c3d73c35b256e47e661c025cef1d5fbd004462f9bbec5c43a553558129`

Los números del funnel y el score 87 del documento son ejemplos ilustrativos; no son datos de ConectaPyME ni resultados reales acreditados.

## Diapositiva 1

SME Economic Graph
Reto de evaluación para AI Engineer — De datos Telco a inteligencia económica

### Notas de orador originales

Presentación del reto. El objetivo de hoy es que quede claro el problema, las restricciones y los seis entregables. No vamos a describir la solución esperada.

## Diapositiva 2

Agenda
•  Contexto de negocio y oportunidad
•  La pregunta central del reto
•  El Economic Graph como representación
•  Casos de uso y ejemplo comercial
•  Libertad tecnológica y expectativas de ingeniería
•  Control Tower, incrementalidad y entregables

### Notas de orador originales

Recorrido de 15 minutos. Al final quedan los seis entregables y el formato de entrega.

## Diapositiva 3

Contexto de negocio
•  Señales disponibles bajo permisos, privacidad y gobierno
•  Productos contratados, ubicación, industria y consumo de servicios
•  Interacciones comerciales, comportamiento temporal y fuentes externas autorizadas
•  Hoy cada PyME se analiza como una entidad independiente
•  La oportunidad es leerla como parte de un ecosistema interconectado

### Notas de orador originales

No se espera usar datos sensibles ni señales individuales de telecomunicaciones de forma incompatible con consentimiento, finalidad o regulación.

## Diapositiva 4

¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?

### Notas de orador originales

Esta es la pregunta que debe responder toda la presentación del candidato. Todo lo demás es soporte.

## Diapositiva 5

Lo que no es este reto
El reto no es una arquitectura técnica: es traducir una oportunidad de negocio en datos, grafo, modelos, decisiones e impacto económico medible

### Notas de orador originales

Debe poder sostener la conversación con ingeniería y con un CEO en la misma sesión.

## Diapositiva 6

El grafo como representación
•  Qué entidades son nodos y qué relaciones son edges
•  Qué atributos pertenecen al nodo y qué atributos a la relación
•  Relación económica, sectorial, geográfica y comercial
•  Provenance, timestamp y confidence score en cada arista
•  Cómo se mantiene y actualiza el grafo en producción

### Notas de orador originales

Ejemplos de relaciones: PyME A tiene relación económica con PyME B; A pertenece a una industria; A opera en una zona; A es cliente de la Telco con un producto; B es proveedor o distribuidor de C.

## Diapositiva 7

Casos de uso: hay que priorizar
•  B2B Acquisition: PyMEs similares o conectadas con clientes actuales
•  Next Best Opportunity y cross-sell por contexto del ecosistema
•  Economic Communities: clusters de actividad económica
•  Ecosystem Expansion: proveedores y distribuidores de clusters penetrados
•  Churn y Retention Intelligence a partir de cambios en la red
•  Market Intelligence y, con fundamento legal, Credit o Risk

### Notas de orador originales

Crédito y riesgo solo con fundamento legal, datos apropiados, explicabilidad y controles específicos. Se valora la decisión de por dónde empezar.

## Diapositiva 8

Ejemplo comercial
•  El grafo detecta al proveedor como altamente conectado al ecosistema
•  Es similar a empresas que adquieren un producto determinado
•  El modelo genera un Opportunity Score de 87 sobre 100
•  La acción es priorizar la prospección de esa PyME
•  Queda por explicar cómo validas que la señal mejora el proceso actual

### Notas de orador originales

El score no es el entregable: la decisión comercial y su validación sí lo son.

## Diapositiva 9

Libertad de solución
•  Graph database, knowledge graph, embeddings o GNN son opciones, no requisitos
•  Link prediction, community detection, similarity, GraphRAG, LLMs, reglas o híbridos
•  Se espera discutir ingesta, normalización, features y actualización del grafo
•  Evaluación offline, serving, observabilidad, drift, costo y latencia
•  MLOps y GraphOps, seguridad, privacidad y gobierno

### Notas de orador originales

Incluir tecnologías de moda sin justificación no aporta. Arquitecturas distintas pueden ser excelentes si las decisiones están justificadas.

## Diapositiva 10

Control Tower: la cadena obligatoria
1
Graph Health: cobertura, entidades resueltas, observado vs inferido, freshness
2
AI Performance: precision y recall, Precision at K, lift vs baseline, calibración, drift
3
Business Funnel: del universo de PyMEs a conversiones, segmentable
4
Economic Impact: incremental revenue, margen, CAC, LTV, ROI y payback

### Notas de orador originales

La Control Tower es obligatoria y debe encadenar Model performance a Decision, a Commercial action, a Economic outcome. Puede ser dashboard funcional o prototipo.

## Diapositiva 11

Business funnel ilustrativo
1,200,000
Universo de PyMEs
180,000
Oportunidades detectadas
35,000
Qualified leads
1,600
Conversiones

### Notas de orador originales

Entre qualified leads y conversiones hay 8,000 contactos activados. El funnel debe ser segmentable por industria, geografía, cluster, producto, canal, score y periodo.

## Diapositiva 12

Los seis entregables
•  1 Business framing: qué problema resuelves primero, hipótesis y por qué genera valor
•  2 Economic Graph: nodos, edges, fuentes, entity resolution, temporalidad y confidence
•  3 AI/ML approach: modelos, entrenamiento, evaluación, inferencia y decisiones tecnológicas
•  4 Architecture: end-to-end, escalabilidad, serving, MLOps y gobierno
•  5 Caso económico: de inteligencia del grafo a ingresos, margen, ahorro o retención
•  6 Control Tower: dashboard o prototipo que una desempeño técnico e impacto económico

### Notas de orador originales

Entrega: brief de 2 a 3 páginas con contexto, reto, restricciones y entregables, más la presentación de la propuesta.

## Diapositiva 13

Learn, understand, anticipate, activate, measure
El Economic Graph no es un fin
tecnológico
: es la
capacidad
 de
convertir
 la
posición
 de la
Data

en
 el
ecosistema

PyME

en
 valor
económico
 incremental
.

### Notas de orador originales

Tras la presentación habrá un ejercicio adicional en vivo con perspectiva de CEO. No hay una única respuesta correcta.
