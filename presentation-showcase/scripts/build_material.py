# ruff: noqa: E501
"""Construir datos embebidos, fuentes navegables, guion y trazabilidad sin servicio externo."""

import ast
import csv
import html
import json
from pathlib import Path

from content import FINANCE_STORY_SPEECHES, SLIDES
from contextual_data import build_contextual
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "presentation-showcase"
E = APP / "evidence"
DOCS = APP / "docs"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_ref(ref):
    parts = ref.split(":", 1)
    rel, symbol = parts[0], parts[1] if len(parts) == 2 else None
    path = ROOT / rel
    if not path.exists():
        raise FileNotFoundError(ref)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    start, end = 1, len(lines)
    if symbol:
        tree = ast.parse(text)
        found = next(
            (
                n
                for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == symbol
            ),
            None,
        )
        if found:
            start, end = found.lineno, found.end_lineno
        else:
            found = next(
                (
                    n
                    for n in tree.body
                    if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == symbol for t in n.targets)
                ),
                None,
            )
            if not found:
                raise ValueError(f"Símbolo no encontrado: {ref}")
            start, end = found.lineno, found.end_lineno
    filename = rel.replace("/", "__") + ".html"
    legacy = E / "source-html" / filename
    if legacy.is_file():
        # V1 evidence is immutable in this iteration; reuse its existing viewer and copy.
        return {
            "path": rel,
            "symbol": symbol,
            "start": start,
            "end": end,
            "url": "evidence/source-html/" + filename + "#L" + str(start),
            "original": not rel.startswith("presentation-showcase/"),
            "provenance": "Evidencia conservada de V1; registros automatizados de Codex",
        }
    target = E / "iteration-2/source-html" / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    lexer = PythonLexer()
    formatter = HtmlFormatter(nowrap=True)

    def color(line):
        return (
            highlight(line, lexer, formatter).rstrip("\n")
            if path.suffix == ".py"
            else html.escape(line)
        )

    source_lines = "\n".join(
        f'<div class="line" id="L{i}"><a href="#L{i}">{i}</a><code>{color(line) or " "}</code></div>'
        for i, line in enumerate(lines, 1)
    )
    target.write_text(
        f"""<!doctype html><html lang="es-MX"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(rel)}</title><style>
body{{background:#0b2033;color:#d5e3e8;margin:0;font:14px/1.7 Consolas,monospace}}header{{position:sticky;top:0;background:#102d43;padding:16px 25px;border-bottom:1px solid #34536a;z-index:2;font:13px/1.6 system-ui}}header a{{color:#58dfc6}}main{{padding:22px 0}}.line{{display:flex;gap:20px;min-width:max-content;padding-right:30px;scroll-margin-top:90px}}.line>a{{text-align:right;min-width:65px;color:#6f94a8;text-decoration:none;border-right:1px solid #30495c;padding-right:15px}}code{{white-space:pre}}.line:target{{background:#1f4f50;color:white}}.k,.kn,.kd{{color:#59e3c9}}.s1,.s2,.sa{{color:#ffc181}}.nf,.nc{{color:#a4cbff}}.c1,.sd{{color:#86a6b6}}.mi{{color:#ffc181}}
</style><header><a href="../../../index.html">← Presentación</a> · <strong>{html.escape(rel)}</strong><br>{"Fuente auditada: " + COMMIT if not rel.startswith("presentation-showcase/") else "Documento de apoyo de la versión anterior; consulta su fuente y alcance. No forma parte del motor original."}</header><main>{source_lines}</main></html>""",
        encoding="utf-8",
    )
    # Preserve readable originals, including any source referenced beyond the initial inventory.
    copy = E / "iteration-2/source" / rel
    copy.parent.mkdir(parents=True, exist_ok=True)
    copy.write_text(text, encoding="utf-8")
    return {
        "path": rel,
        "symbol": symbol,
        "start": start,
        "end": end,
        "url": "evidence/iteration-2/source-html/" + filename + "#L" + str(start),
        "original": not rel.startswith("presentation-showcase/"),
        "provenance": "Documento nuevo de apoyo; decisiones declaradas por el candidato y contexto técnico según el archivo",
    }


