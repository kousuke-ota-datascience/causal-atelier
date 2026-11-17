# ENH-E11 G10 P05 — compatibility_evidence

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G10 / **Package:** P05 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P03,P04  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G10_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G10_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy/license evidence・顧客Legal非認定。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** 41 Method/10 UCの再実行・Manifest/依存・科学証拠・旧v2互換を統合する。

**科学/Designの必須制約:** 各GateのScience999を省略しない。GPLの顧客個別License判断は別。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 旧causal-analysis-spec/2/CLI/Web/API/Worker/DB非破壊、privacy/license evidence・顧客Legal非認定。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | Port/Value/Facade integration (no duplicate implementation) | authorize(self, *, study:ValidatedStudy, cli_row_flag:bool, root:TrustedLocalRoot, principal:LocalPrincipal, policy:VerifiedStudyPolicyEvidence|None, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Constructor/FieldsはDD30_61〜63のClass sectionを守り、未知のConcrete引数を創作しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent source)

以下のInstance Fields/Constructor/Method/Failureは本Packageの規範。外部DD参照はProvenanceのみ。Designed Classが実在する証拠ではないのでSource/ABIを実行時検証する。

### 3.1. `LocalCausalUseCase` — complete Class method protocol

### 1.1. 識別情報・責務

- **Class:** `ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。既存Product Stage runnerとは別のLocal Class契約である。
- **責務:** versioned Local Studyのpreflight→identification→method eligibility→adapter execution→staging→publish→readbackを順序付け、科学的Negativeとtechnical failureを混同しない。
- **責務外:** Scientific Estimatorの数学本体、Product DB/UoW/Worker/Web API、実行済み独立Science PASSの宣言。
- **関連契約:** 23_41 §3〜5、23_42 §2/6/7、30_61 §1〜5、30_60 §11〜12、30_62 §7。

### 1.2. フィールド

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
| `policy_verifier` | `LocalPolicyVerifierPort` | composition root | immutable; preauthorization from independent authority |
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context：** `ariadne.capabilities.causal.local_execution.LocalRunContext`は`root: TrustedLocalRoot`、`principal: LocalPrincipal`、`cli_row_flag: bool`、`policy_anchor: TrustedPolicyAnchor|None`を持つimmutable value。OS Root/Principalの型Authorityは`ariadne.shared.local_fs`、生成責務はCLI composition rootのTrustedRoot Factory。現行CLIの入力ContentRefと出力Bundleは同じRoot下の異なる相対keyで扱う。Policy AnchorはCLI composition rootがStudy外のsecure runtime trust configurationから取得する。G01集計専用のとき`policy_anchor=null`を許容するが、行出力要求では欠落を拒否する。Study YAMLからContextの信頼属性を構築してはならない。

**Application Port配置：** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`、`ariadne.capabilities.causal.ports.local_io.LocalPublicationPort/LocalManifestReaderPort`、`ariadne.capabilities.causal.ports.local_policy.LocalPolicyVerifierPort`、`ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`。`LocalPrivacyPolicy` ConcreteはLocalPrivacyPolicyPortの実装であり、ApplicationはCLI Concreteをimportしない。Policy verifierはStudyと独立のTrust Anchorで事前承認証拠を検証する。

### 1.3. Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`discovery: DiscoveryPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`reader: LocalManifestReaderPort`、`policy_verifier: LocalPolicyVerifierPort`、`privacy: LocalPrivacyPolicyPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, policy_verifier: LocalPolicyVerifierPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。公開ApplicationはPort抽象にのみ依存する。
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. 失敗は契約に対応する型付きErrorとして返す。
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

### 1.4. メソッド

~~~python
def preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport: ...
def run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: ValidatedStudy, context: LocalRunContext) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: ValidatedStudy, context: LocalRunContext) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

### 1.5. 処理仕様

