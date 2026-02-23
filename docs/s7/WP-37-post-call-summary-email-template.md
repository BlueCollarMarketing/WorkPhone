# S7 - Implement post-call summary email template

**YouTrack:** WP-37  
**Sprint:** S7 - Post-call email summaries (23 Feb - 6 Mar 2026)  
**Date recorded:** 2026-02-23  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 360h (Implementation)  
**Ideal days:** 45  
**Status:** Complete

## Purpose

Implement summary email template covering caller, number, need, urgency, and next step. Record template version for deliverable D-05.

## Scope

| Field | Value |
|-------|--------|
| Template ID | WP-SUMMARY-EMAIL |
| Version | v0 |
| Deliverable | D-05 |
| Config | `data/summary/summary_email_template_v0.json` |
| Linked schema | WP-INTAKE-SCHEMA v0 |
| Evidence label | Executed |

## Template slots (D-05)

| Slot | Source | Missing behavior |
|------|--------|------------------|
| caller | intake `name` | Render `MISSING` |
| number | intake `phone` | Render `MISSING` |
| need | job_type / inquiry_topic / service_type | Render `MISSING` |
| urgency | urgency_level or hazard_type | Render `MISSING` |
| next_step | handoff / policy outcome | Render `MISSING` |
| notes | intake notes (optional) | Empty string OK |

## Subject / body

- Subject: `[Workphone] Call summary - {{caller}} - {{need_short}}`
- Body lists caller, number, need, urgency, next step, notes, plus template id/version footer

## Guardrails

- Never invent caller, number, need, or urgency
- next_step comes from policy/handoff path, not free invent
- Version string recorded for D-05 audit trail

## Lab

```text
python -m workphone_lab summary
```

Demo renders estimate and emergency examples from intake schema into subject/body.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s7/WP-37-post-call-summary-email-template.md` |
| Template | `data/summary/summary_email_template_v0.json` |
| Demo export | `outputs/s7_summary_email_demo.json` |
| Experiment log | `docs/experiment-log.md` |
