# S5 - Enforce corpus gate before bulk policy changes

**YouTrack:** WP-31  
**Sprint:** S5 - Dialogue policy + corpus gate (5-16 Jan 2026)  
**Date recorded:** 2026-01-14  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 405h (Documentation)  
**Ideal days:** 51  
**Status:** Complete - M3 gate recorded

## Purpose

Corpus gate: no bulk production policy change without an approved corpus version. Tag corpus and record gate decision for M3.

## Rule

No bulk production policy change without an approved corpus version.

## Corpus tag (approved)

| Field | Value |
|-------|--------|
| Corpus ID | WP-REG-CORPUS |
| Version | v0.1 |
| Gate tag | approved@v0.1 |
| Approved for | M3 |
| Baseline | WP-SCR-v0 @ v0 |
| Variants | WP-SCR-v0-NJ @ v0-noise-jargon |
| Manifest | `data/corpus/regression_corpus.json` |

## Gate config

`data/gates/corpus_gate_m3.json`

## M3 gate decision (Executed)

| Check | Result |
|-------|--------|
| Corpus version matches approved tag | Pass |
| Policy under gate = WP-DIALOGUE-v0 @ v0 | Pass |
| Bulk change with approved corpus | **PASS** |
| Bulk change with unapproved corpus (demo) | **BLOCKED** |

## Lab

```text
python -m workphone_lab corpus-gate
```

Writes `outputs/s5_corpus_gate_m3.json`.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s5/WP-31-corpus-gate-bulk-policy-m3.md` |
| Experiment log | `docs/experiment-log.md` |
