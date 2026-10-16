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

## DEC-003 — Control Tower obligatoria

- **Estado:** aprobada por requisito comprobado del reto, diapositivas 10 y 12 y sus notas. Corrige la clasificación inicial del brief; no autoriza implementarla en misión 001.
- **Problema:** una visualización opcional no puede volver opcional la conexión entre calidad técnica y efecto económico.
- **Alternativas:** dashboard funcional; prototipo de Control Tower. Streamlit y una interfaz sofisticada siguen siendo opcionales.
- **Justificación:** la fuente requiere enlazar Graph Health, AI Performance, Business Funnel y Economic Impact y admite un prototipo.
- **Riesgos y compromisos:** el prototipo incorporado en 004B no aporta eventos comerciales; un tablero con cifras simuladas no prueba incremento causal.
- **Explicación al CEO:** debemos poder seguir cómo una señal termina en una acción y en un resultado, antes de decidir si conviene escalar.
- **Evidencia para validarla:** prototipo trazable que conecte las cuatro dimensiones y distinga resultados de escenarios; formato aprobado e implementado en DEC-011, revisión Windows pendiente.

## DEC-004 — Validación económica con contrafactual

- **Estado:** aprobada provisionalmente como metodología educativa en ECO-03 a ECO-06 de 003B; ejecución, contactos, presupuesto y despliegue no autorizados. Conserva D-008: no atribuir ROI causal real a supuestos o datos sintéticos.
- **Problema:** cambios en ranking o conversiones podrían deberse a capacidad comercial, selección o contexto y no al grafo.
- **Alternativas:** comparación antes/después; observación de adopción; experimento con control y aleatorización cuando sea viable.
- **Justificación:** un contrafactual permite separar el efecto de la política enriquecida de lo que habría ocurrido con la política actual.
- **Riesgos y compromisos:** potencia insuficiente, spillovers, costos no registrados, diferencias de ejecución y restricciones operativas. Un experimento real excede la PoC.
- **Explicación al CEO:** solo escalaremos por margen adicional atribuible y neto de costos, no porque la demostración se vea convincente.
- **Evidencia para validarla:** protocolo con unidad y ventana, control comparable, costos, análisis ITT e incertidumbre; diseño futuro en `../docs/15-incrementality-experiment.md`, aprobado solo metodológicamente. Faltan fuentes autorizadas, varianza/ICC, muestra e independencia suficiente de bolsas. No hay ensayo ejecutado ni efecto causal medido.

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

## DEC-010 — Calcular hipótesis económicas sin atribuirlas a resultados reales

- **Estado:** ECO-01 a ECO-06 aprobadas provisionalmente y exclusivamente para la PoC educativa tras revisión del PR #5. El usuario autorizó calculador determinista, escenarios, sensibilidad y equilibrio; no validación financiera ni operación real.
- **Problema:** convertir cambios de priorización en una pregunta de margen incremental neto, sin inventar ventas ni atribuir causalidad a los rankings.
- **Alternativas:** usar un ROI de escenario como demostración; comparar antes/después; aleatorizar empresas ignorando sus relaciones; proponer finanzas explícitas y un A/B por bolsas con análisis poblacional ITT. Cambiar el baseline aprobado para que coincida con una práctica real no documentada requeriría otra aprobación.
- **Justificación:** separar margen, costo comercial, implantación, adquisición de datos/operación y efectos del resto permite comprobar el umbral sin duplicar costos. El calculador no consume empresas, ledger ni oráculo. Distingue cinco plazas, 500 plazas hipotéticas y protocolo futuro. Decimal, unidades y metadatos de valoración evitan errores de punto flotante y reutilizar valores presentes bajo otro H/descuento; la reserva se muestra sin convertirla en un segundo gasto.
- **Riesgos y compromisos:** costos y tasas no calibrados, volumen sin validar, identidad/permisos pendientes, interferencia oculta y pocas bolsas independientes. No se calcula muestra sin varianza/ICC. La contabilidad semántica de facturas sigue requiriendo revisión humana; IDs únicos no prueban que dos costos sean distintos. Las reglas 003A permanecen intactas.
- **Explicación al CEO:** cinco plazas no cubren el costo bajo ninguno de los cuatro casos aprobados. Quinientas pueden dar pérdidas o saldos positivos según hipótesis, pero no prueban que el beneficio sea alcanzable. Un saldo cero es el umbral matemático; cero mejora de conversión puede seguir perdiendo dinero. Ninguno autoriza invertir: faltan efecto atribuible, costos reales y autorización operativa.
- **Evidencia:** aprobación explícita del usuario con límites ECO-01 a ECO-06; pruebas de identidades, regresiones, sensibilidad, valoración e aislamiento; resultados reproducibles en `../docs/16-financial-calculation.md`. El diseño futuro sigue en `../docs/15-incrementality-experiment.md`. Calculador implementado; sin ventas por empresa, ensayo, muestra, presupuesto ni despliegue.

