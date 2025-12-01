from __future__ import annotations

import argparse
import json
from pathlib import Path

from .hypothesis_s4 import build_hypothesis_log, write_hypothesis_log
from .scoring import compare_to_baseline, score_pack
from .session import run_demo_session

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "data" / "scripts" / "wp_scr_v0.json"
SCRIPTS_NJ = ROOT / "data" / "scripts" / "wp_scr_v0_noise_jargon.json"
OUT = ROOT / "outputs"


def _ensure_baseline() -> dict:
    path = OUT / "s3_baseline_scores.json"
    pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    report = score_pack(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def cmd_baseline(_: argparse.Namespace) -> int:
    report = _ensure_baseline()
    path = OUT / "s3_baseline_scores.json"
    print(f"Wrote {path}")
    print(f"Intent pass: {report['aggregate']['intent_pass']}/{report['aggregate']['n']}")
    print(f"Entity full: {report['aggregate']['entity_full']}/{report['aggregate']['n']}")
    print(f"Intent accuracy: {report['aggregate']['intent_accuracy']}")
    return 0


def cmd_session(_: argparse.Namespace) -> int:
    events = run_demo_session()
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "session_demo.json"
    path.write_text(json.dumps(events, indent=2), encoding="utf-8")
    for e in events:
        print(f"{e['t']:>6}  {e['state']:<12}  {e['detail']}")
    print(f"Wrote {path}")
    return 0


def cmd_hypothesis_s4(_: argparse.Namespace) -> int:
    baseline = _ensure_baseline()
    log = build_hypothesis_log(baseline)
    path = write_hypothesis_log(log, OUT / "s4_hypothesis_log.json")
    print(f"Wrote {path}")
    for h in log["hypotheses"]:
        print(f"- {h['id']}: {h['statement']}")
    return 0


def cmd_noise_jargon(_: argparse.Namespace) -> int:
    baseline = _ensure_baseline()
    pack = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    stressed = score_pack(pack)
    comparison = compare_to_baseline(baseline, stressed)
    out = {
        "card": "WP-22",
        "label": "Executed",
        "config": {
            "clean_pack": "data/scripts/wp_scr_v0.json",
            "noise_jargon_pack": "data/scripts/wp_scr_v0_noise_jargon.json",
            "path": "workphone_lab noise-jargon",
        },
        "clean": baseline,
        "noise_jargon": stressed,
        "comparison": comparison,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s4_noise_jargon_scores.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    print(
        f"Clean intent: {comparison['clean_intent_accuracy']}  "
        f"Noise+jargon: {comparison['noise_jargon_intent_accuracy']}  "
        f"Delta: {comparison['delta_intent_accuracy']}"
    )
    print(f"H-S4-01 supported: {comparison['hypothesis_supported']}")
    for row in stressed["results"]:
        mark = "OK" if row["intent_ok"] else f"FAIL->{row['predicted_intent']} ({row.get('error_class')})"
        print(f"  {row['script_id']}: {mark}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="workphone_lab", description="Workphone lab simulator")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_base = sub.add_parser("baseline", help="Score WP-SCR-v0 clean scripts (S3-style)")
    p_base.set_defaults(func=cmd_baseline)

    p_sess = sub.add_parser("session", help="Demo ring-answer-greet-end session")
    p_sess.set_defaults(func=cmd_session)

    p_hyp = sub.add_parser("hypothesis-s4", help="Write S4 noise/jargon hypothesis log from S3 baseline")
    p_hyp.set_defaults(func=cmd_hypothesis_s4)

    p_nj = sub.add_parser("noise-jargon", help="Measure intent drop under noise+jargon vs clean baseline (WP-22)")
    p_nj.set_defaults(func=cmd_noise_jargon)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
