# S3 - Run ASR/NLU baseline and score intent capture

**YouTrack:** WP-18  
**Sprint:** S3 - ASR / NLU baseline (3-14 Nov 2025)  
**Date recorded:** 2025-11-04  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 189h (Testing)  
**Ideal days:** 24  
**Status:** Complete

## Purpose

Run ASR/NLU baseline on clean construction scripts. Score intent and entity capture; retain Executed model settings for U1 evidence.

## Hypothesis

On WP-SCR-v0 clean scripts, the Executed ASR/NLU path captures primary intent and required entities well enough to baseline U1 before noise/jargon stress (S4).

## Executed model settings

| Setting | Value |
|---------|--------|
| Script pack | WP-SCR-v0 (WP-17) |
| Audio | Clean / studio-style test reads (no job-site noise pack) |
| ASR path | Executed speech-to-text on S3 stack |
| NLU path | Intent + entity extract on ASR text |
| Scoring | Intent match; entity presence vs script must-capture |
| Evidence label | Executed |

## Scores (WP-SCR-v0)

| Script | Intent OK | Entities OK | Notes |
|--------|-----------|-------------|-------|
| SCR-E01 Estimate | Y | Y | Job type + callback captured |
| SCR-S01 Service | Y | Y | Urgency retained |
| SCR-A01 After-hours | Y | Y | After-hours flag set; no false human claim |
| SCR-I01 Incomplete | Y | Partial | Missing address not invented; clarification path |
| SCR-C01 Callback-only | Y | Y | Callback intent; no forced full intake |

## Aggregate

| Metric | Result |
|--------|--------|
| Intent capture (5/5) | Pass |
| Full entity capture | 4/5 full; 1/5 partial (SCR-I01 by design) |
| Invented fields | None observed on clean set |
| U1 baseline usable | Yes - settings retained below |

## Settings retained for U1 evidence

| Artifact | Note |
|----------|------|
| Model / path label | Executed ASR/NLU on clean WP-SCR-v0 |
| Score table | This note |
| Next | Error taxonomy (WP-19); provider record (WP-20) |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s3/WP-18-asr-nlu-baseline-intent-capture.md` |
| Experiment log | `docs/experiment-log.md` |
