# S7 - Measure summary field accuracy invent and omit rates

**YouTrack:** WP-38  
**Sprint:** S7 - Post-call email summaries (23 Feb - 6 Mar 2026)  
**Date recorded:** 2026-02-24  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Testing)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Hypothesis: summary field accuracy meets target on corpus; invent/omit rates logged. Score against ground-truth call notes.

## Hypothesis

| ID | Statement |
|----|-----------|
| H-S7-01 | Summary field accuracy meets target on corpus; invent and omit rates are logged against ground-truth call notes. |

## Targets (Executed)

| Metric | Target |
|--------|--------|
| Field accuracy | >= 0.80 |
| Invent rate | <= 0.00 |

## Config (Executed)

| Setting | Value |
|---------|--------|
| Template | WP-SUMMARY-EMAIL @ v0 (D-05) |
| Ground-truth pack | `data/summary/ground_truth_call_notes_v0.json` |
| Corpus notes | SCR-E01/S01/A01/I01/C01 + schema emergency |
| Score fields | caller, number, need, urgency, next_step |
| Command | `python -m workphone_lab measure-summary` |
| Export | `outputs/s7_summary_field_accuracy.json` |
| Evidence label | Executed |

## Scoring rules

| Class | Meaning |
|-------|---------|
| correct | Predicted matches ground truth |
| correct_absent | Both absent (no invent, no omit) |
| omit | Ground truth present; predicted MISSING |
| invent | Ground truth absent; predicted filled |
| wrong | Both present but mismatch |

## Results

| Metric | Value |
|--------|------:|
| N notes | 6 |
| N field slots | 30 |
| Field accuracy | 1.00 |
| Invent rate | 0.00 |
| Omit rate (on present GT) | 0.00 |
| H-S7-01 supported | Yes |

## Interpretation

Lab summarizer hits target on the ground-truth note pack with zero invents. Incomplete (I01) and callback-only (C01) notes stay absent where GT is null. Omit rate logged at 0 on this Executed pack.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s7/WP-38-summary-field-accuracy-invent-omit.md` |
| Ground-truth notes | `data/summary/ground_truth_call_notes_v0.json` |
| Export | `outputs/s7_summary_field_accuracy.json` |
| Experiment log | `docs/experiment-log.md` |
