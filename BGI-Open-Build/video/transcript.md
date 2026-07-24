# Bellman Shadow Pricing — proof-film transcript

The film is silent. This transcript contains every displayed sentence, central equation,
meaningful motion, and provenance reference.

## 00:00–00:07 — The missing mechanism

Displayed:

- “BELLMAN SHADOW PRICING”
- “The missing action-pricing mechanism.”
- “FEASIBILITY-FIRST ROUTER”
- “shadow-price signal”
- “diagnostic only”
- “not trusted for selection”
- “Compitum had prices.”
- “It did not let them choose.”

Motion: the report-only shadow-price signal appears beside the feasibility-first router and
is crossed out as a selection input. This does not claim the diagnostic was deleted; it
states precisely that it was absent from the operative route-selection objective.

Provenance: `compitum-fabricpc/docs/Control-of-Error.md`,
`docs/adr/0001-fabricpc-trajectory-observer.md`,
`docs/adr/0002-constraint-pressure-oracle.md`, and `src/compitum/router.py`.

## 00:07–00:15 — FabricPC enters

Displayed:

- “THE INTERVENTION”
- “Can hidden scarcity become a routing price?”
- “FabricPC”
- “history → hidden scarcity belief → routing price → action”
- “The predictor was not the whole problem.”

Motion: the proposed chain assembles from history to action. The final price-to-action
arrow visibly fractures.

Provenance: `SUBMISSION.md`; `NARRATIVE_SOURCE.md`; `CLAIMS.md`; ADRs 0001–0007.

## 00:15–00:28 — The discovered bottleneck

Displayed:

- “THE DEFECT”
- “The price-to-action interface was wrong.”
- `λ(B)`
- `c(a)`
- `λ(B) · c(a) ≠ V(B) − V(B − c(a))`
- “Better belief cannot repair λ × lumpy consumption.”

Motion: a short local tangent appears at the current budget. A lumpy action crosses
several discrete value regions. The scalar approximation is contrasted with the actual
continuation-value loss.

Provenance: `SUBMISSION.md`, sections 1–2; `NARRATIVE_SOURCE.md`, “Why scalar prices
fail”; `CLAIMS.md`, “Negative findings.”

## 00:28–00:42 — Exact reconstruction

Displayed equation:

```text
C_t(a)
=
V_{t+1}(B_t, q_{t+1})
-
V_{t+1}(B_t - c_t(a), q_{t+1})
```

Displayed:

- “THE CORRECTION”
- “Charge the continuation-value loss.”
- “value before action”
- “value after action”
- `Σ_{j=1}^{k} λ_unit[j]`
- `V(B,q) − V(B − kδ,q)`
- “Shadow pricing returns — no longer as a local tangent.”

Motion: two value lookups appear and are joined by their exact difference. Discrete unit
charges telescope into the same two-value difference.

Provenance: `SUBMISSION.md`, section 1; `NARRATIVE_SOURCE.md`, “Discrete shadow-charge
construction”; `CLAIMS.md`, “Proved or exact”; continuation-value and discrete-charge
certificates in `evidence/notebooks/`.

## 00:42–00:54 — Exact Bellman equivalence

Displayed:

- “EXACT EQUIVALENCE”
- “Two rankings. One selected action.”
- “Immediate utility − action charge”
- “Bellman Q”
- “action A”, “action B”, “action C”
- “choices identical”
- “cumulative utility identical”
- “mismatches = 0”

Motion: parallel rankings select action B. Their green selection arrows merge.

Provenance: `SUBMISSION.md`, section 1; `CLAIMS.md`, “Proved or exact”;
`evidence/notebooks/03_online_optimal_equivalence.ipynb` and its green certificate.

## 00:54–00:66 — Certified belief-sensitive state

Displayed:

- “CERTIFIED STATE”
- “Belief changes the optimal action.”
- “remaining steps = 1”
- “budget = 4.5”
- “opportunity observed”
- “q = 0.05” / “SPEND”
- “q = 0.20” / “OPPORTUNITY”
- “Belief crosses a genuine action boundary.”
- “Exact transition point not asserted.”

Motion: the low-belief state appears first. An unlabeled dashed band connects it to the
high-belief state, where the certified action changes.

Provenance: `evidence/local_sources/04_belief_sensitive_boundary.py`, its notebook, and
its green certificate. No exact transition threshold is asserted.

## 00:66–00:77 — Tranche 7 split verdict

Left column, displayed:

- “MODEL VERDICT”
- “Fixed FabricPC topology”
- “did not clear the gate.”
- “PCN = backprop = 0.314”
- “15.4% recovered”

Right column, displayed:

- “PROGRAM VERDICT”
- “FabricPC exposed the missing mechanism.”
- “Exact Bellman charge”
- “recovered the full gap.”

Footer: “The predictor failed its gate. The intervention recovered the right economics.”

Motion: the red model verdict resolves separately from the green program verdict. They
remain two distinct results, not one blended pass/fail score.

Provenance: `SUBMISSION.md`, sections 2–3; `CLAIMS.md`, “Empirically supported,”
“Negative findings,” and “Limitations.” Predictive coding did not beat same-topology
backprop, and FabricPC did not directly produce zero regret.

## 00:77–00:85 — Closing

Displayed:

- “THE FABRICPC PREDICTOR DID NOT CLEAR THE GATE.”
- “THE FABRICPC INTERVENTION RECOVERED THE RIGHT ECONOMICS.”
- “The model lost. The experiment succeeded.”
- “Compitum × FabricPC”
- “Bellman Shadow Pricing”
- “certified executable evidence”

Motion: the negative model result appears first and remains visible. The meta-level
program result resolves beneath it, followed by four green certificate marks.

## Accessibility description

A dark, high-contrast silent animation begins with Compitum’s report-only shadow-price
diagnostic disconnected from its feasibility-first selector. FabricPC enters as an
experiment intended to turn predicted scarcity into a routing price, but the final
price-to-action arrow fractures. A gold piecewise value curve and red lumpy-action arrow
show why better belief cannot repair a scalar tangent multiplied by discrete consumption.
The film reconstructs the exact two-lookup Bellman action charge, shows zero-mismatch
online equivalence, and presents two certified belief states without inventing a
threshold. It closes with two simultaneous truths: the bounded FabricPC predictor missed
its gate, while the FabricPC intervention successfully recovered the right economic
mechanism.