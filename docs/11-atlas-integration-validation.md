# Validación de integración MongoDB Atlas — evidencia 002C y posterior al PR #6

**Estado actual:** validación local reportada por el usuario, ampliada tras integrar el PR #6 en `main`/`c9194ed`. Se conserva abajo el cierre histórico 002C. Ninguna evidencia Atlas de este documento procede de una ejecución de Codex Cloud.
**Entorno de las ejecuciones reportadas:** Windows con VS Code.
**Procedencia:** resultados comunicados por el usuario en esta conversación; **no son ejecuciones realizadas por Codex Cloud**.

## Evidencia histórica local reportada — misión 002C

| Comprobación | Resultado comunicado por el usuario |
|---|---|
| Conexión mediante PyMongo | Exitosa |
| Ping al servidor MongoDB Atlas | Exitoso |
| `validate_design.py` | 0 errores y 5 advertencias conocidas |
| Primera carga | 83 observaciones insertadas |
| Segunda carga | 0 observaciones insertadas y 83 sin cambios |

| Consulta en Atlas | Empresas conocidas | Observaciones |
|---|---:|---:|
| T0 | 12 | 28 |
| T1 | 17 | 54 |
| T2 | 23 | 83 |

Los cortes definidos por el proyecto son T0 `2026-01-15T12:00:00Z`, T1 `2026-05-15T12:00:00Z` y T2 `2026-09-15T12:00:00Z`. Los conteos reportados coinciden con ese plan. No se atribuyen aquí resultados adicionales de relaciones, identidad o rendimiento.

En el reporte histórico 002C el usuario no aportó salidas completas de terminal ni el SHA utilizado localmente. Se conserva la procedencia como reporte del usuario, sin inventar una traza de ejecución, versiones, fecha de ejecución o commit local. No se publican URI, contraseñas ni otros valores de credenciales.

## Qué permite concluir el reporte 002C

Según las ejecuciones locales reportadas, el proyecto pudo conectarse y recibir una respuesta real de Atlas, persistir las 83 observaciones y recuperarlas en los tres cortes. La segunda carga demuestra ausencia de nuevas inserciones y conservación de los 83 registros en esa repetición concreta.

Las cinco advertencias conocidas permanecen documentadas como DV-001 a DV-005 en [la auditoría del diseño](10-design-validation.md). El resultado de 0 errores no las elimina ni aporta evidencia nueva para fusionar alias o inventar transiciones/caducidades.

## Separación respecto a Codex Cloud — cierre histórico 002C

La validación real anterior corresponde a Windows con VS Code. Los intentos previos de conexión desde Codex Cloud no obtuvieron un ping exitoso; el último diagnóstico fue un timeout de resolución DNS/SRV. El éxito local no demuestra que esa conectividad cloud se haya resuelto.

Para este cierre, Codex Cloud ejecuta únicamente pruebas offline y comprobaciones de Ruff. No repite cargas ni consultas reales contra Atlas y no modifica su configuración de seguridad. La prueba opcional de integración queda excluida de esa ejecución de pruebas, sin presentarla como aprobada.

En el cierre 002C, el README incluía comandos de instalación, validación, carga y consulta como referencia. La ruta actual del [README](../README.md) utiliza el ledger existente y separa Atlas de solo lectura de las herramientas de carga; documentarlas no equivale a ejecutarlas de nuevo.

Comprobaciones históricas ejecutadas por Codex Cloud para el cierre documental 002C (no son el total actual de pruebas):

| Comando | Resultado |
|---|---|
| `uv run pytest -m "not integration"` | 97 pruebas aprobadas; 1 prueba de integración excluida |
| `uv run ruff check .` | Correcto |
| `uv run ruff format --check .` | Correcto |

Estos resultados de pruebas offline y calidad no sustituyen ni reproducen la validación Atlas local reportada arriba.

## Alcance del cierre histórico 002C

La misión 002C registra evidencia técnica de conectividad, persistencia, repetición de carga y consultas temporales, con la procedencia indicada. No acredita seguridad de roles, escalabilidad, latencia, métricas de ML ni valor económico incremental.

En aquella misión quedaron fuera de alcance funcionalidades nuevas, scoring, eventos comerciales, ventas simuladas, evaluación causal y Control Tower. Rankings, calculador e interfaz se implementaron posteriormente; su estado actual está en la [matriz](02-challenge-traceability.md). El reto de Totalplay sigue requiriendo justificar cómo el Economic Graph produciría valor y cómo se mediría de forma incremental; esta validación técnica no demuestra ese efecto.

## Validación posterior al merge del PR #6 — reporte local del usuario

