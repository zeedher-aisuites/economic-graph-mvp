# ruff: noqa: E501
"""Capturas auténticas de Streamlit mediante Chromium; no genera interfaces simuladas."""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "presentation-showcase/evidence"


def main():
    manifest, errors = [], []
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
            args=["--no-sandbox"],
        )
        page = browser.new_page(viewport={"width": 1600, "height": 1050}, device_scale_factor=1)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto("http://127.0.0.1:8501")
        page.get_by_text("Empresas conocidas · global", exact=True).wait_for(timeout=60000)

        def stable():
            page.wait_for_timeout(1300)
            assert page.locator('[data-testid="stException"]').count() == 0

        def view(name):
            page.get_by_text(name, exact=True).first.click()
            stable()

        def choose(label, name):
            combo = page.get_by_role("combobox", name=label, exact=True)
            combo.click()
            page.get_by_role("option", name=name, exact=True).click()
            stable()

        def panel(name, expanded=True):
            target = page.get_by_text(name, exact=True)
            current = target.evaluate("e => e.closest('details')?.open")
            if current != expanded:
                target.click()
                stable()

        def capture(
            filename,
            screen,
            demonstrates,
            cut="T2",
            params=None,
            source="app/control_tower.py",
            limitations="Datos sintéticos; no acredita resultados de negocio ni integración Atlas.",
        ):
            stable()
            main = page.locator('[data-testid="stMainBlockContainer"]')
            main.screenshot(path=str(OUT / "screenshots" / filename))
            page.screenshot(
                path=str(OUT / "screenshots" / filename.replace(".png", "-viewport.png"))
            )
            text = page.locator("body").inner_text()
            (OUT / "results" / filename.replace(".png", ".txt")).write_text(text, encoding="utf-8")
            manifest.append(
                {
                    "id": filename[:-4],
                    "file": "screenshots/" + filename,
                    "screen": screen,
                    "demonstrates": demonstrates,
                    "captured_at": datetime.now(ZoneInfo("America/Mexico_City")).isoformat(),
                    "source_commit": commit,
                    "mode": "offline",
                    "cut": cut,
                    "parameters": params or {},
                    "source": source,
                    "limitations": limitations,
                    "browser": browser.version,
                    "viewport": "1600×1050",
                    "authentic": True,
                }
            )
            (OUT / "screenshots/manifest.json").write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            print(filename, flush=True)

        capture(
            "01-resumen-t2.png",
            "Resumen",
            "23 conocidas, 21 elegibles, tres sustituciones y escenarios etiquetados.",
        )
        view("Graph Health")
        page.get_by_text("Red económica al corte", exact=True).wait_for()
        capture(
            "02-graph-cafe.png",
            "Graph Health",
            "Red focal de Café Jacaranda con dos vínculos confirmados.",
            params={"company": "Café Jacaranda", "network": "Empresa y vecinos"},
        )
        panel("Ficha de cuenta y respaldo completo")
        page.get_by_text("Posición grafo global", exact=True).wait_for()
        capture(
            "03-graph-ficha.png",
            "Graph Health · ficha",
            "Posiciones globales #10 → #3, puntos y respaldo de la cuenta.",
            params={"company": "Café Jacaranda", "expanded": "Ficha de cuenta y respaldo completo"},
        )
        panel("Ficha de cuenta y respaldo completo", False)
        page.get_by_text("Red completa del segmento", exact=True).click()
        stable()
        capture(
            "04-graph-completa.png",
            "Graph Health · red completa",
            "Red observable completa; no usa la verdad privada.",
            params={"network": "Red completa del segmento"},
        )
        choose("Período", "T0")
        panel("Evolución global al corte")
        capture(
            "05-graph-t0.png",
            "Graph Health · T0",
            "28 observaciones y evolución sin cortes futuros.",
            cut="T0",
            params={
                "network": "Red completa del segmento",
                "expanded": "Evolución global al corte",
            },
        )
        choose("Período", "T1")
        capture(
            "06-graph-t1.png",
            "Graph Health · T1",
            "54 observaciones y 17 empresas conocidas.",
            cut="T1",
            params={
                "network": "Red completa del segmento",
                "expanded": "Evolución global al corte",
            },
        )
        choose("Período", "T2")
        view("AI Performance")
        capture(
            "07-ai-global.png",
            "AI Performance · global",
            "Dos rankings y tres sustituciones bajo K=5.",
        )
        panel("Auditar ranking, empates y filtros de score")
        capture(
            "08-ranking-global.png",
            "AI Performance · tabla global",
            "Ranking completo antes de filtrar.",
            params={"industry": "Todas", "company": "Todas", "score_minimum": 0},
        )
        summary = json.loads((OUT / "results/global-ranking-demo.json").read_text())
        choose("Industria", summary["industry"])
        panel("Auditar ranking, empates y filtros de score")
        capture(
            "09-ranking-industria.png",
            "AI Performance · industria",
            "Café Jacaranda conserva #10 → #3 al filtrar industria.",
            params={"industry": summary["industry"], "company": "Todas", "score_minimum": 0},
        )
        choose("Empresa", "Café Jacaranda")
        panel("Auditar ranking, empates y filtros de score")
        page.get_by_text("Posición grafo global", exact=True).wait_for()
        capture(
            "10-ranking-cafe.png",
            "AI Performance · empresa",
            "Una sola empresa visible conserva posición global 3.",
            params={
                "industry": summary["industry"],
                "company": "Café Jacaranda",
                "score_minimum": 0,
            },
        )
        number = page.get_by_role("spinbutton", name="Score mínimo · solo tabla")
        number.fill("11")
        number.press("Enter")
        stable()
        capture(
            "11-ranking-score.png",
            "AI Performance · score",
            "El filtro de tabla oculta la fila sin recalcular la ficha global.",
            params={
                "industry": summary["industry"],
                "company": "Café Jacaranda",
                "score_minimum": 11,
            },
        )
        view("Business Funnel")
        page.get_by_role("button", name="Mostrar todas las empresas", exact=True).click()
        stable()
        capture(
            "12-business-funnel.png",
            "Business Funnel",
            "23 → 21 → 5; dos exclusiones aparte y ventas no observadas.",
            params={"policy": "graph", "industry": "Todas", "company": "Todas"},
        )
        choose("Política mostrada", "Baseline")
        capture(
            "13-business-baseline.png",
            "Business Funnel · baseline",
            "Cambiar política no inventa contactos ni ventas.",
            params={"policy": "baseline", "industry": "Todas", "company": "Todas"},
        )
        view("Economic Impact")
        capture(
            "14-economic-five.png",
            "Economic Impact · cinco plazas",
            "Cuatro escenarios, incluido caso base negativo a cinco plazas.",
            cut="Independiente",
            params={"scope": "demo"},
        )
        page.get_by_text("Escenario hipotético · 500 plazas", exact=True).click()
        stable()
        capture(
            "15-economic-500.png",
            "Economic Impact · 500 plazas",
            "+39,000 base frente a −41,000 nulo; hipótesis, no ventas.",
            cut="Independiente",
            params={"scope": "hypothetical"},
        )
        panel("Explorar sensibilidad · sin editar supuestos")
        choose("Variable explorada", "contract_margin_per_activation")
        capture(
            "16-economic-sensitivity.png",
            "Economic Impact · sensibilidad",
            "Exploración sin modificar los supuestos originales.",
            cut="Independiente",
            params={"scope": "hypothetical", "parameter": "contract_margin_per_activation"},
        )
        assert not errors, errors
        (OUT / "screenshots/manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        (OUT / "results/browser-tower.json").write_text(
            json.dumps(
                {
                    "views_visited": 5,
                    "states_captured": len(manifest),
                    "javascript_errors": errors,
                    "atlas_access_attempted": False,
                },
                indent=2,
            )
            + "\n"
        )
        browser.close()


if __name__ == "__main__":
    main()
