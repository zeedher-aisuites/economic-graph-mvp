# Product Brief — v1.0

**Producto:** ConectaPyME Economic Intelligence\
**Tipo:** PoC local, operada por humanos\
**Escenario:** ConectaPyME Telecom, Distrito Centro, Villa Conecta (todo ficticio)\
**Horizonte:** 3 días

## 1. Problema y oportunidad

**Problema priorizado:** baja eficiencia potencial en adquisición comercial B2B. Un analista puede tener un listado de PyMEs con información incompleta y pocas señales para decidir a quién contactar primero.

No se presenta este diagnóstico como hallazgo real: debe sostenerse en los datos del caso simulado y distinguirse de la futura verificación con una Telco real.

**Pregunta de producto:** ¿puede un usuario priorizar prospectos con mejores argumentos si ve sus características y sus relaciones económicas, en lugar de una lista aislada?

## 2. Usuario y trabajos principales

**Usuario principal: analista comercial B2B.** Quiere filtrar prospectos, comprender sus necesidades posibles, inspeccionar relaciones y generar un orden de contacto explicable.

**Usuario secundario: gerente comercial.** Quiere observar funnel, calidad de señales y un marco de medición de impacto económico.

La decisión de contactar, ofrecer o descartar sigue siendo **humana**.

## 3. Propuesta de valor

> Ayudar a elegir **qué PyMEs explorar primero y por qué**, usando señales empresariales y relacionales auditables.

Una relación no prueba intención de compra. El ranking solo apoya el juicio comercial.

## 4. Hipótesis a evaluar

- **H1 — Información:** un grafo puede representar y consultar vínculos útiles entre empresas y mantener su procedencia y temporalidad.
- **H2 — Decisión:** las señales relacionales cambian de modo explicable la prioridad de algunos prospectos respecto a un baseline razonable.
- **H3 — Economía (solo diseño de validación):** una estrategia enriquecida podría aumentar el margen comercial neto frente al proceso actual, una vez evaluada experimentalmente.

**H1 y H2** pueden ilustrarse en datos sintéticos; **H3 no se demuestra con 30 empresas inventadas**.

## 5. Recorrido mínimo

1. El analista consulta el catálogo de empresas.
2. Selecciona una empresa y examina atributos y relaciones disponibles.
3. Compara un **baseline** de priorización con una variante enriquecida por señales del grafo.
4. Inspecciona las razones del orden sugerido.
5. Consulta indicadores mínimos o tablas para discutir calidad de datos, funnel y escenarios.

La interfaz puede ser **tablas y gráficos reproducibles**; Streamlit es opcional. No se exige una aplicación web sofisticada.

## 6. Funciones necesarias (priorización)

| Nivel | Capacidad | Evidencia mínima |
|---|---|---|
| P0 | Datos sintéticos coherentes | 30 empresas, relaciones, identificadores y fechas válidas |
| P0 | Grafo consultable | Consultas de nodos y conexiones con procedencia |
| P0 | Comparación de estrategias | Baseline vs. ranking con señales relacionales, resultados explicados |
| P0 | Caso económico y experimento | Fórmula, supuestos y estrategia de atribución causal |
| P0 | Trazabilidad del reto | Seis secciones cubiertas y defendibles |
| P1 | Visualización sencilla | Grafo o diagrama comprensible |
| P0 | Control Tower, dashboard o prototipo | Cadena de cuatro dimensiones con vínculo entre desempeño, decisión, acción y resultado; interfaz elaborada opcional |
| P2 | UX avanzada, filtros elaborados | No indispensable para la defensa |

**P0 = obligatorio, P1 = deseable, P2 = prescindible.**

## 7. Medición de éxito

**PoC técnica:** integridad de datos, consultas repetibles, procedencia, ausencia de fuga temporal y rankings auditables.

**Comparación exploratoria:** cambios de prioridad, calidad de explicación y resultados sobre datos sintéticos; las cifras no son evidencia de generalización.

**Éxito económico futuro:** margen incremental atribuible neto de costos adicionales, estimado respecto a un grupo de control comparable; también monitorear conversión, CAC, cobertura comercial y retención si aplica.

## 8. Criterios de aceptación del MVP

- Se puede reproducir el conjunto sintético con una semilla documentada.
- Las 30 empresas y sus relaciones están almacenadas o disponibles para consultas repetibles.
- El método enriquecido utiliza **solo relaciones y atributos observables a la fecha de decisión**.
- Hay dos métodos claros de priorización y una tabla que permite compararlos.
- Los resultados explican al menos qué variables influyeron en el ranking.
- La presentación cubre los seis apartados del reto y explica cómo medir incrementalidad real.
- La documentación diferencia **implementado**, **simulado** y **propuesto**.

## 9. Fuera de alcance

Agentes de IA, LLM, LangGraph, LangChain, campañas autónomas, integraciones de CRM real, GNN, autenticación empresarial, despliegue productivo, desarrollo de interfaz elaborada y prueba causal con clientes reales.

## 10. Incertidumbres explícitas

Pendiente de diseño: estructura exacta de datos, tipos y cantidad de relaciones, fuentes simuladas, reglas de generación del historial, método de scoring, visualización y supuesto económico de referencia. **No inventar estas definiciones en la documentación antes de acordarlas.**
