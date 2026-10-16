# Caso económico incremental — diseño 003B

**Estado: propuesta para revisión; supuestos económicos no aprobados.** Este documento define fórmulas y escenarios, sin implementar un simulador financiero, generar ventas ni ejecutar un experimento. Versión de diseño: `003b-design-v1`.

## 1. Auditoría y pregunta de inversión

Base: `main` en `0e1088c233f4b49eaf22deab8161d6d610748656`, con el PR #4 integrado, incluida su corrección de portabilidad. Se revisaron las 13 diapositivas y notas del [reto original](../presentations/references/Reto-AI-Engineering-SME-Economic-Graph.pptx), la [trazabilidad](02-challenge-traceability.md), el alcance, DEC-004/009 y los [rankings aprobados](12-commercial-ranking.md).

Las diapositivas 4, 5 y 8 exigen conectar la señal con decisión e impacto; la 10 pide margen, CAC, LTV, ROI y payback dentro de la Control Tower; la 12 exige caso económico y brief final. Estas son métricas que debemos justificar según los datos disponibles, no resultados existentes. El score 87 de la diapositiva 8 y el funnel de la 11 son ilustraciones del reto, no parámetros financieros de esta PoC.

La pregunta propuesta es: **a igual capacidad comercial, ¿el margen adicional generado por cambiar la priorización cubre los costos incrementales de construir y operar el grafo?** La comparación se refiere a las dos reglas aprobadas, no a una política actual de Totalplay observada. DEC-004 sigue siendo una propuesta metodológica; aprobar el alcance documental 003B no aprueba sus parámetros.

| Categoría | Evidencia disponible | Qué permite concluir |
|---|---|---|
| Observación técnica real reportada por el usuario | Ping, carga idempotente y consultas Atlas desde Windows; [002C](11-atlas-integration-validation.md) | Funcionamiento técnico local reportado; sin ventas ni costos medidos |
| Datos y resultados sintéticos reproducidos offline | Ledger público de 83 observaciones; conocidas 12/17/23; elegibles 12/17/21; K=5; dos seleccionadas en común y tres sustituciones por corte | Cambian las selecciones; no se deriva una tasa de conversión de esos cambios |
| Supuestos financieros propuestos | Conversiones esperadas, márgenes, costos, volumen y horizonte de las secciones siguientes | Explorar condiciones de rentabilidad; no describir desempeño observado |
| Resultados medibles solo con datos comerciales autorizados y experimento | Activaciones, margen por cuenta asignada, costos y efecto con incertidumbre | Estimar incrementalidad bajo el protocolo y sus limitaciones |

Se auditó únicamente el ledger observable: sus atributos son nombre, sector, tamaño, sucursales, calificación, reseñas, servicio activo, afirmaciones relacionales y alias. No hay conversiones, precios, facturación, costos ni eventos comerciales. **Desconocido no significa cero ventas.** No se consultó el oráculo para proponer resultados económicos.

Las reglas `003a-conservative-v1`, sus pesos, elegibilidad, desempate y capacidad de cinco cuentas permanecen intactos. T0/T1/T2 son instantáneas superpuestas: no son tres cohortes independientes, quince clientes contactados ni tres brazos experimentales.

## 2. Variables y datos que faltan

Propuesta de unidad monetaria: MXN nominales, sin IVA recuperable, antes de financiamiento e impuesto sobre la renta; confirmar con Finanzas. Cada entrada futura deberá tener unidad, definición, período, fuente, responsable, estado (observado/supuesto), versión y fecha de aprobación.

