from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .measure_summary import (
    predict_summary_from_intake,
    predict_summary_from_script,
    score_note,
)


def load_fidelity_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _predict_for_note(
    note: dict[str, Any],
    scripts_by_id: dict[str, dict[str, Any]],
    mode: str,
    injections: dict[str, dict[str, str]] | None,
) -> dict[str, str]:
    if "intake_record" in note:
        predicted = predict_summary_from_intake(note["intake_record"])
    else:
        script = scripts_by_id[note["script_id"]]
        predicted = predict_summary_from_script(script)

    if mode == "collapse_probe" and injections:
        inj = injections.get(note["note_id"]) or {}
        for k, v in inj.items():
            predicted[k] = v
    return predicted


def spot_check_fidelity(
    cfg: dict[str, Any],
    gt_pack: dict[str, Any],
    scripts_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    notes_by_id = {n["note_id"]: n for n in gt_pack["notes"]}
    score_fields = gt_pack["score_fields"]
    rows = []
    collapse_flagged = 0

    for check in cfg["spot_checks"]:
        injections = (check.get("collapse") or {}).get("injections")
        note_scores = []
        totals = {"correct": 0, "correct_absent": 0, "wrong": 0, "omit": 0, "invent": 0}
        for nid in check["note_ids"]:
            note = notes_by_id[nid]
            predicted = _predict_for_note(note, scripts_by_id, check["mode"], injections)
            scored = score_note(note, predicted, score_fields)
            note_scores.append(scored)
            for k, v in scored["counts"].items():
                totals[k] = totals.get(k, 0) + v

        n_fields = len(check["note_ids"]) * len(score_fields)
        accurate = totals["correct"] + totals["correct_absent"]
        field_accuracy = round(accurate / n_fields, 4) if n_fields else 0.0
        invent_rate = round(totals["invent"] / n_fields, 4) if n_fields else 0.0
        omit_count = totals["omit"]
        invent_count = totals["invent"]

        # RJ-S8-01: invent/omit never scored as pass
        invent_scored_as_pass = False
        omit_scored_as_pass = False

        silent_collapse = check["mode"] == "collapse_probe" and (
            invent_count > 0 or field_accuracy < cfg["collapse_accuracy_max"]
        )
        if silent_collapse:
            collapse_flagged += 1

        if check["mode"] == "faithful":
            check_pass = (
                field_accuracy >= cfg["baseline_accuracy_min"]
                and invent_count == 0
                and not invent_scored_as_pass
                and not omit_scored_as_pass
            )
        else:
            # collapse probe: card check passes when collapse is FLAGGED (not hidden)
            check_pass = silent_collapse and not invent_scored_as_pass and not omit_scored_as_pass

        rows.append(
            {
                "id": check["id"],
                "load_id": check["load_id"],
                "n": check["n"],
                "mode": check["mode"],
                "field_accuracy": field_accuracy,
                "invent_count": invent_count,
                "omit_count": omit_count,
                "invent_rate": invent_rate,
                "totals": totals,
                "silent_collapse_flagged": silent_collapse,
                "invent_scored_as_pass": invent_scored_as_pass,
                "omit_scored_as_pass": omit_scored_as_pass,
                "check_pass": check_pass,
                "notes": note_scores,
            }
        )

    invent_marked_pass = sum(1 for r in rows if r["invent_count"] > 0 and r["invent_scored_as_pass"])
    omit_marked_pass = sum(1 for r in rows if r["omit_count"] > 0 and r["omit_scored_as_pass"])
    all_ok = all(r["check_pass"] for r in rows)
    rule_ok = invent_marked_pass == 0 and omit_marked_pass == 0
    return {
        "card": "WP-45",
        "label": "Executed",
        "uncertainty": "U3",
        "hypothesis_id": cfg["hypothesis"]["id"],
        "hypothesis": cfg["hypothesis"]["statement"],
        "pack_id": cfg["pack_id"],
        "version": cfg["version"],
        "rules": cfg["rules"],
        "safe_n": cfg["safe_n"],
        "results": rows,
        "collapse_flagged": collapse_flagged,
        "invent_marked_as_pass": invent_marked_pass,
        "omit_marked_as_pass": omit_marked_pass,
        "rule_ok": rule_ok,
        "hypothesis_supported": all_ok and rule_ok,
        "rejected_configs": [
            {
                "id": "RJ-S8-01",
                "config": "Mark invent/omit as pass under concurrent load",
                "reason": "Silent quality collapse must be flagged as defect",
            }
        ],
    }
