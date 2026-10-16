# Matriz de trazabilidad del reto — v1.0

**Pregunta central:** ¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?

**Fuente contrastada:** presentación original `../presentations/references/Reto-AI-Engineering-SME-Economic-Graph.pptx`, 13 diapositivas y sus notas, revisadas en la misión 001. La diapositiva 12 enumera estos seis entregables. La matriz sigue siendo la referencia del alcance del MVP completo; inicializar el repositorio no completa esos entregables.

| Bloque | Pregunta que debemos responder | Evidencia a entregar | Criterio de aceptación | Estado |
|---|---|---|---|---|
| 1. Business Framing | ¿Qué problema de adquisición B2B se resuelve y cómo genera valor? | Hipótesis de usuario, embudo, mecanismo económico y KPIs | Conecta problema → decisión → intervención → resultado medible | Contexto definido; evidencia por completar |
| 2. Economic Graph | ¿Qué son nodos y aristas, de dónde vienen y cuán confiables son? | Modelo de entidades/relaciones, fuentes, resolución de identidad, fechas, confianza y procedencia; ejemplo consultable | Se puede reconstruir por qué existe una conexión y desde cuándo era conocida | Construcción verificada offline en 002B; consultas Atlas T0/T1/T2 reportadas por el usuario desde Windows en 002C; identidad fuerte pendiente |
| 3. AI/ML Approach | ¿Cómo usar las señales y demostrar que superan un baseline? | Baseline, ranking enriquecido, características, evaluación sin fuga; plan ML si escala | Elección justificada de regla/ML, métricas claras y límites reconocidos | Comparación determinista 003A implementada offline; sin evidencia de superioridad comercial ni predictiva |
| 4. Architecture | ¿Cómo fluye y se gobierna la información desde fuentes hasta usuarios? | Diagrama PoC + arquitectura objetivo; ingestión, entity resolution, procesamiento, serving, escalabilidad, seguridad, gobernanza, MLOps condicional | Diferencia claramente lo implementado de lo propuesto para producción | Separación e ingesta implementadas; integración Atlas local reportada por el usuario en 002C; conectividad desde Codex Cloud y escala no verificadas |
| 5. Economic Case | ¿Cuál es la rentabilidad incremental atribuible? | Modelo de unit economics, costos, escenarios, diseño A/B y fórmula de margen neto incremental | Identifica contrafactual, unidad de asignación, horizonte y costos de operación | Calculador 003B y metodología aprobados provisionalmente solo para PoC; escenarios y umbrales ejecutados, sin rentabilidad real ni efecto causal medido |
| 6. Control Tower | ¿Cómo monitorear datos, método y negocio? | Indicadores Graph Health, AI Performance, Business Funnel y Economic Impact | Cada indicador tiene definición, frecuencia/fuente futura y limitaciones | Diseño visual/técnico 004A propuesto con fuentes y aceptación; CT-01 a CT-05 pendientes; interfaz no implementada |

## 1. Business Framing

**Decisión actual:** enfocar el caso en priorización de prospectos para adquisición B2B.\
**Cadena causal postulada:** señales del grafo → mejor selección de cuentas/contactos → uso más eficiente del esfuerzo comercial → mayor margen neto potencial.\
**Condición:** esto es una hipótesis; se requiere experimento real para atribuir efecto.

**Pendiente:** cuantificar línea base, costos por contacto, valor por contrato, restricciones comerciales y supuestos de operación; en la PoC se usarán escenarios declarados.

## 2. Economic Graph

El diseño deberá cubrir explícitamente:

- **Entidades:** PyMEs y, si aportan valor, oportunidades, sucursales u otras entidades justificadas.
- **Relaciones:** relaciones económicas definidas con dirección y significado; no confundir cercanía geográfica con transacción.
- **Fuentes:** cuáles serían accesibles legítimamente a una Telco en realidad; cuáles son datos de simulación.
- **Resolución de identidad:** unificación y deduplicación de negocios entre fuentes, con explicación de errores posibles.
- **Tiempo:** vigencia de relaciones, tiempo del hecho y momento en que fue conocido.
- **Confianza y procedencia:** evidencia observada/inferida, método y nivel de confianza.

**Riesgo crítico:** la simulación tiene una «verdad de mundo» más rica que la información observable; **la priorización no puede usarla directamente**.

