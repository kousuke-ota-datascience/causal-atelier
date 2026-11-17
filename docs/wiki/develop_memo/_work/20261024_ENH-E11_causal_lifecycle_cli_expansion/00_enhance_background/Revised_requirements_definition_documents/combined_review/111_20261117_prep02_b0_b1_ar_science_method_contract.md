# PREP-02 F07 — B0/B1 just-identified robust Anderson–Rubin scientific computation contract

- Date: 2026-11-17 JST
- Kind: FLOW / science-method design determination **for independent reviewer**, not a runtime scientific PASS
- Authority: SR-03 S2/I2/G2, 41-Method mapping [10_32](../10_requirements_definition/10_32_scientific_method_scope.md), [30_63](../30_detailed_design/30_63_e11_method_adapters.md), [DEC-PREP02-D](decisions/95_20261117_dec_prep02_four_owner_choices.md)
- Methods: `P3-M10` B0, `P3-M11` B1; `P3-M09` Wald ratio is a separate Method and is **not automatically guaranteed** an AR confidence set
- Status: `SCIENTIFIC_FORMULAS_PROPOSED / ASSUMPTIONS_FIXED_TO_OWNER_SCOPE / NUMERIC_ORACLE_NOT_RUN / SCIENCE_ACCEPTANCE_NOT_PASSED`

## 1. Estimand and scope (normative adopted bounds)

| Variant | Endogenous `A`, excluded instrument `Z` | Exogenous design `Q` | Scientific target |
|---|---|---|---|
| B0 / P3-M10 | binary A and Z; 1 instrument, 1 endogenous regressor | intercept only, **no controls** | complier LATE **only under** instrument independence, exclusion, relevance and monotonicity assumptions; Wald and 2SLS point estimate coincide for identical sample/weight convention |
| B1 / P3-M11 | one binary A and binary Z; 1 excluded instrument | full-rank [intercept, **predeclared pre-treatment** C] | `LINEAR_IV_STRUCTURAL_COEFFICIENT`, **not** automatically complier LATE/ATE/CATE; correct additive linear structural and IV conditional exogeneity assumptions |
| Outside support | multiple excluded instruments/endogenous treatments, arbitrary panel/cluster/HAC, arbitrary continuously valued A, conditional IV effect heterogeneity | not covered | `METHOD_COMBINATION_UNSUPPORTED`; no invented CI or semantic target conversion |

Scientific assumptions are **declared and scrutinized**, not proven from an observed First-stage F statistic or backend convergence. Weak-IV robust AR inference does not repair invalid exclusion/independence/monotonicity.

## 2. Precise robust AR statistic: proposed deterministic reference

For n independent rows, column `Y` outcome, `A` endogenous binary treatment, `Z` excluded binary instrument, and full-column-rank exogenous matrix Q: `X=[Q,Z]`. For each candidate real β under `H0: β=β0`:

1. Set `r_β = Y − β A`, fit OLS `r_β = Qγ_β + Zπ_β + u_β` and test **single** exclusion `H0: π_β=0`. No endogenous 2SLS residual is used for this null test.
2. Use heteroskedasticity-robust OLS HC1 covariance for `π_β` and asymptotic `χ²(1)` critical value `χ²_(1,1−α)`; define `T_AR(β) = π̂_β² / Var_HC1(π̂_β)`. This is a **specified implementation candidate**, not a proof of finite-sample exactness.
3. `C_AR = {β∈R : T_AR(β) ≤ χ²_(1,1−α)}`, including equality at finite boundaries where variance is well-defined. Confidence level is `1−α∈(0,1)`; retain exactly what is inverted.
4. To support lossless unbounded/disconnected/ALL_REAL topologies, **do not** infer the set from a finite β grid. Use algebraic quadratic inversion, with certified numeric error bounds/root and boundary checks or an independently verified full-real-domain solver.

For reproducible algebraic inversion let `M_Q=I−Q(Q'Q)^{-1}Q'`, `z_tilde = M_Q Z`, `gY=z_tilde'Y`, `gA=z_tilde'A`. Let `M_X=I−X(X'X)^{-1}X'`, `eY=M_X Y`, `eA=M_X A`; and `k=rank(X)`, `h=n/(n−k)` (HC1 factor, n>k). Then

`s0=Σ_i z_tilde_i² eY_i²`, `s1=Σ_i z_tilde_i² eY_i eA_i`, `s2=Σ_i z_tilde_i² eA_i²`;

`q(β)=(gY−β gA)²−c·h·(s0−2βs1+β²s2)`, where `c=χ²_(1,1−α)`.

The candidate confidence set is the **valid test domain** `h(s0−2βs1+β²s2)>0` intersected with `q(β)≤0`. Expanded coefficients are `q2=gA²−c·h·s2`, `q1=−2gYgA+2c·h·s1`, `q0=gY²−c·h·s0`. Candidate solver must handle positive/negative/near-zero q2, double roots, q≡0, one-point sets, open singular exclusions, and extreme-tail behavior. Every computed boundary must be independently checked using the original `T_AR` or stable score-equivalent, not only polynomial rounding.

**Rank/definition rules:** If Z lacks both groups, `X` is rank deficient, `n≤k`, or HC1 variance is nonpositive/undefined at relevant β, **do not silently use a χ² approximation or supply a fake interval**. Emit typed `AR_TEST_NOT_DEFINED` / `AR_VARIANCE_DEGENERATE` and diagnostic evidence, with actual `InferenceAvailability` determined by how much of the set is mathematically verifiable. The full-set result cannot be claimed if undefined points are hidden. Numerical tolerance/precision strategy and fallback are to be frozen with an independent oracle, not guessed.

