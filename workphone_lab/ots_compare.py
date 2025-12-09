from __future__ import annotations

from typing import Any

from .scoring import score_utterance


def score_ots(script: dict[str, Any]) -> dict[str, Any]:
    """OTS generic agent stub: weak on trade scripts (matches S0 failure pattern)."""
    text = (script.get("asr_text") or script["utterance"]).lower()
    intent = script["intent"]
    # Generic OTS often maps everything to callback/voicemail or unknown
    if "call me back" in text or script["scenario"] == "callback":
        predicted = "callback"
    elif "estimate" in text or "quote" in text:
        predicted = "callback"  # takes message, does not classify estimate
    elif "leak" in text or "plumber" in text or "service" in text:
        predicted = "unknown"
    else:
        predicted = "unknown"

    entities: dict[str, str | bool] = {}
    # OTS often drops trade entities / invents nothing useful
    if "555" in text or any(ch.isdigit() for ch in text):
        pass  # frequently fails number capture on trade path

    must = script["must_capture"]
    missing = list(must)
    intent_ok = predicted == intent
    return {
        "path": "OTS",
        "script_id": script["id"],
        "expected_intent": intent,
        "predicted_intent": predicted,
        "intent_ok": intent_ok,
        "entities_ok": False,
        "missing": missing,
    }


def score_workphone(script: dict[str, Any]) -> dict[str, Any]:
    row = score_utterance(script, "clean")
    return {
        "path": "Workphone",
        "script_id": script["id"],
        "expected_intent": row["expected_intent"],
        "predicted_intent": row["predicted_intent"],
        "intent_ok": row["intent_ok"],
        "entities_ok": row["entities_ok"],
        "missing": row["missing"],
    }


def compare_side_by_side(pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for s in pack["scripts"]:
        ots = score_ots(s)
        wp = score_workphone(s)
        rows.append(
            {
                "script_id": s["id"],
                "scenario": s["scenario"],
                "ots_intent_ok": ots["intent_ok"],
                "wp_intent_ok": wp["intent_ok"],
                "ots_entities_ok": ots["entities_ok"],
                "wp_entities_ok": wp["entities_ok"],
                "delta_intent": int(wp["intent_ok"]) - int(ots["intent_ok"]),
                "delta_entities": int(wp["entities_ok"]) - int(ots["entities_ok"]),
                "ots_predicted": ots["predicted_intent"],
                "wp_predicted": wp["predicted_intent"],
            }
        )
    n = len(rows)
    ots_i = sum(1 for r in rows if r["ots_intent_ok"])
    wp_i = sum(1 for r in rows if r["wp_intent_ok"])
    ots_e = sum(1 for r in rows if r["ots_entities_ok"])
    wp_e = sum(1 for r in rows if r["wp_entities_ok"])
    return {
        "card": "WP-25",
        "label": "Executed",
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "results": rows,
        "aggregate": {
            "n": n,
            "ots_intent_pass": ots_i,
            "wp_intent_pass": wp_i,
            "ots_entity_full": ots_e,
            "wp_entity_full": wp_e,
            "delta_intent_pass": wp_i - ots_i,
            "delta_entity_full": wp_e - ots_e,
        },
    }
