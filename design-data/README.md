# Ubicación, aprobación y acceso — misión 002B

Este README incorpora el adjunto de los tres paquetes. Todos quedaron **aprobados** para la misión 002B; su procedencia, versión y SHA-256 original están en `manifest.json`.

Los nombres de archivo e IDs se conservan. Por separación física, todos los CSV/JSON citados abajo están en `design-data/restricted/`, no en la raíz de `design-data/`. Los Markdown están en `docs/`. Desde este README se consultan como `../docs/`.

Solo la ingesta y las pruebas del simulador pueden acceder a `restricted/`. La interfaz comercial lee `data/observable/observations.json`, que no contiene campos del oráculo ni empresas sin descubrir. Estos archivos ficticios no son secretos de producción, pero tampoco son entradas autorizadas para un ranking. No montar este directorio en un proceso comercial.

# Catálogo de 30 empresas — Entregable de diseño

Archivos:

- `docs/07-company-catalog.md`: especificación legible, 30 perfiles individuales y reglas de uso.
- `design-data/companies_world_design.csv`: tabla editable para revisar perfiles; **solo diseño de verdad sintética**.
- `design-data/companies_world_design.json`: los mismos perfiles aprobados como referencia exclusiva del simulador.

**No cargar directamente CSV/JSON en el Economic Graph observable ni usar estos campos como entrada al ranking.** Son datos privados del simulador. El CRM T0 y las observaciones T0–T2 se materializan en una capa distinta, con controles de procedencia y fecha.

El paquete de diseño no contiene código ejecutable ni datos reales. Su implementación está en `src/economic_graph/`; no se generaron eventos comerciales ni resultados económicos.

# Relaciones económicas — Paquete de diseño v1.0

**Diseño aprobado por el usuario para misión 002B.** Contiene únicamente datos ficticios y referencias de diseño.

- `docs/08-relationship-matrix.md`: matriz de 48 relaciones y criterios de revisión.
- `design-data/world_relationships_design.csv` y `.json`: verdad sintética de referencia.
- `design-data/false_claims_design.json`: tres afirmaciones equivocadas planificadas, fuera de la verdad.
- `design-data/referrals_design.json`: tres referencias comerciales planificadas.

Requiere el catálogo `07-company-catalog.md` y su JSON. No copiar directamente esta verdad al grafo accesible para ConectaPyME.


# Plan de observabilidad v1.0 — Distrito Centro

**Diseño aprobado por el usuario para misión 002B.** No contiene resultados comerciales.

Archivos:
- `docs/09-observability-plan.md`: reglas, escenarios, criterios de aceptación.
- `design-data/observation_plan.json` y `.csv`: 83 observaciones sintéticas planificadas (28 T0, 26 T1, 29 T2).
- `design-data/company_discovery_plan.json`: 12 T0, 5 T1, 6 T2, 7 NEVER.
- `design-data/relationship_visibility_plan.json`: 48 relaciones aprobadas sin modificarlas.
- `design-data/identity_alias_plan.json`: dos alias candidatos.

**Precaución:** los campos `truth_reference` y `company_id_truth` son identificadores del oráculo sintético para pruebas. **Nunca deben entrar al grafo comercial observable ni al ranking.**

Para Codex: aprobación recibida en misión 002B. Implementar solo construcción, trazabilidad y observabilidad, sin scoring ni eventos comerciales.
