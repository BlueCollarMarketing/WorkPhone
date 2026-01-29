# S6 - Evidence Gate intake schema and wrong-rate tables

**YouTrack:** WP-36  
**Sprint:** S6 - Intake field model and handoff (26 Jan - 6 Feb 2026)  
**Date recorded:** 2026-01-29  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 390h (Documentation)  
**Ideal days:** 49  
**Status:** Complete - S6 close

## Purpose

Complete Evidence Gate for intake schema plus measured incomplete/wrong rates. Mark Present / Missing / Location for S6 close.

## Evidence Gate checklist (S6)

| Item | Present / Missing | Location |
|------|-------------------|----------|
| Intake field map D-04 | Present | `data/intake/intake_field_map_v0.json` |
| Intake schema v0 | Present | `data/intake/intake_schema_v0.json` |
| Negative intake cases pack | Present | `data/intake/negative_intake_cases_v0.json` |
| Handoff rules email/SMS/CRM | Present | `data/handoff/handoff_rules_v0.json` |
| Schema validation note | Present | `docs/s6/WP-32-intake-schema-contractor-fields.md` |
| Required-field enforcement rates | Present | `docs/s6/WP-33-required-field-enforcement-handoffs.md` |
| Handoff channel rules note | Present | `docs/s6/WP-34-handoff-rules-email-sms-crm.md` |
| Negative intake safe handling | Present | `docs/s6/WP-35-negative-intake-cases.md` |
| Handoff enforcement export | Present | `outputs/s6_handoff_enforcement.json` |
| Negative intake export | Present | `outputs/s6_negative_intake.json` |
| Schema report export | Present | `outputs/s6_intake_schema_report.json` |
| Live CRM production write audit | Missing | Planned; stub only on Executed path |

## Wrong-rate / incomplete tables (Executed)

| Metric | Value | Source |
|--------|------:|--------|
| Incomplete handoff rate (no enforcement) | 0.83 | WP-33 |
| Incomplete handoff rate (with enforcement) | 0.00 | WP-33 |
| Wrong rate (with enforcement) | 0.00 | WP-33 |
| Negative cases safe (no fabricate) | 3/3 | WP-35 |

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-S6-01 | Allow handoff without name/phone/service |
| RJ-S6-02 | Invent address on refuse/partial cases |
| RJ-S6-03 | Treat Planned CRM as Executed |

## Lab

```text
python -m workphone_lab gate-s6
```

## S6 close decision

| Gate | Decision |
|------|----------|
| Intake schema + rate tables | Pass |
| Rejected configs retained | Pass |
| S6 sprint close | Closed - proceed to S7 summaries |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s6/WP-36-evidence-gate-intake-schema.md` |
| Experiment log | `docs/experiment-log.md` |
