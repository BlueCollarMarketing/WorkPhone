# S6 - Run negative intake cases refuse info partial address callback

**YouTrack:** WP-35  
**Sprint:** S6 - Intake field model and handoff (26 Jan - 6 Feb 2026)  
**Date recorded:** 2026-01-28  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 337h (Testing)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Run negative cases: caller refuses info, partial address, callback request. Confirm safe handling with no fabricated fields.

## Cases (Executed)

| ID | Case | Safe handling rule |
|----|------|--------------------|
| NEG-REFUSE | Caller refuses address/last name | Keep phone/callback; do not invent address |
| NEG-PARTIAL-ADDR | Landmark only, no street number | Mark address missing; keep site_area partial |
| NEG-CALLBACK | Callback-only | Name/phone/callback only; no invented job/urgency |

## Results

| ID | Pass | Notes |
|----|------|-------|
| NEG-REFUSE | Pass | No fabricated address |
| NEG-PARTIAL-ADDR | Pass | Address marked missing/partial |
| NEG-CALLBACK | Pass | No invented job_type/urgency |
| **Aggregate** | **3/3** | **safe_no_fabricate=True** |

## Lab

```text
python -m workphone_lab negative
```

Pack: `data/intake/negative_intake_cases_v0.json`  
Export: `outputs/s6_negative_intake.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s6/WP-35-negative-intake-cases.md` |
| Experiment log | `docs/experiment-log.md` |