## 3. AI/ML Approach

- **Baseline:** puntuación comercial a partir de atributos empresariales observables.
- **Tratamiento enriquecido:** misma base + características relacionales disponibles antes del contacto.
- **PoC:** comparación reproducible de rankings y, solo si la muestra lo permite, un análisis ilustrativo de resultados simulados.
- **Producción:** especificar dataset con fechas de corte, división temporal, métrica de negocio, validación, monitoreo y eventual modelado ML. **No forzar una GNN ni un modelo entrenado en 30 entidades.**
- **Inferencia:** explicar qué se recalcula, cuándo y cómo se exponen explicaciones y puntuaciones al usuario.

## 4. Architecture

**PoC sugerida:** generación sintética → MongoDB/PyMongo → extracción de señales y ranking en Python → tabla, gráfico o visualización pequeña.\
**Producción propuesta, no implementada:** ingestión autorizada, controles de calidad/identidad, grafo versionado, pipelines, serving, acceso por roles, monitoreo, auditoría y ciclo de vida de modelos si se agregan.\
**Decisiones por justificar:** por qué MongoDB es suficiente en el MVP, cuándo harían falta otros componentes y trade-offs de costo/latencia/escalado.

## 5. Economic Case: núcleo de la defensa

El efecto comercial relevante **no** es «el ranking parece mejor» sino el incremento atribuible del resultado económico al cambiar la política de priorización.

**Medida orientativa:**

`Valor incremental neto = (margen de contribución del grupo tratado − margen contrafactual estimado) − costo incremental de construir y operar la solución`

Definir claramente período, unidad y tratamiento de costos. Para comparar grupos de distinto tamaño se debe normalizar por unidad asignada antes de extrapolar.

**Diseño futuro de prueba:**

1. Registrar política comercial actual y métrica principal (por ejemplo, margen de contribución neto por cuenta elegible asignada durante una ventana fija).
2. Asignar prospectos o agrupaciones de cuentas al **control** (priorización actual) y **tratamiento** (grafo), con aleatorización adecuada.
3. Mantener comparables presupuesto, capacidad, canales y reglas de contacto, o registrarlos para el análisis.
4. Atender **contaminación/spillovers**: empresas conectadas y vendedores pueden influenciarse; considerar asignación por cluster o equipo cuando haga falta.
5. Predefinir horizonte de observación, tamaño muestral/potencia, reglas de exclusión y análisis de intención de tratar.
6. Medir ingresos, conversión, costos de contacto, costo de datos/infraestructura y margen, con incertidumbre estadística.
7. Escalar solo si el valor **incremental neto** y la confiabilidad operativa justifican continuar.

**Nunca:** atribuir a la PoC sintética ingresos reales, uplift causal o ROI verificado.

## 6. Control Tower

| Dimensión | Indicadores candidatos | Advertencia |
|---|---|---|
| Graph Health | entidades enlazadas, relaciones con procedencia, datos incompletos, edad de relaciones, duplicados | No inventar exactitud de entity resolution sin verdad etiquetada |
| AI Performance | cambio de ranking, cobertura de scoring, métricas offline cuando haya etiquetas, drift futuro | Si no hay ML entrenado, llamarlo desempeño analítico, no precisión de IA |
| Business Funnel | prospectos priorizados, contactos, oportunidades, cierres y tiempos | No se han materializado eventos comerciales; requieren datos y definiciones autorizados |
| Economic Impact | margen por cuenta elegible, CAC incremental, costo de plataforma, valor incremental neto | Distinguir escenarios de estimaciones causales reales |

## Verificación final de entrega

- [ ] Los seis bloques tienen al menos una lámina/sección defendible.
- [ ] Todo número aparece con su procedencia: sintético, supuesto, resultado ejecutado o dato real.
- [ ] Los límites del prototipo de 30 empresas están señalados.
- [ ] El plan causal identifica control y contrafactual.
- [ ] Los elementos no implementados se etiquetan como diseño futuro.
- [ ] El prototipo no consume información que un operador Telco desconocería.

## Contraste con la fuente y límites de la misión 001

