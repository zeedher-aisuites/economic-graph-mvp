# ruff: noqa: E501
"""Reunir evidencia offline sin escribir en las fuentes originales ni consultar Atlas."""

import ast
import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from economic_graph.contracts import CUTS
from economic_graph.finance import financial_report, load_financial_config
from economic_graph.observable import load_observations
from economic_graph.tower_read_model import build_context, ranking_table, sector, segment_ids

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "presentation-showcase/evidence"


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    ledger = ROOT / "data/observable/observations.json"
    rows = load_observations(ledger)
    contexts = {cut: build_context(rows, cut) for cut in CUTS}
    for cut, context in contexts.items():
        dump(OUT / f"results/context-{cut}.json", context)
    context = contexts["T2"]
    cafe = next(
        c
        for c in context["view"]["companies"]
        if c["attributes"]["display_name"]["value"] == "Café Jacaranda"
    )
    cafe_id = cafe["company_id"]
    industry = sector(cafe)
    all_rows = ranking_table(context)
    segmented = ranking_table(context, segment_ids(context, industry=industry))
    focused = ranking_table(context, segment_ids(context, industry=industry, company_id=cafe_id))
    original = next(r for r in all_rows if r["ID"] == cafe_id)
    assert original == next(r for r in segmented if r["ID"] == cafe_id) == focused[0]
    assert (original["Posición baseline"], original["Posición grafo"]) == (10, 3)
    # Contraejemplo controlado: recalcular solo con una cuenta produce #1, no #3.
    # No es el comportamiento de la app original ni una modificación del dataset.
    demonstration = {
        "source_commit": commit,
        "cut": "T2",
        "industry": industry,
        "company_id": cafe_id,
        "global_count": len(all_rows),
        "industry_count": len(segmented),
        "global": original,
        "industry_filtered": next(r for r in segmented if r["ID"] == cafe_id),
        "company_filtered": focused[0],
        "assertion": "Las tres filas son idénticas; #10 → #3 se conserva.",
        "limitation": "Prueba sintética de consistencia; no calidad comercial ni causalidad.",
    }
    dump(OUT / "results/global-ranking-demo.json", demonstration)
    finance = financial_report(
        load_financial_config(ROOT / "config/financial_assumptions.json"), sensitivity=True
    )
    dump(OUT / "results/finance.json", finance)
    world_path = ROOT / "design-data/restricted/companies_world_design.json"
    world = json.loads(world_path.read_text(encoding="utf-8"))
    universe = len(world["companies"]) if isinstance(world, dict) else len(world)
    assert universe == 30
    summary = {
        "source_commit": commit,
        "mode": "offline",
        "synthetic": True,
        "generated_at": datetime.now(ZoneInfo("America/Mexico_City")).isoformat(),
        "universe_design_only": universe,
        "cuts": [
            {
                "cut": cut,
                "as_of": CUTS[cut],
                **c["summary"],
                "eligible": c["ranking"]["eligible_companies"],
                "substitutions": len(c["ranking"]["comparison"]["entered_graph"]),
                "coverage": c["coverage"],
                "input_sha256": c["ranking"]["visible_input_sha256"],
            }
            for cut, c in contexts.items()
        ],
        "cafe": demonstration,
        "finance": [
            {
                k: r[k]
                for k in (
                    "scenario",
                    "scope",
                    "slots",
                    "activation_rate_increment",
                    "contract_margin_per_activation_mxn",
                    "net_present_value_mxn",
                    "reserve_mxn",
                    "net_after_reserve_mxn",
                    "break_even",
                )
            }
            for r in finance["results"]
        ],
    }
    dump(OUT / "results/summary.json", summary)
    paths = [
        *ROOT.glob("src/economic_graph/*.py"),
        *ROOT.glob("tests/*.py"),
        ROOT / "app/control_tower.py",
        ROOT / "config/financial_assumptions.json",
        ledger,
        *ROOT.glob("docs/*.md"),
        ROOT / "src/economic_graph/simulator/project.py",
        ROOT / "src/economic_graph/simulator/design.py",
    ]
    manifest = []
    symbols = {}
    for path in paths:
        rel = str(path.relative_to(ROOT))
        dest = OUT / "source" / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        content = path.read_bytes()
        manifest.append(
            {"path": rel, "sha256": hashlib.sha256(content).hexdigest(), "source_commit": commit}
        )
        if path.suffix == ".py":
            for node in ast.walk(ast.parse(content)):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    symbols[f"{rel}:{node.name}"] = {
                        "path": rel,
                        "start": node.lineno,
                        "end": node.end_lineno,
                    }
    dump(OUT / "source/manifest.json", manifest)
    dump(OUT / "source/symbols.json", symbols)
    print(
        json.dumps(
            {
                "cuts": summary["cuts"],
                "cafe": original,
                "universe": universe,
                "financial_results": summary["finance"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
