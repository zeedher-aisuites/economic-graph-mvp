# Comparación reproducible de rankings — misión 003A

Resultados de la política `003a-conservative-v1`, aprobada por el usuario, sobre datos sintéticos observables. Se calcularon offline en Codex Cloud; no proceden de una consulta real nueva a Atlas. Pesos, evidencia y límites: [diseño de rankings](12-commercial-ranking.md).

Reproducir desde la raíz del repositorio, también en Windows PowerShell:

```powershell
uv run python scripts/rank_companies.py --all-cuts --format markdown
```

La salida del comando reproduce las tres secciones siguientes. El formato JSON de la misma CLI permite inspeccionar IDs, contribuciones, fuentes, estados, fechas y notas. Los empates se resuelven por ID público: varias cuentas seleccionadas no tienen una ventaja comercial acreditada sobre otras empatadas. No se modificaron pesos para obtener estas selecciones.

## Corte 2026-01-15T12:00:00Z

Política `003a-conservative-v1`; capacidad **5**. Conocidas: 12; elegibles: 12; excluidas: 0; observaciones: 28.

- Top-5 baseline: Hornos del Centro, Comedor del Andén, Ruta Corta Mensajería, Papelería Horizonte, Ferretería Cinco Calles.
- Top-5 graph: Hornos del Centro, Papelería Horizonte, Café Jacaranda, Enlace Punto POS, Nodo Azul Soporte TI.
- Coincidencias: 2; entran con grafo: 3; salen: 3.
- Empate que atraviesa el límite: baseline sí, grafo no.

| Cuenta | Pos. baseline | Puntos baseline | Pos. grafo | Puntos grafo | Δ posición | Extra grafo | Selección |
|---|---:|---:|---:|---:|---:|---:|---|
| Hornos del Centro | 1 | 10 | 1 | 10 | +0 | 0 | Ambas |
| Comedor del Andén | 2 | 0 | 6 | 0 | -4 | 0 | Solo baseline |
| Ruta Corta Mensajería | 3 | 0 | 7 | 0 | -4 | 0 | Solo baseline |
| Papelería Horizonte | 4 | 0 | 2 | 5 | +2 | 5 | Ambas |
| Ferretería Cinco Calles | 5 | 0 | 8 | 0 | -3 | 0 | Solo baseline |
| Cobro Ágil Pagos | 6 | 0 | 9 | 0 | -3 | 0 | Ninguna |
| Bitácora Software | 7 | 0 | 10 | 0 | -3 | 0 | Ninguna |
| Café Jacaranda | 8 | 0 | 3 | 5 | +5 | 5 | Solo grafo |
| Enlace Punto POS | 9 | 0 | 4 | 5 | +5 | 5 | Solo grafo |
| La Espiga del Barrio | 10 | 0 | 11 | 0 | -1 | 0 | Ninguna |
| Brasa y Huerto | 11 | 0 | 12 | 0 | -1 | 0 | Ninguna |
| Nodo Azul Soporte TI | 12 | 0 | 5 | 5 | +7 | 5 | Solo grafo |

Δ positivo significa subir respecto al baseline. El desempate por ID no expresa prioridad comercial. Cero puntos no demuestra falta de potencial.

SHA-256 de las observaciones visibles: `7ec89be2b800bef4818828a767506ac52829f63c1cfc3c1ffe29bcf9ed778a49`.

Datos sintéticos observables; sin conversiones ni efecto económico medido.

## Corte 2026-05-15T12:00:00Z

Política `003a-conservative-v1`; capacidad **5**. Conocidas: 17; elegibles: 17; excluidas: 0; observaciones: 54.

- Top-5 baseline: Panificadora Valle Claro, Carga Urbana del Centro, Comedor del Andén, Mesa de Barrio, Ruta Corta Mensajería.
- Top-5 graph: Panificadora Valle Claro, Carga Urbana del Centro, Papelería Horizonte, Café Jacaranda, Enlace Punto POS.
- Coincidencias: 2; entran con grafo: 3; salen: 3.
- Empate que atraviesa el límite: baseline sí, grafo sí.

