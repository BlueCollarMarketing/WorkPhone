# S4 - Side-by-side OTS vs Workphone on same scripts

**YouTrack:** WP-25  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-12-09  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 54h (Testing)  
**Ideal days:** 7  
**Status:** Complete

## Purpose

Compare OTS generic agent vs Workphone path on the same scripts. Retain delta table as Executed evidence.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Scripts | WP-SCR-v0 clean pack (`data/scripts/wp_scr_v0.json`) |
| OTS path | Generic agent stub (`workphone_lab.ots_compare.score_ots`) |
| Workphone path | Lab NLU path (`workphone_lab.scoring`) |
| Command | `python -m workphone_lab compare-ots` |
| Export | `outputs/s4_ots_vs_workphone.json` |
| Evidence label | Executed |

## Aggregate delta

| Metric | OTS | Workphone | Delta (WP - OTS) |
|--------|-----|-----------|------------------|
| Intent pass | 1/5 | 5/5 | **+4** |
| Entity full | 0/5 | 4/5 | **+4** |

## Per-script delta table

| Script | OTS predicted | WP predicted | d_intent | d_entities |
|--------|---------------|--------------|----------:|-----------:|
| SCR-E01 | callback | estimate | +1 | +1 |
| SCR-S01 | unknown | service | +1 | +1 |
| SCR-A01 | callback | estimate | +1 | 0 |
| SCR-I01 | unknown | service | +1 | +1 |
| SCR-C01 | callback | callback | 0 | +1 |

## Interpretation

On the same clean construction scripts, Workphone outperforms OTS on intent and entity capture. Delta table retained as Executed U1 evidence (aligns with S0 OTS rejection).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-25-ots-vs-workphone-side-by-side.md` |
| Experiment log | `docs/experiment-log.md` |