## DEC-011 — Control Tower que distingue evidencia y supuestos

- **Estado:** aprobada expresamente en 004B, CT-01 a CT-05 con ampliación CT-02; pulido 004C autorizado. PR #6 sin integración automática. El usuario confirmó funcionamiento/271 pruebas Windows de 004B; nueva revisión visual 004C pendiente.
- **Problema:** demostrar Graph Health → priorización → acción → resultado sin ocultar los eslabones comerciales no observados ni presentar hipótesis como desempeño medido.
- **Alternativas:** CLI/Markdown actuales; HTML estático o web propia; Streamlit local con módulos existentes. Para la red: Vega-Lite integrado frente a bibliotecas especializadas; selección lateral sincronizada frente a callbacks de clic en nodos.
- **Justificación:** cinco vistas y adaptación descriptiva conservan fuentes únicas de reglas/finanzas. Streamlit 1.66.0 en grupo opcional `ui` aporta controles y Vega-Lite; no hace falta otra dependencia directa de red. Layout circular determinista y selector evitan complejidad de motor gráfico. Los filtros mantienen posiciones/top-5 y economía independiente de empresas; Atlas manual solo lectura con paridad e invalidación de contexto.
- **Riesgos y compromisos:** transitivas como pandas/PyArrow aumentan instalación; versión fijada, probada Linux y 004B Windows confirmada por el usuario. Nueva revisión visual 004C pendiente. Datos escasos, identidad sin resolver, ausencia de etiquetas/eventos y superposición en red completa. Foco, nombres por hover/tablas y detalle reducen complejidad; sin inferir distancia comercial ni confianza del oráculo. La red no acredita efecto económico.
- **Explicación al CEO:** el tablero muestra qué cuentas se consideran y por qué, dónde falta evidencia y qué mejora hipotética pagaría la solución. Ventas no observadas y escenarios educativos se distinguen; una tarjeta positiva no autoriza invertir.
- **Evidencia:** pruebas de paridad, aislamiento temporal/privado, filtros sin nuevas reglas, etapas No observado, finanzas intactas y lectura Atlas con doble `find`. AppTest y Chromium Linux ejercitan vistas/red; regresión pública aislada sin red/env/simulador. CT-A01 a CT-A13 en `../docs/17-control-tower-design.md`; resultados y guion en `../docs/18-control-tower-demo.md`. Windows 004B es reporte del usuario, no ejecución Codex; sin nueva validación real Atlas o rendimiento a escala.
- **Seguimiento Windows:** el usuario confirmó instalación y reportó timeout del primer AppTest más bloqueo de IPC interno. Se separa carga fría de dependencias del presupuesto funcional y se admite únicamente `socketpair` local, sin abrir acceso a servicios. Se conservan 271 pruebas y timeout de 15 segundos; confirmación nativa pendiente. El diagnóstico detallado y la incertidumbre sobre la duración original están en la guía 004B; no cambia la arquitectura o política aprobada.
- **Pulido 004C aprobado:** tras confirmar 271 pruebas y funcionamiento Windows, el usuario solicita jerarquía ejecutiva y red centrada. Se conserva Vega-Lite/Streamlit y se usan tarjetas, matriz y paneles contraídos en vez de agregar bibliotecas. El grosor de vínculos referencia evidencia de la feature ya calculada; evita otro scoring. Beneficio esperado: explicar la decisión en cinco minutos, sin equiparar selección o escenario con ventas. Compromiso: más detalle requiere expandir auditoría; puede restablecerse el segmento explícitamente. Se valida navegador a 1366×900, paridad, foco temporal y auditoría accesible; no es evidencia comercial. Guion actualizado en la guía, nueva revisión visual Windows pendiente; no hay merge.
