# 30_62_e11_local_execution_publication — E11 Local Use Case / Publication物理詳細設計

## 1. Scopeと既存コードの境界

現行 `interfaces/cli/scientific_stage.py` は `ScientificCoreAdapter` 実行後にManifestを `Path.write_text` する。現行 `interfaces/cli/estimation.py` は旧Product互換の `REQUIRES_REVIEW` を許す場合がある。現行 `product/ports/artifact_store.py` の `store/retrieve/exists/delete` は複数fileの一括公開を保証しない。

E11では新しいversioned Local laneへ分ける。既存の `causal-analysis-spec/2`／Product Web API/DB/Workerを遡及変更しない。本書は新Class候補の実装契約であり、コード／独立Science証拠ではない。

## 2. `E11LocalCausalUseCase`（PROPOSED：Owner 7区分）

### 2.1. 識別情報・責務

- **Class:** `causal.local_application.use_case.E11LocalCausalUseCase`。Implementation Status **PROPOSED / SOURCE_NOT_PRESENT**。既存`interfaces.cli.scientific_stage.run_stage`は別の旧Product CLI実装であり、このClassのSourceではない。
- **責務:** versioned Local Studyのpreflight→identification→method eligibility→adapter execution→staging→publish→readbackを順序付け、科学的Negativeとtechnical failureを混同しない。
- **責務外:** Scientific Estimatorの数学本体、Product DB/UoW/Worker/Web API、実行済み独立Science PASSの宣言。
- **Design Authority:** 23_41 §3〜5、23_42 §2/6/7、30_61 §1/5〜8、DEC09 ARC09-01〜07。具体ADRとSchemaはFreeze pending。

### 2.2. フィールド

**Constructor-injected Port fields（現行設計候補）:**

| Field | Type | Value origin | Mutable / constraint |
| --- | --- | --- | --- |
| `decoder` | `LocalConfigDecoder` | composition root | immutable; strict E11 version dispatch |
| `refs` | `ContentReferencePort` | composition root | immutable; trusted-root hash-bound read |
| `capabilities` | `MethodCapabilityPort` | composition root | immutable; effective profile and no silent fallback |
| `identifier` | `IdentificationPort` | composition root | immutable; Domain proof/negative outcome |
| `estimators` | `EstimatorPort` | composition root | immutable; typed scientific result to staging |
| `diagnostics` | `DiagnosticPort` | composition root | immutable; method-specific typed diagnostics |
| `publisher` | `LocalPublicationPort` | composition root | immutable; all writes staged |
| `runtime` | `RuntimeEnvironmentPort` | composition root | immutable; effective provenance not fabricated |
| `clock` | `ClockPort` | composition root | immutable; injected timestamp authority |

No shared mutable per-run state is retained in the use-case object; per-run staged artifacts/status are returned via typed RunOutcome or scoped Context. This last concurrency invariant is **PROPOSED**, not source-verified.

### 2.3. Constructor / Factory