| Fuente original | Requisito comprobado | Tratamiento |
|---|---|---|
| Diapositiva 4 | Pregunta central del Economic Graph e incrementalidad | Criterio prioritario en todas las misiones |
| Diapositivas 3, 6 y notas | Fuentes autorizadas; procedencia, tiempo, confianza e identidad | Diseño pendiente; no ingerir datos reales |
| Diapositiva 9 | Libertad tecnológica; evaluación, serving, costo, latencia, MLOps/GraphOps y gobierno | Justificar elecciones; no obliga a usar LLM, GNN ni agentes |
| Diapositiva 10 y notas | Control Tower **obligatoria**, dashboard o prototipo: desempeño → decisión → acción comercial → resultado económico | Se corrige la prioridad P1 del brief inicial a P0; implementación pendiente de otra misión |
| Diapositiva 11 y notas | Funnel segmentable por industria, geografía, cluster, producto, canal, score y período; incluye contactos activados | Ejemplo del reto, no datos propios ni resultados alcanzados |
| Diapositiva 12 y notas | Seis entregables; brief de 2–3 páginas y presentación de propuesta | Esta misión crea la estructura de la presentación; brief final pendiente |
| Diapositiva 13 y notas | Defensa adicional con perspectiva de CEO | Guía de comunicación y registro de decisiones |

Las cifras de score y funnel de las diapositivas 8 y 11 son **ilustraciones del reto**. No son evidencia de esta PoC ni metas aprobadas.

**Discrepancias registradas:** el brief inicial hacía opcional una Control Tower visual. La fuente exige el entregable, aunque permite un prototipo: se conserva flexibilidad de interfaz y se corrige la obligatoriedad. La arquitectura y las 30 PyMEs describen el MVP futuro; la instrucción explícita de misión 001 limita el trabajo actual a su base técnica. No se resuelven P-001 a P-008 ni se aprueba un esquema de datos.

**Trazabilidad de esta misión:** configuración, PyMongo, pruebas, instalación y documentación habilitan el bloque 4 (Architecture). El deck y las reglas ejecutivas organizan los seis bloques, sin declarar su implementación. La conexión real requiere servidor y configuración válida; no se considera verificada mediante mocks.

## Evidencia de misión 002B

El diseño de `06-economic-graph-design.md` y los tres paquetes fueron aprobados explícitamente. `10-design-validation.md` registra procedencia, invariantes y discrepancias con IDs. No se considera implementada una fusión, transición o caducidad ausente en el plan aprobado.

| Bloque | Evidencia implementada | Límite |
|---|---|---|
| Economic Graph | 30 empresas/48 relaciones en fuentes restringidas; 83 observaciones materializadas; vistas T0/T1/T2 con empresas 12/17/23; historia, procedencia, conflictos y alias candidatos | 7 empresas y 25 relaciones verdaderas permanecen desconocidas; no se revelan a la interfaz comercial |
| Architecture | `simulator/design.py` audita todos los archivos; `simulator/project.py` proyecta sin enriquecer desde el catálogo; `observable.py` consulta solo el ledger público | Separación por archivos e interfaces; roles comerciales de Atlas no provisionados y sin validación a escala |
| Architecture / persistencia | `mongo_observable.py` limita base y colecciones, rechaza contenido ajeno y usa inserciones inmutables por ID; prueba de idempotencia offline | Al cierre de 002B no se había ejecutado carga en Atlas; el reporte local posterior se registra en 002C |
| Graph Health como evidencia de calidad | Pruebas de IDs, enlaces huérfanos, tipos, tiempos, incertidumbre, duplicados, ausencia de verdad y desconocidos | No es una Control Tower implementada ni precisión medida de entity resolution |
| AI/ML, economía y funnel | Contratos y límites documentados | Sin scoring, ML, eventos, conversiones, causalidad ni valor económico medido |

Pruebas relevantes: `tests/test_design.py`, `test_observable.py`, `test_mongo_observable.py` y `test_graph_commands.py`. La integración está separada en `tests/integration/test_atlas_observable.py`. Las 2/11/23 relaciones verdaderas observadas son un conteo restringido de validación del simulador, no una métrica comercial de confirmaciones.

## Evidencia de misión 002C — integración local reportada

Fuente: [validación Atlas](11-atlas-integration-validation.md), resultados comunicados por el usuario desde Windows con VS Code. No se atribuyen a ejecuciones de Codex Cloud.

