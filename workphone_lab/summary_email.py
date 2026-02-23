from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_template(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _get(record: dict[str, Any], *keys: str, default: str = "MISSING") -> str:
    cur: Any = record
    for k in keys:
        if not isinstance(cur, dict) or k not in cur or cur[k] in (None, ""):
            return default
        cur = cur[k]
    return str(cur)


def intake_to_summary_fields(record: dict[str, Any], next_step: str) -> dict[str, str]:
    need = _get(record, "service", "job_type", default="")
    if need == "MISSING" or not need:
        need = _get(record, "service", "inquiry_topic", default="")
    if need == "MISSING" or not need:
        st = _get(record, "service", "service_type")
        need = st if st != "MISSING" else "MISSING"
    urgency = _get(record, "urgency", "urgency_level")
    if urgency == "MISSING":
        hazard = _get(record, "urgency", "hazard_type", default="")
        urgency = hazard if hazard and hazard != "MISSING" else "MISSING"
    return {
        "caller": _get(record, "name"),
        "number": _get(record, "phone"),
        "need": need if need else "MISSING",
        "urgency": urgency,
        "next_step": next_step if next_step else "MISSING",
        "notes": _get(record, "notes", default=""),
    }


def render_email(template: dict[str, Any], fields: dict[str, str]) -> dict[str, str]:
    ctx = {
        **fields,
        "need_short": (fields.get("need") or "call")[:40],
        "template_id": template["template_id"],
        "version": template["version"],
    }
    subject = template["subject"]
    body = template["body_text"]
    for k, v in ctx.items():
        subject = subject.replace("{{" + k + "}}", v)
        body = body.replace("{{" + k + "}}", v)
    return {"subject": subject, "body": body}


def demo_summary(template: dict[str, Any], schema_examples: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for name, record in schema_examples.items():
        next_step = (
            "Escalate / high-priority voicemail"
            if record.get("service", {}).get("service_type") == "emergency"
            else "Email business + CRM stub row"
        )
        fields = intake_to_summary_fields(record, next_step)
        email = render_email(template, fields)
        rows.append(
            {
                "example": name,
                "fields": fields,
                "email": email,
                "has_required_slots": all(k in fields for k in template["fields"]),
                "caller_present": _present_in_record(record, "caller"),
                "number_present": _present_in_record(record, "number"),
            }
        )
    return {
        "card": "WP-37",
        "template_id": template["template_id"],
        "version": template["version"],
        "deliverable": template["deliverable"],
        "label": "Executed",
        "results": rows,
    }


def _present_in_record(record: dict[str, Any], field: str) -> bool:
    if field == "caller":
        return bool(record.get("name"))
    if field == "number":
        return bool(record.get("phone"))
    return True
