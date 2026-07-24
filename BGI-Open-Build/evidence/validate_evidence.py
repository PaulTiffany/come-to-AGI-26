"""Validate the deposited BGI Open Build evidence surface."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ADAPTERS = (
    "01_continuation_value",
    "02_discrete_shadow_charge",
    "03_online_optimal_equivalence",
    "04_belief_sensitive_boundary",
)
GREEN_FIELDS = ("policy_ok", "source_ran", "notebook_ran", "validation_passed")
EXPECTED_EDGE_TARGETS = {
    "compitum.regret_lab.belief_bellman",
    "compitum.regret_lab.belief_pricing",
    "compitum.regret_lab.belief_regime",
    "compitum.regret_lab.environment",
    "compitum.regret_lab.metrics",
    "compitum.regret_lab.pricing",
    "compitum.regret_lab.simulator",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> object:
    return json.loads(path.read_bytes())


def validate(root: Path, source_evidence: Path | None, source_adapters: Path | None) -> None:
    json_paths = sorted(root.rglob("*.json"))
    for path in json_paths:
        load_json(path)
    for path in sorted(root.rglob("*.ipynb")):
        load_json(path)

    index = load_json(root / "evidence-index.json")
    assert isinstance(index, dict)
    assert index["schema"] == "bgi-open-build.evidence-index.v1"
    items = index["items"]
    assert isinstance(items, list) and len(items) == 4

    for adapter, item in zip(ADAPTERS, items, strict=True):
        assert isinstance(item, dict)
        certificate_path = root / "notebooks" / f"{adapter}.ipynb.certificate.json"
        notebook_path = root / "notebooks" / f"{adapter}.ipynb"
        source_path = root / "local_sources" / f"{adapter}.py"
        certificate = load_json(certificate_path)
        assert isinstance(certificate, dict)
        assert all(certificate[field] is True for field in GREEN_FIELDS)
        assert all(item[field] is True for field in GREEN_FIELDS)
        assert item["source_sha256"] == certificate["input_sha256"] == sha256(source_path)
        assert item["notebook_sha256"] == certificate["notebook_sha256"] == sha256(notebook_path)
        links = item["links"]
        assert isinstance(links, dict)
        for relative in links.values():
            resolved = (root / relative).resolve()
            assert resolved.is_relative_to(root.resolve()) and resolved.is_file()

    manifest = load_json(root / "system_manifest.json")
    assert isinstance(manifest, dict)
    assert manifest["python_files_total"] == 337
    assert manifest["encoding_error_files"] == []
    assert manifest["syntax_error_files"] == []
    edges = {
        (edge["importer"], edge["imported"])
        for edge in manifest["internal_import_edges"]
    }
    importer = "compitum.regret_lab.belief_action_pricing"
    assert EXPECTED_EDGE_TARGETS <= {target for source, target in edges if source == importer}

    primary_paths = json.dumps(items)
    assert "diagnostics/" not in primary_paths
    assert not list((root / "notebooks").glob("belief_*.ipynb"))

    sums_path = root / "SHA256SUMS"
    for line in sums_path.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        assert relative != "SHA256SUMS"
        assert sha256(root / relative) == expected

    if source_evidence is not None:
        for name in ("EVIDENCE_INDEX.md", "system_manifest.json", "system_report.md"):
            assert (root / name).read_bytes() == (source_evidence / name).read_bytes()
        for adapter in ADAPTERS:
            for suffix in (
                ".ipynb",
                ".ipynb.audit.json",
                ".ipynb.certificate.json",
                ".ipynb.manifest.json",
            ):
                target = root / "notebooks" / f"{adapter}{suffix}"
                source = source_evidence / "notebooks" / f"{adapter}{suffix}"
                assert target.read_bytes() == source.read_bytes()
        for source in sorted((source_evidence / "diagnostics").rglob("*")):
            if source.is_file():
                relative = source.relative_to(source_evidence)
                assert (root / relative).read_bytes() == source.read_bytes()

    if source_adapters is not None:
        for adapter in ADAPTERS:
            target = root / "local_sources" / f"{adapter}.py"
            source = source_adapters / f"{adapter}.py"
            assert target.read_bytes() == source.read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--source-evidence", type=Path)
    parser.add_argument("--source-adapters", type=Path)
    args = parser.parse_args()
    validate(args.root.resolve(), args.source_evidence, args.source_adapters)
    print("evidence validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
