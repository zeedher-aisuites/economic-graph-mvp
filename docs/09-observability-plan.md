# 09 — Plan de observabilidad del Economic Graph v1.0

**Estado:** plan aprobado por el usuario para misión 002B. La implementación se audita en `10-design-validation.md`; no es evidencia de ventas.\
**Dependencias:** catálogo de 30 empresas aprobado; matriz de 48 relaciones verdaderas aprobada; modelo conceptual v1.0; CRM inicial con 12 empresas.

## 1. Propósito

Separar lo que existe en la realidad simulada de lo que ConectaPyME puede conocer en cada fecha, con fuentes, evidencia, temporalidad e incertidumbre. Este documento **no** modifica las 48 relaciones aprobadas ni fabrica resultados comerciales. El objetivo laboral principal sigue siendo construir un Economic Graph y definir cómo medir su **valor económico incremental**.

## 2. Fechas de corte aprobadas de la simulación

| Corte | Fecha UTC | Empresas nuevas | Empresas acumuladas | Observaciones planificadas |
|---|---|---:|---:|---:|
| T0 | 15 enero 2026, 12:00 | 12 | 12 | 28 |
| T1 | 15 mayo 2026, 12:00 | 5 | 17 | 26 |
| T2 | 15 septiembre 2026, 12:00 | 6 | 23 | 29 |

Al final, **7 de las 30 empresas permanecen desconocidas**. El corte T0/T1/T2 no es el momento de ocurrencia de cada transacción económica, sino la fecha a la que la información quedó disponible para la Telco.

## 3. Cinco fuentes aprobadas

- **CRM**: nombres, notas, oportunidades y observaciones registradas por comerciales. No garantiza exactitud.
- **TELCO_INTERNAL**: información de clientes actuales a la que la Telco tiene acceso legítimo, con límite por finalidad y permisos. No disponible para prospectos externos.
- **DIRECTORY**: fichas de directorio empresarial ficticio, potencialmente desactualizadas y duplicadas.
- **PUBLIC_PROFILE**: simulación de perfiles de negocios y sitios públicos (calificaciones y reseñas inventadas). Sin extracción real ni afirmación de acceso a datos de Google.
- **REFERRAL**: recomendaciones o testimonios voluntarios, no equivalentes a transacciones verificadas.

**Regla de fuente y afirmación:** la relación dirigida se registra como lo que *afirma* la fuente. Una mención comercial aislada no convierte la relación en confirmada. La calidad de evidencia y el tipo de fuente son propiedades diferentes.

## 4. Identidad y empresas descubiertas

El archivo `company_discovery_plan.json` indica exactamente qué empresa es visible desde qué corte. Inicialmente las 12 empresas son: EMP-001, EMP-002, EMP-004, EMP-006, EMP-007, EMP-010, EMP-013, EMP-017, EMP-018, EMP-020, EMP-025, EMP-026. En T1 se descubren EMP-003, EMP-005, EMP-014, EMP-019, EMP-029; en T2 se descubren EMP-008, EMP-009, EMP-012, EMP-015, EMP-027, EMP-030. Permanecen ocultas: EMP-011, EMP-016, EMP-021, EMP-022, EMP-023, EMP-024, EMP-028.

El ID `EMP-xxx` de la verdad sintética se usa **solo como referencia de conciliación y prueba**. En una aplicación real, el sistema de observaciones debe generar IDs canónicos propios y no revelar que existen entidades todavía no descubiertas. No debe usarse el catálogo completo para enriquecer las empresas observadas.

**Dos alias candidatos:** `ALIAS-001` corresponde en la verdad a EMP-002 y `ALIAS-002` a EMP-017. Son registros potencialmente duplicados que deben revisarse antes de fusionar. No generan empresas 31 y 32 en el universo de verdad.

## 5. Relaciones observadas

Se preservan exactamente los planes aprobados en `relationship_visibility_plan.json`: **2 vínculos verdaderos observables en T0, 9 más en T1, 12 más en T2 y 25 que nunca se descubren**. Los 23 vínculos observables mantienen las fuentes y estados de la matriz anterior, aunque una fuente pública o una recomendación solo respalde una *afirmación*, no la existencia independiente de transacciones. Las 3 afirmaciones falsas `CLM-001` a `CLM-003` se presentan como reportadas/inferidas, jamás como aristas verdaderas.

