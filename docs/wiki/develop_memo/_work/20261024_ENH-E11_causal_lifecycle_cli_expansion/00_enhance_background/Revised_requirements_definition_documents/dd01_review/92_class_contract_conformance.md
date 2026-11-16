# DD-01 follow-up — Class/Protocol 7区分適合性のSource基準監査

**実施日:** 2026-11-17 JST  
**文書種別:** Flow / Audit  
**基準:** Owner採用の[30_01_class_design_template](../30_detailed_design/30_01_class_design_template.md)。Class/Protocol/DTO別に識別責務、Field、Constructor、Method、Flow、I/O・Failure、Testの7節が必要。  
**判定:** `DD_CLASS_TEMPLATE_FAIL / CLASS_SOURCE_RECONCILIATION_PARTIAL / INDEPENDENT_REVIEW_OPEN`。

## 1. 7区分の適用対象の選定

すべての`30_detailed_design/` 28個の番号付きMarkdown（監査時点）の見出しを確認した。全部がClass文書というわけではない。次の異なる責務を分ける。

- **物理Class/DTO/Port：** 具体Class/Protocolとして責務・Field・Callableがある。7区分すべてが必須。該当なしは理由付き`N/A`。
- **Module-level function：** Signature、引数・戻り値、Side effect、Exception、Test Traceを必須にする。架空のClassとして扱わない。
- **Topic/process/UX narrative：** Class定義の代替にならない。基本設計に移管するか、対応するClass/Module/Algorithmとして追加具体化するか判断する。

## 2. 全主要Classの粒度照合

| Symbol | 設計文書 | Existing / Proposed | 7区分 | 具体Gap |
|---|---|---|---|---|
| `GraphVersion` | `30_10` | Existing | FAIL | 単一短縮§5。Field／Constructor／Method／I/O・State／Error／Testの区分なし |
| `PlanValidator` | `30_20` | Existing | FAIL | §2はClass短縮表、Constructorの実型/Default、Validate Error、Returnの詳細を節別に規定しない |
| `StageRunnerRegistry` | `30_20` | Existing | FAIL | Registry fieldのmutability・DuplicateRegistration・RunnerNotRegistered等の表記不足 |
| `ExecutionOutcome` | `30_21` | Existing | FAIL | DTOがExecutorと一節、各field型は記載されるがConstructor/Serialization/N/A検証節がない |
| `GenericExecutor` | `30_21` | Existing | FAIL | §4が旧Navigation §4と章番号衝突。Class separate 7区分なし |
| `StoredArtifact` | `30_50` | Existing | FAIL | Protocolとの合同§6。DTOの生成・不変性・Validationの整理不足 |
| `ArtifactStorePort` | `30_50` | Existing | FAIL | 4 OperationのSignatureはあるがI/O failureと7区分なし |
| `CliManifest` | `30_60` | Existing | FAIL | Field群と`to_dict`はあるがデフォルト生成とnested mutability・7区分なし |
| `ContentRef` / `LocalStudySpec` | `30_61` | Proposed | FAIL | 2〜3節で複数型一括、厳密Field/Factory/例外/SHA未freeze |
| `LocalConfigDecoder` / `GraphEvidence` / `EndpointEdge` | `30_61` | Proposed | FAIL | Type単位の7節不在、ErrorとCanonical JSONの実装詳細未確定 |
| `IdentificationOutcome` / `EstimatorRequest` | `30_61` | Proposed | FAIL | DTO別ConstructorとMethod、State/exception個別定義不足 |
| `ARConfidenceSet` / `InferenceEvidence` | `30_61` | Proposed | FAIL | 数学的Invariant説明はあるが物理Constructor/fields/methods表が型ごとに未完成 |
| `EffectOutcome` / `BackendCapabilityRecord` | `30_61` | Proposed | FAIL | Typed resultsは設計されるが7区分に未展開 |
| `E11LocalCausalUseCase` | `30_62` | Proposed | FAIL | 5下位節で、個別Field/Constructor/Exception/Port tableが不足 |
| `MethodCapabilityRegistry` / Adapter Factory | `30_62` | Proposed | FAIL | Registry/Factoryが合同、ConstructorとMethod Exception別定義不足 |
| `LocalArtifactPublisher` | `30_62` | Proposed | FAIL | Atomic Flowはあるが、状態ごとのField mutability、Caller/transaction/error/rollback表の7節不足 |
| `LocalManifestReader` / `LocalRunManifest` | `30_62` | Proposed | FAIL | Reader ClassとManifest DTOが合同、7区分未分離 |
| `LocalPrivacyPolicy` | `30_62` | Proposed | FAIL | 3下位節。認可判定/例外/I/OとTestの分離不足 |
| `ScientificAdapter`／各Method Adapter Class候補 | `30_63` | Proposed | FAIL | Method ID 41件の対応表はClassごとのField/Factory/Methodの物理仕様ではない |

