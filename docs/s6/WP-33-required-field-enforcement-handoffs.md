# S6 - Test required-field enforcement on intake handoffs

**YouTrack:** WP-33  
**Sprint:** S6 - Intake field model and handoff (26 Jan - 6 Feb 2026)  
**Date recorded:** 2026-01-26  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Testing)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Hypothesis: required-field enforcement reduces incomplete handoffs without killing conversion. Measure incomplete/wrong rates on the corpus.

## Hypothesis

Required-field enforcement reduces incomplete handoffs that reach the business, without driving allowed conversion to zero.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Schema | WP-INTAKE-SCHEMA @ v0 |
| Corpus | WP-SCR-v0 + WP-SCR-v0-NJ |
| Command | `python -m workphone_lab handoff` |
| Export | `outputs/s6_handoff_enforcement.json` |
| Evidence label | Executed |

## Results

| Metric | Value |
|--------|------:|
| N | 12 |
| Incomplete handoff rate (no enforcement) | 0.83 |
| Incomplete handoff rate (with enforcement) | 0.00 |
| Incomplete delta | 0.83 |
| Allowed conversion rate (with enforcement) | 0.17 |
| Wrong rate (with enforcement) | 0.00 |
| Hypothesis supported | Yes |

## Interpretation

Enforcement blocks incomplete handoffs (incomplete-through rate falls to 0). Some conversion is deferred (allowed 0.17 on this corpus) rather than killed to zero; wrong rate stays 0.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s6/WP-33-required-field-enforcement-handoffs.md` |
| Experiment log | `docs/experiment-log.md` |
