# Matriz de trazabilidad del reto — estado de entrega 005C

**Pregunta central:** ¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?

**Base auditada:** `main` en `c9194ed8425cc1f62eaac6174656a658810e6597`, merge del PR #6 verificado en GitHub. Control Tower 004B/004C integrada; las referencias históricas a revisiones pendientes no describen su estado actual.

**Fuente prioritaria:** [reto original](../presentations/references/Reto-AI-Engineering-SME-Economic-Graph.pptx), 13 diapositivas y notas. La diapositiva 4 contiene la pregunta central; 10–11 exigen las cuatro dimensiones de Control Tower y segmentación; 12 enumera seis entregables y un brief de 2–3 páginas; 13 pide defensa desde perspectiva de CEO. Las cifras de funnel/score de la presentación son ilustrativas, no resultados de esta PoC.

## Estado actual de los seis entregables

| Entregable | Cumplimiento demostrable en la PoC | Evidencia que falta |
|---|---|---|
| Business Framing | Hipótesis de adquisición B2B y mecanismo económico definidos | Validación del problema, demanda y restricciones con clientes reales |
| Economic Graph | Ledger observable, procedencia, cortes, conflictos e identidad candidata implementados | Identidad fuerte, evidencia para transiciones/caducidades y validación operacional |
| AI/ML Approach | Dos rankings deterministas comparables, explicables y reproducibles | Modelo predictivo entrenado, etiquetas y superioridad comercial; no se afirman |
| Architecture | Arquitectura PoC implementada offline; Atlas local reportado y UI integrada | Arquitectura productiva, roles, escala, gobierno operacional y MLOps condicional |
| Economic Case | Calculador, escenarios hipotéticos, sensibilidad, equilibrio y protocolo futuro | Costos calibrados, experimento A/B ejecutado y margen incremental/ROI real |
| Control Tower | Cinco vistas funcionales, red interactiva y Atlas manual de solo lectura | Eventos comerciales y métricas predictivas/económicas observadas |

Los seis bloques tienen soporte para una defensa de la PoC; **no equivalen a seis resultados de negocio demostrados ni a una entrega final sin pendientes**. El brief final aún requiere consolidación. La [ruta rápida del README](../README.md) instala desde `main`, prueba offline y reproduce UI, rankings y finanzas sin credenciales. Los comandos siguientes se ejecutan desde la raíz con el grupo UI instalado.

### 1. Business Framing

**Objetivo:** mejorar la priorización de cuentas B2B bajo capacidad comercial fija, explicando por qué explorar unas antes que otras.

**Evidencia documental:** [brief](01-product-brief.md), [caso económico](14-incremental-economic-case.md), [experimento futuro](15-incrementality-experiment.md) y [presentación ejecutiva](../presentations/executive-deck.md). La cadena postulada es información → selección → intervención humana → margen neto potencial.

**Código y reproducción:** `rankings.py`, `tower_read_model.py` y vistas Resumen/Business Funnel de `app/control_tower.py`; `uv run --group ui streamlit run app/control_tower.py` muestra 23 conocidas → 21 elegibles → 5 priorizadas en T2, con dos exclusiones aparte.

**Estado y límite:** framing definido y demostración sintética implementada; sin entrevistas, clientes/contactos reales ni validación comercial. Servicio desconocido no equivale a no-cliente. Contactos, oportunidades, activaciones y ventas permanecen **No observado**, sin ceros inventados.

### 2. Economic Graph

**Objetivo:** reconstruir qué sabe la Telco, desde cuándo, con qué fuente y con qué incertidumbre.

**Evidencia documental:** [diseño](06-economic-graph-design.md), [catálogo](07-company-catalog.md), [relaciones](08-relationship-matrix.md), [observabilidad](09-observability-plan.md), [auditoría DV-001 a DV-005](10-design-validation.md) y [validación Atlas reportada](11-atlas-integration-validation.md).

**Código y reproducción:** `src/economic_graph/observable.py`, `mongo_observable.py`, `data/observable/observations.json` y `scripts/inspect_graph.py`. Ejecutar `uv run --group ui python scripts/inspect_graph.py --as-of T2 --summary`, repitiendo T0/T1. Empresas 12/17/23, observaciones 28/54/83, afirmaciones económicas 2/13/26 y referencias 0/2/3. T2 conserva dos candidatos de identidad y dos atributos en conflicto.