| Variable | Definición y unidad | Estado y fuente futura requerida |
|---|---|---|
| `K` | Capacidad por bolsa comercial y corte: cinco cuentas | Aprobada solo para 003A; extenderla a bolsas experimentales requiere aprobar el protocolo |
| `J` / `S=K×J` | Bolsas distintas a desplegar / plazas comerciales totales de una campaña | Volumen hipotético, sin mercado ni personal acreditados; validar con Comercial |
| `N` | Todas las cuentas elegibles de esas bolsas, incluidas no seleccionadas | La PoC conoce 12/17/21 elegibles por corte; no acredita una población real desplegable |
| `p_B`, `p_G` | Probabilidad de primera activación de adquisición antes de `W`, por plaza seleccionada bajo cada política | Desconocida; CRM/facturación/activación autorizados. Una plaza sin contacto o sin cierre no se retira del denominador |
| `Δp=p_G−p_B` | Diferencia absoluta de probabilidades | Supuesto de escenario o estimación futura; nunca derivada del score, vecinos o cambios del top-5 |
| `R_im`, `V_im` | Ingreso neto cobrable y costo variable de prestar servicio a cuenta `i` en mes `m` | Desconocidos; Finanzas, facturación, ajustes y operación. Incluir impago/reembolsos sin descontarlos dos veces |
| `I_i`, `t_i` | Instalación, equipo subsidiado y comisión por alta; momento de activación | Desconocidos; evitar duplicarlos en otros costos |
| `M_a(H)` | Margen por primer contrato activado bajo brazo `a`, en valor presente hasta el horizonte común `H` | Supuesto; en producción derivado de ingreso, servicio, fecha de activación, permanencia y alta |
| `c_a`, `Δc=c_G−c_B` | Costo comercial por plaza / diferencia entre políticas, en valor presente | Desconocido; tiempo de prospección y validación, viajes e intentos fallidos. Comisión de alta ya está en `I_i` |
| `F` | Costo fijo futuro incremental frente al baseline | Cotizar construcción/adaptación, integración, evaluación/piloto y puesta en operación; no recontar gastos ya incurridos |
| `ΔO(H)` | Operación incremental durante `H`, en valor presente | Adquisición/licencias de datos, infraestructura, almacenamiento, actualización, revisión de identidad, soporte y gobierno; restar costos equivalentes del baseline |
| `ΔU(H)` | Diferencia de margen de cuentas no seleccionadas y otros canales dentro de la población | Desconocida; contempla sustitución/canibalización y spillovers internos. Cero es un supuesto, no una comprobación |
| `W`, `H`, `d` | Ventana de activación, horizonte desde asignación y descuento mensual | Propuestos: 90 días, 12 meses y 1% mensual. Requieren aprobación y datos de duración del ciclo comercial |
| `B_reserva` | Colchón de inversión adicional al punto de equilibrio | Propuesta: 20% de `F+ΔO`; tolerancia al riesgo por aprobar |

Una bolsa es una cartera comercial sin cuentas repetidas en la campaña, no una réplica de los 30 negocios ficticios. `J` de despliegue no es el número de unidades que necesita el A/B. La capacidad total, el personal y el número de cuentas disponibles deben verificarse antes de proyectar escala.

Costos comunes que no cambian entre políticas cancelan en la diferencia, pero deben constar en el presupuesto total. No se presenta capacidad liberada como ahorro de caja si la nómina no disminuye; su costo de oportunidad se registra aparte, sin sumarlo otra vez. Un servicio cloud gratuito hoy tampoco garantiza costo cero de producción. No se han solicitado precios ni modificado infraestructura.

El costo comercial total de campaña se distribuye entre las plazas para obtener `c_a`, incluyendo la validación de candidatos que luego no se seleccionan. `U_a` recoge su margen de contratos, sin restar otra vez esos costos comerciales. La revisión técnica de identidad del grafo pertenece a operación; la calificación comercial pertenece a prospección: una misma hora o factura solo puede aparecer en una categoría.

## 3. Modelo financiero propuesto

`a=B` es baseline y `a=G` es la misma base con grafo. Se propone una sola campaña por cuenta, una primera alta de adquisición como máximo y seguimiento común desde la asignación. Todos los importes se llevan a valor presente en esa fecha.

Para un contrato activado antes de `W`:

```text
M_a(H) = E[ Σ(m=1..H) activo_im × (R_im − V_im)/(1+d)^m
            − I_i/(1+d)^t_i | activación antes de W, política a ]
```

`activo_im` incorpora activación tardía y baja: no se asignan doce mensualidades completas a alguien que activa en el mes tres. El costo de alta incluye instalación y comisión; costos de intentos sin alta se registran en `c_a`. La fórmula es una definición propuesta, no una estimación de permanencia. En la tabla de escenarios `M` se introduce directamente como un supuesto ya descontado; no se vuelve a descontar.

```text
V_a = S × p_a × M_a(H) − S × c_a + U_a(H) − F_a − O_a(H)

ΔV = S × [p_G × M_G − p_B × M_B − Δc] + ΔU − F − ΔO
```

