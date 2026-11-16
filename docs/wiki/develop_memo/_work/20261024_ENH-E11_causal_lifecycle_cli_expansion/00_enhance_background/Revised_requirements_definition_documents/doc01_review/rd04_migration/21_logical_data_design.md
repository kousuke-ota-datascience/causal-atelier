# DOC-01 — 21論理データ設計：RD-04移管記録の履歴保全

**Kind:** FLOW/AUDIT, not a canonical LDD contract. **Source commit:** `eccd66163b281287dfb74296560c1bb914af392a`.

## 21_10_entity_project_context.md

**Source blob:** `642936b06c064ecbca29c7902bd28c6d4806cae4` — migrated constraints 4.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-002（SPLIT）

- 元要件（設計上の拘束を含む）：Projectはtopic、objective、memoを保持し、decision contextはversioned `ResearchContextVersion`の責務として保持する
- RD改訂後の要求：Projectの研究目的と意思決定文脈を区別して保持・参照できる
- Trace：`FR-002`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-006（SPLIT）

- 元要件（設計上の拘束を含む）：Analysis Specificationは一つのResearch Context Versionを参照する
- RD改訂後の要求：分析仕様が参照する研究文脈の版を特定できる
- Trace：`FR-006`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.3. FR-007（SPLIT）

- 元要件（設計上の拘束を含む）：Executionは参照ResearchContextVersionを固定し、受付時のobjective/rationale等の再現に必要なsnapshot metadata/hashを保持する。ResearchContext全体の重複保存を必須化しない
- RD改訂後の要求：分析実行時点の研究目的と理由を後から再現できる
- Trace：`FR-007`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.4. FR-008（REWRITE_RD）

- 元要件（設計上の拘束を含む）：ResearchContextVersionから利用AnalysisSpecification、Execution、Resultへcanonical lineage/read modelで遡及・追跡できる
- RD改訂後の要求：研究文脈から分析仕様・実行・結果までの来歴を追跡できる
- Trace：`FR-008`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_11_entity_dataset_view.md

**Source blob:** `107040447ea9fcbdf30cb94a1a47c2364f87d835` — migrated constraints 2.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-011（SPLIT）

- 元要件（設計上の拘束を含む）：DatasetVersionにcontent hash、schema、row count、column countおよびcurrent profile summaryを保持する。登録時の独立full profile生成を必須化しない
- RD改訂後の要求：各データ版の同一性・構造・規模・品質概要を確認できる
- Trace：`FR-011`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-020（SPLIT）

- 元要件（設計上の拘束を含む）：Explore stateのdata-selection semantics（row_filter、selected_columns、derived_columns、missing_value_policy、time_cutoff、sampling）からAnalysisView DRAFTを作成できる。presentation-only chart stateはAnalysisViewへ保存しない
- RD改訂後の要求：探索中に選択したデータ条件をAnalysis Viewの草案として作成できる
- Trace：`FR-020`; Status=`ACTIVE`; Implementation=`NOT_IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_12_entity_specification_graph.md

**Source blob:** `a438b5682d8019dca03b2f44c35f045fcf905387` — migrated constraints 3.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-045（MOVE_BD）

- 元要件（設計上の拘束を含む）：Treatment / Outcome inferred typeを正規化文字列で保存し、外部型objectを永続化しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】FR-044の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-045`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-051（SPLIT）

- 元要件（設計上の拘束を含む）：同一immutable `dataset_version_id`の先行Exploratory Resultを用いたconfirmatory分析では`EXPLORATORY_REUSE_SAME_DATA` warningとevidence Result IDを保持する
- RD改訂後の要求：同一データを探索と確認的分析で再利用する場合、その事実と根拠を警告できる
- Trace：`FR-051`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.3. FR-054（SPLIT）

- 元要件（設計上の拘束を含む）：Causal ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion/AnalysisView、GraphVersion、上流Result、Artifactへcanonical lineageで遡れる
- RD改訂後の要求：因果分析結果から入力データ・仮定・実行・成果物の来歴を追跡できる
- Trace：`FR-054`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_13_entity_execution.md

**Source blob:** `c4372cbddb27415da1f76f2981c7ede106a60934` — migrated constraints 6.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-076（SPLIT）

- 元要件（設計上の拘束を含む）：Plannerはversionedで不変なExecution Planを生成する
- RD改訂後の要求：分析の実行計画を版管理し、実行時の条件を後から復元できる
- Trace：`FR-076`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-077（MOVE_BD）

