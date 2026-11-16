# DOC-01 — 22基本設計：RD-04移管原記録（1/2）

**Kind:** FLOW/AUDIT; permanent design contracts are in the domain-specific stock BD files. **Source HEAD:** `b7d53becd73d36a0d0ad7f5b561f254ef1e99c57`.

## 22_00_overall_BD.md

**Source blob:** `a146ffbd35261352fc5085aa09bfcc7e6bff0b56` — migrated constraints 1.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. NFR-018（MOVE_BD）

- 既存要件の設計情報を含む原文：Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Original Requirement：`NFR-018`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

## 22_01_information_architecture.md

**Source blob:** `42013ada65b64b7f10c22e8e66894e5b99040748` — migrated constraints 4.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-169（SPLIT）

- 既存要件の設計情報を含む原文：Results / Lineageはpersisted cross-analysis aggregation、comparison、Artifact、Lineage、Annotationを所有し、Analysis Workspaceはexecution-local / stage-local presentationを担う
- RDに残る能力／Legacy Trace：Project横断結果の比較・来歴と実行中の分析結果を適切に区別して閲覧できる
- Original Requirement：`FR-169`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-163（SPLIT）

- 既存要件の設計情報を含む原文：`/projects`をProject Listのcanonical surfaceとする
- RDに残る能力／Legacy Trace：Project一覧へ一意の正規画面からアクセスできる
- Original Requirement：`FR-163`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-164（SPLIT）

- 既存要件の設計情報を含む原文：`/projects/new`をProject Registerのcanonical surfaceとし、作成成功後は`/projects/{new_project_id}/overview`へ遷移する
- RDに残る能力／Legacy Trace：Project作成後に対象Projectの概要画面へ遷移できる
- Original Requirement：`FR-164`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-165（SPLIT）

- 既存要件の設計情報を含む原文：`/projects/{project_id}/overview`をselected Projectのdefault canonical surfaceとし、`/projects/{project_id}`はhistory-replaceでoverviewへnormalizeする
- RDに残る能力／Legacy Trace：対象Projectの標準表示画面を一意に復元できる
- Original Requirement：`FR-165`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

---

## 22_02_web_operation.md

**Source blob:** `a758e82be2951107b7b9616760a8aa54ae52c308` — migrated constraints 3.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-002（SPLIT）

- 既存要件の設計情報を含む原文：Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する
- RDに残る能力／Legacy Trace：Projectの研究目的と意思決定文脈を区別して保持・参照できる
- Original Requirement：`FR-002`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-011（SPLIT）

- 既存要件の設計情報を含む原文：DatasetVersionにcontent hash、schema、row count、column countおよびcurrent profile summaryを保持する。登録時の独立full profile生成を必須化しない
- RDに残る能力／Legacy Trace：各データ版の同一性・構造・規模・品質概要を確認できる
- Original Requirement：`FR-011`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-020（SPLIT）

- 既存要件の設計情報を含む原文：Explore stateのdata-selection semantics（row_filter、selected_columns、derived_columns、missing_value_policy、time_cutoff、sampling）からAnalysisView DRAFTを作成できる。presentation-only chart stateはAnalysisViewへ保存しない
- RDに残る能力／Legacy Trace：探索中に選択したデータ条件をAnalysis Viewの草案として作成できる
- Original Requirement：`FR-020`; Status：`ACTIVE`; Implementation：`NOT_IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

---

## 22_03_navigation_application.md

**Source blob:** `48039ff9fb668edd60232cf12f013077bf48121e` — migrated constraints 23.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-143（MOVE_BD）

- 既存要件の設計情報を含む原文：runtime layerはNavigation Stage ID、browser route、tab/sidebar stateへ依存しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-025の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-143`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-107（SPLIT）

- 既存要件の設計情報を含む原文：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- RDに残る能力／Legacy Trace：操作の可否と不可理由を一貫した権限・状態に基づいて表示できる
- Original Requirement：`FR-107`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-108（SPLIT）

- 既存要件の設計情報を含む原文：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- RDに残る能力／Legacy Trace：分析仕様・実行・結果・Graphへ文脈を保持して直接移動できる
- Original Requirement：`FR-108`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-109（SPLIT）