| Requisito | Evidencia local reportada | Límite |
|---|---|---|
| Architecture: conexión y persistencia | PyMongo y ping exitosos; primera carga de 83 observaciones | No demuestra conectividad desde Codex Cloud ni rendimiento a escala |
| Architecture: carga repetible | Segunda carga: 0 insertadas, 83 sin cambios | Valida la repetición reportada, sin ampliar la afirmación a escenarios no ejecutados |
| Economic Graph: consultas observacionales | T0: 12 empresas/28 observaciones; T1: 17/54; T2: 23/83 | No añade evidencia de identidad fuerte ni resultados de relaciones no reportados |
| Calidad del diseño | `validate_design.py`: 0 errores y 5 advertencias conocidas | DV-001 a DV-005 permanecen documentadas |

Este cierre no incorpora funcionalidades ni resultados de scoring, funnel, economía, causalidad o Control Tower. La evidencia técnica no se convierte en valor económico incremental demostrado.

## Evidencia de misión 003A — rankings comparables

La [auditoría de señales y política aprobada](12-commercial-ranking.md) cubre el bloque 3 (AI/ML Approach), apoyado por los bloques 2 y 4. Se verificó la cobertura real por corte leyendo solo el ledger observable: sucursales sin conflicto en 2/3/3 cuentas y vínculos económicos confirmados 2/2/4. No existen etiquetas de conversión ni información suficiente para afirmar que todas las cuentas sin servicio observado sean prospectos nuevos.

El usuario aprobó explícitamente fórmula, elegibilidad y K=5 (DEC-009). `rankings.py` y `rank_companies.py` implementan la política `003a-conservative-v1`. No se modifica el ledger ni se realizan escrituras en Atlas.

| Requisito | Evidencia implementada | Límite |
|---|---|---|
| AI/ML: baseline y variante con grafo | Baseline por sucursales adicionales; misma base más vecinos económicos confirmados distintos; pesos y contribuciones explicables | Reglas exploratorias; sin probabilidades ni modelo entrenado |
| Comparabilidad y selección | Mismas 12/17/21 cuentas elegibles y cinco plazas por corte; posiciones, diferencias, top-5, entradas/salidas y empates | T2 excluye dos clientes activos confirmados; las demás cuentas requieren validación comercial |
| Economic Graph: trazabilidad y tiempo | Solo ledger observable, filtros `available_at <= as_of`, historia y procedencia por contribución; sin fusión de candidatos | Evidencia escasa; los conflictos conservan incertidumbre; no se evalúa exactitud contra el oráculo para priorizar |
| Architecture: consumo reproducible | CLI offline y lectura MongoDB opcional; prueba de paridad con un doble que solo admite `find` | Integración real de rankings Atlas no verificada; sin escrituras ni validación de escala |
| Comparación de políticas | [Tablas T0/T1/T2](13-ranking-comparison.md): dos seleccionadas en común y tres sustituciones por corte | Baseline atraviesa empates en los tres cortes; grafo en T1/T2; no demuestra mejor conversión ni valor incremental |

Pruebas nuevas: `tests/test_rankings.py` y `tests/test_ranking_commands.py`. Verifican regresiones temporales, contribuciones, incertidumbre, duplicados, alias, elegibilidad, ausencia de campos restringidos y ejecución con solo módulos públicos/ledger. Los seis entregables completos no quedan terminados: economía, experimento causal, funnel, Control Tower y brief final siguen pendientes de sus respectivas misiones.

