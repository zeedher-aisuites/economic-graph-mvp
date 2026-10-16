# Economic Graph de PyMEs — Especificación conceptual v1.0

**Proyecto:** ConectaPyME Economic Intelligence\
**Misión:** 002A — Diseño (sin implementación)\
**Fecha:** 15 de octubre de 2026\
**Estado:** Diseño aprobado por el usuario para la misión 002B; implementación y límites en `10-design-validation.md`\
**Prioridad:** Reto laboral: «¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?»

## 1. Propósito y límites

El sistema representa conocimiento empresarial parcial que una Telco ficticia, **ConectaPyME**, obtiene sobre **Distrito Centro**, una localidad ficticia con **30 empresas**. Su propósito es apoyar la **adquisición B2B**, no recrear fielmente toda la economía de una ciudad. El prototipo debe demostrar la construcción y evolución de un grafo de entidades y vínculos, y permitir una futura comparación verificable contra un enfoque comercial convencional.

**No se implementarán todavía** agentes, LLM, automatización autónoma, dashboards complejos, scraping, integraciones externas reales, ML o promesas de mejora comercial. Esta especificación no constituye un resultado experimental ni una demostración de impacto económico.

## 2. Decisiones aprobadas

1. Cuatro entidades conceptuales centrales: **Empresa, Relación, Observación y Evento comercial**.
2. Separar técnicamente **verdad sintética** de **conocimiento observable por ConectaPyME**.
3. Usar identificadores internos estables, independientes del nombre comercial.
4. Conservar procedencia, fechas y evidencias contradictorias.
5. Distinguir referencias y relaciones no verificadas de hechos confirmados.
6. En cualquier fecha de decisión, utilizar únicamente información **disponible entonces**.
7. No usar agentes ni automatización autónoma en el MVP.
8. Simular cinco clases de fuentes: CRM, operación interna Telco, directorios, perfiles/sitios públicos y referencias comerciales.
9. Relaciones de negocio: `SUPPLIES_TO`, `PARTNERS_WITH`, `REFERS_TO`; la equivalencia `SAME_BUSINESS_AS` es un **caso de resolución de identidad**, no una relación económica persistente entre empresas consolidadas.
10. Estados de relación: `CONFIRMED`, `REPORTED`, `INFERRED`, `DISCARDED`, con historial; una relación puede además constar como `EXPIRED` según evidencia temporal.
11. En **T0** el CRM conoce **12 de 30** empresas, con atributos incompletos.
12. Hay tres cortes analíticos **T0, T1, T2** para representar descubrimiento progresivo, sin anticipar información futura.

## 3. Alcance del mundo simulado

**Población cerrada para el MVP:** exactamente 30 entidades empresariales reales dentro de la simulación. Distribución sectorial aprobada con nombres y perfiles en `07-company-catalog.md`:

| Sector | Empresas |
|---|---:|
| Panaderías | 3 |
| Logística | 2 |
| Tecnología | 7 |
| Fintech | 4 |
| Restaurantes y cafeterías | 8 |
| Comercio minorista | 6 |
| **Total** | **30** |

No todas deben conocerse al terminar T2. Los registros de origen pueden contener duplicados, aliases y sucursales; esto **no incrementa** el número de empresas reales del mundo simulado. Los conteos de empresas conocidas se calculan sobre **entidades canónicas**, no filas importadas.

La materialización debe ser **determinista; con estos insumos aprobados no hay aleatoriedad ni se requiere semilla**, preservar consistencia sectorial y relaciones posibles, y documentar la distribución de cobertura sin asumir que todas las empresas tienen datos completos.

## 4. Arquitectura conceptual de información

### 4.1. Capa privada: verdad sintética (solo simulador/evaluación)

Contiene el conjunto completo de 30 empresas, atributos subyacentes, relaciones reales simuladas, necesidades comerciales latentes y eventos que ocurrieron en el mundo. Puede servir para verificar precisión de identidad, cobertura o errores en simulación. **Nunca** debe importarse directamente al entorno accesible por la lógica de priorización.

### 4.2. Capa observable: conocimiento de ConectaPyME

