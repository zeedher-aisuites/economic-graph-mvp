# Calculador financiero educativo — 003B

Ejercicio hipotético no calibrado, exclusivamente para la PoC educativa. No representa datos observados de Totalplay ni de las 30 PyMEs. Un saldo positivo no valida causalidad ni autoriza inversión, contactos, piloto o despliegue.

Moneda: MXN nominales; ventana: 90 días; H: 12 meses; descuento mensual: 1.00%. Todos los importes están en valor presente a la asignación.

## Demostración: cinco plazas

| Escenario | Δ conversión (pp) | Δ margen seleccionado | Δ costo comercial | Δ margen resto | F + O | Saldo neto | Reserva | Saldo tras reserva | Equilibrio (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Conservador | -2.00 | -400.00 | 500.00 | -1000.00 | 32000.00 | -33900.00 | 6400.00 | -40300.00 | 167.500000 (inviable) |
| Base | 2.00 | 800.00 | 250.00 | 0.00 | 16000.00 | -15450.00 | 3200.00 | -18650.00 | 40.625000 |
| Optimista | 5.00 | 3000.00 | 125.00 | 0.00 | 8000.00 | -5125.00 | 1600.00 | -6725.00 | 13.541667 |
| Nulo | 0 | 0.00 | 250.00 | 0.00 | 16000.00 | -16250.00 | 3200.00 | -19450.00 | 40.625000 |

Referencia base de saldo nulo: ΔV = 0 por definición en Δp = 40.62500 pp; no es conversión observada.

## Escenario hipotético: 500 plazas

| Escenario | Δ conversión (pp) | Δ margen seleccionado | Δ costo comercial | Δ margen resto | F + O | Saldo neto | Reserva | Saldo tras reserva | Equilibrio (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Conservador | -2.00 | -40000.00 | 50000.00 | -1000.00 | 32000.00 | -123000.00 | 6400.00 | -129400.00 | 4.150000 |
| Base | 2.00 | 80000.00 | 25000.00 | 0.00 | 16000.00 | 39000.00 | 3200.00 | 35800.00 | 1.025000 |
| Optimista | 5.00 | 300000.00 | 12500.00 | 0.00 | 8000.00 | 279500.00 | 1600.00 | 277900.00 | 0.341667 |
| Nulo | 0 | 0.00 | 25000.00 | 0.00 | 16000.00 | -41000.00 | 3200.00 | -44200.00 | 1.025000 |

Referencia base de saldo nulo: ΔV = 0 por definición en Δp = 1.02500 pp; no es conversión observada.

El escenario nulo tiene Δp=0 y ΔU=0, conserva los costos base y puede perder dinero. La reserva es un colchón, no un gasto adicional del saldo neto. Los importes de tabla se redondean a centavos; JSON conserva más precisión.

## Sensibilidad base — demo

Rangos exploratorios, no intervalos de confianza. Al variar volumen, costos constantes solo aíslan su efecto; no son cotizaciones a escala. H y descuento requieren revalorar los importes o aportar flujos mensuales compatibles.

| Parámetro | Valor | Plazas | Saldo neto MXN | Saldo tras reserva MXN |
|---|---:|---:|---:|---:|
| activation_rate_increment | -0.02 | 5 | -17050.00 | -20250.00 |
| activation_rate_increment | 0 | 5 | -16250.00 | -19450.00 |
| activation_rate_increment | 0.01 | 5 | -15850.00 | -19050.00 |
| activation_rate_increment | 0.02 | 5 | -15450.00 | -18650.00 |
| activation_rate_increment | 0.05 | 5 | -14250.00 | -17450.00 |
| contract_margin_per_activation | 4000 | 5 | -15850.00 | -19050.00 |
| contract_margin_per_activation | 8000 | 5 | -15450.00 | -18650.00 |
| contract_margin_per_activation | 12000 | 5 | -15050.00 | -18250.00 |
| incremental_commercial_cost_per_slot | 25 | 5 | -15325.00 | -18525.00 |
| incremental_commercial_cost_per_slot | 50 | 5 | -15450.00 | -18650.00 |
| incremental_commercial_cost_per_slot | 100 | 5 | -15700.00 | -18900.00 |
| fixed_incremental_cost | 5000 | 5 | -10450.00 | -12650.00 |
| fixed_incremental_cost | 10000 | 5 | -15450.00 | -18650.00 |
| fixed_incremental_cost | 20000 | 5 | -25450.00 | -30650.00 |
| operating_incremental_cost | 3000 | 5 | -12450.00 | -15050.00 |
| operating_incremental_cost | 6000 | 5 | -15450.00 | -18650.00 |
| operating_incremental_cost | 12000 | 5 | -21450.00 | -25850.00 |
| unselected_margin_increment | -1000 | 5 | -16450.00 | -19650.00 |
| unselected_margin_increment | 0 | 5 | -15450.00 | -18650.00 |
| unselected_margin_increment | 1000 | 5 | -14450.00 | -17650.00 |
| reserve_rate | 0 | 5 | -15450.00 | -15450.00 |
| reserve_rate | 0.20 | 5 | -15450.00 | -18650.00 |
| reserve_rate | 0.50 | 5 | -15450.00 | -23450.00 |
| pools | 1 | 5 | -15450.00 | -18650.00 |
| pools | 10 | 50 | -10500.00 | -13700.00 |
| pools | 100 | 500 | 39000.00 | 35800.00 |

Los cruces Δp × margen y volumen × costos están en la salida JSON.

## Sensibilidad base — hypothetical

Rangos exploratorios, no intervalos de confianza. Al variar volumen, costos constantes solo aíslan su efecto; no son cotizaciones a escala. H y descuento requieren revalorar los importes o aportar flujos mensuales compatibles.

| Parámetro | Valor | Plazas | Saldo neto MXN | Saldo tras reserva MXN |
|---|---:|---:|---:|---:|
| activation_rate_increment | -0.02 | 500 | -121000.00 | -124200.00 |
| activation_rate_increment | 0 | 500 | -41000.00 | -44200.00 |
| activation_rate_increment | 0.01 | 500 | -1000.00 | -4200.00 |
| activation_rate_increment | 0.02 | 500 | 39000.00 | 35800.00 |
| activation_rate_increment | 0.05 | 500 | 159000.00 | 155800.00 |
| contract_margin_per_activation | 4000 | 500 | -1000.00 | -4200.00 |
| contract_margin_per_activation | 8000 | 500 | 39000.00 | 35800.00 |
| contract_margin_per_activation | 12000 | 500 | 79000.00 | 75800.00 |
| incremental_commercial_cost_per_slot | 25 | 500 | 51500.00 | 48300.00 |
| incremental_commercial_cost_per_slot | 50 | 500 | 39000.00 | 35800.00 |
| incremental_commercial_cost_per_slot | 100 | 500 | 14000.00 | 10800.00 |
| fixed_incremental_cost | 5000 | 500 | 44000.00 | 41800.00 |
| fixed_incremental_cost | 10000 | 500 | 39000.00 | 35800.00 |
| fixed_incremental_cost | 20000 | 500 | 29000.00 | 23800.00 |
| operating_incremental_cost | 3000 | 500 | 42000.00 | 39400.00 |
| operating_incremental_cost | 6000 | 500 | 39000.00 | 35800.00 |
| operating_incremental_cost | 12000 | 500 | 33000.00 | 28600.00 |
| unselected_margin_increment | -1000 | 500 | 38000.00 | 34800.00 |
| unselected_margin_increment | 0 | 500 | 39000.00 | 35800.00 |
| unselected_margin_increment | 1000 | 500 | 40000.00 | 36800.00 |
| reserve_rate | 0 | 500 | 39000.00 | 39000.00 |
| reserve_rate | 0.20 | 500 | 39000.00 | 35800.00 |
| reserve_rate | 0.50 | 500 | 39000.00 | 31000.00 |
| pools | 1 | 5 | -15450.00 | -18650.00 |
| pools | 10 | 50 | -10500.00 | -13700.00 |
| pools | 100 | 500 | 39000.00 | 35800.00 |

Los cruces Δp × margen y volumen × costos están en la salida JSON.

## Protocolo experimental futuro

Diseño 1:1 por bolsas independientes, KPI de margen neto comercial por cuenta elegible asignada, ITT, IC bilateral 95% y potencia objetivo 80%. Sin muestra calculada ni experimento ejecutado. Cinco o 500 plazas financieras no acreditan bolsas suficientes para inferencia causal.

Versión: `003b-finance-v1`; SHA-256 de supuestos: `f37dc44da51250b1a065bff79637d9cbe2c54440804136ce895f6beac274a4a1`.
