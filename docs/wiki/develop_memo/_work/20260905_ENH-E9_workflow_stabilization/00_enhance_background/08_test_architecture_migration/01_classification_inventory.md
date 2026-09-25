# テスト分類Inventory

**状態:** `INITIAL_BASELINE`  
**Inventory date:** 2026-09-06  
**Repository branch:** `bugfix/ariadne_mvp_e9`

## 1. 分類語彙

| Classification / Action | 意味 |
|---|---|
| `PROMOTE` | 現在のauthoritative behaviorを恒久regressionへ昇格する |
| `PROMOTE_REWRITE` | semantic coverageを維持しつつ、歴史的Enhancement identityやobsolete structureを除去して再記述する |
| `MERGE` | 重複するtest coverageをより小さいcurrent regressionへ統合する |
| `SPLIT` | current invariantとmigration/history専用assertionを分離する |
| `ACTIVE_ENH` | 現在のEnhancement staging areaに保持する |
| `BENCHMARK` | 通常regressionと分離したscientific/statistical benchmarkとして保持する |
| `ARCHIVE` | historical evidenceとして保持するがactive regressionから外す |
| `REVIEW_SUPERSEDED` | 後続テストと比較し、現在も有効な固有invariantのみ残す |
| `KEEP` | 現在の配置・責務を維持する |

## 2. 現在のトップレベル構造

```text
tests/
├── browser_e2e/
├── integration/
├── legacy_archive/
├── product/
├── scientific/
└── scientific_benchmarks/
```

現状は、lifecycle / authorityとverification layerが同一階層で混在している。`product` / `scientific` はdomain・purpose寄りの分類である一方、`integration` / `browser_e2e` はverification layerであり、分類軸が揃っていない。

## 3. Test family別の初期inventory

### 3.1 Generic product tests

例:

- `tests/product/compose_golden_path_smoke.py`
- `tests/product/test_api_worker_e2e.py`
- `tests/product/test_architecture.py`
- `tests/product/test_cli_contract.py`
- `tests/product/test_domain_and_snapshot.py`
- `tests/product/test_frontend_contract.py`
- `tests/product/test_postgres_contract.py`

初期判定: 実際のverification layerに応じて `tests/regression/<layer>/...` へ **PROMOTE**。

### 3.2 ENH-E1 / E2 / E3 product tests

Analysis specification/view、causal workflow、predictive workflow、exploratory workflow、research context、lineage/export、estimator compatibility、frontend contract等を含む。

初期判定: **PROMOTE_REWRITE**。現在も有効なbehaviorに対し、`_e3` 等の歴史的suffixを恒久regression identityとして残さない。

### 3.3 ENH-E4 execution-authority tests

E4には、恒久的なexecution semanticsと、当時のmigration/cutover assertionが混在している。

恒久invariantの例:

- rerunが新しいcanonical executionを作成する;
- base executionがimmutableである;
- stage semanticsとrevision lineageを保持する;
- canonical execution/result/artifact authorityが一貫する。

初期判定: **SPLIT**。

- durable current invariant -> `PROMOTE_REWRITE`
- migration/cutover procedure/history -> invariant抽出後に `ARCHIVE` またはretire

### 3.4 ENH-E5 tests

Navigation系はE6/E7の後続navigation architectureでsupersedeされている可能性が高い。

初期判定:

- old navigation/history shell -> `REVIEW_SUPERSEDED`
- predictive/causal/exploratory semantics -> `PROMOTE_REWRITE` / `MERGE`

### 3.5 ENH-E6 tests

Navigation / stage-presentation behaviorは現在も有効な可能性が高い。一方、特定historical Browser runner filenameの存在そのものをassertするtestはimplementation-specificである。

初期判定:

- navigation semantics -> `PROMOTE_REWRITE`
- specific runner integration assertion -> `SPLIT`し、generic Browser harness contractへ再記述

### 3.6 ENH-E7 tests

Project / Analysis routingとsurface architectureはcurrent regressionの主要sourceである。一方、migration/cutover/cleanup assertionも混在する。

初期判定:

- current Project / Analysis invariant -> `PROMOTE_REWRITE` / `MERGE`
- migration/cutover/history assertion -> `SPLIT` / `ARCHIVE`

