# Manifiesto de exportación pública

Este es un plan de copia limpia; no crea repositorios ni publica cambios.

## Incluir obligatoriamente

`README.md`, `pyproject.toml`, `uv.lock`, `.python-version`, `.env.example`, `src/`, `app/`, `scripts/`, `tests/`, `config/financial_assumptions.json`, `data/observable/observations.json`, `briefs/`, `case-studies/telcomx/`, `presentation-showcase/` y la documentación técnica enlazada desde el README.

## Incluir opcionalmente

Capturas, anexos y documentación técnica adicional, después de revisar rutas, nombres personales y procedencia.

## Mantener solo en privado

`.git/`, `AGENTS.md`, `.codex/`, `.env`, bitácoras de misiones, decisiones internas, referencias completas del reto original, PRs históricos, conversaciones y material bruto de TelcoMx.

## Requiere decisión del propietario

`design-data/`, documentación de Atlas, capturas históricas y archivos cuyo origen dependa de un entorno privado.

El script `scripts/export_public_portfolio.py` trabaja en modo simulación por defecto, rechaza sobrescribir una carpeta no vacía y nunca elimina archivos del repositorio fuente. La versión actual del brief es `briefs/conectapyme-executive-brief.pdf`, generada con `briefs/build_brief_pdf.py` desde el HTML editable: 3 páginas A4, 5,926 bytes, SHA-256 `fdbc6f83deb8d376534ab3080f25a585548a425193acd983d721353aafa679ac`.
