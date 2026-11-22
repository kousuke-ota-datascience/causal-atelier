# ENH-E11 S05 execution runbook for Owner's existing Linux VM (DEC-S05-03=A)

**This runbook is not evidence that any command has run.** Only execute in the approved internal Linux development VM with a read-only Git checkout and no changes to `src/`, `tests/`, `pyproject.toml`, `uv.lock`, Git refs or canonical docs. Owner permitted isolated review environments, but the current ChatGPT tool session cannot log in to that VM. Save reports, dependency freeze, version and source hashes outside the repo. This runbook assumes a shell with Git, `uv`, and outbound access to package indexes (or a trusted prepopulated wheel cache).

## A. Prerequisites and source pin

```bash
set -euo pipefail
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"
git status --porcelain=v1
git rev-parse HEAD
uv python list --only-installed
# Must explicitly record and freeze the SHA being assessed; no moving branch during execution.
```

If the checkout is dirty or source SHA differs from frozen review candidate, record BLOCKED. Never silently run on another Git state. This step is not a Git repository clone instruction.

## B. Schema B02 — G01 FCI-specific standard validation first; 200 factored later by owning Gate

```bash
E11_DIR="$REPO_ROOT/docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/Revised_requirements_definition_documents"
OUT="$HOME/_work/e11_s05_review_$(git rev-parse --short=12 HEAD)"
mkdir -p "$OUT"
uv venv --python 3.12 "$OUT/env-schema"
uv pip install --python "$OUT/env-schema/bin/python" 'jsonschema>=4,<5'
"$OUT/env-schema/bin/python" "$E11_DIR/combined_review/tools/e11_profile_factor_compiler.py" --report "$OUT/b02_200_schema_validator.json"
sha256sum "$OUT/b02_200_schema_validator.json" > "$OUT/b02_200_schema_validator.sha256"
```

The 200-profile compiler command below is an **optional cross-Gate diagnostic** until relevant G02–G09 ownership is reviewed; its report must say `PASS_SCHEMA_STRUCTURAL_AND_VALIDATOR_PARITY` to prove the full 200 parity, but **absence of that full report does not block G01** under Owner DEC-PREPCODE-01=B. For **G01 S10**, run standard Draft202012Validator.check_schema and independent positive/negative instance validation of the four specialized G01/P1-M06 Config/Question/Design draft Schema paths (discover exact paths from current Git), the six shared E11 v1 payload schemas, and Graph/FCI cross-wire semantic compatibility, with each schema's exact blob SHA. There is no factual claim that this G01-specific standard validation has run. A partial fake 200 PASS is prohibited.

## C. B04 — G01 ENV-BASE first; four separately resolved Backend environments by owning Gate

The following release candidates are **not** selected working versions until resolver+signature+fit results have been reviewed. Do not merge into one environment or change the project `uv.lock`.

```bash
for pair in 'BASE causal-learn==0.1.4.8 statsmodels==0.14.6' 'DOWHY dowhy==0.14' 'ECONML econml==0.17.1' 'TIGRAMITE tigramite==5.2.10.1'; do
  read -ra fields <<< "$pair"
  name="${fields[0]}"; packages=("${fields[@]:1}")
  uv venv --python 3.12 "$OUT/env-$name"
  uv pip install --python "$OUT/env-$name/bin/python" "${packages[@]}"
  uv pip list --python "$OUT/env-$name/bin/python" --format freeze > "$OUT/ENV-$name.freeze"
  "$OUT/env-$name/bin/python" "$E11_DIR/combined_review/tools/e11_backend_probe.py" --profile "ENV-$name" --output "$OUT/ENV-$name.api.json"
  sha256sum "$OUT/ENV-$name.freeze" "$OUT/ENV-$name.api.json" > "$OUT/ENV-$name.sha256"
done
```

**Owner DEC-PREPCODE-01=B:** G01 pre-code evidence requires only `ENV-BASE` actual Python3.12 resolver/signature and a small standalone `causal-learn` FCI fit + negative eligibility/API probe; **no DoWhy/EconML/Tigramite acceptance is a G01-specific prerequisite**. The loop remains available to collect later Gate evidence without changing `uv.lock`; do not run optional later-Backend probes under G01 and then treat them as supported. The separate environment check returns `API_PROBED_NOT_SCIENCE_VALIDATED` at best; **not** method-specific fit/inference. If installation/symbol verification fails, preserve exact failure output and isolate compatibility/ABI/uncertain license obligations. Then run approved Method-specific tiny valid/invalid fit + CI/graph output fixture suite; no fallback method or CATE/IV target relabeling. Independently inspect the exact **tagged** package metadata and solver resolution rather than treating PyPI landing page as successful installation.

