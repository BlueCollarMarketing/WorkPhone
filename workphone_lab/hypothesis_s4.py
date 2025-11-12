from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


def build_hypothesis_log(baseline: dict[str, Any]) -> dict[str, Any]:
    agg = baseline.get("aggregate", {})
    return {
        "series": "S4 noise/jargon",
        "card": "WP-21",
        "created": str(date.today()),
        "comparison_starting_point": {
            "pack_id": baseline.get("pack_id"),
            "version": baseline.get("version"),
            "label": baseline.get("label", "Executed"),
            "intent_pass": agg.get("intent_pass"),
            "entity_full": agg.get("entity_full"),
            "n": agg.get("n"),
            "source": "outputs/s3_baseline_scores.json (from WP-18 / workphone_lab baseline)",
            "taxonomy": "docs/s3/WP-19-asr-nlu-error-taxonomy.md",
        },
        "hypotheses": [
            {
                "id": "H-S4-01",
                "statement": "Under job-site noise, intent capture drops vs clean S3 baseline while entity capture drops faster.",
                "compare_to": "S3 aggregate intent_pass / entity_full",
                "primary_classes": ["E-Overlap", "E-Omit"],
            },
            {
                "id": "H-S4-02",
                "statement": "Trade jargon variants raise E-Jargon mis-maps vs clean WP-SCR-v0 without changing true caller intent.",
                "compare_to": "S3 per-script intent_ok on SCR-E01/SCR-S01",
                "primary_classes": ["E-Jargon"],
            },
            {
                "id": "H-S4-03",
                "statement": "Spoken phone numbers and addresses under noise increase E-Num failures vs clean baseline digit capture.",
                "compare_to": "S3 entity number capture on all SCR-*",
                "primary_classes": ["E-Num"],
            },
            {
                "id": "H-S4-04",
                "statement": "Clarification-loop prompts recover part of the S3-to-S4 intent gap at low confidence without inventing fields.",
                "compare_to": "S3 invent_risk=false on SCR-I01",
                "primary_classes": ["E-Invent", "E-Omit"],
            },
        ],
    }


def write_hypothesis_log(log: dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(log, indent=2), encoding="utf-8")
    return path
