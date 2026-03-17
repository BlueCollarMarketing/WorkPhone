from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_breakpoint_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _simulate_leg(n: int, leg: int, safe_n: int, stagger_ms: int) -> dict[str, Any]:
    """Deterministic lab model: delay grows with N; drops begin after safe_n."""
    base_answer = 1.2
    contention = max(0, n - 1) * 0.9
    overflow = max(0, n - safe_n) * 2.5
    answer_delay_s = round(base_answer + contention + overflow + leg * 0.05, 4)
    drop = n > safe_n and leg > safe_n
    # First overflow legs may still answer late; legs beyond capacity drop
    if n > safe_n and leg > safe_n:
        drop = True
        answer_delay_s = None
    stuck = False
    return {
        "leg": leg,
        "stagger_ms": stagger_ms * (leg - 1),
        "answered": not drop,
        "answer_delay_s": answer_delay_s,
        "drop_or_reject": drop,
        "stuck_session": stuck,
    }


def run_at_n(n: int, cfg: dict[str, Any]) -> dict[str, Any]:
    safe_n = cfg["lab_capacity_model"]["safe_n"]
    stagger = cfg["search"]["stagger_ms"]
    thr = cfg["thresholds"]
    legs = [_simulate_leg(n, i + 1, safe_n, stagger) for i in range(n)]
    answered = [L for L in legs if L["answered"]]
    drops = sum(1 for L in legs if L["drop_or_reject"])
    stuck = sum(1 for L in legs if L["stuck_session"])
    delays = [L["answer_delay_s"] for L in answered if L["answer_delay_s"] is not None]
    max_delay = max(delays) if delays else None
    drop_rate = round(drops / n, 4) if n else 0.0
    excess_delay = max_delay is not None and max_delay > thr["max_answer_delay_s"]
    drop_fail = drop_rate > thr["max_drop_rate"]
    stuck_fail = stuck > thr["stuck_sessions_allowed"]
    within_limits = not (excess_delay or drop_fail or stuck_fail)
    return {
        "n": n,
        "legs": legs,
        "answered": len(answered),
        "drops": drops,
        "drop_rate": drop_rate,
        "stuck_sessions": stuck,
        "max_answer_delay_s": max_delay,
        "excess_answer_delay": excess_delay,
        "within_limits": within_limits,
        "fail_reasons": [
            r
            for r, bad in (
                ("excess_answer_delay", excess_delay),
                ("drop_rate", drop_fail),
                ("stuck_session", stuck_fail),
            )
            if bad
        ],
    }


def measure_breakpoint(cfg: dict[str, Any]) -> dict[str, Any]:
    n_min = cfg["search"]["n_min"]
    n_max = cfg["search"]["n_max"]
    sweep = [run_at_n(n, cfg) for n in range(n_min, n_max + 1)]
    break_point = next((row["n"] for row in sweep if not row["within_limits"]), None)
    last_ok = None
    for row in sweep:
        if row["within_limits"]:
            last_ok = row["n"]
        else:
            break
    supported = break_point is not None
    return {
        "card": "WP-43",
        "label": "Executed",
        "uncertainty": "U3",
        "hypothesis_id": cfg["hypothesis"]["id"],
        "hypothesis": cfg["hypothesis"]["statement"],
        "pack_id": cfg["pack_id"],
        "version": cfg["version"],
        "thresholds": cfg["thresholds"],
        "provider_configs": cfg["provider_configs"],
        "lab_capacity_model": cfg["lab_capacity_model"],
        "sweep": sweep,
        "break_point_n": break_point,
        "last_ok_n": last_ok,
        "hypothesis_supported": supported,
    }
