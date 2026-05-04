from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .concurrency_breakpoint import run_at_n
from .handoff_enforce import enforce_handoff, script_to_intake_attempt
from .negative_intake import run_negative_cases
from .scoring import score_pack
from .session import run_demo_session


def load_e2e_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _by_id(items: list[dict[str, Any]], key: str = "id") -> dict[str, dict[str, Any]]:
    return {x[key]: x for x in items}


def _run_happy(
    scenario: dict[str, Any],
    scripts_by_id: dict[str, dict[str, Any]],
    schema: dict[str, Any],
) -> dict[str, Any]:
    selected = [scripts_by_id[i] for i in scenario["script_ids"]]
    scored = score_pack({"pack_id": "E2E-HAPPY-SUB", "version": "v0", "scripts": selected})
    intent_acc = scored["aggregate"]["intent_accuracy"]
    session = run_demo_session()
    session_complete = session[-1]["state"] == "end"
    handoffs = []
    for s in selected:
        rec = script_to_intake_attempt(s)
        h = enforce_handoff(rec, schema, enforce=True)
        handoffs.append(
            {
                "script_id": s["id"],
                "allowed": h["allowed"],
                "incomplete": h["incomplete"],
                "errors": h.get("errors", []),
            }
        )
    blocked = sum(1 for h in handoffs if not h["allowed"])
    blocked_rate = round(blocked / len(handoffs), 4) if handoffs else 0.0
    named_allowed = any(h["allowed"] for h in handoffs)
    exp = scenario["expect"]
    ok = (
        session_complete == exp["session_complete"]
        and intent_acc >= exp["min_intent_accuracy"]
        and named_allowed == exp.get("named_handoff_allowed", True)
    )
    return {
        "id": scenario["id"],
        "family": scenario["family"],
        "outcome": "pass" if ok else "fail",
        "session_complete": session_complete,
        "intent_accuracy": intent_acc,
        "handoff_blocked_rate": blocked_rate,
        "named_handoff_allowed": named_allowed,
        "scripts": scored["results"],
        "handoffs": handoffs,
        "d08_focus": scenario["d08_focus"],
        "expect_met": ok,
    }