候補：`causal.local_application.use_case.E11LocalCausalUseCase`。
注入Port：`decoder: LocalConfigDecoder`、`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Proposed signature:** `__init__(self, *, decoder, refs, capabilities, identifier, estimators, diagnostics, publisher, runtime, clock)` with typed Ports above.
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. Any actual exception class/type is Freeze pending.
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

### 2.4. メソッド

~~~python
def preflight(self, spec: LocalStudySpec) -> PreflightReport: ...
def run(self, spec: LocalStudySpec) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: LocalStudySpec) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: LocalStudySpec) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

### 2.5. 処理仕様

1. `schema_version`を明示dispatchし、strict YAML/JSON parse。旧v2と無版はE11解釈禁止。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. Identificationを実行又は上流proofを検証。未確定Graphやunsupported strategyを成功へ変更しない。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. typed ResultとGraph/diagnostics/Manifestを生成。Privacyとartifact hashesを検証し一括publish後readback。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

**Precondition:** Input Spec passed strict schema/version check and trusted content refs. **Postcondition:** either immutable fully validated bundle with commit marker, or typed non-success/negative without false completed marker. Method/estimand/Graph conditional result is never guessed from a Backend label.

### 2.6. I/O・連携・失敗処理

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

- **I/O:** reads via ContentReferencePort, writes only via StagingArtifactSink/LocalPublicationPort. Each run has pinned request/content hash and effective API/seed evidence.
- **Transactions:** This is a Local FS unit, not a Product UoW. Publication atomicity and crash recovery specified in §4 and IF 23_42.
- **Errors:** invalid config/schema, missing/mismatched refs, unsupported capability, scientific negative, runtime failure and publication failure remain separately typed. **Retry/rollback:** idempotent same-hash readback allowed; another request hash with same run ID rejected; uncommitted staging never advertised as success.

### 2.7. 検証

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

| Acceptance | Required |
| --- | --- |
| Unit/Contract | Preflight performs zero Backend scientific calls; run calls Estimator only for proven eligible request; payload/status axes preserved |
| Negative | wrong version, hash mismatch, Graph uncertainty, unsupported CI, unavailable extra, no row export flag, publication failure |
| Regression | old v2 identify/estimate/refute/sensitivity and existing Product Stage runner unchanged |

**Trace:** DD-E11-RUN01〜RUN07、FR-185/187/201/202/203、NFR-029/032/036、AR-029/034/040、BD01-F04/F06/F07/F12。Test execution NOT_RUN.

## 3. `MethodCapabilityRegistry`（PROPOSED：Owner 7区分）

### 3.1. 識別情報・責務

- **Class:** `causal.local_application.capability_registry.MethodCapabilityRegistry`、**PROPOSED / SOURCE_NOT_PRESENT**。Existing `ScientificCoreAdapter`はこのRegistryの実装証拠ではない。
- **責務:** 41 Method IDごとのOperation/Estimand/Eligibility/Inference/Backend/Profileをstrictに選択し、Version/API capabilityを検証し、Adapter importを遅延させる。外部Libraryの既定推論を黙認しない。
- **責務外:** Estimator計算、Local FS publication、Customer Delivery LegalのPASS。
- **References:** DEC08、30_63 Method41 allocation、23_41 §6〜7、BD01-F08/F09、各Method SCI evidence。

### 3.2. フィールド

候補：`causal.local_application.capability_registry.MethodCapabilityRegistry`。Method IDごとにOperation、Estimand Family、Design/Eligibility、Backend ID、推論方式、Profile/Extra、Adapter Factoryを宣言。外部libraryはresolution後にlazy import。Methodが同じでも対象Estimand・inference configが異なれば別個の互換性判断を要する。

| Field（Proposed） | Type | 生成元 | 可変性／制約 |
| --- | --- | --- | --- |
| `descriptors` | `Mapping[str, MethodDescriptor]` | pinned Method41 Registry | Immutable; Method ID unique; target Estimand/Inference explicit |
| `backend_factories` | `Mapping[str, AdapterFactory]` | composition root | Immutable; import lazy; only eligible Method/Profile |
| `effective_env` | `RuntimeEnvironmentPort` | runtime injection | Observed installed version/API; no fake availability |
| `inference_registry` | `InferenceRegistry` | fixed Method-specific policy | Immutable, point-only vs confirmatory separated |

These fields are candidate architecture bindings; actual class signatures/extra names require freeze.

### 3.3. Constructor / Factory

- **Proposed** `__init__(self, descriptors, backend_factories, effective_env, inference_registry)`. Validate unique IDs, declared Operation/Estimand and versioned descriptor schema; do not import optional modules.
- **Factory** is a collaborator of Registry, **not an additional implemented Class** by implication. If a separately implemented Adapter Factory is adopted, it requires its own Owner 7-section physical specification.
- **Failure:** Invalid registry/duplicate ID/unsupported policy fails during preflight without selecting unrelated Method or importing missing Backend.

### 3.4. メソッド

~~~python
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime・SBOM・Legalは別軸で記録。

| Method | Observable contract | Side effects / exceptions |
| --- | --- | --- |
| `describe(method_id)` | pinned descriptor | pure; unknown ID typed rejection |
| `resolve(method_id, backend_id, profile)` | effective Capability Record | inspect distribution/API/version; unavailable reason, never auto fallback |
| `load_adapter(capability)` | scientifically eligible Adapter | only this method may lazy import; import failure localized as capability error |

### 3.5. 処理仕様

1. Resolve declared Method ID and operation/estimand eligibility from frozen descriptor.
2. Check profile/extras and **effective installed distribution+API version**, not just `pyproject.toml` declaration.
3. Check Method-specific inference availability for requested analysis_mode. Backend default is not evidence of valid CI.
4. Return typed supported/unavailable/unsupported with reasons. Only eligible selected capability permits actual lazy import; never fallback to other Method.
5. Export effective config/version/seed/algorithm facts for Manifest, not a pre-run Science PASS.

### 3.6. I/O・連携・失敗処理

- **Input:** MethodRequest, Backend ID/Profile, versioned method descriptors, effective runtime probe.
- **Output:** `MethodDescriptor`, `BackendCapabilityRecord`, `ScientificAdapter` only after eligibility; external estimator objects never enter Domain persistence.
- **No DB/FS mutation** from `describe`/`resolve`; `load_adapter` may import optional modules.
- **Errors:** unknown method, incompatible estimand/inference, missing extra, incompatible API signature, import failure. Each is typed and does not disable core or legacy v2 startup. Combined env/BLAS conflicts are not silently ignored.

### 3.7. 検証

`DD-E11-CAP01`ENV-BASE隔離、`CAP02`単独3Profile、`CAP03`Combined API parity、`CAP04`Versionとunsupported mode、`CAP05`transitive package有無とMethod選択区別、`CAP06`Customer Delivery legal blocked。

**Trace:** DD-E11-CAP01〜CAP06、FR-185/194/195/196/197/202、NFR-028〜030/032、AR-034/040、BD01-F08/F09/F12。ENV smoke/Science benchmarks are NOT_RUN.

## 4. `LocalArtifactPublisher`（PROPOSED：Owner 7区分）

### 4.1. 識別情報・責務

- **Module / Class:** `interfaces.cli.e11.publication.LocalArtifactPublisher`（提案。現行Sourceには未実装）
- **責務:** 同一local filesystem上の複数Artifactをrun単位で検証・原子的に公開し、readback成功を確認する。新E11のLocal authorityでありProductの`ArtifactStorePort`ではない。
- **責務外:** Scientific Estimator、HTTP/DB、顧客配布Legal、外部FSのcross-device atomicity。
- **設計参照:** 23_42 §2/6/7、BD01-F03/F05/F06/F12。Current Product Port blob `e5bb990f9b69ef68df46a1559560ffb67b64caaf`。新Port/Schemaの最終freezeは未実施。

### 4.2. フィールド

| Field | Type（Proposed） | 生成元 | 可変性・制約 |
| --- | --- | --- | --- |
| `root` | `Path` | 呼出し元からTrusted Root注入 | Immutable root reference。実FSの所有者・権限／同一devをpreflight |
| `run_id` | `str` | 正規化済LocalStudySpec | Immutable。23_42のsafe grammar |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Immutable。小文字SHA256 hex64 |
| `state` | `PublishState` | FactoryでPREPARING | PREPARING→STAGING→VALIDATING→COMMITTED/ABORTED |
| `staging_handle` | `StagingHandle|None` | begin | State依存。Trusted FS descriptorを閉鎖管理 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Commitまで追加、公開後immutable |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Resultのrelease policyと一致を要求 |

### 4.3. Constructor / Factory

- **Proposed** `__init__(self, root: Path, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。注入されたrootは存在するTrusted directoryのみ、random staging tokenは`begin`時に生成する。
- **前提:** `run_id`にseparator/「.」「..」を含まない、request hashはcanonical versionと一致。Trusted Root所有者／同一FS／OS principalの確認に失敗したらstaging生成しない。
- **Failure:** `CONFIG_INVALID`/ `INPUT_PATH_INVALID`/ `PERMISSION_DENIED`などのtyped error。実際のException class名・Constructor実装はADR/06 Freeze時に確定。

### 4.4. メソッド

| Signature（Proposed） | Return | 責務・副作用 | Failure / retry |
| --- | --- | --- | --- |
| `begin(self) -> StagingArtifactSink` | staging sink | 0700 staging dir作成、state遷移 | 重複begin/権限不一致拒否。未公開ならabort可 |
| `stage_bytes(self, key: RelativeArtifactKey, data: bytes, media_type: str, classification: PrivacyClass) -> ArtifactDescriptor` | descriptor | dirfd相当のroot閉じ込めで0600 file作成/追加 | traversal/symlink/サイズ/重複key拒否 |
| `validate(self, manifest: LocalRunManifest) -> ValidatedBundle` | readback済み候補 | 各Artifact→Manifest→markerのhash/Schema/Privacy検証 | missing/hash mismatch/個票漏洩ならfail-closed |
| `commit(self, validated: ValidatedBundle) -> CommittedRunRef` | published run ref | no-clobber rename、親dir fsync、公開後readback | 競合／FS障害時に既存run上書き不可。出所不明runは消去しない |
| `abort(self, reason: str) -> None` | None | 未公開stagingを隔離しHandle解放 | rename後は既公開の可能性があるため破壊的abort禁止 |

### 4.5. 処理仕様（Preconditions／状態／Postconditions）

1. `PREPARING`でroot/safe run ID・output policy・同一FSを検査する。
2. `begin`で`root/.staging/{random-token}`を0700作成。Path文字列チェックだけでなく、全componentをtrusted dirfd下に開くか同等のanti-symlink手法を適用。
3. `STAGING`でArtifactを0600でcreate。全bytesのhash/size/schema/Parquet列/Privacyを検証し、同じkeyの二重書込を拒否。
4. `VALIDATING`でManifestを作り、Artifactリストを走査。Manifest自体のhashを外側の`_COMMITTED.json`へ格納し、Readerと同一アルゴリズムでstagingをreadbackする。File・Directoryをfsync。
5. `commit`は`runs/{run_id}`未存在を**非原子的exists判定に依存せず**保証するno-replace primitiveまたは実証済みのprocess-wide/exclusive FS lockを要求。単純`Path.rename()`をno-clobber保証としない。
6. 同一FSで一括公開後、親directory fsyncと公開版の完全readbackが成功して初めて`COMMITTED`。再試行は既存runのrequest hash一致かつ全readback PASSのときのみ同じrefを返す。
7. Rename後の異常は`COMMITTED`と断定せず、Readerの現在値とRecovery規則で解決。異なるrequest hashは`RUN_ID_CONFLICT`。科学計算のexactly-onceは保証しない。

**Postconditions:** `COMMITTED`ではMarker→Manifest→全Artifactが検証可能、output runはimmutable。失敗時に誤った部分成果物を「成功」へ昇格させない。External store/NFS/cross-deviceは同等のatomicityを自動主張しない。

### 4.6. I/O・連携・失敗処理

- **Caller:** E11LocalCausalUseCase。`StagingArtifactSink`はScientific Adapterにのみ渡し、final `runs` pathを渡さない。
- **Artifact schema:** 23_42のResult、Graph、Parquet、Manifest、commit marker。それぞれrelative POSIX key＋media_type＋size＋SHA256＋Privacy class。
- **Transaction:** local same-FS staging → validate → no-clobber directory publication → durable parent sync → readback。DB UoWやProduct ArtifactStoreのtransactionとは無関係。
- **Failure classes（意味）:** Invalid path、Permission、HASH_MISMATCH、SCHEMA_INVALID、RUN_ID_CONFLICT、NON_ATOMIC_FILESYSTEM、PUBLICATION_FAILED、READBACK_FAILED。実Python Exceptionの命名は未Freeze。
- **Rollback:** 公開前は未公開stagingを隔離。公開後は既存成果物を勝手に削除しない。Concurrent writers／crashはstagingとrunを混同しない。

### 4.7. 検証

| Test ID | Unit / Contract / Negative | 判定 |
| --- | --- | --- |
| DD-E11-PUB01〜04 | disk full、commit marker前後、rename前後、fsync例外 | Partial bundleをsuccessとしない |
| DD-E11-PUB05 | Concurrent same run_id／異request hash | no-clobber、同hash readback only |
| DD-E11-PUB06 | path traversal、intermediate symlink、TOCTOU | root外read/write拒否 |
| DD-E11-PUB07〜09 | corruption、private 0700/0600、Reader roundtrip | 全bytes/hash/privacy/readback |
| DD-E11-PUB10 | Legacy Product Portと旧v2 CLIの回帰 | E11 publicationをProductの永続authorityへ混入しない |

**Trace:** FR-185/201/203、NFR-029/031/032/036、BD01-F03/F05/F06/F12、IF IO-E11-01〜09。実FS fault injectionと独立ReviewはNOT_RUN。

## 5. E11 Local Manifest／Reader（別々のProposed Class）

以下は一つの「Class」ではない。**`LocalRunManifest`（Data/Value）と`LocalManifestReader`（I/O Adapter）を独立に7区分化する**。両者はSource未実装であり、確定JSON Schema／Exception型とsecurity implementationはFreeze待ち。

### 5.1. `LocalRunManifest`（PROPOSED）

#### 5.1.1. 識別情報・責務

- **Class/Module（候補）:** `interfaces.cli.e11.manifest.LocalRunManifest`、immutable typed DTO。**PROPOSED / SOURCE_NOT_PRESENT**。
- **責務:** 1 Local runのidentity、lineage、Method/Science/Runtime、artifact inventoryをversioned schemaで保持し、canonical bytesのauthorityを定義する。
- **責務外:** file open、hash verificationのI/O、実効科学計算、Local OS permission enforcement。
- **Authority:** IF `23_42` §6、`23_41` §5。Existing `interfaces.cli.manifest.CliManifest`（blob `97216eca9d777e97f7a5ebd4e248afd31c6b4de0`）とは別schema。

#### 5.1.2. フィールド

| Field | Proposed type | Origin | Constraint |
| --- | --- | --- | --- |
| `manifest_version` | `Literal["e11-local-manifest/1"]` | Schema | mandatory, no v2 fallback |
| `run_id, operation, request_hash` | `str, LocalOperation, str` | validated Study | fixed identity, digest hex64 |
| `lineage` | typed refs + hashes | Question/Design/Graph/Dataset/Identification | graph/estimand/adapter provenance lossless |
| `execution_status` | typed technical + scientific axes | LocalRunOutcome | actual facts, independent science not faked |
| `runtime` | `RuntimeEvidence` | effective probe | Python/backend/lock/seed/fold/BLAS explicit |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | Publisher stage validation | relative keys, size, hash, media, privacy |
| `review` | evidence refs + legal release state | SCI + policy | absent proof remains null / NOT_EVALUATED |

This table is a logical field grouping; exact nested JSON Schema property names, optionality and enum must be frozen before Coding.

#### 5.1.3. Constructor / Factory

- **Proposed:** `from_payload(payload: Mapping[str, JsonValue]) -> LocalRunManifest`、`from_run_evidence(evidence: ValidatedRunEvidence) -> LocalRunManifest`。
- **Precondition:** strict schema/version + no unknown critical keys; content hash references are normalized; `Manifest` must **not** include its own bytes hash; marker is outside Artifact list. Factories do not read the filesystem.
- **N/A:** runtime backend import is not part of this DTO. Factory naming and exact exception classes remain ADR/Schema Freeze pending.

#### 5.1.4. メソッド

| Signature（Proposed） | Result | Side effect / failure |
| --- | --- | --- |
| `validate_invariants(self) -> tuple[Reason,...]` | typed reasons | pure; reject broken cross-refs, privacy and science axis inconsistency |
| `to_canonical_bytes(self) -> bytes` | canonical versioned JSON bytes | pure deterministic encoding; reject NaN/Infinity/raw credentials |
| `from_payload(payload) -> LocalRunManifest` | immutable DTO | pure strict decode; unsupported version rejected |

#### 5.1.5. 処理仕様

1. Normalize schema version and all typed scientific statuses without collapsing negative outcomes.
2. Validate artifact keys unique and safe relative; no absolute input path/secret/row data in Manifest.
3. Validate lineage digest/target and effective runtime evidence with missing values distinguished from fabricated defaults.
4. Produce canonical bytes deterministically, independent of map insertion order or local time display. Result identity is a logical run identity, **not** evidence of successful file publication.

#### 5.1.6. I/O・連携・失敗処理

- `LocalArtifactPublisher` creates Manifest bytes; Reader consumes those same canonical bytes. Marker stores SHA256 of Manifest bytes, not a self-reference.
- **I/O:** N/A in DTO; byte serialization is pure. Actual file I/O/permission, partial bundle, crash and retry belong to Publisher/Reader.
- **Failure:** `SCHEMA_INVALID`, `VERSION_UNSUPPORTED`, `HASH_INVALID`, `PRIVACY_POLICY_CONFLICT`; no automatic v2 upgrade.

#### 5.1.7. 検証

`DD-E11-MAN01` canonical bytes roundtrip; `MAN02` unknown version/unknown critical; `MAN03` marker outside artifact list; `MAN04` science negative vs technical outcome independent; `MAN05` absolute path/raw secret/row data rejection; `MAN06` legacy v2 readback isolation。**NOT_RUN**。Trace：FR-201/202/203、NFR-029/030/032、AR-040、BD01-F06/F07/F12。

### 5.2. `LocalManifestReader`（PROPOSED）

#### 5.2.1. 識別情報・責務

- **Class/Module（候補）:** `interfaces.cli.e11.manifest_reader.LocalManifestReader`。**PROPOSED / SOURCE_NOT_PRESENT**。
- **責務:** already-published runをMarker→Manifest→Artifactの順に検証し、`VerifiedLocalRun`を返す。存在だけでCOMMITTEDと判断しない。
- **責務外:** publish、legacy v2の無断E11解釈、科学的Oracle計算、実Artifactの編集。
- **Authority:** IF `23_42` §6〜8、BD01-F03/F05/F06/F12。

#### 5.2.2. フィールド

| Field | Type | Origin | Constraint |
| --- | --- | --- | --- |
| Instance fields | N/A（stateless Reader候補） | N/A | trusted root/run IDはper-call引数。Cacheを設ける場合は別ADR |

#### 5.2.3. Constructor / Factory

- `__init__()`は特別な依存なし（**Proposed、N/A理由：read_runがrootを明示注入するstateless API**）。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

#### 5.2.4. メソッド

| Signature（Proposed） | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: Path, run_id: str) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

