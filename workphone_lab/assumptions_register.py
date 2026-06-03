from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED = {"Validated", "Revised", "Removed"}


def load_assumptions_register(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sweep_assumptions_register(register: dict[str, Any]) -> dict[str, Any]:
    rows = []
    bad = []
    for entry in register["entries"]:
        disp = entry.get("disposition")
        ok = disp in ALLOWED
        if not ok:
            bad.append({"id": entry.get("id"), "disposition": disp})
        rows.append(
            {
                "id": entry["id"],
                "assumption": entry["assumption"],
                "source": entry.get("source"),
                "disposition": disp,
                "evidence": entry.get("evidence", []),
                "note": entry.get("note", ""),
                "sweep_ok": ok,
            }
        )

    counts = {d: sum(1 for r in rows if r["disposition"] == d) for d in sorted(ALLOWED)}
    sweep_pass = len(bad) == 0 and len(rows) > 0 and sum(counts.values()) == len(rows)

    return {
        "card": register.get("card", "WP-58"),
        "register_id": register["register_id"],
        "version": register["version"],
        "sprint": register.get("sprint", "Close-out"),
        "register_tag": register.get("register_tag"),
        "label": register.get("label", "Executed"),
        "purpose": register.get("purpose"),
        "entries": rows,
        "counts": counts,
        "invalid_dispositions": bad,
        "rejected_configs": register.get("rejected_configs", []),
        "summary": {
            "n_entries": len(rows),
            "validated": counts.get("Validated", 0),
            "revised": counts.get("Revised", 0),
            "removed": counts.get("Removed", 0),
            "sweep_pass": sweep_pass,
            "final_register_filed": sweep_pass,
        },
    }
