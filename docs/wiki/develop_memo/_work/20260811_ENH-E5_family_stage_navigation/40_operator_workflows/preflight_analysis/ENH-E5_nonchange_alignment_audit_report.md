# ENH-E5 ③-1 ↔ ENH-E4実装 完全整合監査報告

- 監査目的: 物件③-1（ENH-E5文書のうちE4→E5非変更部分）が、物件①（ENH-E4完了時点の実装）を正確に記述しているか確認する。
- 物件① baseline: `a770cc4f38137063cd5f22d8035e91e3c63b7502`
- 物件②: 同baselineに格納されたENH-E4 approved target snapshot（10/21/22/23/30）
- 物件③: ENH-E5 instruction bundle v5 の revised 10/21/22/23/30
- 判定規則: ③-1に `MISMATCH / PARTIAL_MATCH / UNVERIFIED` が1件でもあれば完全整合FAIL。

## 1. 最終判定

**FAIL — 物件③-1は物件①と完全一致していない。**

要件ID単位の③-1は166件。内訳:

- MATCH: 108
- PARTIAL_MATCH: 33
- MISMATCH: 24
- UNVERIFIED: 1

Requirementsの非MATCH/部分一致57件は、E4文書とE5文書で要求本文が同一であり、診断はすべて **Case B（②=③-1, ①≠②）**。NFR-019のみsource implementationで真偽を判定できないdocumentation requirementとしてUNVERIFIED。

設計current-contract監査単位の内訳:

- MATCH: 58
- PARTIAL_MATCH: 3
- MISMATCH: 6

## 2. 要件レベルのMISMATCH（24件）

| ID | 要件 | ①との不一致 | 診断 |
|---|---|---|---|
| FR-002 | Projectにtopic、objective、decision contextおよびmemoを保持できる | Project entity/API has topic/objective/memo but no decision_context; decision_context belongs to ResearchContextVersion. | Case B |
| FR-015 | Analysis Viewの式と参照列を型付きSchemaで検証する | AnalysisView validates shape/known columns/deterministic compilation, but filter operator/value logical-type compatibility is not enforced by the domain validator. | Case B |
| FR-020 | Exploreのfilter・chart状態からAnalysis View draftを作成できる | No implemented Explore filter/chart-state -> AnalysisView draft conversion was found in the E4 frontend/application path. | Case B |
| FR-021 | 機微列、利用制限および説明をcolumn metadataへ付与できる | Dataset column metadata is essentially logical type/schema; sensitive/use-restriction/description metadata was not implemented. | Case B |
| FR-028 | correlation / association matrixを型に応じて生成できる | Exploratory operations do not include a correlation/association matrix operation. | Case B |
| FR-032 | 探索ResultからCausalまたはPredictive Analysis Specificationのdraftを作成できる | No implemented Exploratory Result -> Causal/Predictive AnalysisSpecification draft conversion was confirmed. | Case B |
| FR-062 | validation partitionまたはcross-validationでhyperparameter selectionを行える | Predictive validation explicitly rejects non-empty automated tuning candidates; automated hyperparameter selection is not supported. | Case B |
| FR-067 | 指定subgroupごとのperformanceとsample sizeを確認できる | Subgroups are accepted in evaluation_spec, but subgroup performance computation/output was not found. | Case B |
| FR-090 | 共通Result Envelopeにfamily、type、schema version、execution、stageを保持する | Canonical Result does not directly contain family or generic schema_version; execution result may have no stage_execution_id. | Case B |
| FR-092 | Artifactにfamily、type、schema version、media type、hash、sizeを保持する | Canonical Artifact contains type/media/hash/size but not family or generic schema_version. | Case B |
| FR-108 | Result、Execution、Graph、Analysisへ直接遷移できる | Frontend routes are workspace surfaces; dedicated deep routes to Result/Execution/Graph/Analysis resources are not generally implemented. | Case B |
| FR-110 | 一覧と比較でfamily、status、dataset、context、dateによるfilterを提供する | Results UI filters by a narrower set (e.g. family/type/status); dataset/context/date filtering is not fully implemented. | Case B |
| FR-114 | 作成系APIでidempotency keyを受け付ける | Some create endpoints accept Idempotency-Key, but Project creation and other create APIs do not. | Case B |
| FR-118 | CLIからFamily別Specificationをsubmitしstatus/resultを取得できる | Current scientific CLI runs local/headless scientific stages; it is not a generic Product CLI for submitting Family specifications and polling Product status/results. | Case B |
| FR-122 | 作成、更新、archive、execution、cancel、retry、exportをaudit logへ記録する | No general AuditLog domain/persistence resource implementing the listed action audit contract was found. | Case B |
| FR-126 | Metadata、Artifact、logの保持期間と削除policyを設定できる | No configurable metadata/artifact/log retention and deletion policy implementation was found. | Case B |
| FR-127 | API、DB、Worker、Artifact Storeのhealth / readinessを提供する | `/health/ready` returns only `{"status":"ok"}` and does not check API/DB/Worker/Artifact Store component readiness. | Case B |
| FR-128 | Algorithm、Runner、size limit、timeoutをconfigurationで管理する | Algorithm/runner/size/timeout configuration is not comprehensively externalized/configurable. | Case B |
| NFR-004 | 通常一覧・詳細APIの95 percentileを2秒以内、重い集計は非同期化する | No evidence of a 95th-percentile <=2s acceptance/performance implementation or regression gate was found. | Case B |
| NFR-013 | すべてのSpec、Plan、Result、Artifact descriptorにschema versionを持つ | Spec/Plan have schema versions, but canonical Result/Artifact descriptors do not each directly carry a generic schema_version. | Case B |
| NFR-017 | upload size、row count、column count、memory、timeoutに明示上限を持つ | No comprehensive explicit limits for upload size/rows/columns/memory/timeout were found. | Case B |
| NFR-020 | Local filesystemとobject storageをPortで切り替えられる | ArtifactStore Port exists, but current adapter/wiring contains only LocalArtifactStore; no object-storage adapter is available to switch to. | Case B |
| AR-016 | subgroup metricはsample sizeと不確実性を併記する | Subgroup metrics/uncertainty output is not implemented. | Case B |
| AR-017 | Result比較は同一Task / Estimand / Outcome等の比較可能性を検証する | Result comparison validates same family/result type, not same Task/Estimand/Outcome semantic comparability. | Case B |

