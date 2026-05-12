from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_m6_gate(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gate_m6(root: Path, gate: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for item in gate["checklist"]:
        path = root / item["path"]
        present = path.exists()
        rows.append(
            {
                "item": item["item"],
                "status": "Present" if present else "Missing",
                "location": item["path"],
                "section": item.get("section", ""),
                "regenerable": item.get("regenerable", False),
            }
        )

    hard_missing = [r for r in rows if r["status"] == "Missing" and not r["regenerable"]]
    soft_missing = [r for r in rows if r["status"] == "Missing" and r["regenerable"]]
    gaps = [
        {
            "id": g["id"],
            "item": g["item"],
            "status": g["status"],
            "label": g["label"],
            "note": g["note"],
            "blocks_gate": False,
        }
        for g in gate.get("explicit_gaps", [])
    ]

    gate_pass = len(hard_missing) == 0
    return {
        "card": "WP-56",
        "sprint": "S10",
        "milestone": gate["milestone"],
        "gate_id": gate["gate_id"],
        "version": gate["version"],
        "gate_tag": gate.get("gate_tag"),
        "label": gate.get("label", "Executed"),
        "rule": gate.get("rule"),
        "checklist": rows,
        "explicit_gaps": gaps,
        "rejected_configs": gate.get("rejected_configs", []),
        "summary": {
            "present": sum(1 for r in rows if r["status"] == "Present"),
            "missing": sum(1 for r in rows if r["status"] == "Missing"),
            "hard_missing": len(hard_missing),
            "soft_missing_regenerable": len(soft_missing),
            "explicit_gaps": len(gaps),
            "gate_pass": gate_pass,
            "s10_closed": gate_pass,
        },
    }
