# S9 - Measure time-to-live from form submit to callable number

**YouTrack:** WP-50  
**Sprint:** S9 - Onboarding to live agent (13-24 Apr 2026)  
**Date recorded:** 2026-04-16  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 337h (Testing)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Measure time from onboarding form submit to a callable Workphone number. Record distribution for D-07.

## Metric definition

| Mark | Meaning |
|------|---------|
| t0 | `form_submit` (onboarding form accepted) |
| t1 | `callable_number` (lab number answers inbound invite) |
| ttl_s | t1 - t0 = validate + map + provision + smoke_ring |

## Config (Executed)

| Setting | Value |
|---------|--------|
| Deliverable | D-07 |
| Workstream | WS4 |
| Path | Executed lab (validate + map + stub provision + smoke ring) |
| N | 20 runs (roofing / plumbing) |
| Pack | `data/onboarding/time_to_live_runs_v0.json` |
| Command | `python -m workphone_lab time-to-live` |
| Evidence label | Executed |

## Draft working targets (D-07)

| Metric | Draft max |
|--------|----------:|
| p50 | 300 s |
| p95 | 900 s |

## Distribution (retained)

| Metric | Value (s) |
|--------|----------:|
| N | 20 |
| min | 47.5 |
| p50 | 63.4 |
| p90 | 96.82 |
| p95 | 104.54 |
| max | 128.1 |
| mean | 70.225 |
| Within draft targets | Yes |

### Histogram

| Bin (s) | Count |
|---------|------:|
| [0, 60) | 9 |
| [60, 90) | 7 |
| [90, 120) | 3 |
| [120, 180) | 1 |
| [180, 300) | 0 |
| [300, inf) | 0 |

## Lab

```text
python -m workphone_lab time-to-live
```

Export: `outputs/s9_time_to_live_distribution.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s9/WP-50-time-to-live-form-to-callable.md` |
| Experiment log | `docs/experiment-log.md` |
