from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .concurrency_breakpoint import run_at_n
from .handoff_enforce import script_to_intake_attempt
from .negative_intake import run_negative_cases
from .scoring import compare_to_baseline, score_pack


def load_continuity_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_cont_u1(exp: dict[str, Any], clean: dict[str, Any], noise: dict[str, Any]) -> dict[str, Any]:
    clean_report = score_pack(clean)
    noise_report = score_pack(noise)
    cmp = compare_to_baseline(clean_report, noise_report)
    delta = float(cmp["delta_intent_accuracy"])
    ok = delta >= float(exp["expect"]["min_intent_delta"])
    return {
        "id": exp["id"],
        "uncertainty": exp["uncertainty"],
        "name": exp["name"],
        "outcome": "pass" if ok else "fail",
        "expect_met": ok,
        "clean_intent_accuracy": cmp["clean_intent_accuracy"],
        "noise_intent_accuracy": cmp["noise_jargon_intent_accuracy"],
        "delta_intent_accuracy": delta,
        "post_status": exp["expect"]["post_status"],
        "note": "Noise/jargon still degrades intent; U1 remains Partial",
    }


def _run_cont_u2(exp: dict[str, Any], neg: dict[str, Any], clean: dict[str, Any]) -> dict[str, Any]:
    neg_report = run_negative_cases(neg)
    safe = bool(neg_report["aggregate"]["safe_no_fabricate"])
    scripts = {s["id"]: s for s in clean["scripts"]}
    incomplete = scripts.get("SCR-I01")
    invent_free = True
    if incomplete:
        rec = script_to_intake_attempt(incomplete)
        for banned in incomplete.get("omit", []):
            if banned == "address" and "address" in rec:
                invent_free = False
            if banned == "urgency" and "urgency" in rec:
                invent_free = False
    ok = safe == exp["expect"]["safe_no_fabricate"] and invent_free
    return {
        "id": exp["id"],
        "uncertainty": exp["uncertainty"],
        "name": exp["name"],
        "outcome": "pass" if ok else "fail",
        "expect_met": ok,
        "safe_no_fabricate": safe,
        "incomplete_invent_free": invent_free,
        "negative_pass": neg_report["aggregate"]["pass"],
        "negative_n": neg_report["aggregate"]["n"],
        "post_status": exp["expect"]["post_status"],
        "note": "Negative/incomplete intake still safe; U2 remains Partial (wrong-path / live conversion Planned)",
    }


def _run_cont_u3(exp: dict[str, Any]) -> dict[str, Any]:
    safe_n = int(exp["expect"]["safe_n"])
    break_n = int(exp["expect"]["break_point_n"])
    cfg = {
        "lab_capacity_model": {"safe_n": safe_n},
        "search": {"stagger_ms": 150},
        "thresholds": {
            "max_answer_delay_s": 8.0,
            "max_drop_rate": 0.0,
            "stuck_sessions_allowed": 0,
        },
    }
    safe = run_at_n(safe_n, cfg)
    brk = run_at_n(break_n, cfg)
    ok = safe["within_limits"] and not brk["within_limits"]
    return {
        "id": exp["id"],
        "uncertainty": exp["uncertainty"],
        "name": exp["name"],
        "outcome": "pass" if ok else "fail",
        "expect_met": ok,
        "safe_run": {
            "n": safe["n"],
            "within_limits": safe["within_limits"],
            "max_answer_delay_s": safe["max_answer_delay_s"],
            "drop_rate": safe["drop_rate"],
        },
        "break_run": {
            "n": brk["n"],
            "within_limits": brk["within_limits"],
            "max_answer_delay_s": brk["max_answer_delay_s"],
            "drop_rate": brk["drop_rate"],
            "fail_reasons": brk["fail_reasons"],
        },
        "post_status": exp["expect"]["post_status"],
        "note": "U3-LIMITS-v0 continuity holds; provider channel limit still Planned; U3 remains Partial",
    }