| Cuenta | Pos. baseline | Puntos baseline | Pos. grafo | Puntos grafo | Δ posición | Extra grafo | Selección |
|---|---:|---:|---:|---:|---:|---:|---|
| Panificadora Valle Claro | 1 | 50 | 1 | 50 | +0 | 0 | Ambas |
| Carga Urbana del Centro | 2 | 10 | 2 | 10 | +0 | 0 | Ambas |
| Comedor del Andén | 3 | 0 | 7 | 0 | -4 | 0 | Solo baseline |
| Mesa de Barrio | 4 | 0 | 8 | 0 | -4 | 0 | Solo baseline |
| Ruta Corta Mensajería | 5 | 0 | 9 | 0 | -4 | 0 | Solo baseline |
| Papelería Horizonte | 6 | 0 | 3 | 5 | +3 | 5 | Solo grafo |
| Ferretería Cinco Calles | 7 | 0 | 10 | 0 | -3 | 0 | Ninguna |
| Cobro Ágil Pagos | 8 | 0 | 11 | 0 | -3 | 0 | Ninguna |
| Bitácora Software | 9 | 0 | 12 | 0 | -3 | 0 | Ninguna |
| Café Jacaranda | 10 | 0 | 4 | 5 | +6 | 5 | Solo grafo |
| Enlace Punto POS | 11 | 0 | 5 | 5 | +6 | 5 | Solo grafo |
| La Espiga del Barrio | 12 | 0 | 13 | 0 | -1 | 0 | Ninguna |
| Mercado Verde Insumos | 13 | 0 | 14 | 0 | -1 | 0 | Ninguna |
| Hornos del Centro | 14 | 0 | 15 | 0 | -1 | 0 | Ninguna |
| Caja Vecina Digital | 15 | 0 | 16 | 0 | -1 | 0 | Ninguna |
| Brasa y Huerto | 16 | 0 | 17 | 0 | -1 | 0 | Ninguna |
| Nodo Azul Soporte TI | 17 | 0 | 6 | 5 | +11 | 5 | Ninguna |

Δ positivo significa subir respecto al baseline. El desempate por ID no expresa prioridad comercial. Cero puntos no demuestra falta de potencial.

SHA-256 de las observaciones visibles: `354fbeaf8072e91a6c9179d8c343727382d21d2629711e5ffafa7c9f21cc31a0`.

Datos sintéticos observables; sin conversiones ni efecto económico medido.

## Corte 2026-09-15T12:00:00Z

Política `003a-conservative-v1`; capacidad **5**. Conocidas: 23; elegibles: 21; excluidas: 2; observaciones: 83.

- Top-5 baseline: Panificadora Valle Claro, Carga Urbana del Centro, Comedor del Andén, Mesa de Barrio, Mapa Digital Studio.
- Top-5 graph: Panificadora Valle Claro, Carga Urbana del Centro, Café Jacaranda, Hornos del Centro, Papelería Horizonte.
- Coincidencias: 2; entran con grafo: 3; salen: 3.
- Empate que atraviesa el límite: baseline sí, grafo sí.

| Cuenta | Pos. baseline | Puntos baseline | Pos. grafo | Puntos grafo | Δ posición | Extra grafo | Selección |
|---|---:|---:|---:|---:|---:|---:|---|
| Panificadora Valle Claro | 1 | 50 | 1 | 50 | +0 | 0 | Ambas |
| Carga Urbana del Centro | 2 | 10 | 2 | 10 | +0 | 0 | Ambas |
| Comedor del Andén | 3 | 0 | 8 | 0 | -5 | 0 | Solo baseline |
| Mesa de Barrio | 4 | 0 | 9 | 0 | -5 | 0 | Solo baseline |
| Mapa Digital Studio | 5 | 0 | 10 | 0 | -5 | 0 | Solo baseline |
| Ruta Corta Mensajería | 6 | 0 | 11 | 0 | -5 | 0 | Ninguna |
| Papelería Horizonte | 7 | 0 | 5 | 5 | +2 | 5 | Solo grafo |
| Cobro Ágil Pagos | 8 | 0 | 12 | 0 | -4 | 0 | Ninguna |
| Bitácora Software | 9 | 0 | 13 | 0 | -4 | 0 | Ninguna |
| Café Jacaranda | 10 | 0 | 3 | 10 | +7 | 10 | Solo grafo |
| Moda Prisma Local | 11 | 0 | 14 | 0 | -3 | 0 | Ninguna |
| La Espiga del Barrio | 12 | 0 | 15 | 0 | -3 | 0 | Ninguna |
| Bici Centro Taller y Tienda | 13 | 0 | 16 | 0 | -3 | 0 | Ninguna |
| Mercado Verde Insumos | 14 | 0 | 6 | 5 | +8 | 5 | Ninguna |
| Taller de Datos Centro | 15 | 0 | 17 | 0 | -2 | 0 | Ninguna |
| Hornos del Centro | 16 | 0 | 4 | 10 | +12 | 10 | Solo grafo |
| Caja Vecina Digital | 17 | 0 | 18 | 0 | -1 | 0 | Ninguna |
| Brasa y Huerto | 18 | 0 | 19 | 0 | -1 | 0 | Ninguna |
| Nube Sencilla Sistemas | 19 | 0 | 20 | 0 | -1 | 0 | Ninguna |
| Saldo Claro Finanzas | 20 | 0 | 21 | 0 | -1 | 0 | Ninguna |
| Nodo Azul Soporte TI | 21 | 0 | 7 | 5 | +14 | 5 | Ninguna |

Δ positivo significa subir respecto al baseline. El desempate por ID no expresa prioridad comercial. Cero puntos no demuestra falta de potencial.

Excluidas por servicio activo confirmado: Ferretería Cinco Calles, Enlace Punto POS.

SHA-256 de las observaciones visibles: `eec342c3310480c788977e8382c7271dd0da24dc6a2d1b2e19ab1414dd5bb0ba`.

Datos sintéticos observables; sin conversiones ni efecto económico medido.
