from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .intake_schema import PHONE_RE, load_schema, validate_record
from .measure_policy import expected_path_for_script


def script_to_intake_attempt(script: dict[str, Any]) -> dict[str, Any]:
    """Build a partial intake record from script text (lab ASR/utterance)."""
    text = script.get("asr_text") or script["utterance"]
    t = text.lower()
    record: dict[str, Any] = {"notes": text[:120]}

    if "jordan" in t:
        record["name"] = "Jordan"
    elif "sam" in t:
        record["name"] = "Sam"

    m = re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", text)
    if m:
        record["phone"] = m.group(0)
    elif "five five five" in t:
        # spoken digits under noise - often incomplete handoff
        pass

    scenario = script.get("scenario", "")
    intent = script.get("intent", "")
    if intent == "estimate" or scenario in ("estimate", "after_hours"):
        record["service"] = {"service_type": "estimate", "job_type": "trade_job"}
    elif intent == "service" or scenario in ("service", "incomplete"):
        record["service"] = {"service_type": "repair", "job_type": "repair"}
    elif intent == "callback" or scenario == "callback":
        record["service"] = {"service_type": "inquiry", "inquiry_topic": "callback"}

    if "this week" in t:
        record["urgency"] = {"urgency_level": "this_week"}
    if "scarborough" in t or "basement" in t:
        record.setdefault("location_window", {})["site_area"] = "area"
    if "tomorrow" in t or "call me back" in t:
        record.setdefault("location_window", {})["callback_window"] = "callback"

    return record


def enforce_handoff(record: dict[str, Any], schema: dict[str, Any], *, enforce: bool) -> dict[str, Any]:
    """If enforce=True, block incomplete handoffs; else allow (legacy)."""
    check = validate_record(record, schema)
    if not enforce:
        return {
            "allowed": True,
            "enforced": False,
            "incomplete": not check["ok"],
            "wrong": False,
            "errors": check["errors"],
            "conversion_kept": True,
        }
    allowed = check["ok"]
    return {
        "allowed": allowed,
        "enforced": True,
        "incomplete": not allowed,
        "wrong": False,
        "errors": check["errors"],
        "conversion_kept": allowed,  # allowed handoffs remain convertible
    }


def measure_enforcement(packs: list[dict[str, Any]], schema: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for pack in packs:
        for s in pack["scripts"]:
            attempt = script_to_intake_attempt(s)
            off = enforce_handoff(attempt, schema, enforce=False)
            on = enforce_handoff(attempt, schema, enforce=True)
            rows.append(
                {
                    "script_id": s["id"],
                    "pack_id": pack["pack_id"],
                    "attempt_fields": list(attempt.keys()),
                    "without_enforcement": off,
                    "with_enforcement": on,
                    "incomplete_reduced": off["incomplete"] and not on["allowed"],
                    "conversion_killed": off["conversion_kept"] and not on["conversion_kept"] and off["incomplete"] is False,
                }
            )

    n = len(rows)
    # Incomplete that still get handed off (the failure mode we want to reduce)
    passed_incomplete_without = sum(
        1 for r in rows if r["without_enforcement"]["allowed"] and r["without_enforcement"]["incomplete"]
    )
    passed_incomplete_with = sum(
        1 for r in rows if r["with_enforcement"]["allowed"] and r["with_enforcement"]["incomplete"]
    )
    allowed_with = sum(1 for r in rows if r["with_enforcement"]["allowed"])
    wrong_with = sum(1 for r in rows if r["with_enforcement"]["allowed"] and r["with_enforcement"]["wrong"])

    return {
        "card": "WP-33",
        "label": "Executed",
        "hypothesis": "Required-field enforcement reduces incomplete handoffs without killing conversion",
        "schema_id": schema["schema_id"],
        "schema_version": schema["version"],
        "results": rows,
        "aggregate": {
            "n": n,
            "incomplete_handoffs_without": passed_incomplete_without,
            "incomplete_handoffs_with": passed_incomplete_with,
            "incomplete_rate_without": round(passed_incomplete_without / n, 4),
            "incomplete_rate_with": round(passed_incomplete_with / n, 4),
            "incomplete_delta": round((passed_incomplete_without - passed_incomplete_with) / n, 4),
            "allowed_conversion_rate_with": round(allowed_with / n, 4),
            "wrong_rate_with": round(wrong_with / n, 4) if n else 0.0,
            "hypothesis_supported": passed_incomplete_with < passed_incomplete_without and allowed_with > 0,
        },
    }
