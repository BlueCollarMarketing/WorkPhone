from __future__ import annotations

import argparse
import json
from pathlib import Path

from .clarification import run_clarification_pack
from .concurrency_breakpoint import load_breakpoint_config, measure_breakpoint
from .concurrency_queue_rates import load_queue_config, measure_queue_rates
from .concurrency_scenarios import design_report, load_scenarios
from .concurrency_summary_fidelity import load_fidelity_config, spot_check_fidelity
from .corpus import load_corpus, validate_corpus
from .corpus_gate import evaluate_corpus_gate, load_json
from .dialogue_policy import demo_policy, load_policy
from .evidence_gate import gate_s4
from .evidence_gate_s6 import gate_s6
from .handoff_enforce import measure_enforcement
from .handoff_rules import demo_handoff_rules, load_rules
from .hypothesis_s4 import build_hypothesis_log, write_hypothesis_log
from .intake_map import load_field_map, validate_field_map
from .intake_schema import load_schema, validate_schema_pack
from .m4_freeze import evaluate_m4_freeze, load_m4_freeze
from .measure_policy import measure_packs
from .measure_summary import load_gt_pack, measure_summary_accuracy
from .negative_intake import load_cases, run_negative_cases
from .ots_compare import compare_side_by_side
from .scoring import compare_to_baseline, score_pack
from .session import run_demo_session
from .status_board import load_board, render_board
from .summary_email import demo_summary, load_template
from .summary_failure_modes import evaluate_failure_modes, load_failure_modes
from .summary_latency import load_latency_pack, measure_summary_latency

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "data" / "scripts" / "wp_scr_v0.json"
SCRIPTS_NJ = ROOT / "data" / "scripts" / "wp_scr_v0_noise_jargon.json"
CORPUS = ROOT / "data" / "corpus" / "regression_corpus.json"
POLICY = ROOT / "data" / "policy" / "dialogue_policy_v0.json"
INTAKE = ROOT / "data" / "intake" / "intake_field_map_v0.json"
SCHEMA = ROOT / "data" / "intake" / "intake_schema_v0.json"
NEG_CASES = ROOT / "data" / "intake" / "negative_intake_cases_v0.json"
HANDOFF_RULES = ROOT / "data" / "handoff" / "handoff_rules_v0.json"
SUMMARY_TMPL = ROOT / "data" / "summary" / "summary_email_template_v0.json"
SUMMARY_GT = ROOT / "data" / "summary" / "ground_truth_call_notes_v0.json"
SUMMARY_LAT = ROOT / "data" / "summary" / "summary_latency_runs_v0.json"
SUMMARY_FM = ROOT / "data" / "summary" / "summary_failure_modes_v0.json"
CONC_SCENARIOS = ROOT / "data" / "concurrency" / "load_scenarios_v0.json"
CONC_BREAK = ROOT / "data" / "concurrency" / "breakpoint_config_v0.json"
CONC_QUEUE = ROOT / "data" / "concurrency" / "queue_rates_config_v0.json"
CONC_FIDELITY = ROOT / "data" / "concurrency" / "summary_fidelity_under_load_v0.json"
BOARD = ROOT / "data" / "status" / "u1_u3_status_board.json"
CORPUS_GATE = ROOT / "data" / "gates" / "corpus_gate_m3.json"
M4_FREEZE = ROOT / "data" / "gates" / "m4_intake_summary_freeze.json"
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


def cmd_intake(_: argparse.Namespace) -> int:
    fmap = load_field_map(INTAKE)
    report = validate_field_map(fmap)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s5_intake_field_map_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Intake map {report['map_id']} {report['version']} ({report['deliverable']})")
    print(f"Fields: {report['field_count']}  Call types: {', '.join(report['call_types'])}")
    for ct, spec in report["summary_table"].items():
        print(f"  {ct}: required={spec['required']}")
    print(f"Validation OK: {report['ok']}")
    for err in report["errors"]:
        print(f"  ERROR: {err}")
    print(f"Wrote {path}")
    return 0 if report["ok"] else 1


