# Registro de decisiones importantes

Estados permitidos: **propuesta**, **aprobada**, **descartada**. Las aprobaciones de producto requieren instrucción explícita; las elecciones técnicas menores no se elevan a decisiones estratégicas. Las decisiones previas D-001 a D-013 se conservan en `../docs/03-scope-and-decisions.md`.

## DEC-001 — Base de desarrollo mínima y reproducible

- **Estado:** aprobada para misión 001 por solicitud expresa del usuario; vincula D-011 y el bloque Architecture.
- **Problema:** preparar una demostración reproducible en tres días sin consumir el plazo en infraestructura.
- **Alternativas:** scripts sin dependencias fijadas; ODM/ORM; plataforma con servicios adicionales; paquete pequeño con PyMongo directo.
- **Justificación:** Python >=3.11, uv, PyMongo y python-dotenv cubren instalación y acceso; pytest y Ruff verifican comportamiento y calidad. Python 3.12 es la versión de desarrollo elegida y disponible. No se aprueba todavía el modelo de colecciones.
- **Riesgos y compromisos:** requiere un servidor MongoDB externo a este paquete y configuración válida. Elegir MongoDB no demuestra idoneidad para recorridos profundos ni escala de producción.
- **Explicación al CEO:** invertimos en una base pequeña que permita repetir y revisar la demostración, sin pagar complejidad anticipada.
- **Evidencia para validarla:** instalación bloqueada, pruebas aisladas, lint y formato; `ping` real solo cuando haya servidor y acceso. Crear el cliente no basta.

## DEC-002 — Acotar misión 001 antes de modelar o simular

- **Estado:** aprobada por restricción explícita de la misión; vincula D-012 y los seis bloques.
- **Problema:** evitar que decisiones de datos y analítica no aprobadas se implementen de forma accidental.
- **Alternativas:** generar inmediatamente las 30 empresas; diseñar e implementar todo el grafo; preparar primero la base y decidir el modelo después.
- **Justificación:** P-001 a P-008 siguen pendientes; la prioridad es una respuesta defendible, no acumular funcionalidades.
- **Riesgos y compromisos:** al cerrar esta misión no existe demostración analítica ni económica. Queda trabajo esencial del MVP.
- **Explicación al CEO:** dejamos lista la herramienta de trabajo antes de decidir qué información será válida para orientar una inversión comercial.
- **Evidencia para validarla:** repositorio sin generadores ni scoring, pendientes explícitos y aprobación del modelo antes de la misión siguiente.

## DEC-003 — Control Tower obligatoria; interfaz por decidir

- **Estado:** aprobada por requisito comprobado del reto, diapositivas 10 y 12 y sus notas. Corrige la clasificación inicial del brief; no autoriza implementarla en misión 001.
- **Problema:** una visualización opcional no puede volver opcional la conexión entre calidad técnica y efecto económico.
- **Alternativas:** dashboard funcional; prototipo de Control Tower. Streamlit y una interfaz sofisticada siguen siendo opcionales.
- **Justificación:** la fuente requiere enlazar Graph Health, AI Performance, Business Funnel y Economic Impact y admite un prototipo.
- **Riesgos y compromisos:** las definiciones y el prototipo aún no existen; un tablero con cifras simuladas no prueba incremento causal.
- **Explicación al CEO:** debemos poder seguir cómo una señal termina en una acción y en un resultado, antes de decidir si conviene escalar.
- **Evidencia para validarla:** prototipo trazable que conecte las cuatro dimensiones y distinga resultados de escenarios; formato concreto pendiente.

## DEC-004 — Validación económica con contrafactual

- **Estado:** propuesta metodológica; refleja la restricción aprobada D-008 de no atribuir ROI real a datos sintéticos. El experimento concreto no está aprobado.
- **Problema:** cambios en ranking o conversiones podrían deberse a capacidad comercial, selección o contexto y no al grafo.
- **Alternativas:** comparación antes/después; observación de adopción; experimento con control y aleatorización cuando sea viable.
- **Justificación:** un contrafactual permite separar el efecto de la política enriquecida de lo que habría ocurrido con la política actual.
- **Riesgos y compromisos:** potencia insuficiente, spillovers, costos no registrados, diferencias de ejecución y restricciones operativas. Un experimento real excede la PoC.
- **Explicación al CEO:** solo escalaremos por margen adicional atribuible y neto de costos, no porque la demostración se vea convincente.
- **Evidencia para validarla:** protocolo con unidad y ventana, control comparable, costos, análisis predefinido e incertidumbre. El diseño detallado está propuesto en `../docs/15-incrementality-experiment.md` (003B), todavía sin aprobación ni ejecución. No hay efecto causal medido.

