# S2 - Stabilize greeting and human/voicemail fallback rules

**YouTrack:** WP-14  
**Sprint:** S2 - Telephony Hardening + Evidence Gate (29 Sep - 10 Oct 2025)  
**Date recorded:** 2025-10-06  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 142h (Development)  
**Ideal days:** 18  
**Status:** Complete

## Purpose

Stabilize greeting plus transfer-to-voicemail or human fallback rules. Record final config for the S2 telephony baseline.

## Hypothesis

A single locked greeting and fallback rule set covers business-hours and after-hours paths without conflicting transfers or silent dead-ends.

## Final config (Executed)

| Setting | Value |
|---------|--------|
| Greeting | Short trade-neutral open; company name; offer to take message or connect |
| Business hours human fallback | Transfer to configured human destination when requested or on escalate keyword |
| After-hours / unreachable human | Route to voicemail capture; confirm callback intent |
| No-answer / busy human | Fallback to voicemail after one attempt |
| Idle / no speech | Re-prompt once, then voicemail offer, then clean end |
| Evidence label | Executed |

## Stabilization checks

| Check | Result | Notes |
|-------|--------|-------|
| Greeting plays before any transfer | Pass | Consistent on S1/S2 path |
| Human transfer only when reachable | Pass | No fake human connect after-hours |
| Voicemail path when human unavailable | Pass | Message + callback intent logged |
| Abandoned mid-fallback | Pass | Aligns with WP-13 teardown |
| Config recorded for baseline pack | Pass | This note is the S2 source |

## Interpretation

Greeting and human/voicemail fallback rules are stable enough to freeze for the S2 telephony baseline pack (WP-15) and Evidence Gate.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s2/WP-14-stabilize-greeting-human-voicemail-fallback.md` |
| Experiment log | `docs/experiment-log.md` |
