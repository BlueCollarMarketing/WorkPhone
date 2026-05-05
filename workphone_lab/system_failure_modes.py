from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_system_fm(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def classify_probe(probe: dict[str, Any], modes_by_id: dict[str, Any]) -> dict[str, Any]:
    mode_id = probe["mode_id"]
    mode = modes_by_id[mode_id]
    obs = probe["observed"]
    defect = False
    detail = ""

    if mode_id == "SYS-DRIFT":
        defect = bool(obs.get("clean_intent_ok")) and not bool(obs.get("noise_intent_ok"))
        detail = (
            f"clean={obs.get('clean_predicted')} noise={obs.get('noise_predicted')} "
            f"unit_passed={obs.get('unit_test_passed')}"
        )
    elif mode_id == "SYS-DROP":
        drop_rate = float(obs.get("drop_rate", 0.0))
        delay = float(obs.get("max_answer_delay_s") or 0.0)
        limit = float(obs.get("max_answer_delay_limit_s", 8.0))
        n = int(obs.get("n", 0))
        safe_n = int(obs.get("safe_n", 0))
        defect = n > safe_n and (drop_rate > 0.0 or delay > limit)
        detail = f"n={n} safe_n={safe_n} drop_rate={drop_rate} max_delay={delay}"
    elif mode_id == "SYS-SUM-INTAKE":
        mismatches = list(obs.get("mismatch_fields") or [])
        if not mismatches:
            # derive from need/number if present
            if obs.get("summary_need") != obs.get("intake_need"):
                mismatches.append("need")
            if obs.get("summary_number") != obs.get("intake_number"):
                mismatches.append("number")
        defect = len(mismatches) > 0
        detail = "mismatch=" + ",".join(mismatches) if mismatches else "aligned"
    elif mode_id == "SYS-FIDELITY-LOAD":
        invent = int(obs.get("invent_count", 0))
        omit = int(obs.get("omit_count", 0))
        collapse = bool(obs.get("collapse_flagged"))
        defect = collapse or invent > 0 or omit > 0
        detail = (
            f"n={obs.get('n')} invent={invent} omit={omit} "
            f"acc={obs.get('field_accuracy')} quiet_unit_pass={obs.get('quiet_unit_summary_pass')}"
        )
    else:
        defect = True
        detail = f"unknown mode {mode_id}"

    # System-only defects must never be scored as pass
    scored_as_pass = False if defect else True
    return {
        "probe_id": probe["probe_id"],
        "mode_id": mode_id,
        "mode_name": mode["name"],
        "severity": mode["severity"],
        "script_id": probe.get("script_id"),
        "linked_evidence": probe.get("linked_evidence", []),
        "defect": defect,
        "scored_as_pass": scored_as_pass,
        "retained_for_d08": defect,
        "invisible_in": mode.get("invisible_in"),
        "d08_link": mode.get("d08_link"),
        "detail": detail,
        "note": probe.get("note"),
    }


def evaluate_system_fm(library: dict[str, Any]) -> dict[str, Any]:
    modes_by_id = {m["id"]: m for m in library["modes"]}
    rows = [classify_probe(p, modes_by_id) for p in library["probes"]]
    defects = [r for r in rows if r["defect"]]
    pass_violations = [r for r in defects if r["scored_as_pass"]]
    rule_ok = len(pass_violations) == 0 and len(defects) == len(rows)
    # All listed probes are known system defects; library complete when each retained
    notes_filed = all(r["retained_for_d08"] for r in rows)
    return {
        "card": library["card"],
        "label": library["label"],
        "library_id": library["library_id"],
        "version": library["version"],
        "sprint": library["sprint"],
        "deliverable": library["deliverable"],
        "purpose": library["purpose"],
        "path": library["path"],
        "why_unit_tests_miss": library["why_unit_tests_miss"],
        "scoring_rule": library["scoring_rule"],
        "modes": library["modes"],
        "n_probes": len(rows),
        "n_defects": len(defects),
        "pass_violations": len(pass_violations),
        "rule_ok": rule_ok,
        "notes_filed_for_d08": notes_filed,
        "results": rows,
        "d08_notes": [
            f"{r['probe_id']} {r['mode_id']}: DEFECT - {r['note']}" for r in rows if r["defect"]
        ],
        "rejected_configs": library.get("rejected_configs", []),
    }
