# Caso económico incremental — misión 003B

**Estado: ECO-01 a ECO-06 aprobadas provisionalmente y exclusivamente como metodología para la PoC educativa**, por respuesta explícita del usuario al PR #5. Calculador determinista `003b-finance-v1` implementado; supuestos no calibrados y resultados solo hipotéticos. La aprobación no valida finanzas de Totalplay, acceso a datos reales, contactos, presupuesto, piloto operativo ni despliegue. El experimento sigue siendo diseño futuro, no ejecutado.

## 1. Auditoría y pregunta de inversión

Base: `main` en `0e1088c233f4b49eaf22deab8161d6d610748656`, con el PR #4 integrado, incluida su corrección de portabilidad. Se revisaron las 13 diapositivas y notas del [reto original](../presentations/references/Reto-AI-Engineering-SME-Economic-Graph.pptx), la [trazabilidad](02-challenge-traceability.md), el alcance, DEC-004/009 y los [rankings aprobados](12-commercial-ranking.md).

Las diapositivas 4, 5 y 8 exigen conectar la señal con decisión e impacto; la 10 pide margen, CAC, LTV, ROI y payback dentro de la Control Tower; la 12 exige caso económico y brief final. Estas son métricas que debemos justificar según los datos disponibles, no resultados existentes. El score 87 de la diapositiva 8 y el funnel de la 11 son ilustraciones del reto, no parámetros financieros de esta PoC.

La pregunta es: **a igual capacidad comercial, ¿el margen adicional generado por cambiar la priorización cubre los costos incrementales de construir y operar el grafo?** La comparación se refiere a las dos reglas aprobadas, no a una política actual de Totalplay observada. La revisión posterior del usuario aprueba provisionalmente la metodología de DEC-004/010 para uso educativo; su aplicación operativa no está autorizada.

| Categoría | Evidencia disponible | Qué permite concluir |
|---|---|---|
| Observación técnica real reportada por el usuario | Ping, carga idempotente y consultas Atlas desde Windows; [002C](11-atlas-integration-validation.md) | Funcionamiento técnico local reportado; sin ventas ni costos medidos |
| Datos y resultados sintéticos reproducidos offline | Ledger público de 83 observaciones; conocidas 12/17/23; elegibles 12/17/21; K=5; dos seleccionadas en común y tres sustituciones por corte | Cambian las selecciones; no se deriva una tasa de conversión de esos cambios |
| Supuestos financieros propuestos | Conversiones esperadas, márgenes, costos, volumen y horizonte de las secciones siguientes | Explorar condiciones de rentabilidad; no describir desempeño observado |
| Resultados medibles solo con datos comerciales autorizados y experimento | Activaciones, margen por cuenta asignada, costos y efecto con incertidumbre | Estimar incrementalidad bajo el protocolo y sus limitaciones |

Se auditó únicamente el ledger observable: sus atributos son nombre, sector, tamaño, sucursales, calificación, reseñas, servicio activo, afirmaciones relacionales y alias. No hay conversiones, precios, facturación, costos ni eventos comerciales. **Desconocido no significa cero ventas.** No se consultó el oráculo para proponer resultados económicos.

Las reglas `003a-conservative-v1`, sus pesos, elegibilidad, desempate y capacidad de cinco cuentas permanecen intactos. T0/T1/T2 son instantáneas superpuestas: no son tres cohortes independientes, quince clientes contactados ni tres brazos experimentales.

## 2. Variables y datos que faltan

Unidad monetaria de la PoC: MXN nominales, sin IVA recuperable, antes de financiamiento e impuesto sobre la renta; cualquier uso real requeriría confirmar el criterio con Finanzas. Cada entrada conserva unidad, base de valoración, período y condición de supuesto. El archivo versionado fija su origen educativo y su SHA-256 permite reproducir la configuración.

