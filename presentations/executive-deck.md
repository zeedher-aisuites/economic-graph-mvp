# ConectaPyME Economic Intelligence

Fuente editable de la única presentación ejecutiva principal. Presentación de 12 diapositivas actualizada a la Control Tower local 004B; **no constituye la defensa final ni contiene resultados de negocio observados**. Los títulos en inglés conservan la nomenclatura de los seis entregables del reto; el contenido se comunica en español.

## 1. Pregunta central y propuesta de trabajo

¿Cómo construir un Economic Graph de PyMEs para una Telco y demostrar valor económico incremental?

Proponemos una PoC pequeña para explorar decisiones comerciales explicables y un diseño experimental para medir su impacto real. Caso ficticio: ConectaPyME Telecom.

Fuente: `../docs/00-project-context.md`; reto, diapositiva 4. Estado: alcance aprobado; demostración pendiente.

## 2. Business Framing — priorizar adquisición B2B

El analista necesita decidir qué cuentas explorar primero y por qué. La hipótesis es aprovechar señales relacionales para emplear mejor la capacidad comercial. Contactar o descartar sigue siendo una decisión humana.

Pendiente: línea base, restricciones operativas y evidencia del problema en una Telco real.

Fuente: `../docs/01-product-brief.md`, secciones 1–4.

## 3. Economic Graph — construcción verificable y conocimiento parcial

Diseño aprobado y materializado: universo sintético restringido de 30 empresas y 48 vínculos verdaderos. La Telco solo conoce 12 empresas en T0, 17 en T1 y 23 en T2, a partir de 83 observaciones con fuente, evidencia y disponibilidad.

Las 7 restantes permanecen fuera de la interfaz comercial. Los 2/11/23 vínculos verdaderos observados son cifras de auditoría del simulador; no son relaciones confirmadas ni métricas comerciales.

Fuente: `../docs/10-design-validation.md`; estado: verificado offline con datos ficticios, sin Atlas.

## 4. Economic Graph — qué sabe la Telco y dónde debe desconfiar

El usuario ve afirmaciones y referencias con su estado, fecha y procedencia; no las etiquetas de verdad del simulador. Se preservan dos conflictos de atributos y dos alias candidatos sin fusionar. Un reporte o inferencia no se convierte automáticamente en confirmación.

La construcción oculta los diagnósticos que revelaban falsedad en tres notas y consulta solo datos disponibles al corte. Esto evita usar respuestas del simulador, pero no demuestra que el método detecte por sí solo todas las afirmaciones falsas.

Fuente: `../docs/10-design-validation.md`, DV-001 a DV-005; `decision-log.md`, DEC-005/006. Pendiente: evidencia fuerte para resolver alias y evaluar calidad con datos operacionales autorizados.

## 5. AI/ML Approach — comparación comprensible

Comparamos una regla por sucursales adicionales observadas con esa misma base más vecinos económicos confirmados. El usuario aprobó pesos exploratorios y capacidad de cinco cuentas; se excluyen clientes con servicio activo confirmado y el resto requiere validación comercial.

En los tres cortes, las políticas seleccionan dos cuentas en común y tres distintas. Los reportes muestran contribuciones, evidencia y empates: el baseline atraviesa un empate en las tres selecciones y la variante con grafo en T1/T2. El desempate por ID no tiene significado comercial.

La comparación se ejecutó offline sobre el ledger sintético observable, sin oráculo ni datos posteriores al corte. Pocos atributos están disponibles; los puntos no son probabilidades y una relación no prueba intención de compra. No hay precisión predictiva ni incremento de ventas medidos.

Fuente: `../docs/02-challenge-traceability.md`, bloque 3; `../docs/12-commercial-ranking.md`; `../docs/13-ranking-comparison.md`; `decision-log.md`, DEC-009; reto, diapositiva 9.

## 6. Architecture — del diseño aprobado a la vista observable

Implementado: fuentes ficticias aprobadas y restringidas → auditoría de archivos → proyección unidireccional → ledger público → consultas T0/T1/T2, historia y conflictos. La interfaz comercial no lee el catálogo completo ni completa atributos ausentes.

Carga PyMongo explícita en base dedicada, con dry-run e idempotencia probada offline. En 002C el usuario reportó ping, carga de 83 observaciones, segunda carga sin inserciones y consultas temporales exitosos desde Windows con VS Code. No son ejecuciones de Codex Cloud; roles de acceso y rendimiento productivo siguen sin verificarse. En 003A, una CLI de solo lectura consume el ledger local o MongoDB y deriva rankings; la opción MongoDB de rankings se verifica con un doble, sin nuevas escrituras ni validación real Atlas.

Fuente: `../docs/10-design-validation.md`; `../docs/11-atlas-integration-validation.md` (reporte del usuario); `../docs/12-commercial-ranking.md`; `decision-log.md`, DEC-005/007/008/009.

## 7. Architecture — criterios para producción

Ingestión autorizada, resolución de identidad, actualización, serving, observabilidad, seguridad, privacidad y gobierno serían necesarios a escala. MLOps solo si se incorpora un modelo entrenado; GraphOps debe abordar mantenimiento y calidad del grafo.

Pendiente: volúmenes, costos, latencias objetivo y decisiones de escalabilidad. No hay despliegue productivo.

Fuente: `../docs/04-architecture-overview.md`, secciones 6–8; reto, diapositiva 9.

## 8. Economic Case — mecanismo de valor

