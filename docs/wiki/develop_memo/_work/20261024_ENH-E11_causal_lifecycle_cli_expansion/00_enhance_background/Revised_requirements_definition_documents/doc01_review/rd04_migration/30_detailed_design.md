# DOC-01 — 30詳細設計：RD-04移管原記録

**Kind:** FLOW/AUDIT; module/class contracts remain in stock Detailed Design. **Source HEAD:** `cce43523b701713e3e4d595fd7389299bdbf6e80`.

## 30_10_domain_resources.md

**Source blob:** `735c3a0de7805c4c12e31e1e4d2f7b66cc94af80`; constraints 1.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-007（SPLIT）

- 移管する原条項の具体内容：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない
- 上位Requirementと整合する要求核：分析実行時点の研究目的と理由を後から再現できる
- `FR-007`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

---

## 30_11_schema_canonicalization.md

**Source blob:** `c8a5070661613db7c5212463fcba1fda04d263dd`; constraints 1.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-003（SPLIT）

- 移管する原条項の具体内容：Canonical JSONとhash生成はfield順やprocessに依存しない
- 上位Requirementと整合する要求核：同一内容から環境に依存しない同一性識別値を生成できる
- `NFR-003`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_20_planning_validation.md

**Source blob:** `3d75438187c96932499632805e4c2c6c2f4486ec`; constraints 6.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-075（MOVE_BD）

- 移管する原条項の具体内容：Family別PlannerをRegistryから解決する
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-075`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. FR-079（MOVE_BD）

- 移管する原条項の具体内容：Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-079`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.3. FR-080（MOVE_BD）

- 移管する原条項の具体内容：canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】FR-081の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-080`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.4. FR-089（MOVE_BD）

- 移管する原条項の具体内容：Generic validationとFamily-specific validationを分離して実行する
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】FR-085の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-089`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.5. FR-128a（MOVE_BD）

- 移管する原条項の具体内容：Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】FR-035／NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-128a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.6. FR-128b（SPLIT）

- 移管する原条項の具体内容：size limit、timeout等のoperational resource configurationを一元管理する
- 上位Requirementと整合する要求核：運用上の処理規模と実行時間の上限を設定・適用できる
- `FR-128b`；Status=`DEFERRED`；Implementation=`NOT_IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

---

## 30_21_execution_runtime.md

**Source blob:** `2c476697b2fa6ade815398a0b817cdd18ff09135`; constraints 6.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-086a（SPLIT）

- 移管する原条項の具体内容：stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する
- 上位Requirementと整合する要求核：確率的処理を再試行しても同じ実効乱数条件を再現できる
- `FR-086a`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. FR-086b（SPLIT）

- 移管する原条項の具体内容：Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する
- 上位Requirementと整合する要求核：処理ごとの時間・資源上限を設定できる
- `FR-086b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.3. NFR-001b（SPLIT）

- 移管する原条項の具体内容：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- 上位Requirementと整合する要求核：解析結果を再現するため実効ライブラリ版・乱数条件を取得できる
- `NFR-001b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.4. NFR-006a（SPLIT）

- 移管する原条項の具体内容：current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる
- 上位Requirementと整合する要求核：中断・再送時にExecutionを安全に再開・再試行できる
- `NFR-006a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.5. NFR-006b（SPLIT）

- 移管する原条項の具体内容：retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない
- 上位Requirementと整合する要求核：再試行・再起動で成功済み成果物の重複作成を防止する
- `NFR-006b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.6. AR-019（SPLIT）

- 移管する原条項の具体内容：random seedだけでなくsplit indexまたはpartition artifactを保存する
- 上位Requirementと整合する要求核：分析のデータ分割を再現可能な情報として保持しなければならない
- `AR-019`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_35_predictive_training.md

**Source blob:** `15a97f07a11fb7a938e1f1d59bb5dadc054f85b9`; constraints 2.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-176（SPLIT）

- 移管する原条項の具体内容：Predictive Navigation Stageを新しいbackend Execution modelまたは1:1 runtime Stageとして扱わず、既存Prediction Task → Split → Training → Evaluation → Explanation → Model Card semanticsを保持する
- 上位Requirementと整合する要求核：既存の予測タスク設定・データ分割・学習・評価・説明・Model Cardの意味を維持し、Navigation変更で分析実行契約を変更しない
- `FR-176`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. AR-016（SPLIT）

- 移管する原条項の具体内容：subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない
- 上位Requirementと整合する要求核：評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない
- `AR-016`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_36_predictive_explanation.md

**Source blob:** `16bc6a741c786c9215ecc475aeddd00960b2708c`; constraints 2.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-068（SPLIT）

- 移管する原条項の具体内容：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- 上位Requirementと整合する要求核：学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる
- `FR-068`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. FR-180（SPLIT）

- 移管する原条項の具体内容：fitted modelはserialize/load round-trip後もmodel/task/feature/preprocessor identityを保持し、同一runtime/config fixtureでprediction contractを満たす
- 上位Requirementと整合する要求核：保存済み学習モデルを復元し、適合条件下で同等の予測を再実行できる
- `FR-180`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

---

## 30_41_navigation_routing.md

**Source blob:** `d410b56d9bfde118802126c11db698cea44c78d5`; constraints 4.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-143（MOVE_BD）

- 移管する原条項の具体内容：runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-025の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-143`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. FR-140（MOVE_BD）

