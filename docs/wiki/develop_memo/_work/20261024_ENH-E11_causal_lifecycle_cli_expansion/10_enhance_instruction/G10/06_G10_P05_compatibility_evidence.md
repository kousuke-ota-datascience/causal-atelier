# ENH-E11 G10 P05 — compatibility_evidence

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G10 / **Package:** P05 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P03,P04  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G10_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G10_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy・Method依存version照合（外部顧客Legalは別判定）。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 41 Method/10 UCの再実行・Manifest/依存・科学証拠・旧v2互換を統合する。

**科学/Designの必須制約:** 各GateのScience999を省略しない。GPLの顧客配布時の手動License審査は内部分析Gate外。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy・Method依存version照合（外部顧客Legalは別判定）。

### 2A. 41 Method横断Reuseと既存ABIの実在確認（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter`は`run_discovery(DiscoveryInput, Path)`、`run_identification(IdentificationInput, Path)`、`run_estimation(EstimationInput, Path)`、`run_refutation(RefutationInput, Path)`、`run_sensitivity(SensitivityInput, Path)`の公開ABI（返値はいずれも`list[ScientificResultDescriptor]`）。対応実体は`scientific/discovery|identification|inference|refutation|sensitivity/adapter.py`の各`run(input_, output_dir)`。これらは旧Product Path APIであり、E11の`Discovery/Identification/Estimator/DiagnosticPort`のtyped Request/Outcomeとは互換性を自動仮定しない。
- **横断責務:** G10は41 Method×Operation/Estimand/Backend/Result/Manifestの再実行と統合検証を所有するが、科学計算Kernel、G01 Registry、GraphVersion writer、Publisher、Reader、G05 local executor double-opt-in eligibilityを複製しない。旧ABI・Product v2を変更せず、既存upstream Gateの同一Class・Method profileを参照する。Sourceに存在しないE11新規Classを「導入済み」と呼ばない。
- **科学的Boundary:** G10の横断テストには全41 MethodのDGP/NEG/独立REF、実効Backend/lock/fixture SHA、Source/Environment/seed、preregistered K/R/MC-SE/coverage/threshold、FWER=.05とMethod別Inference profileが必要。未決は該当MethodのBLOCKED、G10全体のGate PASS禁止。

### 2B. Standalone Operation/Result/Manifest契約
| Operation | 必須Artifact | 禁止・Negative |
|---|---|---|
| DISCOVER | `study.json`・`status.json`・Graph成功なら`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`と理由必須、`schema_dispatch.graph=null`。Backend失敗との混同禁止 |
| IDENTIFY | `study.json`・`status.json`・`identification.json` | Effect `result.json`禁止。非識別もtypedでGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`・`status.json`・`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、科学PASSと混同禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`・`status.json`・`diagnostics.json` | Effectの再発行禁止、元Effect/Graph/Design hash、seed/適用条件の照合 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）、ただし両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key、実bytes SHA256/size/MediaType/Privacyを網羅。 `request_hash=SHA256(JCS(validated typed Study JSON))`。Manifestに自己hashを格納せず、Markerの`manifest_sha256`にManifest実bytes hashを保存。ReaderはMarker→Manifest→実File→Operation/Profile→上流hashをTrustedRootで検証し、一致しない未コミット/破損データを拒否。Outputは既存G01のStaging→同一FS atomic no-clobber publish、個票bytesはG05のStudy＋CLI二重opt-in/OS適格性確認以前に生成禁止。各Methodのpoint/uncertainty/science_acceptance/statusを別軸で保持し、計算成功はScience PASSでない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | Port/Value/Facade integration (no duplicate implementation) | authorize(self, *, study:ValidatedStudy, cli_row_flag:bool, root:TrustedLocalRoot, principal:LocalPrincipal, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降に埋め込んだClass Field/Constructor/Public Methodが実装の一次規範。外部DDは履歴/Provenanceのみであり、unknown Concrete型/Backend/Runtime値を補完しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent source)

以下のInstance Fields/Constructor/Method/Failureは本Packageの規範。外部DD参照はProvenanceのみ。Designed Classが実在する証拠ではないのでSource/ABIを実行時検証する。

### 3.1. `LocalCausalUseCase` — complete Class method protocol

#### 識別情報・責務

- **Class:** `ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。既存Product Stage runnerとは別のLocal Class契約である。
- **責務:** versioned Local Studyのpreflight→identification→method eligibility→adapter execution→staging→publish→readbackを順序付け、科学的Negativeとtechnical failureを混同しない。
- **責務外:** Scientific Estimatorの数学本体、Product DB/UoW/Worker/Web API、実行済み独立Science PASSの宣言。
- **関連契約:** 23_41 §3〜5、23_42 §2/6/7、30_61 §1〜5、30_60 §11〜12、30_62 §7。

