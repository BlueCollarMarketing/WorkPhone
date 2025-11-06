# S3 - Record Executed provider and model settings

**YouTrack:** WP-20  
**Sprint:** S3 - ASR / NLU baseline (3-14 Nov 2025)  
**Date recorded:** 2025-11-06  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 22h (Documentation)  
**Ideal days:** 3  
**Status:** Complete

## Purpose

Record Executed provider/model settings and list Planned alternatives. Keep Executed / Planned / Confirmed evidence labels for S3 evidence.

## Executed settings (S3 ASR/NLU)

| Layer | Setting | Label | Notes |
|-------|---------|-------|-------|
| Script pack | WP-SCR-v0 | Executed | WP-17 |
| ASR path | Speech-to-text on S3 stack used for WP-18 scoring | Executed | WP-18 |
| NLU path | Intent + entity extract on ASR text | Executed | WP-18 |
| Audio condition | Clean / studio-style reads | Executed | Pre-S4 noise pack |
| Error taxonomy | E-Jargon / E-Num / E-Overlap (+ omit/invent/intent) | Executed | WP-19 |
| Telephony substrate | S1/S2 Executed forward + lifecycle | Executed | WP-10, WP-14 |

## Planned alternatives (not claimed as Executed)

| Alternative | Why considered | Label |
|-------------|----------------|-------|
| Alternate ASR vendor / model tier | Latency or jargon accuracy comparison | Planned |
| Alternate NLU / LLM intent layer | Stronger entity packing on incomplete calls | Planned |
| Job-site noise-augmented audio as S3 baseline | Premature; belongs in S4 (WP-22/WP-23) | Planned (deferred) |
| Treating marketing model claims as Confirmed | No gate archive yet | Rejected as Executed |

## Evidence label rules (S3)

| Label | Practice |
|-------|----------|
| Executed | Provider/model path actually used in WP-18/WP-19 with retained scores |
| Planned | Considered or deferred; not used for U1 baseline claims |
| Confirmed | Reserved for Evidence Gate acceptance with exports (later cards) |

## Interpretation

U1 ASR/NLU claims for S3 must cite Executed rows only. Planned alternatives stay listed so they are not silently re-labeled as Executed.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s3/WP-20-executed-provider-model-settings.md` |
| Experiment log | `docs/experiment-log.md` |
