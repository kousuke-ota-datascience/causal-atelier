# テストMigration Execution Record

**状態:** `M01_PHYSICAL_COMPLETE / RUNTIME_VERIFICATION_PENDING`  
**目的:** physical test-code migration batchの追記型実行証跡

## 1. 実行policy

各migration batchは以下を記録する。

- batch ID
- execution date/time
- before SHA
- after SHA
- changed paths
- 実装したmanifest row
- 実行command / verification method
- collection / test result
- manifestからのdeviation
- blocker / failure classification
- 必要なfollow-up

Design decisionの変更は本書で行わず、`04_migration_decision_log.md` を更新してdecision IDを参照する。

## 2. 現在状態

```text
Migration batch count: 1
Physical migration completed: M01
Product semantic changes: NONE
Gate contract/candidate remediation: NONE
Comprehensive repository-wide migration: DEFERRED TO ENH-E12+
```

## 3. Batch M01 — ENH-E9 active tests to enhancement architecture

**状態:** `PHYSICAL_COMPLETE / RUNTIME_VERIFICATION_PENDING`

```text
Executed at: 2026-09-06
Before SHA: 5011a879a4d30cbb8ff6fd22bb96992f07c95677
Migration commit: ce65c20ae7f3f6d5d4c3be0e9661137ef8a140bd
Evidence update commit(s): cedf36f99822a92a6aa2695dc815f5bba38b0e50 and subsequent record update
Related decisions: D001, D005, D009, D010, D011, D012
Related manifest: 03_migration_manifest.md / M01
```

### Scope

ENH-E9で現在activeな6本のstatic frontend/source contract testを、Gate ownershipに従って `tests/enhancement/enh_e9/<gate>/frontend/` へ移動した。

### Files changed

```text
tests/product/test_enh_e9_g01_analysis_view_context_clarity.py
  -> tests/enhancement/enh_e9/g01/frontend/test_analysis_view_context_clarity.py

tests/product/test_enh_e9_g02_p01_discovery_copy_help_overflow.py
  -> tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py

tests/product/test_enh_e9_g02_p02_selection_comparison_clarity.py
  -> tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py

tests/product/test_enh_e9_g02_p03_adoption_feedback_export.py
  -> tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py

tests/product/test_enh_e9_estimation_submission_regression.py
  -> tests/enhancement/enh_e9/g03/frontend/test_estimation_submission_regression.py

tests/product/test_enh_e9_causal_result_presentation.py
  -> tests/enhancement/enh_e9/g04/frontend/test_causal_result_presentation.py
```

### Test-side rewrite

旧配置ではrepo rootを固定depthで取得していた。

```python
Path(__file__).parents[2]
Path(__file__).resolve().parents[2]
```

新配置ではdirectory depthに依存しないよう、ancestorから `pyproject.toml` を探索してrepo rootを解決する方式へ変更した。

この変更はtest harness/path resolutionのみであり、assertion semanticsおよびproduct codeは変更していない。

### Verification results

| Verification | Result | Evidence |
|---|---|---|
| branch fast-forward | `PASS` | migration commit `ce65c20ae7f3f6d5d4c3be0e9661137ef8a140bd` |
| 6 source paths -> 6 target paths | `PASS` | GitHub compareで6件すべて `renamed` |
| change scope | `PASS` | compare上のchanged filesは対象test 6本のみ |
| assertion body preservation | `PASS (SOURCE REVIEW)` | 各file差分はrepo-root helper追加 + fixed-depth行削除 |
| product code mutation | `NONE` | compare上product file変更なし |
| Gate contract / candidate mutation | `NONE` | migration対象外、変更なし |
| pytest collection | `NOT_EXECUTED` | 本セッションにrepository runtime execution environmentなし |
| targeted ENH-E9 tests | `NOT_EXECUTED` | 同上 |
| Browser E2E | `NOT_APPLICABLE` | M01はstatic test migration。Browser実行batchではない |

### Runtime verification limitation

ローカルcloneによるpytest実行を試みたが、このexecution environmentからGitHubへのnetwork cloneが利用できなかった。また、migration commitに対する自動CI statusは登録されていなかった。

したがって、M01について **physical migrationとsource-level structural verificationは完了**しているが、pytest collection / targeted runtime verificationのPASSは主張しない。

