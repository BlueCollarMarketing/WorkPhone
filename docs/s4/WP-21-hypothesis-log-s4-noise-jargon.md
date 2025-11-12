# S4 - Write hypothesis log for S4 noise/jargon series

**YouTrack:** WP-21  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-11-12  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 22h (Documentation)  
**Ideal days:** 3  
**Status:** Complete

## Purpose

Write hypothesis log for the next noise/jargon experiment series (S4). Link S3 baseline scores as the comparison starting point.

## Comparison starting point (S3)

| Source | Path / note |
|--------|-------------|
| Clean-script scores | WP-18 (`docs/s3/WP-18-asr-nlu-baseline-intent-capture.md`) |
| Error taxonomy | WP-19 (`docs/s3/WP-19-asr-nlu-error-taxonomy.md`) |
| Executed settings | WP-20 (`docs/s3/WP-20-executed-provider-model-settings.md`) |
| Runnable baseline export | `python -m workphone_lab baseline` -> `outputs/s3_baseline_scores.json` |

## Hypothesis log (S4 series)

| ID | Hypothesis | Compare to S3 | Primary classes |
|----|------------|---------------|-----------------|
| H-S4-01 | Under job-site noise, intent capture drops vs clean S3 baseline; entity capture drops faster | WP-18 aggregate intent / entities | E-Overlap, E-Omit |
| H-S4-02 | Trade jargon variants raise E-Jargon mis-maps vs clean WP-SCR-v0 without changing true intent | WP-18 SCR-E01 / SCR-S01 intent_ok | E-Jargon |
| H-S4-03 | Spoken numbers/addresses under noise increase E-Num failures vs clean digit capture | WP-18 number entities | E-Num |
| H-S4-04 | Clarification-loop prompts recover part of the S3-to-S4 gap without inventing fields | WP-18 SCR-I01 invent=false | E-Invent, E-Omit |

## Runnable lab link

```text
python -m workphone_lab hypothesis-s4
```

Writes `outputs/s4_hypothesis_log.json` with the same IDs, linked to the S3 baseline export.

## Next experiments (S4)

| Card | Uses this log |
|------|----------------|
| WP-22 | Measure intent drop under noise/jargon |
| WP-23 | Add noise/jargon variants to corpus |
| WP-24 | Clarification-loop at low confidence |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-21-hypothesis-log-s4-noise-jargon.md` |
| JSON export | `outputs/s4_hypothesis_log.json` (generated) |
| Experiment log | `docs/experiment-log.md` |