## 3. 要件レベルのPARTIAL_MATCH（33件）

| ID | 要件 | 実装で満たす部分 / 不足部分 | 診断 |
|---|---|---|---|
| FR-007 | Executionは受付時のResearch Context snapshotとhashを保持する | Execution persists analysis_spec_json/objective/rationale and snapshot hash, but a dedicated complete ResearchContext snapshot+hash contract was not confirmed. | Case B |
| FR-008 | Contextの履歴、利用Analysisおよび関連Resultを確認できる | Context usage covers AnalysisSpecification plus historical/compatibility family execution/result projections; it is not a complete canonical Execution/Result usage index. | Case B |
| FR-011 | Dataset Versionにcontent hash、schema、row count、column count、基本profileを保存する | DatasetVersion stores profile_summary_json, but registration computes schema/row/column counts and does not compute the required basic profile. | Case B |
| FR-025 | 欠損パターンおよび列別missingnessを確認できる | Column missingness/profile exists; explicit missing-pattern analysis was not confirmed. | Case B |
| FR-026 | 二変量の散布、箱ひげ、クロス集計および関連指標を生成できる | Association operations exist, but the full requested scatter/box/crosstab surface set is not implemented as stated. | Case B |
| FR-034 | 可視化の描画条件、集計条件、samplingおよびcode versionを保存する | Sampling/spec/code-version information exists across contracts, but complete rendering/aggregation-condition persistence as stated was not confirmed. | Case B |
| FR-048 | overlap、balance、weight、sample loss等をDiagnostics Resultとして分離保存する | Causal diagnostics exist and estimator capabilities declare several diagnostics, but the full overlap/balance/weight/sample-loss set is not uniformly produced. | Case B |
| FR-051 | 同一Project・Datasetの先行Discoveryを確認し、確認的Estimationへ探索後推論警告を保存する | Cross-analysis scientific warning behavior exists in parts of the product, but the exact same-Project/same-Dataset prior-Discovery warning contract was not fully confirmed. | Case B |
| FR-054 | Causal ResultからQuestion、Design、Graph、Eligibility、上流Resultへ遡れる | Canonical lineage covers major upstream entities, but the full Question/Design/Graph/Eligibility/upstream Result chain as one complete contract is not fully represented. | Case B |
| FR-068 | prediction、residual / error、metric、model、preprocessorをArtifactとして保存する | Model/preprocessor/prediction artifacts exist, but metrics/errors are primarily Result payloads rather than all being Artifact resources as stated. | Case B |
| FR-072 | 同一Taskのmodel、split、feature、metric差分を比較できる | Comparison enforces same family/result type; it does not fully validate same Task/split/feature/metric semantics. | Case B |
| FR-082 | 同一idempotency keyと同一bodyのCommandを重複実行しない | Idempotency exists on selected command endpoints, not every Command universally. | Case B |
| FR-086 | Stageごとのtimeout、resource limit、random seedを記録する | Random seed and some timeout/lifecycle data exist, but a universal per-stage timeout/resource-limit/random-seed persisted contract is not implemented. | Case B |
| FR-087 | code、runtime、library、schema versionをExecution snapshotへ固定する | Execution stores code_version/runtime_version_json/schema snapshot, but universal explicit library-version capture was not established. | Case B |
| FR-095 | ResultからContext、Dataset、View、Spec、Plan、Stage、Artifactへ遡る | Lineage covers Project/Dataset/View/Execution/Result/Artifact/Graph/Annotation relationships, but does not expose the full Spec/Plan/Stage chain requested. | Case B |
| FR-107 | 操作可否をBackendの正本状態から導出し、拒否理由を表示する | Some APIs expose allowed_actions/backend-derived state, but this policy is not uniformly enforced across all controls. | Case B |
| FR-109 | 非同期処理のloading、empty、partial、error、cancel状態を区別する | Loading/empty/error states exist in places, but the full loading/empty/partial/error/cancel state taxonomy is not consistently implemented. | Case B |
| FR-111 | keyboard操作、focus、label、contrast等の基本accessibilityを満たす | Labels/ARIA/keyboard-related markup exists, but complete keyboard/focus/contrast conformance was not demonstrated. | Case B |
| FR-120 | OpenAPIとSchema exampleを正本contractと同期する | FastAPI generates OpenAPI, but systematic synchronization of canonical schema examples was not established. | Case B |
| FR-121 | Project単位でread、write、operate権限を検証する | Project Closure enforces OWNER/EDITOR/VIEWER roles, but not all routers uniformly pass through that authorization boundary. | Case B |
| FR-123 | preview、artifact、prediction outputへの機微データ露出を権限と設定で制限する | Sensitive Result payload suppression exists, but uniform policy over preview/artifact/prediction output and configurable controls is not complete. | Case B |
| FR-124 | Artifact downloadでProject権限とcontent dispositionを検証する | Project-scoped closure artifact download enforces project role and safe headers, but not every artifact route shares the same authorization boundary. | Case B |
| NFR-001 | 同一snapshot、code version、seed、runtimeで再実行可能な情報を保持する | Reproducibility metadata is substantial, but complete snapshot/code/seed/runtime coverage for every execution path was not established. | Case B |
| NFR-002 | すべてのResultがProject、Context、Dataset、Spec、Execution、Artifactへ遡れる | Lineage is substantial but does not provide the full Project/Context/Dataset/Spec/Execution/Artifact trace for every Result as stated. | Case B |
| NFR-006 | Worker再起動時もclaim、retry、artifact commitの二重実行を防ぐ | Lease/claim/retry mechanisms exist; exactly-once artifact commit across worker restart was not fully established. | Case B |
| NFR-007 | Metadata transactionとArtifact書込みの失敗補償を定義する | Metadata transactions and artifact storage exist, but a complete documented/implemented compensation protocol for cross-store failures was not established. | Case B |
| NFR-008 | 認証、認可、入力検証、path traversal防止、secret非露出を行う | Input validation/path safeguards exist in parts; authentication/authorization is not uniformly applied to all API routes. | Case B |
| NFR-009 | 機微列、prediction、local explanationの表示・exportを最小化できる | Sensitive output suppression exists for Result detail, but full configurable minimization across prediction/local explanations/exports is partial. | Case B |
| NFR-010 | APIとWorkerの障害を分離し、実行中断と再開可否を明示する | API and Worker are separate processes/contracts, but explicit restart/resume semantics are partial. | Case B |
| NFR-011 | structured log、correlation id、execution id、stage id、metricを出力する | Request/execution/stage identifiers exist, but comprehensive structured logs and metrics are not uniformly implemented. | Case B |
| NFR-012 | 主要操作をkeyboardで実行でき、状態を色だけで伝えない | Some accessibility support exists, but complete keyboard/non-color state conformance was not evidenced. | Case B |
| AR-004 | 同一データで探索後に確認的分析を行った事実を警告とLineageで保持する | Warnings/lineage support exists, but the exact same-data exploratory-then-confirmatory tracking contract was not fully established. | Case B |
| AR-020 | local explanationやprediction rowを機微情報として扱える | Sensitive Result handling exists, but row-level prediction/local-explanation handling as a uniform policy is partial. | Case B |

