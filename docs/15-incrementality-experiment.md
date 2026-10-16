# Experimento de incrementalidad — protocolo propuesto 003B

**Estado: diseño no aprobado ni ejecutado.** Complementa las variables y fórmulas de [caso económico](14-incremental-economic-case.md). No autoriza contactos reales, recolección de datos comerciales ni cambios a la política `003a-conservative-v1`.

## 1. Qué efecto queremos estimar

Hipótesis: sustituir la priorización baseline por su variante con grafo podría mejorar el margen neto bajo capacidad comparable. Se evalúa una **política de asignación de esfuerzo**, no el efecto de una arista ni de un punto de score. La diferencia de tres cuentas del top-5 no es un estimador de conversiones incrementales.

El control propuesto es el baseline aprobado de sucursales; el tratamiento usa exactamente ese baseline más vecinos económicos confirmados, con los pesos/topes y desempate vigentes. Ninguno representa una práctica comercial actual de Totalplay documentada. Si se quiere comparar con esa práctica, se necesitará otro diseño y aprobación, sin alterar silenciosamente 003A.

## 2. Población y asignación antes de seleccionar

Para un ensayo real se requieren PyMEs identificadas de forma suficiente, sin servicio activo, con cobertura/producto ofrecible y permisos de contacto. Son comprobaciones previas de operación real pendientes de aprobación, no cambios al ledger ni a la elegibilidad del ranking sintético. Las cuentas conocidas de estado desconocido no se convierten automáticamente en prospectos verificados. Resolver o retirar una identidad ambigua se hará antes de asignar, con evidencia autorizada; nunca por un resultado posterior.

Registrar todas las cuentas elegibles y su bolsa antes de aleatorizar, incluidos sus IDs, criterios, fuentes, fecha de disponibilidad y exclusiones previas. No partir los dos top-5 globales como si fueran brazos aleatorios: comparten cuentas y su selección depende de las señales.

**Unidad propuesta:** bolsa comercial indivisible —cartera/mercado y equipo responsable— construida para contener empresas conectadas y evitar que un vendedor opere ambos tratamientos. Una empresa pertenece a una sola bolsa y no se vuelve a inscribir como adquisición en otro corte. Emparejar bolsas por número de elegibles, sector, zona y capacidad cuando existan esos datos; aleatorizar bolsas completas 1:1 dentro de bloques, con probabilidades registradas. No se asignará tratamiento por score.

Todas las empresas de la bolsa reciben su asignación, aunque solo cinco ocupen plazas. Propuesta de capacidad: una ola de cinco plazas por bolsa en cada brazo, con el mismo presupuesto de esfuerzo, canales, producto, precios y ventana de contacto. La extensión de K=5 a múltiples bolsas reales está pendiente (ECO-04); no modifica el código. Equilibrar tamaños y la razón plazas/elegibles antes de asignar; una bolsa grande no se considerará equivalente a una pequeña por tener el mismo número de contactos.

Si una bolsa no tiene al menos cinco elegibles, resolver antes de aleatorizar mediante exclusión o bloques de capacidad menor común, con aprobación previa. No incorporar rellenos ajenos ni reciclar cuentas para cumplir una cuota. Los rechazos/no contactos posteriores no autorizan reemplazos discrecionales: la propuesta inicial congela el top-5 y registra esas desviaciones como parte del desempeño de la política.

## 3. Interferencia entre empresas y vendedores

Usar exclusivamente relaciones observables disponibles antes de asignar para diseñar las bolsas. Considerar también reportes, referencias y candidatos de identidad como **riesgo de contaminación**, sin convertirlos en señales de scoring ni resolverlos como hechos. No consultar la verdad del simulador para crear grupos aparentemente aislados.

