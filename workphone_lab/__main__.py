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
from .evidence_index import align_evidence_index, load_evidence_index
from .evidence_gate import gate_s4
from .evidence_gate_s6 import gate_s6
from .evidence_gate_s8 import gate_s8, load_s8_gate
from .handoff_enforce import measure_enforcement
from .handoff_rules import demo_handoff_rules, load_rules
from .hypothesis_s4 import build_hypothesis_log, write_hypothesis_log
from .intake_map import load_field_map, validate_field_map
from .intake_schema import load_schema, validate_schema_pack
from .m4_freeze import evaluate_m4_freeze, load_m4_freeze
from .e2e_scenarios import load_e2e_pack, run_e2e_pack
from .m5_pack import assemble_m5, load_m5_pack
from .measure_policy import measure_packs
from .measure_summary import load_gt_pack, measure_summary_accuracy
from .negative_intake import load_cases, run_negative_cases
from .onboarding_map import demo_onboarding, load_onboard_map
from .ots_compare import compare_side_by_side
from .scoring import compare_to_baseline, score_pack
from .session import run_demo_session
from .status_board import load_board, render_board
from .status_board_freeze import freeze_status_board
from .summary_email import demo_summary, load_template
from .summary_failure_modes import evaluate_failure_modes, load_failure_modes
from .summary_latency import load_latency_pack, measure_summary_latency
from .system_failure_modes import evaluate_system_fm, load_system_fm
from .time_to_live import load_ttl_pack, measure_time_to_live
from .trade_profiles import load_trade_profiles, side_by_side as trade_side_by_side
from .voice_greeting import load_voice_cases, run_voice_greeting_pack

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
ONBOARD_MAP = ROOT / "data" / "onboarding" / "onboarding_form_to_agent_config_v0.json"
TRADE_PROFILES = ROOT / "data" / "onboarding" / "trade_profiles_v0.json"
VOICE_CASES = ROOT / "data" / "onboarding" / "voice_greeting_cases_v0.json"
TTL_RUNS = ROOT / "data" / "onboarding" / "time_to_live_runs_v0.json"
BOARD = ROOT / "data" / "status" / "u1_u3_status_board.json"
CORPUS_GATE = ROOT / "data" / "gates" / "corpus_gate_m3.json"
M4_FREEZE = ROOT / "data" / "gates" / "m4_intake_summary_freeze.json"
M5_PACK = ROOT / "data" / "gates" / "m5_concurrency_onboard_pack.json"
S8_GATE = ROOT / "data" / "gates" / "s8_concurrency_evidence_gate.json"
E2E_PACK = ROOT / "data" / "e2e" / "telephony_scenario_pack_v0.json"
SYS_FM = ROOT / "data" / "e2e" / "system_failure_modes_v0.json"
EVIDENCE_INDEX = ROOT / "data" / "evidence" / "evidence_index_v0.json"
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


