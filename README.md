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
| `all` | Run full lab suite smoke check |

Corpus: `data/corpus/regression_corpus.json` (variants linked to clean **WP-SCR-v0 @ v0**)  
Policy: `data/policy/dialogue_policy_v0.json`  
Intake: `data/intake/intake_field_map_v0.json`

**Full smoke check:** `python -m workphone_lab all`
