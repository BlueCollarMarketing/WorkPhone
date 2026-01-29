from __future__ import annotations

from pathlib import Path
from typing import Any


def gate_s6(root: Path) -> dict[str, Any]:
    import json

    items = [
        ("Intake field map D-04", "data/intake/intake_field_map_v0.json", ["WP-28"]),
        ("Intake schema v0", "data/intake/intake_schema_v0.json", ["WP-32"]),
        ("Negative intake cases pack", "data/intake/negative_intake_cases_v0.json", ["WP-35"]),
        ("Handoff rules email/SMS/CRM", "data/handoff/handoff_rules_v0.json", ["WP-34"]),
        ("Schema validation note", "docs/s6/WP-32-intake-schema-contractor-fields.md", ["WP-32"]),
        ("Required-field enforcement rates", "docs/s6/WP-33-required-field-enforcement-handoffs.md", ["WP-33"]),
        ("Handoff channel rules note", "docs/s6/WP-34-handoff-rules-email-sms-crm.md", ["WP-34"]),
        ("Negative intake safe handling", "docs/s6/WP-35-negative-intake-cases.md", ["WP-35"]),
        ("Handoff enforcement export", "outputs/s6_handoff_enforcement.json", ["WP-33"]),
        ("Negative intake export", "outputs/s6_negative_intake.json", ["WP-35"]),
        ("Schema report export", "outputs/s6_intake_schema_report.json", ["WP-32"]),
    ]
    rows = []
    for name, rel, cards in items:
        path = root / rel
        present = path.exists()
        rows.append(
            {
                "item": name,
                "status": "Present" if present else "Missing",
                "location": rel,
                "cards": cards,
                "regenerable": rel.startswith("outputs/"),
            }
        )
    hard_missing = [r for r in rows if r["status"] == "Missing" and not r["regenerable"]]

    wrong_rate_summary = {
        "source": "WP-33 / WP-35 exports",
        "incomplete_rate_without": None,
        "incomplete_rate_with": None,
        "wrong_rate_with": None,
        "negative_cases_safe": None,
    }
    enf = root / "outputs" / "s6_handoff_enforcement.json"
    if enf.exists():
        agg = json.loads(enf.read_text(encoding="utf-8")).get("aggregate", {})
        wrong_rate_summary["incomplete_rate_without"] = agg.get("incomplete_rate_without")
        wrong_rate_summary["incomplete_rate_with"] = agg.get("incomplete_rate_with")
        wrong_rate_summary["wrong_rate_with"] = agg.get("wrong_rate_with")
    neg = root / "outputs" / "s6_negative_intake.json"
    if neg.exists():
        nagg = json.loads(neg.read_text(encoding="utf-8")).get("aggregate", {})
        wrong_rate_summary["negative_cases_safe"] = f"{nagg.get('pass')}/{nagg.get('n')}"

    return {
        "card": "WP-36",
        "sprint": "S6",
        "label": "Executed",
        "checklist": rows,
        "wrong_rate_summary": wrong_rate_summary,
        "rejected_configs": [
            {
                "id": "RJ-S6-01",
                "config": "Allow handoff without name/phone/service",
                "reason": "Violates WP-INTAKE-SCHEMA required core",
            },
            {
                "id": "RJ-S6-02",
                "config": "Invent address on refuse/partial cases",
                "reason": "Fails WP-35 safe handling",
            },
            {
                "id": "RJ-S6-03",
                "config": "Treat Planned CRM as Executed",
                "reason": "WP-34 Executed path only",
            },
        ],
        "summary": {
            "present": sum(1 for r in rows if r["status"] == "Present"),
            "missing": sum(1 for r in rows if r["status"] == "Missing"),
            "hard_missing": len(hard_missing),
            "gate_pass": len(hard_missing) == 0,
        },
    }