1. CLI composition rootが`schema_version`を明示dispatchし、strict YAML/JSON parseで`ValidatedStudy`を構築。旧v2と無版はE11解釈禁止。ApplicationはValidatedStudyを受け取る（再検証するべきInput/Ref/Method/Privacyの意味検査は実行する）。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. 選択済CapabilityをOperation別のValidated Requestに束縛する。`DISCOVER`では`DiscoveryPort.discover(ValidatedDiscoveryRequest, *, sink)`を呼び、同一Method Registryから解決したFCI Adapterを使用する。Identificationを要求せず、未確定Graphを識別済みと扱わない。その他OperationはIdentifier/Estimator/Diagnostic Portへ明示dispatchする。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. 23_42 §2.1のOperation別必須/禁止Artifactとschema_dispatchを検証し、typed Graph/Identification/Effect/Diagnostics、Status/Manifestを生成。`context.policy_anchor`を使って独立Policy verifierが取得した承認証拠、Study、CLI row flag、`context.principal`・Output shapeを`LocalPrivacyPolicyPort.authorize`で照合し、staging seal→一括publish→独立Reader readbackを行う。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

**Precondition:** Input Spec passed strict schema/version check and trusted content refs. **Postcondition:** either immutable fully validated bundle with commit marker, or typed non-success/negative without false completed marker. Method/estimand/Graph conditional result is never guessed from a Backend label.

### 1.6. I/O・連携・失敗処理

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

- **I/O:** reads via ContentReferencePort, writes only via StagingArtifactSink/LocalPublicationPort. Each run has pinned request/content hash and effective API/seed evidence.
- **Transactions:** This is a Local FS unit, not a Product UoW. Publication atomicity and crash recovery specified in §3 and IF 23_42.
- **Errors:** invalid config/schema, missing/mismatched refs, unsupported capability, scientific negative, runtime failure and publication failure remain separately typed. **Retry/rollback:** idempotent same-hash readback allowed; another request hash with same run ID rejected; uncommitted staging never advertised as success.

### 1.7. 検証

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

| Acceptance | Required |
| --- | --- |
| Unit/Contract | Preflight performs zero Backend scientific calls; run calls Estimator only for proven eligible request; payload/status axes preserved |
| Negative | wrong version, hash mismatch, Graph uncertainty, unsupported CI, unavailable extra, no row export flag, publication failure |
| Regression | old v2 identify/estimate/refute/sensitivity and existing Product Stage runner unchanged |

**検証契約:** DD-E11-RUN01〜RUN07。関連要件：FR-185/187/201/202/203、NFR-029/032/036、AR-029/034/040。

### 3.2. `LocalManifestReader` — complete Class method protocol

### 5.1. 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader`。
- **責務:** committed runをMarker→Manifest→Artifactの順に検証し、`VerifiedLocalRun`を返す。存在だけでCOMMITTEDと判断しない。
- **責務外:** publish、legacy v2の無断E11解釈、科学的Oracle計算、実Artifactの編集。
- **参照:** IF `23_42` §6〜8。

### 5.2. フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| Instance fields | N/A（stateless Reader） | N/A | trusted root/run IDはper-call引数。Cacheが必要なら原本Root・run IDとhash一致を保持し、未検証値の再利用を禁止 |

### 5.3. Constructor / Factory

- `__init__()`は特別な依存なし（read_runへ検証済み`TrustedLocalRoot`を明示注入するstateless API）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

### 5.4. メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

### 5.5. 処理仕様

1. Trusted root・run_idとlocal execution principalを検証し、run directoryにsecure open。
2. `_COMMITTED.json`存在/strict schema/version/request hashを確認。
3. `manifest.json`を同一安全dirfd scopeでopen、markerに保存されたManifest SHA256と照合し、`LocalRunManifest`をstrict decode。
4. Artifactの相対key重複、SHA256/size/MediaType、privacy class、必要なLineage Refの一致を検査。
5. Private Parquetには出力Policy/OS principalの許可なしでrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

### 5.6. I/O・連携・失敗処理

- **Caller:** Local causal UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

### 5.7. 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。関連要件：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

