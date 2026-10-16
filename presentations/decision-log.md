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
- **Evidencia para validarla:** protocolo con unidad y ventana, control comparable, costos, análisis predefinido e incertidumbre. Todos permanecen pendientes.

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

- **Estado:** elección técnica de implementación dentro de la autorización 002B; implementada y verificada offline, pendiente de integración Atlas.
- **Problema:** hacer reintentable la carga y reconstruir cortes sin alterar colecciones ajenas ni duplicar perfiles.
- **Alternativas:** reemplazar colecciones; guardar snapshots completos por corte; almacenar observaciones y derivar las vistas.
- **Justificación:** una colección de observaciones por ID y una marca de propiedad bastan. Base dedicada, dry-run por defecto, confirmación explícita, `$setOnInsert` y rechazo de colisiones. Índices por disponibilidad y por sujeto/disponibilidad responden a consultas concretas.
- **Riesgos y compromisos:** el lote no es una transacción; puede quedar incompleto ante un fallo, pero se puede reintentar. No se afirma rendimiento a escala ni se han provisionado roles Atlas.
- **Explicación al CEO:** repetir una preparación no duplica el conocimiento ni modifica datos de otros sistemas.
- **Evidencia:** pruebas de carga repetida, contenido distinto, base incorrecta y colecciones ajenas; prueba real opcional, aún no ejecutada.
