# 30_62_local_execution_publication

---

## 1. `LocalCausalUseCase`

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
| `privacy` | `LocalPrivacyPolicyPort` | composition root | immutable; explicit row release decision |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. UseCaseのper-run状態非共有を不変条件とする。

**Application Context：** `ariadne.capabilities.causal.local_execution.LocalRunContext`は`root:TrustedLocalRoot`、`principal:LocalPrincipal`をimmutableに保持。実行EUIDとprivate root ownerの一致、ext4/XFS local FSの種別と所有UID/owner-only mode/same-FS/dirfdをTrustedRoot Factoryが検証。G05個票はStudyの単一明示opt-inであり署名Policy Anchorは持たない。

**Application Port配置：** `ariadne.capabilities.causal.ports.content_ref.ContentReferencePort`、`ariadne.capabilities.causal.ports.local_io.LocalPublicationPort/LocalManifestReaderPort`、`ariadne.capabilities.causal.ports.local_privacy.LocalPrivacyPolicyPort`。ApplicationはPortのみに依存する。独立署名Policy Verifierは初期G05の責務外。

### 1.3. Constructor / Factory

配置：`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ariadne.causal.design.study.ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs:ContentReferencePort`、`capabilities:MethodCapabilityPort`、`discovery:DiscoveryPort`、`identifier:IdentificationPort`、`estimators:EstimatorPort`、`diagnostics:DiagnosticPort`、`publisher:LocalPublicationPort`、`reader:LocalManifestReaderPort`、`privacy:LocalPrivacyPolicyPort`、`runtime:RuntimeEnvironmentPort`、`clock:ClockPort`。科学BackendはConstructorでimportしない。

- **Constructor signature:** `__init__(self, *, refs: ContentReferencePort, capabilities: MethodCapabilityPort, discovery: DiscoveryPort, identifier: IdentificationPort, estimators: EstimatorPort, diagnostics: DiagnosticPort, publisher: LocalPublicationPort, reader: LocalManifestReaderPort, privacy: LocalPrivacyPolicyPort, runtime: RuntimeEnvironmentPort, clock: ClockPort)`。旧Product v2 APIには変更を加えない。
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
7. 23_42 `2.1のOperation別Artifactとschema_dispatchを検証し、typed Graph/Identification/Effect/Diagnostics、Status/Manifestを生成。G05個票はStudy request、実行UID/private root、Method別OutputShapeを`LocalPrivacyPolicyPort.authorize`でAND評価し、許可後のみG01 staging→Publisher→独立Readerで公開・readbackする。
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

## 2. `MethodCapabilityRegistry`

### 2.1. 識別情報・責務

- **Class:** `ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Product ScientificCoreAdapterとは別契約である。
- **責務:** 41 Method IDごとのOperation/Estimand/Eligibility/Inference/Backend/Profileをstrictに選択し、Version/API capabilityを検証し、Adapter importを遅延させる。外部Libraryの既定推論を黙認しない。
- **責務外:** Estimator計算、Local FS publication、Customer Delivery LegalのPASS。
- **関連契約:** 30_63 Method41 allocation、23_41 §6〜7。

### 2.2. フィールド