- 既存要件の設計情報を含む原文：非同期presentation stateを`IDLE / LOADING / READY / EMPTY / PARTIAL / ERROR / CANCELLED`として区別する
- RDに残る能力／Legacy Trace：読み込み中・空結果・部分結果・失敗・取消を適切に区別して表示できる
- Original Requirement：`FR-109`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-130（SPLIT）

- 既存要件の設計情報を含む原文：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- RDに残る能力／Legacy Trace：現在の分析Familyと画面位置を識別・復元できる
- Original Requirement：`FR-130`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.6. FR-132（SPLIT）

- 既存要件の設計情報を含む原文：Family切替時はCapability descriptorが宣言するdefault Navigation Stage（Exploratory=`profile`, Causal=`setup`, Predictive=`setup`）へ遷移する
- RDに残る能力／Legacy Trace：Family切替後は、そのFamilyの初期画面へ遷移できる
- Original Requirement：`FR-132`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.7. FR-133（MOVE_BD）

- 既存要件の設計情報を含む原文：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-133`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.8. FR-136（SPLIT）

- 既存要件の設計情報を含む原文：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- RDに残る能力／Legacy Trace：分析ページのURLから対象Project・Family・画面位置を復元できる
- Original Requirement：`FR-136`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.9. FR-140（MOVE_BD）

- 既存要件の設計情報を含む原文：Navigation Stageをruntime `StageType` / `StageDefinition` / `StageExecution`として再利用・継承しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-140`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.10. FR-141（MOVE_BD）

- 既存要件の設計情報を含む原文：Navigation StageとExecution Stageの1:1 mappingを要求するcontractを導入しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-141`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.11. FR-144（MOVE_BD）

- 既存要件の設計情報を含む原文：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-144`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.12. FR-145（MOVE_BD）

- 既存要件の設計情報を含む原文：generic application layerはFamily-specific Stage semanticsを集中所有しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-023の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-145`; Status：`ACTIVE`; Implementation：`NOT_IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.13. FR-157（MOVE_BD）

- 既存要件の設計情報を含む原文：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-074の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-157`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.14. FR-158（MOVE_BD）

- 既存要件の設計情報を含む原文：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-158`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.15. FR-159（SPLIT）

- 既存要件の設計情報を含む原文：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- RDに残る能力／Legacy Trace：旧分析画面から正規の分析画面へ一意に遷移できる
- Original Requirement：`FR-159`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.16. FR-160（MOVE_BD）

- 既存要件の設計情報を含む原文：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-021／FR-177の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-160`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.17. FR-171（SPLIT）

- 既存要件の設計情報を含む原文：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- RDに残る能力／Legacy Trace：分析画面で選択Projectを確認でき、Project変更は管理機能で実施できる
- Original Requirement：`FR-171`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.18. NFR-021（SPLIT）

- 既存要件の設計情報を含む原文：Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない
- RDに残る能力／Legacy Trace：画面ナビゲーションの変更が分析実行ライフサイクルに影響しない
- Original Requirement：`NFR-021`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.19. NFR-023（SPLIT）

- 既存要件の設計情報を含む原文：Family-specific Navigation Stage catalogをCapability ownershipで局所化する
- RDに残る能力／Legacy Trace：Familyごとの画面構成を他Familyへの影響を抑えて変更できる
- Original Requirement：`NFR-023`; Status：`ACTIVE`; Implementation：`NOT_IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.20. NFR-025（SPLIT）

- 既存要件の設計情報を含む原文：CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない
- RDに残る能力／Legacy Trace：CLIやライブラリ実行を画面状態なしで行える
- Original Requirement：`NFR-025`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.21. AR-021（SPLIT）

- 既存要件の設計情報を含む原文：Navigation Stageの表示順を分析上必須の実行順序として解釈しない
- RDに残る能力／Legacy Trace：Navigation Stageの表示順を、因果分析その他の科学的な実行順序や必須解析手順として解釈させない
- Original Requirement：`AR-021`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.22. AR-022（MOVE_BD）

- 既存要件の設計情報を含む原文：Family間でStage数・名称を揃えることを科学的workflow要件としない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Original Requirement：`AR-022`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.23. AR-024（SPLIT）

- 既存要件の設計情報を含む原文：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
- RDに残る能力／Legacy Trace：因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる
- Original Requirement：`AR-024`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

## 22_04_workflow_core.md

**Source blob:** `fd954eb6c0db0a3de6c3512d82e607a8d6c9c057` — migrated constraints 14.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-075（MOVE_BD）