#### 5.2.5. 処理仕様

1. Trusted root・run_idとlocal execution principalを検証し、run directoryにsecure open。
2. `_COMMITTED.json`存在/strict schema/version/request hashを確認。
3. `manifest.json`を同一安全dirfd scopeでopen、markerに保存されたManifest SHA256と照合し、`LocalRunManifest`をstrict decode。
4. Artifactの相対key重複、SHA256/size/MediaType、privacy class、必要なLineage Refの一致を検査。
5. Private Parquetには出力Policy/OS principalの許可なしでrow-level bytesを返さない。
6. 未検証・partial・legacy・corruptのいずれでも`VerifiedLocalRun`を返さない。

#### 5.2.6. I/O・連携・失敗処理

- **Caller:** E11 Local UseCaseのReadback／CLI status command、publisherのpublication verification。
- **I/O:** Trusted Rootからread-only。symlink/TOCTOUとstale marker防止のためopenされた同一File Descriptorに対しhashを確認。
- **Errors:** `NOT_COMMITTED`, `MANIFEST_HASH_MISMATCH`, `ARTIFACT_HASH_MISMATCH`, `VERSION_UNSUPPORTED`, `PRIVATE_ARTIFACT_DENIED`等を区分（Exception class名は未Freeze）。
- **Retry:** 不完全runを勝手に修復／削除しない。既存同hash runの再利用は完全Readback PASSに限定。