## 3. EMPTY and weak First-stage: conditional scientific invariant

- If `gA≠0`, finite β̂=`gY/gA` satisfies `g(β̂)=0`; **if** HC1 variance is finite and strictly positive at β̂, `T_AR(β̂)=0`. Thus **the just-identified AR confidence set is nonempty** under these stated sample-level regularity conditions. This is an algebraic implication, not a universal assertion covering zero first stage or singular variance.
- If `gA=0`, the point 2SLS/Wald ratio is undefined, but AR testing/inversion **may still be computable**; do not derive its availability from the point estimate. At the degenerate boundary, no unconditional nonempty guarantee is asserted; independently determine if there is a valid confidence set, and classify algorithm/test/domain failures separately.
- Generic AR wire `EMPTY + components=[] + inversion_evidence` is valid per Owner DEC-PREP02-D. In **B0/B1** where nondegenerate `gA≠0` and positive variance guarantee a nonempty set, computed EMPTY is a **Method-specific SCIENCE_INCONSISTENT** diagnostic, not a normal B0/B1 release. Do not relabel a mathematically computed EMPTY as a numeric `FAILED` without evidence of failure; preserve forensic evidence, `science_acceptance=BLOCKED/INCONCLUSIVE`, and no confirmatory PASS.
- An EMPTY produced from a finite search range is **not** a mathematical EMPTY. Solver must prove the entire real axis or declare `AR_INVERSION_INDETERMINATE`.

## 4. Typed outcome / numeric evidence contract

| Evidence field | Exact scientific meaning | Availability rule |
|---|---|---|
| `method_id`, `estimand_kind` | P3-M10 LATE_COMPLIER or P3-M11 LINEAR_IV_STRUCTURAL_COEFFICIENT; no alias | Required |
| `q_rank`, `x_rank`, `n`, `z_support`, `first_stage_gA` | eligible design and algebraic moment; distinguish zero/weak/strong | Required from verified data |
| `ar_null_test` | `OLS_Z_COEFF_HC1_CHI2_1`, alpha, chi-square critical, exact numerator/variance convention | Required when inference evaluated |
| `coefficient_q2/q1/q0`, `root_solver`, `tail_check`, `singular_points` | full-real-domain inversion provenance and topology evidence | Required for AVAILABLE set |
| `ar_set` | typed components and EMPTY/other topology with open/closed endpoints | Required only if valid and proven |
| `science_acceptance`, `inference.availability`, `point.availability` | independent dimensions | Always explicitly represented |
| `inversion_evidence` | bounded-size redacted diagnostic ContentRef, hash, backend/version/seed/ref | Required for AVAILABLE AR; no raw row values in published summary |

No arbitrary numeric epsilon, F>10 cutoff, bootstrap repetitions or coverage acceptance threshold is **invented** in this contract. These must be preregistered in Method G08 06/07 and checked against independent references.

## 5. Independent oracle / negative matrix (design contract, NOT_RUN)

| ID | Test target | Expected |
|---|---|---|
| AR-B0-01 | binary Z/A valid IV, nonzero First stage | B0 Wald point = 2SLS; correct LATE labeling; AR candidate root passes T_AR |
| AR-B1-02 | valid additive pre-treatment C + full-rank X | B1 structural β recovers known target; **not** mislabeled LATE |
| AR-WEAK-03 | weak/local-to-zero First stage | AR can be unbounded/disconnected/ALL_REAL; no finite Wald interval default |
| AR-ZERO-04 | exactly zero sample first stage | ratio point unavailable, AR availability separately determined; do not force EMPTY or CI |
| AR-REG-05 | Z constant, collinear Q/Z, n≤k, HC variance zero/undefined | typed method test non-identification or numerical failure; never false PASS |
| AR-MATH-06 | quadratic sign, double roots, equality, +/-∞ tails, disconnected ray boundaries | independent exact/numerical reference proves topology and all-real-domain coverage |
| AR-EMPTY-07 | generic valid overidentified inversion EMPTY and B0/B1 nondegenerate impossible EMPTY | Generic preserves valid EMPTY; B0/B1 rejects contradiction with diagnostics |
| AR-IV-08 | exclusion, monotonicity, independence violated | AR computational success is **not** causal identification/Science PASS |
| AR-STAT-09 | independent heteroskedastic DGP/n/seed/α reference | Preregistered type-I/coverage and Monte Carlo uncertainty, independent reviewer Gate07 |
| AR-LEGACY-10 | old v2/Wald and Product interfaces | no changed semantics; scientific statuses uncollapsed |

## 6. Review / Freeze boundary

- Scientific target, one-instrument/one-endogenous independent-observations and robust AR **approach** are Owner adopted. The **specific HC1 regression/null-test/χ² realization and quadratic solver are this design proposal** pending independent statistical reviewer validation and numeric oracle. This document itself does not authorize a new statistical estimator.
- Primary references: [Davidson & MacKinnon (2014), AR inversion](https://doi.org/10.1111/ectj.12015), [RFC 8785 separate codec authority](https://www.rfc-editor.org/rfc/rfc8785.html) (not a scientific source).
- **No numeric experiment, backend API probe, Monte Carlo, Science Gate PASS, independent Reviewer PASS or code implementation executed.**
