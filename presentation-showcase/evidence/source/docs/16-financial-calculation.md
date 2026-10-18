# Resultados hipotéticos reproducibles — misión 003B

Entradas: [supuestos educativos](../config/financial_assumptions.json). Fórmulas, unidades, límites y aprobación provisional: [caso económico](14-incremental-economic-case.md). Estos cálculos son aritmética sobre supuestos no calibrados, sin acceso al ledger, al oráculo ni a Atlas. No se generan ventas por empresa ni resultados de las 30 PyMEs.

Reproducir desde la raíz, también en Windows PowerShell:

```powershell
uv run python scripts/calculate_finance.py --format markdown
uv run python scripts/calculate_finance.py --sensitivity
```

La primera orden reproduce el contenido siguiente; la segunda conserva matrices y trazabilidad en JSON. Las pérdidas y el nulo se muestran junto con los casos positivos. La referencia de saldo cero es el punto de equilibrio algebraico, no un resultado medido.

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

## Protocolo experimental futuro

Diseño 1:1 por bolsas independientes, KPI de margen neto comercial por cuenta elegible asignada, ITT, IC bilateral 95% y potencia objetivo 80%. Sin muestra calculada ni experimento ejecutado. Cinco o 500 plazas financieras no acreditan bolsas suficientes para inferencia causal.

Versión: `003b-finance-v1`; SHA-256 de supuestos: `f37dc44da51250b1a065bff79637d9cbe2c54440804136ce895f6beac274a4a1`.
