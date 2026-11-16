# DOC-01 — 23 Interface設計：RD-04移管原記録

**Kind:** FLOW/AUDIT; design/IF contracts remain in the stock Interface files. **Source HEAD:** `823648335af2224c377dafd5c053ba99bca43027`.

## 23_01_common_conventions.md

**Source blob:** `f3fc65130d202603374dc8e677cd4cbae764288d`; constraints 2.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-120a（SPLIT）

- 旧要件に含まれるIF固有情報：runtime API schemaから生成されるFastAPI OpenAPIをcurrent API contractとして提供する
- RDの要求核／Legacy Trace：APIの機械可読な仕様を提供し実際の動作と一致させる
- `FR-120a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-120b（SPLIT）

- 旧要件に含まれるIF固有情報：canonical schema exampleとOpenAPI/exampleをsystematically同期・検証する
- RDの要求核／Legacy Trace：API仕様と公開する入出力例との整合性を検証できる
- `FR-120b`；Status=`DEFERRED`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_10_api_project_context.md

**Source blob:** `1d785b8392d3f1893cc0ced04f56cd945a6a9178`; constraints 1.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-121（SPLIT）

- 旧要件に含まれるIF固有情報：全project-scoped routeでpersisted ProjectMembership role（OWNER/EDITOR/VIEWER）に基づくauthorizationをservice action前に検証する
- RDの要求核／Legacy Trace：Project内操作を所属Roleに応じて認可し権限外の処理を防止する
- `FR-121`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_11_api_dataset_view.md

**Source blob:** `f900639f54c176a1b82a5b0cadb550771cc2d3f8`; constraints 1.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-015（SPLIT）

- 旧要件に含まれるIF固有情報：AnalysisViewのsource Dataset logical type × operator × value compatibilityをdomain/application validationで検証し、type mismatchを`FILTER_TYPE_MISMATCH`として返す
- RDの要求核／Legacy Trace：データ型と演算子・値が適合しない分析条件は拒否され、理由を確認できる
- `FR-015`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_14_api_causal.md

**Source blob:** `2e404518869f896e8fafb1a640423cfa6c49a40e`; constraints 2.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-051（SPLIT）

- 旧要件に含まれるIF固有情報：同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する
- RDの要求核／Legacy Trace：同一データを探索と確認的分析で再利用する場合、その事実と根拠を警告できる
- `FR-051`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. AR-004（SPLIT）

- 旧要件に含まれるIF固有情報：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する
- RDの要求核／Legacy Trace：同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない
- `AR-004`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

---

## 23_15_api_predictive.md

**Source blob:** `a5404cd44bd114b8e3700d36e35c7f431a2f1e4b`; constraints 5.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-061（SPLIT）

- 旧要件に含まれるIF固有情報：Algorithm Registryはtask compatibilityに加えてmodel capability、parameter schema/default、provider/optional dependency availability/versionを表現し、利用可能なtask-compatible modelをbackend authorityで選択できる
- RDの要求核／Legacy Trace：対象Taskと実行環境に適合するモデルと設定候補を選択できる
- `FR-061`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-071（SPLIT）

- 旧要件に含まれるIF固有情報：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- RDの要求核／Legacy Trace：学習・評価・説明の根拠、限界、再現性情報をModel Cardで確認できる
- `FR-071`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-181（SPLIT）

- 旧要件に含まれるIF固有情報：Predictive Explanationはmodel-method compatibilityをbackend authorityで検証し、`LINEAR_COEFFICIENT_CONTRIBUTION` / `SHAP_TREE` / `LIME_TABULAR`を明示methodとして解決する
- RDの要求核／Legacy Trace：利用可能なモデル説明方式を適合性に応じて選択し、予測への変数寄与を定量的に説明できる
- `FR-181`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-183（SPLIT）

- 旧要件に含まれるIF固有情報：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- RDの要求核／Legacy Trace：予測説明のモデル・入力・出力尺度・計算条件を追跡し再現できる
- `FR-183`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.5. FR-184（SPLIT）

- 旧要件に含まれるIF固有情報：Train / Explainability / Model Managementはbackend capability metadataからcompatible option、availability/reason、parameter definition、provenanceを表示し、Frontendを独立したmodel-method compatibility authorityにしない
- RDの要求核／Legacy Trace：利用可能な学習・説明機能と不可理由、設定条件、由来を一貫して表示する
- `FR-184`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_16_api_execution.md

**Source blob:** `76f5d2c6fc9020216e4fce2fbf4a4525d3eacb27`; constraints 4.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-082（SPLIT）

- 旧要件に含まれるIF固有情報：idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する
- RDの要求核／Legacy Trace：再送された同一依頼の重複処理を防止し、同じ識別子で異なる依頼が来た場合は拒否する
- `FR-082`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-084（SPLIT）

- 旧要件に含まれるIF固有情報：上流Artifactを下流Stage inputへ型付きでbindingする
- RDの要求核／Legacy Trace：依存処理の成果物を適切な形式で後続処理に引き渡せる
- `FR-084`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-085（SPLIT）

- 旧要件に含まれるIF固有情報：未登録Runner、cycle、missing output、schema mismatchをPlan受付時に拒否する
- RDの要求核／Legacy Trace：計画の依存関係や必要な入力が不整合なら実行前に拒否する
- `FR-085`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-087b（SPLIT）

- 旧要件に含まれるIF固有情報：Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する
- RDの要求核／Legacy Trace：分析の再現に必要な実行環境と科学ライブラリの版を確認できる
- `FR-087b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_17_api_result_comparison_lineage.md

