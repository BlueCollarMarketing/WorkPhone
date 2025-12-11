from __future__ import annotations

from pathlib import Path
from typing import Any


def gate_s4(root: Path) -> dict[str, Any]:
    """Present / Missing / Location checklist for S4 Evidence Gate."""
    items = [
        ("Clean script pack WP-SCR-v0", "data/scripts/wp_scr_v0.json", ["WP-17", "WP-18"]),
        ("Noise/jargon variant pack", "data/scripts/wp_scr_v0_noise_jargon.json", ["WP-22", "WP-23"]),
        ("Regression corpus manifest", "data/corpus/regression_corpus.json", ["WP-23"]),
        ("S3 baseline score table", "outputs/s3_baseline_scores.json", ["WP-18"]),
        ("S4 hypothesis log", "docs/s4/WP-21-hypothesis-log-s4-noise-jargon.md", ["WP-21"]),
        ("Noise/jargon score + delta", "docs/s4/WP-22-intent-drop-noise-jargon.md", ["WP-22"]),
        ("Corpus version tags note", "docs/s4/WP-23-noise-jargon-regression-corpus.md", ["WP-23"]),
        ("Clarification-loop outcomes", "docs/s4/WP-24-clarification-loop-low-confidence.md", ["WP-24"]),
        ("OTS vs Workphone delta table", "docs/s4/WP-25-ots-vs-workphone-side-by-side.md", ["WP-25"]),
        ("Error taxonomy (S3)", "docs/s3/WP-19-asr-nlu-error-taxonomy.md", ["WP-19"]),
        ("Executed provider/model settings", "docs/s3/WP-20-executed-provider-model-settings.md", ["WP-20"]),
        ("Rejected telephony settings (S1)", "docs/s1/WP-11-negative-finding-register-telephony.md", ["WP-11"]),
    ]
    rows = []
    for name, rel, cards in items:
        path = root / rel
        # outputs may be regenerateable; mark Missing if absent but note regenerable
        present = path.exists()
        rows.append(
            {
                "item": name,
                "status": "Present" if present else "Missing",
                "location": rel,
                "cards": cards,
                "regenerable": rel.startswith("outputs/"),
            }
        )

    rejected = [
        {
            "id": "RJ-S4-01",
            "config": "Treat noise/jargon pack as clean baseline",
            "reason": "Breaks S3 comparison; versions must stay linked",
            "status": "Rejected",
        },
        {
            "id": "RJ-S4-02",
            "config": "Mark E-Invent cases as pass",
            "reason": "U1 rule: invent is defect",
            "status": "Rejected",
        },
        {
            "id": "RJ-S4-03",
            "config": "Claim OTS parity without delta table",
            "reason": "WP-25 Executed delta required",
            "status": "Rejected",
        },
        {
            "id": "RJ-S4-04",
            "config": "Skip clarification harms logging",
            "reason": "H-S4-04 needs helps/harms/no_change",
            "status": "Rejected",
        },
    ]

    present_n = sum(1 for r in rows if r["status"] == "Present")
    missing = [r for r in rows if r["status"] == "Missing"]
    # Soft-pass if only regenerable outputs missing
    hard_missing = [r for r in missing if not r["regenerable"]]
    return {
        "card": "WP-26",
        "sprint": "S4",
        "label": "Executed",
        "checklist": rows,
        "rejected_configs": rejected,
        "summary": {
            "present": present_n,
            "missing": len(missing),
            "hard_missing": len(hard_missing),
            "gate_pass": len(hard_missing) == 0,
        },
    }
