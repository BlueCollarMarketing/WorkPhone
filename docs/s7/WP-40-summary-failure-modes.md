# S7 - Log summary failure modes delay wrong number hallucination

**YouTrack:** WP-40  
**Sprint:** S7 - Post-call email summaries (23 Feb - 6 Mar 2026)  
**Date recorded:** 2026-02-26  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 337h (Documentation)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Document failure modes: delayed email, wrong number, hallucinated service type. Keep invent cases as defects, not passes.

## Failure-mode library (U3)

| ID | Failure mode | Severity | U3 link |
|----|--------------|----------|---------|
| SF-DELAY | Delayed email after call_end | Major | Timeliness |
| SF-WRONG-NUM | Wrong callback number in summary | Critical | Accuracy |
| SF-HALLUC-SVC | Hallucinated / swapped service type | Critical | Accuracy |
| SF-INVENT | Invented field without GT support | Critical | Accuracy |

## Scoring rule (retained)

| ID | Rule |
|----|------|
| RJ-S7-01 | Invent / hallucinated service / wrong number are **defects**, never passes |
| RJ-S7-02 | Delayed email retained as SF-DELAY evidence for U3 (not ignored) |

## Probe set (Executed)

| Probe | Mode | Script | Result | Notes |
|-------|------|--------|--------|-------|
| SF-P01 | SF-DELAY | SCR-A01 | DEFECT | latency 19.5s >= alert 15s |
| SF-P02 | SF-WRONG-NUM | SCR-E01 | DEFECT (invent family) | 647-555-9999 vs 647-555-0101 |
| SF-P03 | SF-HALLUC-SVC | SCR-C01 | DEFECT (invent family) | need invented on callback-only |
| SF-P04 | SF-INVENT | SCR-I01 | DEFECT (invent family) | urgency invented on incomplete |

## Lab results

| Metric | Value |
|--------|------:|
| Probes | 4 |
| Defects | 4 |
| Invent-family defects | 3 |
| Invent scored as pass (violations) | 0 |
| Rule OK (RJ-S7-01) | Yes |

## Config

| Setting | Value |
|---------|--------|
| Library | `data/summary/summary_failure_modes_v0.json` |
| Command | `python -m workphone_lab summary-fm` |
| Export | `outputs/s7_summary_failure_modes.json` |
| Evidence label | Executed |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s7/WP-40-summary-failure-modes.md` |
| Library | `data/summary/summary_failure_modes_v0.json` |
| Export | `outputs/s7_summary_failure_modes.json` |
| Status board | `data/status/u1_u3_status_board.json` |
| Experiment log | `docs/experiment-log.md` |