## DEC-005 — Separar la construcción del mundo de la consulta comercial

- **Estado:** aprobada por la misión 002B; bloques Economic Graph y Architecture.
- **Problema:** el simulador conoce atributos y vínculos que la Telco no conoce; incluso algunas notas revelan diagnósticos de falsedad.
- **Alternativas:** consultar directamente el catálogo; quitar solo campos `truth`; proyectar un ledger observable y aislar su interfaz.
- **Justificación:** se preservan los originales, se eliminan campos privados, se neutralizan tres notas diagnósticas y se asignan IDs públicos desde la evidencia. El visor nunca consulta el mundo ni su denominador completo.
- **Riesgos y compromisos:** un desarrollador con acceso al checkout puede leer la verdad; producción exige credenciales/roles y montaje separados. No se confunde UUID con autorización.
- **Explicación al CEO:** podemos mostrar lo que sabemos y cuándo lo supimos sin regalar al método respuestas que ningún comercial tendría.
- **Evidencia:** pruebas as-of, desconocidos, rechazo de campos anidados y lectura del ledger sin directorio de diseño; auditoría DV-001. No implica mayor conversión.

## DEC-006 — Conservar incertidumbre sin fabricar resolución

- **Estado:** aprobada por la prohibición explícita de fusiones y confirmaciones arbitrarias en misión 002B.
- **Problema:** alias parecidos, atributos distintos y reportes de fuentes no prueban identidad ni existencia de transacciones.
- **Alternativas:** elegir el dato más reciente; fusionar por nombre; consultar la verdad del simulador; conservar candidatos, conflicto e historia.
- **Justificación:** no hay evidencia fuerte aprobada para fusionar ALIAS-001/002; los valores de CG-001/002 se mantienen sin arbitraje. REPORTED e INFERRED no pasan a CONFIRMED por existir el vínculo en la verdad.
- **Riesgos y compromisos:** menor cantidad de atributos consolidados; faltan ejemplos reales de transición/caducidad y de fusión fuerte. Requieren adenda aprobada, no generación automática.
- **Explicación al CEO:** es preferible reconocer una duda que priorizar una cuenta apoyándonos en una certeza inventada.
- **Evidencia:** historial intacto, candidatos sin empresas adicionales y conflictos visibles. DV-002/003 documentan lo no demostrado.

## DEC-007 — Persistir un ledger mínimo e inmutable

- **Estado:** elección técnica de implementación dentro de la autorización 002B; verificada offline. En 002C el usuario reportó integración Atlas exitosa desde Windows con VS Code; no fue ejecutada por Codex Cloud.
- **Problema:** hacer reintentable la carga y reconstruir cortes sin alterar colecciones ajenas ni duplicar perfiles.
- **Alternativas:** reemplazar colecciones; guardar snapshots completos por corte; almacenar observaciones y derivar las vistas.
- **Justificación:** una colección de observaciones por ID y una marca de propiedad bastan. Base dedicada, dry-run por defecto, confirmación explícita, `$setOnInsert` y rechazo de colisiones. Índices por disponibilidad y por sujeto/disponibilidad responden a consultas concretas.
- **Riesgos y compromisos:** el lote no es una transacción; puede quedar incompleto ante un fallo, pero se puede reintentar. No se afirma rendimiento a escala ni validación de la separación de roles Atlas.
- **Explicación al CEO:** repetir una preparación no duplica el conocimiento ni modifica datos de otros sistemas.
- **Evidencia:** pruebas offline de carga repetida, contenido distinto, base incorrecta y colecciones ajenas. Reporte local del usuario en 002C: primera carga 83 insertadas; segunda 0 insertadas/83 sin cambios; consultas T0/T1/T2 con conteos esperados. Ver `../docs/11-atlas-integration-validation.md`; no se afirma ejecución de la prueba automatizada de integración en cloud.

## DEC-008 — Registrar la integración local con su procedencia

- **Estado:** aprobada por la solicitud explícita de cierre documental de misión 002C; bloques Economic Graph y Architecture.
- **Problema:** distinguir el éxito local reportado de los intentos cloud sin ping exitoso y evitar atribuir resultados a un entorno que no los ejecutó.
- **Alternativas:** mantener toda integración como pendiente; presentar el éxito como validación cloud; registrar por separado el reporte local y las comprobaciones offline de Codex.
- **Justificación:** Windows con VS Code es el entorno de las ejecuciones reales comunicadas por el usuario. Se registran exactamente ping, auditoría, dos cargas y conteos de consultas, sin inventar resultados adicionales.
- **Riesgos y compromisos:** no se aportaron logs completos ni SHA del checkout local. La evidencia no valida conectividad cloud, roles, escala ni impacto económico; las advertencias conocidas permanecen.
- **Explicación al CEO:** ya se reportó funcionamiento real de almacenamiento y consulta en Atlas desde el equipo local. Eso reduce una incertidumbre técnica; todavía no demuestra ventas ni margen adicional.
- **Evidencia:** reporte del usuario preservado en `../docs/11-atlas-integration-validation.md`; pruebas offline y Ruff ejecutados por Codex se informan separadamente. No se añaden funcionalidades ni se modifica Atlas para este cierre.