`F` y `ΔO` ya son diferencias frente al baseline, no costos de ambos brazos sumados. Gastos futuros de piloto/medición se incluyen una sola vez en `F`; gastos pasados se revelan aparte como costos hundidos para la decisión prospectiva. No se mezclan márgenes de doce meses con un costo de operación de un solo mes.

Para aislar inicialmente la hipótesis de priorización se propone **igual margen condicional por contrato en ambos brazos**, `M_G=M_B=M`:

```text
ΔV = S × (Δp × M − Δc) + ΔU − F − ΔO
```

No se supone que las activaciones de las cuentas seleccionadas sean todas causadas por el contacto. `p_a` describe el resultado esperado bajo cada política; `ΔU` evita ocultar efectos en el resto de la población. El experimento mide ambas partes por intención de tratar, sin seleccionar solo los cierres. El supuesto de margen igual debe relajarse si cambia la mezcla de contratos; entonces se usa la fórmula general.

ROI, CAC y payback son secundarios: no se calculan aquí. Un ROI de escenario, si se autoriza después, deberá definir inversión y costos sin duplicarlos, y marcarse como hipotético. CAC incremental carece de interpretación útil si las altas incrementales son nulas o negativas. El payback necesita flujos temporales, no solo el saldo a doce meses; el LTV requiere permanencia más allá de `H` que hoy se desconoce.

## 4. Escenarios para aprobación, no resultados

**Todos los números económicos de esta tabla son supuestos pedagógicos propuestos, sin cotización ni evidencia de mercado.** No son metas aprobadas, pronósticos calibrados ni salidas del ranking. No se asignan probabilidades a los escenarios.

| Entrada | Conservador / deterioro | Base hipotética | Optimista hipotético |
|---|---:|---:|---:|
| `J` bolsas distintas de despliegue | 100 | 100 | 100 |
| `K` / `S` plazas por política | 5 / 500 | 5 / 500 | 5 / 500 |
| `p_B` | 10% | 10% | 10% |
| `Δp`, puntos porcentuales absolutos | −2 pp | +2 pp | +5 pp |
| `p_G=p_B+Δp` | 8% | 12% | 15% |
| `M`, MXN por contrato, mismo valor B/G | 4 000 | 8 000 | 12 000 |
| `c_B`, MXN por plaza | 300 | 300 | 300 |
| `Δc`, MXN por plaza | 100 | 50 | 25 |
| `F`, MXN incrementales | 20 000 | 10 000 | 5 000 |
| `ΔO`, MXN incrementales en 12 meses | 12 000 | 6 000 | 3 000 |
| `ΔU`, MXN en población no seleccionada | −1 000 | 0 | 0 |
| `W` / `H` / `d` | 90 días / 12 meses / 1% mensual | Igual | Igual |

El volumen de 100 bolsas es una hipótesis de despliegue que necesita aprobación propia; no amplía la capacidad del código ni demuestra que existan 500 oportunidades. Se mostrará también `J=1` para mantener visible el costo de una demostración de cinco plazas. No se sumarán T0/T1/T2 para aumentar volumen ni se reutilizará una cuenta como adquisición nueva.

Debe evaluarse además un escenario **nulo**: `Δp=0`, `ΔU=0`, con los costos del caso base. Se permite pérdida económica y no se elige un escenario por favorecer al grafo. No se generan conversiones enteras por empresa: una esperanza matemática fraccionaria futura tampoco sería una venta observada.

## 5. Sensibilidad y umbral mínimo

Con `S>0`, `M>0` y margen igual, el punto de equilibrio es:

```text
Δp_BE = [Δc + (F + ΔO − ΔU)/S] / M
Δp_requerida = [Δc + (F + ΔO + B_reserva − ΔU)/S] / M
```

Igualar el umbral produce saldo cero o el colchón, respectivamente; recomendar inversión exige superarlo. Comprobar `0 ≤ p_B+Δp ≤ 1`; si `Δp_BE > 1−p_B`, el escenario no puede ser rentable por mejora de conversión solamente. `S=0` o `M≤0` impiden usar este umbral simplificado. El presupuesto incremental máximo soportable sin colchón es `S×(Δp×M−Δc)+ΔU`; un resultado negativo no financia el proyecto.

