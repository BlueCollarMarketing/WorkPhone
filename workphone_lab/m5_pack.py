from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_m5_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _check(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    return {
        "location": rel,
        "status": "Present" if path.exists() else "Missing",
        "exists": path.exists(),
    }


def assemble_m5(root: Path, gate: dict[str, Any]) -> dict[str, Any]:
    checklist: list[dict[str, Any]] = []
    for section in ("concurrency", "onboard"):
        for item in gate["pack_artifacts"][section]:
            row = _check(root, item["path"])
            row.update(
                {
                    "section": section,
                    "item": f"{item['id']} @ {item['version']}",
                    "id": item["id"],
                    "version": item["version"],
                    "deliverable": item.get("deliverable"),
                }
            )
            checklist.append(row)
    for doc in gate["evidence_docs"]:
        row = _check(root, doc["path"])
        row.update({"section": "evidence_docs", "item": doc["item"], "id": doc["item"]})
        checklist.append(row)

    hard_missing = [r for r in checklist if r["status"] == "Missing"]
    pack_pass = len(hard_missing) == 0
    return {
        "card": "WP-51",
        "sprint": "S9",
        "milestone": gate["milestone"],
        "gate_id": gate["gate_id"],
        "version": gate["version"],
        "pack_tag": gate["pack_tag"],
        "label": "Executed",
        "rule": gate["rule"],
        "concurrency_limits": gate["concurrency_limits"],
        "onboard_path_e2e": gate["onboard_path_e2e"],
        "checklist": checklist,
        "explicit_gaps": [
            {**g, "blocks_pack": False} for g in gate["explicit_gaps"]
        ],
        "rejected_configs": gate["rejected_configs"],
        "summary": {
            "present": sum(1 for r in checklist if r["status"] == "Present"),
            "missing": len(hard_missing),
            "explicit_gaps": len(gate["explicit_gaps"]),
            "pack_pass": pack_pass,
            "s9_closed": pack_pass,
        },
    }