Se construye exclusivamente con observaciones simuladas disponibles en cada corte. Puede mantener entidades provisionales, hipótesis de relaciones, estados e historia de evidencia. El modelo de priorización solo puede acceder a esta capa mediante una vista **as-of** (fecha de disponibilidad).

**Invariante de aislamiento:** ninguna variable oculta, relación verdadera no descubierta ni resultado comercial futuro puede aparecer en features, decisiones o paneles operativos antes de su descubrimiento legítimo.

## 5. Entidades y contratos conceptuales

Son contratos de información, **no esquemas MongoDB definitivos**. Los tipos y campos adicionales se definirán en la Misión 002B.

### 5.1. Empresa (`Company`)

- `company_id` — identificador canónico estable (obligatorio, único).
- `display_name` — nombre preferido actual (puede ser provisional si la evidencia es incompleta).
- `sector`, `size`, `branch_count`, `location` — atributos opcionales y **derivados de observaciones** en la capa observable.
- `identity_status` — `RESOLVED` o `NEEDS_REVIEW` cuando existan candidatos duplicados.
- `first_known_at` — primera fecha en que la Telco pudo identificarla.
- `aliases` y `source_record_ids` — referencias a denominaciones y registros originales; no reemplazan la evidencia conservada.

El estado comercial (cliente/prospecto/desconocida) debe derivarse de hechos comerciales disponibles, no atribuirse por una propiedad omnisciente. Una empresa desconocida puede existir solamente en la capa privada.

### 5.2. Relación (`Relationship`)

- `relationship_id` — identificador estable.
- `from_company_id`, `to_company_id` — referencias a empresas, canónicas si están resueltas.
- `type` — `SUPPLIES_TO`, `PARTNERS_WITH` o `REFERS_TO`.
- `verification_status` — `CONFIRMED`, `REPORTED`, `INFERRED` o `DISCARDED`.
- `valid_from`, `valid_to` — intervalo de validez en el mundo representado, si se conoce.
- `first_known_at` — momento en el que el sistema pudo conocer la relación.
- `supporting_observation_ids` — evidencias que sostienen o cuestionan el estado.
- `status_history` — cambios auditables (cuándo, motivo, evidencia).

**Direccionalidad:** `SUPPLIES_TO` va de proveedor a comprador; `REFERS_TO` de emisor de la recomendación al negocio referido; `PARTNERS_WITH` es simétrica y debe canonizarse en almacenamiento para no duplicarse. Un `REFERS_TO` **no** demuestra suministro ni asociación entre empresas. No crear relaciones económicas por proximidad o sector compartido. `SAME_BUSINESS_AS` se usa como hipótesis/proceso de identidad sobre registros de origen; nunca se cuenta como relación económica consolidada.

Las relaciones inferidas no deben presentarse como confirmadas. Una relación descartada puede permanecer en el historial para auditoría, pero no actuar como vínculo válido en las métricas de conectividad vigentes. Una relación confirmada también puede vencer.

### 5.3. Observación (`Observation`)

- `observation_id` — ID único.
- `subject_type` — `COMPANY`, `RELATIONSHIP` o `SOURCE_RECORD`.
- `subject_id` — referencia al objeto o registro observado.
- `attribute` / `assertion_type` y `value` — hecho o afirmación observada (incluyendo negaciones cuando proceda).
- `source_type` y `source_record_id` — origen y identificador de fuente para trazabilidad.
- `observed_at` — fecha a la que corresponde el dato o cuando fue observado por la fuente.
- `recorded_at` — fecha de incorporación al sistema de la Telco; define **cuándo estuvo disponible**.
- `valid_from`, `valid_to` — opcionales, si el hecho tiene vigencia conocida.
- `verification_status` — verificada, pendiente o cuestionada, según reglas explícitas.
- `confidence_score` — opcional, heurístico, no probabilidad calibrada.

No descartar una observación solo porque contradice otra. La consolidación debe ser auditable; si las reglas no permiten elegir un valor, marcarlo como `CONFLICTED` o `UNKNOWN`.

### 5.4. Evento comercial (`CommercialEvent`)

