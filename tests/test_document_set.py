from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_five_source_documents_exist():
    docs = list((ROOT / "docs/source").glob("0[1-5]_*.md"))
    assert len(docs) == 5


def test_key_rules_are_consistent():
    text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "docs/source").glob("*.md"))
    for value in ["7 días", "20 %", "80 %", "70/100", "15 %", "USD 50"]:
        assert value in text
