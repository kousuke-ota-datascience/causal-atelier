# 228 — ENH-E11 G01/P04/Trial01 FCI CI-test eligibility ambiguity — Owner scientific decision docket

**Date:** 2026-11-23 JST  
**Status:** `OWNER_SCIENTIFIC_DECISION_PENDING / AUTHOR_EVIDENCE_AND_OPTIONS_ONLY`  
**Decision ID:** `DEC-G01-P04-CI-ELIG-01`  
**Classification:** `CONTRACT_DEFECT / SCIENTIFIC_ELIGIBILITY_POLICY_UNDEFINED`  
**Branch / Agent START_SHA:** `feature/ariadne_mvp_e11` / `748deb4ba6287bbd1b71e233504c36c6f430e5b7`  
**Existing G01 S10 frozen SHA:** `52e5c60176d6b72c91f839ef267f46657bd380b5`  
**Protected completed dependencies:** P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167`; P03 `858c9f73366036a2d1445e558135cd521f611462`  
**P04 checkpoint:** none. **Agent Trial01:** `BLOCKED_CONTRACT_AMBIGUITY`; no P04 files changed or tests executed by Agent after stop.

> This is a non-normative Owner decision docket. No scientific threshold, acceptance semantics, G01 06/07, higher-level design, formal 09, S10 or S11 is changed or approved by this file. Values in the options below are proposals, not current requirements.

## 1. Verified contract gap and source-of-authority trace

- Requirements: `10_requirements_definition/10_13_fr_causal.md` (FR-044 and discovery), `10_32_scientific_method_scope.md` (`P1-M06`), `10_91_acceptance_conditions.md` (method-specific independent science) require method-specific eligibility; they **do not** define the three CI tests' sufficient numeric support/conditioning coverage.
- Logical data: `21_logical_data_design/21_41_scientific_data_constraints.md` defines scientific eligibility/result classifications but not conditional contingency-table thresholds.
- Basic design: `22_product_basic_design/22_06_family_causal.md` preserves PAG ambiguity, method-specific eligibility, distinction between scientific and technical outcomes.
- Interface: `23_api_interface_design/23_41_cli_scientific_ports.md` defines typed validated request, `--check-only` static preflight, selected Method and capability; no CI threshold is specified. Public wire/exit family must not be changed merely to fix this.
- Detailed design: `30_detailed_design/30_63_causal_method_adapters.md` §1.3/4.4 requires P1-M06 sample size, categorical support and CI mode checks but lacks a predicate and the set of conditioning sets. `30_61` and `30_62` preserve Discovery/Capability boundaries.
- Assigned Coding Instruction: `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` §6.4 requires FCI **before-call** rejection of inadequate n/support, without a reproducible decision rule.
- Independent Test Instruction: `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-08 explicitly states that sample/support thresholds and applicability are to be fixed by **Owner-adopted scientific contract and independent Reference** and that unapproved numeric thresholds must not be invented.

**Defect owner:** Method-specific scientific eligibility policy in detailed design, flowed to P04 Coding and independent Test. Not a P01/P03 serialization bug; not evidence that the Backend defaults are the scientifically approved acceptance policy.

## 2. Evidence: pinned causal-learn 0.1.4.8 (static source, not executed runtime science)

