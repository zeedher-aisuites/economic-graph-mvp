# Rankings comerciales comparables — misión 003A

**Estado:** auditoría previa completada; política de puntuación propuesta, pendiente de aprobación explícita del usuario. Todavía no hay scoring implementado en esta misión.

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

## Política propuesta para revisión

Las reglas de esta sección no están aprobadas todavía. Los números son parámetros de una política exploratoria, no estimaciones estadísticas ni probabilidades.

1. **Elegibilidad propuesta:** empresas conocidas al corte, excluyendo únicamente aquellas con servicio activo confirmado y sin conflicto. El resto son cuentas por investigar; no se afirma que sean prospectos nuevos. Se conserva el motivo y la evidencia de cada exclusión. No se excluyen todas las identidades NEEDS_REVIEW, pues ninguna tiene resolución fuerte; esa limitación seguirá visible.
2. **Baseline propuesto:** `10 × min(max(sucursales − 1, 0), 5)`. Solo valores observados REPORTED o CONFIRMED, sin conflicto, podrían aportar puntos. Desconocido, inferido, descartado o en conflicto no aporta puntos, pero tampoco se convierte en un hecho de cero sucursales.
3. **Grafo propuesto:** baseline más `5 × min(vecinos económicos confirmados distintos, 4)`. Se cuentan extremos conocidos de SUPPLIES_TO y PARTNERS_WITH, sin duplicar vecinos por dirección o evidencia repetida. No se interpreta dirección de suministro como dirección de venta Telco. Una referencia comercial no se convierte en vínculo económico confirmado. REPORTED, INFERRED, DISCARDED y conflictos no aportan puntos relacionales.
4. **Capacidad propuesta:** cinco cuentas por corte para cada política. Se ordena por puntuación descendente y, en empate, por ID público ascendente. El desempate asegura repetibilidad; no tiene significado comercial. Se debe advertir cuando el límite de selección atraviese un empate.

Los clientes excluidos de adquisición pueden seguir aportando contexto como vecinos conocidos; no compiten por las cinco plazas. Esta regla también forma parte de la propuesta de elegibilidad.

Los máximos de 50 puntos individuales y 20 relacionales acotan la influencia de cada señal. No se han ajustado para lograr cambios de selección ni se sostiene que sean óptimos. Usar vínculos reportados con peso menor sería una alternativa, pero exigiría aprobar la política de incertidumbre y su peso; la propuesta inicial conserva esos reportes como contexto sin puntuarlos.

## Cómo leer la comparación

- **Característica o feature:** un dato calculable al corte, por ejemplo sucursales adicionales o vecinos distintos confirmados.
- **Scoring:** regla que transforma las características en puntos. Una contribución de cero puede deberse a incertidumbre; debe verse el estado junto al valor.
- **Ranking:** orden de las cuentas por puntuación, con un desempate explícito.
- **Baseline:** política de referencia basada solo en atributos individuales. La variante con grafo debe conservar exactamente esa base.
- **Top-K:** primeras K cuentas que caben en una capacidad hipotética. No representa contactos realizados ni una recomendación automática de contacto.
- **Sesgo:** los negocios mejor documentados pueden acumular más señales y puntos. La ausencia de evidencia puede reducir prioridad aunque la cuenta sea valiosa. Los atributos y las relaciones del escenario sintético no representan una muestra del mercado.
- **Evaluación:** posiciones, diferencias y selección permiten describir cómo cambia una decisión. Sin etiquetas ni resultados comerciales no se calculan precisión predictiva, ingresos, ROI ni incremento causal de ventas.

## Contrato técnico previsto

El cálculo reconstruirá una vista `as_of` a partir de `available_at <= as_of`, usando los cortes exactos de `contracts.CUTS`. Ambas políticas compartirán esa vista y la misma lista elegible. Los reportes deberán incluir versión y parámetros, contribución por característica, estado de disponibilidad/conflicto y observaciones de respaldo con fuente y fechas. No se completarán perfiles ni se fusionarán candidatos.

La lectura Atlas será opcional y de solo lectura, reutilizando `read_observations`. No se cambiarán las funciones de carga ni se ejecutará la integración que escribe datos. La validación real documentada en [002C](11-atlas-integration-validation.md) procede del usuario desde Windows; no demuestra una nueva ejecución cloud de rankings en Atlas.

Pruebas previstas: igualdad de cohortes y baseline compartido; cortes históricos invariables frente a datos posteriores; reglas y sumas explicables; falta de evidencia; conflictos sin arbitraje; duplicados sin inflación; candidatos sin fusión; estados no confirmados sin promoción; rechazo de entradas restringidas; ejecución con solo el ledger público y sin red; lectura MongoDB contra un doble sin operaciones de escritura.

## Decisiones pendientes

El usuario debe confirmar la fórmula/pesos, elegibilidad y K antes de implementar el scoring. Se presentó la propuesta en la conversación. No se interpreta el silencio como aprobación ni se ejecutan rankings con decisiones de negocio pendientes.

La base existente se instaló con `uv sync --locked` y pasó 97 pruebas offline, con 1 integración omitida, además de Ruff y formato. Estos resultados verifican el punto de partida, no un ranking todavía inexistente.