### 3.7 ENH-E8 tests

現行causal/predictive stage-surface behaviorは恒久regression候補。

初期判定: **PROMOTE_REWRITE / MERGE**。

### 3.8 ENH-E9 tests

ENH-E9内で追加・変更されたtestは、Gate単位の由来を保持したまま、まず `tests/enhancement/enh_e9/<gate>/<layer>/...` に整理する。

初期判定: **ACTIVE_ENH**。Gate PASSやEnhancement completion後に、各testを個別にPROMOTE / REWRITE / MERGE / RETIRE / ARCHIVE判定する。

現在確認済みの具体例としてG01/G02由来testやcausal-result/estimation-presentation guardが存在するが、これはinventory上の実在ファイルを示すものであり、本migrationのscopeを特定Gateに限定するものではない。

特記事項: `test_enh_e9_causal_result_presentation.py` はproduct presentation assertionとENH-E9作業文書に対するassertionを混在させているため、恒久promotion前に **SPLIT** が必要。

## 4. Browser E2E inventory

| Existing runner | 初期判定 |
|---|---|
| `run_enh_e1a.py` | `ARCHIVE` + 現在も有効なscenarioを抽出 |
| `run_enh_e3.py` | `ARCHIVE` / `DISTILL` |
| `run_enh_e3_predictive.py` | predictive critical journeyへ `PROMOTE_REWRITE` |
| `run_enh_e6_family_stage_navigation.py` | analysis navigation regressionへ `PROMOTE_REWRITE` |
| `run_enh_e7_project_integration.py` | project lifecycle regressionへ `PROMOTE_REWRITE` |
| `run_enh_e8_g01_project_return.py` | project lifecycle regressionへ `MERGE` |
| `run_enh_e8_g02_causal_stage_content.py` | causal/navigation regressionへ `MERGE` |
| `run_enh_e8_g02_predictive_stage_content.py` | predictive regressionへ `MERGE` |

重要な観測: historical Browser runnerにはdependency chainとstale navigation assumptionが存在する。過去にacceptance runnerだったという理由だけで、immutableなregression authorityとして扱ってはならない。

## 5. Scientific tests

### `tests/scientific/`

Identification/eligibility、discovery graph semantics、estimator recovery、overlap handling、requirement linkage等のdeterministic scientific product semanticsを含む。

初期判定: 主としてcurrent scientific regression layerへ **PROMOTE**。単なるcharacterization扱いにはしない。

### `tests/scientific_benchmarks/`

Synthetic / semi-synthetic repeated scenario、bias/RMSE/coverage、scientific acceptance threshold等を評価する。

初期判定: `tests/benchmarks/scientific/` 配下の **BENCHMARK**。

## 6. Existing integration directory

### `tests/integration/test_core.py`

Pure unit、config、feature semantics、architecture boundary assertionが混在する。

初期判定: unit / contract regressionへ **SPLIT**。

### `tests/integration/test_inference.py`

Estimatorおよびfixed-seed scientific behaviorを含み、新しいscientific testsとの重複可能性がある。

初期判定: **PROMOTE_REWRITE / DEDUPE REVIEW**。

## 7. Legacy / support

### `tests/legacy_archive/`

既にdefault pytest collectionから隔離されている。

初期判定: **KEEP**。

### `conftest.py` / shared fixtures

Fixture placementはpytest scope/discoveryに影響するため、初回migration batchで機械的に移動しない。

初期判定: **SUPPORT REVIEW**。consumer/dependency分析後に移行する。

## 8. 高確度結論と未解決事項

高確度で確定できる事項:

- ENH-E9固有testはまずenhancement stagingで管理する;
- historical Browser runnerはそのまま修理・昇格せず、current invariantをdistillする;
- scientific benchmarkはstandard regressionから分離する;
- legacy archiveはdefault collection外を維持する;
- migration/cutover historyを、単に現在もpassするという理由で恒久product regressionにしてはならない。

Physical migration前に必要な作業:

1. E1-E8のfile-by-file duplicate / superseded比較;
2. 各fileのexact verification layer決定;
3. rename後targetの確定;
4. fixture/import/path dependency分析;
5. CI / Docker / command reference inventory。
