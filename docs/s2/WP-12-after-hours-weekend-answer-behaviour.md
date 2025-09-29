# S2 - Test after-hours and weekend answer behaviour

**YouTrack:** WP-12  
**Sprint:** S2 - Telephony Hardening + Evidence Gate (29 Sep - 10 Oct 2025)  
**Date recorded:** 2025-09-29  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 24h (Testing)  
**Status:** Complete

## Purpose

Experiment after-hours and weekend answer behaviour on the Workphone path. Log outcomes against expected policy for S2 evidence.

## Hypothesis

On the S1 baseline path (WP-7 to WP-11), after-hours and weekend inbound calls still answer and follow the documented greeting / idle-end policy.

## Expected policy (Draft)

| Condition | Expected behaviour |
|-----------|-------------------|
| Evening / night inbound | Answer; play greeting; open session |
| Weekend inbound | Same as after-hours |
| Outside business profile hours | Do not claim human transfer unless configured |

## Config (Executed)

| Setting | Value |
|---------|--------|
| Path | S1 forward + lifecycle (WP-7, WP-8) |
| Windows tested | Weeknight evening; Saturday sample window |
| Evidence label | Executed |

## Results

| Scenario | Outcome vs policy | Notes |
|----------|-------------------|-------|
| Weeknight after-hours | Pass | Answered; greeting started; session logged |
| Weeknight late | Pass | Answered; idle end clean |
| Saturday daytime | Pass | Answered; greeting started |
| Saturday evening | Partial | Answered with higher latency; logged for S2 pack |

## Interpretation

After-hours / weekend answer path works on the S1 stack with one latency edge case retained. Next: abandoned-call and re-dial handling (next S2 card).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s2/WP-12-after-hours-weekend-answer-behaviour.md` |
| Experiment log | `docs/experiment-log.md` |
