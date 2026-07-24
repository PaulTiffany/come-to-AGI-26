"""Build deterministic scene data from published evidence and narrative sources."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SCHEMA = "bgi-open-build.bellman-film-scene-data.v1"
SUBMISSION_COMMIT = "d4c0bbd103849b8afb1019921684a062482d08cc"
RESEARCH_COMMIT = "617f8979daa921d326301266e55740c0746ab95c"
FABRICPC_COMMIT = "32ae295182ab944b8f084abaf4a40da2c50bab5f"
EVIDENCE_BUNDLE = "6b48262f49e6cad498a23ff6e075f1f8522e831004f8cb3dbaeecfe46e28dc05"
REGRETS = {
    "no_pricing": 0.371,
    "pacing": 0.371,
    "exact_belief": 0.000,
    "hmm": 0.000,
    "ridge": 0.000,
    "fixed_prior": 0.057,
    "inverted": 0.057,
    "fabricpc_backprop": 0.314,
    "fabricpc_pcn": 0.314,
    "shuffled_fabricpc": 0.457,
}


def sha256(path: Path) -> str:
    """Return the SHA-256 digest of a file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected JSON object: {path}")
    return value


def require_text(path: Path, fragments: list[str]) -> str:
    """Read a source and require every authoritative fragment."""
    text = path.read_text(encoding="utf-8")
    missing = [fragment for fragment in fragments if fragment not in text]
    if missing:
        raise ValueError(f"{path} is missing required fragments: {missing}")
    return text


def extract_printed_int(notebook: dict[str, Any], key: str) -> int:
    """Extract one printed integer from executed notebook stream output."""
    for cell in notebook.get("cells", []):
        texts = ["".join(cell.get("source", []))]
        texts.extend("".join(output.get("text", [])) for output in cell.get("outputs", []))
        for text in texts:
            match = re.search(rf"(?m)^{re.escape(key)}=(\d+)$", text)
            if match:
                return int(match.group(1))
    raise ValueError(f"Could not find {key}=<int> in notebook")


