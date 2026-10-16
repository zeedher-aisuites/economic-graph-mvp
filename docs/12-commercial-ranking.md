# Rankings comerciales comparables — misión 003A

**Estado:** política conservadora, elegibilidad y capacidad aprobadas explícitamente por el usuario en la conversación de misión 003A. Implementación determinista y comparación offline disponibles. Sin resultados económicos medidos.

## Pregunta y alcance

¿Qué cuentas elegirían dos políticas con las mismas empresas conocidas, el mismo corte y la misma capacidad comercial? Esta comparación cubre el bloque 3, AI/ML Approach, de la [matriz del reto](02-challenge-traceability.md), apoyada por Economic Graph y Architecture. No mide ventas, conversión ni efecto causal.

La única entrada local autorizada para el ranking es `data/observable/observations.json`. La alternativa remota es la lectura temporal existente de `m002b_observations` en la base dedicada `conectapyme_mvp_observable`. El cálculo no necesita ni consulta catálogo, conciliación, planes del simulador ni etiquetas de verdad.

## Auditoría previa de señales

Base revisada: `main` en `dae0d4e`, que incluye el cierre documental 002C. Los conteos siguientes se obtuvieron en Codex Cloud leyendo el ledger observable mediante `snapshot`, sin consultar el mundo restringido.

| Dato disponible sin conflicto | T0, 12 empresas | T1, 17 empresas | T2, 23 empresas | Utilidad y límite |
|---|---:|---:|---:|---|
| Nombre | 12 | 17 | 23 | Identificación, sin puntuar |
| Sector | 12 | 13 | 13 | Contexto; no existe prioridad sectorial comercial aprobada |
| Sucursales | 2 | 3 | 3 | Posible señal exploratoria de complejidad operativa |
| Tamaño empresarial | 0 | 0 | 0 | No utilizable: desconocido o en conflicto |
| Calificación pública | 0 | 2 | 3 | No demuestra necesidad de conectividad ni intención de compra |
| Cantidad de reseñas | 0 | 1 | 2 | No se equipara a volumen de ventas o presupuesto |
| Servicio activo | 0 | 0 | 2 | Ambos valores observados son verdaderos y confirmados; el resto es desconocido |
| Vínculos económicos CONFIRMED | 2 | 2 | 4 | Evidencia relacional disponible, sin consultar su verdad sintética |

Las sucursales de Hornos del Centro están en conflicto desde T1: no se arbitran el valor inicial y los posteriores. El tamaño de Ferretería Cinco Calles está en conflicto en T2. La repetición de una observación compatible no aporta una sucursal ni un vecino extra. Los alias permanecen candidatos y no añaden cuentas canónicas.

No existen observaciones de necesidad de producto, presupuesto, permiso de contacto, no-cliente confirmado, conversión, ingreso ni margen. Ninguna de esas características se reconstruirá por inferencia silenciosa.

## Política aprobada e implementada

Versión `003a-conservative-v1`. Los números son parámetros de una política exploratoria aprobada, no estimaciones estadísticas ni probabilidades.

1. **Elegibilidad:** empresas conocidas al corte, excluyendo únicamente aquellas con servicio activo confirmado y sin conflicto. El resto son cuentas por investigar; no se afirma que sean prospectos nuevos. Se conserva el motivo y la evidencia de cada exclusión. No se excluyen todas las identidades NEEDS_REVIEW, pues ninguna tiene resolución fuerte; esa limitación sigue visible.
2. **Baseline:** `10 × min(max(sucursales − 1, 0), 5)`. Solo valores observados REPORTED o CONFIRMED, sin conflicto, aportan puntos. Desconocido, inferido, descartado o en conflicto no aporta puntos, pero tampoco se convierte en un hecho de cero sucursales.
3. **Grafo:** baseline más `5 × min(vecinos económicos confirmados distintos, 4)`. Se cuentan extremos conocidos de SUPPLIES_TO y PARTNERS_WITH, sin duplicar vecinos por dirección o evidencia repetida. No se interpreta dirección de suministro como dirección de venta Telco. Una referencia comercial no se convierte en vínculo económico confirmado. REPORTED, INFERRED, DISCARDED y conflictos no aportan puntos relacionales.
4. **Capacidad:** cinco cuentas por corte para cada política. Se ordena por puntuación descendente y, en empate, por ID público ascendente. El desempate asegura repetibilidad; no tiene significado comercial. Se advierte cuando el límite de selección atraviesa un empate.

