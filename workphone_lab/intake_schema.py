from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PHONE_RE = re.compile(r"\d{3}[-.\s]?\d{3}[-.\s]?\d{4}|\d{10,}")


def load_schema(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_record(record: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    for key in schema.get("required_core", []):
        if key not in record or record[key] in (None, "", {}):
            errors.append(f"missing required core field: {key}")

    if "name" in record and (not isinstance(record["name"], str) or not record["name"].strip()):
        errors.append("name must be non-empty string")

    if "phone" in record:
        phone = str(record["phone"])
        if not PHONE_RE.search(phone):
            errors.append("phone failed digits_or_formatted pattern")

    service = record.get("service") or {}
    if isinstance(service, dict) and "service_type" in service:
        allowed = schema["properties"]["service"]["properties"]["service_type"]["values"]
        if service["service_type"] not in allowed:
            errors.append(f"invalid service_type: {service['service_type']}")

    urgency = record.get("urgency") or {}
    if isinstance(urgency, dict) and "urgency_level" in urgency:
        allowed_u = schema["properties"]["urgency"]["properties"]["urgency_level"]["values"]
        if urgency["urgency_level"] not in allowed_u:
            errors.append(f"invalid urgency_level: {urgency['urgency_level']}")

    # notes must not invent: if notes present but name/phone missing, still error (already covered)
    return {"ok": len(errors) == 0, "errors": errors, "record": record}


def validate_schema_pack(schema: dict[str, Any]) -> dict[str, Any]:
    results = []
    for name, example in schema.get("examples", {}).items():
        results.append({"example": name, **validate_record(example, schema)})

    # Negative: invent-via-notes-only
    bad = {"notes": "Caller is Alex at 555"}
    results.append({"example": "notes_only_invalid", **validate_record(bad, schema)})

    return {
        "card": "WP-32",
        "schema_id": schema["schema_id"],
        "version": schema["version"],
        "deliverable": schema["deliverable"],
        "sprint": schema["sprint"],
        "label": "Executed",
        "groups": ["name", "phone", "service", "urgency", "location_window", "notes"],
        "results": results,
        "ok": all(r["ok"] for r in results if r["example"] != "notes_only_invalid")
        and any(not r["ok"] for r in results if r["example"] == "notes_only_invalid"),
    }