def build(repo_root: Path, compitum_root: Path) -> dict[str, Any]:
    """Assemble and validate the film's portable scene data."""
    evidence = repo_root / "BGI-Open-Build" / "evidence"
    index_path = evidence / "evidence-index.json"
    index = load_json(index_path)
    if index.get("bundle_sha256") != EVIDENCE_BUNDLE:
        raise ValueError("Evidence bundle hash does not match the accepted bundle")
    if index.get("schema") != "bgi-open-build.evidence-index.v1":
        raise ValueError("Unexpected evidence-index schema")

    submission = compitum_root / "SUBMISSION.md"
    narrative = compitum_root / "handoff" / "bellman_shadow_pricing" / "NARRATIVE_SOURCE.md"
    claims = compitum_root / "handoff" / "bellman_shadow_pricing" / "CLAIMS.md"
    require_text(
        submission,
        [
            "recoverable gap (pacing regret",
            "| 0.371 |",
            "FabricPC captured fraction of recoverable gap | 15.4%",
            "0.314 mean regret",
            RESEARCH_COMMIT,
            FABRICPC_COMMIT,
        ],
    )
    require_text(
        narrative,
        [
            "prices the whole action by the actual drop in continuation value",
            "zero exceptions",
            "fixed network topology",
        ],
    )
    require_text(
        claims,
        [
            "exact-belief regret 0.000",
            "tied exactly on held-out regret: 0.314 mean",
            "captures only\n  15.4% of the recoverable regret gap",
        ],
    )

    boundary_source = evidence / "local_sources" / "04_belief_sensitive_boundary.py"
    boundary_text = require_text(
        boundary_source,
        [
            "remaining_steps = 1",
            "reachable_budget = 4.5",
            "low_belief = 0.05",
            "high_belief = 0.2",
            'low_action == "spend"',
            'high_action == "opportunity"',
        ],
    )
    if "threshold" in boundary_text.lower():
        raise ValueError("Boundary adapter unexpectedly asserts a threshold")

    equivalence_notebook_path = (
        evidence / "notebooks" / "03_online_optimal_equivalence.ipynb"
    )
    equivalence_notebook = load_json(equivalence_notebook_path)
    mismatches = extract_printed_int(equivalence_notebook, "mismatches")
    if mismatches != 0:
        raise ValueError("Published equivalence notebook is not mismatch-free")

    certificate_hashes: dict[str, str] = {}
    certificate_paths: dict[str, str] = {}
    for item in index["items"]:
        certificate_rel = Path(item["links"]["certificate"])
        certificate_path = evidence / certificate_rel
        certificate = load_json(certificate_path)
        green = all(
            certificate.get(field) is True
            for field in ("policy_ok", "source_ran", "notebook_ran", "validation_passed")
        )
        if not green:
            raise ValueError(f"Primary certificate is not green: {certificate_rel}")
        certificate_hashes[item["id"]] = sha256(certificate_path)
        certificate_paths[item["id"]] = (
            Path("BGI-Open-Build") / "evidence" / certificate_rel
        ).as_posix()

    return {
        "schema": SCHEMA,
        "revisions": {
            "submission_commit": SUBMISSION_COMMIT,
            "research_commit": RESEARCH_COMMIT,
            "fabricpc_commit": FABRICPC_COMMIT,
        },
        "evidence_bundle_sha256": EVIDENCE_BUNDLE,
        "historical_context": {
            "existing_shadow_prices": "retrospective local finite-difference diagnostics",
            "selection_role": "report-only; absent from the operative route-selection objective",
            "display_language": [
                "Compitum had prices.",
                "It did not let them choose.",
            ],
        },
        "research_question": "Can predicted hidden scarcity be converted into a useful routing price?",
        "discovered_bottleneck": "scalar price times lumpy consumption",
        "interpretation": {
            "model_verdict": {
                "statement": "The bounded FabricPC predictor did not clear the gate.",
                "pcn_regret": 0.314,
                "same_topology_backprop_regret": 0.314,
                "recoverable_gap_percent": 15.4,
            },
            "program_verdict": {
                "statement": "The FabricPC intervention recovered Compitum's missing action-pricing mechanism.",
                "exact_bellman_charge_recovered_full_gap": True,
                "online_optimal_mismatches": mismatches,
            },
            "summary": "The model lost. The experiment succeeded.",
        },
        "certificate_sha256": dict(sorted(certificate_hashes.items())),
        "certified_boundary": {
            "remaining_steps": 1,
            "reachable_budget": 4.5,
            "observed_opportunity": True,
            "low": {"belief": 0.05, "action": "spend"},
            "high": {"belief": 0.20, "action": "opportunity"},
            "exact_transition_asserted": False,
        },
        "online_equivalence": {"mismatch_count": mismatches},
        "tranche7_regret": REGRETS,
        "fabricpc_recoverable_gap_percent": 15.4,
        "claim_sources": {
            "historical_context": [
                "compitum-fabricpc/docs/Control-of-Error.md",
                "compitum-fabricpc/docs/adr/0001-fabricpc-trajectory-observer.md",
                "compitum-fabricpc/docs/adr/0002-constraint-pressure-oracle.md",
                "compitum-fabricpc/src/compitum/router.py",
            ],
            "fabricpc_research_instrument": [
                "compitum-fabricpc/SUBMISSION.md",
                "compitum-fabricpc/handoff/bellman_shadow_pricing/NARRATIVE_SOURCE.md",
                "compitum-fabricpc/handoff/bellman_shadow_pricing/CLAIMS.md",
            ],
            "whole_action_charge": [
                "compitum-fabricpc/SUBMISSION.md",
                "compitum-fabricpc/handoff/bellman_shadow_pricing/NARRATIVE_SOURCE.md",
            ],
            "bellman_equivalence": [
                "compitum-fabricpc/handoff/bellman_shadow_pricing/CLAIMS.md",
                "BGI-Open-Build/evidence/notebooks/03_online_optimal_equivalence.ipynb",
            ],
            "certified_boundary": [
                "BGI-Open-Build/evidence/local_sources/04_belief_sensitive_boundary.py",
                certificate_paths["belief-sensitive-boundary"],
            ],
            "tranche7_regret": [
                "compitum-fabricpc/SUBMISSION.md",
                "compitum-fabricpc/handoff/bellman_shadow_pricing/CLAIMS.md",
            ],
            "certificate_marks": list(certificate_paths.values()),
        },
    }


def main() -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument(
        "--compitum-root", type=Path, default=Path(r"C:\src\compitum-fabricpc")
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = Path(__file__).with_name("scene_data.json")
    built = build(args.repo_root.resolve(), args.compitum_root.resolve())
    serialized = json.dumps(built, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not output.exists() or output.read_text(encoding="utf-8") != serialized:
            raise SystemExit("scene_data.json is stale; run build_scene_data.py")
        print("scene_data.json: PASS")
        return 0
    output.write_text(serialized, encoding="utf-8", newline="\n")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
