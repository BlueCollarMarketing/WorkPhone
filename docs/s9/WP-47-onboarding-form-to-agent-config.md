# S9 - Map onboarding form fields to agent configuration

**YouTrack:** WP-47  
**Sprint:** S9 - Onboarding to live agent (13-24 Apr 2026)  
**Date recorded:** 2026-04-13  
**Owner:** Hill Alexandria (`alexandria@bluecollarmarketing.com`)  
**Spent time:** 360h (Documentation)  
**Ideal days:** 45  
**Status:** Complete

## Purpose

Map onboarding form fields to agent config (services, hours, voice). Document the mapping path for D-07.

## Version (D-07)

| Field | Value |
|-------|--------|
| Map ID | WP-ONBOARD-MAP |
| Version | v0 |
| Deliverable | D-07 |
| Form schema | `data/onboarding/onboarding_form_schema_v0.json` |
| Map path | `data/onboarding/onboarding_form_to_agent_config_v0.json` |
| Evidence label | Executed |

## Mapping path (D-07)

1. Contractor completes onboarding form (Executed lab form schema)  
2. Validator checks required form groups: business, services, hours, voice  
3. Mapper writes agent_config JSON for Workphone runtime  
4. Config version stamped for D-07 audit  

## Field groups

| Group | Form fields (examples) | Agent path prefix |
|-------|------------------------|-------------------|
| business | business_name, trade_primary | `agent.identity.*` |
| services | services, service_notes | `agent.services.*` |
| hours | weekday open/close, sat/sun, after_hours_mode | `agent.hours.*` |
| voice | voice_id, voice_style, greeting_template | `agent.voice.*` |

## Core mappings

| Form field | Agent config path | Required |
|------------|-------------------|----------|
| business_name | agent.identity.display_name | Yes |
| trade_primary | agent.identity.primary_trade | Yes |
| services | agent.services.offered | Yes |
| hours_weekday_open / close | agent.hours.weekday.open / close | Yes |
| after_hours_mode | agent.hours.after_hours_mode | Yes |
| voice_id | agent.voice.voice_id | Yes |
| voice_style | agent.voice.style | Yes |

## Lab

```text
python -m workphone_lab onboarding-map
```

Demo example `roofing_co` maps services, hours, and voice into `outputs/s9_agent_config_demo.json`.

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s9/WP-47-onboarding-form-to-agent-config.md` |
| Map | `data/onboarding/onboarding_form_to_agent_config_v0.json` |
| Form schema | `data/onboarding/onboarding_form_schema_v0.json` |
| Experiment log | `docs/experiment-log.md` |
