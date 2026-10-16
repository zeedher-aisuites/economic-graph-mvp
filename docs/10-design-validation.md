# Auditoría e implementación del diseño — misión 002B

**Estado:** insumos aprobados por el usuario; validación offline ejecutada. Esta misión demuestra construcción, trazabilidad y observabilidad, sin medir valor económico incremental. Los seis entregables siguen rigiéndose por `02-challenge-traceability.md`.

## Origen y reproducción

Se leyó `main` actualizado en `e81a898` antes de implementar; su base tenía 35 pruebas aprobadas. Se incorporaron los cuatro Markdown de diseño y el README adjunto en `design-data/README.md`, conservando el README principal. `design-data/manifest.json` identifica origen, versión, tamaño y SHA-256 de los 16 adjuntos. Los 11 CSV/JSON están preservados **byte por byte** en `design-data/restricted/`; solo se actualizan estado y seguimiento en los documentos.

Los CSV originales usan BOM UTF-8 y finales CRLF. `.gitattributes` desactiva la conversión de texto solo para los insumos restringidos, de modo que Windows no cambie sus huellas; reconoce CRLF en la comprobación de espacios de esos CSV. No se normalizan ni se cambian los checksums esperados para ocultar diferencias.

`uv run python scripts/validate_design.py` lee todos los insumos y compara CSV/JSON con interpretación explícita de `True`/`False`. Verifica huellas, contratos, IDs, cantidades, fuentes, enlaces y temporalidad. No escribe ni repara datos. Si falta un archivo, se identifica y se detiene la operación. Los errores impiden la materialización; las advertencias siguientes permanecen visibles y no se convierten en pruebas ficticias.

`uv run python scripts/build_observable.py --dry-run` proyecta en memoria; sin esa bandera materializa el ledger aprobado. No hay aleatoriedad: los mismos insumos producen los mismos bytes. No se usa una semilla decorativa.

## Invariantes comprobados sobre los archivos

| Invariante | Resultado |
|---|---|
| Universo canónico | 30 empresas únicas, EMP-001 a EMP-030; sectores 3/2/7/4/8/6 |
| Relaciones económicas verdaderas | 48: 41 SUPPLIES_TO y 7 PARTNERS_WITH; sin huérfanos, auto-relaciones ni duplicados |
| Afirmaciones falsas separadas | 3, CLM-001 a CLM-003; ninguna agregada a las 48 verdaderas |
| Referencias separadas | 3, REF-001 a REF-003; REFERS_TO no demuestra suministro ni alianza |
| Observaciones | 83 IDs únicos; 28 T0, 26 T1, 29 T2 |
| Fuentes | CRM 37; TELCO_INTERNAL 2; DIRECTORY 13; PUBLIC_PROFILE 16; REFERRAL 15 |
| Estados del plan | 73 REPORTED, 7 CONFIRMED, 3 INFERRED; sin confirmación por consulta al oráculo |
| Extremos identificables | Toda relación/referencia tiene ambos extremos disponibles cuando la Telco la conoce |
| Desconocido al cierre | 7 empresas y 25 relaciones verdaderas; solo contados por la evaluación restringida |

| Corte exacto UTC | Empresas conocidas | Observaciones acumuladas | Relaciones verdaderas observadas, solo auditoría | Afirmaciones económicas en la vista comercial | Referencias en la vista |
|---|---:|---:|---:|---:|---:|
| 2026-01-15T12:00:00Z | 12 | 28 | 2 | 2 | 0 |
| 2026-05-15T12:00:00Z | 17 | 54 | 11 | 13 | 2 |
| 2026-09-15T12:00:00Z | 23 | 83 | 23 | 26 | 3 |

El usuario comercial ve las afirmaciones con su estado, **sin saber cuáles son falsas en el simulador**. Por eso 26 afirmaciones económicas no significan 26 vínculos verdaderos ni confirmados. Los conteos de verdad sirven exclusivamente para auditar el escenario aprobado. Se filtra por `available_at <= as_of`; no por fase, fecha de observación ni fin de día. Las pruebas incluyen un microsegundo antes de cada corte y equivalencia entre zonas horarias explícitas.

## Desviaciones y protección de información