配置：`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。Method IDごとにOperation、Estimand Family、Design/Eligibility、Backend ID、推論方式、Profile/Extra、Adapter Factoryを宣言。外部libraryはresolution後にlazy import。Methodが同じでも対象Estimand・inference configが異なれば別個の互換性判断を要する。

| Field | Type | 生成元 | 可変性／制約 |
| --- | --- | --- | --- |
| `descriptors` | `Mapping[str, MethodDescriptor]` | pinned Method41 Registry | Immutable; Method ID unique; target Estimand/Inference explicit |
| `backend_factories` | `Mapping[str, AdapterFactory]` | composition root | Immutable; import lazy; only eligible Method/Profile |
| `effective_env` | `RuntimeEnvironmentPort` | runtime injection | Observed installed version/API; no fake availability |
| `inference_registry` | `InferenceRegistry` | fixed Method-specific policy | Immutable, point-only vs confirmatory separated |

### 2.3. Constructor / Factory

- **Constructor:** `__init__(self, descriptors, backend_factories, effective_env, inference_registry)`. Validate unique IDs, declared Operation/Estimand and versioned descriptor schema; do not import optional modules.
- **Factory** is a collaborator of Registry; 独立実装を置く場合も 独立Factoryを設ける場合も同じMethod×Backend×Inference不変条件に従う。
- **Failure:** Invalid registry/duplicate ID/unsupported policy fails during preflight without selecting unrelated Method or importing missing Backend.

### 2.4. メソッド

~~~python
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime（installed distribution/version/API）を記録する。顧客配布用SBOM/法務承認は内部CLIの必須Artifact/Runtime機能でなく、実配布前に外部で審査。

| Method | Observable contract | Side effects / exceptions |
| --- | --- | --- |
| `describe(method_id)` | pinned descriptor | pure; unknown ID typed rejection |
| `resolve(method_id, backend_id, profile)` | effective Capability Record | inspect distribution/API/version; unavailable reason, never auto fallback |
| `load_adapter(capability)` | scientifically eligible Adapter | only this method may lazy import; import failure localized as capability error |

### 2.5. 処理仕様

1. Resolve declared Method ID and operation/estimand eligibility from frozen descriptor.
2. Check profile/extras and **effective installed distribution+API version**, not just `pyproject.toml` declaration.
3. Check Method-specific inference availability for requested analysis_mode. Backend default is not evidence of valid CI.
4. Return typed supported/unavailable/unsupported with reasons. Only eligible selected capability permits actual lazy import; never fallback to other Method.
5. Export effective config/version/seed/algorithm facts for Manifest, not a pre-run Science PASS.

### 2.6. I/O・連携・失敗処理

- **Input:** MethodRequest, Backend ID/Profile, versioned method descriptors, effective runtime probe.
- **Output:** `MethodDescriptor`, `BackendCapabilityRecord`, `ScientificAdapter` only after eligibility; external estimator objects never enter Domain persistence.
- **No DB/FS mutation** from `describe`/`resolve`; `load_adapter` may import optional modules.
- **Errors:** unknown method, incompatible estimand/inference, missing extra, incompatible API signature, import failure. Each is typed and does not disable core or legacy v2 startup. Combined env/BLAS conflicts are not silently ignored.

### 2.7. 検証

`DD-E11-CAP01`ENV-BASE隔離、`CAP02`単独3Profile、`CAP03`Combined API parity、`CAP04`Versionとunsupported mode、`CAP05`transitive package有無とMethod選択区別、`CAP06`Customer Delivery legal blocked。

**関連ID:** DD-E11-CAP01〜CAP06、FR-185/194/195/196/197/202、NFR-028〜030/032、AR-034/040、BD01-F08/F09/F12。

## 3. `LocalArtifactPublisher`

### 3.1. 識別情報・責務

- **Module / Class:** `ariadne.interfaces.cli.local_causal.publication.LocalArtifactPublisher`
- **責務:** 同一local filesystem上の複数Artifactをrun単位で検証・原子的に公開し、readback成功を確認する。Local File Bundleのpublication authorityでありProductの`ArtifactStorePort`ではない。
- **責務外:** Scientific Estimator、HTTP/DB、顧客配布Legal、外部FSのcross-device atomicity。
- **関連設計:** 23_42 §2/6/7。Product ArtifactStorePortは別のauthorityである。

### 3.2. フィールド

| Field | Type | 生成元 | 可変性・制約 |
| --- | --- | --- | --- |
| `root` | `TrustedLocalRoot` | OS検証済みdirfd Capability | Immutable root handle。所有UID・owner-only mode・local ext4/XFS・同一FSを検証し、commit時もFD/owner/modeを再検証 |
| `run_id` | `str` | 正規化済LocalStudySpec | Immutable。23_42のsafe grammar |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Immutable。小文字SHA256 hex64 |
| `state` | `PublishState` | FactoryでPREPARING | PREPARING→STAGING→VALIDATING→PUBLISHING→COMMITTED/INDETERMINATE、公開前のみABORTED |
| `staging_handle` | `StagingHandle|None` | begin | State依存。Trusted FS descriptorを閉鎖管理 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Commitまで追加、公開後immutable |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Resultのrelease policyと一致を要求 |

### 3.3. Constructor / Factory

- **Constructor:** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。rootはOS EUID/owner/owner-only mode/同一local ext4-XFS/dirfdを検証済みのCapability（任意Pathではない）。random staging tokenは`begin`時に生成する。実装時にRootの変更をcommit境界まで検出する。
- **前提:** `run_id`にseparator/「.」「..」を含まない、request hashはcanonical versionと一致。Trusted Root所有者／同一FS／OS principalの確認に失敗したらstaging生成しない。

### 3.4. メソッド

| Signature | Return | 責務・副作用 | Failure / retry |
| --- | --- | --- | --- |
| `begin(self) -> StagingArtifactSink` | staging sink | 0700 staging dir作成、state遷移 | 重複begin/権限不一致拒否。未公開ならabort可 |
| `stage_bytes(self, key: RelativeArtifactKey, data: bytes, media_type: str, classification: PrivacyClass) -> ArtifactDescriptor` | descriptor | dirfd相当のroot閉じ込めで0600 file作成/追加 | traversal/symlink/サイズ/重複key拒否 |
| `validate(self, manifest: LocalRunManifest) -> ValidatedBundle` | readback済み候補 | 各Artifact→Manifest→markerのhash/Schema/Privacy検証 | missing/hash mismatch/個票漏洩ならfail-closed |
| `commit(self, validated: ValidatedBundle) -> CommittedRunRef` | published run ref | PUBLISHING状態でno-clobber rename、親dir fsync、独立Reader readbackを終えた場合にだけCOMMITTED | rename実施後の失敗・判定不能はINDETERMINATE。既存runは削除・上書きしない |
| `abort(self, reason: str) -> None` | None | 未公開stagingを隔離しHandle解放 | rename後は既公開の可能性があるため破壊的abort禁止 |

### 3.5. 処理仕様（Preconditions／状態／Postconditions）

1. `PREPARING`でroot/safe run ID・output policy・同一FSを検査する。
2. `begin`で`root/.staging/{random-token}`を0700作成。Path文字列チェックだけでなく、全componentをtrusted dirfd下に開くか同等のanti-symlink手法を適用。
3. `STAGING`でArtifactを0600でcreate。全bytesのhash/size/schema/Parquet列/Privacyを検証し、同じkeyの二重書込を拒否。
4. `VALIDATING`でManifestを作り、Artifactリストを走査。Manifest自体のhashを外側の`_COMMITTED.json`へ格納し、Readerと同一アルゴリズムでstagingをreadbackする。File・Directoryをfsync。
5. `commit`は`runs/{run_id}`未存在を**非原子的exists判定に依存せず**保証するLinux `renameat2(RENAME_NOREPLACE)`（同mount/FSの実効対応を確認）を要求。Process lock、排他FS lockのみ、check-then-rename、通常の`Path.rename()`は代替として**禁止**。未対応FSはfail-closed。
6. 同一FSで一括公開後、親directory fsyncと公開版の完全readbackが成功して初めて`COMMITTED`。再試行は既存runのrequest hash一致かつ全readback PASSのときのみ同じrefを返す。
7. Renameの成否が不明、またはRename後のfsync/readbackで異常がある場合は`PublishState=INDETERMINATE`（error `PUBLICATION_INDETERMINATE`）を返し、`COMMITTED`と断定しない。後続の再照合はReaderによる全検査が前提で、既存runを削除・上書きしない。異なるrequest hashは`RUN_ID_CONFLICT`。科学計算のexactly-onceは保証しない。

**Postconditions:** `COMMITTED`ではMarker→Manifest→全Artifactが検証可能、output runはimmutable。失敗時に誤った部分成果物を「成功」へ昇格させない。External store/NFS/cross-deviceは同等のatomicityを自動主張しない。

### 3.6. I/O・連携・失敗処理

- **Caller:** LocalCausalUseCase。`StagingArtifactSink`はScientific Adapterにのみ渡し、final `runs` pathを渡さない。
- **Artifact schema:** 23_42のResult、Graph、Parquet、Manifest、commit marker。それぞれrelative POSIX key＋media_type＋size＋SHA256＋Privacy class。
- **Transaction:** local same-FS staging → validate → no-clobber directory publication → durable parent sync → readback。DB UoWやProduct ArtifactStoreのtransactionとは無関係。
- **Failure classes（意味）:** Invalid path、Permission、HASH_MISMATCH、SCHEMA_INVALID、RUN_ID_CONFLICT、NON_ATOMIC_FILESYSTEM、PUBLICATION_FAILED、READBACK_FAILED。
- **Rollback:** 公開前は未公開stagingを隔離。公開後は既存成果物を勝手に削除しない。Concurrent writers／crashはstagingとrunを混同しない。

### 3.7. 検証

| Test ID | Unit / Contract / Negative | 判定 |
| --- | --- | --- |
| DD-E11-PUB01〜04 | disk full、commit marker前後、rename前後、fsync例外 | Partial bundleをsuccessとしない |
| DD-E11-PUB05 | Concurrent same run_id／異request hash | no-clobber、同hash readback only |
| DD-E11-PUB06 | path traversal、intermediate symlink、TOCTOU | root外read/write拒否 |
| DD-E11-PUB07〜09 | corruption、private 0700/0600、Reader roundtrip | 全bytes/hash/privacy/readback |
| DD-E11-PUB10 | Legacy Product Portと旧v2 CLIの回帰 | E11 publicationをProductの永続authorityへ混入しない |

**関連ID:** FR-185/201/203、NFR-029/031/032/036、BD01-F03/F05/F06/F12、IF IO-E11-01〜09。実FS Fault Injectionと科学的受入は、恒久的な検証義務として別に確認する。

## 4. `LocalRunManifest`

### 4.1. 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.manifest.LocalRunManifest`、immutable typed DTO。
- **責務:** 1 Local runのidentity、lineage、Method/Science/Runtime、artifact inventoryをversioned schemaで保持し、canonical bytesのauthorityを定義する。
- **責務外:** file open、hash verificationのI/O、実効科学計算、Local OS permission enforcement。
- **参照:** IF `23_42` §6、`23_41` §5。Existing Product CliManifestとは別schema。

