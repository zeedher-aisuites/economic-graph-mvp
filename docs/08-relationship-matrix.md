# Matriz de relaciones económicas — Distrito Centro v1.0

**Estado:** matriz aprobada para misión 002B; originales de verdad sintética preservados sin cambios.
**Naturaleza:** relaciones ficticias entre exactamente 30 empresas existentes en el catálogo `07-company-catalog.md`.

## Resumen

- 48 vínculos verdaderos simulados de tipo económico: PARTNERS_WITH: 7, SUPPLIES_TO: 41.
- Observabilidad aprobada: T0: 2, T1: 9, T2: 12, NEVER: 25.
- 3 afirmaciones falsas deliberadas **fuera del conjunto de vínculos verdaderos**.
- 3 referencias comerciales simuladas (`REFERS_TO`), separadas de suministro y alianzas.
- Las 30 empresas participan en al menos un vínculo. Ningún vínculo es creado solo por proximidad o por pertenecer al mismo sector.

## 1. Modelo de dos capas

La matriz principal contiene **verdad sintética privada**. Sus columnas `first_observed_phase`, `planned_source` y `planned_initial_status` son el **plan aprobado de exposición parcial**; la misión 002B materializa únicamente las observaciones de `09-observability-plan.md` con `source_record_id`, `observed_at`, `recorded_at` y evidencias concretas.

El ranking no podrá consultar este archivo ni `truth_exists`, ni `first_observed_phase`. Su entrada será exclusivamente la capa observable reconstruida a la fecha de decisión.

## 2. Matriz íntegra de relaciones verdaderas

