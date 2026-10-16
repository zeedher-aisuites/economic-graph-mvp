# Alcance y registro de decisiones — v1.0

Este documento separa decisiones ya aceptadas, propuestas de implementación y cuestiones pendientes. **No interpretar lo pendiente como aprobado.**

## 1. Decisiones aprobadas

| ID | Decisión | Razón / consecuencia |
|---|---|---|
| D-001 | Prioridad absoluta: reto laboral del Economic Graph y valor económico incremental | La solución y la defensa se evalúan frente a esa pregunta |
| D-002 | PoC pequeña con fuerte justificación económica, arquitectónica y experimental | Tres días no permiten construir producción y evaluarla realmente |
| D-003 | Un único escenario ficticio: ConectaPyME Telecom, Distrito Centro de Villa Conecta | Facilita un relato empresarial coherente |
| D-004 | 30 empresas ficticias en el MVP | Alcance acotado, fácil de inspeccionar; sin pretensión estadística |
| D-005 | Uso directo por analista/gerente; **sin agentes** por ahora | Evita dependencia de LLM y autonomía innecesaria |
| D-006 | Datos sintéticos explícitos, reproducibles y separados de lo observable por la Telco | Evita datos ficticios presentados como evidencia real y fuga de información |
| D-007 | Comparar un baseline comercial con un enfoque enriquecido por relaciones | Permite discutir valor incremental del **método**, sin inventar efecto económico |
| D-008 | No presentar ROI ni uplift causal real derivados de la simulación | La causalidad requiere contrafactual y datos operacionales |
| D-009 | Código y documentación sencillos, profesionales y aptos para juniors | Mantenibilidad y defensa técnica |
| D-010 | Reutilizar para ICEméxico y aprendizaje solo de forma secundaria | Proteger tiempo y alcance del reto |
| D-011 | Misión 001: Python >=3.11, uv, PyMongo, python-dotenv, pytest y Ruff; conexión de solo verificación | Aprobación explícita del usuario; sin instalar servidor MongoDB ni Docker |
| D-012 | Infraestructura inicial sin generación de datos, grafo, scoring ni analítica | La implementación funcional del MVP requiere misiones posteriores |
| D-013 | Una presentación ejecutiva principal de aproximadamente 10–12 diapositivas | Se crea una estructura de 12; sin resultados inventados |
| D-014 | Misión 002B: implementar los paquetes aprobados de diseño, catálogo, relaciones y observabilidad | 30 empresas, 48 relaciones, 3 afirmaciones falsas, 3 referencias y 83 observaciones; no inventar hechos |
| D-015 | Construir solo conocimiento observable en fechas explícitas, separado del simulador | 12/17/23 empresas; consultas por disponibilidad; sin scoring, eventos, economía ni Control Tower |
| D-016 | Misión 003A: política `003a-conservative-v1`, elegibilidad y K=5 aprobados expresamente | Baseline y grafo comparables implementados; DEC-009 y `12-commercial-ranking.md`; no demuestra efecto económico |
| D-017 | Misión 003B, primera fase: exclusivamente diseño económico y experimental en PR borrador | No autoriza supuestos financieros, simulador, eventos ni experimento real |
| D-018 | 003B, aprobación provisional educativa ECO-01 a ECO-06 y calculador determinista | Escenarios, sensibilidad y equilibrio autorizados; metodología no calibrada, sin finanzas reales, datos/contactos, presupuesto, piloto ni despliegue |

## 2. Propuestas técnicas, no decisiones cerradas

- Python, MongoDB/PyMongo, Git/GitHub y `uv` quedan **aprobados para la infraestructura de la misión 001** por instrucción expresa del usuario; ver D-011. Esto no aprueba el esquema de datos ni una arquitectura de producción.
- **Editor:** VS Code es una opción local, no un requisito.
- **Análisis de grafos:** Python; NetworkX solo si simplifica una necesidad real.
- **Presentación interactiva:** Streamlit **opcional**; tablas y gráficos bastan cuando responden mejor al reto.
- **Escenario temporal:** hasta 12 meses de historial comercial sintético, sujeto a un generador sencillo y a las necesidades de evaluación.
- **Visualización:** un diagrama pequeño que explique la topología, si queda tiempo.

La elección final se documentará cuando exista diseño de datos y tarea concreta.

## 3. No construir en estos tres días

- Agentes, LangGraph, LangChain, LLM y ejecuciones autónomas.
- Ingesta de fuentes reales no autorizadas, scraping masivo ni integraciones con CRM real.
- Graph neural networks, plataformas distribuidas o arquitectura de microservicios.
- Sistema de autenticación/roles de producción, despliegue cloud público y aplicación móvil.
- Frontend complejo, editor de grafos o automatizaciones comerciales.
- Datos sintéticos masivos para inflar artificialmente la cantidad de filas.

## 4. Pendientes de decisión (no inventar)

