# 30_62_e11_local_execution_publication — E11 Local Use Case / Publication物理詳細設計

## 1. Scopeと既存コードの境界

現行 `interfaces/cli/scientific_stage.py` は `ScientificCoreAdapter` 実行後にManifestを `Path.write_text` する。現行 `interfaces/cli/estimation.py` は旧Product互換の `REQUIRES_REVIEW` を許す場合がある。現行 `product/ports/artifact_store.py` の `store/retrieve/exists/delete` は複数fileの一括公開を保証しない。

E11では新しいversioned Local laneへ分ける。既存の `causal-analysis-spec/2`／Product Web API/DB/Workerを遡及変更しない。本書は新Class候補の実装契約であり、コード／独立Science証拠ではない。

## 2. `E11LocalCausalUseCase`

### 2.1. Fields / Constructor

候補：`causal.local_application.use_case.E11LocalCausalUseCase`。
注入Port：`decoder: LocalConfigDecoder`、`refs: ContentReferencePort`、`capabilities: MethodCapabilityPort`、`identifier: IdentificationPort`、`estimators: EstimatorPort`、`diagnostics: DiagnosticPort`、`publisher: LocalPublicationPort`、`runtime: RuntimeEnvironmentPort`、`clock: ClockPort`。Constructor時にoptional Backendをimportしない。

### 2.2. Public methods

~~~python
def preflight(self, spec: LocalStudySpec) -> PreflightReport: ...
def run(self, spec: LocalStudySpec) -> LocalRunOutcome: ...
~~~

preflightはversion／secure Input Ref／static capability／privacy／pathと科学的適格性の検証可能範囲を返す。DGPや独立科学受入済みであると報告しない。

### 2.3. 処理順序と状態

1. `schema_version`を明示dispatchし、strict YAML/JSON parse。旧v2と無版はE11解釈禁止。
2. Trusted Root配下でQuestion/Design/Graph/Dataset/Upstream Refをsecure openし、bytes hash・Graph/Estimand/Designの意味上の一致を検査。
3. Method IDのOperation/Estimand/Backend/extra/API versionをresolve。他Method/Backendへのsilent fallback禁止。
4. Identificationを実行又は上流proofを検証。未確定Graphやunsupported strategyを成功へ変更しない。
5. Data EligibilityとEstimator Requestを再評価。NOT_IDENTIFIED、REQUIRES_REVIEW、PARTIALLY_IDENTIFIEDの自動点推定禁止。列挙された緩和可能WARNのみ理由付きoverride可。
6. Adapter実行。Outputはstaging sink限定。Method-specific inference、診断、scientific negative、effective env/seed/foldを収集。
7. typed ResultとGraph/diagnostics/Manifestを生成。Privacyとartifact hashesを検証し一括publish後readback。
8. `LocalRunOutcome`は `technical_status` と `identification_status/point/inference/science_acceptance` を別軸として返す。

### 2.4. Postcondition / Failure

`technical_status=COMPLETED`はVerified Manifestとcommit markerを持つ。Science negativeでも技術的には完了しうる。Config/入力/Backend/Publication exceptionをScientific Negativeに潰さない。途中失敗はcompleted marker無し。無効な上流proofではEstimatorを呼ばない。

### 2.5. Tests

`DD-E11-RUN01`正常pipeline、`RUN02`非識別でEstimator未呼出、`RUN03`wrong Backend/Estimand、`RUN04`confirmatory unsupported CI、`RUN05`Graph再固定は新識別、`RUN06`旧v2挙動不変、`RUN07`abort時はuncommitted。

## 3. `MethodCapabilityRegistry` / Adapter Factory

### 3.1. Fields / Responsibility

候補：`causal.local_application.capability_registry.MethodCapabilityRegistry`。Method IDごとにOperation、Estimand Family、Design/Eligibility、Backend ID、推論方式、Profile/Extra、Adapter Factoryを宣言。外部libraryはresolution後にlazy import。Methodが同じでも対象Estimand・inference configが異なれば別個の互換性判断を要する。

### 3.2. Methods

~~~python
def describe(self, method_id: str) -> MethodDescriptor: ...
def resolve(self, method_id: str, backend_id: str, profile: str) -> BackendCapabilityRecord: ...
def load_adapter(self, capability: BackendCapabilityRecord) -> ScientificAdapter: ...
~~~