### 3.3. `LocalPrivacyPolicy` — complete Class method protocol

### 6.1. 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy`。
- **責務:** row-level exportのrelease条件をANDで評価し、aggregated defaultと最小限の出力対象を固定する。Product RBACをLocal OSへ擬似的に持ち込まない。
- **責務外:** 研究対象者の同意獲得、Product ProjectMembership、Backend numerical inference、Customer Legal approval。

### 6.2. フィールド

**Instance Field：なし。** `LocalPrivacyPolicy`は単一の純粋なPolicy Evaluatorであり、runごとの`principal_uid`、`root_owner_uid`、`classification`、`row_export_requested`、`authorization_evidence`、`allowed_columns`、`max_rows`、`audit_context`を状態として保持しない。各値は信頼された`study`、`root`、`principal`、`policy`、`output_shape`からcall単位で得る。これによりApplicationの再利用可能なstateless UseCaseと両立する。

### 6.3. Constructor / Factory

`__init__(self) -> None`。外部I/O、run情報、Policy Snapshot、Backendを保持・読み込まない。ConcreteはCLI composition rootが`LocalPrivacyPolicyPort`へ依存注入する。実行時のactor/rootは`LocalRunContext`、事前承認は独立Policy verifierが生成する`VerifiedStudyPolicyEvidence`に由来し、CLI flagやStudy自身を信頼主体に昇格させない。

### 6.4. メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `authorize(self, *, study: ValidatedStudy, cli_row_flag: bool, root: TrustedLocalRoot, principal: LocalPrincipal, policy: VerifiedStudyPolicyEvidence|None, output_shape: OutputShape) -> PrivacyDecision` | immutable typed allow / reject | 23_41の公開Portと完全同一署名。純粋Policy、File公開副作用なし |
| `filter_export_columns(self, frame_schema: ColumnSchema, *, decision: PrivacyDecision) -> ColumnSelection` | bounded allowlist | 上記Decisionがrow releaseを許すときにのみ使用。未知・禁止列を拒否 |

`filter_export_columns`はRaw DataFrameではなくColumnSchemaと検証済みDecisionから許可列集合を導出する。行数制限はOutput writerとReaderの両方で再検証し、`PrivacyDecision`に上限・許可列・Policy digestを結び付ける。

### 6.5. 処理仕様

`authorize`は集計結果には個票を含まないこと、root/actorが適格であることを確認する。個票出力を許可する場合はStudyからの明示request ∧ CLI flag ∧ Studyから独立した事前承認済み`VerifiedStudyPolicyEvidence`（scope/columns/row bound一致） ∧ OS Principal/owner/delegation適格 ∧ root permissions ∧ classification/column/minimum-row policy の全条件をrequire。Fail-closedで個票Parquetを生成しない。通常のResult/Manifest/stdout/logにrow valuesを含めない。Shared mount、root container、CI volumeにおける可視性はOS File Modeだけで推測しない。

### 6.6. I/O・連携・失敗処理

- **Input:** `ValidatedStudy`（元CLI `LocalStudySpec`）, CLI intent, runtime principal/effective UID, trusted root/owner/ACL/mount証拠, independently verified policy, output shape/column Schema。
- **Output:** allow/reject（含むReason）と許可されたColumnSelection。Raw rows不要。
- **Side effect:** N/A（純粋Policy）。File create/0600・dir0700とaudit event emissionはPublisher/CLI adapterの責務。
- **Failure:** missing flag、UID mismatch、shared accessible mount、unauthorized column、rows limit、secret/row data leak。No retryで許可状態を推測しない。

### 6.7. 検証

`DD-E11-PRIV01` default no rows、`PRIV02` flag alone deny、`PRIV03` UID mismatch、`PRIV04` 0600/0700、`PRIV05` stdout/log leakage、`PRIV06` shared mount deny、`PRIV07` allowed-columns minimization。関連要件：FR-194/195/203、NFR-031/032、AR-034/035、BD01-F05/F12。

