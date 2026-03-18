# S8 - Measure queue drop and error rates under load

**YouTrack:** WP-44  
**Sprint:** S8 - Concurrency and latency (U3) (16-27 Mar 2026)  
**Date recorded:** 2026-03-18  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 337h (Testing)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Measure queue/drop/error rates under concurrency. Retain provider logs for the U3 concurrency pack.

## Config (Executed)

| Setting | Value |
|---------|--------|
| U3 pack | WP-U3-CONCURRENCY |
| Safe N | 5 (WP-42/WP-43) |
| Queue depth limit | 5 |
| Load points | LOAD-2, LOAD-3, LOAD-N, LOAD-BP (N=6) |
| Config | `data/concurrency/queue_rates_config_v0.json` |
| Command | `python -m workphone_lab concurrency-queue` |
| Evidence label | Executed |

## Error classes

| ID | Description |
|----|-------------|
| E-QUEUE-FULL | Inbound invite rejected; queue at depth limit |
| E-DROP | Session dropped / rejected under concurrency |
| E-ANSWER-TIMEOUT | Answer delay exceeded before connect |
| E-PROVIDER-BLIP | Transient provider error on Executed forward path |

## Results by load point

| Load | N | Answered | Drop rate | Error rate |
|------|--:|---------:|----------:|-----------:|
| LOAD-2 | 2 | 2/2 | 0.00 | 0.00 |
| LOAD-3 | 3 | 3/3 | 0.00 | 0.00 |
| LOAD-N | 5 | 5/5 | 0.00 | 0.00 |
| LOAD-BP | 6 | 5/6 | 0.17 | 0.17 |

## Aggregate (U3 pack)

| Metric | Value |
|--------|------:|
| Offered | 16 |
| Answered | 15 |
| Drops / errors | 1 |
| Queue drop rate | 0.0625 |
| Error rate | 0.0625 |
| Answer rate | 0.9375 |

At and below soft cap (N<=5) drop/error rates stay 0. Break-point load (N=6) contributes the retained failure (E-ANSWER-TIMEOUT).

## Provider logs retained

| Artifact | Path |
|----------|------|
| Rates export | `outputs/s8_concurrency_queue_rates.json` |
| Provider log archive | `outputs/s8_u3_concurrency_provider_logs.json` |
| Pack index | `data/concurrency/u3_concurrency_pack_v0.json` |

16 provider log rows retained (ts, n, leg, event, error_class, queue_depth, detail).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s8/WP-44-queue-drop-error-rates.md` |
| Experiment log | `docs/experiment-log.md` |
