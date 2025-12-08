# S4 - Test clarification-loop prompts at low confidence

**YouTrack:** WP-24  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-12-08  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 142h (Testing)  
**Ideal days:** 18  
**Status:** Complete

## Purpose

Test clarification-loop prompts when confidence is low. Record helps / harms / no-change outcomes for U1.

## Hypothesis

H-S4-04: Clarification-loop prompts recover part of the S3-to-S4 intent gap at low confidence without inventing fields.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Pack | WP-SCR-v0-NJ (`v0-noise-jargon`) |
| Confidence threshold | 0.6 (below => ask clarify) |
| Lab command | `python -m workphone_lab clarify` |
| Export | `outputs/s4_clarification_loop.json` |
| Evidence label | Executed |

## Outcomes summary

| Outcome | Count | Meaning |
|---------|------:|---------|
| helps | 4 | Wrong/unknown before; correct after clarify |
| harms | 0 | Correct before; wrong after (or invent) |
| no_change | 3 | Same correctness, or confidence already high |

## Per-script table

| Script | Conf | Before -> After | Outcome |
|--------|------|-----------------|---------|
| SCR-E01-NJ | 0.41 | callback -> estimate | helps |
| SCR-S01-NJ | 0.25 | unknown -> service | helps |
| SCR-A01-NJ | 0.25 | unknown -> estimate | helps |
| SCR-I01-NJ | 0.25 | unknown -> service | helps |
| SCR-C01-NJ | 0.43 | callback -> callback | no_change |
| SCR-E01-J | 0.65 | (no ask) | no_change |
| SCR-S01-N | 0.61 | (no ask) | no_change |

## U1 interpretation

| Check | Result |
|-------|--------|
| Helps > harms on low-confidence set | Pass (4 vs 0) |
| Invent risk on incomplete path | None in Executed run |
| H-S4-04 supported | Yes (partial recovery, no harm) |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-24-clarification-loop-low-confidence.md` |
| Experiment log | `docs/experiment-log.md` |