| Variable | Definición y unidad | Estado y fuente futura requerida |
|---|---|---|
| `K` | Capacidad por bolsa comercial y corte: cinco cuentas | Aprobada para 003A y conceptualmente para el futuro diseño por bolsas; sin operación real autorizada |
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
| `W`, `H`, `d` | Ventana de activación, horizonte desde asignación y descuento mensual | 90 días, 12 meses y 1% mensual; aprobados solo para PoC, configurables y no calibrados |
| `B_reserva` | Colchón de inversión adicional al punto de equilibrio | 20% de `F+ΔO`, aceptación provisional educativa; no autoriza presupuesto |

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

## 4. Escenarios aprobados solo como ejercicios hipotéticos

**Todos los números económicos de esta tabla son supuestos pedagógicos aprobados provisionalmente, sin cotización ni evidencia de mercado.** No son datos observados de Totalplay, metas operativas, pronósticos calibrados ni salidas del ranking. No se asignan probabilidades a los escenarios. Sus entradas están en [configuración reproducible](../config/financial_assumptions.json).

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

El volumen de 100 bolsas es una hipótesis educativa, no autorización de despliegue ni evidencia de que existan 500 oportunidades. El calculador separa `demo` (`J=1`, cinco plazas) de `hypothetical` (`J=100`, 500 plazas); ningún modo lee empresas ni cambia la capacidad del ranking. El protocolo A/B futuro constituye un tercer nivel, separado de ambos volúmenes financieros. No se suman T0/T1/T2 ni se reutiliza una cuenta como adquisición nueva.

Se incluye obligatoriamente el escenario **nulo**: `Δp=0`, `ΔU=0`, con los costos del caso base, derivado automáticamente para que no se pueda omitir al elegir escenarios. Un nulo de conversión no equivale a saldo cero: con las entradas aprobadas pierde dinero. La referencia de saldo cero se muestra aparte como el punto de equilibrio algebraico. No se generan ventas ni conversiones por empresa.

## 5. Sensibilidad y umbral mínimo

Con `S>0`, `M>0` y margen igual, el punto de equilibrio es:

```text
Δp_BE = [Δc + (F + ΔO − ΔU)/S] / M
Δp_requerida = [Δc + (F + ΔO + B_reserva − ΔU)/S] / M
```

Igualar el umbral produce saldo cero o el colchón, respectivamente; recomendar inversión exige superarlo. Comprobar `0 ≤ p_B+Δp ≤ 1`; si `Δp_BE > 1−p_B`, el escenario no puede ser rentable por mejora de conversión solamente. `S=0` o `M≤0` impiden usar este umbral simplificado. El presupuesto incremental máximo soportable sin colchón es `S×(Δp×M−Δc)+ΔU`; un resultado negativo no financia el proyecto.

Ejemplo puramente algebraico con entradas base propuestas: con `S=500`, el equilibrio requiere `(50+16 000/500)/8 000 = 0,01025`, es decir **1,025 pp** de diferencia absoluta, antes del colchón. Con solo cinco plazas y los mismos costos, requiere **40,625 pp**. Estos umbrales no demuestran que se pueda alcanzar ninguno: muestran cuánto depende el caso del volumen y del costo. No se ha calculado un ROI ni una venta observada.

Análisis implementado mediante `--sensitivity`:

