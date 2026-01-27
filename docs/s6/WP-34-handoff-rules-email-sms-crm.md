# S6 - Define handoff rules for email SMS and CRM stub

**YouTrack:** WP-34  
**Sprint:** S6 - Intake field model and handoff (26 Jan - 6 Feb 2026)  
**Date recorded:** 2026-01-27  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Documentation)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Define handoff rules for email vs SMS vs CRM stub on the Executed path only. Record config and acceptance notes for WS3.

## Scope

| Field | Value |
|-------|--------|
| Rules ID | WP-HANDOFF-RULES |
| Version | v0 |
| Workstream | WS3 |
| Path | Executed lab path only |
| Config | `data/handoff/handoff_rules_v0.json` |
| Evidence label | Executed |

## Channel rules (Executed)

| Channel | When | Requires | Acceptance |
|---------|------|----------|------------|
| email | estimate / service / inquiry (default) | name, phone, service | Structured email with required core fields |
| sms | emergency (and callback ack) | phone | Short urgent ping; not full intake |
| crm_stub | all allowed handoffs | name, phone, service | Stub CRM row; no silent drop |

## Priority

1. SMS if emergency  
2. Email on every allowed handoff  
3. CRM stub mirrors allowed handoffs  

## Guardrails

- Fire only after WP-33 required-field enforcement  
- Never invent fields to satisfy a channel  
- Planned alternate CRMs stay Planned until Confirmed  

## Lab

```text
python -m workphone_lab channels
```

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s6/WP-34-handoff-rules-email-sms-crm.md` |
| Experiment log | `docs/experiment-log.md` |
