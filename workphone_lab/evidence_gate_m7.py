from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_m7_gate(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gate_m7(root: Path, gate: dict[str, Any]) -> dict[str, Any]:
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
    fy = gate.get("fy_freeze", {})
    return {
        "card": "WP-61",
        "sprint": "Close-out",
        "milestone": gate["milestone"],
        "gate_id": gate["gate_id"],
        "version": gate["version"],
        "gate_tag": gate.get("gate_tag"),
        "period_end": gate.get("period_end"),
        "label": gate.get("label", "Executed"),
        "rule": gate.get("rule"),
        "checklist": rows,
        "explicit_gaps": gaps,
        "fy_freeze": {
            **fy,
            "frozen": gate_pass,
        },
        "rejected_configs": gate.get("rejected_configs", []),
        "summary": {
            "present": sum(1 for r in rows if r["status"] == "Present"),
            "missing": sum(1 for r in rows if r["status"] == "Missing"),
            "hard_missing": len(hard_missing),
            "soft_missing_regenerable": len(soft_missing),
            "explicit_gaps": len(gaps),
            "gate_pass": gate_pass,
            "fy_records_frozen": gate_pass,
            "period_closed": gate_pass,
        },
    }


def apply_fy_freeze_to_board(board: dict[str, Any], gate_tag: str, period_end: str) -> dict[str, Any]:
    board = json.loads(json.dumps(board))
    board["updated_card"] = "WP-61"
    board["sprint"] = "Close-out"
    board["fy_freeze_tag"] = gate_tag
    board["period_end"] = period_end
    board["fy_records_frozen"] = True
    for uid in ("U1", "U2", "U3", "System"):
        spec = board["uncertainties"][uid]
        pointers = [p for p in spec.get("evidence_pointers", []) if p.get("card") != "WP-61"]
        pointers.append(
            {
                "card": "WP-61",
                "label": "Executed",
                "note": f"FY period close {period_end}; records frozen ({gate_tag}); status remains {spec['status']}",
            }
        )
        spec["evidence_pointers"] = pointers
    return board
