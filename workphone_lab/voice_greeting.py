from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_voice_cases(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _voice_catalog(pack: dict[str, Any]) -> dict[str, list[str]]:
    return {v["voice_id"]: list(v["styles"]) for v in pack["allowed_voices"]}


def validate_voice_greeting(case: dict[str, Any], pack: dict[str, Any]) -> dict[str, Any]:
    catalog = _voice_catalog(pack)
    errors: list[str] = []
    voice_id = case.get("voice_id")
    style = case.get("voice_style")
    tmpl = case.get("greeting_template") or ""
    biz = case.get("business_name") or ""

    if voice_id not in catalog:
        errors.append("voice_id not in allowed catalog")
    elif style not in catalog[voice_id]:
        errors.append("voice_style not allowed for voice_id")
    if style not in pack["allowed_styles"]:
        errors.append("voice_style not in allowed_styles")

    resolved = tmpl.replace("{{business_name}}", biz).strip()
    if not resolved:
        errors.append("greeting empty after trim")
    elif biz and biz not in resolved:
        errors.append("greeting missing business_name")
    if "{{" in resolved:
        errors.append("unresolved greeting placeholder")

    accepted = len(errors) == 0
    return {
        "case_id": case["case_id"],
        "profile_id": case.get("profile_id"),
        "voice_id": voice_id,
        "voice_style": style,
        "greeting_resolved": resolved if accepted else None,
        "accepted": accepted,
        "errors": errors,
        "expect": case.get("expect"),
        "expect_matched": (accepted and case.get("expect") == "accept")
        or ((not accepted) and case.get("expect") == "fail"),
    }


def run_voice_greeting_pack(pack: dict[str, Any]) -> dict[str, Any]:
    rows = [validate_voice_greeting(c, pack) for c in pack["cases"]]
    accepted = [r for r in rows if r["accepted"]]
    failed = [r for r in rows if not r["accepted"]]
    return {
        "card": "WP-49",
        "label": "Executed",
        "workstream": pack.get("workstream", "WS4"),
        "deliverable": pack.get("deliverable", "D-07"),
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "n_cases": len(rows),
        "n_accepted": len(accepted),
        "n_failed": len(failed),
        "all_expect_matched": all(r["expect_matched"] for r in rows),
        "accepted_configs": [
            {
                "case_id": r["case_id"],
                "profile_id": r["profile_id"],
                "voice_id": r["voice_id"],
                "voice_style": r["voice_style"],
                "greeting_resolved": r["greeting_resolved"],
            }
            for r in accepted
        ],
        "failures": [
            {
                "case_id": r["case_id"],
                "profile_id": r["profile_id"],
                "voice_id": r["voice_id"],
                "voice_style": r["voice_style"],
                "errors": r["errors"],
            }
            for r in failed
        ],
        "results": rows,
    }