def doc_page(title, content):
    return f"""<!doctype html><html lang="es-MX"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><link rel="stylesheet" href="../style.css"><style>body{{background:#f1f4ec;color:#173748;max-width:1060px;margin:0 auto;padding:45px 35px 90px;line-height:1.8}}h1,h2,h3{{font-family:Manrope;line-height:1.3;letter-spacing:-.6px}}h1{{font-size:38px}}h2{{margin-top:50px;font-size:27px;border-top:1px solid #c5d4c4;padding-top:22px;scroll-margin-top:25px}}h3{{font-size:19px;margin-top:25px}}p,li{{font-size:17px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#e3ebdf;padding:20px;font-size:13px}}a{{color:#007468;text-underline-offset:4px}}.box{{background:white;padding:22px 27px;border:1px solid #cbd9c8;border-radius:8px}}.warning{{color:#8e4d20;border-left:3px solid #b87d45;padding-left:18px}}.toc{{columns:2;font-size:14px}}.meta{{font-size:13px;color:#657e6d}}table{{border-collapse:collapse;font-size:14px;width:100%;display:block;overflow:auto}}th,td{{padding:10px 12px;border:1px solid #cbd8c5;text-align:left}}@media print{{body{{max-width:none}}.toc{{columns:2}}h2{{break-before:page}}}}</style><a href="../index.html">← Volver a la presentación</a><h1>{html.escape(title)}</h1>{content}</html>"""


SUMMARY = read_json(E / "results/summary.json")
COMMIT = SUMMARY["source_commit"]


