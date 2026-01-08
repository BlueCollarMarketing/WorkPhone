from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .dialogue_policy import load_policy, route_utterance


def expected_path_for_script(script: dict[str, Any]) -> str:
    scenario = script.get("scenario", "")
    intent = script.get("intent", "")
    text = (script.get("asr_text") or script.get("utterance") or "").lower()
    if any(k in text for k in ("gas", "flood", "fire", "sparking", "burst pipe")):
        return "emergency"
    if scenario in ("estimate", "after_hours") or intent == "estimate":
        return "estimate"
    if scenario in ("service", "incomplete") or intent == "service":
        return "estimate"  # repair/service uses estimate-family intake path in v0 policy
    if scenario == "callback" or intent == "callback":
        return "inquiry"
    return "inquiry"


def _field_present(field: str, text: str, script: dict[str, Any]) -> bool:
    t = text.lower()
    if field in ("name", "contact_name"):
        return any(n in t for n in ("jordan", "sam", "my name", "this is")) or "caller" in t
    if field in ("number", "contact_number"):
        return bool(re.search(r"\d{3}", text)) or "five five five" in t or "number" in t
    if field in ("job_type",):
        return any(k in t for k in ("roof", "basement", "reno", "repair", "estimate", "quote", "sink", "plumb"))
    if field in ("site_area",):
        return any(k in t for k in ("scarborough", "basement", "area", "site"))
    if field in ("callback_window", "callback"):
        return any(k in t for k in ("tomorrow", "call me back", "callback", "this week"))
    if field in ("hazard_type",):
        return any(k in t for k in ("gas", "flood", "fire", "spark", "burst"))
    if field in ("urgency",):
        return any(k in t for k in ("urgent", "this week", "tonight", "immediate", "right now"))
    if field in ("inquiry_topic",):
        return any(k in t for k in ("hours", "location", "info", "question"))
    # fallback: listed in must_capture loosely
    return field in script.get("must_capture", [])


def measure_script(script: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    text = script.get("asr_text") or script["utterance"]
    expected = expected_path_for_script(script)
    routed = route_utterance(text, policy)
    wrong_path = routed["path"] != expected
    required = routed["required_fields"]
    present = [f for f in required if _field_present(f, text, script)]
    missing = [f for f in required if f not in present]
    completion = round(len(present) / len(required), 4) if required else 1.0
    return {
        "script_id": script["id"],
        "scenario": script.get("scenario"),
        "expected_path": expected,
        "routed_path": routed["path"],
        "wrong_path": wrong_path,
        "required_fields": required,
        "present_fields": present,
        "missing_fields": missing,
        "completion_rate": completion,
        "complete": len(missing) == 0,
    }


def measure_packs(policy: dict[str, Any], packs: list[dict[str, Any]]) -> dict[str, Any]:
    rows = []
    for pack in packs:
        for s in pack["scripts"]:
            row = measure_script(s, policy)
            row["pack_id"] = pack["pack_id"]
            row["pack_version"] = pack["version"]
            rows.append(row)
    n = len(rows)
    wrong = sum(1 for r in rows if r["wrong_path"])
    complete = sum(1 for r in rows if r["complete"])
    avg_completion = round(sum(r["completion_rate"] for r in rows) / n, 4) if n else 0.0
    return {
        "card": "WP-29",
        "label": "Executed",
        "policy_id": policy["policy_id"],
        "policy_version": policy["version"],
        "aligns_to": "U2",
        "results": rows,
        "aggregate": {
            "n": n,
            "wrong_path_count": wrong,
            "wrong_path_rate": round(wrong / n, 4) if n else 0.0,
            "complete_count": complete,
            "completion_rate_mean": avg_completion,
            "fully_complete_rate": round(complete / n, 4) if n else 0.0,
        },
    }