| ID | Origen → destino | Tipo | Razón comercial plausible | Conocimiento planeado |
|---|---|---|---|---|
| REL-001 | EMP-029 → EMP-001 | `SUPPLIES_TO` | Insumos de empaque y abastecimiento de mostrador | T1 · REPORTED |
| REL-002 | EMP-029 → EMP-002 | `SUPPLIES_TO` | Suministro de consumibles para tres sucursales | T2 · CONFIRMED |
| REL-003 | EMP-029 → EMP-003 | `SUPPLIES_TO` | Lotes periódicos de insumos para operación mayorista | NEVER · NOT_OBSERVED |
| REL-004 | EMP-003 → EMP-019 | `SUPPLIES_TO` | Panificados al negocio de alimentos | T2 · REPORTED |
| REL-005 | EMP-003 → EMP-023 | `SUPPLIES_TO` | Pan de mesa para servicio de terraza | NEVER · NOT_OBSERVED |
| REL-006 | EMP-002 → EMP-020 | `SUPPLIES_TO` | Pan para menú de restaurante | T1 · REPORTED |
| REL-007 | EMP-002 → EMP-017 | `SUPPLIES_TO` | Piezas de pan para cafetería | T2 · CONFIRMED |
| REL-008 | EMP-001 → EMP-022 | `SUPPLIES_TO` | Pan para desayunos del comedor | NEVER · NOT_OBSERVED |
| REL-009 | EMP-029 → EMP-017 | `SUPPLIES_TO` | Insumos empaquetados para café | NEVER · NOT_OBSERVED |
| REL-010 | EMP-029 → EMP-020 | `SUPPLIES_TO` | Insumos y consumibles para cocina | T2 · REPORTED |
| REL-011 | EMP-029 → EMP-024 | `SUPPLIES_TO` | Suministro de empaques para alimentos | NEVER · NOT_OBSERVED |
| REL-012 | EMP-004 → EMP-001 | `SUPPLIES_TO` | Reparto local de pedidos de panadería | T1 · REPORTED |
| REL-013 | EMP-004 → EMP-017 | `SUPPLIES_TO` | Servicio ocasional de reparto en motocicleta | T1 · REPORTED |
| REL-014 | EMP-004 → EMP-021 | `SUPPLIES_TO` | Reparto de pedidos en zona terminal | NEVER · NOT_OBSERVED |
| REL-015 | EMP-005 → EMP-003 | `SUPPLIES_TO` | Transporte de pedidos al mayoreo | T2 · REPORTED |
| REL-016 | EMP-005 → EMP-029 | `SUPPLIES_TO` | Traslado de inventario para dos puntos de venta | NEVER · NOT_OBSERVED |
| REL-017 | EMP-005 → EMP-026 | `SUPPLIES_TO` | Traslado de materiales y ferretería | NEVER · NOT_OBSERVED |
| REL-018 | EMP-006 → EMP-025 | `SUPPLIES_TO` | Soporte a equipos de punto de venta | T0 · CONFIRMED |
| REL-019 | EMP-006 → EMP-018 | `SUPPLIES_TO` | Mantenimiento de equipo de caja | T1 · REPORTED |
| REL-020 | EMP-006 → EMP-028 | `SUPPLIES_TO` | Soporte de hardware administrativo | NEVER · NOT_OBSERVED |
| REL-021 | EMP-007 → EMP-002 | `SUPPLIES_TO` | Software para seguimiento de pedidos y ventas | T1 · REPORTED |
| REL-022 | EMP-007 → EMP-013 | `SUPPLIES_TO` | Desarrollo de módulo de integración | NEVER · NOT_OBSERVED |
| REL-023 | EMP-008 → EMP-019 | `SUPPLIES_TO` | Soporte a sincronización de inventarios | NEVER · NOT_OBSERVED |
| REL-024 | EMP-008 → EMP-027 | `SUPPLIES_TO` | Servicio básico de nube comercial | T2 · REPORTED |
| REL-025 | EMP-009 → EMP-005 | `SUPPLIES_TO` | Tablero de indicadores de rutas y almacén | NEVER · NOT_OBSERVED |
| REL-026 | EMP-009 → EMP-015 | `SUPPLIES_TO` | Integración y reportes para operación financiera | T2 · REPORTED |
| REL-027 | EMP-010 → EMP-017 | `SUPPLIES_TO` | Instalación y asistencia del punto de venta | T0 · CONFIRMED |
| REL-028 | EMP-010 → EMP-020 | `SUPPLIES_TO` | Terminal y configuración de caja | T1 · REPORTED |
| REL-029 | EMP-010 → EMP-024 | `SUPPLIES_TO` | Mantenimiento a terminal POS | NEVER · NOT_OBSERVED |
| REL-030 | EMP-011 → EMP-013 | `SUPPLIES_TO` | Revisión de seguridad de servicios financieros | NEVER · NOT_OBSERVED |
| REL-031 | EMP-011 → EMP-015 | `SUPPLIES_TO` | Revisión periódica de controles digitales | NEVER · NOT_OBSERVED |
| REL-032 | EMP-012 → EMP-023 | `SUPPLIES_TO` | Diseño de materiales digitales y carta | NEVER · NOT_OBSERVED |
| REL-033 | EMP-012 → EMP-027 | `SUPPLIES_TO` | Diseño de catálogo digital | T2 · REPORTED |
| REL-034 | EMP-013 → EMP-020 | `SUPPLIES_TO` | Procesamiento de cobros electrónicos | T1 · REPORTED |
| REL-035 | EMP-013 → EMP-019 | `SUPPLIES_TO` | Solución de pagos en mostrador | NEVER · NOT_OBSERVED |
| REL-036 | EMP-014 → EMP-025 | `SUPPLIES_TO` | Herramienta de cobros de pequeña escala | NEVER · NOT_OBSERVED |
| REL-037 | EMP-014 → EMP-030 | `SUPPLIES_TO` | Cobros digitales en tienda y taller | T2 · REPORTED |
| REL-038 | EMP-015 → EMP-026 | `SUPPLIES_TO` | Herramienta de conciliación de ventas | NEVER · NOT_OBSERVED |
| REL-039 | EMP-016 → EMP-009 | `SUPPLIES_TO` | Servicio financiero empresarial | NEVER · NOT_OBSERVED |
| REL-040 | EMP-028 → EMP-022 | `SUPPLIES_TO` | Productos de higiene para cocina | NEVER · NOT_OBSERVED |
| REL-041 | EMP-026 → EMP-030 | `SUPPLIES_TO` | Herramientas y consumibles de reparación | T2 · REPORTED |
| REL-042 | EMP-008 → EMP-010 | `PARTNERS_WITH` | Integración conjunta de sistemas POS y nube | T2 · REPORTED |
| REL-043 | EMP-010 → EMP-013 | `PARTNERS_WITH` | Integración de terminales con pasarela de pagos | T1 · REPORTED |
| REL-044 | EMP-006 → EMP-011 | `PARTNERS_WITH` | Atención conjunta de soporte y seguridad | NEVER · NOT_OBSERVED |
| REL-045 | EMP-007 → EMP-009 | `PARTNERS_WITH` | Desarrollo conjunto de tablero y automatizaciones | NEVER · NOT_OBSERVED |
| REL-046 | EMP-004 → EMP-005 | `PARTNERS_WITH` | Colaboración puntual en rutas de reparto | NEVER · NOT_OBSERVED |
| REL-047 | EMP-017 → EMP-019 | `PARTNERS_WITH` | Promoción conjunta de alimentos y bebidas | T2 · REPORTED |
| REL-048 | EMP-021 → EMP-030 | `PARTNERS_WITH` | Promoción local para usuarios de movilidad | NEVER · NOT_OBSERVED |

## 3. Afirmaciones falsas deliberadas (no son relaciones reales)

| ID | Afirmación falsa | Fase | Motivo de prueba |
|---|---|---|---|
| CLM-001 | EMP-014 → EMP-017 (`SUPPLIES_TO`) | T1 | Referencia comercial incorrecta, no debe confirmarse automáticamente |
| CLM-002 | EMP-006 → EMP-026 (`SUPPLIES_TO`) | T2 | Nota de vendedor que confunde proveedores |
| CLM-003 | EMP-025 → EMP-017 (`PARTNERS_WITH`) | T1 | Coincidencia geográfica que no constituye colaboración |

