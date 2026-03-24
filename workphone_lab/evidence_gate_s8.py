from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_s8_gate(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def gate_s8(root: Path, gate: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for item in gate["checklist"]:
        path = root / item["path"]
        present = path.exists()
        rows.append(
            {
                "item": item["item"],
                "status": "Present" if present else "Missing",
                "location": item["path"],
                "cards": item["cards"],
                "regenerable": item.get("regenerable", False),
            }
        )
    hard_missing = [r for r in rows if r["status"] == "Missing" and not r["regenerable"]]

    limits = gate["limits_statement"]
    # Pull live numbers from exports when present
    bp_path = root / "outputs" / "s8_concurrency_breakpoint.json"
    if bp_path.exists():
        bp = json.loads(bp_path.read_text(encoding="utf-8"))
        limits = {
            **limits,
            "measured_break_point_n": bp.get("break_point_n"),
            "measured_last_ok_n": bp.get("last_ok_n"),
        }

    return {
        "card": "WP-46",
        "sprint": "S8",
        "label": "Executed",
        "uncertainty": "U3",
        "gate_id": gate["gate_id"],
        "version": gate["version"],
        "limits_statement": limits,
        "checklist": rows,
        "rejected_configs": gate["rejected_configs"],
        "summary": {
            "present": sum(1 for r in rows if r["status"] == "Present"),
            "missing": sum(1 for r in rows if r["status"] == "Missing"),
            "hard_missing": len(hard_missing),
            "gate_pass": len(hard_missing) == 0,
            "s8_closed": len(hard_missing) == 0,
            "u3_status": "Partial",
            "u3_note": "Concurrency pack + limits Present on Executed lab; provider channel limit Planned (not Confirmed)",
        },
    }