#### フィールド

**Constructor-injected Port fields:**

| Field | Type | Value origin | Mutable / constraint |
| --- | --- | --- | --- |
| `refs` | `ContentReferencePort` | composition root | immutable; trusted-root hash-bound read |
| `capabilities` | `MethodCapabilityPort` | composition root | immutable; effective profile and no silent fallback |
| `discovery` | `DiscoveryPort` | composition root | immutable; selected capabilityに束縛されたGraph Discovery |
| `identifier` | `IdentificationPort` | composition root | immutable; Domain proof/negative outcome |
| `estimators` | `EstimatorPort` | composition root | immutable; typed scientific result to staging |
| `diagnostics` | `DiagnosticPort` | composition root | immutable; method-specific typed diagnostics |
| `reader` | `LocalManifestReaderPort` | composition root | immutable; independent committed run readback |
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context:** `LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal,cli_row_flag:bool)`。G10はStudy＋CLI double opt-inと実行UID/TrustedRoot、Method RowSchemaの適合を検証。署名用Policy Anchorはない。

**Application Port配置:** `ContentReferencePort`、`LocalPublicationPort`/`LocalManifestReaderPort`、`LocalPrivacyPolicyPort`。ApplicationはPortにのみ依存。

#### Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs:ContentReferencePort`、`capabilities:MethodCapabilityPort`、`discovery:DiscoveryPort`、`identifier:IdentificationPort`、`estimators:EstimatorPort`、`diagnostics:DiagnosticPort`、`publisher:LocalPublicationPort`、`reader:LocalManifestReaderPort`、`privacy:LocalPrivacyPolicyPort`、`runtime:RuntimeEnvironmentPort`、`clock:ClockPort`。

- **Constructor signature:** `__init__(self, *, refs:ContentReferencePort,capabilities:MethodCapabilityPort,discovery:DiscoveryPort,identifier:IdentificationPort,estimators:EstimatorPort,diagnostics:DiagnosticPort,publisher:LocalPublicationPort,reader:LocalManifestReaderPort,privacy:LocalPrivacyPolicyPort,runtime:RuntimeEnvironmentPort,clock:ClockPort)`。
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. 失敗は契約に対応する型付きErrorとして返す。
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

#### メソッド

~~~python
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

#### 処理仕様

1. CLI composition rootが`schema_version`を明示dispatchし、strict YAML/JSON parseで`ValidatedStudy`を構築。旧v2と無版はE11解釈禁止。ApplicationはValidatedStudyを受け取る（再検証するべきInput/Ref/Method/Privacyの意味検査は実行する）。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. 選択済CapabilityをOperation別のValidated Requestに束縛する。`DISCOVER`では`DiscoveryPort.discover(ValidatedDiscoveryRequest, *, sink)`を呼び、同一Method Registryから解決したFCI Adapterを使用する。Identificationを要求せず、未確定Graphを識別済みと扱わない。その他OperationはIdentifier/Estimator/Diagnostic Portへ明示dispatchする。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. 本書§2BのOperation別Artifact/typed Result/Status、Lineage、Privacyを検証。G05の個票を要求する場合だけStudy＋CLI opt-in/非root UID所有private ext4/XFS/Method RowSchemaを満たすことを確認し、G01 Publisher/Readerへ渡す。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

**Precondition:** Input Spec passed strict schema/version check and trusted content refs. **Postcondition:** either immutable fully validated bundle with commit marker, or typed non-success/negative without false completed marker. Method/estimand/Graph conditional result is never guessed from a Backend label.