### 4.2. フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| `manifest_version` | `Literal["e11-local-manifest/1"]` | Schema | mandatory, no v2 fallback |
| `run_id, operation, request_hash` | `str, LocalOperation, str` | validated Study | fixed identity, digest hex64 |
| `lineage` | typed refs + hashes | Question/Design/Graph/Dataset/Identification | graph/estimand/adapter provenance lossless |
| `execution_status` | typed technical + scientific axes | LocalRunOutcome | actual facts, independent science not faked |
| `runtime` | `RuntimeEvidence` | effective probe | Python/backend/lock/seed/fold/BLAS explicit |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | Publisher stage validation | relative keys, size, hash, media, privacy |
| `review` | evidence refs + legal release state | SCI + policy | absent proof remains null / NOT_EVALUATED |

この表は論理的なField groupingであり、wireの厳格なversion/Schema検証は23_42に従う。

### 4.3. Constructor / Factory

- **Factory:** `from_payload(payload: Mapping[str, JsonValue]) -> LocalRunManifest`、`from_run_evidence(evidence: ValidatedRunEvidence) -> LocalRunManifest`。`ValidatedRunEvidence`は同じLocal Manifest境界に属するimmutable内部DTOであり、`study:ValidatedStudy`、ValidatedStudyと完全一致する`study_payload`、`e11-local-status/1`の`status_payload`、実測`RuntimeEvidence`、`stochastic`、P02が実bytesからstageした`tuple[ArtifactDescriptor,...]`、`output_graph_ref:ContentRef|None`、`graph_negative_reason_codes:tuple[str,...]`、`review_science_evidence_ref:ContentRef|None`を必須フィールドとする。各Mappingは深いimmutable snapshotを保持し、可変参照を残さない。`ArtifactDescriptor`の公開フィールドは`key/sha256/size_bytes/media_type/privacy_class/visibility`の6個のみで、upstream_refフィールドは追加しない。
- **Precondition:** strict schema/version + no unknown critical keys; content hash references are normalized; `Manifest` must **not** include its own bytes hash; marker is outside Artifact list. Factories do not read the filesystem.
- **N/A:** runtime backend import is not part of this DTO. Factoryはstrict Schema違反を型付きErrorとして返す。

