# B05 — Independent Method Science Reference and quantitative acceptance plan (2026-11-22)

**Status:** All 41 Method ID / DGP / NEG / REF / AC / Gate provenance has been extracted from the formal 10_32 table and machine-checked for nonempty ID lists. Independent numeric or graph references, fixtures and quantitative acceptance are **NOT YET FROZEN**. No coding or scientific Gate tests have been executed.

The machine-readable companion `independent_science_acceptance_registry_draft1.json` contains one record per Method (P1 20 / P2 8 / P3 13); each record preserves the original target and source mapping with explicit **null** fields for missing acceptance choices. A list of REF IDs is a planned target, **not** an independent reference implementation or scientific evidence.

## Preregistered T1/T2/T3 protocol to finalize BEFORE Coding Authorization

**T1 — deterministic contracts:** Schema, Version, Method/Estimand/Backend capability, availability/negative states, content hashes, actual output structure and source lineage; all must pass strict tests. T1 cannot substitute for numerical/Graph truth.

**T2 — pilot:** Fix independent DGP, latent structure/graph truth or analytic estimand, Method-only/adversarial NEG, estimator settings, effective Backend/API, random seed and reference implementation with source + fixture hashes. Estimate pilot runtime and variance; use pilot ONLY to determine a prospectively registered R, K, tolerance and budget. No T2 outcome is scored as a confirmatory PASS.

**T3 — confirmatory:** Freeze a distinct seed/fixture/evidence set; predeclare a family of `K` scientific hypotheses/comparisons, multiplicity unit, test statistic, one-/two-sided decision, rejection criterion and compute budget. Adopt **FWER ≤ 0.05** (as previously approved), with a mathematically justified familywise procedure such as Holm where applicable; do not mistake 95% confidence level for global multiplicity correction. Use `R` independent replicates, track Monte Carlo error and coverage for CI-producing Methods; method-specific nonparametric intervals/weak-IV AR confidence-set shapes and temporal/graph identity tests get tailored metrics. Point-only SCM must NOT be tested as if it delivered CI.

### Precision and coverage formula

For coverage indicator `I_r = 1{truth inside C_r}`, estimate `p_hat = (1/R)Σ I_r` and `MCSE(p_hat)=sqrt(p_hat(1-p_hat)/R)`. Conservative planning bound `MCSE≤1/(2√R)`; a desired precision `ε` implies `R≥ceil(1/(4ε²))`, ignoring additional finite-sample interval uncertainty. **ε is a scientific design decision; no value is invented here.** A preregistered coverage tolerance and test procedure must be specified; fail/inconclusive based on independently measured uncertainty and multiplicity, not convenient post-hoc thresholds.

For known-truth point bias, use `e_r=estimate_r-truth`, `mean_error=mean(e_r)`, `MCSE(mean_error)=sd(e_r)/sqrt(R)`; variance, RMSE and tolerance are Method/Estimand-specific. For graph discovery assess the correct PAG/CPDAG/time-lag *equivalence class*, not forced edge orientation. For IV-LATE do not relabel a conditional structural slope as LATE; weak-IV AR set must represent nonbounded/disconnected/all-real as appropriate. For NEG, check typed no-estimate/failure and absence of fake CI before numerical decision.

## Blockers to finish B05

1. For all 41 Methods, independently establish reference computation/source, analytic truth or graph oracle and frozen source/fixture SHA; backend output under test cannot serve as truth.
2. Explicit per-Method Method Config/Estimand/Design/eligibility and inference availability; effective optional distribution/API verification per B04.
3. Set K/R/ε/tolerances/seed/compute and familywise decision, pre-register before T3; currently fields are null.
4. Validate negative scenarios scientifically, not only via syntactic Schema.
5. Source+fixture+reference+lock version identity and accepted upstream independent Gate999 evidence are needed to claim any PASS.

The present machine-readable registry is **execution-specification scaffolding**, not a runnable numerical acceptance suite. Freezing arbitrary thresholds or fabricating DGP outputs to remove Blockers is prohibited.
