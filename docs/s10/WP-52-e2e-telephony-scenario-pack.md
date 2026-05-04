# S10 - Run end-to-end telephony scenario pack

**YouTrack:** WP-52  
**Sprint:** S10 - E2E Assembly + Evidence Pack (4-15 May 2026)  
**Date recorded:** 2026-05-04  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 663h (Testing)  
**Ideal days:** 83  
**Status:** Complete

## Purpose

Run E2E scenarios (happy path, noise, incomplete intake, concurrent). Capture outcomes for D-08 system assembly notes.

## Pack

| Field | Value |
|-------|--------|
| Pack ID | WP-E2E-TELEPHONY |
| Version | v0 |
| Deliverable | D-08 |
| Config | `data/e2e/telephony_scenario_pack_v0.json` |
| Command | `python -m workphone_lab e2e-scenarios` |
| Evidence label | Executed |

## Path (Executed)

Ring-answer-greet-active-end + ASR/NLU stub + intake/handoff enforcement + concurrency capacity model. Lab path only; live carrier not claimed.

## Scenario outcomes

| ID | Family | Outcome | Notes |
|----|--------|---------|-------|
| E2E-HAPPY | happy_path | pass | Intent accuracy 1.00; session complete; named callback converts |
| E2E-NOISE | noise | degraded_as_expected | Intent under noise/jargon stays <= 0.50; drop documented for D-08 |
| E2E-INCOMPLETE | incomplete_intake | pass | NEG cases safe (no fabricate); omit fields not invented |
| E2E-CONCURRENT | concurrent | pass | N=5 within limits; N=6 breaks (delay/drop) |

Pack: `scenarios=4 expect_met=4 pack_pass=True`

## Concurrent limits (aligned U3-LIMITS-v0)

| Limit | Value | Label |
|-------|------:|-------|
| safe_n | 5 | Executed |
| break_point_n | 6 | Executed |
| max answer delay | 8.0 s | Executed |

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-E2E-01 | Claim E2E live carrier pass from lab-only Executed path |
| RJ-E2E-02 | Treat noise degradation as pack failure when drop is documented for D-08 |
| RJ-E2E-03 | Ship D-08 without concurrent safe_n / break_point outcomes |

## D-08 assembly notes (pointers)

1. Happy path answers and routes clean estimate/service/callback; scripts without spoken name still need clarify before handoff.  
2. Noise/jargon degrades intent on the live-shaped path; retain as known system stress for assembly notes.  
3. Incomplete/refuse/partial stay safe (no invent); enforcement blocks incomplete full handoffs when fields missing.  
4. Concurrent load holds at safe_n=5; break_point_n=6 matches S8 evidence.

## Lab

```text
python -m workphone_lab e2e-scenarios
```

Export: `outputs/s10_e2e_telephony_scenario_pack.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s10/WP-52-e2e-telephony-scenario-pack.md` |
| Scenario pack | `data/e2e/telephony_scenario_pack_v0.json` |
| Export | `outputs/s10_e2e_telephony_scenario_pack.json` |
| Experiment log | `docs/experiment-log.md` |
