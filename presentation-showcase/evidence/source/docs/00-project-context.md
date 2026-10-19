# Contexto del proyecto — v1.0

**Fecha:** 15 de octubre de 2026\
**Proyecto:** ConectaPyME Economic Intelligence (SME Economic Graph)\
**Naturaleza:** caso ficticio + prueba de concepto técnica\
**Plazo de trabajo:** tres días

## Pregunta rectora

> **¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?**

**Esta pregunta es la prioridad absoluta.** La utilidad del prototipo se juzga por cuánto ayuda a contestarla, no por cuántas herramientas incorpora.

## Motivación y contexto

El trabajo responde a un **reto laboral de AI Engineering** en un escenario Telco–PyMEs. Se decidió concentrar el caso de uso en **baja eficiencia de adquisición B2B**: el equipo comercial necesita identificar y priorizar mejor los prospectos y justificar dónde dedicar su esfuerzo.

Como ejercicio de ingeniería se crea una empresa ficticia, **ConectaPyME Telecom**, y una localidad ficticia llamada **Distrito Centro**, situada en **Villa Conecta**. El conjunto inicial tiene **30 empresas sintéticas** de varios sectores con atributos y relaciones económicas plausibles.

La simulación permitirá mostrar cómo podrían conectarse datos empresariales y comerciales, cómo extraer señales útiles y cómo plantear una medición de valor incremental. **No representa datos, clientes ni resultados reales de ninguna Telco.**

## Qué debe quedar respondido

1. **Business Framing:** problema comercial, hipótesis de valor y métricas relevantes.
2. **Economic Graph:** nodos, relaciones, fuentes, identidad, tiempo, confianza y procedencia.
3. **AI/ML Approach:** baseline, enfoque propuesto, entrenamiento/evaluación/inferencia cuando corresponda, y decisión de cuándo NO usar ML.
4. **Architecture:** flujo de extremo a extremo y propuesta de evolución a escala, serving, MLOps y gobierno.
5. **Economic Case:** de dónde surgiría el margen incremental neto y cómo se atribuiría causalmente.
6. **Control Tower:** Graph Health, AI Performance, Business Funnel y Economic Impact.

Estos seis apartados se contrastaron con la presentación original del reto (diapositiva 12). La entrega final requiere un brief de 2–3 páginas y la presentación de la propuesta; la Control Tower es obligatoria como dashboard o prototipo. Véase `02-challenge-traceability.md` para fuentes y alcance por misión.

## Estrategia de respuesta

- **Demostración local pequeña:** datos sintéticos reproducibles, consultas de un grafo económico y dos formas comparables de ordenar prospectos.
- **Defensa técnica y arquitectónica:** decisiones y alternativas, limitaciones, diseño de sistema de producción sin prometer haberlo implementado.
- **Defensa económica y experimental:** modelo de costos/márgenes y plan para probar impacto incremental mediante experimento real.

La demostración no pretende «probar ROI» usando empresas inventadas: servirá para comprobar que el proceso y las señales son técnicamente viables.

## Usuarios y operación

- **Analista comercial:** consulta empresas y relaciones; revisa ranking y explicación.
- **Gerente comercial:** supervisa indicadores, funnel y escenarios económicos.
- **Sistema:** ayuda a analizar, **no contacta prospectos ni actúa autónomamente**.

## Resultados esperados al día 3

- Repositorio reproducible y documentación suficiente para ejecutarlo.
- PoC mínima con 30 PyMEs y relaciones; comparación exploratoria de baseline y señales del grafo.
- Material de presentación que cubra los seis bloques.
- Plan creíble para experimentar en producción y determinar margen incremental atribuible, sin confundir simulación con causalidad.

## Objetivos secundarios

El mismo caso puede nutrir documentación de ICEméxico y un portafolio de habilidades en producto, ingeniería/arquitectura de datos, analítica y ciencia de datos. **No se ampliará el alcance técnico para satisfacer estos objetivos secundarios.**
