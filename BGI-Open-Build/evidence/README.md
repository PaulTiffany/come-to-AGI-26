# Evidence upload contract

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
