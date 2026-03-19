# S8 - Spot-check summary fidelity under concurrent load

**YouTrack:** WP-45  
**Sprint:** S8 - Concurrency and latency (U3) (16-27 Mar 2026)  
**Date recorded:** 2026-03-19  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 390h (Testing)  
**Ideal days:** 49  
**Status:** Complete

## Purpose

Spot-check summary fidelity while load tests run. Flag silent quality collapse; do not mark invent/omit as pass.

## Hypothesis

| ID | Statement |
|----|-----------|
| H-S8-02 | Summary fidelity holds under concurrent load at or below safe_n; silent invent/omit collapse is flagged and never marked pass. |

## Rule (retained)

| ID | Rule |
|----|------|
| RJ-S8-01 | Do not mark invent/omit as pass under concurrent load |

## Spot-checks

| ID | Load | N | Mode | Accuracy | Invent | Collapse flagged | Check |
|----|------|--:|------|---------:|-------:|:----------------:|-------|
| FID-LOAD-2 | LOAD-2 | 2 | faithful | 1.00 | 0 | no | Pass |
| FID-LOAD-3 | LOAD-3 | 3 | faithful | 1.00 | 0 | no | Pass |
| FID-LOAD-N | LOAD-N | 5 | faithful | 1.00 | 0 | no | Pass |
| FID-LOAD-BP-COLLAPSE | LOAD-BP | 6 | collapse_probe | 0.60 | 3 | **yes** | Pass (flagged) |

Faithful path holds through soft cap (N<=5). Overload collapse probe invents need/urgency on callback/incomplete notes; invents stay defects and collapse is flagged.

## Lab

```text
python -m workphone_lab concurrency-fidelity
```

Config: `data/concurrency/summary_fidelity_under_load_v0.json`  
Export: `outputs/s8_summary_fidelity_under_load.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s8/WP-45-summary-fidelity-under-load.md` |
| Experiment log | `docs/experiment-log.md` |
