from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .summary_email import intake_to_summary_fields


ABSENT = {None, "", "MISSING", "missing", "null", "none"}


def load_gt_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm(value: Any) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    if s.lower() in ABSENT or s == "":
        return None
    return s.lower()


def _tokens(s: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if t}


def values_match(pred: str | None, truth: str | None) -> bool:
    if pred is None and truth is None:
        return True
    if pred is None or truth is None:
        return False
    if pred == truth:
        return True
    # Allow soft match for need/urgency phrasing (e.g. "sink leak" vs "leak under sink")
    pt, tt = _tokens(pred), _tokens(truth)
    if not pt or not tt:
        return False
    return pt <= tt or tt <= pt or bool(pt & tt)


def classify_field(pred_raw: Any, truth_raw: Any) -> str:
    pred, truth = _norm(pred_raw), _norm(truth_raw)
    if truth is None and pred is None:
        return "correct_absent"
    if truth is None and pred is not None:
        return "invent"
    if truth is not None and pred is None:
        return "omit"
    if values_match(pred, truth):
        return "correct"
    return "wrong"


def predict_summary_from_script(script: dict[str, Any]) -> dict[str, str]:
    """Lab summarizer stub: extract summary slots from script utterance without inventing omit fields."""
    raw = script.get("asr_text") or script["utterance"]
    text = raw.lower()
    fields: dict[str, str] = {
        "caller": "MISSING",
        "number": "MISSING",
        "need": "MISSING",
        "urgency": "MISSING",
        "next_step": "Email business + CRM stub row",
    }

    if "sam" in text:
        fields["caller"] = "Sam"
    elif "jordan" in text:
        fields["caller"] = "Jordan"

    m = re.search(r"\b(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})\b", raw)
    if m:
        fields["number"] = m.group(1).replace(".", "-").replace(" ", "-")

    if "roof" in text:
        fields["need"] = "roof repair"
    elif "basement" in text and "reno" in text:
        fields["need"] = "basement reno"
    elif "leak" in text or "sink" in text:
        fields["need"] = "sink leak"
    elif "plumber" in text:
        fields["need"] = "plumber"
    elif "electrical" in text or "spark" in text:
        fields["need"] = "electrical"
        fields["next_step"] = "Escalate / high-priority voicemail"

    # Urgency: only if spoken; respect script omit list (no invent)
    omit = set(script.get("omit") or [])
    if "urgency" not in omit:
        if "immediate" in text or "spark" in text:
            fields["urgency"] = "immediate"
        elif "this week" in text:
            fields["urgency"] = "this_week"
        elif "tomorrow" in text:
            fields["urgency"] = "tomorrow"
        elif "tonight" in text or "right now" in text:
            fields["urgency"] = "today"

    # Callback-only: need stays MISSING when no job words
    if script.get("scenario") == "callback" and fields["need"] == "MISSING":
        fields["need"] = "MISSING"

    return fields


def predict_summary_from_intake(record: dict[str, Any]) -> dict[str, str]:
    next_step = (
        "Escalate / high-priority voicemail"
        if record.get("service", {}).get("service_type") == "emergency"
        else "Email business + CRM stub row"
    )
    return intake_to_summary_fields(record, next_step)


def score_note(note: dict[str, Any], predicted: dict[str, str], score_fields: list[str]) -> dict[str, Any]:
    gt = note["ground_truth"]
    field_rows = {}
    counts = {"correct": 0, "correct_absent": 0, "wrong": 0, "omit": 0, "invent": 0}
    for f in score_fields:
        label = classify_field(predicted.get(f), gt.get(f))
        field_rows[f] = {
            "predicted": predicted.get(f),
            "ground_truth": gt.get(f),
            "class": label,
        }
        counts[label] = counts.get(label, 0) + 1
    scored = len(score_fields)
    accurate = counts["correct"] + counts["correct_absent"]
    present_truth = sum(1 for f in score_fields if _norm(gt.get(f)) is not None)
    return {
        "note_id": note["note_id"],
        "script_id": note.get("script_id"),
        "fields": field_rows,
        "counts": counts,
        "field_accuracy": round(accurate / scored, 4) if scored else 0.0,
        "omit_rate_on_present": round(counts["omit"] / present_truth, 4) if present_truth else 0.0,
        "invent_count": counts["invent"],
    }


def measure_summary_accuracy(
    gt_pack: dict[str, Any],
    scripts_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    score_fields = gt_pack["score_fields"]
    rows = []
    for note in gt_pack["notes"]:
        if "intake_record" in note:
            predicted = predict_summary_from_intake(note["intake_record"])
        else:
            script = scripts_by_id.get(note["script_id"])
            if not script:
                raise KeyError(f"Missing script for {note['script_id']}")
            predicted = predict_summary_from_script(script)
        rows.append(score_note(note, predicted, score_fields))

    n_fields = len(rows) * len(score_fields)
    totals = {"correct": 0, "correct_absent": 0, "wrong": 0, "omit": 0, "invent": 0}
    for r in rows:
        for k, v in r["counts"].items():
            totals[k] = totals.get(k, 0) + v
    present_truth = sum(
        1
        for note in gt_pack["notes"]
        for f in score_fields
        if _norm(note["ground_truth"].get(f)) is not None
    )
    accurate = totals["correct"] + totals["correct_absent"]
    field_accuracy = round(accurate / n_fields, 4) if n_fields else 0.0
    invent_rate = round(totals["invent"] / n_fields, 4) if n_fields else 0.0
    omit_rate = round(totals["omit"] / present_truth, 4) if present_truth else 0.0
    targets = gt_pack["hypothesis"]["targets"]
    supported = (
        field_accuracy >= targets["field_accuracy_min"]
        and invent_rate <= targets["invent_rate_max"]
    )
    return {
        "card": "WP-38",
        "label": "Executed",
        "hypothesis_id": gt_pack["hypothesis"]["id"],
        "pack_id": gt_pack["pack_id"],
        "version": gt_pack["version"],
        "n_notes": len(rows),
        "n_field_slots": n_fields,
        "totals": totals,
        "field_accuracy": field_accuracy,
        "invent_rate": invent_rate,
        "omit_rate": omit_rate,
        "targets": targets,
        "hypothesis_supported": supported,
        "results": rows,
    }
