# Close-out - Run continuity experiments on open U1 U2 U3 items

**YouTrack:** WP-57  
**Sprint:** Close-out - Continuity & Records Freeze (1-30 Jun 2026)  
**Date recorded:** 2026-06-02  
**Owner:** Mann Wesley J (`wesley@bluecollarmarketing.com`)  
**Spent time:** 261h (Testing)  
**Ideal days:** 33  
**Status:** Complete

## Purpose

Run continuity experiments on any remaining Open U1/U2/U3 items. Record results and update status pointers for D-10.

## Pack

| Field | Value |
|-------|--------|
| Pack ID | WP-CONTINUITY-U123 |
| Version | v0 |
| Deliverable | D-10 |
| Continuity tag | continuity@d10-v0 |
| Config | `data/closeout/continuity_experiments_v0.json` |
| Command | `python -m workphone_lab continuity` |
| Evidence label | Executed |

## Scope

At start, U1/U2/U3 were all **Partial** (no literal Open rows after S10 freeze). Partial counts as remaining open uncertainty for D-10. Continuity must not mark Resolved without Confirmed close.

## Continuity results

| ID | Uncertainty | Outcome | Status after | Notes |
|----|-------------|---------|--------------|-------|
| CONT-U1 | U1 | pass | Partial | Clean vs noise intent delta still > 0 |
| CONT-U2 | U2 | pass | Partial | Negative cases safe; SCR-I01 omit not invented |
| CONT-U3 | U3 | pass | Partial | N=5 within limits; N=6 breaks (U3-LIMITS-v0) |

`experiments=3 expect_met=3 pack_pass=True`

## Status pointers updated

Board `data/status/u1_u3_status_board.json` updated_card=WP-57 with Executed continuity pointers on U1/U2/U3. Planned Confirmed-close items retained.

## Rejected configs

| ID | Rejected config |
|----|-----------------|
| RJ-D10-01 | Mark U1/U2/U3 Resolved from continuity re-runs alone |
| RJ-D10-02 | Skip status pointer updates after continuity experiments |
| RJ-D10-03 | Treat Planned Confirmed-close items as cleared by lab continuity |

## Lab

```text
python -m workphone_lab continuity
```

Export: `outputs/closeout_continuity_u1_u2_u3.json`

## Record location

| Artifact | Path |
|----------|------|
| This note | `docs/closeout/WP-57-continuity-experiments-u1-u2-u3.md` |
| Pack | `data/closeout/continuity_experiments_v0.json` |
| Board | `data/status/u1_u3_status_board.json` |
| Export | `outputs/closeout_continuity_u1_u2_u3.json` |
| Experiment log | `docs/experiment-log.md` |