- 既存要件の設計情報を含む原文：Family別PlannerをRegistryから解決する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-075`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-076（SPLIT）

- 既存要件の設計情報を含む原文：Plannerはversionedで不変なExecution Planを生成する
- RDに残る能力／Legacy Trace：分析の実行計画を版管理し、実行時の条件を後から復元できる
- Original Requirement：`FR-076`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-077（MOVE_BD）

- 既存要件の設計情報を含む原文：Stage Typeをnamespace、name、versionで識別する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-076の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-077`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-078（SPLIT）

- 既存要件の設計情報を含む原文：PlanはStage dependencyとinput/output bindingをDAGとして保持する
- RDに残る能力／Legacy Trace：分析処理の依存順序と処理間の入力・出力の対応を追跡できる
- Original Requirement：`FR-078`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-079（MOVE_BD）

- 既存要件の設計情報を含む原文：Stage RunnerをRegistryから解決し、Executorへif/elif分岐を集約しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-079`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.6. FR-080（MOVE_BD）

- 既存要件の設計情報を含む原文：canonical lifecycle/application serviceがExecutionのclaim、state、cancel、retry、Result/Artifact metadata commitを所有し、Generic Executorはowned workflow context内で依存順、Stage sequencing、runner invocationを実行する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-081の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-080`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.7. FR-082（SPLIT）

- 既存要件の設計情報を含む原文：idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する
- RDに残る能力／Legacy Trace：再送された同一依頼の重複処理を防止し、同じ識別子で異なる依頼が来た場合は拒否する
- Original Requirement：`FR-082`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.8. FR-084（SPLIT）

- 既存要件の設計情報を含む原文：上流Artifactを下流Stage inputへ型付きでbindingする
- RDに残る能力／Legacy Trace：依存処理の成果物を適切な形式で後続処理に引き渡せる
- Original Requirement：`FR-084`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.9. FR-086b（SPLIT）

- 既存要件の設計情報を含む原文：Stageごとのtimeout / operational resource limitをpersistent/configurable policyとして保持する
- RDに残る能力／Legacy Trace：処理ごとの時間・資源上限を設定できる
- Original Requirement：`FR-086b`; Status：`DEFERRED`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.10. FR-128a（MOVE_BD）

- 既存要件の設計情報を含む原文：Algorithm/Runnerをregistry/capabilityから解決・管理するcurrent contractを維持する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-035／NFR-005の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-128a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.11. NFR-003（SPLIT）

- 既存要件の設計情報を含む原文：Canonical JSONとhash生成はfield順やprocessに依存しない
- RDに残る能力／Legacy Trace：同一内容から環境に依存しない同一性識別値を生成できる
- Original Requirement：`NFR-003`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.12. NFR-005（SPLIT）

- 既存要件の設計情報を含む原文：新Analysis Familyを既存Executor変更なしにRegistry追加できる
- RDに残る能力／Legacy Trace：新しい分析領域を既存分析の挙動を壊さず追加できる
- Original Requirement：`NFR-005`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.13. NFR-006a（SPLIT）