## 4. UNVERIFIED

- `NFR-019`: 現行の正本requirements/design snapshotだけで機能・データ・API・詳細設計を理解できる — Documentation-only requirement; cannot be established from source implementation alone.

## 5. 要件表以外 / 設計文書で検出した非整合

| ID | 文書 | 箇所 | 判定 | ①との不一致 | 診断 |
|---|---|---|---|---|---|
| D10-004 | 10 | 8.4 Stage Execution | MISMATCH | Document omits CANCELLED transitions that implementation supports from PENDING/READY/RUNNING. | Case B |
| D10-005 | 10 | 9 Permissions | MISMATCH | Persisted Project roles are OWNER/EDITOR/VIEWER; no distinct execute/Operator role model exists and authorization is not uniformly applied to all routers. | Case B |
| D10-006 | 10 | 10 Retention/Audit | MISMATCH | Annotation revision history exists, but no general AuditLog resource and no configurable retention/deletion audit contract exists; LocalArtifactStore.delete removes file directly. | Case B |
| D21-005 | 21 | 5.4.2 AnalysisView constraint | MISMATCH | Domain validator checks envelope/array uniqueness/derived names but not filter operator/value logical-type compatibility. | Case B |
| D22-001 | 22 | 2 System Context | MISMATCH | No canonical Product Outbox resource/publisher is present in E4 completion implementation. | Case B |
| D22-002 | 22 | 3.1 Layer / Ports | MISMATCH | Current product ports are artifact_store, clock, repositories, scientific_core, unit_of_work; runner/auth/event ports are not present. | Case B |
| D22-003 | 22 | 3.1/14 Adapter boundary | PARTIAL_MATCH | LocalArtifactStore exists and scientific core has a port boundary, but there is no object-storage adapter and adapter taxonomy is not implemented as broadly as written. | Case B |
| D22-013 | 22 | 15 Test Architecture | PARTIAL_MATCH | Core domain/workflow/API/scientific tests exist, but the full approved target test architecture (including all browser/accessibility/performance surfaces) is not completely evidenced. | Case B |
| D30-018 | 30 | 20 Test Design existing contract assertions | PARTIAL_MATCH | Detailed design includes target verification surfaces beyond what can be established as complete E4 implementation; current core contract tests exist but full set is not evidenced. | Case B |