**Estado y límite:** construcción, consultas, historia y procedencia implementadas; lectura Atlas T2 posterior al merge reportada por el usuario. Cortes a las 12:00 UTC de 2026-01-15/05-15/09-15 con `available_at <= as_of`. El diseño restringido contiene 30 empresas/48 relaciones verdaderas/3 afirmaciones falsas/3 referencias; no alimenta scoring o UI. Siete empresas y 25 relaciones verdaderas quedan desconocidas en T2; esos últimos son conteos de auditoría restringida, no métricas comerciales. No se fusionan candidatos ni se inventan cambios de estado o eventos comerciales.

### 3. AI/ML Approach

**Objetivo:** comparar, con las mismas cuentas y K=5, la selección basada en atributos individuales frente a la enriquecida con relaciones observables.

**Evidencia documental:** [política aprobada y conceptos](12-commercial-ranking.md), [tablas T0/T1/T2](13-ranking-comparison.md), DEC-009 en el [registro de decisiones](../presentations/decision-log.md).

**Código y reproducción:** `src/economic_graph/rankings.py`, `scripts/rank_companies.py`, `tests/test_rankings.py` y `tests/test_ranking_commands.py`; `uv run --group ui python scripts/rank_companies.py --all-cuts --format markdown`.

**Estado y límite:** `003a-conservative-v1` implementada sin oráculo ni fuga temporal; elegibles 12/17/21. Baseline por sucursales adicionales sin conflicto; grafo agrega vecinos económicos distintos confirmados utilizables. Afirmaciones reportadas/inferidas y referencias no aportan puntos. Cada corte conserva dos selecciones compartidas y tres sustituciones; desempate por ID y empates se declaran. Café Jacaranda en T2: baseline posición 10/score 0, grafo posición 3/score 10 y dos vecinos utilizables. **Son reglas, no probabilidades ni modelo entrenado**; cambiar selección no demuestra mayor conversión ni efecto causal. Rankings T2 en UI Atlas fueron reportados por el usuario; no se reportó ejecución independiente de la CLI `--mongo` ni nueva ejecución cloud contra Atlas.

### 4. Architecture

**Objetivo:** separar verdad sintética, observaciones disponibles, lógica de dominio, persistencia opcional y presentación, con trazabilidad y reproducción local.

**Evidencia documental:** [arquitectura](04-architecture-overview.md), [auditoría de materialización y persistencia](10-design-validation.md), [evidencia Atlas](11-atlas-integration-validation.md) y [diseño UI](17-control-tower-design.md). Algunas cabeceras históricas de estos diseños aún requieren actualización fuera de 005C; esta matriz distingue el estado vigente.

**Código y reproducción:** `config.py`, `database.py`, `observable.py`, `mongo_observable.py`, `rankings.py`, `finance.py`, `tower_read_model.py` y `app/control_tower.py`, dentro de `src/economic_graph/` salvo la app. `uv sync --locked --group ui` y `uv run --group ui pytest -m "not integration"` verifican la PoC sin Atlas. Fuente offline predeterminada; `--mongo` y UI Atlas son lecturas explícitas opcionales, con base dedicada y sin fallback silencioso.

**Estado y límite:** arquitectura PoC implementada con separación de archivos/interfaces y fuentes únicas de cálculos; no es aislamiento operativo por roles de producción. Carga protegida explícita e idempotencia local reportadas en 002C, no repetidas en 005C. Producción es propuesta: fuentes autorizadas → ingestión/calidad/identidad → historial gobernado → serving/acceso por roles → monitoreo y MLOps solo si hubiera modelos. No se verifican escala, latencias objetivo, seguridad integral o conectividad cloud con Atlas.

### 5. Economic Case

**Objetivo:** identificar qué mejora de margen neto justificaría los costos incrementales y cómo medirla frente a un contrafactual.

**Evidencia documental:** [fórmulas y supuestos](14-incremental-economic-case.md), [protocolo futuro](15-incrementality-experiment.md), [resultados hipotéticos](16-financial-calculation.md) y ECO-01 a ECO-06/DEC-004/010. Aprobación provisional, exclusivamente metodológica para la PoC educativa; no validación financiera ni autorización operativa.

**Código y reproducción:** `src/economic_graph/finance.py`, `config/financial_assumptions.json`, `scripts/calculate_finance.py`, `tests/test_finance.py` y `tests/test_finance_commands.py`; `uv run --group ui python scripts/calculate_finance.py --format markdown` y el mismo comando con `--sensitivity`.

