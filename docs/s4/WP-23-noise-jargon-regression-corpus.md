# S4 - Add noise and jargon variants to regression corpus

**YouTrack:** WP-23  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-12-02  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 54h (Documentation)  
**Ideal days:** 7  
**Status:** Complete

## Purpose

Add noise/jargon variants to the construction corpus. Keep version tags linked to the clean S3 baseline pack.

## Corpus versioning

| Field | Value |
|-------|--------|
| Corpus ID | WP-REG-CORPUS |
| Corpus version | v0.1 |
| Clean baseline pack | WP-SCR-v0 @ **v0** |
| Variant pack | WP-SCR-v0-NJ @ **v0-noise-jargon** |
| Link rule | Every variant `base_id` + `linked_baseline_version=v0` |
| Evidence label | Executed |

## Manifest paths

| Artifact | Path |
|----------|------|
| Corpus manifest | `data/corpus/regression_corpus.json` |
| Clean pack (S3) | `data/scripts/wp_scr_v0.json` |
| Noise/jargon pack | `data/scripts/wp_scr_v0_noise_jargon.json` |

## Variant index (linked to clean v0)

| Variant ID | Base (clean v0) | Tags |
|------------|-----------------|------|
| SCR-E01-NJ | SCR-E01 | noise:job_site, jargon:flashing, jargon:rough-in |
| SCR-S01-NJ | SCR-S01 | noise:job_site |
| SCR-A01-NJ | SCR-A01 | noise:phone_hiss, jargon:reno |
| SCR-I01-NJ | SCR-I01 | noise:overlap |
| SCR-C01-NJ | SCR-C01 | noise:static |
| SCR-E01-J | SCR-E01 | jargon:flashing, jargon:ridge_vent |
| SCR-S01-N | SCR-S01 | noise:crew_radio |

## Lab validation

```text
python -m workphone_lab corpus
```

Checks baseline file presence, `linked_baseline_version=v0`, and every `base_id` exists in the clean pack.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-23-noise-jargon-regression-corpus.md` |
| Experiment log | `docs/experiment-log.md` |