| ID | Registros exactos y problema | Impacto | Resolución mínima y estado |
|---|---|---|---|
| DV-001 | OBS-043, OBS-044 y OBS-073: notas como «incorrecta», «no constituye colaboración» y «confunde proveedores» revelan diagnóstico del oráculo | Eliminar solo `truth_reference` seguiría filtrando la falsedad en texto | Originales intactos en el área restringida. La proyección de estas tres notas describe únicamente la afirmación y su verificación pendiente/inferida. No cambia tipo, extremos, fechas ni estado. Implementado como protección de interfaz |
| DV-002 | ALIAS-001/OBS-054 y ALIAS-002/OBS-083 solo aportan nombre y condición de candidato | No hay evidencia fuerte para fusionar ni para demostrar el segundo caso de AC-08 del diseño conceptual | Candidatos sugeridos por normalización de nombre, siempre NEEDS_REVIEW. No se fusionan ni se crean empresas 31/32. Demostración de fusión detenida: requeriría adenda de evidencia aprobada |
| DV-003 | Las 26 afirmaciones económicas y 3 referencias tienen una sola observación de relación cada una; ninguna aporta transición, descarte ni vigencia | AC-10 del diseño conceptual y un ejemplo real de caducidad no pueden demostrarse con estos 83 registros | Se conserva historial. Soporte de estado DISCARDED y corte histórico probado solo con fixtures de prueba identificados como tales. No se añaden hechos al dataset. Ampliar evidencia o reglas requiere aprobación |
| DV-004 | Las 83 filas no incluyen `source_record_id`, aunque el contrato conceptual lo exige | Falta una clave técnica estable de origen | Se asigna `SRC-<source_type>-<observation_id>` por registro importado. Es una clave de trazabilidad del paquete, no una factura, identificación fiscal ni documento externo inventado |
| DV-005 | CLM-003/OBS-044 expresa EMP-025 → EMP-017 en PARTNERS_WITH | El orden de la fuente no es el orden canónico de una relación simétrica | Se preserva el original; se ordenan solo los IDs observables al materializar la alianza. No cambia su significado ni se confirma la hipótesis |

También se resuelven diferencias de vocabulario sin inventar entidades: `COMPANY_ALIAS` pasa a `SOURCE_RECORD` observable y `REFERRAL` a una afirmación `RELATIONSHIP` de tipo `REFERS_TO`. La aprobación explícita de esta misión sustituye las etiquetas antiguas «pendiente de aprobación» y el requisito de semilla: no se modifica ningún hecho aprobado. Los eventos y la evaluación económica mencionados como trabajo futuro en 002A **no están autorizados en 002B**.

No se requieren cambios de datos para cumplir los conteos ni los cortes. Permanecen detenidos únicamente los ejemplos que exigirían nueva evidencia de fusión, transición o caducidad. No se inventan para hacer pasar los criterios históricos.

## Contrato físico y límites de acceso

| Área | Contenido y acceso |
|---|---|
| `design-data/restricted/` | Catálogo completo, relaciones del mundo, afirmaciones falsas, referencias, planes y alias originales. Solo ingesta y evaluación |
| `src/economic_graph/simulator/` | Auditoría y proyección unidireccional; el visor y la persistencia pública no importan este módulo |
| `data/synthetic/restricted/reconciliation.json` | Conciliación EMP/REL/CLM/REF → IDs públicos; generado, ignorado por Git y con permisos locales restringidos |
| `data/observable/observations.json` | Ledger público de 83 registros sin verdad ni perfiles ocultos; única entrada local del visor |
| `observable.py` y `inspect_graph.py` | Solo lecturas públicas: instantánea, historial, conflictos, candidatos; no escriben |
| MongoDB dedicado | Solo `conectapyme_mvp_observable`, colecciones `m002b_observations` y `m002b_metadata`; no se carga el mundo privado |

Los IDs `CO-`, `LINK-` y `REC-` se derivan mediante UUID determinista de la primera observación, no del ordinal del mundo ni de su clase verdadera/falsa. Los `OBS-*` se conservan para trazabilidad. Una clave pública desconocida devuelve ausencia de datos; nunca activa búsqueda en el catálogo. UUID no es un control de autorización.

