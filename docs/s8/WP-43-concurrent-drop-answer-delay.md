# S8 - Test concurrent session drop and answer-delay limits

**YouTrack:** WP-43  
**Sprint:** S8 - Concurrency and latency (U3) (16-27 Mar 2026)  
**Date recorded:** 2026-03-17  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 668h (Testing)  
**Ideal days:** 84  
**Status:** Complete

## Purpose

Hypothesis: concurrent sessions beyond N cause drop or excess answer delay. Log break-point N and provider configs.

## Hypothesis

| ID | Statement |
|----|-----------|
| H-S8-01 | Concurrent sessions beyond N cause drop or excess answer delay. |

## Thresholds (from WP-42 draft)

| Metric | Limit |
|--------|------:|
| max answer delay | 8.0 s |
| max drop rate | 0.0 |
| stuck sessions allowed | 0 |

## Provider configs

### Executed

| Setting | Value |
|---------|--------|
| Numbering | Business number forward to Workphone lab path (WP-7/WP-10) |
| Session control | Ring-answer-greet-active-end (WP-8) |
| Harness | `workphone_lab concurrency-breakpoint` |
| Channel limit claimed | none (no production claim) |

### Planned

| Setting | Value |
|---------|--------|
| Alternate SIP trunk channel pool | Considered; not Confirmed |
| Confirmed concurrent channel limit | unset |

## Sweep results (Executed lab)

| N | max answer delay (s) | drop rate | Result |
|--:|---------------------:|----------:|--------|
| 2 | 2.20 | 0.00 | OK |
| 3 | 3.15 | 0.00 | OK |
| 4 | 4.10 | 0.00 | OK |
| 5 | 5.05 | 0.00 | OK |
| 6 | 8.45 | 0.17 | FAIL (excess delay + drop) |
| 7 | 11.85 | 0.29 | FAIL |
| 8 | 15.25 | 0.38 | FAIL |

## Break-point

| Field | Value |
|-------|------:|
| last_ok_n | 5 |
| break_point_n | 6 |
| H-S8-01 supported | Yes |

Break-point aligns with WP-42 lab soft cap (safe_n=5): beyond N=5, sessions drop or exceed answer-delay limit.

## Lab

```text
python -m workphone_lab concurrency-breakpoint
```

Config: `data/concurrency/breakpoint_config_v0.json`  
Export: `outputs/s8_concurrency_breakpoint.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s8/WP-43-concurrent-drop-answer-delay.md` |
| Config | `data/concurrency/breakpoint_config_v0.json` |
| Export | `outputs/s8_concurrency_breakpoint.json` |
| Experiment log | `docs/experiment-log.md` |