**Source blob:** `7a9862aeb805fdf4fe8c3ae3345ac8d1aa4c3f48`; constraints 4.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-090（SPLIT）

- 旧要件に含まれるIF固有情報：canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない
- RDの要求核／Legacy Trace：分析結果について実行・科学的状態・診断・警告を一貫して参照できる
- `FR-090`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-091（SPLIT）

- 旧要件に含まれるIF固有情報：Result payloadはFamily・Type別Schemaで検証する
- RDの要求核／Legacy Trace：結果の種類に適合した検証を行い不正な結果を受け入れない
- `FR-091`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-092（SPLIT）

- 旧要件に含まれるIF固有情報：canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない
- RDの要求核／Legacy Trace：成果物について帰属先・種類・同一性・取得情報を追跡できる
- `FR-092`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-099（SPLIT）

- 旧要件に含まれるIF固有情報：Manifest、Result summary、Specification、Artifact参照をexportできる
- RDの要求核／Legacy Trace：分析条件・結果要約・成果物参照を外部へ出力できる
- `FR-099`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_18_api_annotation_artifact.md

**Source blob:** `eebd9d84784bab96a4fc0b1e88cb965826defb2a`; constraints 3.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-124a（SPLIT）

- 旧要件に含まれるIF固有情報：Artifact metadata/downloadでProject境界とsafe content dispositionを検証するcurrent contractを維持する
- RDの要求核／Legacy Trace：成果物の情報・取得をProject境界内で安全に利用できる
- `FR-124a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-124b（SPLIT）

- 旧要件に含まれるIF固有情報：legacy/generic routeを含むArtifact downloadでProjectMembership authorizationを一貫適用する
- RDの要求核／Legacy Trace：旧経路を含む成果物取得に同じProject権限を適用する
- `FR-124b`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. AR-020（SPLIT）

- 旧要件に含まれるIF固有情報：prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する
- RDの要求核／Legacy Trace：個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する
- `AR-020`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

---

## 23_20_browser_navigation.md

**Source blob:** `7d74a93ebc1a1a1bfe96f25b7a0bf29398a480a2`; constraints 14.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-175（SPLIT）

- 旧要件に含まれるIF固有情報：Data Qualityはdedicated backend operationを新設せずread-only availabilityとして扱い、Comparisonの`TIME_TREND`は既存grouping/aggregation semanticsを維持し、Findingsの`CHART`は既存persistent operation/result/artifact semanticsを維持する
- RDの要求核／Legacy Trace：探索のデータ品質・時間推移・Findingを既存意味で利用できる
- `FR-175`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-150（SPLIT）

- 旧要件に含まれるIF固有情報：既存Predictive UIの設定項目、validation、generated `predictive-analysis-spec/1` semanticsを全量保持する
- RDの要求核／Legacy Trace：既存の予測機能・入力検証・保存済み仕様の意味を維持する
- `FR-150`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. FR-107（SPLIT）

- 旧要件に含まれるIF固有情報：操作可否をBackend authoritative state/authorizationから導出し、`allowed / reason_code / message`としてpresentationへ返す
- RDの要求核／Legacy Trace：操作の可否と不可理由を一貫した権限・状態に基づいて表示できる
- `FR-107`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.4. FR-108（SPLIT）

- 旧要件に含まれるIF固有情報：AnalysisSpecification、Execution、Result、GraphVersionへFamily/Navigation Stage contextを保持したdeep routeで直接遷移できる
- RDの要求核／Legacy Trace：分析仕様・実行・結果・Graphへ文脈を保持して直接移動できる
- `FR-108`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.5. FR-130（SPLIT）

- 旧要件に含まれるIF固有情報：Current Familyをactive stateとcanonical route `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`の双方で一意に識別できる
- RDの要求核／Legacy Trace：現在の分析Familyと画面位置を識別・復元できる
- `FR-130`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.6. FR-133（MOVE_BD）

- 旧要件に含まれるIF固有情報：FamilyごとにCapability-owned immutable descriptorでStage ID、slug、label、order、default Stageを独立定義する
- RDの要求核／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-133`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.7. FR-136（SPLIT）

- 旧要件に含まれるIF固有情報：canonical URL `/projects/{project_id}/analysis/{family_slug}/{stage_slug}`からProject、Family、Navigation Stageを復元できる
- RDの要求核／Legacy Trace：分析ページのURLから対象Project・Family・画面位置を復元できる
- `FR-136`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.8. FR-144（MOVE_BD）

