# S1 - Configure session lifecycle ring-answer-greet-end

**YouTrack:** WP-8  
**Sprint:** S1 - Telephony Answer Path (1-12 Sep 2025)  
**Date recorded:** 2025-09-02  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 24h (Implementation)  
**Status:** Complete

## Purpose

Implement/configure session lifecycle from ring through answer, agent greeting, and idle end. Record settings used for the reproducible S1 answer path.

## Hypothesis

A documented session lifecycle (ring -> answer -> greet -> idle end) makes the WP-7 forward path reproducible across test calls.

## Lifecycle stages (Executed)

| Stage | Behaviour | Setting notes |
|-------|-----------|---------------|
| Ring | Inbound invite received on forwarded path | Provider ring timeout recorded |
| Answer | Session accepted | Answer event logged |
| Greet | Agent greeting plays | Greeting prompt / voice config recorded |
| Active | Dialogue session open | Session ID retained in test log |
| Idle end | Session closes on hangup / idle timeout | Idle timeout value recorded |

## Config snapshot

| Item | Value |
|------|--------|
| Depends on | WP-7 forward answer path |
| Greeting | Default Workphone contractor greeting (test build) |
| Idle end | Timeout + remote hangup handlers enabled |
| Evidence label | Executed |

## Result

| Criterion | Result |
|-----------|--------|
| Full lifecycle configured | Pass |
| Settings recorded | Pass |
| Reproducible with WP-7 path | Pass on scripted retests |

## Interpretation

Session lifecycle is ready for latency / failure-to-answer measurement (WP-9) and negative-finding register (WP-11).

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s1/WP-08-session-lifecycle-ring-answer-greet-end.md` |
| Experiment log | `docs/experiment-log.md` |