#### 5.2.7. 検証

`DD-E11-READ01` valid; `READ02` marker missing; `READ03` corrupted bytes/size; `READ04` wrong version; `READ05` individual export suppression; `READ06` old v2 not E11; `READ07` symlink/path race。**NOT_RUN**。Trace：IF IO-E11-01〜09、FR-201〜203、NFR-031/032、BD01-F03/F05/F06/F12。

## 6. `LocalPrivacyPolicy`（PROPOSED：Owner 7区分）

### 6.1. 識別情報・責務

- **Class/Module候補:** `interfaces.cli.e11.privacy.LocalPrivacyPolicy`、**PROPOSED / SOURCE_NOT_PRESENT**。
- **責務:** row-level exportのrelease条件をANDで評価し、aggregated defaultと最小限の出力対象を固定する。Product RBACをLocal OSへ擬似的に持ち込まない。
- **責務外:** 研究対象者の同意獲得、Product ProjectMembership、Backend numerical inference、Customer Legal approval。

### 6.2. フィールド

| Field | Type（Proposed） | 生成元 | 制約 |
| --- | --- | --- | --- |
| `principal_uid, root_owner_uid` | `int` | OS effective actor + trusted root | mismatch reject unless explicit delegated policy |
| `classification` | `PrivacyClass` | Study Spec | default non-row / explicit restricted |
| `row_export_requested` | `bool` | Study spec | flagだけで認可しない |
| `row_export_authorized` | `bool` | scope-specific policy | separate positive authorization |
| `allowed_columns` | `tuple[str,...]` | policy | whitelisted minimal fields |
| `max_rows` | `int` | policy | bounded; enforce before output |
| `audit_context` | `Mapping[str,JsonValue]` | local provenance | secrets/raw rows forbidden |

