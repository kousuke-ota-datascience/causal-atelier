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

## B. Schema B02 — fully independent standard Draft 2020-12 validator

```bash
E11_DIR="$REPO_ROOT/docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/00_enhance_background/Revised_requirements_definition_documents"
OUT="$HOME/_work/e11_s05_review_$(git rev-parse --short=12 HEAD)"
mkdir -p "$OUT"
uv venv --python 3.12 "$OUT/env-schema"
uv pip install --python "$OUT/env-schema/bin/python" 'jsonschema>=4,<5'
"$OUT/env-schema/bin/python" "$E11_DIR/combined_review/tools/e11_profile_factor_compiler.py" --report "$OUT/b02_200_schema_validator.json"
sha256sum "$OUT/b02_200_schema_validator.json" > "$OUT/b02_200_schema_validator.sha256"
```

The report must say `PASS_SCHEMA_STRUCTURAL_AND_VALIDATOR_PARITY`, 200/200 with exact source Git blob hashes; otherwise B02 stays BLOCKED. The current tool has only proved 200 AST identity and a limited JS subset, **not** this standard validator on all 200.

## C. B04 — four separately resolved pinned Backend environments (candidates only)

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

The separate environment check returns `API_PROBED_NOT_SCIENCE_VALIDATED` at best; **not** method-specific fit/inference. If installation/symbol verification fails, preserve exact failure output and isolate compatibility/ABI/uncertain license obligations. Then run approved Method-specific tiny valid/invalid fit + CI/graph output fixture suite; no fallback method or CATE/IV target relabeling. Independently inspect the exact **tagged** package metadata and solver resolution rather than treating PyPI landing page as successful installation.

## D. Independent Review Agent

Start a **fresh** Codex/independent-science Review Agent session on the pinned checkout, using the self-contained prompt in `combined_review/158_20261122_s05_independent_science_reviewer_prompt.md`. The Reviewer must not be fed the author's verdict as trusted evidence, and must report actual independent computations, primaries, insufficiencies and 41 per-Method outcomes. Do not run a coding implementation agent (S11 not authorized). If no authorized independent process can be launched, record `S05-B05-REVIEWER_NOT_LAUNCHED`.

## E. Block/freeze criteria

- B02 PASS requires actual standard `jsonschema` run with full 200 source files, exact SHA and negative/positive parity.
- B03 PASS requires strict typed payload and independent semantic readback, study/manifest/contentref status, no row leak.
- B04 PASS requires effective Python3.12 isolated dependency resolution, signatures, **fitted** method-level API and approved inference semantics.
- B05 readiness requires independent analytic/graph oracle, actual reference fixtures+source hashes, T2 pilot and preregistered K/R/eps/threshold/family/seed/compute budget, and independent statistical approval of G08 HC1 realization.
- B06 71-file static finding list is a design correction obligation for S06–S09; not a reason to pretend S05 statistical checks ran.

No Contract Freeze/S11 Coding Authorization may be inferred from the Owner's A/A decisions.