- 元要件（設計上の拘束を含む）：Stage Typeをnamespace、name、versionで識別する
- RD改訂後の要求：【設計制約移管・Legacy Trace】FR-076の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-077`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.3. FR-078（SPLIT）

- 元要件（設計上の拘束を含む）：PlanはStage dependencyとinput/output bindingをDAGとして保持する
- RD改訂後の要求：分析処理の依存順序と処理間の入力・出力の対応を追跡できる
- Trace：`FR-078`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.4. FR-082（SPLIT）

- 元要件（設計上の拘束を含む）：idempotency対象Commandでは`(project_id, command_scope, idempotency_key)`をauthorityとし、同一semantic requestをreplay、異なるrequestを`IDEMPOTENCY_CONFLICT`で拒否する
- RD改訂後の要求：再送された同一依頼の重複処理を防止し、同じ識別子で異なる依頼が来た場合は拒否する
- Trace：`FR-082`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.5. FR-086a（SPLIT）

- 元要件（設計上の拘束を含む）：stochastic Stageのactual effective random seedを`StageAttempt.effective_random_seed`へ保存し、同一logical Stageのretryで同じseedを再利用する
- RD改訂後の要求：確率的処理を再試行しても同じ実効乱数条件を再現できる
- Trace：`FR-086a`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.6. FR-087b（SPLIT）

- 元要件（設計上の拘束を含む）：Execution `runtime_version_json`にAriadne code、Python、platform、machineおよび実際に利用したscientific library versionを保持する
- RD改訂後の要求：分析の再現に必要な実行環境と科学ライブラリの版を確認できる
- Trace：`FR-087b`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_14_entity_result_artifact_lineage.md

**Source blob:** `28755b476c2dca2f1cd49e1a33bccd7e569f0c2c` — migrated constraints 5.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-090（SPLIT）

- 元要件（設計上の拘束を含む）：canonical Resultはexecution/stage relation、result type、scientific status、summary/payload/diagnostics/warningsを保持する。family/generic schema_versionをResult direct fieldへ重複保持しない
- RD改訂後の要求：分析結果について実行・科学的状態・診断・警告を一貫して参照できる
- Trace：`FR-090`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-091（SPLIT）

- 元要件（設計上の拘束を含む）：Result payloadはFamily・Type別Schemaで検証する
- RD改訂後の要求：結果の種類に適合した検証を行い不正な結果を受け入れない
- Trace：`FR-091`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.3. FR-092（SPLIT）

- 元要件（設計上の拘束を含む）：canonical Artifactはproject/execution/stage/result relation、artifact type/scope、object_key、media type、hash、size、metadataを保持する。family/generic schema_versionをdirect fieldへ重複保持しない
- RD改訂後の要求：成果物について帰属先・種類・同一性・取得情報を追跡できる
- Trace：`FR-092`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.4. FR-095（SPLIT）

- 元要件（設計上の拘束を含む）：ResultからResearchContextVersion、AnalysisSpecification、ExecutionPlan、Execution、StageExecution、DatasetVersion、AnalysisView、GraphVersion、input Result、base Execution、Artifactへ遡れるcanonical lineage read modelを提供する
- RD改訂後の要求：結果に影響した研究条件・データ・実行・上流結果・成果物を追跡できる
- Trace：`FR-095`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.5. NFR-002（SPLIT）

- 元要件（設計上の拘束を含む）：canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する
- RD改訂後の要求：研究条件から入力・計画・実行・結果・成果物までの追跡が可能である
- Trace：`NFR-002`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

---

## 21_21_value_navigation_context.md

**Source blob:** `283636d7a3e1d187ca4b1a8923729d0738981002` — migrated constraints 2.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-148（SPLIT）

- 元要件（設計上の拘束を含む）：Findingsは既存Result / Annotation / Lineageを利用可能とし、新規persistent Finding resourceを必須化しない
- RD改訂後の要求：探索上のFindingで既存の結果・注釈・来歴を利用できる
- Trace：`FR-148`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-177（SPLIT）

- 元要件（設計上の拘束を含む）：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RD改訂後の要求：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- Trace：`FR-177`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_22_value_analysis_specifications.md

**Source blob:** `dd0d963873b301d5be3584091c05036c13659759` — migrated constraints 9.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. FR-029（SPLIT）

- 元要件（設計上の拘束を含む）：Chart Specificationを保存し、同じDataset Versionで再実行できる
- RD改訂後の要求：可視化の条件を保存し同じデータ版で再実行できる
- Trace：`FR-029`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.2. FR-032（SPLIT）

- 元要件（設計上の拘束を含む）：Exploratory Resultからcanonical Causal/Predictive `AnalysisSpecification`をDRAFTとしてpersistし、source Resultとの`MOTIVATED` relationを保持できる。auto FIX / auto executionは行わない
- RD改訂後の要求：探索結果から因果・予測分析の草案を生成し由来を追跡できる。本人の確定・実行を必要とする
- Trace：`FR-032`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.3. FR-034（SPLIT）

- 元要件（設計上の拘束を含む）：Exploratory provenanceとしてdata-selection semantics、analysis-significant family_spec、sampling、Execution code/runtime metadataおよびResult/Artifact lineageを再構成できる
- RD改訂後の要求：探索に用いたデータ選択・分析設定・実行環境および成果物の由来を再構成できる
- Trace：`FR-034`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.4. FR-068（SPLIT）

- 元要件（設計上の拘束を含む）：fitted model、fitted preprocessor、prediction等のdurable outputをArtifactとして保存し、provider-specific fitted modelはartifact schema/provider/payload identityから対応loaderを一意に解決してfresh-process相当で再読込・predictionできる
- RD改訂後の要求：学習済みモデルと前処理を保存し、適合する環境で復元して再予測できる
- Trace：`FR-068`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.5. FR-071（SPLIT）

- 元要件（設計上の拘束を含む）：intended use、training data、metric、limitationsに加え、model/provider/version、effective parameters、seed/deterministic settings、feature/preprocessor identity、explanation method等の再現性provenanceをModel Cardへ記録する
- RD改訂後の要求：学習・評価・説明の根拠、限界、再現性情報をModel Cardで確認できる
- Trace：`FR-071`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.6. FR-183（SPLIT）

- 元要件（設計上の拘束を含む）：explanation Result/Artifactはmethod/model/provider、feature/sample identity、model/prediction output scale、background/reference、effective seed/parameters、library version等のprovenanceを保持する
- RD改訂後の要求：予測説明のモデル・入力・出力尺度・計算条件を追跡し再現できる
- Trace：`FR-183`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.7. FR-157（MOVE_BD）

- 元要件（設計上の拘束を含む）：既存`AnalysisSpecification.analysis_family`をFamily discriminatorとして再利用し、duplicate Family field/enumを追加しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】FR-074の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-157`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.8. FR-158（MOVE_BD）

