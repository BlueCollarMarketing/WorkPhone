# S1 - Build negative-finding register for rejected telephony settings

**YouTrack:** WP-11  
**Sprint:** S1 - Telephony Answer Path (1-12 Sep 2025)  
**Date recorded:** 2025-09-09  
**Owner:** Damczyk Jennifer (`jennifer@bluecollarmarketing.com`)  
**Spent time:** 8h (Documentation)  
**Status:** Complete

## Purpose

Log rejected telephony settings and failure modes. Retain negative findings for the S1 baseline pack.

## Inputs

- WP-7 forward answer path outcomes
- WP-8 session lifecycle settings
- WP-9 latency / failure-to-answer log
- WP-10 Executed vs Planned stack labels

## Negative-finding register

| ID | Rejected setting / approach | Failure mode | Linked evidence | Keep? |
|----|----------------------------|--------------|-----------------|-------|
| NF-T01 | Unlimited ring with no idle end | Sessions hang; unclean teardown | WP-8 | Yes |
| NF-T02 | Forward without answer-latency logging | Cannot baseline S1 metrics | WP-7, WP-9 | Yes |
| NF-T03 | Treating Planned carrier swap as Executed | False stack claim | WP-10 | Yes |
| NF-T04 | Ignoring failure-to-answer (N failures = 0 claim) | Hides provider / forward gaps | WP-9 F-01, F-02 | Yes |
| NF-T05 | Greeting disabled on answer | Breaks reproducible greet stage | WP-8 | Yes |

## S1 baseline pack contents (index)

| Item | Path / note |
|------|-------------|
| Forward path | `docs/s1/WP-07-business-number-forward-answer-path.md` |
| Lifecycle | `docs/s1/WP-08-session-lifecycle-ring-answer-greet-end.md` |
| Latency / FTA | `docs/s1/WP-09-answer-latency-failure-to-answer.md` |
| Stack labels | `docs/s1/WP-10-executed-vs-planned-telephony-stack.md` |
| This register | `docs/s1/WP-11-negative-finding-register-telephony.md` |

## Interpretation

Rejected settings stay listed so later sprints do not reintroduce them silently. S1 Evidence Gate (S2) can cite this register as Present.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s1/WP-11-negative-finding-register-telephony.md` |
| Experiment log | `docs/experiment-log.md` |