1. Variar una entrada manteniendo las demás en base: `Δp` en −2/0/+1/+2/+5 pp; `M` en 4 000/8 000/12 000; `Δc` en 25/50/100; `F` en 5 000/10 000/20 000; `ΔO` en 3 000/6 000/12 000; `J` en 1/10/100; `ΔU` en −1 000/0/+1 000; reserva en 0/20/50%. Son 26 variaciones por modo, siempre etiquetadas exploratorias. No sustituyen los valores aprobados predeterminados.
2. Cruzar `Δp × M` (15 celdas) y `J × (F+ΔO)` (9 celdas, con costos base multiplicados por 0,5/1/2). Las tasas inviables se señalan, no se omiten silenciosamente. Los costos constantes al variar volumen aíslan su efecto matemático; no son cotizaciones a escala ni evidencia de economías reales.
3. Activación tardía, bajas e impago requerirían entradas de flujos agregados o nuevas valoraciones explícitas; no se inventan trayectorias. Al variar `H` o `d`, la CLI rechaza valores presentes etiquetados con otro horizonte/descuento. Los flujos mensuales proporcionados por el usuario se revaloran según la configuración. No hay una matriz temporal automática sin esos insumos.
4. No tratar estos rangos como intervalos de confianza. La incertidumbre causal solo se estimará con el [experimento propuesto](15-incrementality-experiment.md). No se asignarán distribuciones ni se implementará Monte Carlo en esta fase.

**Regla metodológica aprobada provisionalmente:** un escenario favorable no autoriza financiar un piloto ni desplegar. Una decisión real exigiría aprobación operativa adicional, evidencia experimental válida y que el límite inferior del intervalo de confianza del margen ITT por cuenta, transportado a una población/capacidad comparable, cubra costos incrementales y reserva. Con `τ_ITT` neto de costo comercial variable:

```text
N_despliegue × límite_inferior_95%(τ_ITT) − F_despliegue − ΔO_despliegue > B_reserva
```

No descontar dos veces `c_a`, ya incluido en el KPI ITT. Esta extrapolación exige misma mezcla, proporción de capacidad `S/N` y supuestos de costos válidos; fuera de ese soporte no se recomienda escalar. Un efecto incierto o datos incompletos no se convierten en aprobación. No hay base actual para afirmar que la inversión es rentable.

## 6. Registro de aprobación provisional y límites

| ID | Aprobación explícita del usuario, limitada a metodología PoC |
|---|---|
| ECO-01 | MXN nominales, 90 días, 12 meses y descuento mensual del 1%; configurables como supuestos no calibrados |
| ECO-02 | Tres escenarios financieros como hipótesis, con nulo obligatorio; ningún importe o conversión es un dato observado de Totalplay |
| ECO-03 | Población conceptual sujeta a cobertura, identidad, ausencia de servicio activo, autorización de contacto y validaciones comerciales/legales; sin datos reales ni contactos autorizados |
| ECO-04 | Diseño futuro 1:1 por bolsas independientes y capacidad comparable de cinco plazas; inferencia causal inviable si faltan unidades independientes suficientes |
| ECO-05 | KPI de margen neto comercial por cuenta elegible asignada, ITT, IC bilateral 95% y potencia objetivo 80%; muestra sin determinar hasta disponer de varianza, ICC y datos comerciales |
| ECO-06 | Reserva provisional del 20% de costos fijos/operativos; inversión exige evidencia experimental válida y rentabilidad suficiente. Sin presupuesto real, piloto operativo ni despliegue autorizados |

La fuente es la respuesta del usuario tras revisar el PR #5, no una aprobación inferida por publicar el PR. Se autorizó únicamente un calculador financiero determinista con escenarios, sensibilidad y equilibrio. No se ejecuta el experimento, calcula muestra, genera ventas por empresa, accede a datos reales, modifica rankings/ledger ni opera Atlas.

## 7. Uso y contrato del calculador

La CLI y sus comandos PowerShell están en el [README](../README.md). [`finance.py`](../src/economic_graph/finance.py) es cálculo puro con biblioteca estándar; [`calculate_finance.py`](../scripts/calculate_finance.py) solo lee el JSON de supuestos y emite UTF-8. No necesita `.env`, PyMongo, Atlas, catálogo, ledger ni oráculo. No utiliza aleatoriedad. El JSON versiona entradas y resultados y devuelve una huella SHA-256; los importes se serializan como cadenas decimales con precisión interna de 50 cifras. Las tasas son fracciones: `0.02` significa dos puntos porcentuales absolutos para `Δp`, no 2% relativo.

