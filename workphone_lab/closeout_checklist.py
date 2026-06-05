from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_closeout_checklist(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_closeout(root: Path, pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for item in pack["items"]:
        path = root / item["path"]
        present = path.exists()
        rows.append(
            {
                "id": item["id"],
                "criterion": item["criterion"],
                "done_when": item["done_when"],
                "status": "Present" if present else "Missing",
                "location": item["path"],
                "required": item.get("required", True),
            }
        )

    hard_missing = [r for r in rows if r["status"] == "Missing" and r["required"]]

    acceptance_path = pack["partner_acceptance"]
    # Prefer separate acceptance file if present
    accept_file = root / "data" / "closeout" / "partner_acceptance_v0.json"
    if accept_file.exists():
        acceptance = json.loads(accept_file.read_text(encoding="utf-8"))
    else:
        acceptance = acceptance_path

    acceptors = acceptance.get("acceptors", [])
    accepted = [
        a
        for a in acceptors
        if a.get("decision") == "Accepted" and a.get("included_role", True)
    ]
    partner_ok = len(accepted) >= 1 and acceptance.get("span_end") == pack.get("span_end")

    checklist_pass = len(hard_missing) == 0 and partner_ok
    return {
        "card": pack["card"],
        "checklist_id": pack["checklist_id"],
        "version": pack["version"],
        "sprint": pack["sprint"],
        "deliverable": pack["deliverable"],
        "checklist_tag": pack.get("checklist_tag"),
        "span_end": pack.get("span_end"),
        "label": pack.get("label", "Executed"),
        "purpose": pack.get("purpose"),
        "checklist": rows,
        "partner_acceptance": {
            "span_end": acceptance.get("span_end"),
            "statement": acceptance.get("statement"),
            "acceptors": acceptors,
            "accepted_count": len(accepted),
            "partner_ok": partner_ok,
            "notes": acceptance.get("notes", []),
        },
        "rejected_configs": pack.get("rejected_configs", []),
        "summary": {
            "present": sum(1 for r in rows if r["status"] == "Present"),
            "missing": sum(1 for r in rows if r["status"] == "Missing"),
            "hard_missing": len(hard_missing),
            "partner_ok": partner_ok,
            "checklist_pass": checklist_pass,
            "d11_complete": checklist_pass,
        },
    }
