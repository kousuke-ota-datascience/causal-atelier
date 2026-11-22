# ENH-E11 S05 execution runbook for Owner's existing Linux VM (DEC-S05-03=A)

**This runbook is not evidence that any command has run.** Only execute in the approved internal Linux development VM with a read-only Git checkout and no changes to `src/`, `tests/`, `pyproject.toml`, `uv.lock`, Git refs or canonical docs. Owner permitted isolated review environments, but the current ChatGPT tool session cannot log in to that VM. Save reports, dependency freeze, version and source hashes outside the repo. This runbook assumes a shell with Git, `uv`, and outbound access to package indexes (or a trusted prepopulated wheel cache).

## A. Prerequisites and source pin

```bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
# A fresh independent operator must supply a previously pinned, immutable source SHA.
# Never set this to "$(git rev-parse HEAD)" merely to make the check pass.
: "${G01_REVIEW_TARGET_FULL_SHA:?Set the independently selected pinned 40-hex review SHA}"
if [[ ! "$G01_REVIEW_TARGET_FULL_SHA" =~ ^[a-f0-9]{40}$ ]]; then
  echo "BLOCKED: review target must be a 40-hex full SHA" >&2; exit 1
fi
ACTUAL_SHA="$(git rev-parse HEAD)"
if [[ "$ACTUAL_SHA" != "$G01_REVIEW_TARGET_FULL_SHA" ]]; then
  echo "BLOCKED: review target differs from checkout HEAD" >&2; exit 1
fi
if [[ -n "$(git status --porcelain=v1)" ]]; then
  echo "BLOCKED: review checkout dirty" >&2; exit 1
fi
git rev-parse HEAD
git hash-object uv.lock
sha256sum uv.lock
uv python list --only-installed
# Save immutable commit, lock hash, installed Python and package index provenance
# alongside each report outside the checkout; do not move the branch during execution.
```

If the checkout is dirty or source SHA differs from frozen review candidate, record BLOCKED. Never silently run on another Git state. The review target must be an **external independently selected full commit SHA** that existed before this checkout preflight; a clean checkout checked against itself is not an integrity check. Store its source provenance with `git hash-object uv.lock` and exact `sha256sum uv.lock`. This step is not a Git repository clone instruction.

## B. Schema B02 — **G01-only** Draft202012 validation entry

Owner `DEC-PREPCODE-01=B` sets **G01 common E11 wire + P1-M06** as the current S09/S10 scope. The following setup does **not** execute 200 non-FCI Profiles or any later Gate's science:

```bash
E11_DIR="$REPO_ROOT/docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/Revised_requirements_definition_documents"
OUT="$HOME/_work/e11_g01_review_$(git rev-parse --short=12 HEAD)"
mkdir -p "$OUT"
# Inherit the external immutable SHA verified in section A.
G01_REVIEW_SHA="$G01_REVIEW_TARGET_FULL_SHA"
```

**Only after a later owning Gate needs it:** `combined_review/tools/e11_profile_factor_compiler.py --report "$OUT/b02_200_schema_validator.json"` performs the **full 40×5=200** factorization check. It is **not invoked by the G01 commands below**, and its absence does **not** block G01 S10. The G01-specific validator is run in §B.1. The old `e11_g01_fci_method_config_v1.schema.json` is **historical non-dispatch** according to `schema_drafts/README.md`; its equality to active P1-M06 Config must **not** be a G01 readiness condition. A full source Profile SHA parity test does not replace G01-specific strict semantic joins, public Schema instances or independent MAG/PAG truth.

### B.1 G01-only standard validator and strict FCI profiles (read-only)

A review-only G01 executor exists at `combined_review/tools/e11_g01_schema_precode_probe.py`. It checks standard `Draft202012Validator.check_schema` for **six public E11 wire draft schemas and **three active P1-M06 FCI profile schemas****, independently enumerated **structural** positive/negative FCI Config/Question/Design instance fixtures, a **nonblocking diagnostic** comparison with the historical `e11_g01_fci_method_config` draft (which must never be selected by Method-ID dispatch), Local Graph Product IDs `null`, Study explicit row boolean, and Manifest/Status technical status enums. It is authored test preparation, **not** independent S09 reviewer output.