def cmd_gate_s8(_: argparse.Namespace) -> int:
    gate = load_s8_gate(S8_GATE)
    report = gate_s8(ROOT, gate)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s8_evidence_gate.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lim = report["limits_statement"]
    print(f"Evidence Gate S8 concurrency pack (WP-46)")
    print(
        f"present={report['summary']['present']} missing={report['summary']['missing']} "
        f"gate_pass={report['summary']['gate_pass']}"
    )
    print(
        f"limits: safe_n={lim['safe_n']} break_point_n={lim.get('measured_break_point_n', lim['break_point_n'])} "
        f"max_delay={lim['max_answer_delay_s']}s"
    )
    for r in report["checklist"]:
        print(f"  [{r['status']}] {r['item']} -> {r['location']}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"U3 status: {report['summary']['u3_status']} ({report['summary']['u3_note']})")
    print(f"S8 closed: {report['summary']['s8_closed']}")
    print(f"Wrote {path}")
    return 0 if report["summary"]["gate_pass"] else 1


def cmd_onboarding_map(_: argparse.Namespace) -> int:
    mapping = load_onboard_map(ONBOARD_MAP)
    report = demo_onboarding(mapping)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s9_onboarding_map_report.json"
    demo_cfg = OUT / "s9_agent_config_demo.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    configs = [r["agent_config"] for r in report["results"] if r["agent_config"]]
    if configs:
        demo_cfg.write_text(json.dumps(configs[0], indent=2), encoding="utf-8")
    print(f"Onboarding map {report['map_id']} {report['version']} ({report['deliverable']})")
    print(f"fields={report['field_count']} groups={report['groups']} ok={report['ok']}")
    for step in report["mapping_path"]["steps"]:
        print(f"  path: {step}")
    for r in report["results"]:
        print(f"  [{r['example']}] form_ok={r['form_ok']} mapped={r['mapped_groups']}")
        for e in r["errors"]:
            print(f"    ERROR: {e}")
    print(f"Wrote {path}")
    if configs:
        print(f"Wrote {demo_cfg}")
    return 0 if report["ok"] else 1


def cmd_trade_profiles(_: argparse.Namespace) -> int:
    pack = load_trade_profiles(TRADE_PROFILES)
    scripts = json.loads(SCRIPTS.read_text(encoding="utf-8"))["scripts"]
    report = trade_side_by_side(pack, scripts)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s9_trade_profiles_side_by_side.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Trade profiles side-by-side (WP-48 / {report['hypothesis_id']})")
    print(
        f"profiles={report['profiles']} n={report['n_scripts']} "
        f"distinct_all={report['distinct_on_all']} both_correct={report['both_correct_on_all']} "
        f"supported={report['hypothesis_supported']}"
    )
    for row in report["side_by_side"]:
        print(
            f"  {row['script_id']}: distinct={row['behaviours_distinct']} "
            f"roof={row['roofing']['path_hint']} plumb={row['plumbing']['path_hint']} "
            f"ah={row['roofing']['after_hours_action']}/{row['plumbing']['after_hours_action']}"
        )
    print(f"Wrote {path}")
    return 0 if report["hypothesis_supported"] else 1


def cmd_voice_greeting(_: argparse.Namespace) -> int:
    pack = load_voice_cases(VOICE_CASES)
    report = run_voice_greeting_pack(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s9_voice_greeting_ws4.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Voice/greeting WS4 (WP-49) accepted={report['n_accepted']} failed={report['n_failed']}")
    print(f"all expect matched: {report['all_expect_matched']}")
    for a in report["accepted_configs"]:
        print(f"  ACCEPT {a['case_id']}: {a['voice_id']}/{a['voice_style']}")
    for f in report["failures"]:
        print(f"  FAIL {f['case_id']}: {', '.join(f['errors'])}")
    print(f"Wrote {path}")
    return 0 if report["all_expect_matched"] else 1


def cmd_time_to_live(_: argparse.Namespace) -> int:
    pack = load_ttl_pack(TTL_RUNS)
    report = measure_time_to_live(pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s9_time_to_live_distribution.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    d = report["distribution"]
    print(f"Time-to-live form_submit->callable (WP-50 / D-07)")
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


def cmd_e2e_scenarios(_: argparse.Namespace) -> int:
    pack = load_e2e_pack(E2E_PACK)
    clean = json.loads(SCRIPTS.read_text(encoding="utf-8"))
    noise = json.loads(SCRIPTS_NJ.read_text(encoding="utf-8"))
    neg = load_cases(NEG_CASES)
    schema = load_schema(SCHEMA)
    report = run_e2e_pack(
        pack,
        clean_scripts=clean,
        noise_scripts=noise,
        negative_cases=neg,
        schema=schema,
    )
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s10_e2e_telephony_scenario_pack.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    summ = report["summary"]
    print(f"E2E telephony scenario pack (WP-52 / {report['pack_id']} @ {report['version']})")
    print(
        f"scenarios={summ['scenarios']} expect_met={summ['expect_met']} "
        f"pack_pass={summ['pack_pass']}"
    )
    for row in report["results"]:
        print(f"  {row['id']}: {row.get('outcome')} expect_met={row.get('expect_met')}")
    for note in report["d08_notes"]:
        print(f"  D-08 {note}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if summ["pack_pass"] else 1


def cmd_system_fm(_: argparse.Namespace) -> int:
    library = load_system_fm(SYS_FM)
    report = evaluate_system_fm(library)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s10_system_failure_modes.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"System-only failure modes {report['library_id']} {report['version']} (WP-53)")
    print(
        f"probes={report['n_probes']} defects={report['n_defects']} "
        f"rule_ok={report['rule_ok']} notes_filed={report['notes_filed_for_d08']}"
    )
    for r in report["results"]:
        mark = "DEFECT" if r["defect"] else "ok"
        print(f"  {r['probe_id']} {r['mode_id']}: {mark} ({r['detail']})")
    for note in report["d08_notes"]:
        print(f"  D-08 {note}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if report["rule_ok"] and report["notes_filed_for_d08"] else 1


def cmd_freeze_status_board(_: argparse.Namespace) -> int:
    board = load_board(BOARD)
    report = freeze_status_board(board)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s10_status_board_draft_freeze.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    # Also refresh the simple board export
    simple = render_board(board)
    simple["card"] = "WP-54"
    simple["freeze_tag"] = board.get("freeze_tag")
    (OUT / "s5_u1_status_board.json").write_text(json.dumps(simple, indent=2), encoding="utf-8")
    summ = report["summary"]
    print(f"Status board draft freeze {report['freeze_tag']} (WP-54)")
    print(
        f"uncertainties={summ['uncertainties']} by_status={summ['by_status']} "
        f"freeze_pass={summ['freeze_pass']}"
    )
    for row in report["rows"]:
        print(
            f"  {row['id']}: {row['status']} "
            f"(evidence={row['evidence_count']}, labels={row['labels']})"
        )
    for uid in ("U1", "U2", "U3"):
        print(f"{uid} pointers:")
        for p in board["uncertainties"][uid]["evidence_pointers"]:
            print(f"  - {p['card']} [{p['label']}]: {p['note']}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if summ["freeze_pass"] else 1


def cmd_evidence_index(_: argparse.Namespace) -> int:
    pack = load_evidence_index(EVIDENCE_INDEX)
    report = align_evidence_index(ROOT, pack)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s10_evidence_index_timesheet_alignment.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    hs = report["hours_summary"]
    es = report["evidence_summary"]
    print(f"Evidence index {report['index_id']} {report['version']} (WP-55 / D-09)")
    print(
        f"hours_aligned={hs['hours_aligned']} youtrack={hs['youtrack_total_hours']} "
        f"labour={hs['labour_target_total_hours']} delta={hs['delta_hours']}"
    )
    for r in report["role_alignment"]:
        mark = "OK" if r["aligned"] else "MISS"
        print(
            f"  {r['role_key']}: yt={r['youtrack_hours']} target={r['labour_target_hours']} "
            f"delta={r['delta_hours']} {mark}"
        )
    print(
        f"evidence present={es['present']} planned={es['planned']} "
        f"missing={es['missing']} missing_through_wp55={es['missing_through_wp55']}"
    )
    print(
        f"roles_only_ok={report['roles_only_ok']} index_pass={report['summary']['index_pass']}"
    )
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"Wrote {path}")
    return 0 if report["summary"]["index_pass"] else 1


def cmd_gate_m5(_: argparse.Namespace) -> int:
    gate = load_m5_pack(M5_PACK)
    report = assemble_m5(ROOT, gate)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "s9_m5_concurrency_onboard_pack.json"
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    lim = report["concurrency_limits"]
    print(f"M5 pack {report['pack_tag']} (WP-51)")
    print(
        f"present={report['summary']['present']} missing={report['summary']['missing']} "
        f"pack_pass={report['summary']['pack_pass']}"
    )
    print(
        f"limits: safe_n={lim['safe_n']} break_point_n={lim['break_point_n']} "
        f"max_delay={lim['max_answer_delay_s']}s"
    )
    print("onboard path: " + " -> ".join(report["onboard_path_e2e"]["steps"]))
    for r in report["checklist"]:
        print(f"  [{r['status']}] {r['item']} -> {r['location']}")
    for g in report["explicit_gaps"]:
        print(f"  {g['id']} [{g['label']}] {g['item']}")
    for rj in report["rejected_configs"]:
        print(f"  {rj['id']}: {rj['config']}")
    print(f"S9 closed: {report['summary']['s9_closed']}")
    print(f"Wrote {path}")
    return 0 if report["summary"]["pack_pass"] else 1


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
        ("gate-s8", cmd_gate_s8),
        ("onboarding-map", cmd_onboarding_map),
        ("trade-profiles", cmd_trade_profiles),
        ("voice-greeting", cmd_voice_greeting),
        ("time-to-live", cmd_time_to_live),
        ("gate-m5", cmd_gate_m5),
        ("e2e-scenarios", cmd_e2e_scenarios),
        ("system-fm", cmd_system_fm),
        ("freeze-status-board", cmd_freeze_status_board),
        ("evidence-index", cmd_evidence_index),
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

    p_g8 = sub.add_parser("gate-s8", help="Evidence Gate concurrency pack + limits statement; U3 pointers (WP-46)")
    p_g8.set_defaults(func=cmd_gate_s8)

    p_ob = sub.add_parser("onboarding-map", help="Map onboarding form fields to agent config D-07 (WP-47)")
    p_ob.set_defaults(func=cmd_onboarding_map)

    p_tp = sub.add_parser("trade-profiles", help="Side-by-side roofing vs plumbing agent behaviour (WP-48)")
    p_tp.set_defaults(func=cmd_trade_profiles)

    p_vg = sub.add_parser("voice-greeting", help="Voice selection and greeting customization WS4 (WP-49)")
    p_vg.set_defaults(func=cmd_voice_greeting)

    p_ttl = sub.add_parser("time-to-live", help="Measure form-submit to callable number TTL for D-07 (WP-50)")
    p_ttl.set_defaults(func=cmd_time_to_live)

    p_m5 = sub.add_parser("gate-m5", help="Assemble M5 concurrency limits + onboard path pack / S9 close (WP-51)")
    p_m5.set_defaults(func=cmd_gate_m5)

    p_e2e = sub.add_parser("e2e-scenarios", help="Run E2E telephony scenario pack for D-08 (WP-52)")
    p_e2e.set_defaults(func=cmd_e2e_scenarios)

    p_sfm = sub.add_parser("system-fm", help="Document system-only failure modes for D-08 (WP-53)")
    p_sfm.set_defaults(func=cmd_system_fm)

    p_fsb = sub.add_parser("freeze-status-board", help="Freeze U1/U2/U3 status board draft (WP-54)")
    p_fsb.set_defaults(func=cmd_freeze_status_board)

    p_ei = sub.add_parser("evidence-index", help="Evidence index + YouTrack/timesheet alignment D-09 (WP-55)")
    p_ei.set_defaults(func=cmd_evidence_index)

    p_all = sub.add_parser("all", help="Run full lab suite smoke check")
    p_all.set_defaults(func=cmd_all)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
