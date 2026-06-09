# Workphone

AI voice agent / 24/7 phone receptionist for construction and blue-collar contractors.

**Organization:** Blue Collar Marketing / Imperium Social Ltd.  
**GitHub:** https://github.com/BlueCollarMarketing/WorkPhone  
**YouTrack:** WP  
**Project span:** 1 Jul 2025 - 30 Jun 2026

## Lab simulator (runnable)

Stdlib-only Python lab path (no live carrier required). From the repo root:

```powershell
cd C:\Users\Hassan\Downloads\AI_Driven_Video_Translation\WorkPhone

python -m workphone_lab baseline
python -m workphone_lab session
python -m workphone_lab hypothesis-s4
python -m workphone_lab noise-jargon
python -m workphone_lab corpus
python -m workphone_lab clarify
python -m workphone_lab compare-ots
python -m workphone_lab gate-s4
python -m workphone_lab policy
python -m workphone_lab intake
python -m workphone_lab measure-policy
python -m workphone_lab status-board
python -m workphone_lab corpus-gate
python -m workphone_lab schema
python -m workphone_lab handoff
python -m workphone_lab channels
python -m workphone_lab negative
python -m workphone_lab gate-s6
python -m workphone_lab summary
python -m workphone_lab measure-summary
python -m workphone_lab summary-latency
python -m workphone_lab summary-fm
python -m workphone_lab gate-m4
python -m workphone_lab concurrency-scenarios
python -m workphone_lab concurrency-breakpoint
python -m workphone_lab concurrency-queue
python -m workphone_lab concurrency-fidelity
python -m workphone_lab gate-s8
python -m workphone_lab onboarding-map
python -m workphone_lab trade-profiles
python -m workphone_lab voice-greeting
python -m workphone_lab time-to-live
python -m workphone_lab gate-m5
python -m workphone_lab e2e-scenarios
python -m workphone_lab system-fm
python -m workphone_lab freeze-status-board
python -m workphone_lab evidence-index
python -m workphone_lab gate-m6
python -m workphone_lab continuity
python -m workphone_lab assumptions
python -m workphone_lab timesheet-reconcile
python -m workphone_lab closeout
python -m workphone_lab gate-m7
```

| Command | What it does |
|---------|----------------|
| `baseline` | Scores WP-SCR-v0 clean scripts -> `outputs/s3_baseline_scores.json` |
| `session` | Demo ring-answer-greet-end -> `outputs/session_demo.json` |
| `hypothesis-s4` | S4 hypothesis log from S3 baseline -> `outputs/s4_hypothesis_log.json` |
| `noise-jargon` | Intent drop vs clean baseline (WP-22) -> `outputs/s4_noise_jargon_scores.json` |
| `corpus` | Validate regression corpus version tags (WP-23) -> `outputs/regression_corpus_report.json` |
| `clarify` | Clarification-loop helps/harms/no_change (WP-24) -> `outputs/s4_clarification_loop.json` |
| `compare-ots` | OTS vs Workphone delta table (WP-25) -> `outputs/s4_ots_vs_workphone.json` |
| `gate-s4` | S4 Evidence Gate Present/Missing (WP-26) -> `outputs/s4_evidence_gate.json` |
| `policy` | Dialogue policy estimate/emergency/inquiry demo (WP-27) -> `outputs/s5_dialogue_policy_demo.json` |
| `intake` | Intake field map validation D-04 (WP-28) -> `outputs/s5_intake_field_map_report.json` |
| `measure-policy` | Policy completion + wrong-path on corpus (WP-29) -> `outputs/s5_policy_completion_wrong_path.json` |
| `status-board` | U1-U3 status board with evidence labels (WP-30) -> `outputs/s5_u1_status_board.json` |
| `corpus-gate` | Corpus gate before bulk policy changes M3 (WP-31) -> `outputs/s5_corpus_gate_m3.json` |
| `schema` | Intake schema validation D-04/S6 (WP-32) -> `outputs/s6_intake_schema_report.json` |
| `handoff` | Required-field enforcement on handoffs (WP-33) -> `outputs/s6_handoff_enforcement.json` |
| `channels` | Handoff rules email/SMS/CRM stub (WP-34) -> `outputs/s6_handoff_channels.json` |
| `negative` | Negative intake refuse/partial/callback (WP-35) -> `outputs/s6_negative_intake.json` |
| `gate-s6` | S6 Evidence Gate schema + wrong rates (WP-36) -> `outputs/s6_evidence_gate.json` |
| `summary` | Post-call summary email template D-05 (WP-37) -> `outputs/s7_summary_email_demo.json` |
| `measure-summary` | Summary invent/omit vs ground-truth notes (WP-38) -> `outputs/s7_summary_field_accuracy.json` |
| `summary-latency` | Call-end to email latency distribution U3 (WP-39) -> `outputs/s7_summary_latency_distribution.json` |
| `summary-fm` | Summary failure modes delay/wrong-num/hallucination (WP-40) -> `outputs/s7_summary_failure_modes.json` |
| `gate-m4` | M4 intake+summary core path freeze / S7 close (WP-41) -> `outputs/s7_m4_intake_summary_freeze.json` |
| `concurrency-scenarios` | Design 2/3/N inbound load scenarios U3 (WP-42) -> `outputs/s8_concurrency_load_scenarios.json` |
| `concurrency-breakpoint` | Concurrent drop/answer-delay break-point N (WP-43) -> `outputs/s8_concurrency_breakpoint.json` |
| `concurrency-queue` | Queue/drop/error rates + provider logs U3 (WP-44) -> `outputs/s8_concurrency_queue_rates.json` |
| `concurrency-fidelity` | Summary fidelity under load; invent/omit not pass (WP-45) -> `outputs/s8_summary_fidelity_under_load.json` |
| `gate-s8` | S8 Evidence Gate concurrency pack + limits (WP-46) -> `outputs/s8_evidence_gate.json` |
| `onboarding-map` | Onboarding form to agent config D-07 (WP-47) -> `outputs/s9_onboarding_map_report.json` |
| `trade-profiles` | Roofing vs plumbing side-by-side behaviour (WP-48) -> `outputs/s9_trade_profiles_side_by_side.json` |
| `voice-greeting` | Voice selection and greeting customization WS4 (WP-49) -> `outputs/s9_voice_greeting_ws4.json` |
| `time-to-live` | Form-submit to callable number TTL D-07 (WP-50) -> `outputs/s9_time_to_live_distribution.json` |
| `gate-m5` | M5 concurrency limits + onboard path pack / S9 close (WP-51) -> `outputs/s9_m5_concurrency_onboard_pack.json` |
| `e2e-scenarios` | E2E telephony scenario pack happy/noise/incomplete/concurrent D-08 (WP-52) -> `outputs/s10_e2e_telephony_scenario_pack.json` |
| `system-fm` | System-only failure modes drift/drop/summary-intake/load D-08 (WP-53) -> `outputs/s10_system_failure_modes.json` |
| `freeze-status-board` | Freeze U1/U2/U3 status board draft Open/Partial/Resolved (WP-54) -> `outputs/s10_status_board_draft_freeze.json` |
| `evidence-index` | Evidence index + YouTrack/timesheet alignment D-09 (WP-55) -> `outputs/s10_evidence_index_timesheet_alignment.json` |
| `gate-m6` | Evidence Gate core pack Present/Missing/Location M6 / S10 close (WP-56) -> `outputs/s10_m6_core_evidence_gate.json` |
| `continuity` | Continuity experiments on open U1/U2/U3 items D-10 (WP-57) -> `outputs/closeout_continuity_u1_u2_u3.json` |
| `assumptions` | Assumptions Register sweep Validated/Revised/Removed (WP-58) -> `outputs/closeout_assumptions_register_sweep.json` |
| `timesheet-reconcile` | Final YouTrack/timesheet reconcile included roles (WP-59) -> `outputs/closeout_timesheet_reconciliation.json` |
| `closeout` | Close-out checklist + Partner acceptance D-11 (WP-60) -> `outputs/closeout_d11_checklist_partner_acceptance.json` |
| `gate-m7` | Final Evidence Gate period close 30 Jun 2026 M7 (WP-61) -> `outputs/closeout_m7_period_close_gate.json` |
| `all` | Run full lab suite smoke check |