Hipótesis: mejores señales → mejor priorización → uso más eficiente del esfuerzo comercial → mayor margen potencial.

Propuesta 003B: a igual capacidad, margen adicional de las cuentas seleccionadas y del resto de la población, menos costo comercial adicional, implantación y operación del grafo. Se consideran adquisición de datos, infraestructura y revisión humana; el punto de equilibrio depende de volumen, margen y diferencia de conversión, no de puntos de score.

ECO-01 a ECO-06 fueron aprobadas provisionalmente solo para la PoC educativa. El calculador muestra conservador, base, optimista, nulo y sensibilidad sin calibración financiera. Con cinco plazas todos pierden; con 500 hipotéticas el caso base da 39 000 MXN y el nulo −41 000 MXN. Son resultados aritméticos de supuestos, sin ventas observadas de Totalplay ni de las 30 PyMEs. La reserva se muestra aparte y ningún saldo positivo autoriza invertir.

Fuente: `../docs/02-challenge-traceability.md`, bloque 5; `../docs/14-incremental-economic-case.md`; `../docs/16-financial-calculation.md`; `decision-log.md`, DEC-010.

## 9. Economic Case — demostrar incrementalidad

Propuesta 003B: asignar bolsas comerciales completas antes de seleccionar cuentas y comparar el baseline aprobado con su variante enriquecida. Igual límite de esfuerzo; medir margen neto por toda cuenta elegible asignada, incluso sin contacto. Las políticas aprobadas no representan una práctica actual de Totalplay observada.

Diseño futuro aprobado solo metodológicamente: agrupar conectadas y separar equipos, activar dentro de 90 días y seguir margen hasta doce meses desde asignación; ITT, IC bilateral95% y potencia objetivo80%. No hay tamaño muestral sin varianza/ICC ni población operativa autorizada; pocas bolsas independientes hacen inviable la inferencia causal bajo este diseño. Cinco y 500 plazas del cálculo no son tamaños de muestra.

Fuente: `../docs/15-incrementality-experiment.md`; `decision-log.md`, DEC-004/010. Estado: metodología educativa provisional, sin ensayo ni autorización operativa.

## 10. Control Tower — de señal técnica a resultado

Entregable obligatorio como dashboard o prototipo. Cadena: Graph Health → AI Performance → Business Funnel → Economic Impact. Debe conectar desempeño del método, decisión, acción comercial y resultado económico.

Implementación 004B: tablero local con Resumen y las cuatro dimensiones, usando fuentes y reglas aprobadas. Red económica observable con selección de cuenta → conexiones directas → ficha → score/evidencia. Distingue datos sintéticos, ejecución técnica, acción comercial No observado e hipótesis financieras. Streamlit opcional, offline predeterminado y Atlas manual de solo lectura; revisión visual nativa Windows pendiente. El dibujo de la red no prueba valor económico.

Fuente: reto, diapositiva 10 y notas; `../docs/02-challenge-traceability.md`, bloque 6; `../docs/17-control-tower-design.md`; `decision-log.md`, DEC-011.

## 11. Control Tower — funnel segmentable y límites

Universo elegible → oportunidades → leads calificados → contactos activados → conversiones. El reto pide segmentación por industria, geografía, cluster, producto, canal, score y período.

Implementación 004B: período exacto, industria observable, empresa y score permiten inspeccionar resultados sin modificar decisiones. Geografía, cluster, producto y canal carecen de soporte y están deshabilitados. En T2 hay 23 conocidas, 21 elegibles y cinco priorizadas por política; dos excluidas. Contactos, oportunidades, activaciones y ventas siguen No observado, no cero. Una cuenta elegible en la PoC no es un lead calificado ni permiso de contacto.

Fuente: reto, diapositiva 11 y notas; `../docs/02-challenge-traceability.md`; `../docs/17-control-tower-design.md`. La segmentación propuesta conserva top-5 y posiciones globales; no produce rentabilidad por cuenta/sector.

## 12. Estado, riesgos y siguiente decisión

Las misiones 002B/003A demuestran construcción, trazabilidad, conocimiento parcial y comparación de decisiones bajo igual capacidad. No demuestran mejores resultados comerciales, ventas ni margen adicional. Los datos son ficticios y no constituyen evidencia causal.

Ya existen dos políticas aprobadas, un calculador financiero educativo y la Control Tower local 004B para revisión. ECO-01 a ECO-06 son aprobación metodológica provisional: no validan finanzas ni autorizan contactos, datos reales, presupuesto, piloto o despliegue. Invertir requeriría evidencia experimental válida y margen atribuible que cubra costos y reserva con incertidumbre aceptable. No hay eventos comerciales. La entrega final conserva el brief de 2–3 páginas y la defensa con perspectiva de CEO. Guion de cinco minutos: `../docs/18-control-tower-demo.md`.

Riesgos vigentes: identidad sin evidencia fuerte, conflictos abiertos, cobertura escasa, empates, sesgo del escenario sintético y atribuir efecto a una demostración técnica. No se agregan observaciones para inventar ejemplos de fusión, transición o caducidad.

Fuente: `../docs/10-design-validation.md`; `../docs/12-commercial-ranking.md`; `../docs/13-ranking-comparison.md`; `../docs/14-incremental-economic-case.md`; `../docs/15-incrementality-experiment.md`; `../docs/16-financial-calculation.md`; `../docs/02-challenge-traceability.md`.
