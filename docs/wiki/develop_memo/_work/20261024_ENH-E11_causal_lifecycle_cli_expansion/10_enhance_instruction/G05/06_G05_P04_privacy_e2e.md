# ENH-E11 G05 P04 — privacy_e2e

### G05現行個票出力契約 — Owner 2026-11-21改訂

- **機能/範囲:** FR-195、NFR-031、P2-15。一般ユーザーがlocal Linux ext4/XFSで個票中間データを出力する場合、実行者がStudy requestとCLI flagで明示opt-inする。独立した人的承認者・暗号署名・鍵管理・承認失効はこの範囲に要求しない。
- **Privacy/OS:** EUIDが所有するprivate TrustedRoot、root/staging 0700、row file 0600、ACL/mount/namespace/symlink/dirfdとsame-FSを検査。rootと同一UIDのプロセスは隔離できない。個票は`RESTRICTED_ROW_LEVEL`に分類。
- **Eligibility:** `Study.privacy.row_export_requested=true` ∧ `--allow-row-level-export` ∧ private verified root/UID ∧ Method別`ApprovedRowSchema`/許可列・行ID・row/byte/memory上限 ∧ 同一runのG01 staging。初期denyはPrivacy exit3、Source反復0・row bytes0、暗黙aggregate fallback無し。通常集計は個票権限と独立。
- **内部Port:** `LocalRunContext(root,principal,cli_row_flag)`、`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,principal,output_shape)->PrivacyDecision`、`LocalCausalUseCase`に署名Verifier依存無し。`e11-local-study/1`の任意`privacy.policy_ref`は現行unsigned modeではnullのみ。
- **Writer:** 既決`RowEffectsParquetWriter.__init__(*,serializer,max_memory_bytes)`、`write(*,source,study,decision,selection,sink)->ArtifactDescriptor`、`RowEffectsWriterFactory.create(*,serializer,max_memory_bytes)`、`DeferredRowEffectsSource.schema/read_rows`、`ValidatedParquetSerializer.encode(*,rows,schema)->bytes`を維持。実行条件成立後だけread_rows、G01 Sink以外へ書かない。
- **Publication/test:** `row_effects.parquet`／`application/vnd.apache.parquet`のみG01 Publisher/Readerが原子的にpublish・readback。Stage/Seal/Publish前にroot/UID/mount/runを再検査、障害後にCOMMITTEDを偽装しない。個票値はaggregate Result/Manifest/CLI/logsへ出さない。未検証事項：Method RowSchema、実FS/Parquet、07独立Science/Privacy Test、Freeze、Coding Authorization。


**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G05 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02,P03  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G05_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G05_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。

**Scope:** Local intermediate row artifact only. Science CATE/DRIVの対象は変更せず、行出力はStudy＋CLI二重opt-inとnonroot private rootを満たす場合だけ。


Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** Denied時row bytes 0 / COMMITTED marker無し、shared mounts、root UID差、stdout/log leak負例。