**Estado y límite:** calculador determinista implementado: MXN nominales, 90 días de activación, doce meses, descuento mensual 1% y reserva 20%. Conservador/base/optimista/nulo, costos sin duplicación, sensibilidad y equilibrio; cinco plazas separadas de 500 hipotéticas y del experimento. No lee empresas ni fabrica ventas por cuenta. Con 500, base +39 000 MXN y nulo −41 000 MXN antes de reserva son hipótesis; 1.025 pp es umbral base requerido, no logrado. No hay ROI real ni A/B ejecutado. Diseño futuro 1:1 por bolsas independientes, KPI neto comercial por cuenta elegible asignada, ITT, IC95% y potencia objetivo80%; sin tamaño muestral por falta de varianza/ICC, y causalidad inviable si faltan bolsas independientes. Sin autorización de contactos, datos reales, presupuesto, piloto o despliegue.

### 6. Control Tower

**Objetivo:** conectar salud del grafo → comparación de políticas → decisión de priorización → hipótesis económica, mostrando qué falta observar.

**Evidencia documental:** [diseño e indicadores](17-control-tower-design.md), [guía/guion actual desde main](18-control-tower-demo.md), aprobación CT-01 a CT-05 y criterios CT-A01 a CT-A13. `app/control_tower.py`, `src/economic_graph/tower_read_model.py`, `tests/test_control_tower.py` y `tests/test_tower_read_model.py` implementan y verifican las vistas.

| Vista / dimensión del reto | Evidencia implementada | Limitación visible |
|---|---|---|
| Resumen | Hallazgo tres sustituciones, top-5, indicadores y escenarios | Cambio de selección no demuestra ventas |
| Graph Health | Red temporal, estados, procedencia, frescura, conflictos y candidatos | Sin precisión de identidad, verdades ocultas ni fusión automática |
| AI Performance | Comparación, scores, aportes, empates y cobertura | Sin precision/recall, lift comercial, calibración o drift predictivo medidos |
| Business Funnel | Conocidas, elegibles, priorizadas y exclusiones | Contactos/activaciones/oportunidades/ventas No observado |
| Economic Impact | Cuatro escenarios, reserva, sensibilidad y equilibrio | Hipótesis educativas; sin ingresos, CAC, LTV, ROI o payback reales |

**Reproducción y estado:** `uv run --group ui streamlit run app/control_tower.py`; Resumen/T2/Offline al iniciar. Interfaz integrada en `main`, cinco vistas y lectura Atlas de solo lectura confirmadas por reporte local del usuario. Filtros soportados: período, industria, empresa, score y evidencia según vista, sin recalcular rankings globales. Geografía, cluster, producto y canal quedan deshabilitados por falta de datos; `source_type` no es canal. Las finanzas no se segmentan por cuenta/corte. No es un tablero productivo ni un sistema comercial autónomo.

## Validaciones y procedencia de la evidencia actual

| Procedencia | Resultado y alcance |
|---|---|
| Usuario, Windows 11 / PowerShell / VS Code, `main`/`c9194ed` | Instalación correcta; 284 aprobadas, una integración excluida; Ruff correcto, 60 archivos con formato; cinco vistas funcionales; ping, lectura Atlas T2 y captura UI Atlas reportados. Detalle en [validación Atlas](11-atlas-integration-validation.md) |
| Codex Cloud/Linux, auditoría 005C sobre esa base | Instalación UI con lockfile, 284 aprobadas/una integración excluida, Ruff y formato correctos (60); CLI offline T0/T1/T2, rankings y finanzas reproducidas. Sin acceso Atlas, ejecución Windows ni nueva revisión de navegador |

No se confunden datos sintéticos observables, ejecuciones técnicas, supuestos financieros y resultados que solo un experimento real podría medir. El laboratorio CRM independiente de 240 prospectos no está incorporado ni forma parte de las 30 empresas del grafo. Ninguna prueba offline acredita un experimento A/B, ventas o ROI.

## Pendientes de entrega y hallazgos fuera del alcance 005C

Esta auditoría modifica solo README, esta matriz, validación Atlas y guía de demo. Se registran las siguientes inconsistencias sin cambiar otros archivos:

