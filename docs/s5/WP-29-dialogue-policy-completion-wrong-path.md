# S5 - Measure dialogue policy completion and wrong-path rate

**YouTrack:** WP-29  
**Sprint:** S5 - Dialogue policy + corpus gate (5-16 Jan 2026)  
**Date recorded:** 2026-01-08  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 668h (Testing)  
**Ideal days:** 84  
**Status:** Complete

## Purpose

Run dialogue policy against the versioned corpus. Measure completion and wrong-path rate for U2 evidence.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Policy | WP-DIALOGUE-v0 @ v0 |
| Corpus | WP-SCR-v0 @ v0 + WP-SCR-v0-NJ @ v0-noise-jargon |
| Command | `python -m workphone_lab measure-policy` |
| Export | `outputs/s5_policy_completion_wrong_path.json` |
| Evidence label | Executed |

## Aggregate (U2)

| Metric | Value |
|--------|------:|
| N (scripts) | 12 |
| Mean field completion | 0.48 |
| Fully complete rate | 0.00 |
| Wrong-path count | 8 |
| **Wrong-path rate** | **0.67** |

## Score table (sample)

| Script | Expected | Routed | Wrong-path | Completion |
|--------|----------|--------|------------|------------|
| SCR-E01 | estimate | estimate | N | 0.80 |
| SCR-S01 | estimate | inquiry | Y | 0.33 |
| SCR-A01 | estimate | estimate | N | 0.60 |
| SCR-I01 | estimate | inquiry | Y | 0.67 |
| SCR-C01 | inquiry | inquiry | N | 0.67 |
| SCR-E01-NJ | estimate | inquiry | Y | 0.33 |
| SCR-S01-N | estimate | inquiry | Y | 0.00 |

(Full table in JSON export.)

## U2 interpretation

| Finding | Note |
|---------|------|
| Clean estimate scripts route better than service/noise variants | Service triggers not yet in estimate path list |
| High wrong-path under noise/jargon | Aligns with S4 intent drop; feeds WP-30/WP-31 corpus gate |
| Completion rarely full | Missing name/callback_window patterns on garbled ASR text |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s5/WP-29-dialogue-policy-completion-wrong-path.md` |
| Experiment log | `docs/experiment-log.md` |
