# Comunicación ejecutiva

La pregunta rectora es cómo construir el Economic Graph de PyMEs para una Telco y demostrar valor económico incremental. Cada argumento debe conectar una decisión técnica con una decisión comercial y una forma verificable de medir su resultado.

## Ficha para decisiones importantes

| Elemento | Pregunta para la audiencia ejecutiva |
|---|---|
| Problema empresarial | ¿Qué decisión comercial hoy es difícil y a quién afecta? |
| Beneficio esperado | ¿Qué mecanismo podría mejorar adquisición, margen o esfuerzo comercial? |
| Costo y complejidad | ¿Qué necesitamos construir, operar y mantener? ¿Qué dejamos fuera? |
| Riesgos | ¿Qué puede fallar en datos, privacidad, adopción, atribución o costo? |
| Alternativas | ¿Qué opción más simple existe y qué compromisos tiene cada una? |
| Evidencia necesaria | ¿Qué prueba técnica, comparación o experimento permitiría decidir? |
| Impacto potencial | ¿Qué unidad, horizonte, costos y supuestos sostienen la estimación? |

Registrar la ficha en `../presentations/decision-log.md` cuando afecte la arquitectura, el método o el caso económico. No crear una ficha por cada función ni duplicar argumentos completos en varios documentos.

## Reglas del relato

- Una diapositiva comunica una idea principal y remite a su fuente o evidencia.
- Comenzar por el problema y la decisión humana; explicar herramientas solo para justificar costo, viabilidad o riesgos.
- Etiquetar afirmaciones: **implementado y verificado**, **simulado**, **supuesto**, **propuesto** o **pendiente**. Indicar comando y contexto para resultados técnicos.
- Separar capacidad técnica de efecto económico: un `ping` comprueba acceso al servidor, no el valor de un grafo; cambiar un ranking no prueba mayor margen.
- No inventar conversiones, ingresos, precisión, ahorro ni retorno. Las cifras ilustrativas del reto tampoco son resultados propios.
- Comparar contra el proceso actual y considerar costos incrementales. El diseño causal debe explicitar control, unidad de asignación, horizonte, contaminación entre empresas y vendedores e incertidumbre.
- Mantener una sola fuente editable de presentación: `../presentations/executive-deck.md`, organizada por los seis entregables de `02-challenge-traceability.md`.

## Ejemplo aplicable a la misión 001

**Decisión aprobada:** usar Python y PyMongo con dependencias bloqueadas y pruebas sin servidor.

**Explicación al CEO:** primero hacemos reproducible y comprobable la base de la demostración. Su costo y complejidad se limitan a un pequeño paquete y una comprobación de acceso. Todavía no hay datos, señales comerciales ni evidencia de ingresos adicionales. La inversión se justifica como preparación para ensayar el mecanismo, no como ROI demostrado.

## Preguntas que debemos poder defender

¿Por qué el grafo cambia una decisión útil? ¿Qué sabe legítimamente la Telco y cuándo lo sabe? ¿Qué hace mejor que el baseline? ¿Qué cuesta mantenerlo? ¿Cómo separaríamos su efecto del trabajo comercial habitual? ¿Qué evidencia nos haría detener o escalar la inversión?

Las respuestas aún no ejecutadas permanecen pendientes. La entrega final deberá incluir el brief de 2–3 páginas solicitado en las notas del reto y la defensa con perspectiva de CEO.