```bash
# Execute in the approved Python3.12 read-only checkout, not from this chat.
# Inherit the external immutable SHA verified in section A.
G01_REVIEW_SHA="$G01_REVIEW_TARGET_FULL_SHA"
uv venv --python 3.12 "$OUT/env-g01-schema"
uv pip install --python "$OUT/env-g01-schema/bin/python" 'jsonschema>=4,<5'
"$OUT/env-g01-schema/bin/python" \
  "$E11_DIR/combined_review/tools/e11_g01_schema_precode_probe.py" \
  --expected-head "$G01_REVIEW_SHA" \
  --report "$OUT/g01_b02_schema_author_diagnostic.json"
sha256sum "$OUT/g01_b02_schema_author_diagnostic.json" > "$OUT/g01_b02_schema_author_diagnostic.sha256"
```

A `PASS_AUTHOR_STRUCTURAL_PRECODE_DIAGNOSTIC` result is evidence only for the **tested structural cases**. It does **not** validate all six public wire Schemas with complete positive/negative instances or independently prove cross-file same-run identities, FCI eligibility, BK contradiction handling, effective Backend, independent MAG/PAG truth, JCS goldens, or actual Reader/FS. Those remain explicitly required and require separate independent review/evidence. `--expected-head` is the actual newly pinned checkout SHA, not the old manifest source snapshot commit.

## C. B04 — **G01 ENV-BASE only**, additional Backend profiles deferred to their owning Gates

The following **runs only ENV-BASE**, `causal-learn==0.1.4.8` and `statsmodels==0.14.6` as locked **candidates**. Do not change the project `uv.lock`; save full resolver/installed freeze, probes and hashes outside the checkout. A package name in lock or a tagged source file is **not** an observed installed API/fit or scientific correctness result.

```bash
uv venv --python 3.12 "$OUT/env-BASE"
uv pip install --python "$OUT/env-BASE/bin/python" 'causal-learn==0.1.4.8' 'statsmodels==0.14.6'
uv pip list --python "$OUT/env-BASE/bin/python" --format freeze > "$OUT/ENV-BASE.freeze"
"$OUT/env-BASE/bin/python" "$E11_DIR/combined_review/tools/e11_backend_probe.py" \
  --profile ENV-BASE --output "$OUT/ENV-BASE.api.json"
sha256sum "$OUT/ENV-BASE.freeze" "$OUT/ENV-BASE.api.json" > "$OUT/ENV-BASE.sha256"
```

If the resolver or API report fails, capture actual stderr and record `BLOCKED`. A successful `e11_backend_probe.py` is **API-only**, not fitted FCI/Graph-science evidence. Run the actual tiny-fit smoke in §C.1 and independent MAG/PAG reference review separately. Tagged `causal-learn 0.1.4.8` `FCI.py` includes a non-null BK bug and stdout leak as recorded in `175`; **do not** enable BK solely because Python import succeeds.

**Deferred envs (not run for G01):** `ENV-DOWHY (dowhy==0.14)`, `ENV-ECONML (econml==0.17.1)`, `ENV-TIGRAMITE (tigramite==5.2.10.1)`. The applicable owning Gates have separate S09/S10; they must execute their own isolated Python3.12 dependency/API/fit suites at that time. This is a **timing deferral, not a waiver** of later scientific acceptance. Do not merge environments or install all extra dependencies during G01 review.

### C.1 G01 P1-M06 fitted Backend API probe, and tagged BK hazard

For the **first Gate G01**, `combined_review/tools/e11_g01_fci_backend_precode_probe.py` is a separate **review-only, not application** Python3.12 tiny-fit and negative-CI probe. It demands exact `causal-learn==0.1.4.8`, effective `fci` signature including `node_names`, deterministic 3-node continuous Gaussian `fisherz` fit **and separate integer-coded binary categorical `chisq`/`gsq` tiny fits** (all BK=null), strict returned node/edge identities and no unexpected stdout/stderr, plus rejected invalid independence test. The categorical inputs are author-defined valid API probes; they do **not** establish Ariadne's preflight rejection of mixed/float/missing/sparse categories or the scientific validity of FCI orientation. It **does not** claim independent MAG/PAG truth or T2/T3 and **intentionally never calls FCI with non-null BK**; the tagged source has known hazard (`combined_review/175`).