## D. Independent Review Agent (G01 scoped and common baseline first)

Start a **fresh** Codex/independent-science Review Agent session on the pinned checkout, using the applicable G01-scoped science and `combined_review/165` independent S09 instructions. `combined_review/158_20261122_s05_independent_science_reviewer_prompt.md` is the **full-41** research reviewer preparation reference, not an order to require G02–G09 40 unrelated Method scientific approvals before G01 S10. G01 science reviewer must examine P1-M06 FCI with independent MAG/PAG oracle and negative/refusal rules; the broader 41 review occurs incrementally by owner Gate and finally G10. The Reviewer must not be fed the author's verdict as trusted evidence, and must report actual independent computations, primaries, insufficiencies and 41 per-Method outcomes. Do not run a coding implementation agent (S11 not authorized). If no authorized independent process can be launched, record `S05-B05-REVIEWER_NOT_LAUNCHED`.

## E. Evidence verdicts: before coding vs after authorization

**Authority:** Owner **DEC-PREPCODE-01=B is adopted**. Each Gate needs its own independent scoped S09 plus common/actual-upstream closure, followed by **separate Owner S10 Freeze** and **separate Owner S11 Coding Authorization**. G01 starts; G02+ need upstream Gate999. No Gate automatic permission follows from this runbook. This runbook does **not** approve gate-scoped Freeze or exempt any Method from its eventual 07/999.

| ID | Pre-code contract readiness | Actual E11 candidate Gate07/999 |
| --- | --- | --- |
| B02 | For G01: standard Python3.12 `jsonschema` validation of its four specialized FCI draft profile schemas plus six public E11 v1 schemas and their shared dispatch/Graph invariants, with independent positive/negative fixtures. For G02–G09: standard original-vs-factored Method-specific parity for the actual owned profiles and their shared bundles; **200/200 evidence is a cross-Gate milestone, not a G01 blocker** | Actual runtime Schema Registry, Method/Study rejection and accepted method-specific CLI payload integration |
| B03 | Accept complete operation-specific Artifact/Manifest/Status/Reader **semantic contracts** and synthetic typed positive/negative fixture shapes; cross-file equality, path/ContentRef, non-scalar, no-row-denial rules must be independently reviewable. A real production E11 Reader **cannot be required to have passed** before it is implemented | Real Linux FD/root/atomic no-clobber/manifest/marker/Reader actual byte readback, privacy, CATE/Event/ITS/SCM and negative/corrupt bundle tests; until then B03 **runtime verification remains NOT_RUN**, not `PASS` |
| B04 | Isolated approved Python3.12 ENV-BASE dependency resolution and *small standalone* FCI API/fit/negative feasibility probes for G01; independently establish other optional Backends only when owning Gates are reviewed; do not substitute the existing optional dependency name for effective availability | Full E11 Method Adapter fit/result/inference integration, CI support, no fallback and final effective `uv.lock` provenance |
| B05 | Independently accepted Method-specific target/algorithm/assumptions, true DGP/negative/reference test design, scientific acceptance protocol, and real reference-source/fixture identity for the **approved Freeze scope**. An unapproved HC1/χ² weak-IV AR realization remains blocked for G08. A pre-code independent T2 pilot is useful where actually executable and necessary for algorithm choice, but don't fabricate one | Independent candidate T1/T2 (pilot) and T3 (confirmatory) execution for each required Method, with fixed independent-reference and preregistered K/R/seed/MC-SE/threshold/compute parameters **before T3**, full FWER and failed-case disclosure. Do not retroactively accept outputs as truth |
| B06/S09 | 71 Gate instructions, seven operator prompts, current 10/22/23/30/Schema, self-contained 06/Pxx/07, actual independent S09 design verdict on fixed SHA | Candidate-specific 07/999 and protected Product regression; Author document audit alone is not an independent verdict |

**References:** `combined_review/173_20261122_dec_precode01_owner_gate_scoped_s09_s10_s11.md` (Owner-adopted B) and `combined_review/172_20261122_prep04_s10_precode_evidence_phase_assignment.md`. The historical `combined_review/147` all-41 pre-global-Freeze language is superseded **only as to timing**: pre-code evidence is required before **each owning Gate**'s S10; final candidate T2/T3 evidence after S11 and independent 999; G10 still needs valid science evidence for all 41. G08/G09 unresolved Method-specific contracts do not block G01, though any common/shared effect still does. No waiver.

B02 formal runtime, B03 actual Reader integration, B04 real target environment and B05 independent numeric science have **not** been executed by this chat. An execution probe is not a PASS without the exact expected source/lock/fixture/environments, logs and signed-off independent acceptance.

No Contract Freeze/S11 Coding Authorization may be inferred from the Owner's A/A decisions.
