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

## 4. `LocalArtifactPublisher`

### 4.1. Fields / State

候補：`interfaces.cli.e11.publication.LocalArtifactPublisher`。Fieldsは `root: Path`、`run_id: str`、`request_hash: str`、`state: PREPARING/STAGING/VALIDATING/COMMITTED/ABORTED`、`staging_handle`、`artifacts: tuple[ArtifactDescriptor,...]`、`permission_policy`。rootはtrusted existing directoryで同一FileSystemを前提とする。

### 4.2. Methods

~~~python
def begin(self) -> StagingArtifactSink: ...
def stage_bytes(self, key: RelativeArtifactKey, data: bytes,
                media_type: str, classification: PrivacyClass) -> ArtifactDescriptor: ...
def validate(self, manifest: LocalRunManifest) -> ValidatedBundle: ...
def commit(self, validated: ValidatedBundle) -> CommittedRunRef: ...
def abort(self, reason: str) -> None: ...
~~~

StagingArtifactSinkによりBackendの出力先をstagingへ限定。絶対pathやroot外Objectへの書き込みはPort上禁止する。

### 4.3. Atomic algorithm

1. `root/.staging/{random-token}`を `0700` で作り、fileは`0600`。安全なdirfd/openatと`O_NOFOLLOW`相当を使い、単なる文字列のPath正規化でraceを防げたとみなさない。
2. 全Artifactをstagingへwrite、flush/fsync。JSON Schema・Parquet column/row privacy・size/sha256/relative keyをvalidate。
3. Manifest（Artifact一覧、source hash、runtime、privacy/Science）を作り、Manifest bytes hashを含む`_COMMITTED.json`を作る。Manifestに自身のdigestを含めない。
4. Readerと同じMarker→Manifest→全Artifact/readbackをstagingで実施。
5. filesystemの同一devと `runs/{run_id}`の非存在を確認。**no-clobber atomic directory rename**で一括公開する。単純なexists→renameを並行書込安全とみなさず、no-replace primitive／排他lockの実効方式を実装段階で検証。
6. `runs`親dirをfsync。公開後再readback。COMMITTEDを返す。
7. 失敗がrename前なら未公開stagingを保全・abort。rename後は公開済みの可能性があるので勝手に削除／上書きせず、ReaderとrecoveryがIntegrityを判定する。

Atomicityは**同一local filesystemでのdirectory visibility**であり、異Filesystem、object-store、NFS、電源断耐久性の一般的保証ではない。実機fsync/rename semantics、fault injectionが必須。

### 4.4. Idempotency / Recovery

既存`run_id`には同一`request_hash`かつ完全readback PASSの場合のみ既存Refを返す。違うrequestは`RUN_ID_CONFLICT`。corrupt/marker無しrunは隔離・診断対象でありoverwriteしない。staging cleanupはownerとactive lock/retentionを確認し、完了扱いしない。exactly-once科学計算は保証しない。

### 4.5. Tests

`DD-E11-PUB01`disk-full/crash、`PUB02`manifest/marker前後、`PUB03`rename前後、`PUB04`fsync failure、`PUB05`concurrent same run_id、`PUB06`symlink/path race、`PUB07`checksum corruption、`PUB08`private permissions、`PUB09`readback、`PUB10`既存Product Port独立。

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