## 6. Case診断

### Case A — ②=①, ③-1≠①
今回の監査で確定したCase Aは **0件**。確認した不一致はE5で新たに作った誤記というより、E4 target snapshotからの継承が中心。

### Case B — ②=③-1, ①≠②
- 要件表: 57件（24 MISMATCH + 33 PARTIAL_MATCH）
- 要件表外/設計: StageExecution cancel記述、権限taxonomy、Audit/Retention、AnalysisView型整合、Outbox、Port/Adapter taxonomy等を確認。
- ②自身が「approved target contractでありproduction implementation completionをassertしない」と明記しているため、E4完了時点でも未実装targetが残り得る。

### Case C — 三者不一致
今回の確定事項では **0件**。

### Case D — ③-1=①, ②≠①
V5では既に複数のhistorical driftをsourceに合わせて修正済み。代表例:
- current authをBearer/OIDCではなくX-User-Id/anonymousとして記載
- canonical Result/Artifact fieldをORM/current APIに合わせて記載
- Worker claimをpublic claim_tokenではなくExecution lease ownershipとして記載
- 独立Execution/Stage event publisherを既存contractとして扱わない
- Causal plannerをone-operation/one-stage compatibility planとして記載
- Predictive full plan順序をsplit -> prepare -> train -> evaluate -> optional explainへ修正
- Research Context relationの一般cycle検出をcurrent実装factとしては記載しない

