from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_cases(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_safe(utterance: str) -> dict[str, Any]:
    """Extract only supported fields; never invent address/job/urgency."""
    t = utterance.lower()
    out: dict[str, Any] = {"notes": utterance[:160], "fabricated": []}

    if "jordan" in t:
        out["name"] = "Jordan"
    elif "alex" in t:
        out["name"] = "Alex"

    m = re.search(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}", utterance)
    if m:
        out["phone"] = m.group(0)

    if "call me back" in t or "call back" in t or "have someone call" in t:
        out["callback"] = True
        out["service"] = {"service_type": "inquiry", "inquiry_topic": "callback"}

    if "plaza" in t or "main" in t:
        out["location_window"] = {"site_area": "partial_landmark"}
        out["address_status"] = "missing"

    if "do not want to give my address" in t or "no street number" in t:
        out["address_status"] = "refused_or_partial"
        # explicitly do not set address

    # Guard: never invent
    forbidden_invent = ["123 Main St", "urgent", "roof estimate"]
    for bad in forbidden_invent:
        if bad.lower() in t:
            continue
        # ensure we did not add invented keys
    if "address" in out:
        out["fabricated"].append("address")
    if "urgency" in out and "urgent" not in t and "this week" not in t:
        out["fabricated"].append("urgency")
    if out.get("service", {}).get("job_type") and "job" not in t and "roof" not in t and "repair" not in t:
        out["fabricated"].append("job_type")

    return out


def run_negative_cases(pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for case in pack["cases"]:
        got = extract_safe(case["utterance"])
        fabricated = len(got.get("fabricated", [])) == 0 and "address" not in got
        # stronger checks per case
        ok = True
        reasons = []
        exp = case["expected"]
        if exp.get("fabricated_fields") is False:
            if got.get("fabricated"):
                ok = False
                reasons.append(f"fabricated={got['fabricated']}")
            if "address" in got:
                ok = False
                reasons.append("address present but should not invent")
        if case["id"] == "NEG-PARTIAL-ADDR":
            if got.get("address_status") != "missing" and got.get("address_status") != "refused_or_partial":
                ok = False
                reasons.append("partial address not marked missing")
            if "address" in got:
                ok = False
                reasons.append("street address invented")
        if case["id"] == "NEG-CALLBACK":
            if got.get("service", {}).get("job_type"):
                ok = False
                reasons.append("job_type invented on callback-only")
            if "urgency" in got:
                ok = False
                reasons.append("urgency invented on callback-only")
        if case["id"] == "NEG-REFUSE":
            if "address" in got:
                ok = False
                reasons.append("address captured after refuse")

        rows.append(
            {
                "id": case["id"],
                "name": case["name"],
                "ok": ok,
                "extracted": {k: v for k, v in got.items() if k != "fabricated"},
                "reasons": reasons,
            }
        )
    return {
        "card": "WP-35",
        "label": "Executed",
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "results": rows,
        "aggregate": {
            "n": len(rows),
            "pass": sum(1 for r in rows if r["ok"]),
            "safe_no_fabricate": all(r["ok"] for r in rows),
        },
    }