Las 3 recomendaciones `REF-001` a `REF-003` se representan como actos `REFERS_TO` para descubrimiento; **no cuentan entre las 48 relaciones económicas verdaderas** ni prueban actividad económica bilateral.

### Regla de consistencia temporal

Una relación no se incorpora al grafo visible hasta que sus extremos están identificados de forma suficiente. Todos los vínculos del plan respetan esta condición. Si llega una referencia a una empresa aún no identificada, se retiene como observación pendiente sin crear una identidad falsamente confirmada.

## 6. Esquema de la observación (contrato conceptual)

Cada fila del `observation_plan.json` incluye:

- `observation_id`: identificador de la afirmación observada.
- `phase`: T0/T1/T2; fecha de corte.
- `subject_type`, `subject_id`: empresa, relación, referencia o alias.
- `attribute`, `value`: qué afirma la fuente; `value` puede ser valor simple u objeto tipado.
- `source_type`, `verification_status`: procedencia y situación de evidencia.
- `observed_at`: cuándo se obtuvo la evidencia sintética.
- `recorded_at`: cuándo quedó asentada.
- `available_at`: primer instante permitido para usarla en una decisión.
- `evidence_note`: explicación legible, sin información personal.
- `truth_reference`: vínculo exclusivo para validación **fuera del grafo observable**.
- `conflict_group`: identificador de posibles contradicciones sin resolver.

**Importante para Codex:** `truth_reference` y `company_id_truth` de alias son **metadatos del oráculo**, no atributos que deba almacenar o exponer el CRM. En implementación deberá existir una exportación/transformación que los elimine del conjunto observable. `subject_id` de empresa utiliza IDs del mundo solo como clave técnica compartida para evaluar la PoC: el generador los conoce, pero el ranking no debe derivar presencia, ordinales o conexiones ocultas de esa clave. Preferible proyectar IDs observables separados al materializar la base.

Las fechas son UTC, explícitas y ordenadas. `available_at <= fecha_de_corte` es una precondición obligatoria. Para eventos históricos, el dato además debe corresponder al periodo que pretende describir; registrar hoy un hecho antiguo no permite usarlo retrospectivamente como si se conociera entonces.

## 7. Conflictos y dificultades deliberadas

- **CG-001:** EMP-002 aparece con 2 sucursales en T0 y 3 en T1; en T2 hay una confirmación posterior. Conservamos todas las observaciones, sin borrar la anterior. Podría reflejar crecimiento real o información inicialmente incorrecta; no presuponer cuál sin evidencia.
- **CG-002:** EMP-026 aparece como `Micro` según directorio y con tamaño distinto según CRM en T2. El conflicto queda abierto, sin sobrescribir una fuente con otra por defecto.
- **CLM-001/002:** afirmaciones de suministro falsas en la verdad sintética.
- **CLM-003:** alianza inferida erróneamente por proximidad.
- **ALIAS-001/002:** candidatos a duplicado que requieren evidencia adicional.
- **Observaciones incompletas:** no hay atributos de tamaño, sucursales o calificaciones para todas las empresas; ausencia de dato no equivale a cero.

**No mezclar los estados de verdad con verificación:** `truth_exists` solo vive en el oráculo; las observaciones pueden reportar una relación verdadera que aún no esté confirmada, o una afirmación falsa que todavía no haya sido descartada.

## 8. Reglas de generación para la Misión 002B

1. Mantener sin cambios los 30 registros del catálogo y las 48 relaciones del mundo sintético.
2. Materializar únicamente este plan aprobado; exportar orden e IDs deterministas. No hay aleatoriedad que requiera semilla.
3. Al materializar la capa Telco, excluir todo lo que sea `truth_reference`, `company_id_truth`, `truth_exists`, atributos `_truth` y relaciones `NEVER`.
4. Registrar únicamente las 12 empresas iniciales en T0, sumar 5 en T1 y 6 en T2. Nunca materializar automáticamente las otras 7.
5. Conservar evidencia, orden temporal y conflictos, sin actualizar destructivamente el historial.
6. Mantener estados CONFIRMED/REPORTED/INFERRED en su significado documental; no transformar reportes públicos en confirmaciones automáticas.
7. No inferir proveedores basándose únicamente en proximidad, sector, reseñas o popularidad.
8. No introducir empresas extras a partir de alias; los duplicados se quedan como registros de fuente candidatos.
9. No crear ventas, ingresos, conversiones, probabilidades de compra ni costos comerciales a partir de este plan.
10. Separar los datos del oráculo de la capa observable mediante módulos, archivos y colecciones diferentes; el servicio de ranking tendrá acceso solo a la capa observable.
11. Si una regla no puede implementarse directamente, registrar la limitación en lugar de inventar un comportamiento silencioso.

