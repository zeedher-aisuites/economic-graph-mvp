# ruff: noqa: E501
"""Revisión reproducible de la presentación con navegador real y exportación PDF."""

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from playwright.sync_api import Error, sync_playwright

APP = Path(__file__).resolve().parents[1]
OUT = APP / "evidence/iteration-2/results"
SHOTS = APP / "evidence/iteration-2/presentation"
BROWSER = os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium")


def main():
    SHOTS.mkdir(exist_ok=True)
    report = {
        "run_at": datetime.now(ZoneInfo("America/Mexico_City")).isoformat(),
        "origin": "Validación de la presentación, misión 2, realizada por Codex. Las pruebas y capturas originales se conservan sin repetir ni atribuir al candidato.",
        "base_commit": "bad88c56d850a87d188a9b0d7a4d515f6766f408",
        "javascript_errors": [],
        "failed_requests": [],
        "layouts": [],
        "checks": [],
    }
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=BROWSER, args=["--no-sandbox"])
        context = browser.new_context(
            viewport={"width": 1600, "height": 1030}, device_scale_factor=1
        )
        page = context.new_page()
        page.on("pageerror", lambda err: report["javascript_errors"].append(str(err)))
        page.on(
            "requestfailed",
            lambda req: report["failed_requests"].append({"url": req.url, "failure": req.failure}),
        )
        response = page.goto("http://127.0.0.1:8765/")
        assert response.status == 200
        page.wait_for_function("window.DECK_API")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(350)
        slides = page.evaluate("window.DECK_API.slides.map(s=>({id:s.id,title:s.title}))")
        assert len(slides) == 30
        for width, height in [(1600, 1030), (1366, 768)]:
            page.set_viewport_size({"width": width, "height": height})
            for i, slide in enumerate(slides):
                page.evaluate("i=>window.DECK_API.goto(i)", i)
                page.wait_for_timeout(320)
                layout = page.evaluate("""() => {
                  const s=document.querySelector('.slide.active'), c=s.querySelector('.slide-content'), cr=c.getBoundingClientRect();
                  const issues=[];
                  if(c.scrollWidth>c.clientWidth+2||c.scrollHeight>c.clientHeight+2)issues.push('contenedor desbordado');
                  for(const e of c.querySelectorAll('h2,h3,p,pre,table,svg,.number,.cover-title,.cover-subtitle')){
                    const r=e.getBoundingClientRect();
                    if(r.width===0||r.height===0)continue;
                    if(r.bottom>cr.bottom+2||r.right>cr.right+2||r.left<cr.left-2||r.top<cr.top-2)issues.push(e.tagName+': '+e.textContent.trim().slice(0,70));
                    if(e.tagName==='PRE'&&(e.scrollHeight>e.clientHeight+2||e.scrollWidth>e.clientWidth+2))issues.push('código requiere scroll');
                  }
                  const images=[...s.querySelectorAll('img')].map(e=>({file:e.getAttribute('src'),loaded:e.complete&&e.naturalWidth>0,width:e.naturalWidth,height:e.naturalHeight}));
                  const stage=document.querySelector('#stage').getBoundingClientRect();
                  return {issues,images,stage_fits:stage.width<=innerWidth+1,body_horizontal_scroll:document.body.scrollWidth>innerWidth+1};
                }""")
                report["layouts"].append(
                    {"slide": i + 1, "id": slide["id"], "viewport": f"{width}×{height}", **layout}
                )
                if width == 1600:
                    page.locator("#stage").screenshot(
                        path=str(SHOTS / f"{i + 1:02d}-{slide['id']}.png")
                    )
            print(f"Recorridas {len(slides)} diapositivas a {width}×{height}.", flush=True)
        page.set_viewport_size({"width": 1600, "height": 1030})
        page.evaluate("window.DECK_API.goto(0)")
        page.keyboard.press("ArrowRight")
        assert page.locator(".slide.active").get_attribute("data-index") == "1"
        page.keyboard.press("ArrowLeft")
        assert page.locator(".slide.active").get_attribute("data-index") == "0"
        page.keyboard.press("End")
        assert page.locator(".slide.active").get_attribute("data-index") == "15"
        page.keyboard.press("Home")
        page.keyboard.press("i")
        assert page.locator("#overlay").is_visible()
        page.locator('#overlay [data-goto="a-flujo"]').click()
        assert page.locator(".slide.active").get_attribute("data-index") == "16"
        page.keyboard.press("n")
        assert "Recibe observaciones" in page.locator("#overlay-body").inner_text()
        page.keyboard.press("Escape")
        report["checks"].append("Teclado: flechas, Home, End, índice, anexo, notas y Escape.")

        page.evaluate("window.DECK_API.goto('filtros')")
        for value, count in [("industry", 3), ("cafe", 1), ("all", 3)]:
            page.locator(f'[data-filter="{value}"]').click()
            assert page.locator("#fixed-position").inner_text() == "#3"
            assert page.locator("#filter-table tbody tr").count() == count
            assert page.locator("#filter-table .highlight").inner_text().split()[-2:] == [
                "#10",
                "#3",
            ]
        report["checks"].append(
            "Reconstrucción de filtros: #10 y #3 se conservan en los tres estados."
        )
        page.evaluate("window.DECK_API.goto('economia')")
        page.locator('[data-scope="demo"]').click()
        assert "−$15,450" in page.locator("#economic-cases").inner_text()
        assert "40.625" in page.locator("#economic-details").inner_text()
        page.locator('[data-scope="hypothetical"]').click()
        assert "+$39,000" in page.locator("#economic-cases").inner_text()
        assert "−$41,000" in page.locator("#economic-cases").inner_text()
        assert "1.025" in page.locator("#economic-details").inner_text()
        report["checks"].append(
            "Escalas y cuatro escenarios: resultados y umbrales iguales a los JSON reproducidos."
        )
        page.evaluate("window.DECK_API.goto('torre')")
        for i in range(5):
            page.locator(f'[data-tower="{i}"]').click()
            page.wait_for_function(
                "document.querySelector('#tower-image img').complete && document.querySelector('#tower-image img').naturalWidth>0"
            )
        page.locator("#tower-image img").click()
        assert page.locator("#image-viewer").is_visible()
        page.keyboard.press("Escape")
        page.locator('[data-tower="0"]').click()
        report["checks"].append(
            "Cinco capturas de la torre cargadas; ampliación y cierre funcionan."
        )
        for i in range(len(slides)):
            page.evaluate("i=>window.DECK_API.goto(i)", i)
            page.locator('[data-action="evidence"]').click()
            assert page.locator("#overlay .source-links a").count() > 0
            page.keyboard.press("Escape")
        content = json.loads((APP / "content.json").read_text())
        for slide in content:
            page.evaluate("id=>window.DECK_API.goto(id)", slide["id"])
            page.locator('[data-action="notes"]').click()
            assert page.locator(".note-speech").inner_text() == slide["speech"]
            page.keyboard.press("Escape")
        assert (
            "¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?"
            == page.evaluate("window.DECK_DATA.challengeQuestion")
        )
        assert sum(not x.get("annex") for x in content) == 16
        recorded = json.loads((APP / "evidence/results/context-T2.json").read_text())
        assert page.evaluate("window.DECK_DATA.context") == recorded
        report["checks"].append(
            "Guion de las 30 diapositivas idéntico a la fuente regenerada; pregunta del reto y datos técnicos conservados."
        )
        checked = set()
        for slide in content:
            for source in slide["sources"]:
                url = source["url"]
                if url in checked:
                    continue
                checked.add(url)
                path, anchor = url.split("#")
                assert (APP / path).is_file(), path
                assert f'id="{anchor}"' in (APP / path).read_text(), url
                assert page.request.get("http://127.0.0.1:8765/" + path).status == 200
        report["source_links_checked"] = len(checked)
        report["checks"].append(
            "Los 30 paneles de evidencia abren y todas las fuentes resuelven con anclas de línea."
        )

        page.evaluate("window.DECK_API.goto('cafe')")
        with context.expect_page() as popup:
            page.locator('[data-action="presenter"]').click()
        presenter = popup.value
        presenter.wait_for_function("window.DECK_API")
        presenter.wait_for_selector(".presenter-notes")
        page.evaluate("window.DECK_API.goto('arquitectura')")
        presenter.wait_for_function("location.hash==='#arquitectura'")
        presenter.locator('#presenter-view [data-action="next"]').click()
        page.wait_for_function("location.hash==='#torre'")
        presenter.screenshot(path=str(SHOTS / "presentador.png"))
        presenter.close()
        report["checks"].append(
            "Presentador: notas e iframe, sincronización bidireccional con ventana principal."
        )

        # Real user-click fullscreen, clean mode, keyboard and both exit paths.
        page.evaluate("window.DECK_API.goto('cafe')")
        page.locator('[data-action="start"]').click()
        page.wait_for_function("window.DECK_API.isPresenting()")
        page.wait_for_timeout(500)
        assert page.locator(".slide.active").get_attribute("data-index") == "0"
        assert not page.locator(".appbar").is_visible()
        assert not page.locator(".deck-nav").is_visible()
        native = page.evaluate("!!document.fullscreenElement")
        report["fullscreen"] = {
            "native_api_accepted": native,
            "clean_mode": True,
            "starts_at_first_slide": True,
        }
        if not native:
            assert page.locator("#presentation-message").is_visible()
        page.set_viewport_size({"width": 1920, "height": 1080})
        for i, slide in enumerate(slides):
            page.evaluate("i=>window.DECK_API.goto(i)", i)
            page.wait_for_timeout(100)
            layout = page.evaluate("""() => {
                const s=document.querySelector('.slide.active'),c=s.querySelector('.slide-content'),r=document.querySelector('#stage').getBoundingClientRect();
                return {issues:(c.scrollWidth>c.clientWidth+2||c.scrollHeight>c.clientHeight+2)?['contenedor desbordado']:[],images:[...s.querySelectorAll('img')].map(e=>({loaded:e.complete&&e.naturalWidth>0})),stage_fits:r.width<=innerWidth+1,body_horizontal_scroll:document.body.scrollWidth>innerWidth+1};
            }""")
            report["layouts"].append(
                {"slide": i + 1, "id": slide["id"], "viewport": "1920×1080 inmersivo", **layout}
            )
            if i in [0, 3, 15]:
                page.screenshot(path=str(SHOTS / f"immersive-{i + 1:02d}.png"))
        page.evaluate("window.DECK_API.goto(0)")
        page.keyboard.press("ArrowRight")
        assert page.locator(".slide.active").get_attribute("data-index") == "1"
        page.keyboard.press("n")
        assert page.locator("#overlay").is_visible()
        page.keyboard.press("Escape")
        assert page.evaluate("window.DECK_API.isPresenting()")
        page.keyboard.press("Escape")
        page.wait_for_function("!window.DECK_API.isPresenting()")
        page.wait_for_function("!document.fullscreenElement")
        page.evaluate("window.DECK_API.goto('cafe')")
        page.locator('[data-action="resume"]').click()
        page.wait_for_function("window.DECK_API.isPresenting()")
        assert page.locator(".slide.active").get_attribute("data-index") == "8"
        page.locator('[data-action="exit-presentation"]').click()
        page.wait_for_function("!window.DECK_API.isPresenting()")
        page.wait_for_function("!document.fullscreenElement")
        # A browser-origin fullscreen exit also restores the ordinary interface.
        page.locator('[data-action="resume"]').click()
        page.wait_for_timeout(300)
        if page.evaluate("!!document.fullscreenElement"):
            page.evaluate("document.exitFullscreen()")
            page.wait_for_function("!window.DECK_API.isPresenting()")
            report["fullscreen"]["browser_exit_restores_normal"] = True
        else:
            page.evaluate("window.DECK_API.leavePresentation()")
            report["fullscreen"]["browser_exit_restores_normal"] = (
                "not exercised; native fullscreen unavailable"
            )
        report["checks"].append(
            "Iniciar desde primera, continuar en actual, teclado, cierre de notas, Esc, botón Salir y salida nativa de pantalla completa."
        )

        # Controlled browser-API failure: validates the fallback without bypassing policy.
        denied = context.new_page()
        denied.add_init_script(
            "Element.prototype.requestFullscreen=function(){window.__attempts=(window.__attempts||0)+1;return Promise.reject(new DOMException('Rechazo inyectado para QA','NotAllowedError'));};"
        )
        denied.goto("http://127.0.0.1:8765/")
        denied.wait_for_function("window.DECK_API")
        denied.locator('[data-action="start"]').click()
        denied.wait_for_function(
            "document.querySelector('#presentation-message').textContent.includes('F11')"
        )
        assert denied.evaluate("window.DECK_API.isPresenting() && !document.fullscreenElement")
        assert denied.evaluate("window.__attempts") == 1
        denied.keyboard.press("ArrowRight")
        assert denied.locator(".slide.active").get_attribute("data-index") == "1"
        denied.screenshot(path=str(SHOTS / "fullscreen-denied-fixture.png"))
        denied.locator('[data-action="dismiss-message"]').click()
        denied.keyboard.press("Escape")
        assert not denied.evaluate("window.DECK_API.isPresenting()")
        denied.close()
        unsupported = context.new_page()
        unsupported.add_init_script(
            "Object.defineProperty(Element.prototype,'requestFullscreen',{value:undefined,configurable:true});Object.defineProperty(Element.prototype,'webkitRequestFullscreen',{value:undefined,configurable:true});"
        )
        unsupported.goto("http://127.0.0.1:8765/")
        unsupported.wait_for_function("window.DECK_API")
        unsupported.locator('[data-action="start"]').click()
        assert unsupported.evaluate("window.DECK_API.isPresenting()")
        assert "F11" in unsupported.locator("#presentation-message").inner_text()
        unsupported.locator('[data-action="exit-presentation"]').click()
        assert not unsupported.evaluate("window.DECK_API.isPresenting()")
        unsupported.close()
        report["fullscreen"]["controlled_denial_fallback"] = (
            "PASS; API rejection fixture, not a natural denial"
        )
        report["fullscreen"]["controlled_unsupported_fallback"] = "PASS; API unavailable fixture"
        report["checks"].append(
            "Fallos controlados de fullscreen: rechazo y API ausente mantienen modo inmersivo, mensaje manual y salida funcional."
        )

        page.set_viewport_size({"width": 390, "height": 844})
        page.evaluate("window.DECK_API.goto(0)")
        page.wait_for_timeout(350)
        assert page.evaluate("document.body.scrollWidth <= innerWidth")
        page.keyboard.press("n")
        assert page.locator("#overlay").is_visible()
        page.screenshot(path=str(SHOTS / "movil-notas.png"))
        page.keyboard.press("Escape")
        report["checks"].append(
            "Móvil 390×844: escenario ajustado sin scroll horizontal y notas consultables. No revisión de legibilidad de proyección en móvil."
        )

        page.set_viewport_size({"width": 1600, "height": 1030})
        page.evaluate("window.DECK_API.goto('arquitectura')")
        svg = page.locator(".architecture-svg").evaluate(
            "e=>{let n=e.cloneNode(true);n.setAttribute('xmlns','http://www.w3.org/2000/svg');n.setAttribute('width','1280');n.setAttribute('height','375');n.setAttribute('style','background:#f3f5ef;font-family:Arial,sans-serif');return n.outerHTML}"
        )
        report["original_diagram_reused"] = bool(svg)
        page.evaluate("window.DECK_API.goto(0)")
        page.evaluate(
            "window.DECK_API.setScope('hypothetical');window.DECK_API.setFilter('all');window.DECK_API.setTower(0)"
        )
        page.emulate_media(media="print")
        page.pdf(
            path=str(APP / "ConectaPyME.pdf"),
            prefer_css_page_size=True,
            print_background=True,
            display_header_footer=False,
        )
        page.emulate_media(media="screen")
        info = subprocess.check_output(["pdfinfo", str(APP / "ConectaPyME.pdf")], text=True)
        assert "Pages:           30" in info
        report["pdf"] = {
            "file": "ConectaPyME.pdf",
            "pages": 30,
            "format": "16:9, 1440×810 CSS px",
            "speaker_notes": "docs/guia-estudio.html, no incluidas en diapositivas PDF",
        }

        # Installation independent of the repository, with no .venv, original app or node_modules.
        clean = APP / "work/clean-check"
        if clean.exists():
            shutil.rmtree(clean)
        clean.mkdir(parents=True)
        for name in [
            "index.html",
            "app.js",
            "data.js",
            "style.css",
            "assets",
            "evidence",
            "docs",
            "README.md",
        ]:
            source = APP / name
            if source.is_dir():
                shutil.copytree(source, clean / name)
            else:
                shutil.copy2(source, clean / name)
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "http.server",
                "8766",
                "--bind",
                "127.0.0.1",
                "--directory",
                str(clean),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            time.sleep(0.5)
            isolated = context.new_page()
            assert isolated.goto("http://127.0.0.1:8766/").status == 200
            isolated.wait_for_function("window.DECK_API")
            isolated.evaluate("document.fonts.ready")
            for i in range(len(slides)):
                isolated.evaluate("i=>window.DECK_API.goto(i)", i)
                assert isolated.locator(".slide.active").count() == 1
            isolated.close()
        finally:
            server.terminate()
            server.wait(timeout=5)
        offline = browser.new_context(offline=True, viewport={"width": 1440, "height": 900})
        local = offline.new_page()
        file_check = "not_verified"
        try:
            local.goto((clean / "index.html").as_uri())
            local.wait_for_function("window.DECK_API")
            assert local.locator(".slide").count() == 30
            local.evaluate("window.DECK_API.goto('cafe')")
            local.wait_for_function(
                "document.querySelector('#slide-cafe img').complete && document.querySelector('#slide-cafe img').naturalWidth > 0"
            )
            local.keyboard.press("n")
            assert local.locator("#overlay").is_visible()
            file_check = "PASS"
        except Error as error:
            if "ERR_BLOCKED_BY_ADMINISTRATOR" not in str(error):
                raise
            file_check = "NOT_VERIFIED: file:// blocked by managed browser policy; use the verified local HTTP server."
        offline.close()
        report["clean_install"] = {
            "standalone_copy": True,
            "http_server_as_readme": True,
            "all_30_slides_traversed": True,
            "file_url_with_network_offline": file_check,
            "requires_original_server": False,
            "runtime_packages_installed": 0,
        }
        report["checks"].append(
            "Copia independiente verificada con servidor del README, sin instalar dependencias. Apertura file:// se registra aparte según política del navegador."
        )
        browser.close()
    import hashlib

    preservation = json.loads((OUT / "preservation-baseline.json").read_text())
    changed = []
    for rel, expected in preservation["files"].items():
        path = APP.parent / rel
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            changed.append(rel)
    report["preserved_original_files"] = {"count": len(preservation["files"]), "changed": changed}
    assert not changed, changed
    failures = [
        row
        for row in report["layouts"]
        if row["issues"]
        or not row["stage_fits"]
        or row["body_horizontal_scroll"]
        or not all(img["loaded"] for img in row["images"])
    ]
    report["layout_failures"] = failures
    report["result"] = (
        "PASS"
        if not failures and not report["javascript_errors"] and not report["failed_requests"]
        else "FAIL"
    )
    (OUT / "presentation-qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "result": report["result"],
                "layouts": len(report["layouts"]),
                "failures": failures,
                "source_links": len(checked),
                "checks": report["checks"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    assert report["result"] == "PASS"


if __name__ == "__main__":
    main()