- 元要件（設計上の拘束を含む）：AnalysisSpecification / ExecutionPlan / Execution / StageExecutionへNavigation Stage fieldを追加しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】NFR-021の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-158`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

### 98.9. FR-160（MOVE_BD）

- 元要件（設計上の拘束を含む）：Family / Navigation / application IAの変更だけを理由にDB schema migrationまたはnavigation-state persistenceを導入しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】NFR-021／FR-177の実現に係る既存設計制約。具体的な実装契約は下位設計とRD-04移管台帳で管理し、元ID・MUST・Statusの追跡を維持する
- Trace：`FR-160`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/95_rd04_fr_application_review.md)

---

## 21_23_value_execution_snapshot.md

**Source blob:** `1c27b9bb41e830e3cbef39c4e27b0bac01fc6190` — migrated constraints 3.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. NFR-001b（SPLIT）

- 元要件（設計上の拘束を含む）：actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する
- RD改訂後の要求：解析結果を再現するため実効ライブラリ版・乱数条件を取得できる
- Trace：`NFR-001b`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

### 98.2. NFR-013（SPLIT）

- 元要件（設計上の拘束を含む）：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- RD改訂後の要求：変化するデータ契約を識別し後方互換を制御できる
- Trace：`NFR-013`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

### 98.3. AR-019（SPLIT）

- 元要件（設計上の拘束を含む）：random seedだけでなくsplit indexまたはpartition artifactを保存する
- RD改訂後の要求：分析のデータ分割を再現可能な情報として保持しなければならない
- Trace：`AR-019`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

---

## 21_40_integrity_constraints.md

**Source blob:** `d5824a62a519543dd04b4971d55ab7850f63bcdd` — migrated constraints 1.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. NFR-011a（SPLIT）

- 元要件（設計上の拘束を含む）：current request/execution/stage correlation identifiersをlogへ出力する
- RD改訂後の要求：Request・実行・処理単位をまたいで障害を追跡できる
- Trace：`NFR-011a`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

---

## 21_41_scientific_data_constraints.md

**Source blob:** `b97e6c4add41691fac09a5d1100f9afd6c2801bc` — migrated constraints 3.

## 98. RD-04：要求の論理データ制約の受入・Trace

**Status:** `DESIGN_CONSTRAINT_MIGRATION / OWNER_CONTENT_REVIEW_PENDING`。以下はRD-04で抽象化した元要件のうち、データ定義・同一性・来歴・正本性に関係する条項を論理設計側に残したもの。原文は出典保証目的で保持する。現行コードで検証済みと主張しない。

### 98.1. AR-004（SPLIT）

- 元要件（設計上の拘束を含む）：同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する
- RD改訂後の要求：同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない
- Trace：`AR-004`; Status=`ACTIVE`; Implementation=`PARTIAL`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

### 98.2. AR-008（SPLIT）

- 元要件（設計上の拘束を含む）：Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する
- RD改訂後の要求：推定に必要な変数型が適格かを識別できなければならない
- Trace：`AR-008`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

### 98.3. AR-009（MOVE_BD）

- 元要件（設計上の拘束を含む）：外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない
- RD改訂後の要求：【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する
- Trace：`AR-009`; Status=`ACTIVE`; Implementation=`IMPLEMENTED`; [逐条レビュー](../rd04_review/96_rd04_nfr_ar_application_review.md)

---