| Documento | Hallazgo que requiere revisión posterior |
|---|---|
| [Brief](01-product-brief.md), sección 10 | Aún enumera modelo, fuentes, scoring y visualización como pendientes de diseño; la aceptación exige semilla aunque la materialización es determinista sin azar |
| [Alcance](03-scope-and-decisions.md), P-010 y sección 13 | Presenta revisión Windows/merge del PR #6 como pendientes; debe distinguirlos del historial legítimo de D-019/004A |
| [Arquitectura](04-architecture-overview.md), cabecera y sección 10 | Conviven diseño preliminar, Control Tower pendiente e implementación posterior; revisión Windows figura pendiente |
| [Guía de rankings](12-commercial-ranking.md), lectura Atlas y portabilidad | Falta incorporar el reporte posterior de UI Atlas T2/Windows; no extrapolarlo a una ejecución independiente de la CLI `--mongo` |
| [Diseño UI](17-control-tower-design.md), aceptación y pulido | La revisión nativa Windows aún figura pendiente |
| [Decisiones](../presentations/decision-log.md), DEC-003/009/011; [deck](../presentations/executive-deck.md), lámina 10; [AGENTS](../AGENTS.md), alcances 004B/004C | Conservan pendientes de revisión Windows/PR #6 o evidencia Atlas anterior; requieren contextualización, sin reaprobar decisiones |

Pendientes materiales: consolidar brief final de 2–3 páginas y defensa final, alinear esos estados históricos y, para evaluar valor real, obtener datos comerciales autorizados, identidad/cobertura/permisos y costos calibrados antes de considerar el experimento. No se amplía alcance ni se autorizan operaciones.

## Historial de trazabilidad por misión

**Contexto histórico:** las secciones siguientes conservan lo registrado al cierre de cada misión. Expresiones como «pendiente», «sin scoring», «sin interfaz» o «PR sin integrar» describen aquella etapa y quedan sustituidas, para el estado actual, por la matriz y las evidencias anteriores. Se preservan porque permiten seguir la evolución del proyecto, no porque hoy falten rankings, calculador o Control Tower.

### Misión 001 — contraste histórico con la fuente

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

### Evidencia de misión 002B

El diseño de `06-economic-graph-design.md` y los tres paquetes fueron aprobados explícitamente. `10-design-validation.md` registra procedencia, invariantes y discrepancias con IDs. No se considera implementada una fusión, transición o caducidad ausente en el plan aprobado.

| Bloque | Evidencia implementada | Límite |
|---|---|---|
| Economic Graph | 30 empresas/48 relaciones en fuentes restringidas; 83 observaciones materializadas; vistas T0/T1/T2 con empresas 12/17/23; historia, procedencia, conflictos y alias candidatos | 7 empresas y 25 relaciones verdaderas permanecen desconocidas; no se revelan a la interfaz comercial |
| Architecture | `simulator/design.py` audita todos los archivos; `simulator/project.py` proyecta sin enriquecer desde el catálogo; `observable.py` consulta solo el ledger público | Separación por archivos e interfaces; roles comerciales de Atlas no provisionados y sin validación a escala |
| Architecture / persistencia | `mongo_observable.py` limita base y colecciones, rechaza contenido ajeno y usa inserciones inmutables por ID; prueba de idempotencia offline | Al cierre de 002B no se había ejecutado carga en Atlas; el reporte local posterior se registra en 002C |
| Graph Health como evidencia de calidad | Pruebas de IDs, enlaces huérfanos, tipos, tiempos, incertidumbre, duplicados, ausencia de verdad y desconocidos | No es una Control Tower implementada ni precisión medida de entity resolution |
| AI/ML, economía y funnel | Contratos y límites documentados | Sin scoring, ML, eventos, conversiones, causalidad ni valor económico medido |

Pruebas relevantes: `tests/test_design.py`, `test_observable.py`, `test_mongo_observable.py` y `test_graph_commands.py`. La integración está separada en `tests/integration/test_atlas_observable.py`. Las 2/11/23 relaciones verdaderas observadas son un conteo restringido de validación del simulador, no una métrica comercial de confirmaciones.

### Evidencia de misión 002C — integración local reportada

Fuente: [validación Atlas](11-atlas-integration-validation.md), resultados comunicados por el usuario desde Windows con VS Code. No se atribuyen a ejecuciones de Codex Cloud.

