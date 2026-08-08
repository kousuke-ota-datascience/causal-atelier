# ENH-E3 実装順序補正・段階Gate適用指示

## 1. 本指示の目的

ENH-E3の実装は既に開始されている。

既存の承認済み `06_Ariadne_ENH-E3_実装指示書.md` に記載したWork Package自体を破棄するのではなく、実装順序を補正し、アーキテクチャ変更による既存Causal Capabilityへの回帰を早期に検出できる段階Gate方式へ変更する。

現在までに作成済みのコードは、明確な不整合または不要実装であることが確認されない限りrevertしない。

一方、Gateで要求された検証が完了するまでは、後続Capabilityの新規実装を進めてはならない。

---

## 2. 作業開始時の現状固定

最初に現在の作業状態を監査し、以下を記録すること。

```bash
git rev-parse HEAD
git status --short
git log --oneline --decorate -20
git diff --stat
```

加えて、ENH-E3開始基準コミットと現在HEADとの差分を確認し、既に実装された変更を以下へ分類すること。

* Generic Workflow Core
* Causal Adapter / Causal regression
* Analysis View
* Explore
* Predictive Specification
* Split / Leakage Validation
* Training
* Evaluation
* Explain
* Frontend
* Cross-analysis Lineage
* E2E / Verification

既に後続ステップのコードが存在していても削除しない。

ただし、その存在をもって当該ステップをCompletedとは判定しない。各ステップは、本指示で定義するGateをPASSした場合のみCompletedとする。

現在のHEAD、未commit差分、上記分類結果を実装報告書へ記録すること。

---

## 3. 旧Work Packageと補正後フローの対応

既存実装指示書のWork Packageを以下の順序へ再配置する。

| 補正後Phase                              | 既存WP    | 扱い                              |
| ------------------------------------- | ------- | ------------------------------- |
| E3-1A Generic Workflow Core           | WP-2    | 先行実施                            |
| E3-1B Causal Adapter / Regression     | WP-6    | WP-2直後へ前倒し                      |
| Gate G1                               | 新規Gate  | E3-1完了判定                        |
| E3-2 Analysis View                    | WP-3    | G1 PASS後                        |
| E3-2 Explore                          | WP-4    | Analysis Viewと連続実施              |
| E3-2 Explore UI                       | WP-7の一部 | Exploreと同時完成                    |
| Gate G2                               | 新規Gate  | E3-2完了判定                        |
| E3-3 Predictive Specification + Split | WP-5の一部 | 独立Phaseへ分離                      |
| Gate G3                               | 新規Gate  | Predictive data contract完了判定    |
| E3-4 Training + Evaluation            | WP-5の一部 | 独立Phaseへ分離                      |
| Gate G4                               | 新規Gate  | Predictive model evaluation完了判定 |
| E3-5 Explain                          | WP-5の一部 | 独立Phaseへ分離                      |
| E3-5 Predictive UI                    | WP-7の一部 | Explainと統合                      |
| Gate G5                               | 新規Gate  | Predictive Capability完了判定       |
| E3-6 Cross-analysis Lineage           | WP-8    | 後段統合                            |
| E3-6 Full E2E                         | WP-9    | 最終検証                            |
| Gate G6                               | 新規Gate  | ENH-E3完了判定                      |

WP-6をWP-2直後へ移動することが本補正の最重要変更である。

---

# 4. E3-1A: Generic Workflow Core

以下を完成させること。

* Planner Registry
* Stage Runner Registry
* Generic Execution Plan
* Stage dependency
* Plan validation
* input/output binding
* Artifact binding
* Stage Attempt
* Generic Executor
* retry / cancel / compensation
* schema version管理

Generic Workflow CoreにはCausal、Exploratory、Predictive固有の科学的意味論を直接埋め込まない。

Family固有validationはCapability側へ保持する。

Product層または新規Web API層から `ariadne.legacy` への新規依存を追加してはならない。

E3-1A終了後、直ちにE3-1Bへ進むこと。Analysis View、Explore、Predictiveの追加実装へ進んではならない。

---

# 5. E3-1B: Causal Adapter / Regression

Generic Workflow Core上で既存Causal Capabilityを接続する。

最低限、以下の既存Operationが新Workflow経由で成立すること。

```text
DISCOVERY
IDENTIFICATION
ESTIMATION
REFUTATION
SENSITIVITY
```

