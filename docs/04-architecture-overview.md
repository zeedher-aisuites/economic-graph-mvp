# Arquitectura propuesta — v0.1

> **Estado:** diseño preliminar para orientar el MVP, **no** descripción de funcionalidades ya implementadas. El modelo de datos, índices y estrategia de consulta se decidirán después de definir el grafo conceptual.

**Base implementada en misión 001:** `src/economic_graph/config.py` lee y valida configuración; `database.py` crea un cliente PyMongo con tiempos de espera de cinco segundos y ofrece `ping`; `scripts/check_connection.py` presenta un resultado seguro y cierra la conexión. `ping` se dirige a la base configurada, no crea colecciones ni inserta datos. La instancia MongoDB debe existir previamente, local o administrada por el usuario; no se instala en esta misión. Crear el cliente no confirma conectividad y un `ping` exitoso no demuestra permisos de lectura/escritura, disponibilidad del grafo ni rendimiento.

**Ampliación 002B implementada:** archivos aprobados restringidos → auditoría → proyección de 83 observaciones → ledger público → consultas temporales, conflictos e identidad candidata. PyMongo permite cargar explícitamente solo el ledger en una base dedicada; idempotencia probada con dobles. En 002C el usuario reportó integración real exitosa desde Windows con VS Code, registrada en `11-atlas-integration-validation.md`; no fue ejecutada por Codex Cloud. El contrato físico y sus límites se detallan en `10-design-validation.md`.

El siguiente diagrama describe el flujo objetivo del MVP completo: extracción de señales, rankings, gráficos y Control Tower siguen **pendientes**. No se generan datos aleatorios ni eventos comerciales en 002B.

## 1. Arquitectura mínima de demostración

```text
Generador sintético reproducible
  ├─ 30 PyMEs + atributos
  ├─ relaciones + procedencia + fechas
  └─ historial comercial observable
                 │
                 ▼
           MongoDB / PyMongo
                 │
                 ▼
        Consultas y validaciones
                 │
                 ▼
     Python: extracción de señales
          ├─ ranking baseline
          └─ ranking con grafo
                 │
                 ▼
      Evidencia para la defensa
    (tablas, gráficos y, si conviene,
        visualización sencilla)
```

**Interacción:** el usuario ejecuta consultas y revisa resultados. No existen agentes, acciones autónomas ni generación de mensajes comerciales.

## 2. Componentes y responsabilidades

| Componente | Responsabilidad | Criterio de sencillez |
|---|---|---|
| Generación de datos | Producir un mundo sintético coherente, con semilla y reglas documentadas | Un script reproducible; no sistema de simulación extenso |
| MongoDB | Persistencia y consulta de empresas, relaciones y eventos | Colecciones mínimas, índices justificados por consultas reales |
| Acceso a datos | Encapsular conexión y consultas repetidas | PyMongo directamente; evitar ORM abstracto |
| Validación de datos | Detectar duplicados, referencias rotas, rangos y fechas inválidas | Funciones pequeñas y pruebas |
| Análisis | Obtener señales empresariales y relacionales con corte temporal | Lógica separada de I/O; evitar ML si una regla basta |
| Presentación | Explicar el grafo, comparar rankings y ofrecer métricas | Tablas/gráficos; Streamlit solo si agrega valor demostrable |

## 3. Modelo lógico: temas obligatorios

**Nodos iniciales:** empresas PyME. Evaluar otros nodos solo si existe un caso de uso concreto.\
**Aristas:** relaciones económicas dirigidas cuando aplique, con tipo definido, fuente, fecha de vigencia y fecha de observación.\
**Identidad:** identificadores estables y estrategia de deduplicación; no asumir coincidencia por nombre.\
**Confianza:** distinguir hecho verificado, inferencia y ausencia de evidencia.\
**Trazabilidad:** poder explicar qué fuente justificó una relación o feature.

**Separación de dos capas:**

1. **Verdad sintética** del generador: sirve para comprobar coherencia de la simulación.
2. **Vista observable** de la Telco: única entrada permitida para rankings y decisiones de negocio.

El esquema concreto de colecciones, embebido/referenciado, validaciones e índices está **pendiente**. No asumir que MongoDB es una base de datos de grafos especializada; justificar consultas de relaciones según la profundidad realmente necesaria.

## 4. Flujo temporal y prevención de fuga

Para cada análisis histórico fijar un instante `t`. Solo utilizar atributos y relaciones disponibles/observados hasta `t`. El resultado de un contacto o cierre posterior no puede influir en la puntuación calculada en `t`. Documentar las diferencias entre *fecha del hecho* y *fecha de conocimiento*.

## 5. Comparación analítica

- **Baseline** con información empresarial individual disponible.
- **Variante enriquecida** con las mismas variables más features de relaciones económicas observadas.
- Registrar fecha de corte, entradas, versión de reglas y razones del ranking.
- No entrenar ni atribuir métricas predictivas a un modelo inexistente.
- Para una Telco real: proponer validación temporal, monitoreo de calidad, deriva, calibración y ciclo de vida de ML solo si se elige un modelo entrenado.

## 6. Arquitectura objetivo de producción (solo propuesta)

```text
Fuentes autorizadas (CRM, cobertura, registros consentidos, fuentes públicas permitidas)
      ↓ ingestión + contratos de datos + controles de privacidad
Normalización + entity resolution + deduplicación + evidencia/procedencia
      ↓
Repositorio de entidades y relaciones con historial temporal
      ↓
Cálculo versionado de features y puntuaciones
      ↓
Serving para analista comercial / CRM (con controles de acceso)
      ↓
Medición experimental + Control Tower + auditoría
```

**Aspectos a explicar en la defensa, no implementar ahora:** seguridad y acceso por rol, privacidad, calidad de datos, actualización incremental, desempeño de consultas, manejo de fallas, costos, observabilidad, gobernanza y MLOps si existe un modelo ML.

## 7. Criterios de evolución

Aumentar componentes **solo** cuando un requisito medido lo exija: más fuentes, mayor volumen, menor latencia, consultas de varios saltos, necesidades regulatorias o carga de usuarios. Considerar la conveniencia de tecnología especializada en grafos según consultas y costo total, no por preferencia estética.

Los agentes son una línea **posterior a la entrega**, no una dependencia ni condicionante de este diseño.

## 8. Riesgos técnicos principales

- Aristas inventadas sin procedencia plausible o datos confidenciales que una Telco no podría conocer.
- Mezclar verdad del simulador con información comercial observada.
- Fuga temporal al evaluar resultados.
- Overfitting o conclusiones estadísticas a partir de 30 empresas.
- Tratar la representación visual del grafo como prueba de valor económico.
- Añadir plataforma web/agentes antes de resolver preguntas de negocio.

## 9. Verificación de la PoC

Antes de considerar la PoC lista: generación repetible, integridad referencial, consultas funcionando, rankings auditables, pruebas básicas y documentación de lo **implementado**, **simulado** y **propuesto**.