| Requisito | Evidencia local reportada | Límite |
|---|---|---|
| Architecture: conexión y persistencia | PyMongo y ping exitosos; primera carga de 83 observaciones | No demuestra conectividad desde Codex Cloud ni rendimiento a escala |
| Architecture: carga repetible | Segunda carga: 0 insertadas, 83 sin cambios | Valida la repetición reportada, sin ampliar la afirmación a escenarios no ejecutados |
| Economic Graph: consultas observacionales | T0: 12 empresas/28 observaciones; T1: 17/54; T2: 23/83 | No añade evidencia de identidad fuerte ni resultados de relaciones no reportados |
| Calidad del diseño | `validate_design.py`: 0 errores y 5 advertencias conocidas | DV-001 a DV-005 permanecen documentadas |

Este cierre no incorpora funcionalidades ni resultados de scoring, funnel, economía, causalidad o Control Tower. La evidencia técnica no se convierte en valor económico incremental demostrado.

### Evidencia de misión 003A — rankings comparables

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

### Evidencia de misión 003B — calculador educativo y protocolo futuro

Se releyeron las 13 diapositivas y notas del reto original desde `main` en `0e1088c`. Tras revisar el PR #5, el usuario aprobó provisionalmente ECO-01 a ECO-06 solo como metodología educativa y autorizó el calculador determinista. [Caso económico](14-incremental-economic-case.md), [protocolo futuro](15-incrementality-experiment.md) y [resultados hipotéticos](16-financial-calculation.md) desarrollan el bloque 5. Las cifras del reto y los cambios de ranking no se usan como tasas de conversión.

| Requisito | Diseño entregado | Evidencia que sigue faltando |
|---|---|---|
| Business Framing → margen | Igual capacidad; margen neto de ventas y costo comercial, efectos sobre no seleccionadas y costo incremental de datos/plataforma | Demanda, producto/cobertura, permisos, conversión, margen y costos reales |
| Economic Case: reproducibilidad | `finance.py`, CLI offline y supuestos versionados: escenarios conservador/base/optimista/nulo, sensibilidad, equilibrio y reserva; unidades, valoración, IDs de costos y decimales validados | Aprobación exclusivamente provisional/metodológica; sin fuentes financieras reales ni ROI causal |
| Economic Case: contrafactual | Diseño futuro por bolsas 1:1, asignación previa a selección, KPI neto por cuenta elegible asignada, ITT, IC95% y potencia objetivo80%, madurez y control de contaminación | Sin población operativa autorizada, varianza/ICC, muestra, ejecución o resultados; inferencia inviable si faltan bolsas independientes suficientes |
| Control Tower: definición futura | KPI económico y métricas secundarias con requisitos de medición | Eventos comerciales, instrumentación y dashboard/prototipo no implementados |

DEC-004/010 registran aprobación provisional metodológica y límites. Cinco plazas de demostración, 500 hipotéticas y experimento futuro son niveles separados; T0/T1/T2 no se convierten en cohortes independientes. El nulo conserva costos y pierde dinero con las entradas aprobadas; los casos positivos no autorizan invertir. Las nuevas pruebas matemáticas/CLI están en `test_finance.py` y `test_finance_commands.py`; no se modifican rankings, ledger, Atlas ni dependencias. No se generan eventos comerciales o ventas por empresa. Datos reales, contactos, presupuesto, piloto y despliegue siguen sin autorizarse. El PR #5 queda listo para revisión sin integración automática.

### Propuesta de misión 004A — Control Tower sin interfaz implementada

Desde `main` en `8e39c8b`, con PR #5 ya integrado, se revisaron reto original (diapositivas/notas 10–12), módulos y evidencia. [Diseño de Control Tower](17-control-tower-design.md) detalla arquitectura visual/técnica, cinco vistas, diccionario de indicadores, filtros, fuentes existentes, trazabilidad, fallos y CT-A01 a CT-A12. No se instalan dependencias ni se programa UI.

| Dimensión obligatoria | Propuesta verificable contra fuentes actuales | Límite explícito |
|---|---|---|
| Graph Health | Snapshot y resumen por corte: empresas, afirmaciones y referencias separadas, estados, fuentes, conflictos, candidatos y frescura descriptiva | Sin denominador privado, confianza numérica inventada ni fusiones/verdad inferidas del simulador |
| AI Performance | Informe 003A: posiciones y contribuciones, top-5, cambios, cobertura y empates | Comparación de reglas sin modelo; no etiquetas para precision/recall/lift/calibración |
| Business Funnel | Conocidas, elegibles, priorizadas por una política y exclusiones; segmentación descriptiva | Contactos, oportunidades, activaciones y ventas como No observado, sin ceros/tasas fabricadas |
| Economic Impact | Informe 003B: cinco/500 plazas, cuatro escenarios, sensibilidad y umbrales | Hipótesis educativa, sin segmentación económica por cuenta/sector, efecto causal ni permiso de invertir |
| Filtros del reto | Período exacto, industria conocida/desconocida, empresa y rangos de score; fuente/tipo/estado para inspección | Geografía, cluster, producto y canal sin soporte deshabilitados o pendientes; source_type no es canal |