### 4.4. メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `validate_invariants(self) -> tuple[Reason,...]` | typed reasons | pure; reject broken cross-refs, privacy and science axis inconsistency |
| `to_canonical_bytes(self) -> bytes` | canonical versioned JSON bytes | pure deterministic encoding; reject NaN/Infinity/raw credentials |
| `from_payload(payload) -> LocalRunManifest` | immutable DTO | pure strict decode; unsupported version rejected |

### 4.5. 処理仕様

1. Normalize schema version and all typed scientific statuses without collapsing negative outcomes. `request_hash=SHA256(JCS(typed validated Study wire))`を再計算し、Study/Status/Manifestのrun_id、Operation、Method、Estimand、Privacy、technical/scientific statusを純粋な値として照合する。
2. G01 DISCOVERではManifestの`lineage.question/design/dataset`はStudy入力の各5-field ContentRefと完全一致し、`lineage.identification=null`。**`lineage.graph`は生成Graphの出力ContentRef**（Graph-positiveのみ）であり、G01の`Study.inputs.graph=null`とは区別する。生成Graph参照はTrustedRoot起点で`runs/{run_id}/graph.json`、Inventory Descriptorの`key`はbundle起点で`graph.json`とし、prefixを明示的に写像してSHA/MIMEを照合する。staging中の未来公開パスを直接openせず、P02がstaging実bytesを、公開後Readerが最終Refの実bytesを検証する。Graphの意味/科学的正当性と実bytes hashの証明はP03/P05/P02に委ねる。
3. G01 Graph-positiveは`study.json/status.json/graph.json`、科学的Graph-negativeは`study.json/status.json/diagnostics.json`をInventoryに厳密要求し、Graph-negativeは非空の型付き理由がStatusに存在することを要求する。`schema_dispatch.result=null`、Manifest/Markerの自己Inventory混入禁止、個票禁止。G01のindependent Scienceは`NOT_EVALUATED`でreview ref null。
4. Validate inventory keys unique/safe and exact six-field Descriptor schema; runtime requires actual repo/dirty/Python/platform/uv.lock bytes SHA/distributions/API probes, while pure Manifest validation **must not claim measurement or trusted FD bytes**. Missing facts must not be fabricated. Exact bytes SHA/size, file-to-wire content and atomic publication/readback are P02/P05 responsibilities.
5. Produce canonical bytes deterministically (sorted inventory keys, strict JCS), independent of map insertion order or local time display. A staged `COMPLETED` Status/Manifest is a candidate statement; only P02 independent committed Reader verification permits an externally returned `COMPLETED` outcome. Result identity is a logical run identity, **not** evidence of successful file publication.

### 4.6. I/O・連携・失敗処理

