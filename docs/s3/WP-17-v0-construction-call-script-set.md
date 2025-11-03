# S3 - Build v0 construction call script set

**YouTrack:** WP-17  
**Sprint:** S3 - ASR / NLU baseline (3-14 Nov 2025)  
**Date recorded:** 2025-11-03  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 54h (Documentation)  
**Ideal days:** 7  
**Status:** Complete

## Purpose

Build v0 construction call scripts covering estimate, service, after-hours, and incomplete info. Version the pack for U1 baseline testing.

## Pack version

| Field | Value |
|-------|--------|
| Pack ID | WP-SCR-v0 |
| Version | v0 |
| Use | U1 ASR/NLU baseline (WP-18+) |
| Evidence label | Executed |

## Script set (v0)

| ID | Scenario | Caller goal | Must capture | Pass cue |
|----|----------|-------------|--------------|----------|
| SCR-E01 | Estimate | New job estimate (roofing / reno style) | Name, number, job type, site area, preferred callback | Intent = estimate; callback window noted |
| SCR-S01 | Service | Repair / maintenance booking | Name, number, issue, urgency, access notes | Intent = service; urgency not dropped |
| SCR-A01 | After-hours | Evening / weekend inbound | Same as estimate or service; after-hours flag | Answered; no false human-transfer claim |
| SCR-I01 | Incomplete info | Omits address or urgency | Partial fields; clarification or voicemail path | Does not invent missing address/urgency |
| SCR-C01 | Callback-only | Ask for callback, minimal detail | Name, number, callback intent | No forced full intake hallucination |

## Script text notes (v0)

| ID | Prompt outline |
|----|----------------|
| SCR-E01 | "Hi, I need an estimate for [trade job] at [area]. Can someone call me back tomorrow?" |
| SCR-S01 | "Something is leaking / broken. I need service this week. Number is [N]." |
| SCR-A01 | Same as E01 or S01 placed outside business hours on the WP-12 path |
| SCR-I01 | Gives name + need only; refuses or skips address when asked once |
| SCR-C01 | "Just have them call me back" with number; no job detail |

## Versioning rules

| Rule | Detail |
|------|--------|
| Immutable v0 | Do not edit SCR-* text in place after WP-18 scoring starts |
| Changes | New variants go to v0.1+ or S4 noise/jargon pack (WP-23) |
| Link to OTS | Aligns themes with S0 SCR-01 to SCR-05; IDs are WP-SCR-v0 |

## U1 baseline readiness

| Check | Result |
|-------|--------|
| Estimate / service / after-hours / incomplete covered | Pass |
| Pack versioned WP-SCR-v0 | Pass |
| Ready for ASR/NLU scoring (WP-18) | Pass |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s3/WP-17-v0-construction-call-script-set.md` |
| Experiment log | `docs/experiment-log.md` |