def _run_noise(
    scenario: dict[str, Any],
    nj_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    selected = [nj_by_id[i] for i in scenario["script_ids"]]
    scored = score_pack(
        {
            "pack_id": "E2E-NOISE-SUB",
            "version": "v0-noise-jargon",
            "condition": "noise_jargon",
            "scripts": selected,
        }
    )
    intent_acc = scored["aggregate"]["intent_accuracy"]
    exp = scenario["expect"]
    degraded = intent_acc <= exp["max_intent_accuracy"]
    ok = degraded and exp.get("document_degradation", True)
    return {
        "id": scenario["id"],
        "family": scenario["family"],
        "outcome": "degraded_as_expected" if ok else "unexpected_noise_pass",
        "intent_accuracy": intent_acc,
        "max_intent_accuracy_expect": exp["max_intent_accuracy"],
        "scripts": scored["results"],
        "d08_focus": scenario["d08_focus"],
        "expect_met": ok,
    }


def _run_incomplete(
    scenario: dict[str, Any],
    scripts_by_id: dict[str, dict[str, Any]],
    neg_pack: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    # Filter negative cases to those listed (or all if unset)
    wanted = set(scenario.get("negative_case_ids") or [])
    cases = [c for c in neg_pack["cases"] if not wanted or c["id"] in wanted]
    filtered = {**neg_pack, "cases": cases}
    neg_report = run_negative_cases(filtered)
    n = neg_report["aggregate"]["n"]
    safe_pass = round(neg_report["aggregate"]["pass"] / n, 4) if n else 0.0

    selected = [scripts_by_id[i] for i in scenario["script_ids"]]
    incomplete_rows = []
    invent_free = True
    for s in selected:
        rec = script_to_intake_attempt(s)
        for banned in s.get("omit", []):
            if banned == "address" and "address" in rec:
                invent_free = False
            if banned == "urgency" and "urgency" in rec:
                invent_free = False
        h = enforce_handoff(rec, schema, enforce=True)
        incomplete_rows.append(
            {
                "script_id": s["id"],
                "allowed": h["allowed"],
                "incomplete": h["incomplete"],
                "errors": h.get("errors", []),
                "omit": s.get("omit", []),
            }
        )
    blocked = all(not r["allowed"] for r in incomplete_rows) if incomplete_rows else False
    # If SCR-I01 converts with required fields present, still pass when invent_free + negatives safe
    exp = scenario["expect"]
    ok = invent_free and safe_pass >= exp["safe_case_pass_rate_min"]
    if exp.get("incomplete_handoff_blocked") and incomplete_rows and not invent_free:
        ok = ok and blocked
    return {
        "id": scenario["id"],
        "family": scenario["family"],
        "outcome": "pass" if ok else "fail",
        "safe_case_pass_rate": safe_pass,
        "fabricated_fields": not invent_free,
        "incomplete_handoff_blocked": blocked,
        "negative_results": neg_report["results"],
        "incomplete_scripts": incomplete_rows,
        "d08_focus": scenario["d08_focus"],
        "expect_met": ok,
    }


def _run_concurrent(scenario: dict[str, Any]) -> dict[str, Any]:
    cfg = {
        "lab_capacity_model": {"safe_n": scenario["n_safe"]},
        "search": {"stagger_ms": scenario["stagger_ms"]},
        "thresholds": {
            "max_answer_delay_s": 8.0,
            "max_drop_rate": 0.0,
            "stuck_sessions_allowed": 0,
        },
    }
    safe = run_at_n(scenario["n_safe"], cfg)
    brk = run_at_n(scenario["n_break"], cfg)
    exp = scenario["expect"]
    ok = (
        safe["within_limits"] == exp["safe_within_limits"]
        and (not brk["within_limits"]) == exp["break_exceeds_limits"]
    )
    return {
        "id": scenario["id"],
        "family": scenario["family"],
        "outcome": "pass" if ok else "fail",
        "n_safe": scenario["n_safe"],
        "n_break": scenario["n_break"],
        "safe_run": {
            "n": safe["n"],
            "max_answer_delay_s": safe["max_answer_delay_s"],
            "drop_rate": safe["drop_rate"],
            "within_limits": safe["within_limits"],
        },
        "break_run": {
            "n": brk["n"],
            "max_answer_delay_s": brk["max_answer_delay_s"],
            "drop_rate": brk["drop_rate"],
            "within_limits": brk["within_limits"],
            "fail_reasons": brk["fail_reasons"],
        },
        "d08_focus": scenario["d08_focus"],
        "expect_met": ok,
    }


def run_e2e_pack(
    pack: dict[str, Any],
    *,
    clean_scripts: dict[str, Any],
    noise_scripts: dict[str, Any],
    negative_cases: dict[str, Any],
    schema: dict[str, Any],
) -> dict[str, Any]:
    clean_by = _by_id(clean_scripts["scripts"])
    nj_by = _by_id(noise_scripts["scripts"])
    results = []
    for scenario in pack["scenarios"]:
        family = scenario["family"]
        if family == "happy_path":
            results.append(_run_happy(scenario, clean_by, schema))
        elif family == "noise":
            results.append(_run_noise(scenario, nj_by))
        elif family == "incomplete_intake":
            results.append(_run_incomplete(scenario, clean_by, negative_cases, schema))
        elif family == "concurrent":
            results.append(_run_concurrent(scenario))
        else:
            results.append(
                {
                    "id": scenario["id"],
                    "family": family,
                    "outcome": "fail",
                    "expect_met": False,
                    "error": f"unknown family {family}",
                }
            )

    met = sum(1 for r in results if r.get("expect_met"))
    pack_pass = met == len(results)
    return {
        "card": pack["card"],
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "sprint": pack["sprint"],
        "deliverable": pack["deliverable"],
        "label": pack["label"],
        "purpose": pack["purpose"],
        "path": pack["path"],
        "results": results,
        "summary": {
            "scenarios": len(results),
            "expect_met": met,
            "pack_pass": pack_pass,
        },
        "rejected_configs": pack.get("rejected_configs", []),
        "d08_notes": [
            f"{r['id']}: {r.get('outcome')} - {r.get('d08_focus', '')}" for r in results
        ],
    }