Seguimiento de portabilidad: el reporte de fallo Windows motivó una reproducción con tuberías cp1252 y la corrección del contrato UTF-8 del CLI y su consumidor de pruebas. Las regresiones conservan el aislamiento e incluyen ambos formatos, rutas con espacios/acentos y diagnóstico sin URI privadas. Causa, comprobaciones y límite de validación nativa Windows en [la guía de rankings](12-commercial-ranking.md#corrección-de-portabilidad-tras-el-reporte-de-windows).

## Evidencia de misión 003B — calculador educativo y protocolo futuro

Se releyeron las 13 diapositivas y notas del reto original desde `main` en `0e1088c`. Tras revisar el PR #5, el usuario aprobó provisionalmente ECO-01 a ECO-06 solo como metodología educativa y autorizó el calculador determinista. [Caso económico](14-incremental-economic-case.md), [protocolo futuro](15-incrementality-experiment.md) y [resultados hipotéticos](16-financial-calculation.md) desarrollan el bloque 5. Las cifras del reto y los cambios de ranking no se usan como tasas de conversión.

| Requisito | Diseño entregado | Evidencia que sigue faltando |
|---|---|---|
| Business Framing → margen | Igual capacidad; margen neto de ventas y costo comercial, efectos sobre no seleccionadas y costo incremental de datos/plataforma | Demanda, producto/cobertura, permisos, conversión, margen y costos reales |
| Economic Case: reproducibilidad | `finance.py`, CLI offline y supuestos versionados: escenarios conservador/base/optimista/nulo, sensibilidad, equilibrio y reserva; unidades, valoración, IDs de costos y decimales validados | Aprobación exclusivamente provisional/metodológica; sin fuentes financieras reales ni ROI causal |
| Economic Case: contrafactual | Diseño futuro por bolsas 1:1, asignación previa a selección, KPI neto por cuenta elegible asignada, ITT, IC95% y potencia objetivo80%, madurez y control de contaminación | Sin población operativa autorizada, varianza/ICC, muestra, ejecución o resultados; inferencia inviable si faltan bolsas independientes suficientes |
| Control Tower: definición futura | KPI económico y métricas secundarias con requisitos de medición | Eventos comerciales, instrumentación y dashboard/prototipo no implementados |

DEC-004/010 registran aprobación provisional metodológica y límites. Cinco plazas de demostración, 500 hipotéticas y experimento futuro son niveles separados; T0/T1/T2 no se convierten en cohortes independientes. El nulo conserva costos y pierde dinero con las entradas aprobadas; los casos positivos no autorizan invertir. Las nuevas pruebas matemáticas/CLI están en `test_finance.py` y `test_finance_commands.py`; no se modifican rankings, ledger, Atlas ni dependencias. No se generan eventos comerciales o ventas por empresa. Datos reales, contactos, presupuesto, piloto y despliegue siguen sin autorizarse. El PR #5 queda listo para revisión sin integración automática.

## Propuesta de misión 004A — Control Tower sin interfaz implementada

Desde `main` en `8e39c8b`, con PR #5 ya integrado, se revisaron reto original (diapositivas/notas 10–12), módulos y evidencia. [Diseño de Control Tower](17-control-tower-design.md) detalla arquitectura visual/técnica, cinco vistas, diccionario de indicadores, filtros, fuentes existentes, trazabilidad, fallos y CT-A01 a CT-A12. No se instalan dependencias ni se programa UI.

| Dimensión obligatoria | Propuesta verificable contra fuentes actuales | Límite explícito |
|---|---|---|
| Graph Health | Snapshot y resumen por corte: empresas, afirmaciones y referencias separadas, estados, fuentes, conflictos, candidatos y frescura descriptiva | Sin denominador privado, confianza numérica inventada ni fusiones/verdad inferidas del simulador |
| AI Performance | Informe 003A: posiciones y contribuciones, top-5, cambios, cobertura y empates | Comparación de reglas sin modelo; no etiquetas para precision/recall/lift/calibración |
| Business Funnel | Conocidas, elegibles, priorizadas por una política y exclusiones; segmentación descriptiva | Contactos, oportunidades, activaciones y ventas como No observado, sin ceros/tasas fabricadas |
| Economic Impact | Informe 003B: cinco/500 plazas, cuatro escenarios, sensibilidad y umbrales | Hipótesis educativa, sin segmentación económica por cuenta/sector, efecto causal ni permiso de invertir |
| Filtros del reto | Período exacto, industria conocida/desconocida, empresa y rangos de score; fuente/tipo/estado para inspección | Geografía, cluster, producto y canal sin soporte deshabilitados o pendientes; source_type no es canal |

Streamlit opcional, cinco vistas, semántica de filtros, economía de solo lectura y flujo offline/Atlas quedan propuestos en CT-01 a CT-05 y DEC-011. No reinterpretar la obligatoriedad del entregable como aprobación técnica/visual. La misión termina en PR borrador para decisión del usuario, no en tablero funcional ni evaluación causal.
