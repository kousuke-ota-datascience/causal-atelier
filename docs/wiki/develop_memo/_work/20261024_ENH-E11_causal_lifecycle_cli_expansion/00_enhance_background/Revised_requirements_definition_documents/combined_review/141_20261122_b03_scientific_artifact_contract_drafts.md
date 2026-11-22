# B03 — Typed Scientific Artifact Contracts (2026-11-22)

STATUS: STRUCTURAL_DRAFT_AUTHORED; SEMANTIC_PROOF_BACKEND_AND_PRIVACY_NOT_YET_VERIFIED; NO SCIENCE PASS.

OUT-01 P2-M01..08: non-row CATE surface is a predeclared reference grid, NOT observed row vectors; distinguish NON_IV_CATE from CONDITIONAL_IV_STRUCTURAL_SLOPE. Without an approved grid return typed GRID_UNSPECIFIED; individual results only through separately authorized G05 Parquet. `result.json` scalar point must be NOT_AVAILABLE (NON_SCALAR_TARGET), not a fabricated ATE.

OUT-02 P3-M05: event-time/cohort vector with predeclared reference period, explicit temporal key, inference availability and pretrend evidence. No forced scalar effect.

OUT-03 P3-M12: SCM PRE/POST observed-minus-counterfactual time gaps, donor/pre-period/objective refs, point-only inference; assert gap arithmetic, donor eligibility and weights in semantic validator.

OUT-04 P1-M01..05: identification.json has explicit estimand, conditional state, assumption refs and Question/Design/Graph/Dataset lineage; M05 requires binary B0 LATE target/assumption rule and must not claim proven independence from a declared assumption. No result.json.

OUT-05 P1-M12..20: diagnostics.json has typed statistical roles, p-values/null distribution refs only when meaningful; non-significant negative control does NOT prove absence of confounding; no fake identification or Effect.

Each JSON document under internal_scientific/ is an INTERNAL draft version, not one of the five public E11 wire versions. Effective artifact required/forbidden map and cross-artifact source/method/estimand/ref hashes must be added to 23_42/Method Output profiles and independently tested. JSON Schema checks structural shape only; finite values, unique keys, CI availability, privacy of grids, temporal ordering, SCM arithmetic, proof status, null distribution and cross-asset integrity need additional semantic validation. The old scalar `e11-local-effect-result/1` is unchanged pending full backward-contract review.