### 6.3. Constructor / Factory

- **Proposed:** `__init__(self, *, principal_uid, root_owner_uid, classification, row_export_requested, row_export_authorized, allowed_columns, max_rows, audit_context)`。
- **Preconditions:** OS effective identity＋permission sourceはruntime evidenceから採取。HeaderやCLI flagを信頼済principalの証拠に昇格しない。
- **Postconditions:** policy object immutable。構築時に実outputを生成しない。Delegated/CI/container UID規則はADR＋negative testで最終確定。

### 6.4. メソッド

| Signature（Proposed） | Result | Side effect / failure |
| --- | --- | --- |
| `assert_export_allowed(self, spec: LocalStudySpec, cli_flag: bool, runtime_principal: LocalPrincipal) -> None` | allow / typed reject | pure authorization check; no implicit file write |
| `filter_export_columns(self, frame_schema: ColumnSchema) -> ColumnSelection` | bounded allowlist | pure; unknown or prohibited columns rejected |

`filter_export_columns`は**設計上の候補**であり、採用する場合はDataFrame raw dataをこのPolicyに渡さず、Schemaのみを渡す。実装署名は未Freeze。

### 6.5. 処理仕様

`assert_export_allowed`は Spec policy許可 ∧ CLI flag ∧ OS Principal/owner/delegation適格 ∧ root permissions ∧ classification/column/minimum-row policy の全条件をrequire。Fail-closedで個票Parquetを生成しない。通常のResult/Manifest/stdout/logにrow valuesを含めない。Shared mount、root container、CI volumeにおける可視性はOS File Modeだけで推測しない。

