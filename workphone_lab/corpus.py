from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_corpus(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_corpus(root: Path, corpus: dict[str, Any]) -> dict[str, Any]:
    baseline_path = root / corpus["baseline_pack"]["path"]
    errors: list[str] = []
    if not baseline_path.exists():
        errors.append(f"missing baseline pack: {baseline_path}")
    else:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        if baseline.get("version") != corpus["baseline_pack"]["version"]:
            errors.append("baseline version mismatch vs corpus manifest")
        base_ids = {s["id"] for s in baseline["scripts"]}
    for vp in corpus["variant_packs"]:
        vpath = root / vp["path"]
        if not vpath.exists():
            errors.append(f"missing variant pack: {vpath}")
            continue
        variants = json.loads(vpath.read_text(encoding="utf-8"))
        if variants.get("linked_baseline_version") != corpus["baseline_pack"]["version"]:
            errors.append(f"{vp['pack_id']}: linked_baseline_version != {corpus['baseline_pack']['version']}")
        for s in variants["scripts"]:
            if s.get("base_id") not in base_ids:
                errors.append(f"{s.get('id')}: base_id {s.get('base_id')} not in clean pack")
    for row in corpus["variant_index"]:
        if row["baseline_version"] != corpus["baseline_pack"]["version"]:
            errors.append(f"index {row['variant_id']}: baseline_version tag mismatch")
    return {
        "corpus_id": corpus["corpus_id"],
        "version": corpus["version"],
        "baseline_version": corpus["baseline_pack"]["version"],
        "variant_count": len(corpus["variant_index"]),
        "ok": len(errors) == 0,
        "errors": errors,
    }
