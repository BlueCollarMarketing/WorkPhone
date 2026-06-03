# Close-out - Complete Assumptions Register sweep

**YouTrack:** WP-58  
**Sprint:** Close-out - Continuity & Records Freeze (1-30 Jun 2026)  
**Date recorded:** 2026-06-03  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 260h (Documentation)  
**Ideal days:** 33  
**Status:** Complete - final register filed

## Purpose

Sweep Assumptions Register entries to Validated / Revised / Removed. File the final register for close-out.

## Register

| Field | Value |
|-------|--------|
| Register ID | WP-ASSUMPTIONS-REGISTER |
| Version | v1.0-final |
| Register tag | swept@closeout-v0 |
| Config | `data/closeout/assumptions_register_v0.json` |
| Command | `python -m workphone_lab assumptions` |
| Evidence label | Executed |

## Sweep summary

| Disposition | Count |
|-------------|------:|
| Validated | 7 |
| Revised | 3 |
| Removed | 5 |
| **Total** | **15** |

`sweep_pass=True` · final register filed.

## Final register (A-WP-01..15)

| ID | Disposition | Short note |
|----|-------------|------------|
| A-WP-01 | Validated | OTS insufficient for construction intake |
| A-WP-02 | Validated | Executed lab path acceptable within span |
| A-WP-03 | Revised | Clean ASR alone does not close U1 |
| A-WP-04 | Validated | Clarification loops help without net harm |
| A-WP-05 | Revised | Booking-grade policy not achieved; U2 Partial |
| A-WP-06 | Removed | Invent-as-pass forbidden |
| A-WP-07 | Revised | Latency alert not frozen absolute SLA |
| A-WP-08 | Validated | Lab soft cap N=5 safe on Executed path |
| A-WP-09 | Removed | Provider channel != lab soft cap |
| A-WP-10 | Validated | D-07 TTL within Draft band on lab path |
| A-WP-11 | Removed | Unit-test pass does not clear system FM |
| A-WP-12 | Removed | No Resolved at S10 without Confirmed |
| A-WP-13 | Validated | Five included roles only for labour hours |
| A-WP-14 | Removed | Live CRM/SMTP not in M4 Executed core |
| A-WP-15 | Validated | Max answer delay 8.0s Executed threshold |

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-AR-01 | Leave entries without Validated/Revised/Removed disposition |
| RJ-AR-02 | Treat Removed assumptions as still operative for Confirmed claims |
| RJ-AR-03 | File close-out without final Assumptions Register |

## Lab

```text
python -m workphone_lab assumptions
```

Export: `outputs/closeout_assumptions_register_sweep.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/closeout/WP-58-assumptions-register-sweep.md` |
| Final register | `data/closeout/assumptions_register_v0.json` |
| Export | `outputs/closeout_assumptions_register_sweep.json` |
| Experiment log | `docs/experiment-log.md` |