```bash
# Run after section C creates ENV-BASE; use a clean pinned review checkout.
G01_REVIEW_SHA="$G01_REVIEW_TARGET_FULL_SHA"
# Syntax check only: do not generate __pycache__ in the read-only checkout.
"$OUT/env-BASE/bin/python" -B -c 'import ast, pathlib, sys; ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))' \
  "$E11_DIR/combined_review/tools/e11_g01_fci_backend_precode_probe.py"
"$OUT/env-BASE/bin/python" \
  "$E11_DIR/combined_review/tools/e11_g01_fci_backend_precode_probe.py" \
  --expected-head "$G01_REVIEW_SHA" \
  --report "$OUT/g01_b04_envbase_tinyfit_author_diagnostic.json"
sha256sum "$OUT/g01_b04_envbase_tinyfit_author_diagnostic.json" > "$OUT/g01_b04_envbase_tinyfit_author_diagnostic.sha256"
```

If `PASS_AUTHOR_FCI_TINY_FIT_DIAGNOSTIC` occurs, it proves only the listed **selected-package tiny synthetic API/shape/console smoke** on the executed Python3.12 environment and source SHA; an actual read-only independent science Reviewer still needs primary MAG/PAG oracle and scientific evidence. A non-pass must be preserved with exact logs and must **not** be relabeled as scientific-negative or G01 S10 readiness. The tagged `0.1.4.8` source (`FCI.py` Git blob `869b8de01ed495ce4738d3452e0217604dc31e9b`) calls `print` inside `fci_orient_bk` for non-null BK despite `verbose=false/show_progress=false`, and `add_directed_edge` for forbidden edges can over-orient PAG TAIL (open [#266](https://github.com/py-why/causal-learn/issues/266)). Non-null BK, including empty arrays, is therefore preflight-denied pending independent motif and stdout verification; **the Schema may allow its representation without granting execution capability**. Future G01_999 BK obligations remain, not waived.

## D. Independent Review Agent (G01 scoped and common baseline first)

**G01 Science Reference preparation:** `combined_review/176_20261122_g01_p1_m06_graph_a_independent_oracle_candidate_cases.md` provides **author-only analytic CI truth** for the adopted DGP-021 collider/mediator variants and a formal DGP-011 bivariate latent nonidentification counterexample. This is **not an independently accepted complete MAG/PAG equivalence oracle**: no fixture/source SHA, independent proof, numeric K/R/seed, BK remedy or T2/T3 execution is available. The separate Reviewer must derive the full admissible MAG/PAG equivalence targets and independently challenge all assertions, not accept the document as truth.


Start a **fresh** Codex/independent-science Review Agent session on the pinned checkout, using the applicable G01-scoped science and `combined_review/165` independent S09 instructions. `combined_review/158_20261122_s05_independent_science_reviewer_prompt.md` is the **full-41** research reviewer preparation reference, not an order to require G02–G09 40 unrelated Method scientific approvals before G01 S10. G01 science reviewer must examine P1-M06 FCI with independent MAG/PAG oracle and negative/refusal rules; the broader 41 review occurs incrementally by owner Gate and finally G10. The Reviewer must not be fed the author's verdict as trusted evidence, and must report actual independent computations, primaries, insufficiencies and **P1-M06-specific** outcomes for G01; remaining 40 Methods are `NOT_REVIEWED` and are covered at their owning Gates and G10. Do not run a coding implementation agent (S11 not authorized). If no authorized independent process can be launched, record `S05-B05-REVIEWER_NOT_LAUNCHED`.

## E. Evidence verdicts: before coding vs after authorization

**Authority:** Owner **DEC-PREPCODE-01=B is adopted**. Each Gate needs its own independent scoped S09 plus common/actual-upstream closure, followed by **separate Owner S10 Freeze** and **separate Owner S11 Coding Authorization**. G01 starts; G02+ need upstream Gate999. No Gate automatic permission follows from this runbook. This runbook **implements the already Owner-adopted gate-scoped procedure** but does not itself grant a G01 S09 PASS, S10 Freeze or S11 authorization, and exempts no Method from its eventual 07/999.

| ID | Pre-code contract readiness | Actual E11 candidate Gate07/999 |
| --- | --- | --- |
| B02 | For G01: standard Python3.12 `jsonschema` validation of its **three active P1-M06** FCI profile schemas plus **six public E11** v1 schemas and their shared dispatch/Graph invariants, with independent positive/negative fixtures. For G02–G09: standard original-vs-factored Method-specific parity for the actual owned profiles and their shared bundles; **200/200 evidence is a cross-Gate milestone, not a G01 blocker** | Actual runtime Schema Registry, Method/Study rejection and accepted method-specific CLI payload integration |
| B03 | Accept complete operation-specific Artifact/Manifest/Status/Reader **semantic contracts** and synthetic typed positive/negative fixture shapes; cross-file equality, path/ContentRef, non-scalar, no-row-denial rules must be independently reviewable. A real production E11 Reader **cannot be required to have passed** before it is implemented | Real Linux FD/root/atomic no-clobber/manifest/marker/Reader actual byte readback, privacy, CATE/Event/ITS/SCM and negative/corrupt bundle tests; until then B03 **runtime verification remains NOT_RUN**, not `PASS` |
| B04 | Isolated approved Python3.12 ENV-BASE dependency resolution and *small standalone* FCI API/fit/negative feasibility probes for G01; independently establish other optional Backends only when owning Gates are reviewed; do not substitute the existing optional dependency name for effective availability | Full E11 Method Adapter fit/result/inference integration, CI support, no fallback and final effective `uv.lock` provenance |
| B05 | Independently accepted Method-specific target/algorithm/assumptions, true DGP/negative/reference test design, scientific acceptance protocol, and real reference-source/fixture identity for the **approved Freeze scope**. An unapproved HC1/χ² weak-IV AR realization remains blocked for G08. A pre-code independent T2 pilot is useful where actually executable and necessary for algorithm choice, but don't fabricate one | Independent candidate T1/T2 (pilot) and T3 (confirmatory) execution for each required Method, with fixed independent-reference and preregistered K/R/seed/MC-SE/threshold/compute parameters **before T3**, full FWER and failed-case disclosure. Do not retroactively accept outputs as truth |
| B06/S09 | 71 Gate instructions, seven operator prompts, current 10/22/23/30/Schema, self-contained 06/Pxx/07, actual independent S09 design verdict on fixed SHA | Candidate-specific 07/999 and protected Product regression; Author document audit alone is not an independent verdict |

**References:** `combined_review/173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md` (Owner-adopted B) and `combined_review/172_20261122_prep04_s10_precode_evidence_phase_assignment.md`. The historical `combined_review/147` all-41 pre-global-Freeze language is superseded **only as to timing**: pre-code evidence is required before **each owning Gate**'s S10; final candidate T2/T3 evidence after S11 and independent 999; G10 still needs valid science evidence for all 41. G08/G09 unresolved Method-specific contracts do not block G01, though any common/shared effect still does. No waiver.

B02 formal runtime, B03 actual Reader integration, B04 real target environment and B05 independent numeric science have **not** been executed by this chat. An execution probe is not a PASS without the exact expected source/lock/fixture/environments, logs and signed-off independent acceptance.

No Contract Freeze/S11 Coding Authorization may be inferred from the Owner's A/A decisions.


### C.2 Supplementary categorical coverage and SHA authority (2026-11-22)

At execution time, pin a clean, externally selected full commit SHA and preserve the precise `categorical_ci_fits` reports (`chisq` and `gsq`) as well as the continuous result. Do not treat a single `fisherz` fit as complete P1-M06 three-CI feasibility. This is still author-only read-only evidence and cannot supersede independent G01 S09/B05. Review the current G01 subset against `s09_g01_scoped_review_inventory_draft7.json` (historical draft3 remains immutable).

**Preflight failure behavior:** Before any FCI import or fit, the review-only script checks Python exactly 3.12, full `--expected-head` equality and clean Git worktree. On mismatch it writes `BLOCKED_PRECONDITION_NO_BACKEND_EXECUTION` to the report and exits nonzero without invoking FCI. If the prerequisites pass but one CI fit raises, the failure is retained under that method, while the remaining `fisherz/chisq/gsq` diagnostics and invalid-CI negative may still be collected. The report still cannot certify cross-process stdout isolation, the application adapter, or independent MAG/PAG/BK scientific acceptance. An exception, nonzero exit or missing report must be treated as BLOCKED, never erased by successful modes.

### B.2 Schema validator provenance guard (2026-11-22)

The review-only `e11_g01_schema_precode_probe.py` now checks Python **exactly** 3.12, the externally specified full HEAD SHA and clean checkout **before invoking any Draft202012 schema validation**. A failed prerequisite yields `BLOCKED_PRECONDITION_NO_SCHEMA_VALIDATION` with an out-of-repository JSON report and nonzero exit, rather than running Schema fixtures on unapproved source. See supplemental blob `564a3dcbb9a20cdbcce1bdf95760a4f80336bd2a` in G01 scoped `draft7`. Actual B02 schema validation and independent fixtures are still `NOT_RUN`; the script is not an independent Reviewer.
