# S0 - Open YouTrack WP structure and experiment-log template

**YouTrack:** WP-5  
**Sprint:** S0 - Framing & OTS Rejection (1-11 Jul 2025)  
**Date recorded:** 2025-07-04  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 8h (Implementation)  
**Status:** Complete

## Purpose

Confirm S0-S10 and Close-out sprints in YouTrack WP. Add an experiment-log template for hypothesis -> config -> result tracking.

## YouTrack WP sprint structure (confirmed)

| Sprint | Focus |
|--------|--------|
| S0 | Framing and OTS rejection |
| S1 | Telephony answer path |
| S2 | Telephony hardening + Evidence Gate |
| S3 | ASR / NLU baseline |
| S4 | Noise / jargon corpus + Evidence Gate |
| S5 | Dialogue policy + corpus gate |
| S6 | Intake field model and handoff |
| S7 | Post-call email summaries |
| S8 | Concurrency and latency (U3) |
| S9 | Onboarding to live agent |
| S10 | E2E assembly + evidence pack |
| Close-out | Continuity experiments and records freeze |

## Experiment-log template

Use one row (or linked note) per hypothesis test:

| Field | Required content |
|-------|------------------|
| Date | Work date (YYYY-MM-DD) |
| Card | YouTrack ID (WP-*) |
| Sprint | S0-S10 or Close-out |
| Author | Assignee name |
| Observation | What was seen |
| Hypothesis | What is being tested |
| Config | Settings / models / scripts used (Executed vs Planned) |
| Result | Pass / Fail / Partial with metrics or notes |
| Interpretation | What changes next |

Template file: `docs/templates/experiment-log-entry.md`  
Living index: `docs/experiment-log.md`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s0/WP-05-youtrack-wp-structure-experiment-log-template.md` |
| Entry template | `docs/templates/experiment-log-entry.md` |
| Experiment log | `docs/experiment-log.md` |