El ledger conserva fuente, clave técnica de registro, `observed_at`, `recorded_at`, `available_at`, estado, nota segura y grupo de conflicto. Los perfiles se reconstruyen de observaciones: ningún atributo ausente se copia del catálogo ni se convierte en cero. Si hay valores distintos sin arbitraje aprobado, el atributo queda CONFLICTED y sin valor consolidado, aunque exista una observación posterior confirmada. CG-001 podría representar crecimiento o error; no se presupone cuál. CG-002 permanece abierto.

Las identidades conocidas siguen NEEDS_REVIEW por ausencia de identificador externo fuerte. Normalizar nombres solo sugiere candidatos; no prueba equivalencia. En relaciones, `active_claim` significa que la afirmación no está descartada ni en conflicto, **no** que sea verdadera o confirmada.

Los directorios están separados físicamente y las interfaces comerciales rechazan archivos de diseño y campos privados anidados. Los permisos POSIX locales de las zonas restringidas se preparan como 700/600; Git no transporta esos permisos y Windows requiere sus ACL propias. Un desarrollador con acceso al repositorio completo puede leer el simulador. **No se afirma aislamiento frente a ese usuario.** Para un consumidor comercial se debe entregar únicamente el directorio observable o un usuario MongoDB con rol de lectura limitado a `m002b_observations`, sin montar el checkout restringido. La credencial de carga pertenece al operador, no al visor; estos roles no se han provisionado en Atlas.

## MongoDB: carga y consultas

La carga es explícita: `--dry-run` es el comportamiento por defecto y no lee `.env` ni abre red. `--apply` exige confirmación literal del nombre de la base dedicada; también se verifica `MONGODB_DATABASE` antes de conectarse. Se rechaza la base si contiene colecciones ajenas o colecciones existentes sin marca de propiedad compatible. No se llama a drop, delete, replace ni a actualizaciones destructivas.

Los documentos son inmutables por ID: una colisión con contenido diferente detiene el lote antes de nuevas escrituras. Se usa `$setOnInsert`, lo que permite reintentar una carga interrumpida sin duplicar observaciones; empresas y relaciones se reconstruyen del mismo ledger. No se presenta el lote como transacción atómica. Una carrera con contenido diferente se detecta al releer, sin reemplazar el registro ajeno.

Índices mínimos justificados: `_id` para unicidad/idempotencia; `available_at` para cortes; `(subject_id, available_at)` para lectura de historial por sujeto. Los tiempos se almacenan como BSON Date UTC y se normalizan al leer. Las consultas MongoDB ejecutan el filtro temporal en el servidor; el historial de una empresa añade `subject_id` a ese filtro. No se han medido latencia ni escalabilidad; 30 empresas no validan rendimiento de producción.

## Evento comercial: contrato pendiente

Se conservan las cuatro entidades conceptuales. Para `CommercialEvent` siguen pendientes catálogo definitivo de eventos, hechos, fuente y permisos, campos de costo/resultado y reglas de cronología. El diseño 002A enumera campos posibles; no se ha materializado ningún registro ni colección de eventos. No se construye un evento DISCOVERED a partir de una observación sin autorización adicional.

## Verificación y límites reales

Las pruebas offline verifican cantidades, referencias, fechas, rechazo de contratos inválidos, aislamiento, desconocidos, conflictos, aliases, no promoción de reportes/inferencias y carga repetida contra un doble de MongoDB. Incluyen lectura del ledger sin que exista el directorio de diseño. La prueba de integración está separada, marcada `integration` y requiere activación explícita y confirmación de base.

En esta ejecución no hay `MONGODB_URI` ni `MONGODB_DATABASE` inyectados y no existe `.env` local: **integración real no verificada**. No se insertó nada en Atlas. Los comandos de PowerShell son instrucciones; no se ejecutaron en Windows. El acceso a la API GitHub continúa bloqueado por el proxy; Git HTTPS sí funciona.

No hay scoring, modelos ML, dashboard, simulación de ventas, conversiones, causalidad ni cálculos económicos. La siguiente fase requiere autorización propia y evidencia económica futura; esta misión no la ejecuta.

Resultados de esta ejecución: `uv run pytest` ejecutó **97 pruebas aprobadas y 1 integración omitida** por falta de activación/configuración real. `uv run ruff check .` y `uv run ruff format --check .` pasan. `uv sync --locked` y la repetición determinista se comprueban antes de publicar; el reporte de entrega indica el SHA remoto real.