### 2A. 既存SourceとRow Release authorityの境界（`2cf28f59a324`）
- **既存:** `src/ariadne/product/application/graph_version_service.py`の`GraphVersionService.create(...)`/`fix_graph(...)`はProduct GraphVersion Authorityであり、Local CLIが同名Publisher/Version writerを作って代替しない。`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(input_: EstimationInput, output_dir: Path)`は旧Path API、HTEと認可済Parquet Writerの実装済み証拠ではない。
**Input/output:** Studyはe11-local-study/1でpolicy_refはnull。run/Study/Data/Method ref hash、private ext4/XFS root、G01 stagingとReader一致を確認し、旧v2と混同しない。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | 禁止・negative条件 |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`＋nonempty reason、`schema_dispatch.graph=null`。Backend失敗との混同は禁止 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Effect `result.json`禁止。識別negativeもtyped、Graph/Design/Estimand/Proof hashを照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。point欠落はnull＋理由で表し、非識別への推定値偽装禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effect再発行禁止。上流Effect/Graph/Design hash、seed・適用条件の検証が必須 |


## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `LocalCausalUseCase` | `ariadne.capabilities.causal.local_execution.LocalCausalUseCase` | Port/Value/Facade integration (no duplicate implementation) | preflight(self,spec:ValidatedStudy,context:LocalRunContext)->PreflightReport / run(self,spec:ValidatedStudy,context:LocalRunContext)->LocalRunOutcome |
| `LocalPrivacyPolicy` | `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy` | Port/Value/Facade integration (no duplicate implementation) | authorize(self, *, study:ValidatedStudy, cli_row_flag:bool, root:TrustedLocalRoot, principal:LocalPrincipal, output_shape:OutputShape)->PrivacyDecision / filter_export_columns(self,frame_schema:ColumnSchema,*,decision:PrivacyDecision)->ColumnSelection |
| `LocalManifestReader` | `ariadne.interfaces.cli.local_causal.manifest_reader.LocalManifestReader` | Port/Value/Facade integration (no duplicate implementation) | read_run(trusted_root:TrustedLocalRoot,run_id:RunId) |

**Class boundary:** LocalPrivacyPolicyがStudy・CLI・EUID/TrustedRoot・Method ApprovedRowSchemaを検証する。RowWriter/Factoryは許可後Serializerだけを所有し、G01 Publisherは変更しない。

**Responsibility:** 本PackageはScientific Adapter数値本体を新規所有しない。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class/Method contracts (independent of external DD)

このPxxの実行に必要なClassのField/Constructor/Method/Process/Failureを以下に内包。外部DDはTraceabilityのみ。現行SourceとのABI差分は開始時に確認し、欠陥ならOwnerレビューに戻す。

### 3.1. `LocalCausalUseCase` — normative implementation contract

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

**Application Context:** `LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal,cli_row_flag:bool)`。一般EUID/private root/ACL/mountをCLI composition rootが検証し、StudyとCLI両方のopt-inで行生成適格性を評価する。

**Application Port配置:** `ContentReferencePort`、`LocalPublicationPort`/`LocalManifestReaderPort`、`LocalPrivacyPolicyPort`。Applicationが具体adapterを直接参照しない。

#### Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs:ContentReferencePort`、`capabilities:MethodCapabilityPort`、`discovery:DiscoveryPort`、`identifier:IdentificationPort`、`estimators:EstimatorPort`、`diagnostics:DiagnosticPort`、`publisher:LocalPublicationPort`、`reader:LocalManifestReaderPort`、`privacy:LocalPrivacyPolicyPort`、`runtime:RuntimeEnvironmentPort`、`clock:ClockPort`。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。公開ApplicationはPort抽象にのみ依存する。
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
7. Operation別の正しいGraph/Identification/Effect/Diagnostics/Statusを保持し、G05行出力はStudy＋CLI double opt-inとEUID/private root＋Method Schemaを検証した後だけG01 Sinkへ送る。
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

### 3.2. `LocalPrivacyPolicy` — normative implementation contract

#### 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy`。
- **責務:** row-level exportのrelease条件をANDで評価し、aggregated defaultと最小限の出力対象を固定する。Product RBACをLocal OSへ擬似的に持ち込まない。
- **責務外:** 研究対象者の同意獲得、Product ProjectMembership、Backend numerical inference、Customer Legal approval。

#### フィールド

**Instance Field：なし。** `LocalPrivacyPolicy`は単一の純粋なPolicy Evaluatorであり、runごとの`principal_uid`、`root_owner_uid`、`classification`、`row_export_requested`、`authorization_evidence`、`allowed_columns`、`max_rows`、`audit_context`を状態として保持しない。各値は信頼された`study`、`root`、`principal`、`policy`、`output_shape`からcall単位で得る。これによりApplicationの再利用可能なstateless UseCaseと両立する。

#### Constructor / Factory

`__init__(self)->None`。`LocalPrivacyPolicy`はstateless pure evaluator。OS principal/rootとStudy/CLI/Method出力適格性を評価し、行の実値を保持しない。

#### メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `authorize(self, *, study: ValidatedStudy, cli_row_flag: bool, root: TrustedLocalRoot, principal: LocalPrincipal, output_shape: OutputShape) -> PrivacyDecision` | immutable typed allow / reject | double opt-in＋private EUID-owned ext4/XFS root/Method-specific schema・row/byte bound/negative Source反復0/G01 Readback |
| `filter_export_columns(self, frame_schema: ColumnSchema, *, decision: PrivacyDecision) -> ColumnSelection` | bounded allowlist | 上記Decisionがrow releaseを許すときにのみ使用。未知・禁止列を拒否 |

`filter_export_columns`はRaw DataFrameではなくColumnSchemaと検証済みDecisionから許可列集合を導出する。行数制限はOutput writerとReaderの両方で再検証し、`PrivacyDecision`に上限・許可列・Policy digestを結び付ける。

#### 処理仕様

`authorize`は通常Resultへの個票混入を禁止し、G05行出力はStudy request∧CLI Flag∧EUID private ext4/XFS root∧Method別ApprovedRowSchema/column/rows/byte capを検証。fail closed。

#### I/O・連携・失敗処理