以下の既存科学契約を変更してはならない。

* `causal-analysis-spec/2`
* Operation input contract
* ResultType / ScientificStatus contract
* Graph provenance
* Identification status決定規則
* Data Eligibility
* `inferred_types`
* Estimator compatibility
* Estimation prerequisite gate
* `revision_context`
* RERUN / REVISED判定
* `change_reason`
* `scientific_warnings`
* post-discovery inference warning
* Result / Artifact / Lineage
* Annotation
* retry / revision semantics

この作業完了後、Gate G1を実行する。

---

# 6. Gate G1: Generic Workflow Core + Causal Regression Gate

## 6.1. Gate位置

```text
WP-2 Generic Workflow Core
        ↓
WP-6 Causal Adapter / Regression
        ↓
       G1
        ↓ PASSのみ
WP-3 Analysis View
```

G1をPASSするまで、ExploreおよびPredictive Capabilityの追加実装を進めてはならない。

## 6.2. 既存テストの流用

現在のworking treeに同等テストが存在することを再確認したうえで、最低限以下を実行すること。

```bash
uv run pytest -q \
  tests/product/test_enh_e1_contract.py \
  tests/product/test_enh_e2_contract.py \
  tests/product/test_estimator_compatibility_e1a.py \
  tests/product/test_domain_and_snapshot.py \
  tests/product/test_api_worker_e2e.py \
  tests/product/test_cli_contract.py \
  tests/product/test_frontend_contract.py \
  tests/product/test_architecture.py \
  tests/product/test_postgres_contract.py \
  tests/scientific/test_identification_e1a.py \
  tests/scientific/test_product_adapters.py \
  tests/scientific_benchmarks/test_enh_e1_benchmarks.py \
  tests/scientific_benchmarks/test_enh_e1a_acceptance.py \
  tests/integration/test_inference.py
```

既存テストが移動・改名されている場合は、現在HEAD上の同等テストへ読み替え、その対応をGate報告書へ記録すること。

## 6.3. 新規作成するGate専用テスト

Generic Workflow Coreへの載せ替え自体は既存テストだけでは直接保証できないため、以下相当の新規テストを追加すること。

推奨ファイル名:

```text
tests/product/test_enh_e3_causal_workflow_regression.py
```

最低限以下を検証すること。

* Causal PlannerがGeneric Execution Planを生成できる
* Causal StageがRunner Registryから解決される
* Stage間Artifact bindingが成立する
* Generic Executor経由で既存Causal Operationを実行できる
* 既存Result schemaが変更されない
* failure / retry / cancellationの意味が変わらない
* Causal固有validationがGeneric Coreへ漏出していない

## 6.4. 全回帰テスト

上記targeted test PASS後、必ず全Active testを実行すること。

```bash
uv run pytest -q
```

既存テストを削除、skip、xfail化、assertion緩和することでPASSさせてはならない。

既存仕様の変更が本当に必要な場合は、勝手にテストを変更せず、要件との矛盾として報告すること。

## 6.5. Browser E2E

Web / API / workerを実行可能な環境を構築し、既存Browser E2Eも実行すること。

既存:

```text
tests/browser_e2e/run_enh_e1a.py
```

実行不能の場合、G1をPASSとはせず `BLOCKED` とし、環境上の阻害要因を記録すること。

## 6.6. G1 Exit Criteria

以下を全て満たした場合のみPASS。

* targeted既存回帰テスト: PASS
* 新規Generic Workflow causal regression test: PASS
* `uv run pytest -q`: PASS
* Browser E2E: PASS
* Product/Web APIからlegacyへの新規依存: 0
* 既存Causal API contract破壊: 0
* 既存Scientific Status semantics変更: 0
* 既存scientific benchmark劣化: 0

G1 PASS時点のcommit hashを記録すること。

---

# 7. E3-2: Analysis View + Explore

G1 PASS後のみ開始する。

## 7.1. 実装範囲

* Analysis View Specification
* row selection
* column selection
* filter
* derived column
* missing-value policy
* temporal cutoff
* reproducible compilation
* provenance
* Dataset Versionとのlineage
* profiling
* distribution
* group summary
* association
* time trend
* visualization artifact
* saved exploratory result
* Explore UI

ExploreのUIをWP-7まで後回しにせず、E3-2内でAPI→Result→UIまでvertical sliceとして完成させる。