### 6.6. I/O・連携・失敗処理

- **Input:** `LocalStudySpec`, CLI intent, principal/effective UID, trusted root permission evidence, column Schema。
- **Output:** allow/reject（含むReason）と許可されたColumnSelection。Raw rows不要。
- **Side effect:** N/A（純粋Policy）。File create/0600・dir0700とaudit event emissionはPublisher/CLI adapterの責務。
- **Failure:** missing flag、UID mismatch、shared accessible mount、unauthorized column、rows limit、secret/row data leak。No retryで許可状態を推測しない。

### 6.7. 検証

`DD-E11-PRIV01` default no rows、`PRIV02` flag alone deny、`PRIV03` UID mismatch、`PRIV04` 0600/0700、`PRIV05` stdout/log leakage、`PRIV06` shared mount deny、`PRIV07` allowed-columns minimization。**NOT_RUN**。Trace：FR-194/195/203、NFR-031/032、AR-034/035、BD01-F05/F12。

## 7. CLI entrypoint / Error bridge

候補`interfaces.cli.e11.command.main(argv: list[str]|None) -> int`。IFに従い0=technical complete（負のScience含む）、2=config、3=input/hash/path、4=backend/technical、5=publish。`--check-only`はArtifact無し、Static PreflightでありScience PASSではない。stderrには個票や秘匿入力を含めない。旧`ariadne-estimate`等の既存entrypoint・v2 override挙動は維持する。

