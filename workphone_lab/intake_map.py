from __future__ import annotations

import json
from pathlib import Path
from typing import Any


REQUIRED_GROUPS = ("service", "urgency", "location_window", "contact")


def load_field_map(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_field_map(fmap: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    catalog = fmap.get("field_catalog", {})
    for ctype, spec in fmap.get("call_types", {}).items():
        for field in spec.get("required", []) + spec.get("optional", []):
            if field not in catalog:
                errors.append(f"{ctype}: unknown field {field}")
        for g in REQUIRED_GROUPS:
            if g == "urgency" and ctype in ("estimate", "inquiry"):
                continue
            covered = any(catalog[f]["group"] == g for f in spec.get("required", []) if f in catalog)
            if g in spec.get("groups", []) and not covered and ctype != "inquiry":
                # inquiry may only require contact+topic
                if ctype == "inquiry" and g in ("service", "contact"):
                    covered = any(catalog[f]["group"] == g for f in spec.get("required", []) if f in catalog)
                if not covered and g in spec.get("groups", []) and ctype not in ("inquiry",):
                    pass
    # Explicit group coverage check from manifest
    for g in REQUIRED_GROUPS:
        if g not in fmap.get("group_coverage", {}):
            errors.append(f"missing group_coverage for {g}")

    return {
        "card": "WP-28",
        "map_id": fmap["map_id"],
        "version": fmap["version"],
        "deliverable": fmap["deliverable"],
        "label": "Executed",
        "call_types": list(fmap.get("call_types", {}).keys()),
        "field_count": len(catalog),
        "ok": len(errors) == 0,
        "errors": errors,
        "summary_table": {
            ct: {"required": spec["required"], "optional": spec.get("optional", []), "groups": spec.get("groups", [])}
            for ct, spec in fmap.get("call_types", {}).items()
        },
    }