Primary source: [pinned CIT implementation](https://github.com/py-why/causal-learn/blob/0.1.4.8/causallearn/utils/cit.py) and [pinned FCI implementation](https://github.com/py-why/causal-learn/blob/0.1.4.8/causallearn/search/ConstraintBased/FCI.py).

- `FisherZ.__call__` in `cit.py` uses the inverse correlation submatrix for `(X,Y,S)` and `sqrt(n-|S|-3)`. A **necessary calculation-domain** rule is `n>|S|+3` plus defined/nonsingular involved correlation matrices. This does **not** prove multivariate Gaussianity, faithfulness or statistical power.
- `Chisq_or_Gsq` builds per-conditioning-stratum observed and expected cell counts; its `_CalculatePValue` may produce `p=1` where computed degrees of freedom are zero. Successful return (or `np.unique` recoding) is not proof of valid declared categories or asymptotically adequate expected counts.
- `FCI.py` `removeByPossibleDsep` calls `getPossibleDsep(...,-1)` and `DepthChoiceGenerator(len(possibleDsep),len(possibleDsep))`, and then tests subsets in that second-stage search. Therefore **the user-configured FAS `depth` cannot safely be treated as an upper bound on all FCI CI conditioning-set sizes**. A `depth=0` study is not automatically an unconditional-only FCI.
- Pinned 0.1.4.8 BK non-null fail-closed remains separately binding as documented in `combined_review/175_20261122_g01_fci_0148_tagged_source_bk_stdout_preflight.md`.
- Static source observation here is not proof of Python3.12 imported ABI, actual FCI fit, expected-count calibration, independent MAG/PAG oracle or G01_999 science.

## 3. Required Owner decision — competing scientific policies

**Option A — conservative exhaustive pre-FCI gate (recommended only for a deliberately bounded, small-p G01 profile).**

1. Before FCI invocation, inspect all unordered distinct observed variable pairs `(X,Y)` and **all** subsets `S ⊆ V\\{X,Y}` up to `|S|=p-2` (regardless of configured `depth`/`max_path_length`). These constitute a conservative **superset** of potentially reached CI calls; rejecting an input does not claim that FCI would necessarily test its offending triple.
2. For `fisherz`, require continuous, finite, nonconstant data; `n>|S|+3` for all such triples, plus a positive-definite, numerically well-conditioned `p×p` sample correlation matrix (an exact, independently specified numerical tolerance would still be required). Report Gaussianity, independent observations and faithfulness as **assumptions**, not verified sample truths. Nonconstant columns alone do not guarantee matrix invertibility.
3. For `chisq` and `gsq`, require finite, exact integer-coded observations consistent with declared categorical domains, no implicit Backend recoding as validation. For **each** `(X,Y,S)` and each declared `S=s` category combination, require observed stratum support, `X,Y` non-degenerate stratum marginals, positive test degrees of freedom and **minimum null-independence expected count ≥5 for every `X×Y` cell**. The value **5 is a proposed conservative heuristic**, not an established universal theorem or already approved Method threshold. Structural zero/absent category combination is rejected under this proposal. The same provisional criterion applies to `chisq` and `gsq` only if Owner explicitly adopts it.
4. Exhaustive checks are exponential in `p`; a workload/resource upper limit and deterministic response when exceeded must be agreed rather than silently truncating the subsets examined or treating an incomplete inspection as PASS. No new public Study field/version is implied.
5. This retains the **FCI-before-call** promise and all three CI families but may reject useful higher-dimensional or sparse valid problems. The policy is **sufficient-for-this-gate** and is not a necessary characterization of all statistically legitimate FCI inputs; actual science power and FWER remain separate.

**Option B — staged CI eligibility with checked actual CI calls (requires an explicit change of the previously approved pre-FCI rule).**

1. Perform strict schema, type, finite, category declaration and possible global mathematical checks **before** FCI. Require the same Owner-approved per-test quantitative criterion for actual `(X,Y,S)` each time the Backend requests a CI test; deny that CI call before p-value computation, abort the FCI run and publish no Graph/status/Marker on failure.
2. This avoids rejecting an input merely because an unvisited `S` is sparse, but changes the literal `06 §6.4` contract of **reject before FCI invocation** into `reject before affected CI evaluation`. The selected Backend API must first demonstrate a safe interception/guard mechanism without algorithm substitution, unapproved monkeypatch, silent fallback or partial publish. If that integration cannot be demonstrated, Option B remains BLOCKED; it is **not** an authorization to call FCI unguarded.
3. Independently choose and approve exact numerical rules, conditioning-stratum definition, tolerance and tests. Positive `fisherz/chisq/gsq` eligibility and scientific G01_999 are all retained; no scope reduction is implied.

**Option C — remove one or both discrete CI test modes from G01** is **not** a defect-only correction: it changes an already approved method scope and G01-07-08 positive acceptance. Do not adopt implicitly; separate scope decision and change-control needed if proposed.

**Recommendation:** Do not approve A or B as a purely editorial fix. Choose the intended *policy/coverage* at Owner level with scientific review of the numeric assumption; A is more faithful to the existing pre-FCI promise but its exponential and overly conservative consequences need an explicit small-p resource policy. B is more scalable in principle but requires new supported Backend integration and changes the preflight execution guarantee. In either option, independently preregister a fixed, reproducible positive/negative fixture matrix and scientifically justify the chosen count/tolerance thresholds.

## 4. Boundary fixtures the eventual formal contract must include

| Case | Required result once the policy is approved |
| --- | --- |
| Continuous `p=3, n=4`, with candidate `|S|=1` | Reject FisherZ: `n-|S|-3=0` even if marginal pair correlations exist |
| Continuous `p=3, n=5`, PD sample correlation | Meets only the stated FisherZ algebraic/numerical gate; not automatic Gaussian/FCI science PASS |
| Continuous full-rank columns but nearly singular correlation | Decide explicit numerical conditioning tolerance; don't silently accept a nonfinite/unstable inverse |
| Discrete two-category X/Y and S with ample **marginal** n but one S stratum count 4 | Under candidate A expected-count≥5, reject even if the unconditioned 2×2 table looks adequate |
| Discrete balanced and fully supported 2×2×2 with each joint category cell count 10 | Candidate A's `S=∅` and `S={Z}` expected-count checks should pass (assuming exact declared categories) |
| Undeclared/noninteger categorical values, category mismatch, constants | Reject before Backend as existing policy already requires |
| Absent conditioning-stratum category combination | Under candidate A fail closed; if alternative policy treats structural zeros differently, decide and test that expressly |
| `depth=0` but FCI Possible-D-Sep test conditions on ≥2 variables | Coverage test must not assume `depth` bounds all tested `S`; reject/guard sparse reachable CI |
| Preflight cannot finish due resource bound | Typed BLOCKED/eligibility unknown, never passed-as-eligible or Graph-positive |
| Non-null BK, even empty required/forbidden arrays | Existing `BACKEND_SEMANTICS_UNVERIFIED`/exit4 before FCI, unchanged |

Expected exit2/3/4 mapping must reuse the approved error families for config/input/backend; no new public CLI code or wire reason is created by this docket. A final amendment must explicitly assign typed phases for each newly defined failure.

## 5. Proposed minimal amendment scope after Owner decision

1. **Design authority:** `30_detailed_design/30_63_causal_method_adapters.md` §1.3/4.4: exact CI-specific eligibility predicate, sets to evaluate, numerical tolerances/expected-count definition, treatment of unreachable vs possible CI calls, bounded resources and assumption-vs-verified distinction. The higher RD/LDD/BD/IF must be checked for semantic consistency and changed **only if the chosen option alters the responsible layer**, not duplicated gratuitously.
2. **Coding instruction:** `10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md` §6.4, §6.6, §7: deterministic preflight order/typing, no fit before approved gate, no silent fallback, FCI selected runtime version, no leaked rows; keep Graph/BK/Provenance obligations unchanged.
3. **Independent tests:** `10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md` G01-07-08: identical approved predicate; boundary positive/negative and marginal-vs-conditional counterexample; actual Backend calls observed; test expected results **not** fitted to present implementation. Keep 07-09/10/999 independent science unchanged.
4. **Formal 09:** new `AMD-E11-G01-P04-001` only after adopting the policy and writing the exact five-layer impact; separate Owner 09 approval, new immutable G01-S10 full-SHA freeze, separate G01-S11 reauthorization are required for P04 Trial01 restart.

**Do not edit:** completed P01/P03 06/07, their source/tests/checkpoints, Product v2, `uv.lock`, strict public versions, P02 Reader or P05 code. P05's existing shared error routing and eventual integration tests must be traced, but a completed-Package change is not established by this blocker. The separate previously authorized P02 Reader compatibility exception remains strictly outside this docket.

## 6. Current disposition / next Owner action

- **Completed:** independently checked repo HEAD, source hierarchy, 06/07 ambiguity, and pinned upstream CIT/FCI control-flow; prepared a decision with counterexamples and exact amendment boundary.
- **Not performed:** normative 06/07/DD revisions, formal 09 approval, S10/S11, implementation, FCI fit, Python3.12 live test, external scientific reviewer or G01_999.
- **Owner action:** decide `DEC-G01-P04-CI-ELIG-01` (A or B, or amended policy) and approve a defensible quantitative support/tolerance rule, conditioning coverage and practical resource boundary. No premature Coding Agent restart.


## 7. Subsequent Owner decision and Author execution (2026-11-23 JST)

**Owner instruction:** 「A案：FCI呼出前に保守的な全候補集合を検査、こちらを採用する」.

**DEC-G01-P04-CI-ELIG-01 = A_ADOPTED.** Select exhaustive screening of every pair and conditioning subset **before any FCI invocation**, including the conservative G01 CI-specific screening predicates detailed in Option A. Reject the per-reached-test interception approach B. This does **not** grant formal G01 09 approval or an automatic S10/S11, and does not establish that the selected heuristic floor is statistically sufficient for all DGPs.

**Author-prepared normative reconciliation:**
- 30_detailed_design/30_63_causal_method_adapters.md §4.4
- 10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md §6.4
- 10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md G01-07-08
- New 09_ENH-E11_G01_AMD-E11-G01-P04-001_Gate_Contract_Amendment.md: formal 09 candidate only.

**Remaining undecided separate facts:** fixed computational cap, any positive-admission numerical-stability tolerance and real Backend/independent statistical calibration evidence. No automatic numeric cap, SCI PASS or optional engine semantics was inferred. The conservative fail-closed rule applies whenever exhaustive or reliable checking cannot be completed.

**Release:** Pending separate formal AMD-001 approval, revised G01 S10 on final immutable SHA, and separate S11 authorization. No P04 code/tests were changed.
