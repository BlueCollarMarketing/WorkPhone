# S10 - Document system-only failure modes from live path

**YouTrack:** WP-53  
**Sprint:** S10 - E2E Assembly + Evidence Pack (4-15 May 2026)  
**Date recorded:** 2026-05-05  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 254h (Documentation)  
**Ideal days:** 32  
**Status:** Complete

## Purpose

Record system failure notes for issues invisible in unit tests (drift, drops, summary/intake mismatches). File for D-08.

## Library

| Field | Value |
|-------|--------|
| Library ID | WP-SYS-FM |
| Version | v0 |
| Deliverable | D-08 |
| Config | `data/e2e/system_failure_modes_v0.json` |
| Command | `python -m workphone_lab system-fm` |
| Evidence label | Executed |

## Why unit tests miss these

| Gap | Detail |
|-----|--------|
| Isolated utterance | Clean ASR/NLU unit score does not see noise-path drift on the same base script |
| Single session | Ring-answer-greet-end demo never opens N concurrent legs |
| Split artifacts | Summary template and intake schema checks do not cross-compare the same call |
| Quiet load | Single-call invent/omit check skips fidelity under concurrency |

## Failure-mode library (system-only)

| ID | Failure mode | Severity | Invisible in |
|----|--------------|----------|--------------|
| SYS-DRIFT | Cross-stage ASR/NLU drift | Major | Per-utterance clean unit score |
| SYS-DROP | Concurrent session drop | Critical | Single-session lifecycle demo |
| SYS-SUM-INTAKE | Summary vs intake mismatch | Critical | Isolated summary or intake unit check |
| SYS-FIDELITY-LOAD | Summary fidelity collapse under load | Critical | Single-call summary invent/omit check |

## Scoring rule (retained)

| ID | Rule |
|----|------|
| RJ-S10-01 | System-only defects stay defects for D-08; unit-test pass does not clear them |

## Probe set (Executed)

| Probe | Mode | Result | Linked evidence |
|-------|------|--------|-----------------|
| SYS-P01 | SYS-DRIFT | DEFECT | WP-22, WP-52/E2E-NOISE |
| SYS-P02 | SYS-DROP | DEFECT | WP-43, WP-52/E2E-CONCURRENT |
| SYS-P03 | SYS-SUM-INTAKE | DEFECT | WP-38, WP-40, WP-33 |
| SYS-P04 | SYS-FIDELITY-LOAD | DEFECT | WP-45, WP-52/E2E-CONCURRENT |

## Lab results

| Metric | Value |
|--------|------:|
| Probes | 4 |
| Defects retained | 4 |
| Pass violations | 0 |
| Rule OK (RJ-S10-01) | Yes |
| Notes filed for D-08 | Yes |

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-S10-01 | Clear SYS-* defects because unit tests passed |
| RJ-S10-02 | File D-08 without system-only failure notes |
| RJ-S10-03 | Treat summary/intake mismatch as summary-only unit bug |

## Lab

```text
python -m workphone_lab system-fm
```

Export: `outputs/s10_system_failure_modes.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s10/WP-53-system-only-failure-modes.md` |
| Library | `data/e2e/system_failure_modes_v0.json` |
| Export | `outputs/s10_system_failure_modes.json` |
| Experiment log | `docs/experiment-log.md` |
