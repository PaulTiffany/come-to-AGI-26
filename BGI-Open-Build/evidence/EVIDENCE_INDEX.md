# Bellman Shadow-Pricing Evidence Index

This is a local submission evidence set. Nothing here modifies the frozen Compitum checkout or
publishes Notebook Compiler.

## Frozen source identity

- Compitum checkout: `C:\src\compitum-fabricpc`
- Submission branch: `submission/bellman-shadow-pricing`
- Submission commit: `d4c0bbd103849b8afb1019921684a062482d08cc`
- Research tag: `fabricpc-compitum-shadow-pricing-v1`
- Research commit: `617f8979daa921d326301266e55740c0746ab95c`
- Package exposure: editable install into Notebook Compiler's local virtual environment with
  `pip install --no-deps -e`; this is non-portable local evidence configuration.
- Per-run policy overlay: `--allow-import-prefix compitum`; the effective prefix is recorded in
  every audit and certificate. Default policy behavior is unchanged.

## Green executable notebooks

Every certificate below records `policy_ok=true`, `source_ran=true`, `notebook_ran=true`, and
`validation_passed=true`.

| Adapter and claim | Canonical modules imported | Adapter source SHA-256 | Certificate SHA-256 | Notebook SHA-256 |
| --- | --- | --- | --- | --- |
| [`01_continuation_value.py`](../../local_sources/bellman-shadow-pricing/01_continuation_value.py): continuation value and canonical marginal price | `belief_bellman`, `belief_regime` | `824ae6809aec9b1978f0a311d70b2eb078afec48618cf9b81ac1f044bb405442` | `54d43112256fb79c42547a6e5ed89e6185484ec60113946d64c48fa8816c8662` | `09e6fcf5bdbe239b040eaf09bf3aa54fa7f0ff6614f9f3ef68d2f31eb054f094` |
| [`02_discrete_shadow_charge.py`](../../local_sources/bellman-shadow-pricing/02_discrete_shadow_charge.py): telescoping unit-price identity equals the two-value-lookup action charge | `belief_action_pricing`, `belief_bellman`, `belief_regime` | `abee4e7b437ca67346ba5ad2a5d6427d78471f70a40c4b7ad67bf540d3551f05` | `193f9927273a32fad5dc5f5a9c052e0d42e39178a7ad88e685f7cdddc1fb3996` | `fdc090b857c6859606a92694bd466f9363a6d51ce9ec1a80bb56dc29a9892002` |
| [`03_online_optimal_equivalence.py`](../../local_sources/bellman-shadow-pricing/03_online_optimal_equivalence.py): identical route choices, cumulative utility, and zero mismatches | `belief_action_pricing`, `belief_bellman`, `belief_online_optimum`, `belief_pricing`, `belief_regime` | `75f7e8da581c7ffe124e9fcbfb5083dde800b1f6242e040b076ff667343c56f9` | `5b74dc67328bff7b74c4123348a7d0490ffe0b1ec75a2aaa08dad3825afbf7d3` | `54d462090252b9b700e5c7ded8b32aee0352bc0b65e0531e07f4eb51965bc288` |
| [`04_belief_sensitive_boundary.py`](../../local_sources/bellman-shadow-pricing/04_belief_sensitive_boundary.py): low and high beliefs cross a genuine Bellman-optimal action boundary | `belief_bellman_v2` | `6bd2ca914aa1d6f4f1ffdba9daf90099a3d0054c677bbf444b228a6ca5d7b370` | `c4f4a437184f2d3003bf75453ddd657ef48c22936cdf81b6fdf83a82a952dbcf` | `42ff134eb26317a2bbe1706c8148eff01689a80728c5b56720d75183225917a2` |

Each notebook's adjacent `.audit.json`, `.certificate.json`, and `.manifest.json` files are in
[`notebooks/`](notebooks/).

## Static canonical source evidence

- [`system_manifest.json`](system_manifest.json): corrected source inventory, hashes, and internal
  dependency graph.
- [`system_report.md`](system_report.md): human-readable projection of the system manifest.

Canonical module hashes used by the adapters:

| Canonical source | SHA-256 |
| --- | --- |
| `src/compitum/regret_lab/belief_action_pricing.py` | `c4446651f6a2362a58648f5c5f2dd0b8c348f855bc14a769aab916bb420f49c8` |
| `src/compitum/regret_lab/belief_bellman.py` | `3fd1492e0749207accf34fec42493ba31b3266877e46c95225683724f56404ee` |
| `src/compitum/regret_lab/belief_bellman_v2.py` | `0e99ae2dfd796b1d682853083843736807fff9bf306c15200845711518855a50` |
| `src/compitum/regret_lab/belief_online_optimum.py` | `dd170d31af156dcac690dbce394516d9cdf8b4ae8538fd86d500ac35ebaba468` |
| `src/compitum/regret_lab/belief_pricing.py` | `7e07330bc96526015e154355696842dde42bb46512c3857d94d084cb357121a1` |
| `src/compitum/regret_lab/belief_regime.py` | `dfb4a7c08f11350778c98bcf93538d5211351fe0dc6bfb1e1629669e5aa85fa3` |

## Diagnostic limitations

- Raw package modules cannot currently execute as standalone files because isolated execution has
  no package context. Their honest failed artifact sets are retained under
  [`diagnostics/package-module-execution/`](diagnostics/package-module-execution/).
- The original `submission_demo.py` default-policy refusal is retained under
  [`diagnostics/submission-demo-policy-refusal/`](diagnostics/submission-demo-policy-refusal/).
- Concept inference is heuristic. Labels such as “NumPy Array Basics” and “Working Python Example”
  are not authoritative descriptions of the Bellman mechanism. Sketched and the authored narrative
  provide conceptual explanation; Notebook Compiler provides deterministic source, execution,
  validation, and provenance records.
- The four adapters are local executable demonstrations that import the canonical frozen package.
  They do not copy or reimplement the Bellman mechanism.
