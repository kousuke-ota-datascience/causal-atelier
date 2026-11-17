# ENH-E11 G01 / 07 テスト・独立検証指示書（PREP-03初稿）

**Status:** `PREP03_G01_07_DRAFT / TEST_NOT_RUN / SCIENCE_ORACLE_PENDING`
**参照:** [G01 / 06](06_Ariadne_ENH-E11_G01_実装指示書.md) と [PREP-02 common design baseline](../../00_enhance_background/Revised_requirements_definition_documents/combined_review/117_20261117_prep02_common_contract_baseline_freeze.md)。**07は当該G01の独立検証契約**であり、「G07＝DiD Workstream」とは別。

## 1. Evidence / execution rules

- Pin 06 implementation code SHA, test fixture SHA and environment/lock SHA at G01 test execution. G01 06/07 must refer to *same* implementation revision; deviations get retried rather than phantom PASS.
- Report each test as `PASS/FAIL/BLOCKED` with exact command, exit, fixture, negative result and independent reviewer notes. This plan does **not** claim any test already ran.
- Pure value/Schema and filesystem/CLI/science results are separate; an import smoke is not an FCI Graph Science PASS. G01 block can be science-BLOCKED without misreporting a technical PASS.
- Confirm no changes to Product canonical requirements, Web/API/DB, or old v2 runtime behavior.

## 2. Gate test contract

| Test ID | Minimum oracle and negative | Pass condition |
|---|---|---|
| G01-07-01 | 5 required v1 identifiers+Marker, unknown versions, legacy v2 and YAML duplicate keys | E11 strict decode rejects unknown/duplicate; legacy Product CLI intact |
| G01-07-02 | ContentRef path traversal/symlink/real bytes SHA mismatch, Graph semantic hash projection mismatch | No TOCTOU path escape; full file hash and projection hash independently validated |
| G01-07-03 | GraphVersion parent identity/edit immutability, CPDAG/PAG endpoint/tag/lag serialization | Round-trip preserves circle/tail/arrow/bidirected and temporal semantics; no silent DAG flattening |
| G01-07-04 | JCS RFC8785 strict wire, 7 positive/7 negative golden vectors, cross-runtime bytes+SHA256 | Independent Python/ECMAScript codec produces **same bytes**, no default=str or Unicode normalization |
| G01-07-05 | Linux same-FS `renameat2(RENAME_NOREPLACE)` two-process collision (same/different hash), fail after every fsync or rename | Existing complete run never clobbered; indeterminate state never claims COMMITTED; no lock fallback |
| G01-07-06 | Commit Marker→Manifest→Artifact full readback with missing/corrupt marker, duplicate files, foreign UID, bad ACL, mount change | Validated complete committed run only; typed failure exit5 for persisted corruption |
| G01-07-07 | Operation `DISCOVER` has no dummy EffectResult, manifest result discriminator is null, status technical/Science separate | Valid bundle and negative scientific outcome serialized without false Effect/Science PASS |
| G01-07-08 | FCI P1-M06 CI compatibility / optional dependency unavailable; unaccepted configuration | Valid eligible configuration enters scientific adapter, invalid one gets typed reasons, no fallback |
| G01-07-09 | **Independent PAG Oracle** from multi-variable latent-variable Graph whose Markov equivalence-class implications are independently enumerated | Score adjacency and PAG endpoint categories against **identifiable equivalence-class truth**, not a single generating DAG |
| G01-07-10 | Two observed-node latent confounder motif from DGP-011; cannot prove latent from observed CI alone | No assertion of uniquely identified latent cause or invented causal direction |
| G01-07-11 | Scientific negative, unsupported CI, backend exception, forbidden row request, path/hash bad, technical failure | Proper typed status, exit0 only valid published negative; exit2/3/4/5 by phase; row files never staged |
| G01-07-12 | Product CLI / prior GraphVersion/Manifest v2 and active test regression | No changes to legacy response/state; no E11-only schema imported by Product |

## 3. G01-specific scientific evidence gate

- Before claiming G01 Science PASS, supply multiple **known equivalence-class** motifs (including multi-node latent structure), independent PAG oracle (exact endpoint oracle or a separately audited reference), CI test correctness at sample sizes and declared distribution assumptions; preserve graph uncertainty. Confirm no request to estimate point treatment effects from PAG ambiguity.
- Preregister K/R/seed/error tolerances and any multiple-testing policy for P1-M06; do not select thresholds after observing trial results. Compute budget and environment Profiles must be recorded.
- Scientifically unresolvable orientation is **not** automatically a software failure; fabricated orientation, unsupported CI test or lost endpoint is.
- Reference: [SR-04 acceptance matrix](../../working_notes/20261115_sr04_method_acceptance_matrix_draft.md) P1-M06 (DGP-011/DGP-021; NEG-003/021/028; REF-G02; AC-D02/G01/G02/G03/G04/G06).

## 4. Outcome

G01 `999` result is based on fixed source revision, actual test outputs and independent Graph Science evidence. This file is a **test specification draft**, not acceptance evidence. `G01_ENTRY_PENDING / G01_TESTS_NOT_RUN / E11_CODING_NOT_AUTHORIZED`.
