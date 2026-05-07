from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


INCLUDED_ROLES = {"okunade", "jennifer", "alexandria", "wesley", "timothy"}


def load_evidence_index(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def align_evidence_index(root: Path, pack: dict[str, Any]) -> dict[str, Any]:
    targets = pack["labour_targets_hours"]
    included = set(pack.get("roles", {}).keys()) | INCLUDED_ROLES
    excluded_keys = set(pack.get("excluded_remaps", {}).keys())

    by_role: dict[str, int] = defaultdict(int)
    foreign_roles: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []

    for entry in pack["entries"]:
        role = entry["role_key"]
        if role in excluded_keys or role not in included:
            foreign_roles.append(
                {
                    "card": entry["card"],
                    "role_key": role,
                    "spent_hours": entry["spent_hours"],
                }
            )
            continue
        by_role[role] += int(entry["spent_hours"])
        doc = entry.get("evidence_doc")
        exists = bool(doc) and (root / doc).exists()
        status = entry.get("evidence_status", "Planned")
        n = int(entry["card"].split("-")[1])
        if status == "Planned" or n > 55:
            disk_status = "Planned" if n > 55 else ("Present" if exists else status)
        elif exists:
            disk_status = "Present"
        else:
            disk_status = "Missing"
        rows.append(
            {
                "card": entry["card"],
                "role_key": role,
                "assignee": entry["assignee"],
                "spent_hours": entry["spent_hours"],
                "date": entry["date"],
                "sprint": entry["sprint"],
                "evidence_doc": doc,
                "evidence_status": disk_status,
                "summary": entry["summary"],
            }
        )

    role_alignment = []
    for role, target in targets.items():
        got = by_role.get(role, 0)
        role_alignment.append(
            {
                "role_key": role,
                "display": pack["roles"][role]["display"],
                "youtrack_hours": got,
                "labour_target_hours": target,
                "delta_hours": got - target,
                "aligned": got == target,
            }
        )

    hours_aligned = all(r["aligned"] for r in role_alignment)
    total_yt = sum(by_role.values())
    total_target = int(pack["labour_total_hours"])

    present = [r for r in rows if r["evidence_status"] == "Present"]
    planned = [r for r in rows if r["evidence_status"] == "Planned"]
    missing = [r for r in rows if r["evidence_status"] == "Missing"]

    # Through WP-55: no Missing allowed among cards <= 55; Planned OK for WP-56+
    missing_due = [r for r in missing if int(r["card"].split("-")[1]) <= 55]
    roles_only_ok = len(foreign_roles) == 0
    index_pass = hours_aligned and roles_only_ok and len(missing_due) == 0

    return {
        "card": "WP-55",
        "index_id": pack["index_id"],
        "version": pack["version"],
        "sprint": pack["sprint"],
        "deliverable": pack["deliverable"],
        "label": pack["label"],
        "purpose": pack["purpose"],
        "included_roles_only": True,
        "excluded_remaps": pack.get("excluded_remaps", {}),
        "role_alignment": role_alignment,
        "hours_summary": {
            "youtrack_total_hours": total_yt,
            "labour_target_total_hours": total_target,
            "delta_hours": total_yt - total_target,
            "hours_aligned": hours_aligned,
        },
        "evidence_summary": {
            "cards": len(rows),
            "present": len(present),
            "planned": len(planned),
            "missing": len(missing),
            "missing_through_wp55": len(missing_due),
        },
        "foreign_roles": foreign_roles,
        "roles_only_ok": roles_only_ok,
        "entries": rows,
        "rejected_configs": pack.get("rejected_configs", []),
        "summary": {
            "index_pass": index_pass,
            "hours_aligned": hours_aligned,
            "roles_only_ok": roles_only_ok,
            "missing_through_wp55": len(missing_due),
        },
    }
