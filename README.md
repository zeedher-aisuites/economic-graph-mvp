# ConectaPyME

## Inteligencia económica para priorizar oportunidades B2B

ConectaPyME es una prueba de concepto de portafolio para una empresa de telecomunicaciones: combina un Economic Graph, datos sintéticos y reglas explicables para ayudar a un equipo comercial a decidir qué empresas investigar primero.

El proyecto nació como respuesta a un reto técnico de Totalplay, pero se presenta aquí como una solución autónoma y reproducible. No contiene datos de clientes ni resultados comerciales observados.

## ¿Qué problema aborda?

En una operación B2B, la información de empresas, sucursales, proveedores y relaciones económicas suele estar fragmentada. ConectaPyME organiza esas señales, conserva su procedencia y muestra cómo una regla de priorización puede cambiar el orden de investigación sin presentarlo como una probabilidad de compra.

Está pensado para Product Managers, líderes comerciales, analistas e ingenieros que necesitan conectar una decisión de negocio con evidencia verificable.

## Qué se construyó

- Ledger observable con un universo sintético de 30 empresas. En T2 se conocen 23 empresas y 21 son elegibles para la demostración; las 83 observaciones corresponden al ledger disponible en ese corte.
- Vista temporal T0/T1/T2, conflictos, fuentes e identidades candidatas.
- Ranking baseline frente a ranking con relaciones económicas confirmadas.
- Control Tower local en Streamlit con cinco vistas y modo offline.
- Caso económico reproducible con escenarios hipotéticos, sin afirmar ROI ni ventas.
- Presentación ejecutiva de 16 diapositivas principales y 14 anexos, con evidencias interactivas.

## Explorar inmediatamente

- [Brief ejecutivo](briefs/conectapyme-executive-brief.pdf) · [fuente editable](briefs/conectapyme-executive-brief.html)
- [Presentación ejecutiva](presentation-showcase/index.html) · [PDF de respaldo](presentation-showcase/ConectaPyME.pdf)
- [Caso consultivo TelcoMx](case-studies/telcomx/telcomx-case-study.pdf) · [fuente editable](case-studies/telcomx/telcomx-case-study.html)
- [Guía de la Control Tower](docs/18-control-tower-demo.md)
- [Arquitectura](docs/04-architecture-overview.md) · [reglas de ranking](docs/12-commercial-ranking.md) · [caso económico](docs/14-incremental-economic-case.md)

## Resultados demostrables y límites

La demo reproduce los cortes T0, T1 y T2, conserva la procedencia de las observaciones y explica las contribuciones del ranking. Las cinco plazas son una capacidad comercial ilustrativa, no el tamaño del universo. En el escenario financiero base, 5 plazas producen −$15,450 MXN y 500 plazas producen +$39,000 MXN antes de reserva; el escenario nulo de 500 plazas produce −$41,000 MXN. Son supuestos educativos, no ingresos observados.

La mejora de activación del 10% al 12% todavía tendría que validarse con un experimento comercial autorizado. No existe modelo entrenado, campaña, A/B test, despliegue productivo ni evidencia causal.

## Ejecutar offline en Windows

Requiere Python 3.12, Git y [uv](https://docs.astral.sh/uv/).

```powershell
uv sync --locked --group ui
uv run --group ui pytest -m "not integration"
uv run --group ui streamlit run app/control_tower.py
```

La Control Tower offline no requiere MongoDB ni credenciales. La conexión Atlas, si se habilita, es opcional y de solo lectura; nunca publiques un archivo `.env`.

## Arquitectura y metodología

Las consultas temporales viven en `src/economic_graph/observable.py`; el ranking en `src/economic_graph/rankings.py`; el cálculo económico en `src/economic_graph/finance.py`; y la adaptación de la interfaz en `app/control_tower.py`. Las pruebas offline están en `tests/` y los supuestos versionados en `config/financial_assumptions.json`.

El caso TelcoMx es un ejercicio consultivo ficticio independiente. Sus puntuaciones y diagnóstico no se mezclan con el ledger sintético de ConectaPyME.

## Uso de IA y autoría

La IA se utilizó como apoyo para explorar alternativas, revisar redacción y acelerar comprobaciones. Las decisiones de alcance, interpretación de resultados, límites de evidencia y revisión final corresponden al autor del proyecto.

Para conocer el inventario de la futura distribución pública, consulta la [auditoría de publicación](docs/release/publication-audit.md) y el [manifiesto de exportación](docs/release/public-export-manifest.md).