`describe`はpure metadata。`resolve`でDistribution metadata、実効API signature/Version、指定Methodの利用可能性・Inference availabilityを検査。`load_adapter`だけがoptional importを実行する。Unavailable時は当該Methodのtyped reasonとし、core起動や旧v2を破壊しない。`pyproject.toml`・universal `uv.lock`・実効runtime・SBOM・Legalは別軸で記録。

### 3.3. Tests

`DD-E11-CAP01`ENV-BASE隔離、`CAP02`単独3Profile、`CAP03`Combined API parity、`CAP04`Versionとunsupported mode、`CAP05`transitive package有無とMethod選択区別、`CAP06`Customer Delivery legal blocked。

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

## 5. `LocalManifestReader` / `LocalRunManifest`

### 5.1. Fields / Interface

Manifest fieldsは `manifest_version=e11-local-manifest/1`、run_id/request_hash、upstream lineage、effective Method/Backend/Inference、seed/fold、runtime/uv.lock/BLAS/SBOM、Science states、artifact descriptors、privacy classification。Product旧`CliManifest`へ混在させない。

~~~python
def read_run(self, trusted_root: Path, run_id: str) -> VerifiedLocalRun: ...
~~~

ReaderはMarker→Manifest→Artifact bytesのhash/size/typeと上流refを検証する。無版、legacy、絶対参照、symlink、非有限JSON、missing output、unknown critical fieldsは拒否。Private Parquetはrow-level policy確認無しにreader APIで開かない。

### 5.2. Tests

`DD-E11-READ01`valid、`READ02`missing marker、`READ03`mismatch、`READ04`wrong version、`READ05`private suppression、`READ06`old v2 readback。

## 6. `LocalPrivacyPolicy`

### 6.1. Fields

`principal_uid, root_owner_uid, classification, row_export_requested, row_export_authorized, allowed_columns, max_rows, audit_context`。OS principalをProduct Membershipの権威とみなさない。

### 6.2. Method / Preconditions

`assert_export_allowed(spec, cli_flag, runtime_principal) -> None`は、Spec policy許可・CLI flag・OS owner/delegation・安全なroot/権限・column minimizationの全条件をANDで要求する。`--allow-row-level-export`フラグは意図であり認可証明ではない。CI共有Volume、sudo、container root、mountを含め実効アクセス境界を確認する。通常Result/JSON/stdout/logには個票を含めない。

### 6.3. Tests

`DD-E11-PRIV01`default no rows、`PRIV02`flag only deny、`PRIV03`UID mismatch、`PRIV04`0600/0700、`PRIV05`stdout/log leakage、`PRIV06`shared mount deny。

## 7. CLI entrypoint / Error bridge

候補`interfaces.cli.e11.command.main(argv: list[str]|None) -> int`。IFに従い0=technical complete（負のScience含む）、2=config、3=input/hash/path、4=backend/technical、5=publish。`--check-only`はArtifact無し、Static PreflightでありScience PASSではない。stderrには個票や秘匿入力を含めない。旧`ariadne-estimate`等の既存entrypoint・v2 override挙動は維持する。

## 8. Traceと受入

| G workstream | Physical obligation | Gate06 Contract |
|---|---|---|
| G01/G02 | local Graph/Question/Design、Identification gate | Graph/Proof/negative roundtrip |
| G03/G04/G05 | Method Registry/CATE、Privacy | Method compatibility/CI/permission |
| G06 | Temporal endpoint/lag | actual API／lossless encoding |
| G07/G08/G09 | Quasi/IV/AR/SCM Adapter | typed Result、Reference planning |
| G10 | Publish/Lock/Manifest/legacy | fault injection、Profile isolation、v2 regression |

Scientific bias/coverage/FWER/MCS/resource・LicenseはMethod別独立Gate07とLegal Gateで判断する。DD設計だけをScience/Legal PASS扱いしない。

参照：[E11 Domain/Port](30_61_e11_local_domain_ports.md)、[IF CLI](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、[IF Manifest](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)、[旧Manifest](30_60_cli_adapters.md)。