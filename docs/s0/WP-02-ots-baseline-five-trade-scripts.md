# S0 - Run OTS baseline on five trade call scripts

**YouTrack:** WP-2  
**Sprint:** S0 - Framing & OTS Rejection (1-11 Jul 2025)  
**Date recorded:** 2025-07-01  
**Owner:** Adesanya Okunade K (`okunade@bluecollarmarketing.com`)  
**Spent time:** 24h (Testing)  
**Status:** Complete

## Purpose

Execute a generic answering / voice-agent baseline on five construction scripts. Log configs and pass/fail for S0 evidence.

## Hypothesis

Off-the-shelf (OTS) generic answering or voice-agent paths fail construction intake on trade-specific scripts (wrong fields, weak trade knowledge, poor after-hours behaviour).

## Scripts exercised

| ID | Script | Intent |
|----|--------|--------|
| SCR-01 | Estimate request | New roofing / reno estimate, callback window |
| SCR-02 | Service call | Scheduled maintenance / repair booking |
| SCR-03 | After-hours | Evening / weekend inbound while crew is offline |
| SCR-04 | Incomplete info | Caller omits address or urgency |
| SCR-05 | Callback | Caller asks only for a callback, minimal detail |

## OTS baseline config (Executed)

| Setting | Value |
|---------|--------|
| Path under test | Generic answering / generic voice-agent trial |
| Call mode | Scripted inbound test calls |
| Logging | Pass/fail + free-text failure notes per script |
| Evidence label | Executed |

## Results

| Script | Pass/Fail | Notes |
|--------|-----------|-------|
| SCR-01 Estimate | Fail | Service type and callback window not reliably captured |
| SCR-02 Service | Fail | Trade vocabulary mishandled; incomplete job context |
| SCR-03 After-hours | Fail | Hold / delayed answer behaviour; no contractor-grade intake |
| SCR-04 Incomplete | Fail | Did not clarify missing address / urgency; empty critical fields |
| SCR-05 Callback | Fail | Message taken without structured next-step fields |

## Interpretation

OTS baseline is insufficient for construction intake. Failure modes feed WP-3 (failure-mode library) and Draft U1-U3 framing.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s0/WP-02-ots-baseline-five-trade-scripts.md` |
| Experiment log | `docs/experiment-log.md` |
