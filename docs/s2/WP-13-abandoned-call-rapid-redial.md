# S2 - Test abandoned-call and rapid re-dial handling

**YouTrack:** WP-13  
**Sprint:** S2 - Telephony Hardening + Evidence Gate (29 Sep - 10 Oct 2025)  
**Date recorded:** 2025-09-30  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 16h (Testing)  
**Status:** Complete

## Purpose

Hypothesis-test abandoned-call and rapid re-dial handling. Confirm no silent stuck sessions; log outcomes for S2.

## Hypothesis

Abandoned calls and rapid re-dials on the S1/S2 path tear down cleanly (no stuck sessions) and allow a new session on re-dial.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Path | WP-7/WP-8 lifecycle + WP-12 after-hours path |
| Cases | Mid-ring abandon; mid-greet hangup; re-dial within 5s / 30s |
| Evidence label | Executed |

## Results

| Case | Stuck session? | Re-dial OK? | Notes |
|------|----------------|-------------|-------|
| Abandon during ring | No | Y | Prior invite cleared |
| Hangup during greeting | No | Y | Idle end fired |
| Re-dial within 5s | No | Y | New session ID |
| Re-dial within 30s | No | Y | New session ID |
| Double re-dial burst | No | Y | No orphan session observed |

## Interpretation

No silent stuck sessions in the tested set. Outcomes feed greeting/fallback stabilization and the S2 telephony baseline pack.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s2/WP-13-abandoned-call-rapid-redial.md` |
| Experiment log | `docs/experiment-log.md` |