## 7.2. 新規テスト

同等テストが現在HEADに既に存在しない場合、以下を新規作成する。

```text
tests/product/test_analysis_view_e3.py
tests/product/test_exploratory_contract_e3.py
tests/product/test_exploratory_api_worker_e2e_e3.py
tests/product/test_exploratory_frontend_contract_e3.py
```

必要に応じてscientific/statistical characterization testも追加する。

---

# 8. Gate G2: Analysis View + Explore Gate

G2では最低限以下を確認する。

* Dataset VersionからAnalysis Viewを決定論的に再構築できる
* filter / derived column / missing policyがmanifestへ保存される
* lineageからsource Dataset Versionへ遡れる
* 同一Specから同一Viewが得られる
* Explore Resultが因果Resultとして誤表示されない
* Saved Explorationを再表示できる
* Explore UIからDraft Causal / Predictive analysisへ引き継ぐ情報が明示的である
* G1の全Causal regression testsが引き続きPASSする

G2でも最後に以下を実行する。

```bash
uv run pytest -q
```

G2 PASS commitを記録する。

---

# 9. E3-3: Predictive Specification + Split

G2 PASS後のみ開始する。

WP-5を一括実装せず、まずPrediction ProblemとDataset Splitだけを完成させる。

## 9.1. 実装範囲

* Predictive Analysis Specification
* task type
* target
* feature set
* prediction unit
* prediction time
* prediction horizon
* feature availability cutoff
* intended use
* metric specification
* split strategy
* random seed
* train / validation / test partition artifact
* group split
* temporal split
* leakage validator

この段階ではモデルTrainingを完成させる必要はない。

## 9.2. 新規テスト

```text
tests/product/test_predictive_spec_e3.py
tests/product/test_predictive_split_e3.py
tests/product/test_predictive_leakage_e3.py
tests/product/test_predictive_split_api_e3.py
```

---

# 10. Gate G3: Predictive Specification + Split Gate

以下を全て確認する。

* target leakageを拒否する
* feature availability cutoff違反を拒否する
* temporal leakageを拒否する
* group leakageを拒否する
* train / validation / testが決定論的に再現できる
* split artifactから元Dataset Versionへlineageを辿れる
* test partitionは後続のmodel selection入力として使用できない契約になっている
* Binary Classification / Regression以外を明示的に拒否する
* G1およびG2の既存テストが全てPASSする

最後に:

```bash
uv run pytest -q
```

G3 PASS commitを記録する。

---

# 11. E3-4: Training + Evaluation

G3 PASS後のみ開始する。

## 11.1. 実装範囲

```text
PREPARE
↓
TRAIN
↓
EVALUATE
```

* preprocessing
* preprocessing fitはtrain partition限定
* model fitting
* validation metric
* model selection
* frozen model artifact
* untouched test evaluation
* prediction artifact
* classification metrics
* regression metrics
* residual
* calibration等の必要診断
* reproducibility metadata

## 11.2. 新規テスト

```text
tests/product/test_predictive_training_e3.py
tests/product/test_predictive_evaluation_e3.py
tests/product/test_predictive_api_worker_e2e_e3.py
tests/scientific_benchmarks/test_predictive_e3_benchmarks.py
```

---

# 12. Gate G4: Training + Evaluation Gate

最低限以下を確認する。

* preprocessingがvalidation/testへfitされない
* test setがhyperparameter selectionへ使われない
* frozen modelでのみtest evaluationされる
* random seedおよびruntime metadataが保存される
* classification / regression metricがtask typeと整合する
  -同一入力・同一seedで再現可能である
* model artifact / prediction / metric間のlineageが成立する
* G1〜G3の全回帰がPASSする

最後に:

```bash
uv run pytest -q
```

G4 PASS commitを記録する。

---

# 13. E3-5: Explain + Predictive UI

G4 PASS後のみ開始する。

## 13.1. 実装範囲

* Explanation Specification
* global explanation
* local explanation
* feature importance
* explanation dataset provenance
* Model Card
* Predictive Workspace UI
* Evaluation UI
* Explanation UI
* error analysis UI

UIとResult Schemaの双方で以下を明確に区別する。

```text
Predictive Explanation
≠ Causal Explanation
≠ Treatment Effect
```

予測モデルのfeature importanceやSHAP系出力を因果効果として表示または説明してはならない。

## 13.2. 新規テスト

