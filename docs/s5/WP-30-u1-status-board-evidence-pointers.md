# S5 - Update U1 status board with evidence pointers

**YouTrack:** WP-30  
**Sprint:** S5 - Dialogue policy + corpus gate (5-16 Jan 2026)  
**Date recorded:** 2026-01-13  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 337h (Documentation)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Update U1 status (Open/Partial) with evidence pointers from S3–S5 speech and dialogue work. Keep evidence labels.

## Status board update (v0.2)

| ID | Prior (WP-4) | Now | Notes |
|----|--------------|-----|-------|
| **U1** | Open | **Partial** | Clean speech/intent evidenced; noise/jargon still degrades; not Confirmed closed |
| U2 | Open | Open | S5 policy/intake started; board focus this card is U1 |
| U3 | Open | Open | Concurrency/summaries not started |
| System | Open | Open | Lab runnable; production carrier not Confirmed |

## U1 evidence pointers (labels kept)

| Card | Label | Pointer |
|------|-------|---------|
| WP-18 | Executed | Clean ASR/NLU baseline intent scores |
| WP-19 | Executed | Error taxonomy E-Jargon / E-Num / E-Overlap |
| WP-20 | Executed | Executed provider/model settings |
| WP-22 | Executed | Noise+jargon intent drop vs clean (delta logged) |
| WP-23 | Executed | Regression corpus variants linked to WP-SCR-v0 |
| WP-24 | Executed | Clarification-loop helps / harms / no_change |
| WP-25 | Executed | OTS vs Workphone delta table |
| WP-26 | Executed | S4 Evidence Gate Present / Missing |
| WP-29 | Executed | Policy/corpus routing under speech stress (related) |

## Machine-readable board

`data/status/u1_u3_status_board.json`

```text
python -m workphone_lab status-board
```

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s5/WP-30-u1-status-board-evidence-pointers.md` |
| Prior board | `docs/s0/WP-04-u1-u3-statements-status-board.md` |
| Experiment log | `docs/experiment-log.md` |