- Medir antes de asignar la fracción de vínculos observables que cruzaría bolsas, solapamientos de cuentas y número/tamaño de unidades independientes. Definir el umbral aceptable con Comercial y evaluación, antes de observar efectos.
- Usar componentes o mercados ampliados cuando sea operativo; separar equipos y acceso a listas para limitar transferencia de recomendaciones. Registrar exposiciones cruzadas, referencias y cambios de responsable sin promover reportes a hechos confirmados.
- Si el grafo forma un componente grande o quedan pocas bolsas, no forzar un A/B por empresa. Rediseñar mercados/equipos o ampliar población autorizada; si no se logra independencia razonable, declarar el ensayo no viable para atribución causal bajo este protocolo.

La agrupación reduce contaminación conocida, no garantiza ausencia de vínculos ocultos. La inferencia propuesta supone interferencia contenida principalmente dentro de bolsa. Los spillovers internos forman parte del efecto de la política; los externos se reportan y pueden invalidar su interpretación. No se eliminarán retrospectivamente cuentas cruzadas para mejorar resultados.

## 4. Operación y horizonte propuestos

1. **Preinscripción:** fijar población, hipótesis, costos, versión de reglas, capacidad, bloques, semilla/método de aleatorización futuro, KPI, exclusiones previas, análisis y regla de decisión. Obtener autorizaciones y presupuesto. No se genera ninguna asignación en 003B.
2. **Corte de entrada:** congelar observaciones con `available_at <= asignación`, sus huellas y la política `003a-conservative-v1`. Aplicar a cada bolsa asignada la regla de su brazo, sin ajustar pesos al resultado. Cambiar el conjunto de candidatos de una bolsa no cambia la fórmula; su implementación operativa futura requerirá revisión. T0/T1/T2 solo reproducen conocimiento histórico ficticio y no determinan fechas del ensayo real.
3. **Ejecución humana:** misma oferta, canal, calendario y límite de esfuerzo; tratamiento recibe lista/explicación con grafo y control la del baseline. Evitar transferir listas entre equipos. Mantener seguimiento de intentos y cambios de ejecución, incluidos incumplimientos.
4. **Ventanas:** propuesta de 90 días desde asignación para activar el primer contrato de adquisición; margen y costos hasta doce meses desde esa misma asignación. No extender el seguimiento doce meses desde cada alta: premiaría activaciones tardías con más exposición. Anotar zona horaria y límites exactos en el protocolo aprobado.
5. **Cierre:** esperar madurez de seguimiento o un análisis intermedio preespecificado; no detener por significancia favorable. Un corte anticipado será descriptivo y no incluirá meses futuros como observados. Activaciones posteriores a los 90 días se analizan por separado, no se cambian ventanas después de ver resultados.

Las mismas condiciones operativas se aplican a ambos brazos; si hay uso desigual de capacidad o costos distintos, se registran y se incluyen, sin borrar cuentas de la asignación. La comparación es bajo el mismo límite de recursos, no una afirmación de ejecución idéntica.

## 5. KPI principal y análisis por intención de tratar

Para cada cuenta `i` originalmente elegible y asignada, definir:

```text
Y_i(H) = margen descontado del primer contrato activado antes de W,
         acumulado hasta H desde asignación
         − costo comercial variable asociado a esa cuenta durante el seguimiento

τ_ITT = E[Y_i | política con grafo asignada]
        − E[Y_i | baseline asignado]
```

Unidad del KPI: **MXN de contribución neta comercial por cuenta elegible asignada**. Instalación/comisión ya están descontadas del margen del contrato. Los costos compartidos de prospección se distribuyen con una regla fijada antes del ensayo, sin cambiar el total. `F` y `ΔO` de plataforma se evalúan después con la fórmula de inversión; no se deducen de `Y_i` y otra vez del resultado escalado.

El denominador incluye seleccionadas, no seleccionadas, no contactadas, rechazos, incumplimientos y cruces posteriores. No usar solo contactadas, cierres o usuarios que aceptaron la recomendación. Incluir las activaciones por otros canales dentro de la población, sin adjudicarlas manualmente al vendedor: así se captura desplazamiento/canibalización y efectos en no seleccionadas. Cero margen bruto exige comprobar ausencia de alta; una cuenta sin resultado verificable es faltante, no un cero. Puede haber `Y_i` negativo por costos sin alta o bajas.

