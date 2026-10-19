"""Preparar evidencias offline desde el ledger y los módulos originales, sin escribir en ellos."""

import hashlib
import json
from pathlib import Path

from content import FINANCE_STORY_SPEECHES
from economic_graph.contracts import CUTS
from economic_graph.finance import financial_report, load_financial_config
from economic_graph.observable import load_observations
from economic_graph.tower_read_model import build_context, ranking_table, segment_ids

ROOT = Path(__file__).resolve().parents[2]
APP = ROOT / "presentation-showcase"
OUT = APP / "evidence/iteration-3/data"
COMMIT = "774dacd80e6410ca43299f63f19d9744a31929c0"
BASE = "5fb3aaa369043733f5c722eb0cc9eaecfb237ed2"
GROUPS = {
    "hornos": ["OBS-028", "OBS-047", "OBS-075"],
    "panificadora": ["OBS-048", "OBS-076"],
    "carga": ["OBS-053"],
    "confirmed": ["OBS-026", "OBS-063"],
    "context": ["OBS-044", "OBS-037", "OBS-045", "OBS-043", "OBS-072"],
}
REFS = {
    "hornos": [
        "src/economic_graph/observable.py:_attribute",
        "src/economic_graph/observable.py:snapshot",
        "src/economic_graph/rankings.py:_branch_feature",
        "tests/test_rankings.py:test_conflicting_branches_remain_unscored_even_after_confirmation",
        "tests/test_observable.py:test_aliases_stay_candidates_without_using_private_mapping",
    ],
    "leaders": [
        "src/economic_graph/rankings.py:_branch_feature",
        "src/economic_graph/rankings.py:_neighbor_feature",
        "src/economic_graph/rankings.py:compare_rankings",
        "tests/test_rankings.py:test_regression_approved_policy_top_five",
        "tests/test_rankings.py:test_ties_empty_and_insufficient_cohort",
    ],
    "confirmed": [
        "src/economic_graph/rankings.py:_relationship_context",
        "src/economic_graph/rankings.py:_neighbor_feature",
        "tests/test_tower_read_model.py:test_focused_network_only_highlights_approved_feature_evidence",
    ],
    "context": [
        "src/economic_graph/rankings.py:_relationship_context",
        "src/economic_graph/rankings.py:_neighbor_feature",
        "tests/test_rankings.py:test_relationship_states_preserved_not_promoted",
        "tests/test_rankings.py:test_referral_is_context_even_when_confirmed",
    ],
    "ledger": [
        "src/economic_graph/observable.py:load_observations",
        "src/economic_graph/observable.py:visible_observations",
        "app/control_tower.py:main",
        "tests/test_observable.py:test_exact_boundary_and_observed_date_do_not_leak_future",
    ],
    "finance": [
        "src/economic_graph/finance.py:financial_report",
        "src/economic_graph/finance.py:_evaluate",
        "tests/test_finance.py:test_manual_arithmetic_regression_all_scenarios",
        "tests/test_control_tower.py:test_finance_tables_match_module_and_do_not_depend_on_company_filters",
    ],
    "filters": [
        "src/economic_graph/tower_read_model.py:build_context",
        "src/economic_graph/tower_read_model.py:segment_ids",
        "src/economic_graph/tower_read_model.py:ranking_table",
        "tests/test_control_tower.py:test_industry_and_score_filters_preserve_global_rankings",
        "tests/test_tower_read_model.py:test_industry_filters_do_not_refill_funnel_or_rankings",
    ],
}