- 既存要件の設計情報を含む原文：current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる
- RDに残る能力／Legacy Trace：中断・再送時にExecutionを安全に再開・再試行できる
- Original Requirement：`NFR-006a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

### 98.14. NFR-006b（SPLIT）

- 既存要件の設計情報を含む原文：retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない
- RDに残る能力／Legacy Trace：再試行・再起動で成功済み成果物の重複作成を防止する
- Original Requirement：`NFR-006b`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

## 22_05_family_exploratory.md

**Source blob:** `5e2d294a7c1a86667140489f1fa3253d2a31a5c2` — migrated constraints 5.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-029（SPLIT）

- 既存要件の設計情報を含む原文：Chart Specificationを保存し、同じDataset Versionで再実行できる
- RDに残る能力／Legacy Trace：可視化の条件を保存し同じデータ版で再実行できる
- Original Requirement：`FR-029`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-032（SPLIT）

- 既存要件の設計情報を含む原文：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- RDに残る能力／Legacy Trace：探索結果から因果・予測分析の草案を生成し由来を追跡できる。本人の確定・実行を必要とする
- Original Requirement：`FR-032`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-034（SPLIT）

- 既存要件の設計情報を含む原文：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- RDに残る能力／Legacy Trace：探索に用いたデータ選択・分析設定・実行環境および成果物の由来を再構成できる
- Original Requirement：`FR-034`; Status：`ACTIVE`; Implementation：`PARTIAL`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-147（SPLIT）

- 既存要件の設計情報を含む原文：Visualizationは各分析Stageの表現手段とし、独立Navigation Stageを設けない
- RDに残る能力／Legacy Trace：可視化は探索の各目的に即して利用できる
- Original Requirement：`FR-147`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-148（SPLIT）

- 既存要件の設計情報を含む原文：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
- RDに残る能力／Legacy Trace：探索上のFindingで既存の結果・注釈・来歴を利用できる
- Original Requirement：`FR-148`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

---

## 22_06_family_causal.md

**Source blob:** `ab1fd895bfa40357231fdcc7c792af2243855e16` — migrated constraints 3.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-043（SPLIT）

- 既存要件の設計情報を含む原文：Identificationは全reasonを収集後、確定的不整合をreview statusより優先してstatus決定する
- RDに残る能力／Legacy Trace：識別判断に確定的不整合がある場合はそれを明示し、レビュー待ちとして誤表示しない
- Original Requirement：`FR-043`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-045（MOVE_BD）

- 既存要件の設計情報を含む原文：Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-044の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-045`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-048（SPLIT）

- 既存要件の設計情報を含む原文：estimator/analysisに適用可能なoverlap、balance、weight、sample loss等のdiagnosticをResultとして保存する。全estimatorへ同一diagnostic setを強制しない
- RDに残る能力／Legacy Trace：推定手法に適合した診断を提示し、適用不能な診断を強制しない
- Original Requirement：`FR-048`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

---

## 22_07_family_predictive.md

**Source blob:** `3d6be1c484466ed77a1a32632c849fa2c03bfa89` — migrated constraints 15.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-059（SPLIT）

- 既存要件の設計情報を含む原文：target leakage、future leakage、group leakage、split overlapをBackendで拒否する
- RDに残る能力／Legacy Trace：目的変数・将来情報・同一GroupなどのLeakageを検出して不適切な評価を拒否する
- Original Requirement：`FR-059`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-061（SPLIT）

- 既存要件の設計情報を含む原文：Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる
- RDに残る能力／Legacy Trace：対象Taskと実行環境に適合するモデルと設定候補を選択できる
- Original Requirement：`FR-061`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-067（SPLIT）

- 既存要件の設計情報を含む原文：untouched TEST population上で指定subgroup columnごとのmetric、`sample_count`、計算可能な場合のbootstrap uncertaintyを確認できる
- RDに残る能力／Legacy Trace：指定Subgroupの評価指標・標本数と計算可能な不確実性を確認できる
- Original Requirement：`FR-067`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. FR-068（SPLIT）

- 既存要件の設計情報を含む原文：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- RDに残る能力／Legacy Trace：学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる
- Original Requirement：`FR-068`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.5. FR-069（SPLIT）

- 既存要件の設計情報を含む原文：explanation method capabilityが宣言するsupported scopeに従いglobal / local Predictive Explanationを生成でき、unsupported scopeを擬似出力で補完しない
- RDに残る能力／Legacy Trace：利用可能な範囲でモデル全体・個別予測の説明を生成でき、未対応の範囲を偽装しない
- Original Requirement：`FR-069`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.6. FR-150（SPLIT）

- 既存要件の設計情報を含む原文：既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する
- RDに残る能力／Legacy Trace：既存の予測機能・入力検証・保存済み仕様の意味を維持する
- Original Requirement：`FR-150`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.7. FR-151（SPLIT）

- 既存要件の設計情報を含む原文：MetricsとExplainabilityを異なる目的のNavigation Stageとして扱い、Predict Stage導入を理由に新規standalone scoring engineを必須化しない
- RDに残る能力／Legacy Trace：予測指標と予測説明の目的を区別して利用できる
- Original Requirement：`FR-151`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.8. FR-176（SPLIT）

- 既存要件の設計情報を含む原文：Predictive Navigation Stageを新しいbackend Execution modelまたは1:1 runtime Stageとして扱わず、既存Prediction Task → Split → Training → Evaluation → Explanation → Model Card semanticsを保持する
- RDに残る能力／Legacy Trace：既存の予測タスク設定・データ分割・学習・評価・説明・Model Cardの意味を維持し、Navigation変更で分析実行契約を変更しない
- Original Requirement：`FR-176`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.9. FR-178（SPLIT）

