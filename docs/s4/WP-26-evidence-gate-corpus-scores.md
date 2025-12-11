# S4 - Evidence Gate corpus scores and rejected configs

**YouTrack:** WP-26  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-12-11  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 45h (Documentation)  
**Ideal days:** 6  
**Status:** Complete - S4 close

## Purpose

Complete Evidence Gate for corpus, score tables, and rejected configs. Mark Present / Missing / Location for S4 close.

## Evidence Gate checklist (S4)

| Item | Present / Missing | Location |
|------|-------------------|----------|
| Clean script pack WP-SCR-v0 | Present | `data/scripts/wp_scr_v0.json` |
| Noise/jargon variant pack | Present | `data/scripts/wp_scr_v0_noise_jargon.json` |
| Regression corpus manifest | Present | `data/corpus/regression_corpus.json` |
| S3 baseline score table | Present | `outputs/s3_baseline_scores.json` (lab) |
| S4 hypothesis log | Present | `docs/s4/WP-21-hypothesis-log-s4-noise-jargon.md` |
| Noise/jargon score + delta | Present | `docs/s4/WP-22-intent-drop-noise-jargon.md` |
| Corpus version tags note | Present | `docs/s4/WP-23-noise-jargon-regression-corpus.md` |
| Clarification-loop outcomes | Present | `docs/s4/WP-24-clarification-loop-low-confidence.md` |
| OTS vs Workphone delta table | Present | `docs/s4/WP-25-ots-vs-workphone-side-by-side.md` |
| Error taxonomy (S3) | Present | `docs/s3/WP-19-asr-nlu-error-taxonomy.md` |
| Executed provider/model settings | Present | `docs/s3/WP-20-executed-provider-model-settings.md` |
| Rejected telephony settings (S1) | Present | `docs/s1/WP-11-negative-finding-register-telephony.md` |
| Raw job-site audio archive (all calls) | Missing | Not claimed; lab ASR text only |
| Production ASR vendor Confirmed export | Missing | Planned until Confirmed gate |

## Rejected configs (S4)

| ID | Rejected config | Reason |
|----|-----------------|--------|
| RJ-S4-01 | Treat noise/jargon pack as clean baseline | Breaks S3 comparison; keep version links |
| RJ-S4-02 | Mark E-Invent cases as pass | U1 invent = defect |
| RJ-S4-03 | Claim OTS parity without delta table | WP-25 Executed delta required |
| RJ-S4-04 | Skip clarification harms logging | H-S4-04 needs helps/harms/no_change |

## Lab command

```text
python -m workphone_lab gate-s4
```

Writes `outputs/s4_evidence_gate.json`. Gate pass when no hard-missing docs/packs.

## S4 close decision

| Gate | Decision |
|------|----------|
| Corpus + score tables | Pass |
| Rejected configs retained | Pass |
| S4 sprint close | Closed - proceed to S5 dialogue policy |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-26-evidence-gate-corpus-scores.md` |
| Experiment log | `docs/experiment-log.md` |
