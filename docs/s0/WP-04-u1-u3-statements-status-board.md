# S0 - Draft U1-U3 statements and status board

**YouTrack:** WP-4  
**Sprint:** S0 - Framing & OTS Rejection (1-11 Jul 2025)  
**Date recorded:** 2025-07-03  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 16h (Documentation)  
**Status:** Complete

## Purpose

Lock Draft technological uncertainties U1 (speech/intent), U2 (dialogue/intake), U3 (concurrency/summaries). Publish the status board as Open with evidence pointers from S0.

## Inputs

- WP-1 contractor missed-call problem framing
- WP-2 OTS baseline (five scripts, all Fail)
- WP-3 OTS failure-mode library (FM-01 to FM-05)

## Draft uncertainty statements

| ID | Statement | Primary evidence pointer |
|----|-----------|--------------------------|
| U1 | Can the agent reliably understand and classify inbound speech under contractor conditions (noise, trade jargon, incomplete info)? | WP-1 framing; WP-2/WP-3 OTS gaps on jargon and incomplete info (FM-02, FM-04) |
| U2 | Can a construction-specific dialogue policy collect booking-grade intake fields without wrong-path handoffs? | WP-2 SCR-01/SCR-02/SCR-05 field failures (FM-01, FM-05) |
| U3 | Can concurrent telephony and post-call summaries stay accurate and timely under load? | WP-1 multi-call / after-hours problem notes; WP-3 FM-03 hold/drop behaviour |

## Status board (Draft lock)

| ID | Status | Notes |
|----|--------|-------|
| U1 | Open | No speech/NLU corpus yet; OTS negative findings only |
| U2 | Open | No dialogue policy or intake schema yet |
| U3 | Open | No concurrency or summary fidelity experiments yet |
| System | Open | End-to-end live path not assembled |

## Change control

These Draft statements match Project Plan Draft v0.1 wording for U1-U3. Any later change requires a written note linked from this board.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s0/WP-04-u1-u3-statements-status-board.md` |
| Experiment log | `docs/experiment-log.md` |
