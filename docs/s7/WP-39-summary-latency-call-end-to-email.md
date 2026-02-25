# S7 - Measure summary latency from call end to email

**YouTrack:** WP-39  
**Sprint:** S7 - Post-call email summaries (23 Feb - 6 Mar 2026)  
**Date recorded:** 2026-02-25  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Testing)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Measure time from call end to email received. Retain latency distribution for U3 evidence.

## Metric definition

| Mark | Meaning |
|------|---------|
| t0 | `call_end` (session idle end) |
| t1 | `email_received` (summary accepted by stub inbox) |
| latency_s | t1 - t0 = render + queue + deliver |

## Config (Executed)

| Setting | Value |
|---------|--------|
| Path | Executed lab (template render + queue stub + email stub) |
| Template | WP-SUMMARY-EMAIL @ v0 |
| N | 20 runs |
| Pack | `data/summary/summary_latency_runs_v0.json` |
| Command | `python -m workphone_lab summary-latency` |
| Export | `outputs/s7_summary_latency_distribution.json` |
| Uncertainty | U3 |
| Evidence label | Executed |

## Draft working targets (U3)

| Metric | Draft max |
|--------|----------:|
| p50 | 30 s |
| p95 | 90 s |

Targets stay Draft until concurrency cards freeze tolerances.

## Distribution (retained)

| Metric | Value (s) |
|--------|----------:|
| N | 20 |
| min | 3.3 |
| p50 | 5.0 |
| p90 | 10.35 |
| p95 | 13.8 |
| max | 19.5 |
| mean | 6.44 |
| Within draft targets | Yes |

### Histogram

| Bin (s) | Count |
|---------|------:|
| [0, 5) | 10 |
| [5, 10) | 7 |
| [10, 15) | 2 |
| [15, 20) | 1 |
| [20, 30) | 0 |
| [30, inf) | 0 |

## U3 board update

U3 moved to **Partial**: summary fidelity (WP-38) + latency distribution (WP-39) on Executed path. Concurrency under load remains later (S8).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s7/WP-39-summary-latency-call-end-to-email.md` |
| Latency pack | `data/summary/summary_latency_runs_v0.json` |
| Distribution export | `outputs/s7_summary_latency_distribution.json` |
| Status board | `data/status/u1_u3_status_board.json` |
| Experiment log | `docs/experiment-log.md` |