**Versión reportada:** rama `main`, commit `c9194ed8425cc1f62eaac6174656a658810e6597` (`c9194ed`), PR #6 integrado, árbol limpio y sin cambios locales pendientes. **Entorno reportado:** Windows 11, PowerShell y VS Code. No se atribuye una fecha de ejecución ni una versión adicional de herramientas que no se haya comunicado para esta validación.

**Procedencia:** ejecuciones locales reportadas por el usuario al solicitar la misión 005C. Codex verificó el merge y el SHA en GitHub; **no ejecutó los comandos contra Atlas, no accedió a Atlas y no realizó una ejecución nativa Windows** en esta auditoría.

### Conexión y lectura T2

Comandos comunicados por el usuario:

```powershell
uv run python scripts/check_connection.py
uv run python scripts/inspect_graph.py --as-of T2 --summary --mongo
```

Respuesta de ping reportada:

> Conexión verificada: MongoDB respondió a ping. No se escribieron datos.

Salida de la consulta T2 reportada:

```json
{
  "as_of": "2026-09-15T12:00:00Z",
  "companies": 23,
  "relationship_claims": 26,
  "referrals": 3,
  "observations": 83,
  "identity_candidates": 2,
  "conflicted_attributes": 2
}
```

Las 26 son **afirmaciones económicas observables**, no 26 relaciones confirmadas ni una comprobación contra la verdad sintética. Las tres referencias se cuentan aparte; dos candidatos de identidad y dos atributos en conflicto no se consideran resueltos.

El usuario también confirmó la ejecución de las cinco vistas mediante `uv run --group ui streamlit run app/control_tower.py` y reportó una captura en modo **Atlas · solo lectura** con indicadores y rankings T2 esperados. Se registra como evidencia visual reportada por él; no se adjunta ni se inventa una captura, ruta, huella o inspección de imagen por Codex en esta auditoría. No se reportó una ejecución independiente de `rank_companies.py --mongo`.

### Instalación y calidad en Windows, sobre la misma versión reportada

| Comando local reportado | Resultado comunicado |
|---|---|
| `uv sync --locked --group ui` | Instalación correcta |
| `uv run --group ui pytest -m "not integration"` | 284 aprobadas; una prueba de integración excluida |
| `uv run ruff check .` | Sin errores |
| `uv run ruff format --check .` | 60 archivos con formato correcto |
| `uv run --group ui streamlit run app/control_tower.py` | Resumen, Graph Health, AI Performance, Business Funnel y Economic Impact funcionales |

**La prueba marcada como integración se excluyó de pytest.** Ping, consulta explícita y revisión local de la UI son evidencias separadas; no equivalen a ejecutar toda la suite de integración contra Atlas.

### Operaciones no ejecutadas y límites

Esta validación posterior no reporta nuevas cargas ni pruebas de escritura. No se ejecutaron en 005C inserciones, actualizaciones, borrados, creación de índices ni cambios de seguridad de Atlas. La carga inicial y su repetición pertenecen exclusivamente al reporte histórico 002C, no a una nueva operación sobre `c9194ed`.

El ping acredita una respuesta del servidor en el entorno local reportado y la consulta acredita lectura T2 con esos conteos. No prueba conectividad cloud, permisos de escritura, mínimo privilegio de los roles, rendimiento a escala, disponibilidad continua o paridad exhaustiva de cada documento. Los conteos no validan hechos empresariales reales. Tampoco se ejecutó un A/B ni se midieron conversiones, ventas, margen incremental o ROI.

La aprobación de las políticas y supuestos sigue siendo metodológica para la PoC educativa, sin autorización de contactos, presupuesto, piloto o despliegue. No se publican valores de credenciales, URI ni direcciones privadas.

## Comprobaciones de la auditoría documental 005C — Codex Cloud/Linux

Sobre la base integrada `c9194ed`, con Python 3.12.14, Codex ejecutó `uv sync --locked --group ui`, `RUN_MONGODB_INTEGRATION=0 uv run --group ui pytest -m "not integration"`, `uv run --group ui ruff check .` y `uv run --group ui ruff format --check .` (con caché uv en una ruta escribible). Resultado: **284 aprobadas, una integración excluida; Ruff correcto y 60 archivos con formato correcto**.

También reprodujo los resúmenes T0/T1/T2, rankings y escenarios financieros **offline**. La coincidencia del resumen local del ledger con el conteo Atlas reportado es una comprobación documental; no es una nueva consulta al servidor ni una ejecución de la suite Atlas. No hubo revisión de navegador o ejecución Windows nueva de Codex en 005C. Comandos de reproducción de solo lectura: [README](../README.md).