**Method ID 41件の列挙は正しくとも、Class数41件と同じではない。** Methodを共有Classのvariantとする場合、当該共有Classの7区分とMethod Config/Registry Variantの識別・差分契約を明示する必要がある。

## 3. Existing Sourceと文書の直接比較（再確認した6 Source）

| Source module / Blob SHA | 実在するClass methodと重要な契約 | 現DDに不足していること |
|---|---|---|
| `product/workflow/plan_validator.py` — `53aab649...` | `PlanValidator.__init__(runners, *, max_timeout_seconds=86400)`、`validate(plan)->tuple[str,...]`、`InvalidExecutionPlan`、DAG topological validation、Duplicate/timeout/runner checks | Constructor default、Error map、side-effect N/A、各Validation invariant |
| `product/workflow/runner_registry.py` — `7ffa673d...` | `_runners: dict[StageType,StageRunner]` mutable、`register/resolve/contains/capability_fingerprint`、DuplicateRegistration/RunnerNotRegistered | Mutation/ExceptionをMethod別の表へ |
| `product/workflow/executor.py` — `81d91e7d...` | `ExecutionOutcome` frozen DTOと`GenericExecutor.execute`、StageAttempt、cancel/skipped/failed、`compensate`、clock callback | Mutable stateとResult、cancel/failure/rollbackの分離、E11 Localへの再利用可否未証明 |
| `product/domain/graph_version.py` — `37ff76e0...` | Mutable `GraphVersion` dataclass、`validate_origin/apply_edit/fix/validate_outcome`、Origin refs、DRAFT→FIXEDとGraphAlreadyFixed/InvalidAnalysisSpec | Field default factory、Constructor post-init、State Transition、Error |
| `product/ports/artifact_store.py` — `e5bb990f...` | `StoredArtifact` frozen、`ArtifactStorePort` Protocol: `store/retrieve/exists/delete` | 多ファイルAtomicの保証はない。個別Method I/OとError・Adapter契約 |
| `interfaces/cli/manifest.py` — `97216eca...` | `CliManifest` frozen dataclassだが`artifacts/warnings/scientific_warnings`はlist、`to_dict()->asdict` | 「frozen＝深い不変」と誤認することを防ぐFieldの可変性・Serialization Test |

ここで示したSource SHAは監査したSource Blobであり、実効科学Backend/テストPASSの証拠ではない。

## 4. 既存30系に混在する別粒度

| File群 | 現内容 | 期待する整理 |
|---|---|---|
| `30_30`〜`30_34` | Exploratory/Causal Stageの画面目的・主な操作・Visibility | UI基本設計の責務は22、具体Runtime/Controller/RunnerはClass DDへ |
| `30_35`〜`30_37` | Predictive UIやFeature selector、LightGBM/SHAP/LIMEの設定も混合 | Presentationは22、Source-backed Model adapter/SchemaとAlgorithmの実装詳細は30 |
| `30_40`〜`30_43` | Project/Workspace/Navigation/Availability、Data/Routeの説明 | 22/23/21の基本/Interfaceに置くべき文言と30の物理Procedureを分離 |
| `30_90` | 恒常的Test/Verification要求、E10固有test path | Contract obligationsはStock可。Gate実施結果／過去Enh経緯はFlowへ |
| `30_99` | CHANGE LOG | Flowへ移管 |

これらは「Classの7区分に適合させれば終わる」種類の問題ではない。**そもそもの文書種別・責務配分の見直し**が必要である。

## 5. Class単位の是正Definition of Done

- 明示されたClass/Protocol/DTO一覧を、各Source/ADR/Versionに対応付けてInventory化。
- 各Classは1つの`### X.Y. ClassName`に統合し、`#### X.Y.1`〜`X.Y.7`の**7節**を必須とする。
- Field表は`Field / Type / Default・生成元 / 可変性 / 制約`を省略しない。ExistingはSource上のDefault/Typeを照合。
- Constructor/Factoryは型付きSignatureと例外/不変条件を明記。Dataclass自動initもその事実とN/Aを明記。
- Method表は`Signature / Return / 処理 / 副作用 / 例外`、PureなMethodは`None / N/A理由`と明記。
- 処理仕様はPre/Post、分岐、状態遷移、数値的制約を分ける。
- I/Oは呼出元/先・Schema Version・Transaction・Retry/Rollback・failure/atomicを分ける。
- Unit/Contract/Negative Test、FR/NFR/AR、Gate、Source SHAを証拠に紐づけ、実行前はNOT_RUNとする。
- Proposedで実装Class名・SignatureがOwner未確定なら`PROPOSED / FREEZE_PENDING`と明記し、存在しているかのように書かない。

**結論:** 現時点でDD-01の**設計案採用**は有効だが、指定されたClassテンプレートを満たした**物理詳細設計完成**とは判定できない。独立Architecture Reviewに移る前にこの再記述が必要である。