Estas afirmaciones deben aparecer como observaciones o hipótesis en la capa de Telco; **no** deben convertirse en aristas verdaderas del oráculo. La falsedad solo es visible al simulador/evaluador; no debe revelarse al ranking.

## 4. Referencias comerciales separadas

| ID | Emisor → referido | Fase | Significado |
|---|---|---|---|
| REF-001 | EMP-017 → EMP-004 | T1 | Recomienda investigar servicio de mensajería, sin afirmar suministro |
| REF-002 | EMP-020 → EMP-003 | T2 | Sugiere contactar fabricante de pan, sin afirmar relación previa |
| REF-003 | EMP-001 → EMP-029 | T1 | Menciona negocio de insumos; no verifica transacción |

`REFERS_TO` es un evento/referencia de descubrimiento; no demuestra vínculo económico. Debe modelarse como relación reportada de referencia en la vista de la Telco, sin introducirse en la lista de relaciones económicas verdaderas.

## 5. Reglas temporales y de observabilidad

- **T0:** el CRM contiene exactamente las 12 empresas marcadas `seed_crm_t0=1` en el catálogo. Solo relaciones con fase T0 y **ambos extremos conocidos** podrían estar visibles; las demás no se cargan por adelantado.
- **T1/T2:** las fuentes descubren gradualmente empresas y vínculos. Una relación planificada para T1/T2 solo aparece una vez que hay observación con fecha de registro válida y ambos extremos cuentan con entidad o registro de origen resoluble.
- **NEVER:** el vínculo existe en el oráculo, pero no está disponible para el CRM ni ranking durante esta PoC.
- `CONFIRMED` y `REPORTED` de la matriz son **estados proyectados** que se deben justificar con evidencia sintética específica en la implementación. Ninguna confirmación se genera automáticamente por ser verdadera en el mundo.
- Evitar porcentajes de cobertura prefijados para T1/T2: el resultado debe ser consecuencia verificable de las observaciones generadas.
- Relaciones vencidas y contradicciones de atributos se crearán en el dataset de observaciones posterior, no se infieren sin soporte en esta matriz.
- La asignación de aparición por fases se ha escogido como **escenario de demostración**, no mediante una muestra estadística ni como mecanismo para garantizar una ventaja del ranking. Su efecto debe discutirse como posible sesgo.

## 6. Criterios de revisión y aceptación

1. Los IDs de extremos corresponden a los 30 IDs existentes en el catálogo; no hay auto-relaciones ni duplicados de arista (tipo + orientación canonizada).
2. Las 30 empresas están representadas por al menos una relación, sin convertirlo en requisito de una Telco real.
3. Suministro dirigido de proveedor a comprador; alianzas con orden de ID canónico.
4. Los tipos económicos verdaderos son solamente `SUPPLIES_TO` y `PARTNERS_WITH`; `REFERS_TO` identifica referencias comerciales, no transacciones.
5. Las afirmaciones falsas están fuera de la lista de relaciones verdaderas.
6. No se copian las relaciones del oráculo al grafo comercial; el plan de observabilidad solo orienta la generación posterior.
7. Hay vínculos verdaderos que nunca se descubren y afirmaciones falsas que sí podrían observarse.
8. No se han creado oportunidades, conversiones, puntuaciones de compra ni resultados económicos.
9. Codex debe validar invariantes y registrar decisiones en documentación, sin atribuir al catálogo evidencia real.

## 7. Seguimiento de pendientes del diseño original

- Formalizar calendario real de fechas T0/T1/T2 y eventos `recorded_at` / `observed_at`.
- Generar registros de fuentes con cobertura y duplicados, sin descubrir a la vez todo el oráculo.
- Diseñar atributos conflictivos, vigencia y al menos un ciclo de corrección de identidad.
- Establecer reglas para que el CRM conozca explícitamente un nuevo nodo antes de enlazarlo.
- Crear historia comercial y evaluación económica de manera independiente de la topología.
- Revisar si vínculos de suministro propuestos requieren un supuesto explícito adicional por actividad real del negocio.

## 8. Traducción ejecutiva

La Telco no necesita saberlo todo. El prototipo permitirá distinguir entre relaciones que existen en la simulación, relaciones que logró conocer y afirmaciones incorrectas. El beneficio esperado es una mejor priorización de prospectos; **su efecto monetario no está demostrado** y deberá validarse por un experimento comercial real.


**Actualización 002B:** las listas de trabajo de 002A se conservan como contexto histórico. Para este alcance están aprobados catálogo, 48 relaciones, 3 afirmaciones falsas, 3 referencias y 83 observaciones. No se crean eventos comerciales ni se resuelven alias sin evidencia. Las rutas `design-data/` citadas en el diseño corresponden ahora a `design-data/restricted/`; el visor usa exclusivamente `data/observable/observations.json`. Véase `10-design-validation.md` para implementación y discrepancias.
