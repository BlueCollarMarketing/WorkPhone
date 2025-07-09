# S0 - Start BRD outline for Workphone requirements

**YouTrack:** WP-6  
**Sprint:** S0 - Framing & OTS Rejection (1-11 Jul 2025)  
**Date recorded:** 2025-07-09  
**Owner:** Lees Emily D (`emily@bluecollarmarketing.com`)  
**Spent time:** 16h (Documentation)  
**Status:** Complete - Draft outline (not a frozen BRD)

## Purpose

Draft a BRD outline with scope, functional requirements (FRs), and placeholder acceptance criteria for telephony, dialogue, summaries, and concurrency. Link to Project Plan and Test Plan.

## Document control (outline)

| Field | Value |
|-------|--------|
| Product | Workphone |
| Company | Blue Collar Marketing / Imperium Social Ltd. |
| Span | 1 Jul 2025 - 30 Jun 2026 |
| Related | Project Plan Draft v0.1; Sprint Plan Draft v0.1; Test Plan Draft v0.1 |
| Status | Draft outline started |

## 1. Problem / opportunity

Contractors miss leads after-hours and on jobs. Generic OTS answering / voice agents fail trade intake (see WP-2, WP-3). Workphone needs a construction-aware 24/7 voice agent with structured intake and post-call summaries.

## 2. Scope (outline)

**In scope:** telephony answer path, trade dialogue/NLU, intake/handoff, email summaries, concurrency limits, onboarding to live agent, evidence packing.

**Out of scope:** sales/SDR/RevOps/finance/video labour; foundation-model training from scratch as a committed baseline; work after 30 Jun 2026.

## 3. Functional requirements (placeholders)

| ID | Area | Requirement (Draft) |
|----|------|---------------------|
| FR-T1 | Telephony | System answers inbound forwarded/provisioned numbers and starts an agent session |
| FR-T2 | Telephony | After-hours and abandoned/re-dial behaviour follows documented policy |
| FR-D1 | Dialogue | Agent distinguishes estimate vs service vs emergency vs general inquiry |
| FR-D2 | Dialogue | Low-confidence turns trigger clarification before wrong booking |
| FR-I1 | Intake | Required fields captured or explicitly marked incomplete |
| FR-I2 | Intake | Handoff path delivers actionable job context to the business |
| FR-S1 | Summaries | Post-call email includes caller, number, need, urgency, next step |
| FR-S2 | Summaries | Invented critical fields are treated as defects (not success) |
| FR-C1 | Concurrency | Multi-call behaviour and break-point N are measured and documented |
| FR-O1 | Onboarding | Business profile maps to live agent config without hidden manual steps |

## 4. Placeholder acceptance criteria (for Test Plan)

| Area | Placeholder AC |
|------|----------------|
| Telephony | Reproducible answer path; latency and fail-to-answer logged (TS-03 to TS-05) |
| Dialogue | Intent/path metrics on versioned corpus (TS-06 to TS-11) |
| Summaries | Fidelity vs ground truth; invent/omit rates logged (TS-15, TS-16) |
| Concurrency | Limits statement for N concurrent calls (TS-17, TS-18) |

## 5. Uncertainties (linked)

Status board: `docs/s0/WP-04-u1-u3-statements-status-board.md` (U1/U2/U3 Open).

## 6. Links

| Document | Role |
|----------|------|
| Workphone Project Plan Draft v0.1 | Objectives, WBS, labour hours, exclusions |
| Workphone Sprint Plan Draft v0.1 | Sprint goals and backlog |
| Workphone Test Plan Draft v0.1 | Scenarios TS-01 to TS-20 and gates G1-G6 |
| This outline | `docs/s0/WP-06-brd-outline-workphone-requirements.md` |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s0/WP-06-brd-outline-workphone-requirements.md` |
| Experiment log | `docs/experiment-log.md` |
