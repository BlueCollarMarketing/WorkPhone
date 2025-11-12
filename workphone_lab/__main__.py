from __future__ import annotations

import argparse
import json
from pathlib import Path

from .hypothesis_s4 import build_hypothesis_log, write_hypothesis_log
from .scoring import score_pack
from .session import run_demo_session

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "data" / "scripts" / "wp_scr_v0.json"
OUT = ROOT / "outputs"


def cmd_baseline(_: argparse.Namespace) -> int:
    pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    report = score_pack(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s3_baseline_scores.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    print(f"Intent pass: {report['aggregate']['intent_pass']}/{report['aggregate']['n']}")
    print(f"Entity full: {report['aggregate']['entity_full']}/{report['aggregate']['n']}")
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
    baseline_path = OUT / "s3_baseline_scores.json"
    if not baseline_path.exists():
        pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(json.dumps(score_pack(pack), indent=2), encoding="utf-8")
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    log = build_hypothesis_log(baseline)
    path = write_hypothesis_log(log, OUT / "s4_hypothesis_log.json")
    print(f"Wrote {path}")
    for h in log["hypotheses"]:
        print(f"- {h['id']}: {h['statement']}")
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

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
