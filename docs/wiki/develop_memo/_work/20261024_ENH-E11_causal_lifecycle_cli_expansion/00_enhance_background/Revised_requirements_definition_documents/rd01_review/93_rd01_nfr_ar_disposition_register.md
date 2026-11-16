# RD-01 — Existing NFR / Scientific AR Register (63 IDs)

**Review ID:** RD-01  
**Date:** 2026-11-16  
**Source branch:** `prototype/ariadne_mvp` / source blob `40b83f29c67b4a39f6db5393be7534c5e892d656`; E11 draft blob `e6b151a0537054a11e8368520e940bd42cb68e2f`  
**Status:** `DISPOSITION_PROPOSED / NOT_YET_APPLIED / OWNER_REVIEW_REQUIRED`. 本書は逐条分類の提案記録であり、正式RD/BD/IF/DDの改訂、既存Requirementの失効、Method Scopeの変更、Gate PASSを意味しない。

**判定原則:** 『何を満たさなければならないか』をRDに残す。方法自体が承認された提供義務の場合は`10_32_scientific_method_scope.md`相当のScope契約で保持し、実装と同一視しない。科学的Estimand/前提の制限は`10_31`等で保持する。移管のみのIDもTrace台帳から削除せず、統合元要求を明記してControlled Publicationで処理する。