## 4. Required implementation — G10/P05 replay and science boundaries

1. **Entry:** G10 06/07/Pxx Frozen、all required G01〜G09 latest canonical 999 PASS、Owner Coding Authorization、full Source/lock/environment SHA、Pxx checkpointを検証。未成立Gateを仮PASSとして扱わない。
2. 旧Product v2のScientificCorePort/CLI DTO/GraphVersion/Legacy run_* signatureを現物と比較し、Public Signature/Schema/Exit Code/Behavior Regressionを実行。
3. 既存`tests/product/`, `tests/integration/`, `tests/scientific/`等のcurrent suiteを現配置で収集し、G01〜G09 protected invariantsと全10 Use Caseを確認する。勝手なmigrationやregression promotion禁止。
4. Methodごとのdistribution/version/optional dependency/License SBOMと実際に利用・配布するComponentを照合。GPLの一般的な性質だけで顧客個別delivery許可を判断しない。
5. 実証できない環境/Profile、No License approval、Backend ABI mismatch、Replay mismatch、Regression failureを個別FAIL/BLOCKEDとして残し、G10 PASSの根拠なしに正本ドキュメント昇格しない。
7. **Boundaries:** Value/Scientific typed Ports→G01 StagingSink/Atomic Publisher/Readerを使い、CLI専用Scientific Kernel、未承認Row export、old v2破壊、Unknown Backendへのfallbackを禁止。科学的・技術的Statusは独立。
8. **Output/Evidence:** Method/Operation/Version/Backend/Profile/Source/Fixture/Oracle/seed/CI/Privacy/Manifest/Result SHA、実行時のenvironment、negativeとaccepted/rejected Reasonを残す。Independent 07/999は本Packageが代行しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Proof:** 正例は10_32のDGP/ACに基づく独立Reference、負例は10_32のNEG/Reasonで検証。Backend自身の出力を真値にしてはならない。FWER=.05、K/R/Compute/MC-SE/CI coverageはMethod-specific 07/independent Pilotが確定してから測定する。未確定状態はMUSTの省略理由にならずBLOCKED/Openとして引き継ぐ。

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
- **Target-specific mandatory cases:** 旧Product v2のScientificCorePort/CLI DTO/GraphVersion/Legacy run_* signatureを現物と比較し、Public Signature/Schema/Exit Code/Behavior Regressionを実行。 既存`tests/product/`, `tests/integration/`, `tests/scientific/`等のcurrent suiteを現配置で収集し、G01〜G09 protected invariantsと全10 Use Caseを確認する。勝手なmigrationやregression promotion禁止。 Methodごとのdistribution/version/optional dependency/License SBOMと実際に利用・配布するComponentを照合。GPLの一般的な性質だけで顧客個別delivery許可を判断しない。 実証できない環境/Profile、No License approval、Backend ABI mismatch、Replay mismatch、Regression failureを個別FAIL/BLOCKEDとして残し、G10 PASSの根拠なしに正本ドキュメント昇格しない。
- P04は§5の全41 MethodについてDGP/NEG/REF/DDと独立数値/構造Oracleを判定する。P01〜P03/P05はScopeに関係するMethod/Result保護義務を保持し、科学Kernelを再実装しない。
- Actual fixture/Source/lock/Backend/API/SBOM SHA、Test layer/lifecycle、collected command、Observed/Expected、Quantitative Science K/R/MC-SE、PASS/FAIL/BLOCKED Reasonを記録。未実施をPASSとすることは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Explicit design/Science/Legal Freeze conditions

Class Fields/Constructors/Public Methodの実行意味は§3、Method固有処理は§4、Method/DD/Science義務は§5〜6に収める。外部DDから不足仕様の推論をCoding Agentに強制しない。**Freeze blockers:** protected v2 suite、actual SBOM/License、delivery者別Legal判断とall upstream canonical 999。 OwnerまとめReviewがこれらを判定するまでNo Coding Authorization/No Science PASS/No canonical promotion。