Los clientes excluidos de adquisición pueden seguir aportando contexto como vecinos conocidos; no compiten por las cinco plazas. Esta regla formó parte de la propuesta de elegibilidad aprobada.

Los máximos de 50 puntos individuales y 20 relacionales acotan la influencia de cada señal. No se han ajustado para lograr cambios de selección ni se sostiene que sean óptimos. Usar vínculos reportados con peso menor sería una alternativa, pero exigiría aprobar la política de incertidumbre y su peso; esta versión conserva esos reportes como contexto sin puntuarlos. El baseline es una regla de referencia para la PoC, no una política comercial observada de una Telco real.

## Cómo leer la comparación

- **Característica o feature:** un dato calculable al corte, por ejemplo sucursales adicionales o vecinos distintos confirmados.
- **Scoring:** regla que transforma las características en puntos. Una contribución de cero puede deberse a incertidumbre; debe verse el estado junto al valor.
- **Ranking:** orden de las cuentas por puntuación, con un desempate explícito.
- **Baseline:** política de referencia basada solo en atributos individuales. La variante con grafo debe conservar exactamente esa base.
- **Top-K:** primeras K cuentas que caben en una capacidad hipotética. No representa contactos realizados ni una recomendación automática de contacto.
- **Sesgo:** los negocios mejor documentados pueden acumular más señales y puntos. La ausencia de evidencia puede reducir prioridad aunque la cuenta sea valiosa. Los atributos y las relaciones del escenario sintético no representan una muestra del mercado.
- **Evaluación:** posiciones, diferencias y selección permiten describir cómo cambia una decisión. Sin etiquetas ni resultados comerciales no se calculan precisión predictiva, ingresos, ROI ni incremento causal de ventas.

## Implementación y contrato de salida

[`rankings.py`](../src/economic_graph/rankings.py) reconstruye una vista `as_of` a partir de `available_at <= as_of`, usando los cortes exactos de `contracts.CUTS`. Ambas políticas comparten esa vista y la misma lista elegible. La API `compare_rankings(rows, as_of)` no lee archivos, abre red ni escribe datos. No completa perfiles ni fusiona candidatos.

La [CLI](../scripts/rank_companies.py) carga solo el ledger observable o, mediante `--mongo`, reutiliza `read_observations`. La base se comprueba antes de conectar y la consulta filtra por disponibilidad en el servidor. No se cambiaron las funciones de carga ni se ejecutó la integración que escribe datos. La validación real documentada en [002C](11-atlas-integration-validation.md) procede del usuario desde Windows; no demuestra una nueva ejecución cloud de rankings en Atlas. La paridad de rankings local/MongoDB se verifica con un doble que solo admite `find`; integración real de rankings en Atlas **no verificada**.

La salida JSON contiene:

- `policy`: versión, capacidad, pesos, topes y reglas. Cambiar prioridades comerciales requiere nueva aprobación, versión y regresiones actualizadas.
- `as_of` y `visible_input_sha256`: corte y huella del contenido visible ordenado; añadir datos futuros no cambia el reporte histórico ni su huella.
- `companies`: misma cohorte para ambas políticas; puntuaciones, posiciones, diferencia, selección y contribuciones. Cada característica conserva evidencia completa con fuente, registro, fechas y estado.
- `excluded`: cuentas con servicio activo confirmado y su evidencia, sin ocupar plazas.
- `top_k` y `comparison`: selecciones ordenadas, coincidencias, entradas/salidas, empates en el límite y plazas sin cubrir si hay menos de cinco elegibles. `position_change = posición baseline − posición grafo`; positivo significa subir.
- `relationship_context`, `identity_candidates` y `conflicts`: afirmaciones, historia, incertidumbre e identidades pendientes, sin arbitraje ni datos del simulador.

El formato Markdown resume las posiciones y contribuciones; para auditar las observaciones concretas se usa el JSON. `policy.capacity` permanece fija en cinco en esta versión, sin opción de CLI para cambiarla silenciosamente.

## Reglas frente a evidencia problemática

