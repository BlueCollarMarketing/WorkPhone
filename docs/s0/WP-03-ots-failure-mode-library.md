# S0 - Document OTS failure-mode library

**YouTrack:** WP-3  
**Sprint:** S0 - Framing & OTS Rejection (1-11 Jul 2025)  
**Date recorded:** 2025-07-07  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 16h (Documentation)  
**Status:** Complete

## Purpose

Record OTS gaps from WP-2 baseline runs: wrong intake fields, missing trade knowledge, hold/drop behaviour. Write the insufficiency note with negative findings retained.

## Source

WP-2 Executed baseline on five trade scripts (SCR-01 to SCR-05). All five failed.

## Failure-mode library

| ID | Failure mode | Seen on | Technical gap |
|----|--------------|---------|---------------|
| FM-01 | Wrong or missing intake fields | SCR-01, SCR-02, SCR-05 | No reliable capture of service type, urgency, location, callback window |
| FM-02 | Missing trade knowledge | SCR-01, SCR-02 | Generic script does not distinguish estimate vs service vs emergency language |
| FM-03 | Hold / drop / delayed answer | SCR-03 | After-hours path does not meet contractor-grade answer behaviour |
| FM-04 | No clarification on incomplete info | SCR-04 | Silent acceptance of empty critical fields |
| FM-05 | Unstructured callback-only message | SCR-05 | Message taken without actionable next-step schema |

## Insufficiency note (negative findings retained)

1. OTS generic answering / voice-agent paths are **not sufficient** for construction intake under the five S0 scripts.
2. Failures are technical (fields, jargon, after-hours behaviour), not only cost comparison.
3. Rejected path: rely on unmodified OTS alone for Workphone MVP evidence.
4. Next: lock Draft U1-U3 (WP-4) using this library as the OTS gap baseline.

## Evidence label

| Item | Label |
|------|--------|
| WP-2 baseline runs | Executed |
| This failure-mode library | Executed (derived from WP-2 logs) |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s0/WP-03-ots-failure-mode-library.md` |
| Baseline results | `docs/s0/WP-02-ots-baseline-five-trade-scripts.md` |
| Experiment log | `docs/experiment-log.md` |
