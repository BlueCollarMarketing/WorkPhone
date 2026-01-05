from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_policy(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def route_utterance(text: str, policy: dict[str, Any]) -> dict[str, Any]:
    t = text.lower()
    paths = policy["paths"]
    # Priority: emergency > estimate > inquiry
    ordered = sorted(paths.items(), key=lambda kv: kv[1]["priority"])
    for name, spec in ordered:
        for trig in spec["triggers"]:
            if trig in t:
                return {
                    "path": name,
                    "route_id": spec["route_id"],
                    "required_fields": spec["required_fields"],
                    "next_step": spec["next_step"],
                    "matched_trigger": trig,
                }
    default = policy.get("default_path", "inquiry")
    spec = paths[default]
    return {
        "path": default,
        "route_id": spec["route_id"],
        "required_fields": spec["required_fields"],
        "next_step": spec["next_step"],
        "matched_trigger": None,
    }


DEMO_UTTERANCES = [
    ("I need an estimate for a roof next week", "estimate"),
    ("There is a gas smell and sparking near the panel", "emergency"),
    ("What are your hours on Saturday?", "inquiry"),
    ("Burst pipe flooding the basement right now", "emergency"),
    ("Can I get a quote for a kitchen reno?", "estimate"),
]


def demo_policy(policy: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for text, expected in DEMO_UTTERANCES:
        routed = route_utterance(text, policy)
        rows.append(
            {
                "utterance": text,
                "expected_path": expected,
                "routed_path": routed["path"],
                "route_id": routed["route_id"],
                "ok": routed["path"] == expected,
                "matched_trigger": routed["matched_trigger"],
            }
        )
    return {
        "card": "WP-27",
        "policy_id": policy["policy_id"],
        "version": policy["version"],
        "aligns_to": policy["aligns_to"],
        "label": "Executed",
        "results": rows,
        "aggregate": {
            "n": len(rows),
            "path_ok": sum(1 for r in rows if r["ok"]),
        },
        "u2_intake_goals": policy["u2_intake_goals"],
    }