def main():
    DOCS.mkdir(exist_ok=True)
    for slide in SLIDES:
        slide["sources"] = [source_ref(ref) for ref in slide["refs"]]
    context = read_json(E / "results/context-T2.json")
    cafe_id = SUMMARY["cafe"]["company_id"]
    industry_ids = [
        c["company_id"]
        for c in context["view"]["companies"]
        if c["attributes"]["sector"]["value"] == SUMMARY["cafe"]["industry"]
    ]
    from economic_graph.tower_read_model import network_data

    snippets = {
        "timezone_original": 'if row["available_at"] == latest["available_at"]',
        "timezone_fixed": 'if parse_time(row["available_at"]) == (\n    parse_time(latest["available_at"])\n)',
        "memory": "class MemoryCollection:\n    def __init__(self):\n        self.documents = {}\n        self.queries = []\n\n    def find(self, query):\n        self.queries.append(deepcopy(query))\n        # Filtra por available_at y subject_id\n        # Devuelve copias de documentos\n",
        "apptest": "\n".join(
            (ROOT / "tests/test_control_tower.py").read_text().splitlines()[121:137]
        ),
    }
    # Snippet "memory" is a labeled excerpt; show an exact short source excerpt instead.
    memory_lines = (ROOT / "tests/test_mongo_observable.py").read_text().splitlines()
    snippets["memory"] = "\n".join(memory_lines[46:55])
    snippets["build_context"] = "\n".join(
        (ROOT / "src/economic_graph/tower_read_model.py").read_text().splitlines()[40:55]
    )
    data = {
        "sourceCommit": COMMIT,
        "presentationBaseCommit": "5fb3aaa369043733f5c722eb0cc9eaecfb237ed2",
        "iteration": 4,
        "contextualEvidence": build_contextual(source_ref),
        "challengeQuestion": "¿Cómo construirías un Economic Graph de PyMEs para una Telco y cómo demostrarías que genera valor económico incremental?",
        "slides": SLIDES,
        "summary": SUMMARY,
        "context": context,
        "industryIds": industry_ids,
        "network": network_data(context, {cafe_id}, cafe_id),
        "captures": read_json(E / "screenshots/manifest.json"),
        "captureDate": SUMMARY["generated_at"][:10],
        "code": {
            key: highlight(value, PythonLexer(), HtmlFormatter(nowrap=True))
            for key, value in snippets.items()
        },
    }
    (APP / "data.js").write_text(
        "// Datos congelados de la ejecución offline; no usa Atlas ni fetch.\nwindow.DECK_DATA = "
        + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    (APP / "content.json").write_text(
        json.dumps(SLIDES, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Guion de exposición y defensa técnica",
        "",
        f"Versión anterior · ConectaPyME: caso de negocio B2B con evidencias opcionales. Implementación de respaldo: `{COMMIT}`. Capturas offline y datos sintéticos de la primera revisión, conservados.",
        "",
        "El relato de alcance, hipótesis y decisiones corresponde a la declaración del candidato. La programación fue asistida por ChatGPT/GPT, Gemini y Codex según esa declaración. Las pruebas, capturas y el experimento de depuración de V1 fueron producidos por Codex y conservan su origen; no acreditan ejecución manual personal. Duraciones a 140 palabras por minuto; ensayar en voz alta.",
        "",
    ]
    guide = [
        '<p class="meta">Fuente '
        + COMMIT
        + " · Datos sintéticos · Atlas no verificado en esta revisión.</p>",
        "<p>Mi relato de decisiones parte de mi declaración como candidato. Usé GPT, Gemini y Codex como apoyo. La evidencia automatizada de V1 conserva su origen en Codex; dirigir, comprender y ejecutar una validación son actividades distintas. Los anexos permiten estudiar y practicar sin inventar autoría.</p>",
        '<div class="toc">',
    ]
    for i, s in enumerate(SLIDES, 1):
        guide.append(f'<p><a href="#{s["id"]}">{i:02d} · {html.escape(s["title"])}</a></p>')
    guide.append("</div>")
    for i, s in enumerate(SLIDES, 1):
        seconds = round(len(s["speech"].split()) / 140 * 60)
        sources = [f"{r['path']}:{r['start']}–{r['end']}" for r in s["sources"]]
        lines += [
            f"## {i:02d}. {s['title']}",
            "",
            f"**Tipo:** {s['status']} · **Duración orientativa:** {seconds} s",
            "",
            "### Discurso",
            "",
            s["speech"],
            "",
            "### Qué señalar",
            "",
            s["point"],
            "",
            "### Pregunta del evaluador",
            "",
            s["question"],
            "",
            "**Respuesta sencilla:** " + s["answer"],
            "",
            "**Si profundiza:** " + s["deep"],
            "",
            "**Verificar en:** " + "; ".join(sources),
            "",
            "**Reproducción:** `" + s["command"] + "`",
            "",
            "**Límite:** " + s["warning"],
            "",
        ]
        if s.get("evidences"):
            lines += ["### Evidencias para mostrar (opcionales)", "", s["evidence_note"], ""]
            lines += [f"- {e['label']} · `{e['id']}`" for e in s["evidences"]]
            lines += [""]
        guide += [
            f'<section><h2 id="{s["id"]}">{i:02d}. {html.escape(s["title"])}</h2><p class="meta">{html.escape(s["status"])} · ~{seconds} segundos</p><div class="box"><p>{html.escape(s["speech"])}</p></div><h3>Qué señalar</h3><p>{html.escape(s["point"])}</p><h3>Pregunta posible</h3><p><strong>{html.escape(s["question"])}</strong></p><p>{html.escape(s["answer"])}</p><h3>Si profundizan</h3><p>{html.escape(s["deep"])}</p><h3>Dónde verificar</h3><ul>'
        ]
        guide.extend(
            f'<li><a href="../{r["url"]}">{html.escape(r["path"])}:{r["start"]}–{r["end"]}</a></li>'
            for r in s["sources"]
        )
        guide += [
            f'</ul><pre>{html.escape(s["command"])}</pre><p class="warning">{html.escape(s["warning"])}</p>'
        ]
        if s.get("evidences"):
            guide += [
                "<h3>Evidencias para mostrar (opcionales)</h3>",
                f"<p>{html.escape(s['evidence_note'])}</p><ul>",
            ]
            guide += [
                f'<li><a href="../index.html?evidence={e["id"]}#{s["id"]}">{html.escape(e["label"])}</a></li>'
                for e in s["evidences"]
            ]
            guide += ["</ul>"]
        guide += ["</section>"]
    lines += [
        "## Evidencia financiera opcional · tres pasos",
        "",
        "Estas notas aparecen únicamente en la vista del presentador cuando se abre `finance-story`; la audiencia ve solo la evidencia financiera.",
        "",
    ]
    for i, speech in enumerate(FINANCE_STORY_SPEECHES, 1):
        lines += [f"### Paso {i} de 3", "", speech, "", "**Duración estimada:** 35–50 segundos", ""]
    guide += [
        '<section><h2 id="finance-story-speech">Evidencia financiera opcional</h2><p class="meta">Tres discursos para la vista del presentador; no se muestran a la audiencia.</p>',
    ]
    for i, speech in enumerate(FINANCE_STORY_SPEECHES, 1):
        guide.append(
            f'<h3>Paso {i} de 3</h3><div class="box"><p>{html.escape(speech)}</p></div><p class="meta">Duración estimada: 35–50 segundos</p>'
        )
    guide.append("</section>")
    (DOCS / "guion.md").write_text("\n".join(lines), encoding="utf-8")
    (DOCS / "guia-estudio.html").write_text(
        doc_page("Guion y guía de defensa", "".join(guide)), encoding="utf-8"
    )
    with (DOCS / "trazabilidad.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(
            [
                "Diapositiva",
                "Afirmación",
                "Tipo",
                "Fuente",
                "Archivo y líneas",
                "Commit de implementación",
                "Prueba o reproducción",
                "Captura",
                "Limitaciones",
                "Origen de verificación",
                "Paneles contextuales opcionales",
                "JSON original del panel",
            ]
        )
        for i, s in enumerate(SLIDES, 1):
            for claim, kind in s["claims"]:
                writer.writerow(
                    [
                        f"{i:02d} · {s['title']}",
                        claim,
                        kind,
                        "Contexto técnico, declaración del candidato y evidencia técnica conservada según las fuentes",
                        "; ".join(f"{r['path']}:{r['start']}–{r['end']}" for r in s["sources"]),
                        COMMIT,
                        s["command"],
                        f"evidence/screenshots/{s['capture']}.png"
                        if s.get("capture")
                        else "Ver resultados y fuentes; sin captura asociada",
                        s["warning"],
                        s.get(
                            "origin", "Evidencia técnica de V1, producida por Codex y conservada"
                        ),
                        "; ".join(e["id"] for e in s.get("evidences", [])),
                        "data/observable/observations.json; config/financial_assumptions.json si corresponde"
                        if s.get("evidences")
                        else "",
                    ]
                )
    brief = [
        "# Práctica personal recomendada",
        "",
        "Mi práctica para defender el proyecto: distinguir mis decisiones de las validaciones automatizadas registradas y comprobar mi comprensión con ejercicios concretos.",
        "",
        "1. Explica la pregunta del reto y por qué elegiste adquisición B2B; distingue el caso ficticio de Totalplay.",
        "2. Reproduce `reproduce.py` y explica 12/17/23, 28/54/83 y el caso Jacaranda.",
        "3. Dibuja las llamadas de `build_context()`; verifica cada rama en el código.",
        "4. Cambia industria y empresa en Streamlit; predice la posición global antes de mirar.",
        "5. Lee MemoryCollection y señala tres diferencias frente a un servidor real.",
        "6. Ejecuta la regresión original en el fixture aislado; explica su fallo esperado.",
        "7. Lee y justifica la comparación experimental de instantes; repite las dos pruebas.",
        "8. Calcula +39,000 y −41,000 en papel e identifica cada supuesto.",
        "9. Explica por qué comparar los dos Top 5 no es un experimento aleatorio.",
        "10. Ensaya las 16 diapositivas principales en voz alta; usa el anexo solo para preguntas.",
        "",
        "Si algo no se entiende, decirlo con claridad y volver al archivo de respaldo. No memorizar una respuesta que no puedas comprobar.",
    ]
    (DOCS / "practica-personal.md").write_text("\n".join(brief), encoding="utf-8")
    duration = sum(len(s["speech"].split()) for s in SLIDES if not s.get("annex")) / 140
    print(
        f"{len(SLIDES)} diapositivas, {sum(not s.get('annex') for s in SLIDES)} principales. Guion principal ~{duration:.1f} minutos a 140 palabras/minuto."
    )
    print("Fuentes resueltas, guion, HTML de estudio y matriz CSV generados.")


if __name__ == "__main__":
    main()