- 移管する原条項の具体内容：Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-140`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.3. FR-145（MOVE_BD）

- 移管する原条項の具体内容：generic application layerはFamily-specific Stage semanticsを集中所有しない
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-023の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-145`；Status=`ACTIVE`；Implementation=`NOT_IMPLEMENTED`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.4. NFR-025（SPLIT）

- 移管する原条項の具体内容：CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない
- 上位Requirementと整合する要求核：CLIやライブラリ実行を画面状態なしで行える
- `NFR-025`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_50_persistence_artifacts.md

**Source blob:** `670ddf107b35d638e365fd5606a4dea7b1552caf`; constraints 2.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-007（SPLIT）

- 移管する原条項の具体内容：Metadata transactionとArtifact writeのcross-store failure compensationを定義する
- 上位Requirementと整合する要求核：成果物と管理情報の不整合が発生した場合、安全に回復・検知できる
- `NFR-007`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-020a（SPLIT）

- 移管する原条項の具体内容：Artifact storageを`ArtifactStore` Port abstraction越しに利用する
- 上位Requirementと整合する要求核：成果物保存先を交換しても分析の振る舞いが維持される
- `NFR-020a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_51_security.md

**Source blob:** `8a9568e5c74afb57628a26271377d1c3d0a34d6b`; constraints 2.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-008a（SPLIT）

- 移管する原条項の具体内容：current input validation、path traversal防止、secret非露出等のsafeguardを維持する
- 上位Requirementと整合する要求核：入力検証と危険なパス・秘密情報の保護を維持する
- `NFR-008a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-018（MOVE_BD）

- 移管する原条項の具体内容：Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない
- 上位Requirementと整合する要求核：【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- `NFR-018`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_52_failure_handling.md

**Source blob:** `01ae0ceac5594a436db89b5674c2876adff6d55e`; constraints 1.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-011a（SPLIT）

- 移管する原条項の具体内容：current request/execution/stage correlation identifiersをlogへ出力する
- 上位Requirementと整合する要求核：Request・実行・処理単位をまたいで障害を追跡できる
- `NFR-011a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_60_cli_adapters.md

**Source blob:** `27c35c0218c71ffba75d9a446c6d08597662639a`; constraints 3.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. FR-120b（SPLIT）

- 移管する原条項の具体内容：canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する
- 上位Requirementと整合する要求核：API仕様と公開する入出力例との整合性を検証できる
- `FR-120b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../95_rd04_fr_application_review.md)

### 98.2. NFR-005（SPLIT）

- 移管する原条項の具体内容：新Analysis Familyを既存Executor変更なしにRegistry追加できる
- 上位Requirementと整合する要求核：新しい分析領域を既存分析の挙動を壊さず追加できる
- `NFR-005`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.3. NFR-010b（SPLIT）

- 移管する原条項の具体内容：Worker restart後の明示的resume/recovery semanticsを定義する
- 上位Requirementと整合する要求核：実行基盤の再起動後に処理状態を復元・回復できる
- `NFR-010b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

## 30_90_verification_traceability.md

**Source blob:** `43169eae1baed54b4cec80c007113f3375a048bb`; constraints 2.

## 98. RD-04：詳細設計へ引き継ぐ要求起源の具体制約

**Status:** `RD04_DETAILED_CONSTRAINT_TRACE / OWNER_CONTENT_REVIEW_PENDING`。RD-04で抽象化した原文から、モジュール・Class・Method・I/O・失敗処理へ落とすべき実現制約を保持する。実装されていると確認した記録ではない。クラスレベル仕様は[共通テンプレート](30_01_class_design_template.md)に従い別途DD設計確認する。

### 98.1. NFR-015（SPLIT）

- 移管する原条項の具体内容：Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる
- 上位Requirementと整合する要求核：Domain・実行・API・UI・科学計算を個別に検証できる
- `NFR-015`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-024（SPLIT）

- 移管する原条項の具体内容：Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる
- 上位Requirementと整合する要求核：画面構成・URL復元・表示・分析実行独立性を個別に検証できる
- `NFR-024`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[逐条Disposition](../96_rd04_nfr_ar_application_review.md)

---

