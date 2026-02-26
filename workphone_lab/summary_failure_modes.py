from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ABSENT = {None, "", "MISSING", "missing", "null", "none"}


def load_failure_modes(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _present(value: Any) -> bool:
    if value is None:
        return False
    return str(value).strip().lower() not in ABSENT and str(value).strip() != ""


def classify_probe(probe: dict[str, Any], modes_by_id: dict[str, Any]) -> dict[str, Any]:
    mode_id = probe["mode_id"]
    mode = modes_by_id[mode_id]
    obs = probe["observed"]
    defect = False
    detail = ""

    if mode_id == "SF-DELAY":
        latency = float(obs["latency_s"])
        alert = float(obs.get("draft_alert_s", 15.0))
        defect = latency >= alert
        detail = f"latency_s={latency} alert_s={alert}"
    elif mode_id == "SF-WRONG-NUM":
        pred = str(obs.get("predicted_number", "")).strip()
        truth = str(obs.get("ground_truth_number", "")).strip()
        defect = pred != truth
        detail = f"predicted={pred} truth={truth}"
    elif mode_id == "SF-HALLUC-SVC":
        pred_need = obs.get("predicted_need")
        truth_need = obs.get("ground_truth_need")
        defect = _present(pred_need) and not _present(truth_need)
        if _present(pred_need) and _present(truth_need) and str(pred_need).lower() != str(truth_need).lower():
            defect = True
        detail = f"predicted_need={pred_need} truth_need={truth_need}"
    elif mode_id == "SF-INVENT":
        # Any predicted field present while GT absent => invent defect
        invent_keys = [k for k in obs if k.startswith("predicted_")]
        defect = False
        parts = []
        for pk in invent_keys:
            field = pk.replace("predicted_", "", 1)
            gk = f"ground_truth_{field}"
            if _present(obs.get(pk)) and not _present(obs.get(gk)):
                defect = True
                parts.append(field)
        detail = "invented=" + ",".join(parts) if parts else "no_invent"
    else:
        defect = True
        detail = f"unknown mode {mode_id}"

    # Invent-family modes are never passes when defect triggered
    invent_family = mode_id in ("SF-INVENT", "SF-HALLUC-SVC", "SF-WRONG-NUM")
    scored_as_pass = False if (defect and invent_family) else (not defect)
    if mode_id == "SF-DELAY":
        scored_as_pass = not defect

    return {
        "probe_id": probe["probe_id"],
        "mode_id": mode_id,
        "mode_name": mode["name"],
        "severity": mode["severity"],
        "script_id": probe.get("script_id"),
        "defect": defect,
        "scored_as_pass": scored_as_pass,
        "invent_kept_as_defect": invent_family and defect and not scored_as_pass,
        "detail": detail,
        "ground_truth_note": probe.get("ground_truth_note"),
    }


def evaluate_failure_modes(library: dict[str, Any]) -> dict[str, Any]:
    modes_by_id = {m["id"]: m for m in library["modes"]}
    rows = [classify_probe(p, modes_by_id) for p in library["probes"]]
    invent_rows = [r for r in rows if r["mode_id"] in ("SF-INVENT", "SF-HALLUC-SVC", "SF-WRONG-NUM") and r["defect"]]
    invent_pass_violations = [r for r in invent_rows if r["scored_as_pass"]]
    rule_ok = len(invent_pass_violations) == 0
    return {
        "card": "WP-40",
        "label": "Executed",
        "library_id": library["library_id"],
        "version": library["version"],
        "uncertainty": library.get("uncertainty", "U3"),
        "scoring_rule": library["scoring_rule"],
        "modes": library["modes"],
        "n_probes": len(rows),
        "n_defects": sum(1 for r in rows if r["defect"]),
        "invent_defects": len(invent_rows),
        "invent_pass_violations": len(invent_pass_violations),
        "rule_ok": rule_ok,
        "results": rows,
        "rejected_configs": [
            {
                "id": "RJ-S7-01",
                "config": "Mark invent / hallucinated service / wrong number as pass",
                "reason": "Invent cases are defects, not passes",
            },
            {
                "id": "RJ-S7-02",
                "config": "Ignore delayed email as non-evidence for U3",
                "reason": "Delay retained as SF-DELAY for timeliness evidence",
            },
        ],
    }
