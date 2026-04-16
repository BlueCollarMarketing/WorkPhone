from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .summary_latency import _histogram, _percentile


def load_ttl_pack(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def measure_time_to_live(pack: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for run in pack["runs"]:
        ttl = round(
            run["validate_s"] + run["map_s"] + run["provision_s"] + run["smoke_ring_s"],
            4,
        )
        rows.append(
            {
                "run_id": run["run_id"],
                "profile": run["profile"],
                "form_submit_s": run["form_submit_s"],
                "validate_s": run["validate_s"],
                "map_s": run["map_s"],
                "provision_s": run["provision_s"],
                "smoke_ring_s": run["smoke_ring_s"],
                "callable_at_s": ttl,
                "ttl_s": ttl,
                "callable": True,
            }
        )
    vals = sorted(r["ttl_s"] for r in rows)
    dist = {
        "n": len(vals),
        "min_s": vals[0] if vals else 0.0,
        "p50_s": _percentile(vals, 50),
        "p90_s": _percentile(vals, 90),
        "p95_s": _percentile(vals, 95),
        "max_s": vals[-1] if vals else 0.0,
        "mean_s": round(sum(vals) / len(vals), 4) if vals else 0.0,
        "histogram_s": _histogram(vals, [0, 60, 90, 120, 180, 300]),
    }
    targets = pack.get("targets_draft", {})
    within = dist["p50_s"] <= targets.get("p50_max_s", float("inf")) and dist[
        "p95_s"
    ] <= targets.get("p95_max_s", float("inf"))
    return {
        "card": "WP-50",
        "label": "Executed",
        "deliverable": pack.get("deliverable", "D-07"),
        "workstream": pack.get("workstream", "WS4"),
        "pack_id": pack["pack_id"],
        "version": pack["version"],
        "metric": pack["metric"],
        "definition": pack["definition"],
        "path": pack["path"],
        "targets_draft": targets,
        "distribution": dist,
        "within_draft_targets": within,
        "runs": rows,
    }