Streamlit opcional, cinco vistas, semántica de filtros, economía de solo lectura y flujo offline/Atlas quedan propuestos en CT-01 a CT-05 y DEC-011. No reinterpretar la obligatoriedad del entregable como aprobación técnica/visual. La misión termina en PR borrador para decisión del usuario, no en tablero funcional ni evaluación causal.

### Implementación 004B — aprobación posterior y evidencia de Control Tower

El usuario aprobó CT-01 a CT-05 y amplió CT-02 con red económica interactiva sencilla. `app/control_tower.py` y `tower_read_model.py` implementan cinco vistas y adaptación pública; Streamlit opcional y Vega-Lite integrado no añaden motor de grafos. [Diseño actualizado](17-control-tower-design.md) y [guía/guion](18-control-tower-demo.md) documentan CT-A01 a CT-A13.

| Dimensión | Evidencia implementada | Límite conservado |
|---|---|---|
| Graph Health | Red al corte, selector sincronizado, conexiones directas, tipos/estados/procedencia, evolución, conflictos y candidatos | Sin oráculo, fusión de alias, resolución fuerte ni exactitud inventada |
| AI Performance | Paridad con 003A, posiciones globales, aportes, top-5/cambios, empates y cobertura | Sin probabilidades, métricas predictivas o superioridad comercial demostrada |
| Business Funnel | Conocidas/elegibles/excluidas/priorizadas; segmento intersectado con selección global | Etapas comerciales No observado; sin ventas, contactos ni tasas fabricadas |
| Economic Impact | Cuatro escenarios cinco/500, reserva, sensibilidad y equilibrio tomados de 003B | Hipótesis educativas de solo lectura, independientes de filtros; no efecto causal ni inversión autorizada |
| Fuentes/filtros | Ledger offline predeterminado, Atlas manual solo `find` y hash de paridad; cortes exactos y segmentos descriptivos | Sin escrituras, respaldo silencioso, filtros sin soporte ni nueva lectura Atlas real verificada |

Pruebas automáticas de adaptador/AppTest, regresión aislada sin red/env/simulador y revisión Chromium Linux. No equivalen a ejecución nativa Windows: el usuario validará visualmente y contrastará resultados antes de integrar PR #6. No cambian ledger, políticas ni supuestos aprobados; brief final y experimento real siguen pendientes.

Portabilidad de la suite 004B: tras reporte Windows de 269 aprobadas/un fallo/un error, se separan importaciones nativas del límite AppTest y se permite solo el IPC `socketpair`, conservando bloqueo de conexiones externas y separación física de datos privados. Los 271 casos se conservan y pasan en Linux; timeout de 15 segundos intacto y pila segura si persiste. Diagnóstico y alcance de evidencia en la guía 004B; nueva ejecución nativa Windows pendiente. Sin cambios de datos, reglas, finanzas o Atlas.

### Pulido 004C — legibilidad ejecutiva del bloque 6

El usuario confirmó posteriormente 271 pruebas aprobadas y funcionamiento Windows de 004B. Esta misión mejora presentación: hallazgo tres de cinco, red centrada con evidencia de feature resaltada, matriz de dos compartidas/tres sustituciones, funnel visual con exclusiones aparte y cuatro escenarios hipotéticos con signo y umbral visible. Paneles contraídos mantienen auditoría de ranking, procedencia, conflictos, incertidumbre, sensibilidad y finanzas; filtros no recalculan decisiones.

Pruebas de regresión amplían foco al corte, conmutación de vistas/escalas, restablecimiento global, estados de paneles y paridad de evidencia resaltada. Se revisa Chromium a 1366×900, sin añadir dependencias. La nueva validación visual Windows queda pendiente; no es nueva evidencia de ventas, causalidad, Atlas, reglas o supuestos. Detalle en `18-control-tower-demo.md` y diseño v3.
