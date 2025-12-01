from __future__ import annotations

import re
from typing import Any


def _extract_number(text: str) -> str | None:
    m = re.search(r"\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b", text)
    if m:
        return m.group(1)
    # Spoken digits often fail under noise in the lab stub
    return None


def predict_intent(text: str, scenario: str) -> str:
    t = text.lower()
    if "estimate" in t or "quote" in t or "bid" in t:
        return "estimate"
    if "leak" in t or "plumber" in t or "service" in t or "broken" in t:
        return "service"
    if "repair" in t and "roof" in t:
        return "estimate"
    if "repair" in t:
        return "service"
    # Callback-only when no stronger intent words
    if scenario == "callback" or "call me back" in t or "callback" in t or (
        "call them" in t and "back" in t
    ):
        return "callback"
    # Jargon-only / heavy drop -> wrong or unknown
    if "flashing" in t or "rough-in" in t:
        return "service"  # mis-map estimate jargon to service
    if scenario == "after_hours" and "reno" in t and "quote" not in t and "estimate" not in t:
        return "unknown"
    return "unknown"


def score_utterance(script: dict[str, Any], path_label: str = "clean") -> dict[str, Any]:
    """Lab ASR/NLU stub. Uses asr_text when present (noise/jargon condition)."""
    raw = script.get("asr_text") or script["utterance"]
    text = raw.lower()
    intent = script["intent"]
    predicted = predict_intent(text, script["scenario"])
    entities: dict[str, str | bool] = {}

    num = _extract_number(raw)
    if num:
        entities["number"] = num

    if "jordan" in text:
        entities["name"] = "Jordan"
    elif "sam" in text:
        entities["name"] = "Sam"
    elif "my number" in text or "call" in text:
        entities["name"] = "caller"

    if predicted == "estimate" or "estimate" in text or "quote" in text:
        entities["job_type"] = "estimate_job"
    if "leak" in text or "plumber" in text or "broken" in text or "sink" in text:
        entities["issue"] = "plumbing_or_repair"
    if "this week" in text:
        entities["urgency"] = "this_week"
    if "scarborough" in text or "basement" in text:
        entities["site_area"] = "area_mentioned"
    if "call me back" in text or "callback" in text:
        entities["callback"] = "requested"
    if "saturday" in text or "night" in text or script["scenario"] == "after_hours":
        entities["after_hours"] = True

    for banned in script.get("omit", []):
        entities.pop(banned, None)

    must = script["must_capture"]
    missing = [k for k in must if k not in entities]
    invent_risk = False
    if script["scenario"] == "incomplete" and ("address" in entities or "urgency" in entities):
        invent_risk = True

    intent_ok = predicted == intent
    error_class = None
    if not intent_ok:
        if "flashing" in text or "rough-in" in text:
            error_class = "E-Jargon"
        elif num is None and "five five five" in text:
            error_class = "E-Num"
        elif "noise" in text or "static" in text or "unclear" in text:
            error_class = "E-Overlap" if "overlap" in str(script.get("noise", "")) else "E-Omit"
        else:
            error_class = "E-Intent"

    return {
        "script_id": script["id"],
        "base_id": script.get("base_id", script["id"]),
        "scenario": script["scenario"],
        "condition": script.get("condition", path_label),
        "expected_intent": intent,
        "predicted_intent": predicted,
        "intent_ok": intent_ok,
        "entities": entities,
        "entities_ok": len(missing) == 0 and not invent_risk,
        "missing": missing,
        "invent_risk": invent_risk,
        "error_class": error_class,
    }


def score_pack(pack: dict[str, Any], path: str | None = None) -> dict[str, Any]:
    label_path = path or (
        "workphone_lab.scoring (noise/jargon)"
        if pack.get("condition") == "noise_jargon"
        else "workphone_lab.scoring (clean scripts)"
    )
    rows = [score_utterance(s, pack.get("condition", "clean")) for s in pack["scripts"]]
    n = len(rows)
    return {
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "condition": pack.get("condition", "clean"),
        "label": "Executed",
        "path": label_path,
        "results": rows,
        "aggregate": {
            "n": n,
            "intent_pass": sum(1 for r in rows if r["intent_ok"]),
            "entity_full": sum(1 for r in rows if r["entities_ok"]),
            "intent_accuracy": round(sum(1 for r in rows if r["intent_ok"]) / n, 4) if n else 0.0,
        },
    }


def compare_to_baseline(baseline: dict[str, Any], stressed: dict[str, Any]) -> dict[str, Any]:
    b = baseline["aggregate"]
    s = stressed["aggregate"]
    delta_intent = round(b["intent_accuracy"] - s["intent_accuracy"], 4) if "intent_accuracy" in b else round(
        b["intent_pass"] / b["n"] - s["intent_pass"] / s["n"], 4
    )
    if "intent_accuracy" not in b:
        b_acc = b["intent_pass"] / b["n"]
        delta_intent = round(b_acc - s["intent_accuracy"], 4)
    return {
        "hypothesis": "H-S4-01",
        "clean_intent_pass": b["intent_pass"],
        "clean_n": b["n"],
        "clean_intent_accuracy": b.get("intent_accuracy", round(b["intent_pass"] / b["n"], 4)),
        "noise_jargon_intent_pass": s["intent_pass"],
        "noise_jargon_n": s["n"],
        "noise_jargon_intent_accuracy": s["intent_accuracy"],
        "delta_intent_accuracy": delta_intent,
        "clean_entity_full": b["entity_full"],
        "noise_jargon_entity_full": s["entity_full"],
        "hypothesis_supported": delta_intent > 0,
    }