Source: [Current source requirements](https://github.com/kousuke-ota-datascience/causal-atelier/blob/8c9a77bde053417270325508fc3174e159719965/docs/wiki/requirement_definition/10_requirements_definition.md)

## 1. NFR (36 IDs)

| ID | 原文（正本 / 草案） | Disposition | RD側の要件核・暫定改訂文 | 下位文書・保持先 | 判定根拠 | Level | Requirement Status | Implementation Status | Delivery |
|---|---|---|---|---|---|---|---|---|---|
| NFR-001a | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | KEEP_RD | current snapshot、code/runtime metadata、seed、schema identity等の再現性情報を保持する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-001b | actual scientific library versionとStageAttempt effective seedを含むenvironment再構築metadataを保持する | SPLIT | 解析結果を再現するため実効ライブラリ版・乱数条件を取得できる | 21 LDD・30 DD | StageAttempt fieldなどの保存手法 | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-002 | canonical lineage read modelでResearchContextVersion→AnalysisSpecification→ExecutionPlan→Execution→StageExecution→Result→Artifactを追跡し、DatasetVersion/AnalysisView/GraphVersion/input Result/base Executionも接続する | SPLIT | 研究条件から入力・計画・実行・結果・成果物までの追跡が可能である | 21 LDD | canonical read modelの具体的構造 | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-003 | Canonical JSONとhash生成はfield順やprocessに依存しない | SPLIT | 同一内容から環境に依存しない同一性識別値を生成できる | 22 BD・30 DD | canonical JSON・hash処理詳細 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-004 | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | KEEP_RD | 通常一覧・詳細APIの95 percentile 2秒等のgeneral performance SLOとregression gateを定義する | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-005 | 新Analysis Familyを既存Executor変更なしにRegistry追加できる | SPLIT | 新しい分析領域を既存分析の挙動を壊さず追加できる | 22 BD・30 DD | RegistryとExecutor非変更の具体方式 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006a | current claim/lease/retry mechanicsでExecution/Stage lifecycleを安全に再試行できる | SPLIT | 中断・再送時にExecutionを安全に再開・再試行できる | 22 BD・30 DD | claim/lease方式 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-006b | retry/restartでsuccessful Stage outputのduplicate durable Artifact materializationを防止する。exactly-once executionは保証しない | SPLIT | 再試行・再起動で成功済み成果物の重複作成を防止する | 22 BD・30 DD | exactly-onceを約束しない技術的限界は明記 | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-007 | Metadata transactionとArtifact writeのcross-store failure compensationを定義する | SPLIT | 成果物と管理情報の不整合が発生した場合、安全に回復・検知できる | 22 BD・30 DD | cross-store compensation手順 | — | DEFERRED | PARTIAL | FUTURE |
| NFR-008a | current input validation、path traversal防止、secret非露出等のsafeguardを維持する | SPLIT | 入力検証と危険なパス・秘密情報の保護を維持する | 22 BD・30 DD | 具体的safeguard実装 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-008b | 全project-scoped routeへProjectMembership authorizationを一貫適用する | KEEP_RD | 全project-scoped routeへProjectMembership authorizationを一貫適用する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-008c | production-grade authentication/security hardeningを完成させる | KEEP_RD | production-grade authentication/security hardeningを完成させる | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | PARTIAL | FUTURE |
| NFR-009a | current sensitive Result suppressionを維持する | KEEP_RD | current sensitive Result suppressionを維持する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-009b | prediction/local explanation/exportのconfigurable minimization policyを提供する | KEEP_RD | prediction/local explanation/exportのconfigurable minimization policyを提供する | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | PARTIAL | FUTURE |
| NFR-010a | API processとWorker processを分離するcurrent deployment boundaryを維持する | SPLIT | 分析実行の負荷がAPIの応答性・稼働に不必要な影響を与えない | 22 BD | API/Worker process分離という配置制約 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-010b | Worker restart後の明示的resume/recovery semanticsを定義する | SPLIT | 実行基盤の再起動後に処理状態を復元・回復できる | 22 BD・30 DD | Worker resume契約 | — | DEFERRED | PARTIAL | FUTURE |
| NFR-011a | current request/execution/stage correlation identifiersをlogへ出力する | SPLIT | Request・実行・処理単位をまたいで障害を追跡できる | 21 LDD・30 DD | correlation IDの形式とlog出力 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-011b | comprehensive structured logging、metrics、operational telemetryを提供する | KEEP_RD | comprehensive structured logging、metrics、operational telemetryを提供する | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | PARTIAL | FUTURE |
| NFR-012 | current surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | KEEP_RD | current surfaceの主要操作をkeyboardで実行でき、focus/name/error/non-color/contrast semanticsを満たす | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | PARTIAL | ENH-E5 |
| NFR-013 | schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない | SPLIT | 変化するデータ契約を識別し後方互換を制御できる | 21 LDD・23 IF | schema_version fieldの物理配置禁止 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-014 | &#96;causal-analysis-spec/2&#96;の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ | SPLIT | 既存v2の因果分析仕様と保存済み結果を継続して読み取れる | 23 IF・22 BD | causal-analysis-spec/2は互換契約として保持 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-015 | Domain、Planner、Runner、API、Worker、UI、scientific benchmarkを分離testできる | SPLIT | Domain・実行・API・UI・科学計算を個別に検証できる | 22 BD・30 DD | Planner/Runner等の試験境界 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-016 | 仮定、warning、negative result、limitationを省略せず表示する | KEEP_RD | 仮定、warning、negative result、limitationを省略せず表示する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-017 | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | KEEP_RD | upload size、row/column count、memory、timeout等にexplicit operational hard limitを定義する | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-018 | Product DomainからWeb Framework、ORMおよびlegacy packageへ依存しない | MOVE_BD | NFR-005の保守性・依存分離を満たすための層間禁止依存として保持 | 22 BD・30 DD | Product DomainのFramework/ORM import禁止 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-019 | &#96;00/10/21/22/23/30&#96;だけでcurrent product concept / requirement / logical model / design / interface contractを自己完結して理解できる | REWRITE_RD | 現行Productの要件・データ・設計・Interface契約を整合した正式資料で追跡・理解できる | — | 文書番号の固定を避ける | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-020a | Artifact storageを&#96;ArtifactStore&#96; Port abstraction越しに利用する | SPLIT | 成果物保存先を交換しても分析の振る舞いが維持される | 22 BD・30 DD | ArtifactStore Portという具体方式 | — | ACTIVE | IMPLEMENTED | BASELINE |
| NFR-020b | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | KEEP_RD | Local filesystemに加えobject storage adapterを提供し、Port越しに切替可能にする | — | 能力・科学的制約・品質または受入結果を規定 | — | DEFERRED | NOT_IMPLEMENTED | FUTURE |
| NFR-021 | Navigation concernの変更がruntime execution lifecycleへ不要に伝播しない | SPLIT | 画面ナビゲーションの変更が分析実行ライフサイクルに影響しない | 22 BD | Navigation依存分離の方式 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-022 | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | KEEP_RD | 同一Project / Family / Stage routeは同一navigation stateへdeterministicに復元される | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-023 | Family-specific Navigation Stage catalogをCapability ownershipで局所化する | SPLIT | Familyごとの画面構成を他Familyへの影響を抑えて変更できる | 22 BD | Capability-owned catalogの構成 | — | ACTIVE | NOT_IMPLEMENTED | ENH-E5 |
| NFR-024 | Navigation descriptor、route、renderer binding、runtime independenceをunit/integration/E2Eで分離検証できる | SPLIT | 画面構成・URL復元・表示・分析実行独立性を個別に検証できる | 22 BD・30 DD | 具体的単体/E2E試験階層 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-025 | CLI / library executionがWeb UI route、tab/sidebar state、NavigationStageDescriptorへ依存しない | SPLIT | CLIやライブラリ実行を画面状態なしで行える | 22 BD・30 DD | NavigationStageDescriptorの禁止依存 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-026 | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | KEEP_RD | Current Family / Stageを色だけでなくsemantic active state、label、focus等でも識別できる | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-027 | navigation metadata取得・renderingがanalysis executionのcritical pathへ不要なI/Oまたはblocking dependencyを追加しない | REWRITE_RD | 画面構成情報の取得・表示によって分析処理の性能を不要に低下させない | — | critical pathの実装表現を一般化 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| NFR-028 | optional analytical engineのimport/availability failureをcore process startup failureへ伝播させず、capability discovery/selection時に局所化してstable unavailable state/errorとして報告する | SPLIT | 任意の分析エンジンが利用不能でも基本機能を継続でき、利用不能理由を識別できる | 22 BD・23 IF | import/availability失敗の処理位置 | — | ACTIVE | IMPLEMENTED | ENH-E10 |

## 2. Scientific AR (27 IDs)

| ID | 原文（正本 / 草案） | Disposition | RD側の要件核・暫定改訂文 | 下位文書・保持先 | 判定根拠 | Level | Requirement Status | Implementation Status | Delivery |
|---|---|---|---|---|---|---|---|---|---|
| AR-001 | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | KEEP_RD | 探索的可視化は仮説生成であり、因果結論または確認的検定へ自動変換しない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-002 | 予測性能は因果効果を示さない | KEEP_RD | 予測性能は因果効果を示さない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-003 | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | KEEP_RD | Predictive Explanationはmodel behaviorの説明でありcausal explanationではない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-004 | 同一immutable &#96;dataset_version_id&#96;を探索とconfirmatory analysisで再利用した場合、&#96;EXPLORATORY_REUSE_SAME_DATA&#96; warningとlineage evidenceを保持する | SPLIT | 同一データを探索と確認的分析に再利用した場合、その事実を示し独立検証として扱わない | 21 LDD・23 IF | 固有warning codeとdataset ID | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-005 | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | KEEP_RD | 因果推定はIdentification ResultとData Eligibility Resultを参照してgateする | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-006 | Identification statusは全reasonを収集後に決定する | REWRITE_RD | 因果識別の成否は全ての不適格理由と不確実性を考慮して決定しなければならない | 10_31 AR | status優先順位の詳細は科学契約 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-007 | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | KEEP_RD | Collider判定はback-door path上のcolliderまたはその子孫を対象とする | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-008 | Eligibilityの型はBINARY、CONTINUOUS、UNSUPPORTED等の正規値で保存する | SPLIT | 推定に必要な変数型が適格かを識別できなければならない | 21 LDD・23 IF | BINARY等の保存enum具体値 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-009 | 外部libraryのdtype objectまたはmodel objectをJSON正本へ保存しない | MOVE_BD | 科学的データ契約を実装ライブラリの型から独立させるための設計制約として保持 | 21 LDD・22 BD | 外部型objectの永続化禁止 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-010 | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | KEEP_RD | Estimation前提不成立時は数値を無理に返さず分析状態を保存する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-011 | Predictive preprocessingはtrain partitionのみでfitする | KEEP_RD | Predictive preprocessingはtrain partitionのみでfitする | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-012 | test partitionをfeature selection、model selection、threshold selectionに利用しない | KEEP_RD | test partitionをfeature selection、model selection、threshold selectionに利用しない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-013 | 時系列Taskは未来観測がtrain featureへ混入しないsplitを使用する | KEEP_RD | 時系列Taskは未来観測がtrain featureへ混入しないsplitを使用する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-014 | 同一entityがtrainとtestへ跨る場合はgroup leakageを検査する | KEEP_RD | 同一entityがtrainとtestへ跨る場合はgroup leakageを検査する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-015 | classification metricはclass imbalance、threshold、calibrationと併記する | KEEP_RD | classification metricはclass imbalance、threshold、calibrationと併記する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-016 | subgroup metricは&#96;sample_count&#96;を必須とし、0.95 percentile bootstrap（1000 resamples、deterministic seed）で計算可能な場合にuncertaintyを併記し、計算不能値を捏造しない | SPLIT | 評価Subgroupの標本数と計算可能な不確実性を示し、計算不能値を生成してはならない | 10_32 Method Scope・22 BD | 0.95/1000回/200回等の採用済検証条件を保持 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-017 | Result比較はsemantic compatibilityとdirect metric comparabilityを分離して判定する | KEEP_RD | Result比較はsemantic compatibilityとdirect metric comparabilityを分離して判定する | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-018 | AUC、RMSE、ATE等を単一の優劣scoreへ変換しない | KEEP_RD | AUC、RMSE、ATE等を単一の優劣scoreへ変換しない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-019 | random seedだけでなくsplit indexまたはpartition artifactを保存する | SPLIT | 分析のデータ分割を再現可能な情報として保持しなければならない | 21 LDD・30 DD | index/partition Artifactの保存方式 | — | ACTIVE | IMPLEMENTED | BASELINE |
| AR-020 | prediction row / local explanationをpotentially sensitive outputとして扱い、Project roleに応じてdetail exposureを制御する | SPLIT | 個票予測と局所説明は機微情報になり得るため、利用権限に応じ露出を制限する | 22 BD・23 IF | 権限制御の具体位置 | — | ACTIVE | PARTIAL | ENH-E5 |
| AR-021 | Navigation Stageの表示順を分析上必須の実行順序として解釈しない | MOVE_BD | ナビゲーション順と処理依存を混同しない設計制約として保持 | 22 BD | 科学的要件ではなくNavigationとRuntimeの分離 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-022 | Family間でStage数・名称を揃えることを科学的workflow要件としない | MOVE_BD | Family別Stage配置を揃えることを科学実行要件としない設計制約として保持 | 22 BD | IAの実装制約 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-023 | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | KEEP_RD | Causal Identificationでは観測データと仮定からestimandが識別可能かをEstimationと分離して扱う | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-024 | Causal Effectsは推定されたeffectの閲覧・利用を扱い、estimator configurationと混在させない | MOVE_BD | 効果の閲覧と推定設定を区別するUI設計制約として保持 | 22 BD | 科学的推定条件ではなく画面責務 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-025 | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | KEEP_RD | Predictive MetricsとPredictive Explainabilityを別目的として扱い、feature importance等をcausal effectへ読み替えない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-026 | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | KEEP_RD | Exploratory Findings / visualizationをcausal conclusionまたはconfirmatory resultへ自動昇格しない | — | 能力・科学的制約・品質または受入結果を規定 | — | ACTIVE | IMPLEMENTED | ENH-E5 |
| AR-027 | coefficient contribution / SHAP / LIMEはmodel behavior explanationであり、feature causal importance、treatment effect、causal mechanismを意味しない | REWRITE_RD | 予測モデルの説明値はモデルの挙動に関するものであり、変数の因果的重要性・介入効果・因果機構を示さない | 10_32 Method Scope | SHAP/LIMEの名称を要件一般文から除外 | — | ACTIVE | IMPLEMENTED | ENH-E10 |