def build_contextual(source_ref):
    OUT.mkdir(parents=True, exist_ok=True)
    ledger_path = ROOT / "data/observable/observations.json"
    finance_path = ROOT / "config/financial_assumptions.json"
    rows = load_observations(ledger_path)
    context = build_context(rows, CUTS["T2"])
    frozen = json.loads((APP / "evidence/results/context-T2.json").read_text(encoding="utf-8"))
    assert context == frozen, "El contexto nuevo difiere del registro original."
    finance = financial_report(load_financial_config(finance_path), sensitivity=True)
    original_finance = json.loads(
        (APP / "evidence/results/finance.json").read_text(encoding="utf-8")
    )
    assert finance == original_finance, "Las finanzas difieren del registro original."
    public_names = {
        c["company_id"]: c["attributes"]["display_name"]["value"]
        for c in context["view"]["companies"]
    }
    ranked = {c["display_name"]: c for c in context["ranking"]["companies"]}
    cafe = ranked["Café Jacaranda"]
    by_id = {r["observation_id"]: r for r in rows}
    lines = ledger_path.read_text(encoding="utf-8").splitlines()
    records = {}
    claims = {r["relationship_id"]: r for r in context["ranking"]["relationship_context"]}
    for row in rows:
        oid = row["observation_id"]
        line = next(i for i, value in enumerate(lines, 1) if f'"{oid}"' in value)
        record = {"record": row, "line": line, "company": public_names.get(row["subject_id"])}
        if row["subject_type"] == "RELATIONSHIP":
            claim = claims[row["subject_id"]]
            record.update(
                {
                    "from_name": public_names[row["value"]["from_company_id"]],
                    "to_name": public_names[row["value"]["to_company_id"]],
                    "scoring_status": claim["scoring_status"],
                    "cafe_contribution": cafe["features"]["confirmed_neighbors"]["weight"]
                    if claim["scoring_status"] == "CONFIRMED"
                    and row["subject_id"]
                    in {
                        rel
                        for neighbor in cafe["features"]["confirmed_neighbors"]["neighbors"]
                        for rel in neighbor["relationship_ids"]
                    }
                    else 0,
                }
            )
        records[oid] = record
    assert [by_id[x]["verification_status"] for x in GROUPS["hornos"]] == [
        "REPORTED",
        "REPORTED",
        "CONFIRMED",
    ]
    assert sum(records[x]["cafe_contribution"] for x in GROUPS["confirmed"]) == 10
    assert not any(records[x]["cafe_contribution"] for x in GROUPS["context"])
    cafe_industry = next(
        c["attributes"]["sector"]["value"]
        for c in context["view"]["companies"]
        if c["company_id"] == cafe["company_id"]
    )
    filters = {}
    for key, ids in (
        ("global", None),
        ("industry", segment_ids(context, industry=cafe_industry)),
        ("company", segment_ids(context, industry=cafe_industry, company_id=cafe["company_id"])),
    ):
        table = ranking_table(context, ids)
        filters[key] = {
            "rows": table,
            "cafe": next(r for r in table if r["ID"] == cafe["company_id"]),
        }
    files = {}
    for original, target in (
        (ledger_path, "observations.json"),
        (finance_path, "financial_assumptions.json"),
    ):
        raw = original.read_bytes().replace(b"\r\n", b"\n")
        (OUT / target).write_bytes(raw)
        files[target] = {
            "path": original.relative_to(ROOT).as_posix(),
            "url": "evidence/iteration-3/data/" + target,
            "sha256": hashlib.sha256(raw).hexdigest(),
        }
    for name, document in (
        ("context-reproduced.json", context),
        ("finance-reproduced.json", finance),
    ):
        (OUT / name).write_text(
            json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    payload = {
        "sourceCommit": COMMIT,
        "presentationBase": BASE,
        "cut": CUTS["T2"],
        "files": files,
        "ledger": json.loads(ledger_path.read_text(encoding="utf-8")),
        "financialConfig": json.loads(finance_path.read_text(encoding="utf-8")),
        "financeStorySpeeches": FINANCE_STORY_SPEECHES,
        "finance": finance,
        "records": records,
        "groups": GROUPS,
        "names": public_names,
        "companies": {
            key: ranked[name]
            for key, name in (
                ("panificadora", "Panificadora Valle Claro"),
                ("carga", "Carga Urbana del Centro"),
                ("cafe", "Café Jacaranda"),
                ("hornos", "Hornos del Centro"),
                ("papeleria", "Papelería Horizonte"),
            )
        },
        "ties": sorted(
            [
                r
                for r in context["ranking"]["companies"]
                if r["graph_score"] == ranked["Carga Urbana del Centro"]["graph_score"]
            ],
            key=lambda r: r["company_id"],
        ),
        "filters": filters,
        "sources": {key: [source_ref(ref) for ref in refs] for key, refs in REFS.items()},
    }
    for sources in payload["sources"].values():
        for source in sources:
            source_lines = (ROOT / source["path"]).read_text(encoding="utf-8").splitlines()
            source["text"] = "\n".join(source_lines[source["start"] - 1 : source["end"]])
    (OUT / "contextual-evidence.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return payload