#### I/O・連携・失敗処理

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

- **I/O:** reads via ContentReferencePort, writes only via StagingArtifactSink/LocalPublicationPort. Each run has pinned request/content hash and effective API/seed evidence.
- **Transactions:** This is a Local FS unit, not a Product UoW. Publication atomicity and crash recovery specified in §3 and IF 23_42.
- **Errors:** invalid config/schema, missing/mismatched refs, unsupported capability, scientific negative, runtime failure and publication failure remain separately typed. **Retry/rollback:** idempotent same-hash readback allowed; another request hash with same run ID rejected; uncommitted staging never advertised as success.

#### 検証

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

| Acceptance | Required |
| --- | --- |
| Unit/Contract | Preflight performs zero Backend scientific calls; run calls Estimator only for proven eligible request; payload/status axes preserved |
| Negative | wrong version, hash mismatch, Graph uncertainty, unsupported CI, unavailable extra, no row export flag, publication failure |
| Regression | old v2 identify/estimate/refute/sensitivity and existing Product Stage runner unchanged |

**検証契約:** DD-E11-RUN01〜RUN07。関連要件：FR-185/187/201/202/203、NFR-029/032/036、AR-029/034/040。

### 3.2. `LocalManifestReader` — complete Class method protocol

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`。
- **責務:** committed runをMarker→Manifest→Artifactの順に検証し、`VerifiedLocalRun`を返す。存在だけでCOMMITTEDと判断しない。
- **責務外:** publish、legacy v2の無断E11解釈、科学的Oracle計算、実Artifactの編集。
- **参照:** IF `23_42` §6〜8。

#### フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| Instance fields | N/A（stateless Reader） | N/A | trusted root/run IDはper-call引数。Cacheが必要なら原本Root・run IDとhash一致を保持し、未検証値の再利用を禁止 |

#### Constructor / Factory

- `__init__()`は特別な依存なし（read_runへ検証済み`TrustedLocalRoot`を明示注入するstateless API）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

#### 処理仕様

1. Trusted root・run_idとlocal execution principalを検証し、run directoryにsecure open。
2. `_COMMITTED.json`存在/strict schema/version/request hashを確認。
3. `manifest.json`を同一安全dirfd scopeでopen、markerに保存されたManifest SHA256と照合し、`LocalRunManifest`をstrict decode。
4. Artifactの相対key重複、SHA256/size/MediaType、privacy class、必要なLineage Refの一致を検査。
5. Private Parquetには出力Policy/OS principalの許可なしでrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

#### I/O・連携・失敗処理

- **Caller:** Local causal UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

#### 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。関連要件：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

### 3.3. `LocalPrivacyPolicy` — complete Class method protocol

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy`。
- **責務:** row-level exportのrelease条件をANDで評価し、aggregated defaultと最小限の出力対象を固定する。Product RBACをLocal OSへ擬似的に持ち込まない。
- **責務外:** 研究対象者の同意獲得、Product ProjectMembership、Backend numerical inference、Customer Legal approval。

#### フィールド

**Instance Field：なし。** `LocalPrivacyPolicy`は単一の純粋なPolicy Evaluatorであり、runごとの`principal_uid`、`root_owner_uid`、`classification`、`row_export_requested`、`authorization_evidence`、`allowed_columns`、`max_rows`、`audit_context`を状態として保持しない。各値は信頼された`study`、`root`、`principal`、`policy`、`output_shape`からcall単位で得る。これによりApplicationの再利用可能なstateless UseCaseと両立する。

#### Constructor / Factory

`__init__(self)->None`。Pure stateless LocalPrivacyPolicy。検証済みStudy/CLI flag・OS principal/root・Method出力Shapeに基づき行出力を評価し、独立署名ProofやKey Storeは不要。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `authorize(self, *, study: ValidatedStudy, cli_row_flag: bool, root: TrustedLocalRoot, principal: LocalPrincipal, output_shape: OutputShape) -> PrivacyDecision` | immutable typed allow / reject | 23_41の公開Portと完全同一署名。純粋Policy、File公開副作用なし |
| `filter_export_columns(self, frame_schema: ColumnSchema, *, decision: PrivacyDecision) -> ColumnSelection` | bounded allowlist | 上記Decisionがrow releaseを許すときにのみ使用。未知・禁止列を拒否 |

