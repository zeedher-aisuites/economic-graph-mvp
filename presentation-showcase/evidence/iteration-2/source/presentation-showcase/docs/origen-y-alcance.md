# Mi respuesta al reto: origen, decisiones y alcance

Esta página registra la perspectiva y las decisiones declaradas por el candidato en la solicitud de la misión 2. No es un historial automatizado de su actividad ni acredita que haya escrito manualmente cada archivo o ejecutado personalmente cada validación.

## Qué me pidió el reto

Fuente principal: el PPTX original de Totalplay, leído completo con sus notas y transcrito en `reto-original.md`. La diapositiva 4 pregunta: **¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?** Las diapositivas 5, 10 y 12 conectan datos, grafo, modelos, decisión, acción comercial e impacto, y establecen los seis entregables. Las opciones tecnológicas son alternativas que deben justificarse, no requisitos obligatorios.

El reto propone información potencial de una Telco y ejemplos comerciales. No constituye una auditoría de operaciones reales de Totalplay. Sus cifras de funnel y score 87 son ilustrativas y no alimentan los resultados de esta PoC.

## Cómo decidí empezar

Antes de elegir tecnología quise definir qué empresa usaría la solución, qué decisión quería mejorar, qué datos tendría, qué relaciones podrían aportar información y cómo mediría una utilidad más allá de un dibujo.

Elegí una Telco ficticia, ConectaPyME, y prioricé la opción del reto **B2B Acquisition: PyMEs similares o conectadas con clientes actuales**. Mi intención es explorar cómo decidir qué prospectos investigar primero. La empresa, el territorio y la operación son una simulación; no diagnostican a Totalplay.

La PoC implementada compara reglas de sucursales y vecinos económicos confirmados. No implementa KNN ni otra similitud aprendida; tampoco añade un peso comercial por ser vecino de un cliente actual. La pertenencia al caso de uso expresa la intención del ejercicio, no una ampliación de la política aprobada.

## Mi hipótesis

Conocer relaciones económicas podría aportar una selección de prospectos más útil que analizar cada empresa aisladamente y, bajo condiciones adecuadas, contribuir al margen. Depende de datos confiables y autorizados, vínculos relevantes/verificados, comparación con una referencia, capacidad de actuar y resultados reales medidos. El cambio de tres lugares del Top 5 es evidencia técnica de una selección distinta, no de más ventas.

## Cómo utilicé IA y cuál fue mi participación

Según mi declaración, utilicé ChatGPT/GPT, Gemini y Codex para acelerar investigación, programación y documentación dentro del plazo. Mi papel fue definir alcance e hipótesis, revisar propuestas y avances, decidir qué tenía sentido y autorizar o pedir cambios. No atribuyo porcentajes, archivos concretos o secuencias de uso a cada herramienta sin un registro que lo respalde.

Dirigir y revisar el desarrollo asistido por IA, comprender un resultado y ejecutar personalmente una validación son actividades diferentes. Los registros de pruebas, capturas y depuración de la misión 1 fueron producidos por Codex y conservan ese origen. La revisión de esta iteración valida la presentación, no cambia retroactivamente la autoría de esas evidencias. Mi capacidad personal de reproducirlas puede demostrarse en una práctica o evaluación en vivo.

## Laboratorio y primera solución

Decidí usar 30 empresas sintéticas por el tiempo limitado y la falta de datos reales de una Telco. El universo privado y el conocimiento observable están separados: 12/17/23 conocidas y 28/54/83 observaciones en T0/T1/T2. Solo se consulta `available_at <= as_of`. No se completa el ranking con empresas del universo que todavía no eran conocidas.

Empecé con reglas comprensibles: baseline individual y su versión con vecinos económicos confirmados. Es la política ya implementada `003a-conservative-v1`, sin cambio de pesos, K, elegibilidad, dataset o resultados en esta iteración. El primer objetivo es entender y comprobar el comportamiento antes de evaluar modelos aprendidos.

## Tecnologías y estados

| Estado | Elementos | Condición o límite |
|---|---|---|
| Utilizadas en la PoC | Python, reglas, registro JSON observable, Streamlit; ruta de persistencia MongoDB opcional | Atlas real sigue sin verificación nueva en estas misiones |
| Utilizadas como apoyo al desarrollo, según declaración del candidato | ChatGPT/GPT, Gemini, Codex | No son un modelo predictivo desplegado dentro del ranking |
| Implementada para exponer | HTML/CSS/JavaScript, fuentes y evidencias locales | Presentación independiente de Streamlit |
| Considerada | KNN para estudiar similitud | Atributos apropiados, escalas/distancia y evaluación acordes; no implementado |
| Considerados | Clasificación o ranking supervisados | Etiquetas reales de activación/conversión y evaluación temporal |
| Consideradas | Técnicas de grafos y comunidades | Objetivo definido y datos apropiados; un cluster no demuestra valor comercial |
| Considerado a mayor plazo | Reinforcement Learning (RL) | Decisiones secuenciales, acciones y recompensas observables y condiciones adecuadas para evaluar; no es un siguiente paso obligatorio |
| Considerados | Híbridos de reglas y modelos | Justificar mejora frente a la referencia; no sumar complejidad por sí misma |

## Los seis entregables y su profundidad actual

| Entregable | Lo construido o definido | Lo que falta |
|---|---|---|
| Business Framing | Problema elegido, hipótesis y cupo de investigación | Relevancia en una Telco real y baseline comercial vigente |
| Economic Graph | Cortes, fuentes, estados, conflictos y candidatos | Identidad fuerte, fuentes reales y proceso productivo de actualización |
| AI/ML Approach | Dos políticas explicables y comparación reproducible | Etiquetas para precision/recall, lift, calibración, drift y modelos aprendidos |
| Architecture | Módulos y rutas de ejecución de la PoC | Escala, serving productivo, gobierno y MLOps cuando corresponda |
| Economic Case | Calculador de supuestos y protocolo experimental | Margen, ventas, costos y efecto causal observados |
| Control Tower | Cinco vistas funcionales con evidencias | Etapas comerciales no observadas y métricas reales de impacto |

Esta es una respuesta parcial y controlada al alcance amplio del reto, con capacidades de PoC, propuestas conceptuales y validaciones pendientes distinguidas. No se atribuyen a Totalplay datos, decisiones, procesos ni resultados no documentados.