## DEC-009 — Comparar reglas explicables con capacidad fija

- **Estado:** aprobada explícitamente por el usuario en las tres respuestas de la conversación 003A: política conservadora, exclusión de servicio activo confirmado y K=5. Implementada como `003a-conservative-v1`.
- **Problema:** explicar qué cuentas elegiría una política con señales del grafo frente a una basada en atributos individuales, usando la misma información temporal y capacidad.
- **Alternativas:** priorizar por sector o reseñas; usar vínculos reportados con descuento; contar solo vecinos confirmados; entrenar un modelo. No existen etiquetas para entrenar ni evidencia que convierta reseñas en intención de compra.
- **Justificación:** baseline `10 × min(max(sucursales − 1, 0), 5)` más `5 × min(vecinos económicos confirmados distintos, 4)` permite mostrar contribuciones sencillas sin consultar el mundo restringido. La auditoría encuentra sucursales sin conflicto solo para 2/3/3 cuentas en T0/T1/T2 y 2/2/4 vínculos económicos confirmados. Ambas políticas comparten cohorte y cinco plazas; no se ajustaron los pesos a resultados. Clientes activos confirmados no compiten por adquisición, pero pueden aportar contexto relacional como vecinos conocidos.
- **Riesgos y compromisos:** fuerte escasez de atributos, sesgo hacia cuentas documentadas, muchos empates e identidad pendiente. Servicio desconocido no equivale a no-cliente. Los puntos no son probabilidades; una selección distinta no demuestra ventas adicionales.
- **Explicación al CEO:** con cinco plazas por corte, estas reglas seleccionan dos cuentas en común y tres distintas. Mostramos qué evidencia explica el cambio y cuándo una plaza depende de un empate técnico. Eso permite revisar una decisión; todavía no demuestra que el esfuerzo comercial rinda más.
- **Evidencia:** aprobación de la política; regresiones offline sin oráculo ni fuga temporal; tabla reproducible y explicación por cuenta en `../docs/12-commercial-ranking.md` y `../docs/13-ranking-comparison.md`. La lectura MongoDB se contrasta con un doble de solo lectura; rankings en Atlas real no verificados. Evaluar superioridad comercial requerirá datos autorizados y un contrafactual.

## DEC-010 — Diseñar el caso económico antes de simular resultados

- **Estado:** propuesta de modelo y protocolo en misión 003B. El usuario autorizó únicamente auditoría, diseño y publicación en PR borrador; los supuestos ECO-01 a ECO-06 no están aprobados.
- **Problema:** convertir cambios de priorización en una pregunta de margen incremental neto, sin inventar ventas ni atribuir causalidad a los rankings.
- **Alternativas:** usar un ROI de escenario como demostración; comparar antes/después; aleatorizar empresas ignorando sus relaciones; proponer finanzas explícitas y un A/B por bolsas con análisis poblacional ITT. Cambiar el baseline aprobado para que coincida con una práctica real no documentada requeriría otra aprobación.
- **Justificación:** descontar costo comercial, implantación, adquisición de datos y operación, y considerar a las no seleccionadas, permite formular un umbral verificable. Bolsas completas asignadas antes del top-5 reducen contaminación conocida sin consultar el oráculo; mantienen la decisión comercial y su contrafactual claros.
- **Riesgos y compromisos:** costos y tasas pedagógicos, volumen de despliegue sin validar, identidad y permisos pendientes, interferencia oculta, pocas unidades independientes y horizontes inmaduros. No se promete potencia ni rentabilidad. La extensión de K=5 a bolsas reales necesita aprobación; las reglas 003A no cambian.
- **Explicación al CEO:** necesitamos saber qué mejora mínima paga el costo total adicional y financiar, como máximo, un piloto para medirla. Que dos listas difieran no demuestra más ventas. Una recomendación de despliegue exige margen atribuible, incertidumbre y costos cotizados.
- **Evidencia para validarla:** aprobación de entradas y protocolo; luego trazabilidad financiera, presupuesto, muestra por bolsas, medición madura y límite inferior del efecto que supere costos/reserva. Ver `../docs/14-incremental-economic-case.md` y `../docs/15-incrementality-experiment.md`. No existe simulador financiero ni ensayo ejecutado.
