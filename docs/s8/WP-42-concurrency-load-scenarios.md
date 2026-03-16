# S8 - Design concurrency load scenarios for inbound calls

**YouTrack:** WP-42  
**Sprint:** S8 - Concurrency and latency (U3) (16-27 Mar 2026)  
**Date recorded:** 2026-03-16  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 251h (Implementation)  
**Ideal days:** 31  
**Status:** Complete

## Purpose

Design load scenarios for 2 / 3 / N simultaneous inbound calls. Document method and limits for U3 tests.

## Method (Executed lab)

| Step | Detail |
|------|--------|
| Path | Session lifecycle ring-answer-greet-active-end |
| Overlap | Start N inbound invites within `stagger_ms` of each other |
| Scripts | Rotate WP-SCR-v0 across concurrent legs |
| Metrics | answer_delay_s; drop_or_reject; stuck_session; optional summary queue backlog |
| Next | WP-43 measures break-point N under these scenarios |

### Draft pass/fail (for later measurement)

| Metric | Draft limit |
|--------|-------------|
| max answer delay | 8.0 s |
| max drop rate | 0.0 |
| stuck sessions allowed | 0 |

## Limits

| Limit | Value | Label |
|-------|------:|-------|
| Lab soft cap N | 5 | Executed (designed working N for LOAD-N) |
| Lab hard cap N | 8 | Executed (max lab search bound) |
| Provider concurrent channels | unset | Planned (not Confirmed) |

Do not claim production concurrency until provider cap is Confirmed.

## Scenarios

| ID | N | Stagger | Scripts | U3 focus |
|----|--:|--------:|---------|----------|
| LOAD-2 | 2 | 100 ms | SCR-E01, SCR-S01 | Answer delay under light concurrency |
| LOAD-3 | 3 | 100 ms | SCR-E01, SCR-S01, SCR-C01 | Drop risk and greet contention |
| LOAD-N | 5 | 150 ms | full WP-SCR-v0 set | Approach soft cap; feed break-point search |

## Lab

```text
python -m workphone_lab concurrency-scenarios
```

Pack: `data/concurrency/load_scenarios_v0.json`  
Export: `outputs/s8_concurrency_load_scenarios.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s8/WP-42-concurrency-load-scenarios.md` |
| Scenario pack | `data/concurrency/load_scenarios_v0.json` |
| Status board | `data/status/u1_u3_status_board.json` |
| Experiment log | `docs/experiment-log.md` |