La estimación debe ponderar por cuentas y respetar aleatorización por bolsas, evitando comparar promedios simples de bolsas de tamaños diferentes. Una opción propuesta y reproducible es el estimador de totales ponderados por probabilidad de asignación:

```text
N = total de cuentas elegibles inscritas; Z_j = 1 si bolsa j recibe grafo
T_j = suma de Y_i de todas las cuentas de bolsa j
π_j = probabilidad conocida de recibir grafo (propuesta: 1/2)

τ_estimado = (1/N) × Σ_j [ Z_j × T_j/π_j − (1−Z_j) × T_j/(1−π_j) ]
```

En términos simples, se comparan totales económicos de bolsas, ajustados por la probabilidad de recibir cada política, y se expresan por cuenta inscrita. El contraste y el intervalo se calculan respetando los bloques y la **bolsa como unidad independiente**, mediante inferencia de aleatorización o un método por clusters predefinido. No tratar empresas conectadas o cortes repetidos como observaciones independientes. Si no hay suficientes unidades, no se publicará una precisión estadística ficticia.

Registrar exposición y contaminación; el análisis principal conserva la asignación original. Un análisis por cumplimiento puede ser descriptivo secundario, sin sustituir ITT ni afirmar causalidad sin supuestos adicionales. Informar faltantes por brazo y hacer límites/sensibilidad bajo hipótesis declaradas; no excluir bajas, impagos o historias incómodas tras asignar.

## 6. Potencia, métricas secundarias y decisión

Propuestas pendientes: intervalo bilateral del 95%, potencia objetivo del 80% y tamaño muestral diseñado para superar el umbral económico, no solo para detectar un efecto distinto de cero. Se necesitan varianza del margen neto, correlación intrabolsa, distribución de tamaños, número de bolsas, ciclo de venta, faltantes y tasa de contaminación. Ninguno se conoce hoy; no se fija un número de empresas o duración total con falsa precisión.

Definir `τ_min=(F_despliegue+ΔO_despliegue+B_reserva)/N_despliegue` y una alternativa económicamente relevante `τ_objetivo>τ_min`; dimensionar el ensayo para distinguir esa brecha usando el diseño por bolsas. No basta un cálculo de conversión binaria que ignore la dispersión del margen. La PoC de treinta empresas ficticias y los tres cortes no proporcionan esa potencia.

Secundarios propuestos: activaciones por cuenta asignada, por plaza, contacto efectivo, tiempo a activación, permanencia, margen por contrato, costo comercial, concentración de selección y contaminación. Desgloses por sector/zona/tamaño de bolsa son exploratorios salvo preespecificación y muestra suficiente. El KPI de conversión por plaza permite contrastar el modelo financiero, pero no reemplaza el KPI ITT poblacional.

Aplicar la regla de inversión de `14-incremental-economic-case.md`, con costos cotizados y un intervalo válido. Resultado inconcluso implica no recomendar despliegue todavía; definir después si ampliar muestra es viable, sin presentar ausencia de significancia como equivalencia ni un escenario positivo como causalidad.

## 7. Datos y aprobaciones que faltan

Contrato de medición futuro: ID de cuenta y bolsa, asignación/probabilidad/bloque, corte y versión de política, posición/selección, exposición/intentos, primer contrato/activación, cobros/ajustes, servicio/baja, costos y fechas de disponibilidad. Conservar origen y auditoría; no registrar credenciales. Esta es una lista de requisitos, **no** una nueva colección, ledger o generador de eventos implementado.

ECO-03 a ECO-06 del caso económico requieren aprobación de población, operación, unidad de aleatorización, contaminación tolerable, ventanas, medición, tamaño muestral y regla de inversión. Las fuentes reales y sus permisos no existen como insumos autorizados de esta misión. Se publica únicamente este diseño; no se ejecuta ni se programa el ensayo o el simulador financiero.
