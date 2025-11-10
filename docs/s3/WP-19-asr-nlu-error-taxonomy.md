# S3 - Classify ASR/NLU error taxonomy

**YouTrack:** WP-19  
**Sprint:** S3 - ASR / NLU baseline (3-14 Nov 2025)  
**Date recorded:** 2025-11-10  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 95h (Investigation)  
**Ideal days:** 12  
**Status:** Complete

## Purpose

Classify errors across jargon, numbers/addresses, and overlapping speech. Document top failure classes with examples for U1.

## Inputs

- WP-18 clean-script ASR/NLU scores
- WP-SCR-v0 scripts (WP-17)
- Spot probes with light jargon / mumbled numbers (not full S4 noise pack)

## Error taxonomy (U1)

| Class ID | Class | Description | Severity |
|----------|-------|-------------|----------|
| E-Jargon | Trade jargon | Trade terms misheard or mapped to wrong intent/entity | Major |
| E-Num | Numbers / addresses | Phone, street number, unit, postal fragments wrong or dropped | Critical |
| E-Overlap | Overlapping speech | Barge-in / crosstalk; ASR truncates or merges turns | Major |
| E-Omit | Entity omit | Required field never captured though spoken | Major |
| E-Invent | Entity invent | Field filled without support in audio/text | Critical |
| E-Intent | Intent swap | Wrong primary intent (e.g. service vs estimate) | Major |

## Top failure classes with examples

| Rank | Class | Example (paraphrase) | Observed effect |
|------|-------|----------------------|-----------------|
| 1 | E-Num | "Call me at six four seven..." read as wrong digit group | Callback number unusable |
| 2 | E-Jargon | "flashing" / "rough-in" mapped to generic repair | Wrong service subtype |
| 3 | E-Overlap | Caller talks over re-prompt | Partial transcript; entity omit |
| 4 | E-Omit | Urgency said once, soft | Urgency missing on SCR-S01-like probe |
| 5 | E-Invent | Incomplete address filled from prior turn | False site location (reject as pass) |
| 6 | E-Intent | Callback-only scored as full estimate intake | Over-capture vs SCR-C01 |

## Class counts (baseline probes)

| Class | Count (probe set) | Notes |
|-------|-------------------|-------|
| E-Num | Highest | Primary U1 risk on contact fields |
| E-Jargon | High | Feeds S4 jargon corpus (WP-23) |
| E-Overlap | Medium | Links to clarification-loop tests (WP-24) |
| E-Omit / E-Invent / E-Intent | Lower on clean WP-18; higher on probes | Keep invent as defect, not pass |

## U1 evidence use

| Use | Action |
|-----|--------|
| Status board | Point U1 risks to E-Num and E-Jargon first |
| S4 design | Noise/jargon variants must cover E-Jargon + E-Num |
| Gate rule | E-Invent never marked success |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s3/WP-19-asr-nlu-error-taxonomy.md` |
| Experiment log | `docs/experiment-log.md` |