def cmd_measure_policy(_: argparse.Namespace) -> int:
    policy = load_policy(POLICY)
    clean = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    nj = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    report = measure_packs(policy, [clean, nj])
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s5_policy_completion_wrong_path.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    agg = report["aggregate"]
    print(f"Policy {report['policy_id']} @ {report['policy_version']} on versioned corpus")
    print(f"N={agg['n']}  mean completion={agg['completion_rate_mean']}  fully complete={agg['fully_complete_rate']}")
    print(f"Wrong-path rate={agg['wrong_path_rate']} ({agg['wrong_path_count']}/{agg['n']})")
    for r in report["results"]:
        wp = "WRONG" if r["wrong_path"] else "ok"
        print(
            f"  {r['script_id']}: path {r['expected_path']}->{r['routed_path']} [{wp}] "
            f"completion={r['completion_rate']}"
        )
    print(f"Wrote {path}")
    return 0


def cmd_status_board(_: argparse.Namespace) -> int:
    board = load_board(BOARD)
    report = render_board(board)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s5_u1_status_board.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Status board {report['board_id']} {report['version']}")
    for row in report["rows"]:
        print(f"  {row['id']}: {row['status']} (evidence={row['evidence_count']}, labels={row['labels']})")
    print("U1 pointers:")
    for p in report["u1"]["evidence_pointers"]:
        print(f"  - {p['card']} [{p['label']}]: {p['note']}")
    print(f"Wrote {path}")
    return 0


