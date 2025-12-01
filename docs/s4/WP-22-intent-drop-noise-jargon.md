# S4 - Measure intent drop under noise and trade jargon

**YouTrack:** WP-22  
**Sprint:** S4 - Noise / jargon corpus + Evidence Gate (1-12 Dec 2025)  
**Date recorded:** 2025-12-01  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 189h (Testing)  
**Ideal days:** 24  
**Status:** Complete

## Purpose

Hypothesis: noise plus trade jargon drops intent accuracy below the clean S3 baseline by a measurable delta. Log configs and score tables for U1.

## Hypothesis

H-S4-01: Under job-site noise and trade jargon, intent accuracy drops vs clean S3 baseline by a measurable delta.

## Config (Executed)

| Setting | Value |
|---------|--------|
| Clean pack | `data/scripts/wp_scr_v0.json` (WP-17 / WP-18) |
| Noise+jargon pack | `data/scripts/wp_scr_v0_noise_jargon.json` |
| Lab command | `python -m workphone_lab noise-jargon` |
| Export | `outputs/s4_noise_jargon_scores.json` |
| Evidence label | Executed |

## Score table

| Condition | Intent pass | N | Intent accuracy |
|-----------|-------------|---|-----------------|
| Clean S3 baseline | 5 | 5 | 1.00 |
| Noise + jargon | 1 | 5 | 0.20 |
| **Delta (clean - stressed)** | | | **0.80** |

### Per-script (noise + jargon)

| Script | Expected | Predicted | Intent OK | Class |
|--------|----------|-----------|-----------|-------|
| SCR-E01-NJ | estimate | callback | N | E-Jargon |
| SCR-S01-NJ | service | unknown | N | E-Num / drop |
| SCR-A01-NJ | estimate | unknown | N | E-Omit |
| SCR-I01-NJ | service | unknown | N | E-Overlap / drop |
| SCR-C01-NJ | callback | callback | Y | - |

## Result vs hypothesis

| Check | Result |
|-------|--------|
| Measurable delta vs S3 | Pass (0.80) |
| H-S4-01 supported | Yes |
| Configs + score tables retained | Yes (JSON + this note) |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s4/WP-22-intent-drop-noise-jargon.md` |
| JSON export | `outputs/s4_noise_jargon_scores.json` |
| Experiment log | `docs/experiment-log.md` |