- 既存要件の設計情報を含む原文：Binary Classification / RegressionでLightGBM backend（`lightgbm_classifier.v1` / `lightgbm_regressor.v1`）をtask-compatible modelとして選択できる
- RDに残る能力／Legacy Trace：表形式分類・回帰で承認済み追加学習方式を選択して学習・評価できる
- Original Requirement：`FR-178`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.10. FR-180（SPLIT）

- 既存要件の設計情報を含む原文：fitted modelはserialize/load round-trip後もmodel/task/feature/preprocessor identityを保持し、同一runtime/config fixtureでprediction contractを満たす
- RDに残る能力／Legacy Trace：保存済み学習モデルを復元し、適合条件下で同等の予測を再実行できる
- Original Requirement：`FR-180`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.11. FR-181（SPLIT）

- 既存要件の設計情報を含む原文：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- RDに残る能力／Legacy Trace：利用可能なモデル説明方式を適合性に応じて選択し、予測への変数寄与を定量的に説明できる
- Original Requirement：`FR-181`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.12. FR-182（SPLIT）

- 既存要件の設計情報を含む原文：`SHAP_TREE`はapproved compatibility範囲でglobal/localを提供し、`LIME_TABULAR`はlocal-onlyを提供する。unsupported capabilityを別methodまたは擬似global出力で補完しない
- RDに残る能力／Legacy Trace：個別予測・モデル全体への説明の提供範囲を明示し、未対応の説明を擬似出力しない
- Original Requirement：`FR-182`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.13. FR-184（SPLIT）

- 既存要件の設計情報を含む原文：Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない
- RDに残る能力／Legacy Trace：利用可能な学習・説明機能と不可理由、設定条件、由来を一貫して表示する
- Original Requirement：`FR-184`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.14. FR-177（SPLIT）

- 既存要件の設計情報を含む原文：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RDに残る能力／Legacy Trace：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- Original Requirement：`FR-177`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.15. AR-016（SPLIT）

- 既存要件の設計情報を含む原文：subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない
- RDに残る能力／Legacy Trace：評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない
- Original Requirement：`AR-016`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

## 22_08_validation_architecture.md

**Source blob:** `bfd888fdf59bd5096caa447a783e2b3e8e26101e` — migrated constraints 4.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. FR-015（SPLIT）

- 既存要件の設計情報を含む原文：AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す
- RDに残る能力／Legacy Trace：データ型と演算子・値が適合しない分析条件は拒否され、理由を確認できる
- Original Requirement：`FR-015`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.2. FR-085（SPLIT）

- 既存要件の設計情報を含む原文：未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する
- RDに残る能力／Legacy Trace：計画の依存関係や必要な入力が不整合なら実行前に拒否する
- Original Requirement：`FR-085`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.3. FR-089（MOVE_BD）

- 既存要件の設計情報を含む原文：Generic validationとFamily-specific validationを分離して実行する
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】FR-085の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Original Requirement：`FR-089`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../95_rd04_fr_application_review.md)

### 98.4. AR-009（MOVE_BD）

- 既存要件の設計情報を含む原文：外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない
- RDに残る能力／Legacy Trace：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Original Requirement：`AR-009`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

## 22_09_results_artifacts_lineage.md

**Source blob:** `c8cdb8070856a231e16363ac7067d356e7071819` — migrated constraints 1.

## 98. RD-04：要件由来の基本設計制約

**Status:** `RD04_DESIGN_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。要件文の抽象化・設計移管で失われてはならない元の実現方式・責務境界を保持する。旧Requirement IDとStatusを維持する。コード検証やArchitecture GateのPASSを意味しない。

### 98.1. NFR-020a（SPLIT）

- 既存要件の設計情報を含む原文：Artifact storageを`ArtifactStore` Port abstraction越しに利用する
- RDに残る能力／Legacy Trace：成果物保存先を交換しても分析の振る舞いが維持される
- Original Requirement：`NFR-020a`; Status：`ACTIVE`; Implementation：`IMPLEMENTED`; [RD-04逐条台帳](../96_rd04_nfr_ar_application_review.md)

---

