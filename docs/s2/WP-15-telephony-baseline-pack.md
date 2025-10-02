# S2 - Assemble telephony baseline pack configs and call table

**YouTrack:** WP-15  
**Sprint:** S2 - Telephony Hardening + Evidence Gate (29 Sep - 10 Oct 2025)  
**Date recorded:** 2025-10-02  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 45h (Documentation)  
**Ideal days:** 6  
**Status:** Complete

## Purpose

Build telephony baseline pack: configs, call table, and failure modes. Prepare M2 pack for Evidence Gate review.

## Pack scope (M2)

| Section | Source cards | Status |
|---------|--------------|--------|
| Forward / answer path | WP-7 | Present |
| Session lifecycle | WP-8 | Present |
| Latency / failure-to-answer | WP-9 | Present |
| Executed vs Planned stack | WP-10 | Present |
| Negative-finding register | WP-11 | Present |
| After-hours / weekend | WP-12 | Present |
| Abandoned / rapid re-dial | WP-13 | Present |
| Greeting / human / voicemail fallback | WP-14 | Present |

## Locked configs (index)

| Config item | Value / pointer |
|-------------|-----------------|
| Business-number forward | WP-7 Executed path |
| Ring-answer-greet-end | WP-8 lifecycle settings |
| Greeting + fallback rules | WP-14 final config |
| After-hours policy | WP-12 policy table |
| Evidence label | Executed (S1/S2 telephony path) |

## Call table (summary)

| Scenario family | N (logged) | Primary outcome | Evidence |
|-----------------|------------|-----------------|----------|
| Business-hours forward answer | WP-7/WP-9 set | Answer + greet | WP-7, WP-9 |
| Answer latency / FTA | N=20 (WP-9) | Latency + causes logged | WP-9 |
| After-hours / weekend | WP-12 set | Pass vs policy | WP-12 |
| Abandoned / rapid re-dial | WP-13 set | No stuck sessions | WP-13 |
| Human / voicemail fallback | WP-14 checks | Pass | WP-14 |

## Failure modes retained

| ID | Mode | Pack section |
|----|------|--------------|
| NF-T01 to NF-T05 | Rejected telephony settings | WP-11 register |
| WP-13 tear-down | Abandoned / burst re-dial | Call table |
| WP-14 unreachable human | Voicemail fallback (not fake human) | Configs |

## M2 readiness for Evidence Gate

| Check | Result |
|-------|--------|
| Configs indexed with paths | Pass |
| Call table covers S1+S2 families | Pass |
| Failure modes linked | Pass |
| Ready for WP-16 Evidence Gate review | Pass |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s2/WP-15-telephony-baseline-pack.md` |
| Experiment log | `docs/experiment-log.md` |
