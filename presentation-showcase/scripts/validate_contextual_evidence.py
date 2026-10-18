# ruff: noqa: E501
"""Validar la misión 3 sin sobrescribir capturas, pruebas ni PDF de las misiones previas."""

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

from PIL import Image, ImageChops
from playwright.sync_api import sync_playwright

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parent
OUT = APP / "evidence/iteration-3"
BASE = "23a8efac164f8631dae57e9c9e8e3bcf9efe66ae"
URL = "http://127.0.0.1:8765/"
MAPPING = {
    "procedencia": ["hornos"],
    "cambio": ["leaders"],
    "cafe": ["confirmed", "context"],
    "arquitectura": ["ledger", "finance", "filters"],
}


def write_capture_manifest():
    files = []
    for path in sorted((OUT / "panels").glob("*.png")):
        with Image.open(path) as shot:
            dimensions = list(shot.size)
        files.append(
            {
                "file": str(path.relative_to(APP)),
                "kind": "Captura de panel o controles de la presentación; no nueva ejecución de Streamlit",
                "captured_at_utc": datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat(),
                "dimensions_px": dimensions,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
        )
    manifest = {
        "base_commit": BASE,
        "product_source_commit": "774dacd80e6410ca43299f63f19d9744a31929c0",
        "mode": "offline, datos sintéticos; árbol de trabajo validado antes del commit",
        "frontend_sha256": {
            name: hashlib.sha256((APP / name).read_bytes()).hexdigest()
            for name in ["index.html", "app.js", "evidence-panels.js", "style.css", "data.js"]
        },
        "captures": files,
        "streamlit_captures_reused": "evidence/screenshots/manifest.json: 08-ranking-global, 09-ranking-industria, 10-ranking-cafe; originales sin cambios",
    }
    (OUT / "panels/manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main():
    shots = OUT / "panels"
    shots.mkdir(parents=True, exist_ok=True)
    report = {
        "run_at": datetime.now(UTC).isoformat(),
        "origin": "Validación automatizada de misión 3 por Codex; no ejecución personal del candidato.",
        "base": BASE,
        "browser": "Chromium/Linux",
        "errors": [],
        "requests_failed": [],
        "checks": [],
        "panel_layouts": [],
    }
    payload = json.loads((OUT / "data/contextual-evidence.json").read_text(encoding="utf-8"))
    for name, meta in payload["files"].items():
        raw = (ROOT / meta["path"]).read_bytes()
        assert (OUT / "data" / name).read_bytes() == raw
        assert hashlib.sha256(raw).hexdigest() == meta["sha256"]
    ledger = json.loads((ROOT / "data/observable/observations.json").read_text(encoding="utf-8"))
    for row in ledger["observations"]:
        entry = payload["records"][row["observation_id"]]
        assert entry["record"] == row
        assert (
            row["observation_id"]
            in (ROOT / "data/observable/observations.json")
            .read_text(encoding="utf-8")
            .splitlines()[entry["line"] - 1]
        )
    assert json.loads(
        (OUT / "data/context-reproduced.json").read_text(encoding="utf-8")
    ) == json.loads((APP / "evidence/results/context-T2.json").read_text(encoding="utf-8"))
    assert json.loads(
        (OUT / "data/finance-reproduced.json").read_text(encoding="utf-8")
    ) == json.loads((APP / "evidence/results/finance.json").read_text(encoding="utf-8"))
    report["checks"].append(
        "83 registros íntegros; copias de JSON byte a byte; contexto y finanzas iguales a V1."
    )
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=os.environ.get("CHROMIUM_PATH", "/usr/bin/chromium"),
            args=["--no-sandbox"],
        )
        ctx = browser.new_context(viewport={"width": 1600, "height": 1030})
        audience = ctx.new_page()
        audience.on("pageerror", lambda err: report["errors"].append(str(err)))
        audience.on("requestfailed", lambda req: report["requests_failed"].append(req.url))
        audience.goto(URL)
        audience.wait_for_function("window.DECK_API")
        audience.evaluate("document.fonts.ready")
        audience.wait_for_timeout(400)
        slides = audience.evaluate("window.DECK_API.slides")
        assert len(slides) == 30 and sum(not s.get("annex") for s in slides) == 16
        previous_slides = json.loads(
            subprocess.check_output(
                ["git", "show", BASE + ":presentation-showcase/content.json"], cwd=ROOT, text=True
            )
        )
        assert all(a["speech"] == b["speech"] for a, b in zip(slides, previous_slides, strict=True))
        report["checks"].append(
            "Los 30 discursos principales/anexos se conservan; las instrucciones opcionales están separadas."
        )
        # Compare actual rendered slides, not only source HTML, with all 30 V2 captures.
        unchanged = []
        for i, slide in enumerate(slides):
            audience.evaluate("i=>DECK_API.goto(i)", i)
            audience.wait_for_timeout(350)
            current = Image.open(io.BytesIO(audience.locator("#stage").screenshot())).convert("RGB")
            before = Image.open(
                APP / f"evidence/iteration-2/presentation/{i + 1:02d}-{slide['id']}.png"
            ).convert("RGB")
            assert current.size == before.size
            diff = ImageChops.difference(current, before)
            assert diff.getbbox() is None, f"Composición visual cambió: {slide['id']}"
            unchanged.append(slide["id"])
            layout = audience.evaluate(
                """() => {const c=document.querySelector('.slide.active .slide-content');return c.scrollWidth<=c.clientWidth+2&&c.scrollHeight<=c.clientHeight+2;}"""
            )
            assert layout
        report["slides_pixel_identical_to_v2"] = unchanged
        report["checks"].append(
            "Las 30 composiciones son idénticas píxel a píxel a las capturas de V2 a 1600×1030."
        )
        links = {r["url"] for slide in slides for r in slide["sources"]}
        links |= {r["url"] for sources in payload["sources"].values() for r in sources}
        for url in links:
            response = ctx.request.get(URL + url.split("#")[0])
            assert response.ok, url
            if "#" in url:
                anchor = url.split("#")[1]
                assert f'id="{anchor}"' in response.text(), url
        report["source_links_checked"] = len(links)
        for meta in payload["files"].values():
            assert ctx.request.get(URL + meta["url"]).body() == (ROOT / meta["path"]).read_bytes()
        # Local controls: explanation -> exact records -> source, without mandatory extra slides.
        for width, height in [(1600, 1030), (1366, 768), (1920, 1080)]:
            audience.set_viewport_size({"width": width, "height": height})
            for slide, ids in MAPPING.items():
                audience.evaluate("id=>DECK_API.goto(id)", slide)
                if width == 1920:
                    audience.locator('[data-action="resume"]').click()
                for evidence in ids:
                    audience.keyboard.press("e")
                    audience.locator(f'#overlay [data-contextual="{evidence}"]').click()
                    audience.wait_for_selector("#overlay.contextual-panel[open]")
                    assert audience.url.endswith("#" + slide)
                    assert audience.locator(".ce-technical").count() == 1
                    assert not audience.locator(".ce-technical").evaluate("e=>e.open")
                    layout = audience.evaluate(
                        """() => {const d=document.querySelector('#overlay'),b=document.querySelector('#overlay-body'),r=d.getBoundingClientRect();return {dialog_fits:r.left>=0&&r.top>=0&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1,body_has_no_horizontal_overflow:b.scrollWidth<=b.clientWidth+2};}"""
                    )
                    assert all(layout.values()), (width, evidence, layout)
                    report["panel_layouts"].append(
                        {"evidence": evidence, "viewport": f"{width}×{height}", **layout}
                    )
                    if width == 1600:
                        audience.screenshot(path=str(shots / f"{evidence}.png"))
                    if evidence in ["hornos", "confirmed", "context", "ledger", "leaders"]:
                        group = {
                            "hornos": "hornos",
                            "confirmed": "confirmed",
                            "context": "context",
                            "ledger": None,
                            "leaders": "panificadora",
                        }[evidence]
                        ids_expected = (
                            payload["groups"][group] if group else ["OBS-001", "OBS-028", "OBS-026"]
                        )
                        audience.locator(".ce-technical > summary").click()
                        originals = audience.locator(".ce-technical > .ce-json")
                        assert originals.count() == len(ids_expected)
                        for i, oid in enumerate(ids_expected):
                            assert (
                                json.loads(originals.nth(i).inner_text())
                                == payload["records"][oid]["record"]
                            )
                        if width == 1600 and evidence == "hornos":
                            audience.locator(".ce-technical").scroll_into_view_if_needed()
                            audience.screenshot(path=str(shots / "hornos-technical.png"))
                    audience.keyboard.press("Escape")
                    assert not audience.locator("#overlay").evaluate("e=>e.open")
                    assert audience.url.endswith("#" + slide)
                if width == 1920:
                    assert audience.evaluate("DECK_API.isPresenting()")
                    audience.keyboard.press("Escape")
            audience.evaluate("DECK_API.goto('cambio')")
            audience.evaluate("DECK_API.requestContextual('leaders',{company:'carga'})")
            assert audience.locator(".ce-company").inner_text() == "Carga Urbana del Centro"
            assert audience.locator(".ce-secondary[open] .ce-table tbody tr").count() == 3
            audience.keyboard.press("Escape")
        report["checks"].append(
            "21 estados de panel sin desbordamiento horizontal; JSON originales exactos y cierre sin cambiar diapositiva."
        )
        audience.set_viewport_size({"width": 1600, "height": 1030})
        presenter = ctx.new_page()
        presenter.on("pageerror", lambda err: report["errors"].append(str(err)))
        presenter.goto(URL + "?presenter=1#procedencia")
        presenter.wait_for_function("window.DECK_API")
        pages_before = len(ctx.pages)
        for slide, ids in MAPPING.items():
            presenter.evaluate("id=>DECK_API.goto(id)", slide)
            audience.wait_for_function("id=>location.hash==='#'+id", arg=slide)
            expected_speech = next(s["speech"] for s in slides if s["id"] == slide)
            assert presenter.locator(".note-speech").inner_text() == expected_speech
            for evidence in ids:
                print("Control remoto:", slide, evidence, flush=True)
                presenter.locator(f'.contextual-buttons [data-contextual="{evidence}"]').click()
                audience.wait_for_selector("#overlay.contextual-panel[open]")
                presenter.wait_for_function(
                    "document.querySelector('#contextual-status').textContent.startsWith('Panel abierto')"
                )
                assert not presenter.locator("#overlay").evaluate("e=>e.open")
                assert audience.url.endswith("#" + slide)
                assert audience.locator("#overlay-title").inner_text()
                presenter.locator('[data-action="close-contextual"]').click()
                audience.wait_for_function("!document.querySelector('#overlay').open")
                assert audience.url.endswith("#" + slide)
        # A close event is queued by the browser: an immediate reopening must keep its new state.
        presenter.evaluate("DECK_API.goto('procedencia')")
        presenter.evaluate("DECK_API.requestContextual('hornos')")
        audience.wait_for_selector("#overlay.contextual-panel[open]")
        presenter.evaluate("DECK_API.closeContextual();DECK_API.requestContextual('hornos')")
        audience.wait_for_timeout(150)
        assert audience.locator("#overlay").evaluate("e=>e.open")
        presenter.locator('[data-action="close-contextual"]').click()
        audience.wait_for_function("!document.querySelector('#overlay').open")
        report["checks"].append(
            "Cierre y reapertura inmediata: el evento close anterior no borra el estado del panel nuevo."
        )
        assert len(ctx.pages) == pages_before
        report["checks"].append(
            "Los siete paneles se abren y cierran desde el presentador en la ventana de audiencia; no crean pestañas."
        )
        presenter.evaluate("DECK_API.goto('cambio')")
        presenter.get_by_role("button", name="Mostrar Carga Urbana", exact=True).click()
        audience.wait_for_function(
            "document.querySelector('.ce-company')?.textContent==='Carga Urbana del Centro'"
        )
        audience.screenshot(path=str(shots / "leaders-carga-remote.png"))
        audience.keyboard.press("Escape")
        presenter.wait_for_function(
            "document.querySelector('#contextual-status').textContent.startsWith('Panel cerrado')"
        )
        presenter.evaluate("DECK_API.goto('arquitectura')")
        for label, key in [
            ("Filtro: general", "global"),
            ("Filtro: industria", "industry"),
            ("Filtro: Jacaranda", "company"),
        ]:
            presenter.get_by_role("button", name=label, exact=True).click()
            audience.wait_for_selector(
                f".ce-tabs button[data-context-options*='{key}'][aria-pressed=\"true\"]"
            )
            assert (
                "#10" in audience.locator(".ce-proof").inner_text()
                and "#3" in audience.locator(".ce-proof").inner_text()
            )
            audience.screenshot(path=str(shots / f"filters-{key}-remote.png"))
        presenter.screenshot(path=str(shots / "presenter-controls.png"))
        audience.locator("[data-ce-zoom]").click()
        audience.wait_for_selector(".ce-full-capture")
        assert audience.locator(".ce-full-capture").evaluate("e=>e.complete&&e.naturalWidth>0")
        audience.screenshot(path=str(shots / "filters-capture-expanded.png"))
        audience.locator(".ce-return").click()
        assert audience.locator('.ce-tabs [aria-pressed="true"]').inner_text() == "Solo Jacaranda"
        presenter.locator('[data-action="close-contextual"]').click()
        audience.wait_for_function("!document.querySelector('#overlay').open")
        # Audience remains in presentation mode while evidence is controlled from the other window.
        audience.bring_to_front()
        audience.locator('[data-action="resume"]').click()
        audience.wait_for_function(
            "document.fullscreenElement!==null&&DECK_API.isPresenting()", timeout=5000
        )
        report["fullscreen_native_verified"] = True
        presenter.locator('.contextual-buttons [data-contextual="ledger"]').click()
        audience.wait_for_selector("#overlay.contextual-panel[open]")
        assert audience.evaluate("document.fullscreenElement!==null")
        presenter.locator('[data-action="close-contextual"]').click()
        audience.wait_for_function("!document.querySelector('#overlay').open")
        assert audience.evaluate("DECK_API.isPresenting()")
        audience.keyboard.press("Escape")
        audience.keyboard.press("ArrowRight")
        assert audience.url.endswith("#torre")
        presenter.wait_for_function("location.hash==='#torre'")
        # Closing via presenter must not stop or reset its clock.
        assert presenter.locator("#timer").inner_text() != "00:00"
        assert audience.evaluate("DECK_DATA.context") == json.loads(
            (APP / "evidence/results/context-T2.json").read_text(encoding="utf-8")
        )
        report["checks"].append(
            "Selectores remotos de empresa y filtros, ampliación y regreso, cierre desde audiencia, reloj y fullscreen nativo conservados."
        )
        # No audience and unavailable BroadcastChannel: explicit local fallback, no new window.
        isolated = browser.new_context(viewport={"width": 1366, "height": 900})
        isolated.add_init_script("window.BroadcastChannel=undefined")
        fallback = isolated.new_page()
        fallback.goto(URL + "?presenter=1#cafe")
        fallback.locator('.contextual-buttons [data-contextual="confirmed"]').click()
        fallback.wait_for_selector("#overlay.contextual-panel[open]")
        assert "Sin confirmación" in fallback.locator("#overlay-body").inner_text()
        assert len(isolated.pages) == 1
        fallback.screenshot(path=str(shots / "controlled-channel-unavailable-fallback.png"))
        fallback.keyboard.press("Escape")
        local = isolated.new_page()
        local.goto(URL + "#cafe")
        local.keyboard.press("e")
        local.locator('#overlay [data-contextual="context"]').click()
        assert local.locator("#overlay.contextual-panel").evaluate("e=>e.open")
        isolated.close()
        report["checks"].append(
            "Fixture controlado sin BroadcastChannel: copia local e instrucciones; los enlaces de la misma presentación siguen funcionando."
        )
        # A clean directory only needs the static files and the README server command.
        clean = APP / "work/clean-contextual"
        if clean.exists():
            shutil.rmtree(clean)
        clean.mkdir(parents=True)
        for name in [
            "index.html",
            "app.js",
            "evidence-panels.js",
            "data.js",
            "style.css",
            "assets",
            "docs",
            "evidence",
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
            check = ctx.new_page()
            # Server starts within this bounded browser retry; no remote connection is involved.
            for _attempt in range(10):
                try:
                    check.goto("http://127.0.0.1:8766/?evidence=hornos#procedencia")
                    break
                except Exception:
                    check.wait_for_timeout(100)
            check.wait_for_selector("#overlay.contextual-panel[open]")
            assert check.locator(".ce-table tbody strong").first.inner_text() == "OBS-028"
            check.close()
        finally:
            server.terminate()
            server.wait(timeout=5)
        report["checks"].append(
            "Copia independiente servida por HTTP local, sin Streamlit, Atlas, npm o paquetes de ejecución."
        )
        ctx.close()
        browser.close()
    files = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", BASE], cwd=ROOT, text=True
    ).splitlines()
    protected = [
        f
        for f in files
        if not f.startswith("presentation-showcase/")
        or any(
            f.startswith("presentation-showcase/" + prefix)
            for prefix in ["evidence/", "assets/", "experiments/"]
        )
        or f == "presentation-showcase/ConectaPyME.pdf"
    ]
    hashes = {}
    for name in protected:
        expected = subprocess.check_output(["git", "show", BASE + ":" + name], cwd=ROOT)
        actual = (ROOT / name).read_bytes()
        assert actual == expected, name
        hashes[name] = hashlib.sha256(actual).hexdigest()
    report["preserved_files"] = {"count": len(hashes), "changed": [], "sha256": hashes}
    report["pdf"] = (
        "Conservado byte a byte: 30 páginas. Los paneles opcionales son exclusivos de la web."
    )
    assert not report["errors"] and not report["requests_failed"]
    write_capture_manifest()
    report["result"] = "PASS"
    (OUT / "results").mkdir(exist_ok=True)
    (OUT / "results/contextual-qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                k: v
                for k, v in report.items()
                if k not in ["preserved_files", "slides_pixel_identical_to_v2"]
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
