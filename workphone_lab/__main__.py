from __future__ import annotations

import argparse
import json
from pathlib import Path

from .clarification import run_clarification_pack
from .corpus import load_corpus, validate_corpus
from .dialogue_policy import demo_policy, load_policy
from .evidence_gate import gate_s4
from .hypothesis_s4 import build_hypothesis_log, write_hypothesis_log
from .ots_compare import compare_side_by_side
from .scoring import compare_to_baseline, score_pack
from .session import run_demo_session

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "data" / "scripts" / "wp_scr_v0.json"
SCRIPTS_NJ = ROOT / "data" / "scripts" / "wp_scr_v0_noise_jargon.json"
CORPUS = ROOT / "data" / "corpus" / "regression_corpus.json"
POLICY = ROOT / "data" / "policy" / "dialogue_policy_v0.json"
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


def cmd_corpus(_: argparse.Namespace) -> int:
    corpus = load_corpus(CORPUS)
    report = validate_corpus(ROOT, corpus)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "regression_corpus_report.json"
    path.write_text(json.dumps({"manifest": corpus, "validation": report}, indent=2), encoding="utf-8")
    print(f"Corpus {report['corpus_id']} {report['version']}")
    print(f"Baseline linked: WP-SCR-v0 @ {report['baseline_version']}")
    print(f"Variants indexed: {report['variant_count']}")
    print(f"Validation OK: {report['ok']}")
    for err in report["errors"]:
        print(f"  ERROR: {err}")
    for row in corpus["variant_index"]:
        print(f"  {row['variant_id']} <- {row['base_id']} [{row['variant_version']}] {', '.join(row['tags'])}")
    print(f"Wrote {path}")
    return 0 if report["ok"] else 1


def cmd_clarify(_: argparse.Namespace) -> int:
    pack = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    report = run_clarification_pack(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s4_clarification_loop.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    print(
        f"helps={report['summary']['helps']}  "
        f"harms={report['summary']['harms']}  "
        f"no_change={report['summary']['no_change']}"
    )
    for r in report["results"]:
        print(
            f"  {r['script_id']}: conf={r['confidence']} "
            f"{r['before_intent']}->{r['after_intent']} => {r['outcome']}"
        )
    return 0


def cmd_compare_ots(_: argparse.Namespace) -> int:
    pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    report = compare_side_by_side(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s4_ots_vs_workphone.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    agg = report["aggregate"]
    print(f"Wrote {path}")
    print(
        f"Intent  OTS {agg['ots_intent_pass']}/{agg['n']}  "
        f"Workphone {agg['wp_intent_pass']}/{agg['n']}  "
        f"delta {agg['delta_intent_pass']:+d}"
    )
    print(
        f"Entity  OTS {agg['ots_entity_full']}/{agg['n']}  "
        f"Workphone {agg['wp_entity_full']}/{agg['n']}  "
        f"delta {agg['delta_entity_full']:+d}"
    )
    for r in report["results"]:
        print(
            f"  {r['script_id']}: OTS={r['ots_predicted']} WP={r['wp_predicted']} "
            f"d_intent={r['delta_intent']:+d} d_ent={r['delta_entities']:+d}"
        )
    return 0


def cmd_gate_s4(_: argparse.Namespace) -> int:
    # Refresh regenerable outputs so gate sees Present where possible
    _ensure_baseline()
    pack_nj = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "s4_noise_jargon_scores.json").write_text(
        json.dumps(
            {
                "card": "WP-22",
                "noise_jargon": score_pack(pack_nj),
                "comparison": compare_to_baseline(_ensure_baseline(), score_pack(pack_nj)),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    report = gate_s4(ROOT)
    path = OUT / "s4_evidence_gate.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    for row in report["checklist"]:
        print(f"  [{row['status']}] {row['item']} -> {row['location']}")
    print("Rejected configs:")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Gate pass: {report['summary']['gate_pass']}")
    return 0 if report["summary"]["gate_pass"] else 1


def cmd_policy(_: argparse.Namespace) -> int:
    policy = load_policy(POLICY)
    report = demo_policy(policy)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s5_dialogue_policy_demo.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Policy {report['policy_id']} {report['version']} (U2)")
    print(f"Path OK: {report['aggregate']['path_ok']}/{report['aggregate']['n']}")
    for r in report["results"]:
        mark = "OK" if r["ok"] else "FAIL"
        print(f"  [{mark}] {r['expected_path']} <- {r['utterance'][:48]}...")
    print(f"Wrote {path}")
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

    p_corp = sub.add_parser("corpus", help="Validate regression corpus version tags vs clean S3 baseline (WP-23)")
    p_corp.set_defaults(func=cmd_corpus)

    p_cl = sub.add_parser("clarify", help="Test clarification-loop prompts at low confidence (WP-24)")
    p_cl.set_defaults(func=cmd_clarify)

    p_ots = sub.add_parser("compare-ots", help="Side-by-side OTS vs Workphone on same scripts (WP-25)")
    p_ots.set_defaults(func=cmd_compare_ots)

    p_gate = sub.add_parser("gate-s4", help="Evidence Gate checklist for S4 close (WP-26)")
    p_gate.set_defaults(func=cmd_gate_s4)

    p_pol = sub.add_parser("policy", help="Demo dialogue policy estimate/emergency/inquiry (WP-27)")
    p_pol.set_defaults(func=cmd_policy)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
