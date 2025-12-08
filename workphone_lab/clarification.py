from __future__ import annotations

from typing import Any

from .scoring import predict_intent, score_utterance


def _confidence(asr_text: str, predicted: str) -> float:
    t = asr_text.lower()
    if predicted == "unknown":
        return 0.25
    markers = ("noise", "static", "unclear", "...", "clipped", "uh")
    penalty = sum(0.12 for m in markers if m in t)
    base = 0.85 if predicted in t or predicted == "callback" and "back" in t else 0.55
    if "flashing" in t or "rough-in" in t:
        base -= 0.2
    return max(0.1, round(base - penalty, 2))


CLARIFY_PROMPTS = {
    "estimate": "Just to confirm - are you looking for a job estimate or quote?",
    "service": "Just to confirm - do you need a repair or service visit?",
    "callback": "Just to confirm - should we only have someone call you back?",
    "unknown": "Sorry, I missed that. Are you calling about an estimate, a repair, or a callback?",
}


def apply_clarification(script: dict[str, Any], caller_reply: str) -> dict[str, Any]:
    """Simulate one clarification turn when confidence is low."""
    before = score_utterance(script, script.get("condition", "noise_jargon"))
    asr = (script.get("asr_text") or script["utterance"]).lower()
    predicted = before["predicted_intent"]
    conf = _confidence(asr, predicted)
    low = conf < 0.6
    prompt = CLARIFY_PROMPTS.get(predicted, CLARIFY_PROMPTS["unknown"]) if low else None

    after_predicted = predicted
    if low:
        reply = caller_reply.lower()
        after_predicted = predict_intent(reply, script["scenario"])
        if after_predicted == "unknown":
            after_predicted = predict_intent(f"{asr} {reply}", script["scenario"])

    after_ok = after_predicted == script["intent"]
    before_ok = before["intent_ok"]

    if not low:
        outcome = "no_change"
    elif after_ok and not before_ok:
        outcome = "helps"
    elif (not after_ok) and before_ok:
        outcome = "harms"
    elif after_ok == before_ok:
        outcome = "no_change"
    else:
        outcome = "no_change"

    invent = False
    if "address" in caller_reply.lower() and script["scenario"] == "incomplete":
        invent = True
        if outcome == "helps":
            outcome = "harms"

    return {
        "script_id": script["id"],
        "expected_intent": script["intent"],
        "confidence": conf,
        "low_confidence": low,
        "prompt": prompt,
        "caller_reply": caller_reply if low else None,
        "before_intent": predicted,
        "before_ok": before_ok,
        "after_intent": after_predicted if low else predicted,
        "after_ok": after_ok if low else before_ok,
        "outcome": outcome,
        "invent_risk": invent,
    }


# Scripted replies for lab (what caller says after clarify)
DEFAULT_REPLIES = {
    "SCR-E01-NJ": "Yes, I need an estimate please",
    "SCR-S01-NJ": "Yes, a repair service this week",
    "SCR-A01-NJ": "I need an estimate for the basement",
    "SCR-I01-NJ": "I need a plumber service",
    "SCR-C01-NJ": "Just a callback thanks",
    "SCR-E01-J": "Estimate, not a repair",
    "SCR-S01-N": "Service visit please",
}


def run_clarification_pack(pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for s in pack["scripts"]:
        reply = DEFAULT_REPLIES.get(s["id"], "I need help with my job")
        rows.append(apply_clarification(s, reply))
    counts = {"helps": 0, "harms": 0, "no_change": 0}
    for r in rows:
        counts[r["outcome"]] += 1
    return {
        "card": "WP-24",
        "label": "Executed",
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "threshold": 0.6,
        "results": rows,
        "summary": counts,
        "hypothesis": "H-S4-04",
    }
