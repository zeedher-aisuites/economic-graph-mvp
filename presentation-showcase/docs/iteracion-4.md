# Iteración 4 · ConectaPyME

Esta iteración simplifica la defensa sin duplicar la infraestructura de evidencias de la iteración 3.

- La diapositiva de organización del desarrollo comunica GitHub, Atlas offline y la revisión de pruebas en tres bloques.
- La diapositiva financiera prioriza costos, activaciones y la comparación de cinco y 500 plazas.
- Economic Impact incorpora el panel opcional `finance-story` con tres pasos: costos, resultado base y escenarios.
- Los siete paneles de la iteración 3 siguen en `evidence/iteration-3/` y no se modifican.

Los importes financieros se presentan como supuestos educativos reutilizando `financial_assumptions.json` y `finance-reproduced.json`. El resultado base de 500 plazas es `+$39,000 MXN` antes de reserva y el escenario nulo es `-$41,000 MXN`; no representan ventas observadas.

Validación final ejecutada: regeneración de materiales, prueba de regresión UTF-8 (`scripts/validate_encoding.py`), sintaxis Python y JavaScript, `git diff --check`, y prueba Playwright con dos ventanas. La prueba bidireccional cubrió apertura desde el presentador, navegación 1 → 2 → 3 y 3 → 2 → 1, actualización del speech, ausencia del speech en audiencia, cierre desde ambas ventanas, reapertura y ausencia de errores JavaScript. Los IDs comprobados conservaron los siete paneles originales y `finance-story`.

El PDF se regeneró desde este directorio con Playwright/Chromium, con 30 páginas y 16 diapositivas principales. Se verificó por extracción de texto que las páginas de organización y economía contienen los diseños de Misión 4. El renderizador Poppler no está instalado, por lo que la inspección visual se realizó mediante el PDF generado y su extracción de texto, no mediante PNGs de Poppler.
