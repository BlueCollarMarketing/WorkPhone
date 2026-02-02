# S6 - Implement intake schema for contractor call fields

**YouTrack:** WP-32  
**Sprint:** S6 - Intake field model and handoff (26 Jan - 6 Feb 2026)  
**Date recorded:** 2026-02-02  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 251h (Development)  
**Ideal days:** 31  
**Status:** Complete

## Purpose

Implement intake schema (name, phone, service, urgency, location/window, notes). Version the schema for D-04 and S6 tests.

## Schema version (D-04)

| Field | Value |
|-------|--------|
| Schema ID | WP-INTAKE-SCHEMA |
| Version | v0 |
| Deliverable | D-04 |
| Sprint | S6 |
| Path | `data/intake/intake_schema_v0.json` |
| Linked field map | WP-INTAKE-MAP @ v0 |
| Evidence label | Executed |

## Groups

| Group | Contents |
|-------|----------|
| name | Caller / business name |
| phone | Callback number (digits or formatted) |
| service | service_type, job_type, inquiry_topic |
| urgency | urgency_level, hazard_type |
| location_window | site_area, address, callback_window, access_notes |
| notes | Free-text; must not invent required fields |

## Required core

`name`, `phone`, `service`

## Lab

```text
python -m workphone_lab schema
```

Validates examples + rejects notes-only invent attempts -> `outputs/s6_intake_schema_report.json`.

## S6 use

Schema is the contract for handoff rules (WP-33/WP-34) and negative intake cases (WP-35).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s6/WP-32-intake-schema-contractor-fields.md` |
| Experiment log | `docs/experiment-log.md` |
