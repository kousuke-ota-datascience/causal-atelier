# テストMigration Manifest

**状態:** `DRAFT`  
**目的:** test architecture再編におけるsource-to-target migration authority

## 1. Manifest rule

各migration itemは以下を記録する。

- source path
- target pathまたはtarget test family
- action
- rationale
- dependency note
- migration後に必要なverification

許可するaction vocabulary:

```text
KEEP
MOVE
RENAME
PROMOTE
REWRITE
MERGE
SPLIT
ARCHIVE
RETIRE
REVIEW_SUPERSEDED
```

Ownershipが曖昧な状態でphysical moveを開始してはならない。

## 2. 初期high-confidence mapping

| Source | Target | Action | Notes |
|---|---|---|---|
| `tests/browser_e2e/run_enh_e7_project_integration.py` | `tests/regression/browser_e2e/run_project_lifecycle.py` | `PROMOTE + REWRITE` | current Project lifecycleのsource |
| `tests/browser_e2e/run_enh_e8_g01_project_return.py` | `tests/regression/browser_e2e/run_project_lifecycle.py` | `MERGE` | return/history scenarioをcanonical project journeyへ統合 |
| `tests/browser_e2e/run_enh_e6_family_stage_navigation.py` | `tests/regression/browser_e2e/run_analysis_navigation.py` | `PROMOTE + REWRITE` | Enhancement identityを除去しcurrent family/stage navigationを保持 |
| `tests/browser_e2e/run_enh_e3_predictive.py` | `tests/regression/browser_e2e/run_predictive_critical_journey.py` | `PROMOTE + REWRITE` | current predictive journeyをdistill |
| `tests/browser_e2e/run_enh_e1a.py` | historical archive + causal scenario source | `ARCHIVE + SPLIT` | canonical regressionとして全体修理しない |
| `tests/browser_e2e/run_enh_e3.py` | historical archive + scenario source | `ARCHIVE + SPLIT` | historical runner dependencyからcurrent invariantのみ抽出 |
| `tests/product/test_enh_e9_g02_p01_discovery_copy_help_overflow.py` | `tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py` | `MOVE + RENAME` | 現在確認済みのENH-E9/G02由来test |
| `tests/product/test_enh_e9_g02_p02_selection_comparison_clarity.py` | `tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py` | `MOVE + RENAME` | 現在確認済みのENH-E9/G02由来test |
| `tests/product/test_enh_e9_g02_p03_adoption_feedback_export.py` | `tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py` | `MOVE + RENAME` | 現在確認済みのENH-E9/G02由来test |
| `tests/scientific_benchmarks/` | `tests/benchmarks/scientific/` | `MOVE + REWRITE_NAMES_AS_NEEDED` | benchmark marker / semanticsを保持 |
| `tests/legacy_archive/` | unchanged | `KEEP` | default collection外を維持 |

上表のG02行は、現時点で具体的source pathが確定しているため記載している。Migrationの対象範囲はENH-E9全Gateおよび既存test体系全体であり、G02限定ではない。

## 3. Generic product tests

初期target family:

| Source pattern | Target family | Action |
|---|---|---|
| `tests/product/test_architecture.py` | `tests/regression/contract/architecture/` | `PROMOTE` |
| `tests/product/test_cli_contract.py` | `tests/regression/contract/` | `PROMOTE` |
| `tests/product/test_domain_and_snapshot.py` | `tests/regression/unit/` | `PROMOTE` |
| `tests/product/test_frontend_contract.py` | `tests/regression/frontend/` | `PROMOTE` |
| `tests/product/test_postgres_contract.py` | `tests/regression/integration/persistence/` | `PROMOTE` |
| `tests/product/test_api_worker_e2e.py` | `tests/regression/integration/` | `PROMOTE_REVIEW_LAYER` |
| `tests/product/compose_golden_path_smoke.py` | `tests/regression/integration/` | `PROMOTE_REVIEW_LAYER` |

Exact filenameはsemantic review後に確定する。

## 4. Enhancement family review group

### E1-E3

現在も有効なbehaviorは `PROMOTE + REWRITE + DEDUPE`。

Provenanceそのものがrequirementでない限り、恒久regression filenameからhistorical Enhancement identityを除去する。

### E4

Action: `SPLIT`。

- canonical execution/result/artifact/lineage invariant -> regression
- migration/cutover procedure assertion -> invariant抽出後archiveまたはretire

### E5

- navigation/history -> E6/E7と比較し `REVIEW_SUPERSEDED`
- causal/predictive/exploratory semantics -> `PROMOTE + MERGE`

### E6-E8

原則 `PROMOTE + MERGE`。Migration/runner-specific assertionはcurrent generic contractへ再記述する。

### E9

ENH-E9全Gateのtestを `tests/enhancement/enh_e9/<gate>/<layer>/...` の体系で整理し、Gate/Enhancementの安定化状態に応じて個別dispositionを行う。

`ACTIVE_ENH` は「ENH-E9全体が未完了であるため永続的にpromotionしない」という意味ではない。PASS済みGateも含め、current authoritative behaviorとして恒久保証すべきtestは明示的にpromotion candidateとして評価する。

## 5. Support migration

`tests/conftest.py` と `tests/product/conftest.py` は初回batchで機械的に移動しない。

事前に以下を記録する。

- fixture consumer
- pytest discovery scope
- environment variables
- import/path assumptions
- Docker/CI reference

Potential target:

```text
tests/support/fixtures/
tests/support/factories/
tests/support/helpers/
```

ただし `conftest.py` placementはpytest semantics上の構造要件として残る可能性がある。

## 6. Manifest completion condition

Physical migration開始条件:

1. 全active test fileにdispositionがある;
2. 全`SPLIT` / `MERGE` rowでdestination invariantが特定されている;
3. Browser / CI / Docker path referenceがinventory済み;
4. pytest fixture scope impactを理解している;
5. ENH-E9全GateのEnhancement-specific testとpermanent regression candidateの責務が分類されている。