def cmd_corpus_gate(_: argparse.Namespace) -> int:
    gate = load_json(CORPUS_GATE)
    corpus = load_corpus(CORPUS)
    policy = load_policy(POLICY)
    # M3 decision: record PASS for tagged approved corpus (no unauthorized bulk change)
    report = evaluate_corpus_gate(gate, corpus, policy, proposed_bulk_policy_change=True)
    # Also show blocked example if corpus version were wrong
    blocked_demo = evaluate_corpus_gate(
        gate,
        {**corpus, "version": "v999-unapproved"},
        policy,
        proposed_bulk_policy_change=True,
    )
    out = {
        "m3_decision": report,
        "blocked_if_unapproved_corpus_demo": blocked_demo,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s5_corpus_gate_m3.json"
    path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Corpus gate {report['gate_id']} ({report['milestone']})")
    print(
        f"Tagged corpus: {report['corpus_tagged']['corpus_id']} @ {report['corpus_tagged']['version']} "
        f"(approved={report['corpus_tagged']['matches_approved']})"
    )
    print(f"M3 decision: {report['decision']} — {report['reason']}")
    print(f"Demo BLOCKED if unapproved: {blocked_demo['decision']}")
    print(f"Wrote {path}")
    return 0 if report["decision"] == "PASS" else 1


def cmd_schema(_: argparse.Namespace) -> int:
    schema = load_schema(SCHEMA)
    report = validate_schema_pack(schema)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s6_intake_schema_report.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Schema {report['schema_id']} {report['version']} ({report['deliverable']})")
    print(f"Groups: {', '.join(report['groups'])}")
    for r in report["results"]:
        print(f"  {r['example']}: {'OK' if r['ok'] else 'FAIL'} {r.get('errors') or ''}")
    print(f"Pack validation OK: {report['ok']}")
    print(f"Wrote {path}")
    return 0 if report["ok"] else 1


def cmd_handoff(_: argparse.Namespace) -> int:
    schema = load_schema(SCHEMA)
    clean = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    nj = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    report = measure_enforcement([clean, nj], schema)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s6_handoff_enforcement.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    agg = report["aggregate"]
    print("Required-field handoff enforcement (WP-33)")
    print(
        f"incomplete without={agg['incomplete_rate_without']}  "
        f"with={agg['incomplete_rate_with']}  delta={agg['incomplete_delta']}"
    )
    print(
        f"allowed conversion with={agg['allowed_conversion_rate_with']}  "
        f"wrong={agg['wrong_rate_with']}  supported={agg['hypothesis_supported']}"
    )
    print(f"Wrote {path}")
    return 0


def cmd_channels(_: argparse.Namespace) -> int:
    rules = load_rules(HANDOFF_RULES)
    schema = load_schema(SCHEMA)
    clean = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    report = demo_handoff_rules(rules, schema, [clean])
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s6_handoff_channels.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Handoff rules {report['rules_id']} {report['version']} ({report['workstream']})")
    print(f"Channels: {', '.join(report['channels_defined'])}  label={report['label']}")
    for r in report["results"]:
        print(f"  {r['script_id']}: allowed={r['allowed']} -> {r['channels']}")
    print(f"Wrote {path}")
    return 0


def cmd_negative(_: argparse.Namespace) -> int:
    pack = load_cases(NEG_CASES)
    report = run_negative_cases(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s6_negative_intake.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Negative intake {report['pack_id']} {report['version']}")
    print(f"Pass {report['aggregate']['pass']}/{report['aggregate']['n']}  safe={report['aggregate']['safe_no_fabricate']}")
    for r in report["results"]:
        print(f"  {r['id']}: {'OK' if r['ok'] else 'FAIL'} {r['reasons']}")
    print(f"Wrote {path}")
    return 0 if report["aggregate"]["safe_no_fabricate"] else 1


def cmd_gate_s6(_: argparse.Namespace) -> int:
    # refresh regenerable exports
    cmd_schema(_)
    cmd_handoff(_)
    cmd_negative(_)
    report = gate_s6(ROOT)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s6_evidence_gate.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {path}")
    for row in report["checklist"]:
        print(f"  [{row['status']}] {row['item']} -> {row['location']}")
    wr = report["wrong_rate_summary"]
    print(
        f"Wrong/incomplete rates: without={wr['incomplete_rate_without']} "
        f"with={wr['incomplete_rate_with']} wrong={wr['wrong_rate_with']}"
    )
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Gate pass: {report['summary']['gate_pass']}")
    return 0 if report["summary"]["gate_pass"] else 1


def cmd_summary(_: argparse.Namespace) -> int:
    tmpl = load_template(SUMMARY_TMPL)
    schema = load_schema(SCHEMA)
    report = demo_summary(tmpl, schema.get("examples", {}))
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s7_summary_email_demo.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Summary template {report['template_id']} {report['version']} ({report['deliverable']})")
    for r in report["results"]:
        print(f"  [{r['example']}] {r['email']['subject']}")
        print(f"    fields={r['fields']}")
    print(f"Wrote {path}")
    return 0


def cmd_measure_summary(_: argparse.Namespace) -> int:
    gt = load_gt_pack(SUMMARY_GT)
    pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    scripts_by_id = {s["id"]: s for s in pack["scripts"]}
    report = measure_summary_accuracy(gt, scripts_by_id)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s7_summary_field_accuracy.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Summary field accuracy (WP-38 / {report['hypothesis_id']})")
    print(
        f"accuracy={report['field_accuracy']}  invent_rate={report['invent_rate']}  "
        f"omit_rate={report['omit_rate']}  n_notes={report['n_notes']}"
    )
    print(f"targets: accuracy>={report['targets']['field_accuracy_min']} invent<={report['targets']['invent_rate_max']}")
    print(f"H-S7-01 supported: {report['hypothesis_supported']}")
    for row in report["results"]:
        print(
            f"  {row['note_id']}: acc={row['field_accuracy']} "
            f"omit={row['counts']['omit']} invent={row['counts']['invent']} wrong={row['counts']['wrong']}"
        )
    print(f"Wrote {path}")
    return 0 if report["hypothesis_supported"] else 1


def cmd_summary_latency(_: argparse.Namespace) -> int:
    pack = load_latency_pack(SUMMARY_LAT)
    report = measure_summary_latency(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s7_summary_latency_distribution.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    d = report["distribution"]
    print(f"Summary latency call_end->email (WP-39 / U3)")
    print(
        f"n={d['n']}  min={d['min_s']}s  p50={d['p50_s']}s  p90={d['p90_s']}s  "
        f"p95={d['p95_s']}s  max={d['max_s']}s  mean={d['mean_s']}s"
    )
    print(f"within draft targets: {report['within_draft_targets']}")
    for b in d["histogram_s"]:
        hi = f"{b['hi_s']}" if b["hi_s"] is not None else "inf"
        print(f"  bin [{b['lo_s']},{hi}): {b['count']}")
    print(f"Wrote {path}")
    return 0


def cmd_summary_fm(_: argparse.Namespace) -> int:
    library = load_failure_modes(SUMMARY_FM)
    report = evaluate_failure_modes(library)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s7_summary_failure_modes.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Summary failure modes {report['library_id']} {report['version']} (WP-40)")
    print(
        f"probes={report['n_probes']} defects={report['n_defects']} "
        f"invent_defects={report['invent_defects']} rule_ok={report['rule_ok']}"
    )
    for r in report["results"]:
        mark = "DEFECT" if r["defect"] else "ok"
        invent = " invent=defect" if r["invent_kept_as_defect"] else ""
        print(f"  {r['probe_id']} {r['mode_id']}: {mark}{invent} ({r['detail']})")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if report["rule_ok"] else 1


def cmd_gate_m4(_: argparse.Namespace) -> int:
    gate = load_m4_freeze(M4_FREEZE)
    report = evaluate_m4_freeze(ROOT, gate)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s7_m4_intake_summary_freeze.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"M4 freeze {report['freeze_tag']} (WP-41)")
    print(
        f"present={report['summary']['present']} missing={report['summary']['missing']} "
        f"gaps={report['summary']['explicit_gaps']} freeze_pass={report['summary']['freeze_pass']}"
    )
    for r in report["checklist"]:
        print(f"  [{r['status']}] {r['item']} -> {r['location']}")
    print("Explicit gaps (do not block freeze):")
    for g in report["explicit_gaps"]:
        print(f"  {g['id']} [{g['label']}] {g['item']}: {g['note']}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"S7 closed: {report['summary']['s7_closed']}")
    print(f"Wrote {path}")
    return 0 if report["summary"]["freeze_pass"] else 1


def cmd_concurrency_scenarios(_: argparse.Namespace) -> int:
    pack = load_scenarios(CONC_SCENARIOS)
    report = design_report(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s8_concurrency_load_scenarios.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Concurrency load scenarios {report['pack_id']} {report['version']} (WP-42 / U3)")
    print(
        f"soft_cap_n={report['limits']['lab_soft_cap_n']} "
        f"hard_cap_n={report['limits']['lab_hard_cap_n']} design_ok={report['design_ok']}"
    )
    for sc in report["scenarios"]:
        print(
            f"  {sc['id']}: N={sc['simultaneous_calls']} stagger_ms={sc['stagger_ms']} "
            f"legs={len(sc['dry_run_legs'])} ok={sc['design_ok']}"
        )
    for err in report["errors"]:
        print(f"  ERROR: {err}")
    print(f"Wrote {path}")
    return 0 if report["design_ok"] else 1


def cmd_concurrency_breakpoint(_: argparse.Namespace) -> int:
    cfg = load_breakpoint_config(CONC_BREAK)
    report = measure_breakpoint(cfg)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s8_concurrency_breakpoint.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Concurrency breakpoint (WP-43 / {report['hypothesis_id']})")
    print(
        f"break_point_n={report['break_point_n']} last_ok_n={report['last_ok_n']} "
        f"supported={report['hypothesis_supported']}"
    )
    for row in report["sweep"]:
        mark = "OK" if row["within_limits"] else "FAIL:" + ",".join(row["fail_reasons"])
        print(
            f"  N={row['n']}: max_delay={row['max_answer_delay_s']} "
            f"drop_rate={row['drop_rate']} {mark}"
        )
    exe = report["provider_configs"]["executed"]
    plan = report["provider_configs"]["planned"]
    print(f"  provider Executed: {exe['numbering']}")
    print(f"  provider Planned: {plan['alternate_sip_trunk']} (limit unset)")
    print(f"Wrote {path}")
    return 0 if report["hypothesis_supported"] else 1


def cmd_concurrency_queue(_: argparse.Namespace) -> int:
    cfg = load_queue_config(CONC_QUEUE)
    report = measure_queue_rates(cfg)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s8_concurrency_queue_rates.json"
    logs_path = OUT / "s8_u3_concurrency_provider_logs.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logs_path.write_text(
        json.dumps(
            {
                "u3_pack": report["u3_pack"],
                "card": "WP-44",
                "label": "Executed",
                "retained": True,
                "n_logs": report["provider_log_count"],
                "logs": report["provider_logs"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    agg = report["aggregate"]
    print(f"Queue/drop/error rates under load (WP-44 / {report['u3_pack']})")
    print(
        f"aggregate drop_rate={agg['queue_drop_rate']} error_rate={agg['error_rate']} "
        f"answer_rate={agg['answer_rate']} offered={agg['offered']}"
    )
    for row in report["results"]:
        print(
            f"  {row['id']} N={row['n']}: drop={row['queue_drop_rate']} "
            f"error={row['error_rate']} answered={row['answered']}/{row['offered']}"
        )
    print(f"provider logs retained: {report['provider_log_count']} -> {logs_path.name}")
    print(f"Wrote {path}")
    return 0


def cmd_concurrency_fidelity(_: argparse.Namespace) -> int:
    cfg = load_fidelity_config(CONC_FIDELITY)
    gt = load_gt_pack(SUMMARY_GT)
    pack = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    scripts_by_id = {s["id"]: s for s in pack["scripts"]}
    report = spot_check_fidelity(cfg, gt, scripts_by_id)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s8_summary_fidelity_under_load.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Summary fidelity under load (WP-45 / {report['hypothesis_id']})")
    print(
        f"collapse_flagged={report['collapse_flagged']} rule_ok={report['rule_ok']} "
        f"supported={report['hypothesis_supported']}"
    )
    for row in report["results"]:
        collapse = " COLLAPSE" if row["silent_collapse_flagged"] else ""
        print(
            f"  {row['id']} N={row['n']}: acc={row['field_accuracy']} "
            f"invent={row['invent_count']} omit={row['omit_count']} "
            f"pass={row['check_pass']}{collapse}"
        )
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if report["hypothesis_supported"] else 1


def cmd_all(_: argparse.Namespace) -> int:
    """Run the full lab suite (smoke check that the project is runnable)."""
    steps = [
        ("baseline", cmd_baseline),
        ("session", cmd_session),
        ("hypothesis-s4", cmd_hypothesis_s4),
        ("noise-jargon", cmd_noise_jargon),
        ("corpus", cmd_corpus),
        ("clarify", cmd_clarify),
        ("compare-ots", cmd_compare_ots),
        ("gate-s4", cmd_gate_s4),
        ("policy", cmd_policy),
        ("intake", cmd_intake),
        ("measure-policy", cmd_measure_policy),
        ("status-board", cmd_status_board),
        ("corpus-gate", cmd_corpus_gate),
        ("schema", cmd_schema),
        ("handoff", cmd_handoff),
        ("channels", cmd_channels),
        ("negative", cmd_negative),
        ("gate-s6", cmd_gate_s6),
        ("summary", cmd_summary),
        ("measure-summary", cmd_measure_summary),
        ("summary-latency", cmd_summary_latency),
        ("summary-fm", cmd_summary_fm),
        ("gate-m4", cmd_gate_m4),
        ("concurrency-scenarios", cmd_concurrency_scenarios),
        ("concurrency-breakpoint", cmd_concurrency_breakpoint),
        ("concurrency-queue", cmd_concurrency_queue),
        ("concurrency-fidelity", cmd_concurrency_fidelity),
    ]
    print("=== workphone_lab all ===")
    for name, fn in steps:
        print(f"\n--- {name} ---")
        code = fn(_)
        if code != 0:
            print(f"FAILED at {name} (exit {code})")
            return code
    print("\n=== all steps OK ===")
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

    p_in = sub.add_parser("intake", help="Validate intake field map per call type for D-04 (WP-28)")
    p_in.set_defaults(func=cmd_intake)

    p_mp = sub.add_parser("measure-policy", help="Measure policy completion and wrong-path rate on corpus (WP-29)")
    p_mp.set_defaults(func=cmd_measure_policy)

    p_sb = sub.add_parser("status-board", help="Print U1-U3 status board with evidence labels (WP-30)")
    p_sb.set_defaults(func=cmd_status_board)

    p_cg = sub.add_parser("corpus-gate", help="Corpus gate before bulk policy changes — M3 (WP-31)")
    p_cg.set_defaults(func=cmd_corpus_gate)

    p_sc = sub.add_parser("schema", help="Validate intake schema for contractor call fields (WP-32)")
    p_sc.set_defaults(func=cmd_schema)

    p_hf = sub.add_parser("handoff", help="Required-field enforcement on intake handoffs (WP-33)")
    p_hf.set_defaults(func=cmd_handoff)

    p_ch = sub.add_parser("channels", help="Handoff rules email/SMS/CRM stub on Executed path (WP-34)")
    p_ch.set_defaults(func=cmd_channels)

    p_neg = sub.add_parser("negative", help="Negative intake cases refuse/partial/callback (WP-35)")
    p_neg.set_defaults(func=cmd_negative)

    p_g6 = sub.add_parser("gate-s6", help="Evidence Gate intake schema and wrong-rate tables (WP-36)")
    p_g6.set_defaults(func=cmd_gate_s6)

    p_sum = sub.add_parser("summary", help="Render post-call summary email template D-05 (WP-37)")
    p_sum.set_defaults(func=cmd_summary)

    p_ms = sub.add_parser("measure-summary", help="Score summary invent/omit vs ground-truth notes (WP-38)")
    p_ms.set_defaults(func=cmd_measure_summary)

    p_sl = sub.add_parser("summary-latency", help="Measure call-end to email latency distribution for U3 (WP-39)")
    p_sl.set_defaults(func=cmd_summary_latency)

    p_fm = sub.add_parser("summary-fm", help="Log summary failure modes delay/wrong-number/hallucination (WP-40)")
    p_fm.set_defaults(func=cmd_summary_fm)

    p_m4 = sub.add_parser("gate-m4", help="Freeze intake+summary core path for M4 / S7 close (WP-41)")
    p_m4.set_defaults(func=cmd_gate_m4)

    p_cs = sub.add_parser("concurrency-scenarios", help="Design 2/3/N inbound load scenarios for U3 (WP-42)")
    p_cs.set_defaults(func=cmd_concurrency_scenarios)

    p_cb = sub.add_parser("concurrency-breakpoint", help="Measure concurrent drop/answer-delay break-point N (WP-43)")
    p_cb.set_defaults(func=cmd_concurrency_breakpoint)

    p_cq = sub.add_parser("concurrency-queue", help="Measure queue/drop/error rates under load; retain provider logs (WP-44)")
    p_cq.set_defaults(func=cmd_concurrency_queue)

    p_cf = sub.add_parser("concurrency-fidelity", help="Spot-check summary fidelity under load; flag invent/omit collapse (WP-45)")
    p_cf.set_defaults(func=cmd_concurrency_fidelity)

    p_all = sub.add_parser("all", help="Run full lab suite smoke check")
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
