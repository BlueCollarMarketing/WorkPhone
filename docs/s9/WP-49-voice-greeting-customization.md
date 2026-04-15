# S9 - Test voice selection and greeting customization

**YouTrack:** WP-49  
**Sprint:** S9 - Onboarding to live agent (13-24 Apr 2026)  
**Date recorded:** 2026-04-15  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 337h (Testing)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Test voice selection and greeting customization per business profile. Log accepted configs and failures for WS4.

## Scope (WS4)

| Field | Value |
|-------|--------|
| Workstream | WS4 |
| Deliverable | D-07 |
| Pack | `data/onboarding/voice_greeting_cases_v0.json` |
| Evidence label | Executed |

## Allowed catalog (Executed)

| voice_id | Allowed styles |
|----------|----------------|
| voice_trade_neutral_01 | neutral, formal |
| voice_trade_friendly_01 | friendly, neutral |
| voice_trade_formal_01 | formal |

Greeting must include business name after placeholder resolve; empty greetings rejected.

## Accepted configs (WS4 log)

| Case | Profile | Voice / style | Result |
|------|---------|---------------|--------|
| VG-OK-ROOF | PROFILE-ROOF | voice_trade_neutral_01 / neutral | Accept |
| VG-OK-PLUMB | PROFILE-PLUMB | voice_trade_friendly_01 / friendly | Accept |

## Failures retained (WS4 log)

| Case | Failure |
|------|---------|
| VG-FAIL-UNKNOWN-VOICE | voice_id not in allowed catalog |
| VG-FAIL-STYLE-MISMATCH | voice_style not allowed for voice_id |
| VG-FAIL-EMPTY-GREETING | greeting empty after trim |
| VG-FAIL-MISSING-BIZ | greeting missing business_name |

| Metric | Value |
|--------|------:|
| Cases | 6 |
| Accepted | 2 |
| Failed | 4 |
| Expect matched | 6/6 |

## Lab

```text
python -m workphone_lab voice-greeting
```

Export: `outputs/s9_voice_greeting_ws4.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s9/WP-49-voice-greeting-customization.md` |
| Experiment log | `docs/experiment-log.md` |