## 8. Traceと受入

| 暫定Plan Workstream | Physical obligation | 各正式Gateの06 Coding Contractへ渡す実装要件 |
|---|---|---|
| G01/G02 | local Graph/Question/Design、Identification gate | Graph/Proof/negative roundtrip |
| G03/G04/G05 | Method Registry/CATE、Privacy | Method compatibility/CI/permission |
| G06 | Temporal endpoint/lag | actual API／lossless encoding |
| G07/G08/G09 | Quasi/IV/AR/SCM Adapter | typed Result、Reference planning |
| G10 | Publish/Lock/Manifest/legacy | fault injection、Profile isolation、v2 regression |

Scientific bias/coverage/FWER/MCS/resource・Licenseは該当Gateの07独立科学検証と別個の顧客配布Legal審査で判断する。DD設計だけをScience/Legal PASS扱いしない。

参照：[E11 Domain/Port](30_61_e11_local_domain_ports.md)、[IF CLI](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、[IF Manifest](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)、[旧Manifest](30_60_cli_adapters.md)。

## 9. DEC-PREP02 approved physical-design guardrails (2026-11-17)

[Owner record](../combined_review/decisions/94_20261117_dec_prep02_owner_architecture_choices.md) adopts **A/A/A**, with no implementation claims. `LocalPrivacyPolicy`: reject UID-root-owner mismatch, delegated/shared/CI/container-root-accessible paths and unverifiable ACL/mount exposure; require Study policy AND CLI flag AND private OS root for row output; default aggregate-only. `LocalArtifactPublisher`: enforce effective atomic **no-clobber** Linux same-FS directory publication; no `exists()+rename` fallback; fail closed on unsupported filesystem; staged full-bundle verification, readback and fsync boundaries remain required. `LocalRunManifest` and `LocalManifestReader`: strict explicit version discriminators for study/graph/effect-result/manifest/status `e11-local-*/1`, legacy Product v2 isolated. Require negative tests: concurrent run_id, unsupported FS, crash at each write/publish/fsync boundary, shared mount, UID mismatch, unknown version, legacy v2. Exact syscall ABI/DTO signatures/JSON Schema and independent Architecture review remain **not frozen/not run**.