- `LocalArtifactPublisher` creates Manifest bytes; Reader consumes those same canonical bytes. Marker stores SHA256 of Manifest bytes, not a self-reference.
- **I/O:** N/A in DTO; byte serialization is pure. Actual file I/O/permission, partial bundle, crash and retry belong to Publisher/Reader.
- **Failure:** `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `HASH_INVALID`, `PRIVACY_POLICY_CONFLICT`; no automatic v2 upgrade.

### 4.7. 検証

`DD-E11-MAN01` canonical bytes roundtrip; `MAN02` unknown version/unknown critical; `MAN03` marker outside artifact list; `MAN04` science negative vs technical outcome independent; `MAN05` absolute path/raw secret/row data rejection; `MAN06` legacy v2 readback isolation。関連要件：FR-201/202/203、NFR-029/030/032、AR-040、BD01-F06/F07/F12。

## 5. `LocalManifestReader`

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
5. Private Parquetは実行者のsingle Study opt-inとOS principal/private rootの適格性なしにrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

**Readerが検査する交差契約:** `e11-local-manifest/1`の`execution.technical_status`と`e11-local-status/1`の`technical_status`は同一の閉Enumであるだけでなく、同runで値の一致を要求する。読戻し成功の`VerifiedLocalRun`は、Marker/Manifest/Study/Statusのrun ID・request hash・Operation/Method・Schema dispatch・独立Artifact SHA/size・Privacyが一致し、公開状態を`COMPLETED`と証明できた場合に限る。内部科学出力のContentRefも公開ContentRefと同じ`relative_key`構文検査を必須とするが、それを理由にsymlink/../race/root外を直接Path I/Oで扱わない。verified dirfd、componentwise `O_NOFOLLOW`または同等の制約付きopen、Owner/FS/FDのidentityとhash検証を適用する。任意の未知status文字列、値不一致、無断Row出力、重複Key、不正内部ContentRefは検証失敗であり、修復せず`VerifiedLocalRun`を発行しない。

### 5.6. I/O・連携・失敗処理

- **Caller:** Local causal UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

### 5.7. 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。関連要件：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

## 6. `LocalPrivacyPolicy`

### 6.1. 識別情報・責務

- **Class/Module:** `ariadne.interfaces.cli.local_causal.privacy.LocalPrivacyPolicy`。
- **責務:** row-level exportのrelease条件をANDで評価し、aggregated defaultと最小限の出力対象を固定する。Product RBACをLocal OSへ擬似的に持ち込まない。
- **責務外:** 研究対象者の同意獲得、Product ProjectMembership、Backend numerical inference、Customer Legal approval。

### 6.2. フィールド

**Instance Field：なし。** `LocalPrivacyPolicy`は単一の純粋なPolicy Evaluatorであり、runごとの`principal_uid`、`root_owner_uid`、`classification`、`row_export_requested`、`allowed_columns`、`max_rows`、`audit_context`を状態として保持しない。各値は厳格に検証された`study`、`root`、`principal`、`output_shape`からcall単位で得る。これによりApplicationの再利用可能なstateless UseCaseと両立する。

### 6.3. Constructor / Factory

`__init__(self) -> None`。外部I/O、run情報、Backendを保持しない。CLI composition rootからPortとして注入する。Study単独の明示要求だけでは権限が成立せず、実行EUIDが所有するprivate TrustedRoot・Method別出力適格性とAND評価する。

### 6.4. メソッド

| Signature | Result | Side effect / failure |
| --- | --- | --- |
| `authorize(self, *, study: ValidatedStudy, root: TrustedLocalRoot, principal: LocalPrincipal, output_shape: OutputShape) -> PrivacyDecision` | immutable typed allow / reject | 23_41の公開Portと完全同一署名。純粋Policy、File公開副作用なし |
| `filter_export_columns(self, frame_schema: ColumnSchema, *, decision: PrivacyDecision) -> ColumnSelection` | bounded allowlist | 上記Decisionがrow releaseを許すときにのみ使用。未知・禁止列を拒否 |

`filter_export_columns`はRaw DataFrameではなくColumnSchemaと検証済みDecisionから許可列集合を導出する。行数制限はOutput writerとReaderの両方で再検証し、`PrivacyDecision`に上限・許可列・Study/Method/Run identityを結び付ける。

### 6.5. 処理仕様

`authorize`は集計結果に個票を含まないことを確認し、G05個票ではStudy明示request ∧ 実行EUID=root owner ∧ private 0700/0600/local ext4/XFS/owner/dirfd適格 ∧ `RESTRICTED_ROW_LEVEL` ∧ Method別`ApprovedRowSchema`/許可列・row/byte/memory上限をAND評価する。Unknown/unsafeはfail-closedでrow bytesを生成しない。aggregate Result/Manifest/stdout/logにrow valuesを含めない。

### 6.6. I/O・連携・失敗処理

- **Input:** `ValidatedStudy`、runtime EUID、verified private root/owner/mode/local FS、OutputShape、Method別`ApprovedRowSchema`。外部署名Policyなし。
- **Output:** allow/reject（含むReason）と許可されたColumnSelection。Raw rows不要。
- **Side effect:** N/A（純粋Policy）。File create/0600・dir0700とaudit event emissionはPublisher/CLI adapterの責務。
- **Failure:** Study row request false/unspecified、UID mismatch、shared accessible mount、unauthorized column、rows limit、secret/row data leak。No retryで許可状態を推測しない。

### 6.7. 検証

`DD-E11-PRIV01` default no rows、`PRIV02` flag alone deny、`PRIV03` UID mismatch、`PRIV04` 0600/0700、`PRIV05` stdout/log leakage、`PRIV06` shared mount deny、`PRIV07` allowed-columns minimization。関連要件：FR-194/195/203、NFR-031/032、AR-034/035、BD01-F05/F12。

## 7. `BackendCapabilityRecord`


### 7.1. 識別情報・責務

**Class / module:** `ariadne.scientific.capabilities.BackendCapabilityRecord`（Runtime能力値としてScientific層が所有）。実効Backend適格性の証拠を保持し、silent fallbackを禁止する。

### 7.2. フィールド

| Field | 制約 |
|---|---|
| `method_id, backend_id` | 明示指定した組 |
| `distribution_version, adapter_version, api_signature_hash` | 観測された実効版とAPI |
| `extra, profile` | effective environment/profile |
| `available, reason` | boolと欠落時のtyped reason |

### 7.3. Constructor / Factory

Constructorは観測証拠から作成。未実測値を使用可能とするdefault/fallback禁止。

### 7.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `check(self, request: ValidatedCapabilityRequest)` | typed compatibility decision | version/Method/API/Inference照合 | unsupported/unavailable typed reason |

### 7.5. 処理仕様

静的Registryと実効Probeから指定Methodと推論方式の可用性を検証。Probeの取得はConcrete Registry/Runtime Port側で行い、Value自身がoptional Backendをimportしない。`load_adapter`時だけBackend import可能。

### 7.6. I/O・連携・失敗処理

RecordはI/Oなし。Runtime probe、distribution inspection、optional importは30_62のCapability Registryと30_63のAdapter実装の責務。

### 7.7. 検証

`DD-E11-EFF03` version/API mismatch、`DD-E11-CAP01〜06` profile isolation/inference availability、no silent fallback。

**能力の単一Authority：** `ariadne.scientific.capabilities.BackendCapabilityRecord`が実効Distribution/API/probeを表現し、`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`がMethod×Estimand×Inferenceの唯一のRegistryになる。Productの既存`ESTIMATOR_CAPABILITIES`を独立した二重Rules表にしない。

## 8. Class間の契約・既存実装との再利用境界

この節はClass定義の前提として独立したLocal Domainを新設する指示ではなく、既存実装との**共通責務境界**を記述する。CLIの採用は科学的Value・推定器・Product Entityの重複作成の根拠にならない。Productの`causal-analysis-spec/2`、Web API/DB/Worker、`CliManifest(2.0)`の互換性を維持する。

| Class / package | 既存の再利用対象 | 固有の追加責務・非重複境界 |
|---|---|---|
| `LocalCausalUseCase` / `ariadne.capabilities.causal.local_execution` | `product.workflow.GenericExecutor`、StageRunnerと既存Scientific Coreの科学計算 | CLIのrun-scoped preflight→eligibility→scientific execution→publicationを順序付けるApplication orchestrator。Product Execution DB/UoW/Workerを模造しない |
| `MethodCapabilityRegistry` / `ariadne.capabilities.causal.method_registry` | `ScientificValidationService.ESTIMATOR_CAPABILITIES`と`StageRunnerRegistry`の役割を分離 | Method ID×Estimand×Inferenceの単一metadata authority。StageRunnerRegistryはStage registrationのみ |
| `LocalArtifactPublisher` / `ariadne.interfaces.cli.local_causal.publication` | `product.ports.artifact_store.ArtifactStorePort`、`adapters.local_artifact_store.LocalArtifactStore`のhash/path処理 | 複数Artifact・Manifest・Markerをrun単位でimmutable/atomic no-clobber公開。単一Object storeの`store`とは異なる；既存Product Storeを無条件に置換しない |
| `LocalRunManifest` / `ariadne.interfaces.cli.local_causal.manifest` | `interfaces.cli.manifest.CliManifest`（既存v2のReader/Writerは変更しない） | `e11-local-manifest/1` wireは既存のversioned識別子として保持。typed status/lineage/codecを検証し旧v2への暗黙castを禁止 |
| `LocalManifestReader` / `ariadne.interfaces.cli.local_causal.manifest_reader` | Product ArtifactStoreのbyte fetch自体は共通化可能 | Marker→Manifest→Artifact→Privacyのbundle全体を検証する独立Readerで、File存在だけで成功にしない |
| `LocalPrivacyPolicy` / `ariadne.interfaces.cli.local_causal.privacy` | ProductのMembership/RBACはProduct DB資源だけに適用 | 実行者のStudy単独の明示opt-in、OS owner/mode/local FS、Method別列・行・byte上限を評価。署名鍵や第三者承認は不要 |
| `BackendCapabilityRecord` / `ariadne.scientific.capabilities` | 既存Method compatibility checksとscientific runtime probe | 実効distribution/API signatureとMethod supportを証拠化するimmutable value。Backend importやRegistry mutationは持たない |

### 8.1. Port FacadeとMethod Registry

公開`MethodCapabilityPort.resolve(request:ValidatedCapabilityRequest)`はOperation/Estimand/Inference/Designを含む要求を厳格検証し、整合が確認できたMethod/Backend/ProfileだけをConcrete `MethodCapabilityRegistry.resolve(method_id,backend_id,profile)`へ委譲するFacadeである。Method ID/Backend/Profileの3値だけから要求全体の適格性を推測してはならない。`describe`はpure、`resolve`は実効Distribution/APIを検査、`load_adapter`だけがoptional importを行う。互換検証とfallback禁止の規則を2系統に複製しない。

**Adapter dispatch：** `MethodCapabilityPort.resolve`はConcrete `MethodCapabilityRegistry`の単一metadata/Runtime probeを使い、`BackendCapabilityRecord`をValidated Requestに付与する。各Scientific Port Concreteは同じRegistryの`load_adapter(capability)`を利用する。UseCaseが任意のBackend objectを受け取らず、`LocalCausalUseCase.run → MethodCapabilityPort.resolve → DiscoveryPort.discover → FciDiscoveryAdapter.execute`を唯一のG01実行経路にする。

### 8.2. Publisher FacadeとConcrete handle

Applicationの`LocalPublicationPort.begin/seal/publish`はrun-scoped `LocalArtifactPublisher.begin/stage_bytes/validate/commit/abort`を用いるFacade。二重の公開アルゴリズムにしない。staging全File/Directory fsync→同一FSの`renameat2(RENAME_NOREPLACE)`→親dir fsync→独立Reader readbackまで成功して初めてCOMMITTED。EEXIST時の同request hash再利用は全bytes/Manifest/Privacy検証済みに限る。rename後の失敗は`PUBLICATION_INDETERMINATE`、削除・上書き禁止。

**公開Portの正規署名：** `LocalPublicationPort.begin(*,run_id,request_hash,root)->StagingArtifactSink`、`seal(*,sink,manifest,privacy)->ValidatedStagedBundle`、`publish(*,bundle,root)->CommittedLocalRun`。`LocalManifestReaderPort.verify(*,root,run_id)->VerifiedLocalRun`。Publisher Concreteはrun-scopedで、Sinkが同一run handleを保持する。Reader readbackは公開成功の必要条件である。

### 8.3. Canonical Codec・Operation dispatch・Reader

`LocalRunManifest.to_canonical_bytes`は`e11-json-jcs-rfc8785/1`のstrict JCSで符号化しProductの`hash_mapping(default=str)`は用いない。request hashはValidatedStudy意味射影、Graph内部hashは自己fieldを除く意味射影、ContentRefとMarkerが指すManifest hashは保存実bytes。Markerはinventory外に置き、非Effect操作の`schema_dispatch.result=null`を認める。これだけでIDENTIFY/REFUTE/SENSITIVITY/DIAGNOSEの成果物を省略してよいことにはならない。23_42 §2.1のOperation Bundle ValidatorがGraph/Identification/Effect/Diagnosticsの必須性、Status、Method、upstream hashを結合検証する。

Concrete `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は公開`LocalManifestReaderPort.verify(*,root:TrustedLocalRoot,run_id:RunId)`から委譲される。Marker→Manifest→Artifact bytes/type/hash/size→cross-refsとPrivacyを検証する。入力Schema不正はexit2、公開済みbundle readback破損はphase=PUBLICATIONのexit5。修復・自動削除は行わない。

