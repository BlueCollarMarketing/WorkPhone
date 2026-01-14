from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_corpus_gate(
    gate: dict[str, Any],
    corpus: dict[str, Any],
    policy: dict[str, Any],
    *,
    proposed_bulk_policy_change: bool,
) -> dict[str, Any]:
    approved = gate["approved_corpus"]
    corpus_ok = (
        corpus.get("corpus_id") == approved["corpus_id"]
        and corpus.get("version") == approved["version"]
    )
    policy_match = (
        policy.get("policy_id") == gate["policy_under_gate"]["policy_id"]
        and policy.get("version") == gate["policy_under_gate"]["version"]
    )

    if proposed_bulk_policy_change and not corpus_ok:
        decision = "BLOCKED"
        reason = "Bulk policy change requires approved corpus version tag"
    elif proposed_bulk_policy_change and corpus_ok:
        decision = "PASS"
        reason = "Approved corpus version present; bulk change may proceed under M3 gate"
    else:
        decision = "PASS"
        reason = "No bulk production policy change requested"

    return {
        "card": "WP-31",
        "gate_id": gate["gate_id"],
        "milestone": gate["milestone"],
        "label": "Executed",
        "corpus_tagged": {
            "corpus_id": corpus.get("corpus_id"),
            "version": corpus.get("version"),
            "matches_approved": corpus_ok,
        },
        "policy": {
            "policy_id": policy.get("policy_id"),
            "version": policy.get("version"),
            "matches_gated_policy": policy_match,
        },
        "proposed_bulk_policy_change": proposed_bulk_policy_change,
        "decision": decision,
        "reason": reason,
        "rule": gate["rule"],
    }
