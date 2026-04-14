# S9 - Test two trade profiles for distinct agent behaviour

**YouTrack:** WP-48  
**Sprint:** S9 - Onboarding to live agent (13-24 Apr 2026)  
**Date recorded:** 2026-04-14  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Testing)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Hypothesis: two different trade profiles produce distinct correct agent behaviour on the same scripts. Retain side-by-side evidence.

## Hypothesis

| ID | Statement |
|----|-----------|
| H-S9-01 | Two different trade profiles produce distinct correct agent behaviour on the same scripts. |

## Profiles (Executed)

| Profile | ID | Trade | After-hours | Voice style |
|---------|----|-------|-------------|-------------|
| Summit Roofing Co | PROFILE-ROOF | roofing | answer | neutral |
| Harbor Plumbing | PROFILE-PLUMB | plumbing | forward | friendly |

Same script pack: WP-SCR-v0 (SCR-E01..C01).

## Side-by-side results

| Script | Distinct | Roofing path | Plumbing path | After-hours |
|--------|:--------:|--------------|---------------|-------------|
| SCR-E01 | Yes | roof_estimate_intake | plumb_estimate_intake | n/a |
| SCR-S01 | Yes | roof_repair_intake | plumb_repair_intake | n/a |
| SCR-A01 | Yes | roof_after_hours_answer | plumb_after_hours_forward | answer / forward |
| SCR-I01 | Yes | roof_clarify_trade | plumb_clarify_trade | n/a |
| SCR-C01 | Yes | roof_callback_queue | plumb_callback_queue | n/a |

| Metric | Value |
|--------|------:|
| N scripts | 5 |
| Distinct on all | Yes |
| Both correct on all | Yes |
| H-S9-01 supported | Yes |

## Lab

```text
python -m workphone_lab trade-profiles
```

Config: `data/onboarding/trade_profiles_v0.json`  
Export: `outputs/s9_trade_profiles_side_by_side.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s9/WP-48-trade-profiles-side-by-side.md` |
| Experiment log | `docs/experiment-log.md` |
