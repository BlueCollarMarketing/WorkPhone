from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .handoff_enforce import enforce_handoff, script_to_intake_attempt
from .intake_schema import load_schema, validate_record


def load_rules(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def select_channels(record: dict[str, Any], rules: dict[str, Any], *, allowed: bool) -> list[str]:
    if not allowed:
        return []
    service = (record.get("service") or {}).get("service_type", "")
    channels = []
    if service == "emergency":
        channels.extend(["sms", "email", "crm_stub"])
    else:
        channels.extend(["email", "crm_stub"])
    # de-dupe preserve order
    seen = set()
    out = []
    for c in channels:
        if c not in seen and c in rules["channels"]:
            seen.add(c)
            out.append(c)
    return out


def demo_handoff_rules(rules: dict[str, Any], schema: dict[str, Any], packs: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for pack in packs:
        for s in pack["scripts"][:5]:  # sample clean pack head + will pass full clean
            attempt = script_to_intake_attempt(s)
            gate = enforce_handoff(attempt, schema, enforce=True)
            chans = select_channels(attempt, rules, allowed=gate["allowed"])
            rows.append(
                {
                    "script_id": s["id"],
                    "allowed": gate["allowed"],
                    "channels": chans,
                    "path_label": rules["label"],
                }
            )
    # also force one emergency example from schema
    emergency = schema["examples"]["emergency"]
    egate = enforce_handoff(emergency, schema, enforce=True)
    rows.append(
        {
            "script_id": "SCHEMA-EMERGENCY",
            "allowed": egate["allowed"],
            "channels": select_channels(emergency, rules, allowed=egate["allowed"]),
            "path_label": rules["label"],
        }
    )
    return {
        "card": "WP-34",
        "rules_id": rules["rules_id"],
        "version": rules["version"],
        "workstream": rules["workstream"],
        "label": "Executed",
        "path_scope": rules["path_scope"],
        "channels_defined": list(rules["channels"].keys()),
        "results": rows,
        "acceptance_notes": [rules["channels"][c]["acceptance"] for c in rules["channels"]],
    }
