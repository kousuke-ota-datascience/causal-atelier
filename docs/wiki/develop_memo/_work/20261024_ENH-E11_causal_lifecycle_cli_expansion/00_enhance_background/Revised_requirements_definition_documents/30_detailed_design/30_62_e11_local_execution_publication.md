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

候補：`causal.local_application.use_case.E11LocalCausalUseCase`。`LocalConfigDecoder`は**CLI composition root**に属し、Strict parse/Version検証済み`ValidatedStudy`のみApplicationへ渡す（Application内で別のdecodeを暗黙に行わない）。
注入Port：`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

- **Proposed signature:** `__init__(self, *, refs, capabilities, identifier, estimators, diagnostics, publisher, runtime, clock)` with typed Ports above.
- **Precondition:** Required Ports non-null and no optional scientific Backend import at construction. Factory wiring belongs to CLI adapter, not Product Web API. Any actual exception class/type is Freeze pending.
- **Postcondition:** A reusable stateless orchestration instance. Constructors must not create run directories or claim science readiness.

### 2.4. メソッド

~~~python
def preflight(self, spec: ValidatedStudy) -> PreflightReport: ...
def run(self, spec: ValidatedStudy) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

| Signature | Returns | Side effects / errors |
| --- | --- | --- |
| `preflight(self, spec: ValidatedStudy) -> PreflightReport` | capability/eligibility/input diagnostic | trusted input read permitted, **no** scientific execution or bundle publication; invalid version/refs typed |
| `run(self, spec: ValidatedStudy) -> LocalRunOutcome` | technical + scientific axes, committed ref or typed negative | backend execution only after validated eligibility; publication only via Publisher; errors preserve kind |

### 2.5. 処理仕様

1. CLI composition rootが`schema_version`を明示dispatchし、strict YAML/JSON parseで`ValidatedStudy`を構築。旧v2と無版はE11解釈禁止。ApplicationはValidatedStudyを受け取る（再検証するべきInput/Ref/Method/Privacyの意味検査は実行する）。
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
| `root` | `TrustedLocalRoot` | OS検証済みdirfd Capability | Immutable root handle。所有者・ACL・mount/同一FSを検証し、commit時にも整合を確認 |
| `run_id` | `str` | 正規化済LocalStudySpec | Immutable。23_42のsafe grammar |
| `request_hash` | `str` | canonical LocalStudySpec bytes | Immutable。小文字SHA256 hex64 |
| `state` | `PublishState` | FactoryでPREPARING | PREPARING→STAGING→VALIDATING→COMMITTED/ABORTED |
| `staging_handle` | `StagingHandle|None` | begin | State依存。Trusted FS descriptorを閉鎖管理 |
| `artifacts` | `tuple[ArtifactDescriptor,...]` | stage_bytes | Commitまで追加、公開後immutable |
| `permission_policy` | `LocalPrivacyPolicy` | 注入Policy | Resultのrelease policyと一致を要求 |

### 4.3. Constructor / Factory

- **Proposed** `__init__(self, root: TrustedLocalRoot, run_id: str, request_hash: str, permission_policy: LocalPrivacyPolicy)`。rootはOS/ACL/mount/dirfdを検証済みのCapability（任意Pathではない）。random staging tokenは`begin`時に生成する。実装時にRootの変更をcommit境界まで検出する。
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
5. `commit`は`runs/{run_id}`未存在を**非原子的exists判定に依存せず**保証するLinux `renameat2(RENAME_NOREPLACE)`（同mount/FSの実効対応を確認）を要求。Process lock、排他FS lockのみ、check-then-rename、通常の`Path.rename()`は代替として**禁止**。未対応FSはfail-closed。
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

- `__init__()`は特別な依存なし（**Proposed、N/A理由：read_runが検証済み`TrustedLocalRoot`を明示注入するstateless API**）。共通`LocalManifestReaderPort.verify(root,run_id)`はConcrete `read_run`へ委譲するAdapter。`Path`単独をTrustedRootに昇格しない。
- Reader instanceに暗黙のworking directory・current Project・Product DB／OS principalを仮定させない。

#### 5.2.4. メソッド

| Signature（Proposed） | Result | Side effect / failure |
| --- | --- | --- |
| `read_run(self, trusted_root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun` | Verified manifest and artifact descriptors | secure read only; marker/hash/version/root/permissions fail-closed |

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
| `authorization_evidence` | `VerifiedStudyPolicyEvidence|None` | Study要求と別の事前Policy権威に照合 | self-asserted Study boolは認可証跡にしない |
| `allowed_columns` | `tuple[str,...]` | policy | whitelisted minimal fields |
| `max_rows` | `int` | policy | bounded; enforce before output |
| `audit_context` | `Mapping[str,JsonValue]` | local provenance | secrets/raw rows forbidden |

### 6.3. Constructor / Factory

- **Proposed:** `__init__(self, *, principal_uid, root_owner_uid, classification, row_export_requested, authorization_evidence, allowed_columns, max_rows, audit_context)`。
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

候補`interfaces.cli.e11.command.main(argv: list[str]|None) -> int`。IFに従い0=technical complete（負のScience含む）、2=config、3=input/hash/path/**privacy/authorization denial（Owner採用）**、4=backend/technical、5=publish。`--check-only`はArtifact無し、Static PreflightでありScience PASSではない。stderrには個票や秘匿入力を含めない。旧`ariadne-estimate`等の既存entrypoint・v2 override挙動は維持する。

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


## 10. F03/F05/F06 機械契約の具体化・残る検証

- [F03 syscall/fsync/Reader ADR](../combined_review/104_20261117_prep02_f03_atomic_publish_contract.md)：staging全bytesとmarker・Manifestのvalidation → 各File/Dir fsync → `renameat2(...RENAME_NOREPLACE)` → `.staging`/`runs` Parent dirfsync → Reader検証。`EEXIST`は既存bundleの完全照合後に限り再利用。post-rename障害は不確定状態であり削除禁止。
- [F05 security threat model](../combined_review/105_20261117_prep02_f05_trusted_root_privacy_contract.md)：Trusted RootはUID一致＋private ACL/mount/namespaceを検証。自分でYAMLに書いた`row_export_authorized: true`を事前承認扱いしない。
- [F06 dispatch/codec/error](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)：5採用済みDiscriminator＋Commit Marker、strict JSON Schema v1草案、typed Error→CLI exit候補、unknown/old versionsの拒否。
- **Open:** Stable trusted Policy authority、Canonical JSON bytes/hash specification、OS/FS ABI and ACL probe, independent reviewer and runtime tests。候補Class仕様であって実装・Freeze・受入PASSではない。


## 11. Owner 4-choice integration: Row Policy / Codec / Exit（2026-11-17）

[DEC-PREP02-D](../combined_review/decisions/95_20261117_dec_prep02_four_owner_choices.md)により、行出力許可は別に事前承認されたPolicy authority（self-declared boolean不可）、明示Study request、CLI flag、OS Trusted Root、column/max_rows全件AND。`RowExportAuthorization.policy_ref`だけでは権限証明にならず、`VerifiedStudyPolicyEvidence`とtrust anchor確認が必要。要求された行出力が不許可なら**exit3**、aggregate出力へ黙ってfallbackしない。Rowをstaging・ログへ漏洩しない。

`LocalRunManifest.to_canonical_bytes()`はProductの`hash_mapping(default=str)`を呼ばず、独立E11 strict canonical Codecを用いる。候補RFC 8785 JCS版ID・cross-runtime vectorsは[F06](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)に規定。Canonical bytesの完全適合・Policy署名/承認機構とOS適格性を含むFreezeは未完了。


## 12. Common Port とPolicy Trust Anchorの物理境界

実装候補のPort署名は[統合Port契約](../combined_review/112_20261117_prep02_f03_f07_shared_port_signature_contract.md)を唯一のCross-Portレビュー入力とし、原文の各Class候補署名との差異をFreeze前に整合させる。`TrustedLocalRoot`はOS/ACL/mountを検証済みのcapabilityであり、単なる`Path`/self-reported Principal Evidenceではない。個票出力Policyは**実行EUIDに書換え権限のない独立Trust Anchor**で検証する必要がある。Ed25519署名付き事前承認artifactと管理者制御の公開鍵登録を[具体候補](../combined_review/113_20261117_prep02_f05_policy_trust_anchor_candidate.md)とするが、署名主体・鍵配布・失効の制度設計とSecurity reviewer判定はまだ未Freeze。

`E11Error`はreason codeと**phase**を保持する。同じSCHEMA_INVALIDでも入力時はCLI exit2、公開済みBundle readback破損時はexit5。Privacy/authorization denialはOwner採用済みexit3。科学的なNegative Outcomeは、正しいManifestを公開完了できる場合に限ってExit0となり得る。


## 13. Façade Port署名とConcrete Classの区別

本書§4の`LocalArtifactPublisher`は1 runの具体的な内部Class候補で、constructorにrun_id/rootを保持する設計案である。一方、E11 Applicationが依存する**公開Port**は[112 Cross-Port contract](../combined_review/112_20261117_prep02_f03_f07_shared_port_signature_contract.md)の`LocalPublicationPort.begin(run_id,request_hash,root)`/`seal`/`publish`であり、Façadeはrun毎のConcrete handleを生成する。`LocalArtifactPublisher.begin(self)`は**その内部HandleのLifecycle Method**であって同名のPort methodを置き換えるものではない。最終freeze前にClass Factory/Concrete Adapterに同一契約のUnit Testが必要。`LocalPrivacyPolicy.assert_export_allowed`もFacade `LocalPrivacyPolicyPort.authorize`による事前承認検証後の内部Guardであり、前者だけでPolicy署名／ACLを省略しない。


## 14. G01 Class.Method単位の実装・検証契約（`2〜7補足）

G01 [06](../../../10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_実装指示書.md)/[07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_テスト指示書.md)のSource of Truth。新Class増殖を目的とせず、**既存`2〜7のClass/Method**を実装対象／繰越しに分ける。

### 14.1 E11LocalCausalUseCase（`2；RUN01〜07）

- `preflight(ValidatedStudy)`はFile/Design/CI eligibility/OS root/Static Method capabilityを検証し、FCI execute/manifest publicationを呼ばない。`run(ValidatedStudy)`のG01分岐は`DISCOVER+P1-M06`に限定し、`ContentRef→Registry→FCI→Graph/Status/Manifest→Publisher→Reader`の順。結果は技術とScienceの別Axis（RUN01/03/04/06/07）。
- RUN02（未識別からEstimator禁止）とRUN05（Graph改訂後の**再識別**）はG02でのIntegration責務。G01 `GraphEvidence.make_revision`単体の証拠は`GRAPH04`で取得。G01ではIdentification/Estimator Portのダミー実行を作らない。

### 14.2 MethodCapabilityRegistry（`3；CAP01〜06）

- `describe`はP1-M06のDISCOVER/GRAPH_STRUCTURE/FCI/PAG descriptorとMethod ID拒否。`resolve(method_id,backend_id,profile)`は実効Distribution/API/Version/CI適格性を検証。`load_adapter`だけがFCI optional import。Base/Legacy import時にFCIをロードしない（G01分: CAP01/04/05）。
- 共通`MethodCapabilityPort.resolve(request:ValidatedCapabilityRequest)`はRegistry `resolve(method_id,backend_id,profile)`への**Facade**。同一Pythonメソッドを2署名で実装しない。CAP02/03の全Profiles、CAP06顧客配布LegalはG10等で検証し、G01 PASSを偽装しない。

### 14.3 LocalArtifactPublisher（`4；PUB01〜10）

| Concrete Method / 公開Port | Precondition/不変条件 | Return/失敗とDD |
|---|---|---|
| `LocalPublicationPort.begin(run_id,request_hash,root)`→`LocalArtifactPublisher.begin()` | TrustedRootが同一effective UID、Private dir/mount/FS、safe ID、random staging 0700 | 1個のSink、二重begin拒否（PUB06/08、PRIV03/04/06） |
| `stage_bytes(key,data,media_type,classification)` | dirfd・relative key・duplicate禁止、File 0600、G01はaggregate only | 実bytes hash/size descriptor。row bytes出力禁止（PUB06〜09、PRIV01/02/05） |
| `LocalPublicationPort.seal`→`validate(manifest)` | 全Artifact/Method/Status/Lineage/Privacy、markerはinventory外、file/dir fsync | sealed ValidatedBundle、欠損・不整合ならrename前abort（PUB01〜04/07、MAN01〜05） |
| `LocalPublicationPort.publish`→`commit(validated)` | Linux同一FS `renameat2(RENAME_NOREPLACE)`、check-then-renameやlock代替禁止 | 親dirs fsyncと独立Readback成功後だけCOMPLETED。競合／post-rename不定は上書き・削除禁止（PUB01〜05/07〜09） |
| `abort(reason)` | 事前公開stagingのみ | handle解放・安全な隔離、rename後は破壊的abort禁止（PUB01〜04） |

LocalPublicationPortはApplicationが依存するFacade、LocalArtifactPublisherはrun固有Concrete handleであり**重複した2つの公開機構ではない**。同一request hashの既存runも完全readbackで認証してから参照する（PUB05）。旧Product ArtifactStoreとは別（PUB10）。

### 14.4 LocalRunManifest / LocalManifestReader（`5）

- `LocalRunManifest.from_run_evidence / validate_invariants / to_canonical_bytes / from_payload`でDISCOVER時は`schema_dispatch.result=null`（Dummy Effect禁止）、Study/Status常在、Graphは有効なときだけ存在。Manifest self hashは禁止、外部Markerは実Manifest bytes SHA256、Codecは`e11-json-jcs-rfc8785/1`。Method/RunID/Graph/ContentRefs/Science axesを突合（MAN01〜06）。
- `LocalManifestReader.read_run(trusted_root:TrustedLocalRoot,run_id:RunId)`は具体Classの実装で、`LocalManifestReaderPort.verify(root,run_id)`から委譲。Marker→Manifest→全artifact bytes/type/hash/size→semantic lineage検査。保存済みBundle破損はexit5、入力時不正configはexit2。既存正常runを自動修復・削除しない（READ01〜07）。
- 有効なedge無しPAGも`graph.json`を発行できる一方、Backend API例外を成功Bundleに偽装しない。`study.json/status.json`は確定したrunに必要であり、Manifest/Markerはartifact inventory外。

### 14.5 LocalPrivacyPolicy / CLI（`6/7；PRIV01〜07）

- G01の個票出力は**未サポート**。Study row要求またはCLI row flagの**いずれか**があれば公開・staging前にexit3。特定用途のStudy Policy参照や自己申告boolだけで許可しない。Private Root/UID/ACL/mount・0700/0600・stdout/logの非漏洩はG01で確認（PRIV01〜06）。
- `PRIV07`のrestricted allow-columns、署名付事前許可、row boundはG05へ繰越し。G01のrow拒否を完全なRestricted export capabilityに見せない。
- `interfaces.cli.e11.command.main`は新入口のみ。Product v2 CLI/Manifestのreader等は触らない（RUN06/PUB10/MAN06/READ06）。

**G01の範囲外:** Identification/Eff/ARのMethod別統計処理、CAP02/03/06、PRIV07、PCMCI(Graph02)等。これらにG01の仮PASSを付けない。ソース未実装・試験未実行であることは本設計変更では変化しない。
