# RD-04 — NFR36 and Scientific AR27 application review

**2026-11-16; State:** `APPLIED_TO_E11_WORKING_COPY / OWNER_CONTENT_CONFIRMATION_PENDING`. ID/Status/Deliveryは元の正本に一致し、E11追加NFR8・AR17の条文は変更しない。

## 1. Result

- KEEP_RD: 29
- SPLIT: 27
- MOVE_BD: 3
- REWRITE_RD: 4
- Original NFR+AR: 63; New E11: 8 NFR + 17 scientific AR (unchanged).
- RD-01再審査: `AR-021`と`AR-024`は単純な設計事項ではなく科学的解釈・ユーザー可観測な分離要求も含むので`MOVE_BD`→`SPLIT`。`AR-016`は不確実性の適格性要件を厳密化し、既存の定量的条件をMethod/Acceptance契約へ残す。
- `AR`は既存科学要件。E11-A（Architecture草案）を科学ARへ混入しない。

## 2. Applied clause revisions (34)

| ID | Disposition | Original requirement | Revised requirement / legacy trace | Design destinations | Reason | Status | Implementation Status |
|---|---|---|---|---|---|---|---|
| NFR-001b | SPLIT | actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する | 解析結果を再現するため実効ライブラリ版・乱数条件を取得できる | 21 LDD・30 DD | StageAttempt fieldなどの保存手法 | ACTIVE | PARTIAL |
| NFR-002 | SPLIT | canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する | 研究条件から入力・計画・実行・結果・成果物までの追跡が可能である | 21 LDD | canonical read modelの具体的構造 | ACTIVE | PARTIAL |
| NFR-003 | SPLIT | Canonical JSONとhash生成はfield順やprocessに依存しない | 同一内容から環境に依存しない同一性識別値を生成できる | 22 BD・30 DD | canonical JSON・hash処理詳細 | ACTIVE | IMPLEMENTED |
| NFR-013 | SPLIT | schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない | 変化するデータ契約を識別し後方互換を制御できる | 21 LDD・23 IF | schema_version fieldの物理配置禁止 | ACTIVE | IMPLEMENTED |
| NFR-019 | REWRITE_RD | `00/10/21/22/23/30`だけでcurrent product concept / requirement / logical model / design / interface contractを自己完結して理解できる | 現行Productの要件・データ・設計・Interface契約を整合した正式資料で追跡・理解できる | — | 文書番号の固定を避ける | ACTIVE | IMPLEMENTED |
| NFR-005 | SPLIT | 新Analysis Familyを既存Executor変更なしにRegistry追加できる | 新しい分析領域を既存分析の挙動を壊さず追加できる | 22 BD・30 DD | RegistryとExecutor非変更の具体方式 | ACTIVE | IMPLEMENTED |
| NFR-006a | SPLIT | current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる | 中断・再送時にExecutionを安全に再開・再試行できる | 22 BD・30 DD | claim/lease方式 | ACTIVE | IMPLEMENTED |
| NFR-006b | SPLIT | retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない | 再試行・再起動で成功済み成果物の重複作成を防止する | 22 BD・30 DD | exactly-onceを約束しない技術的限界は明記 | ACTIVE | PARTIAL |
| NFR-007 | SPLIT | Metadata transactionとArtifact writeのcross-store failure compensationを定義する | 成果物と管理情報の不整合が発生した場合、安全に回復・検知できる | 22 BD・30 DD | cross-store compensation手順 | DEFERRED | PARTIAL |
| NFR-010a | SPLIT | API processとWorker processを分離するcurrent deployment boundaryを維持する | 分析実行の負荷がAPIの応答性・稼働に不必要な影響を与えない | 22 BD | API/Worker process分離という配置制約 | ACTIVE | IMPLEMENTED |
| NFR-010b | SPLIT | Worker restart後の明示的resume/recovery semanticsを定義する | 実行基盤の再起動後に処理状態を復元・回復できる | 22 BD・30 DD | Worker resume契約 | DEFERRED | PARTIAL |
| NFR-011a | SPLIT | current request/execution/stage correlation identifiersをlogへ出力する | Request・実行・処理単位をまたいで障害を追跡できる | 21 LDD・30 DD | correlation IDの形式とlog出力 | ACTIVE | IMPLEMENTED |
| NFR-015 | SPLIT | Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる | Domain・実行・API・UI・科学計算を個別に検証できる | 22 BD・30 DD | Planner/Runner等の試験境界 | ACTIVE | IMPLEMENTED |
| NFR-020a | SPLIT | Artifact storageを`ArtifactStore` Port abstraction越しに利用する | 成果物保存先を交換しても分析の振る舞いが維持される | 22 BD・30 DD | ArtifactStore Portという具体方式 | ACTIVE | IMPLEMENTED |
| NFR-021 | SPLIT | Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない | 画面ナビゲーションの変更が分析実行ライフサイクルに影響しない | 22 BD | Navigation依存分離の方式 | ACTIVE | IMPLEMENTED |
| NFR-023 | SPLIT | Family-specific Navigation Stage catalogをCapability ownershipで局所化する | Familyごとの画面構成を他Familyへの影響を抑えて変更できる | 22 BD | Capability-owned catalogの構成 | ACTIVE | NOT_IMPLEMENTED |
| NFR-024 | SPLIT | Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる | 画面構成・URL復元・表示・分析実行独立性を個別に検証できる | 22 BD・30 DD | 具体的単体/E2E試験階層 | ACTIVE | IMPLEMENTED |
| NFR-025 | SPLIT | CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない | CLIやライブラリ実行を画面状態なしで行える | 22 BD・30 DD | NavigationStageDescriptorの禁止依存 | ACTIVE | IMPLEMENTED |
| NFR-027 | REWRITE_RD | navigation metadata取得・renderingがanalysis executionのcritical pathへ不要なI/Oまたはblocking dependencyを追加しない | 画面構成情報の取得・表示によって分析処理の性能を不要に低下させない | — | critical pathの実装表現を一般化 | ACTIVE | IMPLEMENTED |
| NFR-008a | SPLIT | current input validation、path traversal防止、secret非露出等のsafeguardを維持する | 入力検証と危険なパス・秘密情報の保護を維持する | 22 BD・30 DD | 具体的safeguard実装 | ACTIVE | IMPLEMENTED |
| NFR-014 | SPLIT | `causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ | 既存v2の因果分析仕様と保存済み結果を継続して読み取れる | 23 IF・22 BD | causal-analysis-spec/2は互換契約として保持 | ACTIVE | IMPLEMENTED |
| NFR-018 | MOVE_BD | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | 【設計制約移管・Legacy Trace】NFR-005に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | 22 BD・30 DD | Product DomainのFramework/ORM import禁止 | ACTIVE | IMPLEMENTED |
| NFR-028 | SPLIT | optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する | 任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる | 22 BD・23 IF | import/availability失敗の処理位置 | ACTIVE | IMPLEMENTED |
| AR-004 | SPLIT | 同一immutable `dataset_version_id`を探索とconfirmatory analysisで再利用した場合、`EXPLORATORY_REUSE_SAME_DATA` warningとlineage evidenceを保持する | 同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない | 21 LDD・23 IF | 固有warning codeとdataset ID | ACTIVE | PARTIAL |
| AR-016 | SPLIT | subgroup metricは`sample_count`を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない | 評価Subgroupの標本数と不確実性を明示し、標本条件・推論方法が不適切な場合は計算不能理由を示して未検証区間を生成しない | 10_32 Method Scope・22 BD・30 DD | 元の95%/bootstrap回数など採用済み数値受入条件はMethod契約に残す | ACTIVE | IMPLEMENTED |
| AR-019 | SPLIT | random seedだけでなくsplit indexまたはpartition artifactを保存する | 分析のデータ分割を再現可能な情報として保持しなければならない | 21 LDD・30 DD | index/partition Artifactの保存方式 | ACTIVE | IMPLEMENTED |
| AR-020 | SPLIT | prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する | 個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する | 22 BD・23 IF | 権限制御の具体位置 | ACTIVE | PARTIAL |
| AR-021 | SPLIT | Navigation Stageの表示順を分析上必須の実行順序として解釈しない | Navigation Stageの表示順を、因果分析その他の科学的な実行順序や必須解析手順として解釈させない | 22 BD | 画面ナビゲーション順から科学的妥当性を誤推論しない義務はRDに残す | ACTIVE | IMPLEMENTED |
| AR-022 | MOVE_BD | Family間でStage数・名称を揃えることを科学的workflow要件としない | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | 22 BD | IAの実装制約 | ACTIVE | IMPLEMENTED |
| AR-027 | REWRITE_RD | coefficient contribution / SHAP / LIMEはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない | 予測モデルの説明値はモデルの挙動に関するものであり、変数の因果的重要性・介入効果・因果機構を示さない | 10_32 Method Scope | SHAP/LIMEの名称を要件一般文から除外 | ACTIVE | IMPLEMENTED |
| AR-006 | REWRITE_RD | Identification statusは全reasonを収集後に決定する | 因果識別の成否は全ての不適格理由と不確実性を考慮して決定しなければならない | 10_31 AR | status優先順位の詳細は科学契約 | ACTIVE | IMPLEMENTED |
| AR-008 | SPLIT | Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する | 推定に必要な変数型が適格かを識別できなければならない | 21 LDD・23 IF | BINARY等の保存enum具体値 | ACTIVE | IMPLEMENTED |
| AR-009 | MOVE_BD | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | 【設計制約移管・Legacy Trace】対応する既存上位要件に係る既存設計制約。具体的な実装契約は下位設計へ移し、元ID・Status・科学的制約の追跡を維持する | 21 LDD・22 BD | 外部型objectの永続化禁止 | ACTIVE | IMPLEMENTED |
| AR-024 | SPLIT | Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない | 因果効果の結果閲覧・利用と推定器の設定操作を混同せず、区別して利用できる | 22 BD・23 IF | 推定器設定と効果の意味的混同を避けるユーザー可観測制約 | ACTIVE | IMPLEMENTED |

## 3. Original records unchanged (29)

`NFR-001a`、`NFR-004`、`NFR-008b`、`NFR-008c`、`NFR-009a`、`NFR-009b`、`NFR-011b`、`NFR-012`、`NFR-016`、`NFR-017`、`NFR-020b`、`NFR-022`、`NFR-026`、`AR-001`、`AR-002`、`AR-003`、`AR-005`、`AR-007`、`AR-010`、`AR-011`、`AR-012`、`AR-013`、`AR-014`、`AR-015`、`AR-017`、`AR-018`、`AR-023`、`AR-025`、`AR-026`

## 4. Quantitative safeguards

元の`AR-016`にある信頼区間の水準、bootstrap反復回数、計算不能判定、E11のFWER 0.05やMethod別CI/coverageの受入義務を削除してはならない。方式別の明細・原文は本表及び元の[canonical source](../../../../../../requirement_definition/10_requirements_definition.md)で保持。後続の[RD-04監査](98_rd04_consistency_verification.md)で移管先を明示する。