`filter_export_columns`はRaw DataFrameではなくColumnSchemaと検証済みDecisionから許可列集合を導出する。行数制限はOutput writerとReaderの両方で再検証し、`PrivacyDecision`に上限・許可列・Policy digestを結び付ける。

#### 処理仕様

`authorize`は集計結果へ個票を含めず、G05個票出力時にはStudyの明示要求 ∧ CLI flag ∧ 実行者EUIDが所有するprivate TrustedRoot（Linux local ext4/XFS、適切な0700/0600・owner/mode/local ext4-XFS） ∧ Method別ApprovedRowSchema・列/行/byte/memory上限をAND評価する。条件不成立ならfail-closedでRowSourceを反復せず個票bytesを生成しない。Result/Manifest/stdout/logへ行値を含めない。非root EUID、private owner-only root、local ext4/XFS、same-FS、dirfd/path適格性の不成立は拒否する。独立ACL/namespace証明が不明という理由だけでは拒否しない。

#### I/O・連携・失敗処理

- **Input:** `ValidatedStudy`（元CLI `LocalStudySpec`）, CLI intent, runtime principal/effective UID, trusted root/owner/owner/mode/FS証拠, independently verified policy, output shape/column Schema。
- **Output:** allow/reject（含むReason）と許可されたColumnSelection。Raw rows不要。
- **Side effect:** N/A（純粋Policy）。File create/0600・dir0700とaudit event emissionはPublisher/CLI adapterの責務。
- **Failure:** missing flag、UID mismatch、shared accessible mount、unauthorized column、rows limit、secret/row data leak。No retryで許可状態を推測しない。

#### 検証

`DD-E11-PRIV01` default no rows、`PRIV02` flag alone deny、`PRIV03` UID mismatch、`PRIV04` 0600/0700、`PRIV05` stdout/log leakage、`PRIV06` shared mount deny、`PRIV07` allowed-columns minimization。関連要件：FR-194/195/203、NFR-031/032、AR-034/035、BD01-F05/F12。

## 4. Required implementation — G10/P05 replay and science boundaries

1. **Entry:** G10 06/07/Pxx Frozen、all required G01〜G09 latest canonical 999 PASS、Owner Coding Authorization、full Source/lock/environment SHA、Pxx checkpointを検証。未成立Gateを仮PASSとして扱わない。
2. 旧Product v2のScientificCorePort/CLI DTO/GraphVersion/Legacy run_* signatureを現物と比較し、Public Signature/Schema/Exit Code/Behavior Regressionを実行。
3. 既存`tests/product/`, `tests/integration/`, `tests/scientific/`等のcurrent suiteを現配置で収集し、G01〜G09 protected invariantsと全10 Use Caseを確認する。勝手なmigrationやregression promotion禁止。
4. Methodごとの実効distribution/version/optional dependency/APIとlockを照合する。顧客配布時のみ実配布Component/Licenseを別途手動レビューする。内部CLIでSBOM生成や受領者別法務Evidenceは要求しない。
5. 実証できない必須環境/Profile、Backend ABI mismatch、Replay mismatch、Regression failureを個別FAIL/BLOCKEDとして残し、G10 PASSの根拠なしに正本ドキュメント昇格しない。
6. **Boundaries:** Value/Scientific typed Ports→G01 StagingSink/Atomic Publisher/Readerを使い、CLI専用Scientific Kernel、未承認Row export、old v2破壊、Unknown Backendへのfallbackを禁止。科学的・技術的Statusは独立。
7. **Output/Evidence:** Method/Operation/Version/Backend/Profile/Source/Fixture/Oracle/seed/CI/Privacy/Manifest/Result SHA、実行時のenvironment、negativeとaccepted/rejected Reasonを残す。Independent 07/999は本Packageが代行しない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

