from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_board(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_board(board: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for uid, spec in board["uncertainties"].items():
        rows.append(
            {
                "id": uid,
                "status": spec["status"],
                "evidence_count": len(spec.get("evidence_pointers", [])),
                "labels": sorted({p.get("label", "Executed") for p in spec.get("evidence_pointers", [])}),
                "notes": spec.get("notes", ""),
            }
        )
    return {
        "card": "WP-30",
        "board_id": board["board_id"],
        "version": board["version"],
        "label": board.get("label", "Executed"),
        "rows": rows,
        "u1": board["uncertainties"]["U1"],
    }
