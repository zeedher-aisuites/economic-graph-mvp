"""Regresión de UTF-8 para los speeches financieros generados."""

import json
from pathlib import Path

from content import FINANCE_STORY_SPEECHES

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ROOT / "presentation-showcase/scripts/content.py",
    ROOT / "presentation-showcase/data.js",
    ROOT / "presentation-showcase/docs/guion.md",
    ROOT / "presentation-showcase/docs/guia-estudio.html",
    ROOT / "presentation-showcase/evidence/iteration-3/data/contextual-evidence.json",
]
BAD = ("Ã", "Â", "â")
EXPECTED = ("podría", "establecí", "inversión", "implementación", "operación", "económicamente")


def main():
    speeches = "\n".join(FINANCE_STORY_SPEECHES)
    assert all(word in speeches for word in EXPECTED)
    for path in FILES[1:]:
        text = path.read_text(encoding="utf-8")
        assert all(word in text for word in EXPECTED), f"Speech incompleto en {path}"
        assert "podrÃ­a" not in text and "inversiÃ³n" not in text, f"Mojibake en speech de {path}"
    source = FILES[0].read_text(encoding="utf-8")
    assert r"podr\u00eda" in source and r"inversi\u00f3n" in source
    payload = json.loads(
        (
            ROOT / "presentation-showcase/evidence/iteration-3/data/contextual-evidence.json"
        ).read_text(encoding="utf-8")
    )
    generated = "\n".join(payload["financeStorySpeeches"])
    assert generated == speeches
    assert all(word in generated for word in EXPECTED)
    print("UTF-8 finance speeches: PASS")


if __name__ == "__main__":
    main()
