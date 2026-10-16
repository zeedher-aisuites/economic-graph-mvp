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
| P-005 | Baseline | Variables, regla o fórmula y justificación |
| P-006 | Grafo enriquecido | Features relacionales admisibles y explicaciones |
| P-007 | Evaluación offline | Corte temporal, resultados posibles y limitaciones |
| P-008 | Caso económico | Horizonte, margen, costos, capacidad comercial y escenarios |
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
