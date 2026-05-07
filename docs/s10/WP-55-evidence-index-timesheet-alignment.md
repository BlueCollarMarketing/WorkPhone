# S10 - Align evidence index with YouTrack timesheet hours

**YouTrack:** WP-55  
**Sprint:** S10 - E2E Assembly + Evidence Pack (4-15 May 2026)  
**Date recorded:** 2026-05-07  
**Owner:** Roantree Timothy I (`timothy@bluecollarmarketing.com`)  
**Spent time:** 337h (Documentation)  
**Ideal days:** 42  
**Status:** Complete

## Purpose

Build evidence index and check YouTrack/timesheet alignment for included roles only against project labour hours.

## Index

| Field | Value |
|-------|--------|
| Index ID | WP-EVIDENCE-INDEX |
| Version | v0 |
| Deliverable | D-09 |
| Config | `data/evidence/evidence_index_v0.json` |
| Command | `python -m workphone_lab evidence-index` |
| Evidence label | Executed |

## Included roles only

| Role key | Display | SR&ED % | Labour target (h) |
|----------|---------|--------:|------------------:|
| okunade | Adesanya Okunade K | 75 | 2868 |
| jennifer | Damczyk Jennifer | 72 | 2564 |
| alexandria | Hill Alexandria | 54 | 3058 |
| wesley | Mann Wesley J | 20 | 2087 |
| timothy | Roantree Timothy I | 60 | 3159 |
| **Total** | | | **13736** |

Excluded remaps (not labour owners): emily→timothy, stephen→wesley, jacob→jennifer, parminder→alexandria.

## YouTrack / timesheet alignment (WP-1..WP-61 plan)

| Role | YouTrack hours | Labour target | Delta | Aligned |
|------|---------------:|--------------:|------:|---------|
| okunade | 2868 | 2868 | 0 | Yes |
| jennifer | 2564 | 2564 | 0 | Yes |
| alexandria | 3058 | 3058 | 0 | Yes |
| wesley | 2087 | 2087 | 0 | Yes |
| timothy | 3159 | 3159 | 0 | Yes |

`hours_aligned=True` · `roles_only_ok=True`

## Evidence index coverage

| Status | Count | Rule |
|--------|------:|------|
| Present | 55 | WP-1..WP-55 note files on disk |
| Planned | 6 | WP-56..WP-61 (S10 close + Close-out) |
| Missing through WP-55 | 0 | Must stay 0 for index_pass |

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-D09-01 | Include excluded remapped identities as labour owners |
| RJ-D09-02 | Claim timesheet alignment without card-hour sum matching labour targets |
| RJ-D09-03 | Count Planned close-out cards as Missing evidence for WP-55 gate |

## Lab

```text
python -m workphone_lab evidence-index
```

Export: `outputs/s10_evidence_index_timesheet_alignment.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/s10/WP-55-evidence-index-timesheet-alignment.md` |
| Index | `data/evidence/evidence_index_v0.json` |
| Export | `outputs/s10_evidence_index_timesheet_alignment.json` |
| Experiment log | `docs/experiment-log.md` |