- **Input:** `ValidatedStudy`（元CLI `LocalStudySpec`）, CLI intent, runtime principal/effective UID, trusted root/owner/ACL/mount証拠, independently verified policy, output shape/column Schema。
- **Output:** allow/reject（含むReason）と許可されたColumnSelection。Raw rows不要。
- **Side effect:** N/A（純粋Policy）。File create/0600・dir0700とaudit event emissionはPublisher/CLI adapterの責務。
- **Failure:** missing flag、UID mismatch、shared accessible mount、unauthorized column、rows limit、secret/row data leak。No retryで許可状態を推測しない。

#### 検証

`DD-E11-PRIV01` default no rows、`PRIV02` flag alone deny、`PRIV03` UID mismatch、`PRIV04` 0600/0700、`PRIV05` stdout/log leakage、`PRIV06` shared mount deny、`PRIV07` allowed-columns minimization。関連要件：FR-194/195/203、NFR-031/032、AR-034/035、BD01-F05/F12。

### 3.3. `LocalManifestReader` — normative implementation contract

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

## 4. Required implementation — G05/P04 dedicated processing

1. **Entry:** G04 canonical 999 PASS、G05 Frozen06/07/Pxx、Owner Coding Authorization、Source/lock、依存Pxxを確認。G04のEffect/CATE/Graph/Studyが同一Hash/Version/Estimand対象であることを検証。
2. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
3. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
4. Authorized caseはG05/P03のParquet読戻し、列/行/Schema、manifest SHA、commit marker/row privacy metadataの一致を検証し、旧v2の非認可挙動を変更しない。
5. Study＋CLI double opt-in、nonroot Linux EUIDが所有するprivate ext4/XFS rootとMethod approved row schema/列行byte上限を検証。失敗時に個票Sourceを反復せずexit3。
6. **Privacy boundary:** 未承認・技術的失敗・Authority未定はzero-rowでstopし、許可ErrorをError suppressionやdummy Policyで回避しない。G01 Publisher/Readerは再実装しない。Optional Backend/Science Availabilityも分離する。
7. **Output:** Typed Decision/Evidence/Aggregate/Policy-bound Artifactを必要な場合のみStaging→Atomic Publisherへ渡す。既存Product ABIとException/Exit policyを保護する。

### 設計書で定義済みの実装意味論（本Packageの規範）

以下は既存30_62/30_63の設計規則のうち本Packageへ適用する本文内契約である。外部DDを読ませて仕様を補完することは禁止する。自Packageが所有しないClassは再実装しない。

**Method steps:** P02は拒否時Source反復0を保証。P03は許可されたRowSchema/column orderでmax_rows+1とbyte capを検査し、G01 sinkへstage。P04はOS/FS正常・異常双方をE2E。

Applicationの`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`を用いるFacade。二重の公開アルゴリズムにしない。staging全File/Directory fsync→同一FSの`renameat2(RENAME_NOREPLACE)`→親dir fsync→独立Reader readbackまで成功して初めてCOMMITTED。EEXIST時の同request hash再利用は全bytes/Manifest/Privacy検証済みに限る。rename後の失敗は`PUBLICATION_INDETERMINATE`、削除・上書き禁止。


`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。23_42 §2.1のOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。



**G05/P04 OD-02/03採用済みE2E契約（本Package規範）**


## 5. Method-by-Method DGP/Negative/Reference Obligations

このPackageは新Method IDの科学Kernelを追加しない。既存のG01〜G09 Method/ResultとTyped Portを再利用する。

**Scientific boundary:** G04のCATE(x)／DRIV heterogeneous IV coefficientは異なるEstimand。HTE support/uncertainty、Method別oracleと推論の可用性を混同せず、個票Releaseの可否を科学Statusへ偽装しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g05/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. G05 privacy and evidence test contract

- 必須の受入条件は§4の各分岐、§5のScience/Method依存、§6のunit/contract/実filesystem integrationで個別に判定する。
**Independent test:** 両opt-inと片側だけの拒否、wrong UID/ACL/mount/symlink、許可Method RowSchema、Source iteration count、row/byte cap、atomic commit/Readerと旧v2回帰を独立実測。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** 全required Pxx完了後Candidate Assembly。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Explicit unresolved design — freeze barrier

**Document independence:** Class Fields/Constructor/Methodは§3、専用処理は§4、検証/負例は§6で完結。Owner決定が無い要件は仮構実装で埋めない。

**Remaining design gap:** Method別ApprovedRowSchemaの有効列・型・row identity・科学Target・limit値、実Linux ext4/XFS/ACL/mountおよびParquet effective APIと独立Privacy/Science testsは未実証。

