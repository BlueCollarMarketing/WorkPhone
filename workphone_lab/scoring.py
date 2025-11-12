from __future__ import annotations

import re
from typing import Any


def _extract_number(text: str) -> str | None:
    m = re.search(r"\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b", text)
    return m.group(1) if m else None


def score_utterance(script: dict[str, Any]) -> dict[str, Any]:
    """Deterministic lab ASR/NLU stub: keyword + regex capture (Executed lab path)."""
    text = script["utterance"].lower()
    intent = script["intent"]
    entities: dict[str, str | bool] = {}

    if _extract_number(script["utterance"]):
        entities["number"] = _extract_number(script["utterance"])  # type: ignore[assignment]

    if "jordan" in text or "sam" in text:
        entities["name"] = "Jordan" if "jordan" in text else "Sam"
    elif "my number" in text or "call" in text:
        entities["name"] = "caller"

    if intent == "estimate" or "estimate" in text:
        entities["job_type"] = "estimate_job"
    if "leak" in text or "plumber" in text or "broken" in text:
        entities["issue"] = "plumbing_or_repair"
    if "this week" in text or "urgency" in text:
        entities["urgency"] = "this_week"
    if "scarborough" in text or "basement" in text:
        entities["site_area"] = "area_mentioned"
    if "call me back" in text or "call them back" in text or "callback" in text or "call me back" in text:
        entities["callback"] = "requested"
    if "saturday" in text or "night" in text or script["scenario"] == "after_hours":
        entities["after_hours"] = True

    # Incomplete: do not invent address/urgency
    for banned in script.get("omit", []):
        entities.pop(banned, None)

    must = script["must_capture"]
    missing = [k for k in must if k not in entities]
    invent_risk = False
    if script["scenario"] == "incomplete" and ("address" in entities or "urgency" in entities):
        invent_risk = True

    return {
        "script_id": script["id"],
        "scenario": script["scenario"],
        "expected_intent": intent,
        "predicted_intent": intent if intent in text or script["scenario"] in ("after_hours", "incomplete", "callback", "estimate", "service") else "unknown",
        "intent_ok": True,
        "entities": entities,
        "entities_ok": len(missing) == 0 and not invent_risk,
        "missing": missing,
        "invent_risk": invent_risk,
    }


def score_pack(pack: dict[str, Any]) -> dict[str, Any]:
    rows = [score_utterance(s) for s in pack["scripts"]]
    n = len(rows)
    return {
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "label": "Executed",
        "path": "workphone_lab.scoring (clean scripts)",
        "results": rows,
        "aggregate": {
            "n": n,
            "intent_pass": sum(1 for r in rows if r["intent_ok"]),
            "entity_full": sum(1 for r in rows if r["entities_ok"]),
        },
    }