Ejemplo puramente algebraico con entradas base propuestas: con `S=500`, el equilibrio requiere `(50+16 000/500)/8 000 = 0,01025`, es decir **1,025 pp** de diferencia absoluta, antes del colchón. Con solo cinco plazas y los mismos costos, requiere **40,625 pp**. Estos umbrales no demuestran que se pueda alcanzar ninguno: muestran cuánto depende el caso del volumen y del costo. No se ha calculado un ROI ni una venta observada.

Análisis previsto, todavía sin ejecutar un modelo:

1. Variar una entrada manteniendo las demás en base: `Δp` en −2/0/+1/+2/+5 pp; `M` en 4 000/8 000/12 000; `Δc` en 25/50/100; `F` en 5 000/10 000/20 000; `ΔO` en 3 000/6 000/12 000; `J` en 1/10/100. Mostrar `ΔV`, umbral y supuesto responsable del cambio de decisión.
2. Cruzar `Δp × M` y `J × (F+ΔO)` para localizar regiones de pérdida/ganancia. Recalcular costos cuando escale `J`; no extender costos fijos a cualquier volumen por conveniencia.
3. Estresar activación tardía, bajas, impago, canibalización y costos comerciales, incluso conjuntamente. Al variar `H` (6/12 meses) o `d` (0/1/2% mensual), reconstruir `M` y costos desde sus flujos: no multiplicar un margen ya descontado sin justificación.
4. No tratar estos rangos como intervalos de confianza. La incertidumbre causal solo se estimará con el [experimento propuesto](15-incrementality-experiment.md). No se asignarán distribuciones ni se implementará Monte Carlo en esta fase.

**Regla de decisión propuesta:** un escenario favorable justifica como máximo evaluar un piloto presupuestado. Para recomendar despliegue, pedir evidencia experimental madura y que el límite inferior del intervalo de confianza del margen ITT por cuenta, transportado a una población/capacidad comparable, cubra costos incrementales y reserva. Con `τ_ITT` neto de costo comercial variable:

```text
N_despliegue × límite_inferior_95%(τ_ITT) − F_despliegue − ΔO_despliegue > B_reserva
```

No descontar dos veces `c_a`, ya incluido en el KPI ITT. Esta extrapolación exige misma mezcla, proporción de capacidad `S/N` y supuestos de costos válidos; fuera de ese soporte no se recomienda escalar. Un efecto incierto o datos incompletos no se convierten en aprobación. No hay base actual para afirmar que la inversión es rentable.

## 6. Decisiones pendientes y límite de esta entrega

| ID | Revisión requerida antes de programar o experimentar |
|---|---|
| ECO-01 | Aprobar o sustituir moneda, margen neto, costos incluidos, ventana de 90 días, horizonte de 12 meses y descuento de 1% mensual |
| ECO-02 | Aprobar o sustituir todas las entradas de escenarios, incluido `p_B`, `Δp`, `M`, `ΔU`, presupuestos `F/ΔO` y volumen hipotético `J=100`; aportar fuentes o mantener etiqueta de supuesto |
| ECO-03 | Aprobar población real y validaciones comerciales/legales previas; no confundir elegibilidad del ranking con permiso de contacto |
| ECO-04 | Aprobar unidad de aleatorización, capacidad por bolsa, protocolo de exposición e interferencia de `15-incrementality-experiment.md` |
| ECO-05 | Aprobar KPI, tratamiento de faltantes, potencia, nivel de confianza, regla de análisis y efecto mínimo relevante; obtener datos para calcular muestra |
| ECO-06 | Aprobar colchón propuesto del 20%, regla de inversión, presupuesto de piloto y condiciones para transportar el efecto a despliegue |

La aprobación puede ser parcial y debe quedar registrada por ID. Publicar este diseño en un PR borrador no aprueba ninguna fila. **La entrega termina aquí: no hay simulador financiero, eventos nuevos, cambios de ranking, lecturas del oráculo, operaciones Atlas ni modificaciones al ledger.**

## 7. Verificación documental

En Codex Cloud, Linux/Python 3.12.14: `uv sync --locked` correcto; `uv run pytest` con `RUN_MONGODB_INTEGRATION=0`: **160 aprobadas y 1 integración omitida**; `uv run ruff check .` y `uv run ruff format --check .` correctos. Se comprobaron enlaces locales y ausencia de cambios en código, pruebas, datos y dependencias. Las fórmulas y unidades se revisaron algebraicamente; no se programó ni ejecutó un modelo financiero. Estas verificaciones no validan los supuestos económicos, un experimento real ni Atlas.