### Classification

```text
Physical migration defect: NONE OBSERVED
Runtime verification state: TEST_ENVIRONMENT_LIMITATION
Product defect: NOT INDICATED BY M01
```

### Gate / Enhancement impact

```text
Affected Enhancement: ENH-E9 test infrastructure only
Product candidate impact: NONE
Frozen contract impact: NONE
Product semantic impact: NONE
```

### Follow-up

- 次にENH-E9の実行可能環境で `pytest tests/enhancement/enh_e9/...` のcollection / targeted verificationを行う際、本記録へ結果を追記する。
- Comprehensive Test Code MigrationはENH-E12以降へdeferしたままとする。

## 4. Batch M02 — G02 Trial01 BLOCKED Browser test implementation repair

**状態:** `PASS / READY_FOR_INDEPENDENT_REVERIFICATION`

```text
Executed at: 2026-09-06
Before SHA: 2efa8f114ace89ccd35c7758e873086ba9e73f83
After SHA: 479f0685d348926e29be598cfa7d52aa39779c3e
Purpose: G02 Trial01 BLOCKED test implementation repair
Trial identity: SAME_TRIAL / G02 Trial01
Fixed Trial Candidate impact: NONE (8cf70523093efa53b59a7de2c655f9755dbceb8d unchanged)
```

### Scope

G02 Trial01のcanonical 999で `TEST_IMPLEMENTATION_DEFECT` と分類されたhistorical Browser E2Eのstale initial locatorを置き換える、G02専用のcurrent-UI Browser runnerを追加した。repository-wide migrationまたはproduct remediationではない。

### Changed test / test-infrastructure paths

```text
tests/enhancement/enh_e9/g02/browser_e2e/run_discovery_candidate_adoption.py
Dockerfile.browser-e2e
.dockerignore
```

`Dockerfile.browser-e2e` と `.dockerignore` の変更は、new runnerをtest-only Browser imageのbuild contextへ含めるためだけのorchestration変更である。

### Repair verification

| Verification | Result | Evidence |
|---|---|---|
| Syntax/import compile | PASS | `python3 -c "compile(...)"` completed successfully |
| Browser image build | PASS | new runner copied to `/workspace/tests/enhancement/enh_e9/g02/browser_e2e/` |
| Current UI initial navigation | PASS | `Project List -> #new-project -> /projects/new -> overview` |
| Required G02 journey | PASS | Dataset registration, current Discovery route, two Discovery executions, Graph Comparison, adopted FIXED Graph |
| Failure diagnostics | PASS | runner writes JSON checkpoints/console, trace, screenshot, and video |
| Product code diff | NONE | changed paths are test/test-infrastructure and this M02 record only |

Executed Browser command:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e9-g02-verify --profile e2e run --build --rm --no-deps --entrypoint python browser-e2e tests/enhancement/enh_e9/g02/browser_e2e/run_discovery_candidate_adoption.py
```

Observed result: `PASS`. Evidence: `test-results/browser_e2e/enh-e9-g02-discovery-candidate-adoption-evidence.json`, with all checkpoints through `adopted-fixed-graph`, two Discovery execution IDs, two comparison candidates, and modal feedback confirming a FIXED Graph Version.

### Gate / Enhancement impact

```text
Product code changes: NONE
07 changes: NONE
Fixed Trial Candidate impact: NONE
999 Gate Decision changes: NONE
Remaining blocker: NONE for the repaired test implementation
Next action: Independent Verification continuation for G02 Trial01
```

## 5. Batch template

### Batch Mxx — <title>

**状態:** `PLANNED | RUNNING | PASS | FAIL | BLOCKED | ROLLED_BACK`

```text
Executed at:
Before SHA:
After SHA:
Related decisions:
Related manifest rows:
```

#### Scope

- ...

#### Files changed

```text
source -> target
```

#### Results

| Verification | Result | Evidence |
|---|---|---|
| pytest collection | | |
| targeted tests | | |
| regression tests | | |
| enhancement tests | | |
| Browser/CI path validation | | |

#### Gate / Enhancement impact

```text
Affected Gate(s): NONE | Gxx ...
Product candidate impact: NONE | <explicit route reference>
Frozen contract impact: NONE | <explicit amendment reference>
```
