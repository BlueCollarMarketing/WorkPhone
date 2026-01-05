# S5 - Draft dialogue policy for estimate emergency and inquiry

**YouTrack:** WP-27  
**Sprint:** S5 - Dialogue policy + corpus gate (5-16 Jan 2026)  
**Date recorded:** 2026-01-05  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 360h (Documentation)  
**Ideal days:** 45  
**Status:** Complete

## Purpose

Draft construction dialogue policy for estimate vs emergency vs general inquiry paths. Align policy to U2 intake goals for S5.

## U2 alignment

| U2 intake goal | Policy support |
|----------------|----------------|
| Correct path among estimate / emergency / inquiry | Priority routing: emergency (1) > estimate (2) > inquiry (3) |
| Required fields collected or marked missing (no invent) | Per-path `required_fields` lists |
| Wrong-path handoffs logged as defects | `wrong_path_guard` on each path |

## Policy draft (WP-DIALOGUE-v0)

| Path | Route ID | Priority | Required fields | Next step |
|------|----------|----------|-----------------|-----------|
| emergency | PATH-EMG | 1 | name, number, hazard_type, urgency | Escalate or high-priority voicemail |
| estimate | PATH-EST | 2 | name, number, job_type, site_area, callback_window | Confirm callback; voicemail if no human |
| inquiry | PATH-INQ | 3 | name, number, inquiry_topic | Short answer or message + callback |

### Triggers (summary)

| Path | Example triggers |
|------|------------------|
| emergency | gas, flood, fire, sparking, burst pipe, urgent danger |
| estimate | estimate, quote, bid, pricing, how much |
| inquiry | hours, location, do you do, general question |

## Lab demo

```text
python -m workphone_lab policy
```

Routes sample utterances and writes `outputs/s5_dialogue_policy_demo.json`.

## Machine-readable policy

`data/policy/dialogue_policy_v0.json`

## Next (S5)

| Card | Depends on this policy |
|------|------------------------|
| WP-28 | Map required intake fields per call type |
| WP-29 | Measure completion / wrong-path rate |

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s5/WP-27-dialogue-policy-estimate-emergency-inquiry.md` |
| Experiment log | `docs/experiment-log.md` |
