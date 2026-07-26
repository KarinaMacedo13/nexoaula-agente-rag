from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = "\n".join(p.read_text(encoding="utf-8").lower() for p in (ROOT / "docs/source").glob("*.md"))

REQUIRED = {
    "refund_window_days": ["siete días", "7 días"],
    "refund_max_progress_percent": ["20 %", "20%"],
    "certificate_min_progress_percent": ["80 %", "80%"],
    "certificate_min_grade": ["70 sobre 100", "70/100"],
    "affiliate_commission_percent": ["15 %", "15%"],
    "affiliate_cookie_days": ["30 días"],
    "affiliate_minimum_payout_usd": ["usd 50"],
}

failed = []
for rule, variants in REQUIRED.items():
    if not any(v in TEXT for v in variants):
        failed.append(rule)

if failed:
    raise SystemExit("Reglas no encontradas: " + ", ".join(failed))
print("OK: las reglas maestras están presentes en la documentación.")
