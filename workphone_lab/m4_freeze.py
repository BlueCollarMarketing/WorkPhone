from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_m4_freeze(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check_path(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    return {
        "location": rel,
        "status": "Present" if path.exists() else "Missing",
        "exists": path.exists(),
    }


def evaluate_m4_freeze(root: Path, gate: dict[str, Any]) -> dict[str, Any]:
    checklist: list[dict[str, Any]] = []

    for section in ("intake", "summary", "linked_gates"):
        for item in gate["frozen_core_path"][section]:
            row = _check_path(root, item["path"])
            row.update(
                {
                    "section": section,
                    "item": f"{item['id']} @ {item['version']}",
                    "id": item["id"],
                    "version": item["version"],
                    "deliverable": item.get("deliverable"),
                    "milestone": item.get("milestone"),
                }
            )
            checklist.append(row)

    for doc in gate["evidence_docs"]:
        row = _check_path(root, doc["path"])
        row.update(
            {
                "section": "evidence_docs",
                "item": doc["item"],
                "id": doc["item"],
            }
        )
        checklist.append(row)

    gaps = []
    for g in gate["explicit_gaps"]:
        gaps.append(
            {
                "id": g["id"],
                "item": g["item"],
                "status": g["status"],
                "label": g["label"],
                "note": g["note"],
                "blocks_freeze": False,
            }
        )

    hard_missing = [r for r in checklist if r["status"] == "Missing"]
    freeze_pass = len(hard_missing) == 0
    return {
        "card": "WP-41",
        "sprint": "S7",
        "milestone": gate["milestone"],
        "gate_id": gate["gate_id"],
        "version": gate["version"],
        "freeze_tag": gate["freeze_tag"],
        "label": "Executed",
        "rule": gate["rule"],
        "checklist": checklist,
        "explicit_gaps": gaps,
        "rejected_configs": gate["rejected_configs"],
        "summary": {
            "present": sum(1 for r in checklist if r["status"] == "Present"),
            "missing": len(hard_missing),
            "explicit_gaps": len(gaps),
            "freeze_pass": freeze_pass,
            "s7_closed": freeze_pass,
        },
    }