Corpus: `data/corpus/regression_corpus.json` (variants linked to clean **WP-SCR-v0 @ v0**)  
Policy: `data/policy/dialogue_policy_v0.json`  
Intake: `data/intake/intake_field_map_v0.json`  
Schema: `data/intake/intake_schema_v0.json`  
Negative cases: `data/intake/negative_intake_cases_v0.json`  
Handoff rules: `data/handoff/handoff_rules_v0.json`  
Summary template: `data/summary/summary_email_template_v0.json`  
Summary ground truth: `data/summary/ground_truth_call_notes_v0.json`  
Summary latency: `data/summary/summary_latency_runs_v0.json`  
Summary failure modes: `data/summary/summary_failure_modes_v0.json`  
Concurrency scenarios: `data/concurrency/load_scenarios_v0.json`  
Concurrency breakpoint: `data/concurrency/breakpoint_config_v0.json`  
Concurrency queue rates: `data/concurrency/queue_rates_config_v0.json`  
Concurrency fidelity: `data/concurrency/summary_fidelity_under_load_v0.json`  
U3 concurrency pack: `data/concurrency/u3_concurrency_pack_v0.json`  
Onboarding map: `data/onboarding/onboarding_form_to_agent_config_v0.json`  
Onboarding form schema: `data/onboarding/onboarding_form_schema_v0.json`  
Trade profiles: `data/onboarding/trade_profiles_v0.json`  
Voice/greeting cases: `data/onboarding/voice_greeting_cases_v0.json`  
Time-to-live runs: `data/onboarding/time_to_live_runs_v0.json`  
E2E telephony pack: `data/e2e/telephony_scenario_pack_v0.json`  
System failure modes: `data/e2e/system_failure_modes_v0.json`  
Evidence index: `data/evidence/evidence_index_v0.json`  
Continuity pack: `data/closeout/continuity_experiments_v0.json`  
Assumptions Register: `data/closeout/assumptions_register_v0.json`  
Timesheet reconcile: `data/closeout/timesheet_reconcile_v0.json`  
Close-out checklist D-11: `data/closeout/closeout_checklist_d11_v0.json`  
Partner acceptance: `data/closeout/partner_acceptance_v0.json`  
Status board: `data/status/u1_u3_status_board.json`  
Corpus gate: `data/gates/corpus_gate_m3.json`  
M4 freeze: `data/gates/m4_intake_summary_freeze.json`  
M5 pack: `data/gates/m5_concurrency_onboard_pack.json`  
M6 core Evidence Gate: `data/gates/m6_core_evidence_gate.json`  
M7 period close gate: `data/gates/m7_period_close_gate.json`  
S8 Evidence Gate: `data/gates/s8_concurrency_evidence_gate.json`

**Full smoke check:** `python -m workphone_lab all`