- `event_id` — ID único.
- `company_id` — empresa involucrada según identidad disponible.
- `event_type` — `DISCOVERED`, `CONTACT_ATTEMPT`, `CONTACTED`, `OPPORTUNITY_CREATED`, `PROPOSAL_SENT`, `WON`, `LOST` o equivalente controlado.
- `occurred_at` — cuándo ocurrió.
- `recorded_at` — cuándo ingresó al CRM; indispensable si hay retrasos de registro.
- `channel`, `outcome`, `estimated_cost_mxn` — opcionales y documentados.
- `source_record_id` — registro CRM simulador que sustenta el evento.

Mantener orden temporal plausible: no se puede ganar una oportunidad antes de descubrirla. El resultado de venta no debe utilizarse en el ranking que supuestamente precedió la decisión.

## 6. Fuentes simuladas y límites de acceso

| Fuente | Atributos típicos | Sesgo/limitación simulado | Condición de uso |
|---|---|---|---|
| `CRM` | Contactos, visitas, notas, oportunidades | Omisiones, duplicados, registros tardíos | Solo eventos registrados hasta la fecha de corte |
| `TELCO_INTERNAL` | Servicio contratado, incidencias, sucursales atendidas | Solo clientes existentes; no inventar datos de prospectos | Únicamente información propia y autorizada |
| `DIRECTORY` | Razón/nombre, giro, ubicación, teléfono comercial | Datos viejos, errores y alias | Fuente simulada con procedencia |
| `PUBLIC_PROFILE` | Categoría, sucursales anunciadas, rating, conteo de reseñas | Calificación ≠ intención de compra; dato no verificado | Solo simulación; sin scraping real ni atribución de cifras a Google |
| `REFERRAL` | Recomendación de negocio, mención de vínculo | Subjetividad, posible error | Registro de emisor, fecha y contexto |

No asumir acceso a facturación, pagos, proveedores o clientes de terceros, salvo evidencia autorizada. `PUBLIC_PROFILE.rating` y `review_count` se guardan como señales descriptivas, **sin convertirlos automáticamente en predictores de compra**.

## 7. Reglas de identidad, conflictos y calidad

**Identidad:** normalizar nombres para identificar candidatos; usar identificadores externos fuertes si existen; comparar nombre + ubicación y atributos contextuales; no fusionar registros solo por similitud textual. Conservar `source_record_id`, aliases, historia y motivo de unión. Una sucursal no se convertirá automáticamente en una empresa adicional.

**Calidad mínima:**

1. IDs únicos, referencias válidas y tipos permitidos.
2. Toda afirmación observable tiene `source_type`, `source_record_id` y `recorded_at`.
3. No fabricar atributos faltantes: usar `UNKNOWN` o ausencia explícita según convenio elegido.
4. Conservar contradicciones y registrar resolución, o dejar `CONFLICTED`.
5. El estatus de relación depende de evidencia documentada; no del atractivo comercial del nodo.
6. Registrar intervalos de validez si se conocen; un hecho viejo no es automáticamente falso.
7. Ninguna observación aparece en un corte anterior a `recorded_at`.
8. Evitar relaciones duplicadas del mismo tipo y orientación; para `PARTNERS_WITH`, normalizar orden de IDs.
9. Calcular cobertura sobre empresas canónicas conocidas, distinguiendo el denominador omnisciente (30) **solo en evaluación del simulador**.
10. Evitar filtrar datos privados o campos del oráculo al grafo observable.
11. No utilizar datos reales de empresas ni credenciales en el dataset publicado.
12. La calidad por fuente se reporta por separado; no aplicar una regla universal de "fuente pública = alta confianza".

**Selección de atributo vigente:** privilegiar verificación y consistencia temporal sobre simple recencia. Si hay conflicto no resuelto, conservar incertidumbre y excluir o tratar con cautela la característica del ranking.

## 8. Reglas de generación de datos para la Misión 002B

### Etapa A — Generar mundo sintético

