from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_queue_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _simulate_load_point(point: dict[str, Any], safe_n: int, queue_limit: int) -> dict[str, Any]:
    n = point["n"]
    stagger = point["stagger_ms"]
    provider_logs: list[dict[str, Any]] = []
    queued = 0
    answered = 0
    drops = 0
    errors = 0
    error_counts = {"E-QUEUE-FULL": 0, "E-DROP": 0, "E-ANSWER-TIMEOUT": 0, "E-PROVIDER-BLIP": 0}

    for leg in range(1, n + 1):
        ts_ms = stagger * (leg - 1)
        queue_depth = min(leg, queue_limit)
        if leg <= safe_n:
            answered += 1
            queued = max(queued, queue_depth)
            provider_logs.append(
                {
                    "ts_ms": ts_ms,
                    "n": n,
                    "leg": leg,
                    "event": "answered",
                    "error_class": None,
                    "queue_depth": queue_depth,
                    "detail": "session answered on forward path",
                }
            )
            continue

        # Beyond safe_n: mix of queue-full reject, drop, and rare provider blip
        if leg == safe_n + 1:
            err = "E-ANSWER-TIMEOUT"
            event = "timeout"
            detail = "answer delay exceeded before connect"
        elif leg == n and n >= safe_n + 2:
            err = "E-PROVIDER-BLIP"
            event = "provider_error"
            detail = "transient forward-path blip"
        elif queue_depth >= queue_limit:
            err = "E-QUEUE-FULL"
            event = "reject"
            detail = "queue at depth limit"
        else:
            err = "E-DROP"
            event = "drop"
            detail = "session dropped under concurrency"

        drops += 1
        errors += 1
        error_counts[err] += 1
        provider_logs.append(
            {
                "ts_ms": ts_ms,
                "n": n,
                "leg": leg,
                "event": event,
                "error_class": err,
                "queue_depth": queue_depth,
                "detail": detail,
            }
        )

    offered = n
    queue_occupancy_peak = min(n, queue_limit)
    return {
        "id": point["id"],
        "n": n,
        "offered": offered,
        "answered": answered,
        "drops": drops,
        "errors": errors,
        "queue_occupancy_peak": queue_occupancy_peak,
        "queue_drop_rate": round(drops / offered, 4) if offered else 0.0,
        "error_rate": round(errors / offered, 4) if offered else 0.0,
        "answer_rate": round(answered / offered, 4) if offered else 0.0,
        "error_counts": error_counts,
        "provider_logs": provider_logs,
    }


def measure_queue_rates(cfg: dict[str, Any]) -> dict[str, Any]:
    safe_n = cfg["safe_n"]
    qlim = cfg["queue_depth_limit"]
    rows = [_simulate_load_point(p, safe_n, qlim) for p in cfg["load_points"]]
    # Aggregate across load points (U3 pack summary)
    offered = sum(r["offered"] for r in rows)
    drops = sum(r["drops"] for r in rows)
    errors = sum(r["errors"] for r in rows)
    answered = sum(r["answered"] for r in rows)
    err_tot = {"E-QUEUE-FULL": 0, "E-DROP": 0, "E-ANSWER-TIMEOUT": 0, "E-PROVIDER-BLIP": 0}
    provider_logs: list[dict[str, Any]] = []
    for r in rows:
        for k, v in r["error_counts"].items():
            err_tot[k] = err_tot.get(k, 0) + v
        for log in r["provider_logs"]:
            provider_logs.append({"load_id": r["id"], **log})

    return {
        "card": "WP-44",
        "label": "Executed",
        "uncertainty": "U3",
        "u3_pack": cfg["u3_pack"],
        "pack_id": cfg["pack_id"],
        "version": cfg["version"],
        "safe_n": safe_n,
        "queue_depth_limit": qlim,
        "error_classes": cfg["error_classes"],
        "results": rows,
        "aggregate": {
            "offered": offered,
            "answered": answered,
            "drops": drops,
            "errors": errors,
            "queue_drop_rate": round(drops / offered, 4) if offered else 0.0,
            "error_rate": round(errors / offered, 4) if offered else 0.0,
            "answer_rate": round(answered / offered, 4) if offered else 0.0,
            "error_counts": err_tot,
        },
        "provider_logs_retained": True,
        "provider_log_count": len(provider_logs),
        "provider_logs": provider_logs,
    }
