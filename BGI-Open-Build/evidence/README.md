# Evidence upload contract

## Deposit status

The finalized Bellman shadow-pricing evidence was deposited on 2026-07-24.

- Notebook Compiler base revision: `a6fcc3fd26348545b63e47ba77aba58f0d652066`
  (`feat/show-certificate`, with the accepted local evidence patches recorded by the
  uploaded source and artifact hashes)
- Compitum submission branch: `submission/bellman-shadow-pricing`
- Compitum submission commit: `d4c0bbd103849b8afb1019921684a062482d08cc`
- Research tag: `fabricpc-compitum-shadow-pricing-v1`
- Research commit: `617f8979daa921d326301266e55740c0746ab95c`
- FabricPC commit: `32ae295182ab944b8f084abaf4a40da2c50bab5f`
- Deterministic transfer bundle SHA-256:
  `6b48262f49e6cad498a23ff6e075f1f8522e831004f8cb3dbaeecfe46e28dc05`
- Validation command:
  `python BGI-Open-Build/evidence/validate_evidence.py`

The generated audits retain the explicitly declared `C:\src\...` compilation roots as
machine provenance. No username, credential, token, API key, or private configuration is
present, and the public site does not depend on those local paths.

This directory is the public evidence surface for the finalized local Notebook Compiler bundle.

## Required index

Create `evidence-index.json` with schema:

```json
{
  "schema": "bgi-open-build.evidence-index.v1",
  "bundle_sha256": "<sha256 of finalized zip>",
  "items": [
    {
      "id": "continuation-value",
      "title": "Continuation value",
      "kind": "Notebook Compiler certificate",
      "policy_ok": true,
      "source_ran": true,
      "notebook_ran": true,
      "validation_passed": true,
      "source_sha256": "...",
      "notebook_sha256": "...",
      "links": {
        "notebook": "notebooks/01_continuation_value.ipynb",
        "certificate": "notebooks/01_continuation_value.ipynb.certificate.json",
        "audit": "notebooks/01_continuation_value.ipynb.audit.json",
        "manifest": "notebooks/01_continuation_value.ipynb.manifest.json",
        "source": "local_sources/01_continuation_value.py"
      }
    }
  ]
}
```

## Required primary artifacts

1. Continuation value.
2. Discrete shadow-charge telescoping identity.
3. Online-optimal equivalence.
4. Belief-sensitive action boundary.

Also upload:

- `system_manifest.json`
- `system_report.md`
- `EVIDENCE_INDEX.md`
- the four adapter sources
- the four notebooks
- their certificates, audits, and manifests

Diagnostic failed package-module compilations may be retained under `diagnostics/`, but they must not be listed as primary green evidence.

## Rules

- Preserve generated files byte-for-byte.
- Do not expose absolute local filesystem paths in the public index.
- Verify every declared hash before commit.
- Keep narrative claims separate from machine certificate fields.