1. Crear exactamente 30 empresas canónicas con IDs estables y sectores del cuadro de trabajo.
2. Asignar perfiles coherentes (tamaño, sucursales, servicios y necesidades) con variabilidad realista, sin hacer que el tamaño o grado del grafo determine siempre la conversión.
3. Crear vínculos verdaderos plausibles: proveedores/compradores y socios; la población puede contener empresas aisladas.
4. Crear eventos/condiciones comerciales latentes independientes en parte del grafo: cobertura Telco, presupuesto, competencia, oportunidad temporal y ejecución del vendedor también influyen.
5. Fijar semilla y registrar supuestos; conservar este universo en zona privada, separada de las consultas operativas.

### Etapa B — Simular fuentes imperfectas

1. Generar registros de origen distintos de empresas canónicas: alias, duplicados candidatos, registros incompletos y una confusión sucursal/empresa.
2. Producir observaciones procedentes de las cinco fuentes con `recorded_at` y opcionalmente `observed_at` diferentes.
3. Incluir como mínimo casos de: información desconocida, referencia no confirmada, contradicción de atributos, relación caducada o descartada y discrepancia temporal.
4. Registrar tanto observaciones acertadas como erróneas según reglas explícitas; **no hacer que todas las evidencias apunten correctamente a los mejores prospectos**.
5. Prohibir referencias a empresas reales o a reseñas reales; todo rating será sintético.

### Etapa C — Cortes temporales y CRM progresivo

- **T0:** exactamente **12 empresas canónicas conocidas en CRM**, con cobertura desigual y atributos incompletos.
- **T1:** llegan nuevas observaciones; el plan aprobado fija 17 empresas conocidas acumuladas.
- **T2:** se enriquecen registros y se conservan candidatos de identidad; el plan aprobado fija 23 empresas conocidas y 7 desconocidas.
- Fechas aprobadas: T0 `2026-01-15T12:00:00Z`, T1 `2026-05-15T12:00:00Z`, T2 `2026-09-15T12:00:00Z`; se utiliza `available_at` para consultar.
- Un corte `as_of=Tn` devuelve exclusivamente observaciones cuyo `recorded_at <= Tn` y eventos comerciales registrados antes de Tn; la vigencia del hecho se interpreta adicionalmente.
- Para cada corte, construir el grafo observable sin leer directamente el universo completo; el grafo debe evolucionar mediante evidencias, no recibir "actualizaciones mágicas" desde la capa privada.

### Etapa D — Aislamiento y evaluación

- Mantener artefactos privados de *ground truth* fuera de la ruta de acceso de consultas o scoring del producto.
- Generar casos intencionales de datos erróneos **sin introducir etiquetas de conversión en atributos de priorización**.
- Comparar baseline y enfoque enriquecido con grafo sobre el **mismo conjunto de prospectos elegibles y el mismo instante de decisión**.
- No confundir descubrir más empresas con elevar conversión de las ya conocidas; informar cobertura, precisión del ranking y costos de adquisición de datos por separado.
- Reservar resultados comerciales futuros para evaluación, nunca para entrenamiento/selección de atributos con fuga temporal.

## 9. Criterios de aceptación de la Misión 002B

Se consideran pruebas obligatorias, no resultados actuales:

| ID | Criterio verificable |
|---|---|
| AC-01 | Los mismos archivos aprobados producen bytes idénticos. No se agrega aleatoriedad ni se requiere semilla en misión 002B. |
| AC-02 | Exactamente 30 empresas canónicas en el universo; sectores suman 30. |
| AC-03 | En T0 existen exactamente 12 empresas canónicas conocidas por CRM; no se exige conocer las 30 en T2. |
| AC-04 | Ninguna consulta del producto ni algoritmo de priorización accede a campos de verdad sintética. |
| AC-05 | Cada observación tiene procedencia y fecha de disponibilidad; no aparecen datos anticipados en cortes as-of. |
| AC-06 | Relaciones dirigidas y simétricas siguen sus reglas; no hay extremos inválidos ni aristas económicas duplicadas. |
| AC-07 | Una referencia no crea automáticamente una relación de proveedor/cliente confirmada. |
| AC-08 | Existe al menos un caso reproducible de duplicado candidato sin fusión arbitraria, y otro que puede resolverse con evidencia fuerte. |
| AC-09 | Existe al menos un conflicto de atributos conservado y trazable, sin sobreescritura de evidencia original. |
| AC-10 | Se registra transición de estado en al menos una relación y se preserva su historia. |
| AC-11 | Datos faltantes, contradictorios y obsoletos pueden identificarse mediante métricas de calidad. |
| AC-12 | Los eventos comerciales respetan cronología; resultados futuros quedan fuera de los rankings históricos. |
| AC-13 | La reconstrucción de T0, T1 y T2 muestra evolución verificable del conocimiento sin requerir que todos los cambios sean mejoras. |
| AC-14 | Pruebas unitarias pasan sin Atlas; conexión real y pruebas de integración se reportan aparte. |
| AC-15 | El repositorio contiene instrucciones comprensibles para juniors y no incluye secretos ni datos personales reales. |
| AC-16 | Cada decisión importante se relaciona con al menos un requisito del reto y con una explicación ejecutiva de su propósito. |

