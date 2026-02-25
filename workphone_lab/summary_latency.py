from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_latency_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _percentile(sorted_vals: list[float], p: float) -> float:
    if not sorted_vals:
        return 0.0
    if len(sorted_vals) == 1:
        return sorted_vals[0]
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return sorted_vals[f]
    return round(sorted_vals[f] + (sorted_vals[c] - sorted_vals[f]) * (k - f), 4)


def _histogram(latencies: list[float], edges: list[float]) -> list[dict[str, Any]]:
    bins = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        n = sum(1 for x in latencies if lo <= x < hi)
        bins.append({"lo_s": lo, "hi_s": hi, "count": n})
    last_lo = edges[-1]
    bins.append({"lo_s": last_lo, "hi_s": None, "count": sum(1 for x in latencies if x >= last_lo)})
    return bins


def measure_summary_latency(pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for run in pack["runs"]:
        latency = round(run["render_s"] + run["queue_s"] + run["deliver_s"], 4)
        rows.append(
            {
                "run_id": run["run_id"],
                "script_id": run["script_id"],
                "call_end_s": run["call_end_s"],
                "render_s": run["render_s"],
                "queue_s": run["queue_s"],
                "deliver_s": run["deliver_s"],
                "email_received_s": latency,
                "latency_s": latency,
                "email_received": True,
            }
        )
    latencies = sorted(r["latency_s"] for r in rows)
    dist = {
        "n": len(latencies),
        "min_s": latencies[0] if latencies else 0.0,
        "p50_s": _percentile(latencies, 50),
        "p90_s": _percentile(latencies, 90),
        "p95_s": _percentile(latencies, 95),
        "max_s": latencies[-1] if latencies else 0.0,
        "mean_s": round(sum(latencies) / len(latencies), 4) if latencies else 0.0,
        "histogram_s": _histogram(latencies, [0, 5, 10, 15, 20, 30]),
    }
    targets = pack.get("targets_draft", {})
    within_p50 = dist["p50_s"] <= targets.get("p50_max_s", float("inf"))
    within_p95 = dist["p95_s"] <= targets.get("p95_max_s", float("inf"))
    return {
        "card": "WP-39",
        "label": "Executed",
        "uncertainty": "U3",
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "metric": pack["metric"],
        "definition": pack["definition"],
        "path": pack["path"],
        "targets_draft": targets,
        "distribution": dist,
        "within_draft_targets": within_p50 and within_p95,
        "runs": rows,
    }