## 9. Criterios de aceptación para Codex

- [ ] CAT-01: exactamente 30 empresas de verdad y sus IDs únicos.
- [ ] CAT-02: exactamente 48 relaciones verdaderas de mundo y ninguna alteración de endpoints.
- [ ] CAT-03: CRM T0 contiene 12 empresas, T1 17 y T2 23.
- [ ] CAT-04: 7 empresas nunca aparecen en la capa observable hasta T2.
- [ ] CAT-05: las 48 relaciones se desglosan 2/T0, 9/T1, 12/T2, 25/NEVER.
- [ ] CAT-06: solamente 23 relaciones verdaderas se vuelven observables.
- [ ] CAT-07: existen 3 afirmaciones falsas observadas, diferenciadas del oráculo.
- [ ] CAT-08: existen 3 referencias explícitas `REFERS_TO`, separadas de suministro/alianza.
- [ ] CAT-09: existen al menos 2 conflictos de atributos conservando ambas fuentes.
- [ ] CAT-10: existen 2 alias candidatos sin creación de empresa adicional.
- [ ] CAT-11: ninguna observación entra a un corte anterior a `available_at`.
- [ ] CAT-12: ninguna empresa desconocida ni atributo `_truth` es accesible al ranking.
- [ ] CAT-13: toda relación visible tiene fuente, fecha y estado de verificación.
- [ ] CAT-14: el proceso es reproducible y supera pruebas unitarias sin MongoDB; la prueba de integración se ejecuta separadamente.
- [ ] CAT-15: ninguna parte del flujo estima impacto económico real a partir de la simulación.
- [ ] CAT-16: README y decisiones documentan supuestos, limitaciones y separación del oráculo.

## 10. Limitaciones y decisiones pendientes

- Las fechas T0/T1/T2 y el calendario de descubrimientos quedaron **aprobados** por el usuario en misión 002B.
- El plan es determinista: no afirma representar frecuencias reales de datos faltantes, error de fuentes o cobertura de una Telco mexicana.
- La matriz inicial no define causalmente quién compra ni cuánto paga. El modelo económico se diseñará después y deberá comparar asignaciones comerciales con costos/márgenes y potencial interferencia de empresas conectadas.
- Se requiere definir cuándo una relación expira y las reglas concretas para confirmar/arbitrar evidencias contradictorias. Para el MVP se pueden mantener como pendientes de revisión, sin crear automatización injustificada.
- Las operaciones de creación de índices, consultas MongoDB y representación física están definidas y probadas offline en 002B; véase `10-design-validation.md`. La integración real no está verificada.

## 11. Comunicación ejecutiva

**Mensaje al CEO:** «La Telco no necesita conocer toda la economía local para comenzar. Puede transformar datos dispersos en relaciones explicables, saber dónde tiene evidencia insuficiente y dirigir mejor la investigación comercial. El valor económico deberá medirse comparando una estrategia basada en el grafo con la operación habitual, descontando costos y evitando atribuir a la herramienta mejoras no verificadas».

**No implica:** que el grafo ya haya aumentado conversiones, que las calificaciones públicas predigan ventas o que 23 relaciones sean representativas del mercado real.


**Actualización 002B:** las listas de trabajo de 002A se conservan como contexto histórico. Para este alcance están aprobados catálogo, 48 relaciones, 3 afirmaciones falsas, 3 referencias y 83 observaciones. No se crean eventos comerciales ni se resuelven alias sin evidencia. Las rutas `design-data/` citadas en el diseño corresponden ahora a `design-data/restricted/`; el visor usa exclusivamente `data/observable/observations.json`. Véase `10-design-validation.md` para implementación y discrepancias.
