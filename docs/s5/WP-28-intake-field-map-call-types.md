# S5 - Map required intake fields per call type

**YouTrack:** WP-28  
**Sprint:** S5 - Dialogue policy + corpus gate (5-16 Jan 2026)  
**Date recorded:** 2026-01-06  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 252h (Documentation)  
**Ideal days:** 32  
**Status:** Complete

## Purpose

Map required intake fields for each call type (service, urgency, location/window, contact). Version the field map for D-04.

## Version (D-04)

| Field | Value |
|-------|--------|
| Map ID | WP-INTAKE-MAP |
| Version | v0 |
| Deliverable | D-04 |
| Linked policy | WP-DIALOGUE-v0 @ v0 |
| Path | `data/intake/intake_field_map_v0.json` |
| Evidence label | Executed |

## Field groups

| Group | Purpose |
|-------|---------|
| contact | Name + callback number |
| service | Service / job / inquiry type |
| urgency | Hazard + urgency level |
| location_window | Site area, address, callback window, access |

## Required fields by call type

| Call type | Required | Optional |
|-----------|----------|----------|
| estimate | contact_name, contact_number, service_type, job_type, site_area, callback_window | address, access_notes |
| service | contact_name, contact_number, service_type, job_type, urgency_level, site_area | address, callback_window, access_notes |
| emergency | contact_name, contact_number, service_type, hazard_type, urgency_level | site_area, address |
| inquiry | contact_name, contact_number, inquiry_topic | callback_window |

## Lab

```text
python -m workphone_lab intake
```

Validates catalog references and writes `outputs/s5_intake_field_map_report.json`.

## Rules

- Never invent a required field; mark missing explicitly
- Emergency must capture contact_number before end
- Version bumps: v0.x additive; v1 for breaking renames

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s5/WP-28-intake-field-map-call-types.md` |
| Experiment log | `docs/experiment-log.md` |
