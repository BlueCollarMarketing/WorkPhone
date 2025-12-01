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
```

| Command | What it does |
|---------|----------------|
| `baseline` | Scores WP-SCR-v0 clean scripts -> `outputs/s3_baseline_scores.json` |
| `session` | Demo ring-answer-greet-end -> `outputs/session_demo.json` |
| `hypothesis-s4` | S4 hypothesis log from S3 baseline -> `outputs/s4_hypothesis_log.json` |
| `noise-jargon` | Intent drop vs clean baseline (WP-22) -> `outputs/s4_noise_jargon_scores.json` |

Script pack: `data/scripts/wp_scr_v0.json`  
Evidence notes: `docs/`