```text
tests/product/test_predictive_explanation_e3.py
tests/product/test_predictive_frontend_contract_e3.py
tests/browser_e2e/run_enh_e3_predictive.py
```

---

# 14. Gate G5: Explain + Predictive UI Gate

以下を確認する。

* Explanationがfrozen modelに紐付く
* Explanation datasetが追跡可能
* Predictive / Causal用語が混同されない
* Model CardがSpecification / Dataset / Split / Model / Evaluationへlineageを持つ
* Predictive UIのdeep link / reload / browser backが成立する
* G1〜G4の全テストがPASSする

最後に:

```bash
uv run pytest -q
```

G5 PASS commitを記録する。

---

# 15. E3-6: Cross-analysis Lineage + Full E2E

G5 PASS後のみ開始する。

## 15.1. 実装範囲

以下の関係を統合する。

```text
Research Context
    ↓
Dataset Version
    ├── Exploratory Analysis
    ├── Causal Analysis
    └── Predictive Analysis
```

さらに以下を追跡可能にする。

```text
Exploratory Result → Causal Analysis
Exploratory Result → Predictive Analysis
Dataset Version → 各Analysis View
Execution → Result → Artifact
Result → Annotation
Result → Research Context
```

異なるAnalysis FamilyのResultを同一意味のscoreとして比較してはならない。

---

# 16. Gate G6: ENH-E3 Final Gate

新規テストとして、同等物が存在しなければ以下を追加する。

```text
tests/product/test_cross_analysis_lineage_e3.py
tests/product/test_enh_e3_api_worker_e2e.py
tests/browser_e2e/run_enh_e3.py
```

最終E2Eでは最低限、

```text
Research Context
→ Dataset Version
→ Explore
→ Saved Exploration
→ Predictive Specification
→ Split
→ Train
→ Evaluate
→ Explain
→ Causal Analysis
→ Results / Lineage
```

を通すこと。

さらに以下を実行する。

```bash
uv run pytest -q
```

Migrationについてupgradeおよびdowngrade/re-upgradeを検証する。

OpenAPI contract、CLI contract、Frontend contract、architecture dependency ruleを再確認する。

既存Causal scientific benchmarkと新規Predictive benchmarkの双方をPASSさせる。

Browser E2EをPASSさせる。

G6 PASS commitを記録する。

---

# 17. Gate運用規則

各Gateの結果は以下のいずれかのみとする。

```text
PASS
FAIL
BLOCKED
```

「概ねPASS」「主要テストPASS」等の曖昧な判定は禁止する。

FAILまたはBLOCKED状態で次Phaseへ進んではならない。

既に次Phaseのコードが存在する場合も、そのコードは保持してよいが、新規追加・拡張作業は停止する。

Gateを通すために既存テストを弱体化してはならない。

新旧契約が衝突する場合は自己判断で契約を変更せず、要件・設計不整合として報告する。

---

# 18. Gate報告書

ENH-E3計画ディレクトリ配下の `20_implementation_reports/` にGate報告書を作成すること。

推奨名称:

```text
ENH-E3_gate_execution_report.md
```

各Gateについて最低限以下を記録する。

```text
Gate:
Status:
Start commit:
Completed commit:
Working tree status:
Implemented scope:
Existing tests reused:
New tests added:
Commands executed:
PASS count:
FAIL count:
SKIP count:
Browser E2E result:
Scientific benchmark result:
Migration result:
Known limitations:
Detected deviations:
Reason for PASS / FAIL / BLOCKED:
```

G1〜G6すべての証跡を同一報告書へ蓄積する。

---

# 19. 完了条件

ENH-E3は、単に全機能が実装された状態では完了としない。

以下をすべて満たして初めてCompletedとする。

1. G1〜G6がすべてPASS
2. 全Active pytestがPASS
3. 既存Causal scientific benchmarkがPASS
4. 新規Predictive benchmarkがPASS
5. Browser E2EがPASS
6. Migration round-tripがPASS
7. Product層からlegacyへの新規依存がない
8. Causal scientific semanticsに回帰がない
9. Predictive leakage防止契約がテストされている
10. Cross-analysis LineageがE2Eで確認されている
11. 各Gateのcompleted commitが記録されている
12. `20_implementation_reports/` に実装・テスト証跡が残っている

以上の条件を満たさない状態をENH-E3 Completedとして報告してはならない。
