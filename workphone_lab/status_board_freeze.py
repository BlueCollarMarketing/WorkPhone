from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_STATUSES = {"Open", "Partial", "Resolved"}
ALLOWED_LABELS = {"Executed", "Planned", "Confirmed"}


def load_board(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def freeze_status_board(board: dict[str, Any]) -> dict[str, Any]:
    allowed_status = set(board.get("allowed_statuses", ALLOWED_STATUSES))
    allowed_labels = set(board.get("allowed_evidence_labels", ALLOWED_LABELS))
    rows = []
    label_violations = []
    status_violations = []

    for uid, spec in board["uncertainties"].items():
        status = spec["status"]
        if status not in allowed_status:
            status_violations.append({"id": uid, "status": status})
        pointers = spec.get("evidence_pointers", [])
        labels = []
        for p in pointers:
            lab = p.get("label", "Executed")
            labels.append(lab)
            if lab not in allowed_labels:
                label_violations.append({"id": uid, "card": p.get("card"), "label": lab})
        for plan in spec.get("planned_items", []):
            lab = plan.get("label", "Planned")
            if lab not in allowed_labels:
                label_violations.append({"id": uid, "item": plan.get("item"), "label": lab})
        rows.append(
            {
                "id": uid,
                "status": status,
                "evidence_count": len(pointers),
                "labels": sorted(set(labels)),
                "planned_count": len(spec.get("planned_items", [])),
                "notes": spec.get("notes", ""),
                "evidence_pointers": pointers,
                "planned_items": spec.get("planned_items", []),
            }
        )

    # Draft freeze rule: none may be Resolved unless explicitly allowed later;
    # current freeze expects Partial for U1/U2/U3/System (no false Resolved).
    resolved = [r for r in rows if r["status"] == "Resolved"]
    false_resolved = [
        r
        for r in resolved
        if not any(
            p.get("label") == "Confirmed"
            for p in board["uncertainties"][r["id"]].get("evidence_pointers", [])
        )
    ]

    freeze_pass = (
        len(status_violations) == 0
        and len(label_violations) == 0
        and len(false_resolved) == 0
        and all(r["status"] in allowed_status for r in rows)
        and all(r["evidence_count"] > 0 for r in rows)
    )

    return {
        "card": "WP-54",
        "sprint": board.get("sprint", "S10"),
        "board_id": board["board_id"],
        "version": board["version"],
        "freeze_tag": board.get("freeze_tag"),
        "label": board.get("label", "Executed"),
        "rule": board.get("rule"),
        "rows": rows,
        "status_violations": status_violations,
        "label_violations": label_violations,
        "false_resolved": [{"id": r["id"], "status": r["status"]} for r in false_resolved],
        "rejected_configs": board.get("rejected_configs", []),
        "summary": {
            "uncertainties": len(rows),
            "by_status": {
                s: sum(1 for r in rows if r["status"] == s) for s in sorted(allowed_status)
            },
            "freeze_pass": freeze_pass,
        },
    }
