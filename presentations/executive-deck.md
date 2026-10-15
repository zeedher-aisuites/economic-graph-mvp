# ConectaPyME Economic Intelligence

Fuente editable de la única presentación ejecutiva principal. Estructura inicial de 12 diapositivas; **no constituye la defensa final ni contiene resultados de negocio**. Los títulos en inglés conservan la nomenclatura de los seis entregables del reto; el contenido se comunica en español.

## 1. Pregunta central y propuesta de trabajo

¿Cómo construir un Economic Graph de PyMEs para una Telco y demostrar valor económico incremental?

Proponemos una PoC pequeña para explorar decisiones comerciales explicables y un diseño experimental para medir su impacto real. Caso ficticio: ConectaPyME Telecom.

Fuente: `../docs/00-project-context.md`; reto, diapositiva 4. Estado: alcance aprobado; demostración pendiente.

## 2. Business Framing — priorizar adquisición B2B

El analista necesita decidir qué cuentas explorar primero y por qué. La hipótesis es aprovechar señales relacionales para emplear mejor la capacidad comercial. Contactar o descartar sigue siendo una decisión humana.

Pendiente: línea base, restricciones operativas y evidencia del problema en una Telco real.

Fuente: `../docs/01-product-brief.md`, secciones 1–4.

## 3. Economic Graph — qué conectaremos

El MVP aprobado contempla 30 empresas ficticias y relaciones con significado explícito. La cercanía geográfica no demuestra una transacción.

Pendiente: entidades y relaciones concretas, atributos y consultas que respondan al caso de adquisición. No se generaron datos en misión 001.

Fuente: `../docs/03-scope-and-decisions.md`, P-001; reto, diapositiva 6.

## 4. Economic Graph — por qué confiar en una señal

Cada relación deberá explicar fuente, fecha de conocimiento, vigencia y confianza. La vista observable por la Telco debe estar separada de la verdad del simulador.

Pendiente: diseño de identidad, procedencia y controles temporales; fuentes reales requerirían autorización y gobierno.

Fuente: `../docs/04-architecture-overview.md`, secciones 3–4.

## 5. AI/ML Approach — comparación comprensible

Compararemos un baseline empresarial con una variante que agregue señales del grafo. Una relación no prueba intención de compra. Un modelo entrenado no es requisito para la PoC.

Pendiente: variables, reglas, corte temporal, métricas y explicaciones. No existe scoring implementado ni precisión medida.

Fuente: `../docs/02-challenge-traceability.md`, bloque 3; reto, diapositiva 9.

## 6. Architecture — base técnica y flujo futuro

Base implementada: configuración local → cliente PyMongo → `ping` sin escrituras; dependencias bloqueadas y pruebas unitarias sin servidor.

Flujo propuesto: generación sintética → persistencia → consultas → señales → comparación → evidencia. Estas etapas están pendientes. La selección de MongoDB no aprueba un modelo de colecciones ni demuestra consultas de grafo.

Fuente: `../docs/04-architecture-overview.md`; `decision-log.md`, DEC-001.

## 7. Architecture — criterios para producción

Ingestión autorizada, resolución de identidad, actualización, serving, observabilidad, seguridad, privacidad y gobierno serían necesarios a escala. MLOps solo si se incorpora un modelo entrenado; GraphOps debe abordar mantenimiento y calidad del grafo.

Pendiente: volúmenes, costos, latencias objetivo y decisiones de escalabilidad. No hay despliegue productivo.

Fuente: `../docs/04-architecture-overview.md`, secciones 6–8; reto, diapositiva 9.

## 8. Economic Case — mecanismo de valor

Hipótesis: mejores señales → mejor priorización → uso más eficiente del esfuerzo comercial → mayor margen potencial.

Marco orientativo: valor incremental neto = margen tratado − margen contrafactual estimado − costo incremental de la solución. Deben fijarse unidad, período y normalización antes de calcular.

Pendiente: supuestos, costos, márgenes y escenarios. No hay ingresos, ahorro ni ROI propios calculados.

Fuente: `../docs/02-challenge-traceability.md`, bloque 5.

## 9. Economic Case — demostrar incrementalidad

Propuesta: comparar política actual y política enriquecida mediante asignación aleatoria cuando sea viable. Mantener capacidad comparable y considerar contaminación entre empresas conectadas y equipos comerciales.

Pendiente: unidad de asignación, potencia, horizonte, análisis por intención de tratar e incertidumbre. Treinta empresas inventadas no prueban causalidad.

Fuente: `../docs/02-challenge-traceability.md`, diseño futuro de prueba.

## 10. Control Tower — de señal técnica a resultado

Entregable obligatorio como dashboard o prototipo. Cadena: Graph Health → AI Performance → Business Funnel → Economic Impact. Debe conectar desempeño del método, decisión, acción comercial y resultado económico.

Pendiente: definiciones operativas, fuentes, frecuencia y prototipo. Las dimensiones están identificadas; no existen indicadores ejecutados. Sin modelo entrenado, reportar desempeño analítico con los límites correspondientes.

Fuente: reto, diapositiva 10 y notas; `../docs/02-challenge-traceability.md`, bloque 6.

## 11. Control Tower — funnel segmentable y límites

Universo elegible → oportunidades → leads calificados → contactos activados → conversiones. El reto pide segmentación por industria, geografía, cluster, producto, canal, score y período.

Pendiente: factibilidad y definiciones sobre el modelo aprobado. No copiar cifras ilustrativas del reto como resultados del proyecto ni presentar métricas causales a partir de simulación.

Fuente: reto, diapositiva 11 y notas; `../docs/02-challenge-traceability.md`.

## 12. Estado, riesgos y siguiente decisión

La misión 001 prepara la base de desarrollo; no demuestra aún el Economic Graph ni su valor económico. Riesgos centrales: señales no observables, fuga temporal, atribución incorrecta y crecimiento de alcance.

Siguiente decisión propuesta: revisar y aprobar modelo conceptual, fuentes observables y temporalidad antes de generar datos. La entrega final requiere brief de 2–3 páginas y defensa con perspectiva de CEO.

Fuente: `../docs/03-scope-and-decisions.md`, P-001 a P-008; reto, notas de diapositivas 12–13.