- 旧要件に含まれるIF固有情報：concrete Navigation Stage catalogは各Family-specific Capabilityが所有し、application/interface aggregatorがread-only metadataとして集約する
- RDの要求核／Legacy Trace：【設計制約移管・Legacy Trace】FR-131の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- `FR-144`；Status=`ACTIVE`；Implementation=`PARTIAL`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.9. FR-159（SPLIT）

- 旧要件に含まれるIF固有情報：supported legacy analytical entryはFamily Capability catalogで解決したcanonical Analysis routeへ一方向normalizeし、parallel navigation authorityとして維持しない
- RDの要求核／Legacy Trace：旧分析画面から正規の分析画面へ一意に遷移できる
- `FR-159`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.10. FR-163（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects`をProject Listのcanonical surfaceとする
- RDの要求核／Legacy Trace：Project一覧へ一意の正規画面からアクセスできる
- `FR-163`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.11. FR-164（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects/new`をProject Registerのcanonical surfaceとし、作成成功後は`/projects/{new_project_id}/overview`へ遷移する
- RDの要求核／Legacy Trace：Project作成後に対象Projectの概要画面へ遷移できる
- `FR-164`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.12. FR-165（SPLIT）

- 旧要件に含まれるIF固有情報：`/projects/{project_id}/overview`をselected Projectのdefault canonical surfaceとし、`/projects/{project_id}`はhistory-replaceでoverviewへnormalizeする
- RDの要求核／Legacy Trace：対象Projectの標準表示画面を一意に復元できる
- `FR-165`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.13. FR-171（SPLIT）

- 旧要件に含まれるIF固有情報：Current Projectはcanonical Analysis URLの`project_id`をauthorityとしAnalysis Workspace内ではread-onlyとする。Project変更はProject Management経由で行う
- RDの要求核／Legacy Trace：分析画面で選択Projectを確認でき、Project変更は管理機能で実施できる
- `FR-171`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.14. AR-024（SPLIT）

- 旧要件に含まれるIF固有情報：Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない
- RDの要求核／Legacy Trace：因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる
- `AR-024`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

---

## 23_50_error_contract.md

**Source blob:** `200aa94d7cc593eee7b9be16883f25128df5944c`; constraints 3.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-115（SPLIT）

- 旧要件に含まれるIF固有情報：validation、conflict、not found、forbidden、execution failureをcanonical errorで返す
- RDの要求核／Legacy Trace：利用側が入力不正・競合・不在・権限不足・処理失敗を判別できる
- `FR-115`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. NFR-028（SPLIT）

- 旧要件に含まれるIF固有情報：optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する
- RDの要求核／Legacy Trace：任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる
- `NFR-028`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.3. AR-008（SPLIT）

- 旧要件に含まれるIF固有情報：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
- RDの要求核／Legacy Trace：推定に必要な変数型が適格かを識別できなければならない
- `AR-008`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

---

## 23_51_idempotency_contract.md

**Source blob:** `b74b50de64182bc6b6023ff8913f6afe2182093e`; constraints 2.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-114a（SPLIT）

- 旧要件に含まれるIF固有情報：Idempotency要否をHTTP method/create一般ではなく、retryでduplicate durable side effectを生成し得るCommandかどうかで判定する
- RDの要求核／Legacy Trace：重複する永続的副作用を生む操作の再試行を安全に処理する
- `FR-114a`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-114b（SPLIT）

- 旧要件に含まれるIF固有情報：対象Commandで`Idempotency-Key`を必須化し、missing keyを`IDEMPOTENCY_KEY_REQUIRED`、same key/different requestをHTTP 409 `IDEMPOTENCY_CONFLICT`として扱う
- RDの要求核／Legacy Trace：重複要求と競合要求を識別し、誤った二重処理を防止する
- `FR-114b`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

---

## 23_52_versioning_compatibility.md

**Source blob:** `ed8f205cce38dd86a5ad7423ac2939def28e923b`; constraints 4.

## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-177（SPLIT）

- 旧要件に含まれるIF固有情報：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RDの要求核／Legacy Trace：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- `FR-177`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-113（SPLIT）

- 旧要件に含まれるIF固有情報：HTTP APIをversioned pathとversioned payloadで提供する
- RDの要求核／Legacy Trace：互換性を管理した版付きAPIを提供できる
- `FR-113`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. NFR-013（SPLIT）

- 旧要件に含まれるIF固有情報：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- RDの要求核／Legacy Trace：変化するデータ契約を識別し後方互換を制御できる
- `NFR-013`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.4. NFR-014（SPLIT）

- 旧要件に含まれるIF固有情報：`causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ
- RDの要求核／Legacy Trace：既存v2の因果分析仕様と保存済み結果を継続して読み取れる
- `NFR-014`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

---