## 10. Evidencia exigible para el reto laboral

| Entregable | Evidencia diseñada |
|---|---|
| Business Framing | Caso de adquisición B2B, usuario comercial, hipótesis y restricciones de información. |
| Economic Graph | Modelo de cuatro entidades, tipos de vínculo, identidad, procedencia, temporalidad y confianza. |
| AI/ML Approach | Señales de grafo propuestas vs baseline; evaluación sin fuga temporal; opciones ML justificadas, no necesariamente implementadas. |
| Architecture | Separación oráculo/observable, ingestión de fuentes heterogéneas, almacenamiento, consultas y futura escalabilidad. |
| Economic Case | Diseño para medir margen de contribución incremental menos costo incremental; experimento real posterior. |
| Control Tower | Métricas propuestas de Graph Health, AI/analytical Performance, Business Funnel y Economic Impact; implementación posterior. |

La **Control Tower** es requisito del reto, aunque su versión inicial sea una PoC. La entrega final también contempla un **brief de 2–3 páginas**, a elaborar en una fase posterior.

## 11. Justificación ejecutiva resumida

> ConectaPyME no necesita conocer todos los negocios para empezar. Necesita saber cuáles datos son confiables, qué relaciones son reales o solo sospechas y cuándo obtuvo cada señal. Este diseño evita llamadas comerciales basadas en información engañosa y prepara una comparación justa para determinar si el conocimiento económico adicional justifica su costo.

**Límite de la afirmación:** esta utilidad es una hipótesis de producto. Las 30 empresas sintéticas permiten demostrar funcionamiento, no causalidad ni ganancias económicas reales.

## 12. Seguimiento de los pendientes del diseño original

1. **Aprobado:** catálogo concreto de 30 empresas, nombres y perfiles; originales restringidos.
2. **Aprobado:** instantes T0/T1/T2 de `09-observability-plan.md`. El historial comercial sigue fuera de esta misión.
3. **Aprobado para 002B:** atributos de las 83 observaciones; los atributos del catálogo no observados permanecen desconocidos.
4. **Aprobado:** plan determinista de 83 observaciones y estados. No representa tasas reales de ausencia/error ni se modifica para favorecer al grafo.
5. **Implementado y probado offline:** ledger e índices justificados en `10-design-validation.md`; integración real pendiente.
6. Precisar cómo el ranking baseline y el enriquecido utilizarán los mismos datos elegibles y qué métricas exploratorias reportarán.
7. Definir costos y supuestos para el caso económico, manteniéndolos identificados como escenarios.

**Criterio de paso satisfecho:** el usuario aprobó catálogo, matriz, calendario y plan de observaciones en misión 002B. Los puntos 1–4 quedan cubiertos en esos paquetes para el alcance actual; no se inventa historial comercial ni se amplía el plan. Índices y contrato físico se documentan en `10-design-validation.md`; baseline y economía siguen fuera de alcance.


**Actualización 002B:** las listas de trabajo de 002A se conservan como contexto histórico. Para este alcance están aprobados catálogo, 48 relaciones, 3 afirmaciones falsas, 3 referencias y 83 observaciones. No se crean eventos comerciales ni se resuelven alias sin evidencia. Las rutas `design-data/` citadas en el diseño corresponden ahora a `design-data/restricted/`; el visor usa exclusivamente `data/observable/observations.json`. Véase `10-design-validation.md` para implementación y discrepancias.
