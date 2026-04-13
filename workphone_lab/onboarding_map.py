from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_onboard_map(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _set_path(obj: dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    cur = obj
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = value


def validate_form(form: dict[str, Any], field_map: list[dict[str, Any]]) -> list[str]:
    errors = []
    for row in field_map:
        if not row.get("required"):
            continue
        key = row["form_field"]
        val = form.get(key)
        if val is None or val == "" or val == []:
            errors.append(f"missing required form field: {key}")
        enum = row.get("enum")
        if enum and val is not None and val not in enum:
            errors.append(f"invalid enum for {key}: {val}")
    return errors


def form_to_agent_config(form: dict[str, Any], mapping: dict[str, Any]) -> dict[str, Any]:
    agent: dict[str, Any] = {
        "config_id": "WP-AGENT-CONFIG",
        "version": mapping["version"],
        "deliverable": mapping["deliverable"],
        "source_map": mapping["map_id"],
        "label": "Executed",
    }
    for row in mapping["field_map"]:
        key = row["form_field"]
        if key not in form:
            continue
        _set_path(agent, row["agent_path"], form[key])
    # Expand greeting template
    greet = agent.get("voice", {}).get("greeting_template")
    if isinstance(greet, str) and "{{business_name}}" in greet:
        name = form.get("business_name") or "us"
        agent["voice"]["greeting_template"] = greet.replace("{{business_name}}", name)
    return agent


def demo_onboarding(mapping: dict[str, Any]) -> dict[str, Any]:
    results = []
    for name, form in mapping.get("examples", {}).items():
        errors = validate_form(form, mapping["field_map"])
        config = form_to_agent_config(form, mapping) if not errors else None
        results.append(
            {
                "example": name,
                "form_ok": len(errors) == 0,
                "errors": errors,
                "agent_config": config,
                "mapped_groups": {
                    "services": bool(config.get("agent", {}).get("services")),
                    "hours": bool(config.get("agent", {}).get("hours")),
                    "voice": bool(config.get("agent", {}).get("voice")),
                }
                if config
                else None,
            }
        )
    return {
        "card": "WP-47",
        "label": "Executed",
        "deliverable": mapping["deliverable"],
        "map_id": mapping["map_id"],
        "version": mapping["version"],
        "mapping_path": mapping["mapping_path"],
        "field_count": len(mapping["field_map"]),
        "groups": mapping["groups"],
        "results": results,
        "ok": all(r["form_ok"] for r in results),
    }