Adapterは`ariadne.scientific.causal_methods`に配置し、共通の`ariadne.causal.discovery`・`ariadne.causal.inference`内の既存計算を意味互換で再利用する。新しいFCI/IV/CATE等はMethod固有の新実装が必要な場合のみ追加する。Typed Port=`ariadne.scientific.ports.causal`、Capability Port=`ariadne.scientific.ports.capability`、BackendEvidence=`ariadne.scientific.capabilities`。旧Product `ScientificCorePort.run_*`は公開v2 DTO/Pathの署名を維持し、実装移行時は明示Bridgeから同一科学Kernelを呼ぶ。旧v2の型へAR/PAG/識別状態を損失変換してはいけない。

22 Adapter Class中、`ariadne.scientific.refutation.adapter.RefutationAdapter`と`ariadne.scientific.sensitivity.adapter.SensitivityAdapter`は既存実装であり、旧`run(input_,output_dir)`署名を変更しない。その他のClassはMethodごとのClass契約として定義し、既存ClassのABIを無条件に変更しない。いずれも入口専用の独立数値実装を持つことは認めず、既存`causal.discovery`/`causal.inference`と`scientific.*`の関数・validationを再利用する。

`MethodDescriptor`の唯一のOwnerは`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。`StageRunnerRegistry`のStageType registryと同一視しない。旧Product `ScientificCorePort`の5 Operation署名を維持し、Method別typed Portが同じ科学的Kernelを利用する明示Bridgeを介する。新しいFCI、LATE/AR、CATE、Temporal、Quasiは既存の科学実装で不足する部分だけを別Method Adapterとして追加する。

22 Classの実装ModuleとMethodの対応は§1、41 Methodの対象と制約は§2〜§8がAuthorityである。Backend distribution/API availability・Optional Dependency・LicenseはMethodRegistryと独立Runtime probeで検証し、未取得EvidenceをAVAILABLEや科学的PASSにしない。

`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)`が実行者のdouble opt-inとOS TrustedRoot/Method別出力適格性を判定する。独立Approver/Ed25519/鍵/失効/TrustedPolicyAnchorは初期G05 local個票中間成果物には適用しない。事前の行生成禁止、同一run/Study/Source/Sinkの結合、staging前・seal/publish前のroot/UID/owner/mode/FS再照合を維持し、不適格ならexit3で初期row bytes0。既存G01 Publisher/ReaderとOD-03 WriterのClass/Method署名は不変。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。


**OD-01/02/03/05（2026-11-19 Owner採用）との横断一致規範：**

- `P1-M05`はG02で`IDENTIFY`専用、明示的`B0_BINARY_IV` binary Z/A unadjusted `LATE_COMPLIER`条件付き識別。DoWhy IV internal label/`nonparametric-ate`だけでLATE証明とせず、宣言済みrelevance/exclusion/independence/monotonicity/consistency、Graph/Question/Design/Content hashとeffective APIを検証。`IDENTIFY`のEffect `result.json`は禁止。G08のB0数値推定/B1 slope/DRIVと混同しない。DGP-006、NEG-006/007、REF-I03/REF-G01は別科学Evidence。
- G05 restricted Row ParquetはStudy個票要求とCLI flagのdouble opt-in、Linux非root実効EUID所有private ext4/XFS root（0700/0600、owner/mode/local ext4-XFS/同一FSを検証）、Method別ApprovedRowSchema/ordered column/row/byte/memory capsに合致する場合だけ、認可後の`RowEffectsParquetWriter`がG01 StagingSinkに遅延生成する。初期denyはexit3/Source反復0/row bytes0。署名鍵・独立承認者・失効はOwner 2026-11-21限定改訂で不要。G01 Publisher/Readerが唯一の公開/readback authority。実FS/Parquet/Method RowSchemaの実測未完はBLOCKED。
- OD-05の40 Method専用Config/Question/Design/Output/Inference Profileは各Owner Gate（G02=6、G03=13、G04=8、G06=3、G07=3、G08=5、G09=2）で完成・登録されるまでは`METHOD_PROFILE_UNAVAILABLE`で該当Methodをfail-closed。P1-M06のG01 Draftを除く40件を`config={}`で一括許可しない。G10は全41 Methodの実Backend/Lock/独立DGP/NEG/REF/CI/Regressionを検証するのみ。
- 全決定は設計選択としてOwner採用済みであり、実Source/Test/uv.lock、実効Backend/独立Science、Contract Freeze、Coding Authorization、Customer delivery legal acceptance（配布時のみ）を意味しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof boundary:** G10の全41 Methodの§5 DGP/NEG/REF/ACは検証対象であり、Listが存在するだけで実Fixture/Oracle生成済みやScience PASSを意味しない。独立Reference/Generatorを事前固定し、FWER=.05とMethod別K/R/compute/MC-SE/coverageをFreeze前に確定する。未測定はBLOCKEDであり、Backendの出力を真値にしない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g10/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Package-focused acceptance and evidence matrix

- §4の各段階をunit/contract/実Backend・FS integrationで測定し、実在するlegacy product testsをcurrent checkoutからdiscoverして実行。Completion Reportのpath/commandを物理Authorityにしない。
- **Target-specific mandatory cases:** 旧Product v2のScientificCorePort/CLI DTO/GraphVersion/Legacy run_* signatureを現物と比較し、Public Signature/Schema/Exit Code/Behavior Regressionを実行。 既存`tests/product/`, `tests/integration/`, `tests/scientific/`等のcurrent suiteを現配置で収集し、G01〜G09 protected invariantsと全10 Use Caseを確認する。勝手なmigrationやregression promotion禁止。 Methodごとの実効distribution/version/optional dependency/APIとlockを照合する。顧客配布時のみ実配布Component/Licenseを別途手動レビューする。内部CLIでSBOM生成や受領者別法務Evidenceは要求しない。 実証できない必須環境/Profile、Backend ABI mismatch、Replay mismatch、Regression failureを個別FAIL/BLOCKEDとして残し、G10 PASSの根拠なしに正本ドキュメント昇格しない。
- P04は§5の全41 MethodについてDGP/NEG/REF/DDと独立数値/構造Oracleを判定する。P01〜P03/P05はScopeに関係するMethod/Result保護義務を保持し、科学Kernelを再実装しない。
- Actual fixture/Source/lock/Backend/API SHA、Test layer/lifecycle、collected command、Observed/Expected、Quantitative Science K/R/MC-SE、PASS/FAIL/BLOCKED Reasonを記録。未実施をPASSとすることは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit design/Science/Legal Freeze conditions

Class Fields/Constructors/Public Methodの実行意味は§3、Method固有処理は§4、Method/DD/Science義務は§5〜6に収める。外部DDから不足仕様の推論をCoding Agentに強制しない。**Freeze blockers:** protected v2 suite、実効Method/Backend/API/Lock、独立Science Evidenceとall upstream canonical 999。 OwnerまとめReviewがこれらを判定するまでNo Coding Authorization/No Science PASS/No canonical promotion。

### Owner SIM-01/03/04 initial-Gate simplification (2026-11-21)

Mandatory integration profiles are ENV-BASE, ENV-DOWHY, ENV-ECONML and ENV-TIGRAMITE, each with actual lock/distribution/API smoke and Method-specific science/reproducibility checks. ENV-COMBINED all-extras runtime/CI is an optional later interop check, **not** G10 initial PASS dependency; do NOT claim simultaneous all-extras environment is verified. Local scientific Manifest has NO required `runtime.sbom_ref` or `review.legal_delivery_status` (the active Draft 2020-12 Schema removed them); installed distribution/version/lock source provenance and independent science review evidence remain required. SBOM generation, per-customer authorization state and legal evidence are NOT G10 CLI runtime functionality. Prior to any actual customer external delivery, the Owner/legal reviewer must manually review actual shipped dependencies and block unapproved distribution. FS privacy boundary is ordinary nonroot Linux EUID/private owner-only ext4/XFS root with 0700/0600 and FD-safe paths/same FS; no separate ACL/xattr digest, mount namespace/ID proof or CI/container classification. Preserve G01 Publisher/Reader, NFR-030/031/032/033/035/036, all science, all Method ID targets, upstream Gate999 independence and Product v2. Historical DEC08/PREP02 remains historical, specifically superseded by combined_review/131. No runtime evidence / Gate999 PASS / Coding Authorization.