| ID | Tema | Decisión requerida antes de implementar |
|---|---|---|
| P-001 | Modelo conceptual | Aprobado para 002B en `06-economic-graph-design.md`; evento comercial permanece sin materializar |
| P-002 | Fuentes sintéticas | Aprobadas cinco fuentes y 83 observaciones en `09-observability-plan.md`; no se infieren tasas reales |
| P-003 | Identidad y temporalidad | Aprobados cortes y candidatos; se conservan alias sin fusión fuerte ni evidencia inventada |
| P-004 | Historia comercial | Estados, eventos, políticas de contacto y resultados |
| P-005 | Baseline | Resuelto para 003A: regla aprobada e implementada; no cambiarla en 003B |
| P-006 | Grafo enriquecido | Resuelto para 003A: vecinos económicos confirmados distintos; ver DEC-009 |
| P-007 | Evaluación offline | Comparación temporal 003A implementada; efectividad comercial y causalidad no verificadas |
| P-008 | Caso económico | ECO-01 a ECO-06 aprobadas provisionalmente solo para metodología PoC; calculador implementado. Efecto causal, muestra y aplicación financiera/operativa real no verificados ni autorizados |
| P-009 | Presentación | Estructura inicial de 12 diapositivas autorizada en misión 001; contenido final y brief de 2–3 páginas pendientes |

## 5. Condiciones de cambio

Una nueva funcionalidad debe responder a un entregable del reto (`docs/02-challenge-traceability.md`), tener un criterio de aceptación verificable y caber en el tiempo disponible. Registrar cambios que afecten el alcance en este archivo.

## 6. Significado de «terminado»

**Implementado**: código ejecutado y verificado.\
**Simulado**: datos/eventos artificiales, identificados como tales.\
**Calculado**: número derivado mediante una fórmula visible y supuestos declarados.\
**Propuesto**: arquitectura, proceso o experimento aún no ejecutado.

## 7. Estado después de inicializar la misión 001

Implementado: paquete Python, lectura de configuración, cliente y `ping`, pruebas unitarias y herramientas de calidad. No hay colecciones, datos ni algoritmos del Economic Graph.

El detalle de decisiones relevantes se mantiene en `../presentations/decision-log.md`. La selección de Python 3.12 en `.python-version` es una elección técnica compatible con el mínimo 3.11 aprobado. No altera el alcance del producto.

Contraste con el reto: Control Tower obligatoria como dashboard o prototipo; brief final de 2–3 páginas pendiente. Ver referencias y discrepancias en `02-challenge-traceability.md`. No se cambia ningún pendiente de datos o análisis por conveniencia de implementación.

## 8. Ampliación autorizada en misión 002B

El usuario aprobó diseño y paquetes adjuntos, que sustituyen los pendientes de aprobación de 002A para este alcance. La construcción y las consultas offline están implementadas, con detalle en `10-design-validation.md`. No se amplía historia comercial, scoring ni evaluación económica.

DV-002 y DV-003 registran ejemplos de fusión fuerte y transición/caducidad que no existen en los insumos: se detiene únicamente su generación. Una adenda de evidencia necesitará aprobación; no se cambia el plan de 83 registros para simular que esos ejemplos se ejecutaron.

## 9. Primera fase documental de misión 003B — histórica

La misión 003A ya está integrada en `main` y sus decisiones siguen vigentes. Esta fase de 003B desarrolla únicamente `14-incremental-economic-case.md` y `15-incrementality-experiment.md`, actualizando trazabilidad y comunicación. Las entradas numéricas son propuestas pedagógicas, no datos de mercado ni resultados del ranking. La aprobación requerida se registra por ECO-01 a ECO-06; el PR borrador no la sustituye.

No se programan cálculos, simulaciones ni eventos financieros; no se modifican políticas, código, pruebas, dependencias, ledger o Atlas. La siguiente implementación solo podrá comenzar tras una revisión y aprobación explícita de los supuestos y alcance.

## 10. Aprobación provisional y calculador 003B

La respuesta posterior del usuario al PR #5 autoriza provisionalmente ECO-01 a ECO-06 y un calculador financiero determinista. La aprobación es metodológica y exclusivamente para la PoC educativa: MXN, 90 días, doce meses, descuento mensual 1%, escenarios no observados, nulo obligatorio, reserva 20%, población conceptual y A/B futuro por bolsas independientes con ITT/IC95%/potencia objetivo80%. No hay muestra fijada sin varianza, ICC y datos comerciales.

`finance.py`, `calculate_finance.py` y `config/financial_assumptions.json` implementan aritmética agregada, sensibilidad y equilibrio. No generan ventas ni resultados de las 30 empresas. Separan cinco plazas y 500 plazas hipotéticas del protocolo futuro. No cambian rankings, ledger, oráculo, Atlas ni dependencias.

ECO-03/04/05 son aprobación de diseño, no permiso de ejecutar el experimento; ECO-06 no autoriza presupuesto, piloto o despliegue. El detalle está en `14-incremental-economic-case.md`. La entrega actualiza el PR #5 para revisión, sin integrarlo automáticamente.