def update_board_pointers(board: dict[str, Any], results: list[dict[str, Any]]) -> dict[str, Any]:
    """Update status board with WP-57 continuity pointers; keep Partial unless Confirmed."""
    board = json.loads(json.dumps(board))  # deep copy
    board["updated_card"] = "WP-57"
    board["sprint"] = "Close-out"
    board["continuity_tag"] = "continuity@d10-v0"
    notes_by_u = {r["uncertainty"]: r for r in results}

    for uid in ("U1", "U2", "U3"):
        spec = board["uncertainties"][uid]
        prior = spec["status"]
        exp = notes_by_u.get(uid)
        if not exp:
            continue
        # Only touch Open/Partial remaining items
        if prior not in ("Open", "Partial"):
            continue
        post = exp["post_status"]
        # Never promote to Resolved from continuity alone
        if post == "Resolved":
            post = "Partial"
        spec["status"] = post
        pointer = {
            "card": "WP-57",
            "label": "Executed",
            "note": f"{exp['id']} continuity: {exp['note']}",
        }
        # Avoid duplicate WP-57 pointer
        existing = [p for p in spec.get("evidence_pointers", []) if p.get("card") != "WP-57"]
        existing.append(pointer)
        spec["evidence_pointers"] = existing
        spec["notes"] = (
            f"{prior} -> {post} after continuity {exp['id']}. "
            f"{exp['note']} Not Confirmed closed; not Resolved."
        )
    return board


def run_continuity(
    pack: dict[str, Any],
    *,
    board: dict[str, Any],
    clean_scripts: dict[str, Any],
    noise_scripts: dict[str, Any],
    negative_cases: dict[str, Any],
) -> dict[str, Any]:
    open_items = []
    for uid in ("U1", "U2", "U3"):
        status = board["uncertainties"][uid]["status"]
        if status in ("Open", "Partial"):
            open_items.append({"id": uid, "prior_status": status})

    results = []
    for exp in pack["experiments"]:
        uid = exp["uncertainty"]
        prior = board["uncertainties"][uid]["status"]
        if prior not in exp["expect"]["prior_status_in"]:
            results.append(
                {
                    "id": exp["id"],
                    "uncertainty": uid,
                    "outcome": "skipped",
                    "expect_met": True,
                    "note": f"prior_status={prior} not in scope",
                }
            )
            continue
        if exp["id"] == "CONT-U1":
            row = _run_cont_u1(exp, clean_scripts, noise_scripts)
        elif exp["id"] == "CONT-U2":
            row = _run_cont_u2(exp, negative_cases, clean_scripts)
        elif exp["id"] == "CONT-U3":
            row = _run_cont_u3(exp)
        else:
            row = {
                "id": exp["id"],
                "uncertainty": uid,
                "outcome": "fail",
                "expect_met": False,
                "note": "unknown experiment",
            }
        row["prior_status"] = prior
        results.append(row)

    updated_board = update_board_pointers(board, [r for r in results if r.get("outcome") != "skipped"])
    met = sum(1 for r in results if r.get("expect_met"))
    pack_pass = met == len(results) and all(
        updated_board["uncertainties"][u]["status"] != "Resolved" for u in ("U1", "U2", "U3")
    )

    return {
        "card": pack["card"],
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "sprint": pack["sprint"],
        "deliverable": pack["deliverable"],
        "label": pack["label"],
        "purpose": pack["purpose"],
        "continuity_tag": "continuity@d10-v0",
        "open_items_at_start": open_items,
        "results": results,
        "status_after": {
            u: updated_board["uncertainties"][u]["status"] for u in ("U1", "U2", "U3", "System")
        },
        "rejected_configs": pack.get("rejected_configs", []),
        "updated_board": updated_board,
        "summary": {
            "experiments": len(results),
            "expect_met": met,
            "pack_pass": pack_pass,
        },
    }
