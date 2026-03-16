from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .session import run_demo_session


def load_scenarios(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def design_report(pack: dict[str, Any]) -> dict[str, Any]:
    """Validate scenario design and emit a lab dry-run plan (no live carrier)."""
    limits = pack["limits"]
    soft = limits["lab_soft_cap_n"]
    hard = limits["lab_hard_cap_n"]
    rows = []
    errors = []
    for sc in pack["scenarios"]:
        n = sc["simultaneous_calls"]
        scripts = sc.get("script_rotation") or []
        ok = True
        notes = []
        if n < 2:
            ok = False
            notes.append("N must be >= 2")
            errors.append(f"{sc['id']}: N < 2")
        if n > hard:
            ok = False
            notes.append(f"N={n} exceeds lab_hard_cap_n={hard}")
            errors.append(f"{sc['id']}: exceeds hard cap")
        if sc["id"] == "LOAD-N" and n != soft:
            notes.append(f"LOAD-N uses designed N={n}; soft_cap={soft}")
        if len(scripts) < n:
            notes.append("script_rotation shorter than N; will wrap")
        # Dry-run: clone session lifecycle per leg (design evidence only)
        legs = []
        for i in range(n):
            sid = scripts[i % len(scripts)] if scripts else f"LEG-{i+1}"
            events = run_demo_session()
            legs.append(
                {
                    "leg": i + 1,
                    "script_id": sid,
                    "stagger_ms": sc["stagger_ms"] * i,
                    "lifecycle_states": [e["state"] for e in events],
                }
            )
        rows.append(
            {
                "id": sc["id"],
                "simultaneous_calls": n,
                "stagger_ms": sc["stagger_ms"],
                "intent": sc["intent"],
                "u3_focus": sc["u3_focus"],
                "design_ok": ok,
                "notes": notes,
                "dry_run_legs": legs,
            }
        )
    required_ids = {"LOAD-2", "LOAD-3", "LOAD-N"}
    have = {s["id"] for s in pack["scenarios"]}
    if not required_ids.issubset(have):
        errors.append(f"missing required scenarios: {sorted(required_ids - have)}")
    return {
        "card": "WP-42",
        "label": "Executed",
        "uncertainty": "U3",
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "method": pack["method"],
        "limits": limits,
        "scenarios": rows,
        "required_scenarios_present": required_ids.issubset(have),
        "design_ok": len(errors) == 0 and required_ids.issubset(have),
        "errors": errors,
    }