## 7. 物件①側で記録すべき事項

以下は「実装が非合理」と断定したものではない。②のapproved targetに対する **未実装 / 部分実装 / technical-debt候補** として記録する。

- Project `decision_context`はProjectではなくResearchContextVersionに存在する。要件のresource ownershipが実装と異なる。
- AnalysisViewのtyped filter validationがapproved targetより弱い。
- automated hyperparameter tuningとsubgroup performance/uncertaintyはapproved targetに対して未実装。
- general AuditLog、configurable retention、component readiness checksはapproved targetに対して未実装。
- ArtifactStore Portは存在するが、実装/wiringはLocalArtifactStoreのみでobject-storage adapterがない。
- authorizationはProjectClosure領域にOWNER/EDITOR/VIEWER policyがある一方、全routerへ一律適用されていない。
- canonical Result/Artifact schemaはE4 requirement FR-090/092/NFR-013の表現と異なり、family/schema versionを各entityへ直接保持しない。

これらは、今回の監査だけでは「実装修正すべきbug」か「E4 requirementを現実装に合わせて改定すべき事項」かを決めない。次工程の文書整合修正でdecision pointとして扱う。

## 8. ③-1の文書別判定

| 文書 | 判定 | 主な理由 |
|---|---|---|
| 10 要件定義 | FAIL | 非変更要件166件中、24 MISMATCH / 33 PARTIAL / 1 UNVERIFIED。状態・権限・監査sectionにもCase Bあり。 |
| 21 論理データ設計 | FAIL | 大半のresource contractはsource-alignedだが、AnalysisView typed filter constraintがE4由来の未実装target。 |
| 22 プロダクト基本設計 | FAIL | System ContextのOutbox、runner/auth/event Port、広いAdapter taxonomyがcurrent sourceに存在しない/部分的。 |
| 23 API・インターフェース設計 | PASS（非変更current-contract範囲） | V5でauth、Result/Artifact、Worker lease、event、routes等をcurrent sourceへ修正済み。今回追加の直接矛盾なし。 |
| 30 詳細設計 | PASS（非変更current-contract範囲） | V5でdomain/workflow/persistence/package/runtime契約をcurrent sourceへ具体化済み。今回追加の直接矛盾なし。 |

## 9. 結論 / 次工程への入力

1. **③-1と①の完全整合は成立していない。**
2. 不一致の中心はCase Bであり、E4 target documentの未実装・部分実装要求をE5文書が「current effective requirement/design」として継承していることが原因。
3. 次工程「ドキュメントとの整合」では、Case Bをそのまま①へ合わせて削るのではなく、各項目を次のどちらにするか判断する必要がある。
   - E5でも有効なrequirement/design targetとして維持し、③-2またはtechnical debtとして明示する。
   - 現実装を正としてcurrent effective documentから撤去/修正する。
4. Case Dのsource-aligned correctionsは維持する。

## 10. 添付監査データ

- `ENH-E5_nonchange_requirement_alignment_matrix.csv`: Requirement全215件。③-1/③-2分類と166件のsource判定。
- `ENH-E5_nonchange_design_alignment_matrix.csv`: 10/21/22/23/30の非変更current-contract audit unit。