### 8.4. ローカル実行者の個票出力適格性

一般ユーザーのStudyの単一明示opt-in、実行EUID/private TrustedRoot owner一致、local ext4/XFS・0700/0600・owner/mode/dirfd、Method別`ApprovedRowSchema`と出力上限を`LocalPrivacyPolicyPort.authorize`で検証する。署名鍵、第三者Approver、Trust Anchor、失効は要求しない。RowSource反復前・Stage/Seal/Publish前にOS/root/lineageを再検証し、未知状態はFail Closedとする。Aggregate-onlyを不必要に阻害しない。

### 8.5. CLI entrypoint／error envelope

`ariadne.interfaces.cli.local_causal.command.main(argv: list[str]|None) -> int`。IFに従い0=technical complete（負のScience含む）、2=config、3=input/hash/path/**privacy/authorization denial**、4=backend/technical、5=publish。`--check-only`はArtifact無し、Static PreflightでありScience PASSではない。stderrには個票や秘匿入力を含めない。旧`ariadne-estimate`等の既存entrypoint・v2 override挙動は維持する。

Error envelopeはreason `code`と発生`phase`を区別する。入力Schema=exit2、入力path/hash/認可=exit3、Backend/Capability=exit4、出版/readback=exit5。科学的negativeは完全に検証されたBundleのときのみexit0となり得る。

CLIのVersion dispatch・終了codeは[CLI Interface](../23_api_interface_design/23_41_cli_scientific_ports.md)が所有し、数理的なestimand/identificationをCLI固有のDomainに移さない。

## 9. ローカル個票中間成果物と限定Parquet Writer

本節は一般権限Linuxユーザーがext4/XFSのprivate local filesystemへ個票中間成果物を作成する時だけの仕様である。実行者の自発的opt-inは第三者による独立承認ではない。署名鍵/Ed25519/失効と管理者Trust Registryは現在のLocal CLI対象外。G01 Publisher/Reader・全Methodの科学・公開E11 wire Version・旧Product v2は維持する。

### 9.1. Local executor / private root

- 実行主体はLinux非root effective UID。所属部署・外部Reviewer・Product Membershipを確認しない。
- Study.privacy.row_export_requested=true、privacy.classification=RESTRICTED_ROW_LEVEL、実行EUID=TrustedRoot owner、同一local ext4/XFS、private owner-only root/staging0700・row file0600をAND評価する。
- owner/mode/local FS/symlink・path traversal/UID/root identityを実効OSで検証する。共有・不明・異FS・non-owner・容認不能なアクセス権はfail-closed。rootや同じUID processを攻撃者として隔離したという主張はしない。
- `e11-local-study/1`に`privacy.policy_ref`は存在しない。未知Keyはstrictに拒否。旧署名Policy Schemaは歴史的Draftとしてのみ保持。新たな署名Policy Envelopeの生成や鍵配備を要求しない。
- `LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)->PrivacyDecision`。個票失敗はexit3、`read_rows`呼出0・個票bytes0、silent aggregate fallbackなし。Method別`ApprovedRowSchema`・Capsの欠落は個票をdenyし、科学計算結果を偽のFAILに変換しない。

### 9.2. `RowEffectsParquetWriter` / Factory — Owner承認済み署名を維持

- **Module:** `ariadne.interfaces.cli.local_causal.row_effects_parquet`。
- **Constructor:** `__init__(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int)`。
- **Method:** `write(self, *, source: DeferredRowEffectsSource, study: ValidatedStudy, decision: PrivacyDecision, selection: ColumnSelection, sink: StagingArtifactSink) -> ArtifactDescriptor`。
- **Factory:** `create(self, *, serializer: ValidatedParquetSerializer, max_memory_bytes: int) -> RowEffectsParquetWriter`。
- **Protocols:** `DeferredRowEffectsSource.schema()->ColumnSchema`、`read_rows()->Iterable[Mapping[str,JsonValue]]`；`ValidatedParquetSerializer.encode(*,rows:BoundedRowBatch,schema:ApprovedRowSchema)->bytes`。
- **Precondition:** trusted LocalCausalUseCase has validated same-run Study/Method/Data/OutputShape, effective UID/root, explicit single Study opt-in and a Method-approved ordered ColumnSelection. The typed `PrivacyDecision` cannot be accepted as an unverified user-originated object or used to escape the UseCase/Sink boundary.
- **Algorithm:** schema-only inspection→approved ordered allowlist/row ID/dtype/units→after eligibility, lazily read a maximum of max_rows+1 rows→reject duplicate IDs, nonfinite values, unknown columns, wrong types, row/byte/memory limit→encode bounded Parquet→recheck root/UID/FS/owner/mode/source identity→stage `row_effects.parquet` / `application/vnd.apache.parquet` / `RESTRICTED_ROW_LEVEL` to existing G01 Sink only.
- **Publication:** G01 Publisher alone validates/schema/hash/Manifest/Marker and performs same-FS atomic no-clobber rename and independent Reader readback. Row Writer never writes to final runs/, produces a new Manifest or signs an export.
- **Failure:** initially unapproved ⇒ row iterator zero and row bytes zero. Post-stage FS problem ⇒ no success/marker, private staging quarantined; do not claim old staging bytes vanished. JSON/Manifest/CLI/log contains no row values or secrets.

### 9.3. Independent verification / remaining blockers

G05/P02: Study-only explicit request true/false and root/Method eligibility, actual nonroot UID/private ext4/XFS/root/owner-mode/symlink/dirfd/same-FS tests; G05/P03: Method `ApprovedRowSchema`, ordered columns, row/byte/memory caps, real Parquet API and readback; G05/P04/07: row source pre-auth calls zero, stage/commit races, G01 marker/hash/fault/no-clobber, no row leak, legacy Product v2 regression. Key/signature/revocation tests are excluded. ApprovedRowSchema/Parquet effective ABI/Linux filesystem tests still missing. No G05 Freeze, Coding Authorization or Gate999 pass.

### 9.4. SIM-01 current local-FS proof boundary（Owner 2026-11-21）

初期G05のローカルFS保護は非root EUIDの所有・root/staging 0700・row file 0600・real ext4/XFS・same filesystem・dirfd/O_NOFOLLOW・Symlink/Path拒否で成立する。旧PREP02のACL xattr digest、statx mount-ID追跡、mount namespace可視性の独立証明、CI/container環境検知は必須でない。同じUIDおよびroot管理者からの隔離を保証しない。実行時のOwner/ModeとFS identity・Pathを適切な公開境界で再確認する。NFR-030/031とG01原子的Publisher・独立Readerは継続。内部CLIのSBOM/顧客配布License stateは要求しない。元のFreeze履歴はcombined_review/131により限定的にsupersedeされ、実Linux/FSテストはNOT_RUN。

## Local execution, privacy and publication invariants

`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を正規契約とする。Studyの明示`row_export_requested`はrequest identityに含め、private Root/同一UID/Method別allowlistとbounded outputを実行ごとに検証する。許可されるまで個票Sourceを反復せず、拒否はaggregateへのsilent fallbackとしない。Reader検証前にCOMMITTEDと報告せず、rename後の判定不能を`PUBLICATION_INDETERMINATE`とする。共通WriterはIV構造係数と非IV CATEの列意味を混同せずMethod固有制約を検証する。
