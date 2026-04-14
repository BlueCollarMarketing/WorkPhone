from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_trade_profiles(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _affinity(text: str, keywords: list[str]) -> int:
    t = text.lower()
    return sum(1 for k in keywords if k in t)


def behave(script: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    text = script.get("asr_text") or script["utterance"]
    scenario = script["scenario"]
    path_hint = profile["preferred_path_hints"].get(scenario, f"{profile['trade_primary']}_default")
    affinity = _affinity(text, profile["keywords"])
    # Distinct after-hours behaviour by profile
    if scenario == "after_hours":
        after_hours_action = profile["after_hours_mode"]
    else:
        after_hours_action = "n/a"
    # Trade fit: roofing prefers roof scripts; plumbing prefers sink/plumber
    trade = profile["trade_primary"]
    if trade == "roofing":
        fit = "strong" if any(k in text.lower() for k in ("roof", "flashing")) else (
            "weak" if any(k in text.lower() for k in ("plumb", "sink")) else "neutral"
        )
    else:
        fit = "strong" if any(k in text.lower() for k in ("plumb", "sink", "drain")) else (
            "weak" if "roof" in text.lower() else "neutral"
        )
    return {
        "script_id": script["id"],
        "scenario": scenario,
        "greeting": profile["greeting"],
        "voice_style": profile["voice_style"],
        "path_hint": path_hint,
        "after_hours_action": after_hours_action,
        "keyword_affinity": affinity,
        "trade_fit": fit,
        "services_offered": list(profile["services"]),
    }


def side_by_side(pack: dict[str, Any], scripts: list[dict[str, Any]]) -> dict[str, Any]:
    roof = pack["profiles"]["roofing"]
    plumb = pack["profiles"]["plumbing"]
    rows = []
    distinct_count = 0
    for script in scripts:
        a = behave(script, roof)
        b = behave(script, plumb)
        distinct = (
            a["greeting"] != b["greeting"]
            and a["path_hint"] != b["path_hint"]
            and a["voice_style"] != b["voice_style"]
        )
        # After-hours must also differ in action
        if script["scenario"] == "after_hours":
            distinct = distinct and a["after_hours_action"] != b["after_hours_action"]
        if distinct:
            distinct_count += 1
        # Correctness: each profile uses its own path hints and greeting brand
        roof_ok = (
            "Summit Roofing" in a["greeting"]
            and a["path_hint"].startswith("roof_")
            and (script["scenario"] != "after_hours" or a["after_hours_action"] == "answer")
        )
        plumb_ok = (
            "Harbor Plumbing" in b["greeting"]
            and b["path_hint"].startswith("plumb_")
            and (script["scenario"] != "after_hours" or b["after_hours_action"] == "forward")
        )
        rows.append(
            {
                "script_id": script["id"],
                "scenario": script["scenario"],
                "roofing": a,
                "plumbing": b,
                "behaviours_distinct": distinct,
                "roofing_correct": roof_ok,
                "plumbing_correct": plumb_ok,
                "both_correct": roof_ok and plumb_ok,
            }
        )
    n = len(rows)
    supported = (
        n > 0
        and all(r["both_correct"] for r in rows)
        and all(r["behaviours_distinct"] for r in rows)
        and distinct_count == n
    )
    return {
        "card": "WP-48",
        "label": "Executed",
        "deliverable": pack.get("deliverable", "D-07"),
        "hypothesis_id": pack["hypothesis"]["id"],
        "hypothesis": pack["hypothesis"]["statement"],
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "profiles": {
            "roofing": roof["profile_id"],
            "plumbing": plumb["profile_id"],
        },
        "n_scripts": n,
        "distinct_on_all": distinct_count == n,
        "both_correct_on_all": all(r["both_correct"] for r in rows),
        "hypothesis_supported": supported,
        "side_by_side": rows,
    }
