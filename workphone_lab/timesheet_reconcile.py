from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

INCLUDED_ROLES = {"okunade", "jennifer", "alexandria", "wesley", "timothy"}


def load_reconcile_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def reconcile_timesheet(root: Path, index: dict[str, Any], cfg: dict[str, Any]) -> dict[str, Any]:
    """Final YouTrack/timesheet reconciliation for included roles only."""
    through_card = int(cfg.get("reconcile_through_card", 59))
    targets = index["labour_targets_hours"]
    excluded = set(index.get("excluded_remaps", {}).keys())

    by_role: dict[str, int] = defaultdict(int)
    rows: list[dict[str, Any]] = []
    foreign: list[dict[str, Any]] = []
    gaps: list[dict[str, Any]] = []

    for entry in index["entries"]:
        role = entry["role_key"]
        n = int(entry["card"].split("-")[1])
        if role in excluded or role not in INCLUDED_ROLES:
            foreign.append({"card": entry["card"], "role_key": role, "spent_hours": entry["spent_hours"]})
            gaps.append(
                {
                    "gap_id": f"GAP-ROLE-{entry['card']}",
                    "kind": "excluded_or_foreign_role",
                    "card": entry["card"],
                    "detail": role,
                    "fixed": False,
                }
            )
            continue

        by_role[role] += int(entry["spent_hours"])
        doc = entry.get("evidence_doc")
        exists = bool(doc) and (root / doc).exists()

        if n <= through_card:
            disk_status = "Present" if exists else "Missing"
            if disk_status == "Missing":
                gaps.append(
                    {
                        "gap_id": f"GAP-DOC-{entry['card']}",
                        "kind": "missing_evidence_doc",
                        "card": entry["card"],
                        "detail": doc,
                        "fixed": False,
                    }
                )
        else:
            disk_status = "Planned"

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
        aligned = got == target
        if not aligned:
            gaps.append(
                {
                    "gap_id": f"GAP-HRS-{role}",
                    "kind": "hours_delta",
                    "card": None,
                    "detail": f"yt={got} target={target} delta={got - target}",
                    "fixed": False,
                }
            )
        role_alignment.append(
            {
                "role_key": role,
                "display": index["roles"][role]["display"],
                "email": index["roles"][role]["email"],
                "youtrack_hours": got,
                "labour_target_hours": target,
                "delta_hours": got - target,
                "aligned": aligned,
            }
        )

    hours_aligned = all(r["aligned"] for r in role_alignment)
    roles_only_ok = len(foreign) == 0
    missing_due = [r for r in rows if r["evidence_status"] == "Missing"]
    # Gaps fixed when none remain open
    open_gaps = [g for g in gaps if not g.get("fixed")]
    reconcile_pass = hours_aligned and roles_only_ok and len(missing_due) == 0 and len(open_gaps) == 0

    return {
        "card": "WP-59",
        "sprint": "Close-out",
        "deliverable": "D-09",
        "label": "Executed",
        "reconcile_tag": cfg.get("reconcile_tag", "reconciled@closeout-v0"),
        "index_id": index["index_id"],
        "index_version": index.get("version"),
        "purpose": cfg.get("purpose"),
        "included_roles_only": True,
        "excluded_remaps": index.get("excluded_remaps", {}),
        "reconcile_through_card": through_card,
        "role_alignment": role_alignment,
        "hours_summary": {
            "youtrack_total_hours": sum(by_role.values()),
            "labour_target_total_hours": int(index["labour_total_hours"]),
            "delta_hours": sum(by_role.values()) - int(index["labour_total_hours"]),
            "hours_aligned": hours_aligned,
        },
        "evidence_summary": {
            "cards": len(rows),
            "present": sum(1 for r in rows if r["evidence_status"] == "Present"),
            "planned": sum(1 for r in rows if r["evidence_status"] == "Planned"),
            "missing": len(missing_due),
        },
        "gaps": gaps,
        "gaps_open": len(open_gaps),
        "gaps_fixed": reconcile_pass,
        "foreign_roles": foreign,
        "roles_only_ok": roles_only_ok,
        "entries": rows,
        "rejected_configs": cfg.get("rejected_configs", []),
        "summary": {
            "reconcile_pass": reconcile_pass,
            "hours_aligned": hours_aligned,
            "roles_only_ok": roles_only_ok,
            "ready_for_partner_close": reconcile_pass,
        },
    }