Contrato en `config/financial_assumptions.json`:

- `settings`: MXN, capacidad fija cinco, ventana, horizonte, descuento mensual y reserva. Ventana/horizonte/tasas son configurables sin convertirlos en datos calibrados. La ventana de cada escenario debe coincidir con la de sus supuestos de tasas/margen; no se infieren fechas ni ventas.
- Tres escenarios obligatorios, con márgenes netos de servicio/instalación/comisión y prospección separada. El nulo se deriva de base manteniendo sus costos, con `Δp=ΔU=0`.
- Cada importe declara `unit`: `MXN_per_activation`, `MXN_per_slot` o `MXN_total`. No se admiten importes flotantes JSON, porcentajes con `%`, probabilidades fuera de rango ni valores no finitos.
- Base `present_value`: `value` decimal, `horizon_months` y `monthly_discount_rate` compatibles con settings. No se vuelve a descontar. Cambiar solo la cabecera H/d se rechaza: hacen falta importes revalorados y etiquetados explícitamente.
- Base `monthly_cashflows`: `values` contiene exactamente H+1 cadenas, del mes 0 al H, con la misma unidad; el calculador suma `flujo_m/(1+d)^m`. Son flujos agregados aportados, no eventos de empresas generados. Al cambiar H deben cambiar las longitudes; no se truncan meses silenciosamente. Los valores de margen siguen condicionados a la ventana declarada.
- `costs` contiene categorías `fixed` y `operating`, con importes totales explícitos, incluso cero, y `cost_id` único por escenario. Se rechazan IDs repetidos, claves JSON duplicadas y categorías que reintroduzcan prospección/comisión. La identificación semántica de una misma factura con IDs diferentes todavía requiere revisión humana: la validación de contrato no audita facturas reales.

La salida separa componentes del saldo neto, reserva y saldo tras reserva. `clears_reserve_mathematically` es solo una desigualdad aritmética; `operational_authorization` siempre es falso. La reserva no se descuenta del saldo neto dos veces ni equivale a gasto realizado. Los umbrales no se recortan a probabilidades viables: se informa cuando son inalcanzables; con margen no positivo no se define un umbral de mejora de conversión.

La [tabla reproducida](16-financial-calculation.md) muestra pérdidas, ganancias hipotéticas y el punto de saldo nulo. El nulo de conversión puede perder dinero por los costos. No hay ROI, payback, LTV, etiquetas de entrenamiento ni intervalos de confianza calculados. El IC/potencia del reporte identifican exclusivamente el protocolo futuro; no son resultados estadísticos.

## 8. Verificación

La fase documental inicial pasó 160 pruebas existentes. La implementación añade 73 pruebas de identidades contables, regresiones numéricas, saldo cero, reserva estricta, costos compartidos, duplicados, unidades, probabilidades, ventanas, valoración temporal, sensibilidad, precisión y aislamiento de I/O. La CLI se prueba con solo su módulo público y supuestos, rutas con espacios/acentos y tuberías cp1252/UTF-8.

Comprobaciones ejecutadas en Codex Cloud, Linux/Python 3.12.14:

| Comando | Resultado |
|---|---|
| `uv sync --locked` | Correcto; dependencias sin cambios |
| `uv run pytest` | 233 aprobadas, 1 integración omitida; proceso con `RUN_MONGODB_INTEGRATION=0` |
| `uv run pytest -m "not integration"` | 233 aprobadas, 1 integración excluida |
| `uv run ruff check .` | Correcto |
| `uv run ruff format --check .` | Correcto |
| `uv run python scripts/calculate_finance.py --format markdown` | Tabla de cinco/500 plazas reproducida en `16-financial-calculation.md` |

Las comprobaciones no validan finanzas reales, un experimento, Atlas ni ejecución nativa de Windows. La regresión de codificación reproduce tuberías cp1252 en Linux. Rankings, ledger y componentes MongoDB permanecen intactos.