Se conservan todos los valores históricos de un atributo. Si difieren, la característica queda CONFLICTED sin valor utilizable; ni siquiera una confirmación posterior resuelve ese conflicto. Si coinciden, se comprueba el estado de la evidencia más recientemente disponible: REPORTED o CONFIRMED permiten usar sucursales; INFERRED/DISCARDED no. Estados distintos en el mismo instante quedan VERIFICATION_CONFLICTED. Servicio activo solo excluye si su valor es verdadero, no conflictivo y ese último estado es inequívocamente CONFIRMED. No se inventa una caducidad.

Para vínculos se conserva la historia y se toma el estado disponible más reciente; estados simultáneos incompatibles o cambios de extremos/tipo bajo el mismo ID impiden puntuar. Si afirmaciones con IDs distintos sobre el mismo hecho económico se oponen con confirmación y descarte, se conserva el conflicto y no se puntúa ese hecho. Repetir observaciones, repetir un hecho con otro ID o tener varios tipos/direcciones hacia el mismo vecino no multiplica la característica: cuenta vecinos distintos. Esto no fusiona registros ni empresas. Un cero aquí significa «ningún vecino confirmado utilizable», no «no tiene relaciones en el mundo».

CONFLICTED, VERIFICATION_CONFLICTED, INSUFFICIENT_EVIDENCE y NOT_ECONOMIC son diagnósticos derivados de la política; no sustituyen ni modifican los estados originales del ledger. Los casos adicionales de transiciones y contradicciones de las pruebas son fixtures identificados, no hechos añadidos al diseño aprobado.

## Resultados reproducibles y límites

La [tabla completa T0/T1/T2](13-ranking-comparison.md) fue generada ejecutando la CLI offline en Codex Cloud sobre el ledger aprobado. Con cinco plazas por política, coinciden dos cuentas y se sustituyen tres en cada corte. El baseline atraviesa un empate en los tres cortes y el grafo en T1/T2: varias selecciones dependen del desempate técnico. No se ajustaron los pesos después de observar estos resultados.

T0/T1 comparan 12/17 cuentas. En T2 son 21 de 23 conocidas: se excluyen Enlace Punto POS y Ferretería Cinco Calles por servicio activo confirmado. Por ejemplo, Café Jacaranda pasa de 0 a 10 puntos en T2 por dos vecinos económicos confirmados; esos puntos no acreditan intención de compra. Hornos del Centro recibe cero puntos por sucursales en conflicto y 10 por dos vecinos confirmados.

Los reportes e inferencias que no puntúan siguen visibles: no se descubre su verdad por consultar el oráculo. La política conservadora reduce el uso de afirmaciones no confirmadas a costa de perder señales potencialmente útiles. La etiqueta CONFIRMED del ledger tampoco es garantía externa de exactitud.

Siguen pendientes necesidad de producto, cobertura, permisos de contacto y validación de no-cliente; una plaza representa una cuenta por investigar, no autorización de contacto. Tampoco existen etiquetas para validar precisión, costos, conversiones ni un contrafactual para medir efecto. La elección de estos pesos necesita evaluación futura con datos autorizados y capacidad comparable; un cambio de ranking no demuestra superioridad comercial.

## Verificación

Las pruebas de `test_rankings.py` y `test_ranking_commands.py` cubren cohortes iguales, baseline compartido, top-5 de regresión, límites temporales, explicaciones, topes, incertidumbre, conflictos, duplicados, alias, ausencia de campos restringidos y lectura MongoDB sin escrituras. El cálculo se prueba con acceso a archivos bloqueado; la CLI se ejecuta también desde un directorio con solo módulos públicos y el ledger, sin simulador, diseños ni `.env`.

Comprobaciones ejecutadas en Codex Cloud para esta implementación:

| Comando | Resultado |
|---|---|
| `uv sync --locked` | Correcto; dependencias y lockfile sin cambios |
| `uv run pytest` | 151 aprobadas, 1 integración omitida; incluye 54 pruebas nuevas de rankings |
| `uv run ruff check .` | Correcto |
| `uv run ruff format --check .` | Correcto |
| `uv run python scripts/rank_companies.py --all-cuts --format markdown` | Comparación offline T0/T1/T2 reproducida en `13-ranking-comparison.md` |

La ejecución de pytest fijó `RUN_MONGODB_INTEGRATION=0` en el proceso para impedir expresamente la integración histórica que escribe. Los dobles no sustituyen una lectura real de Atlas ni validación comercial. Los comandos de PowerShell del [README](../README.md) son instrucciones reproducibles; estas comprobaciones se ejecutaron en Linux, no en Windows.
