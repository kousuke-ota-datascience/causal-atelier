# 23_41_cli_scientific_ports

## 1. 境界・Compatibility

本InterfaceはFile I/OとCLI entrypointを介して因果分析UseCaseを実行する公開契約を規定する。ProductのWeb API（/api/v1）、Worker、DB/Execution/Result永続化とは別の公開境界だが、科学的Domain／Estimatorは共通であり、CLI専用の数理ロジックを定義しない。既存Ariadneの `ariadne-identify`／`ariadne-estimate`／`ariadne-refute`／`ariadne-sensitivity`、`causal-analysis-spec/2`、`CliManifest(manifest_version="2.0")`のReaderと呼出し互換性を維持する。

DomainはQuestion／Design／Graph／Estimandの意味と科学的適格性を所有する。CLI composition rootはversion dispatchを所有し、`ariadne.capabilities.causal.local_execution.LocalCausalUseCase`が順序・lineage gateを所有する。Scientific Port/AdapterはMethod-specific executionとBackend evidenceを所有する。CLI/File adapterは入力pathと成果物の安全な公開を所有する。Productの `ScientificCorePort` は既存 `ScientificStatus` のProduct型に依存するため、新しい型付きEffect/AR集合を無検証で同型へキャストしない。

本書はCLIのVersion/Request/Statusと、入口に依存しないScientific Portの型境界を規定する。実装の適合性は独立Contract Testで確認する。

## 2. Versionと入口

| Interface | Interface／互換規則 | 禁止する曖昧性 |
|---|---|---|
| Local causal CLI | `ariadne-causal-local` | 既存 `ariadne-estimate` の引数を異なるStudy解釈に変更しない |
| Study request | `e11-local-study/1` | `causal-analysis-spec/2`を別Schemaとして明示dispatchし、暗黙upgradeしない |
| Effect result | `e11-local-effect-result/1` | Product `TREATMENT_EFFECT_RESULT` payloadを無断拡張しない |
| Graph evidence | `e11-local-graph/1` | PAG/CPDAGをDAGへ暗黙変換しない |
| Run manifest | `e11-local-manifest/1` | 旧 `manifest_version=2.0` に新Fieldを黙示追加しない |
| Run status | `e11-local-status/1` | Technical statusとScientific statusを一軸へ併合しない |

CLI引数契約：`ariadne-causal-local --config STUDY.yaml --output-root ROOT [--check-only] [--json]`。
- `--config`：必須。ファイル読取、版識別、schema validationをしてからpath解決を行う。
- `--output-root`：必須。成功時のimmutabilityと公開境界。作業ディレクトリの暗黙採用は禁止。
- `--check-only`：実行・出力publish無しでconfig／path／hash／静的capability／eligibilityを検査。外部Backendが必要な深い科学実行のPASSを主張しない。
- `--json`：stdoutへ機械可読の制御Envelopeのみ。個票・秘匿データをstdoutへ流さない。
- 個票出力はStudyの`privacy.row_export_requested=true`で明示opt-in。外部CLI再確認Flagは設けない。実効UID所有private TrustedRootとMethod別schema/row/byte制限のAND判定は維持。
- 5つの`e11-local-*/1`識別子は固定。Marker`e11-commit/1`は別の内部versionである。無版入力を既定Versionとして推測しない。

## 3. Config request（Schema contract）

次はF06のstrict v1 wire（JSON Schema）に沿った構造例。P1-M08の個別config/eligibilityはMethod Registry側で別途判定するため、例だけでは実行可能としない。`ContentRef`は`identity/relative_key/sha256/media_type/schema_version`の5項目を持ち、旧例の`path`省略形を本Schema Versionで暗黙受理しない。ゼロ埋め`sha256`は**未実測のダミー**であり、実際の入力bytes検証には通らない。

~~~yaml
schema_version: e11-local-study/1
operation: ESTIMATE
run_id: example-run
analysis_mode: EXPLORATORY
inputs:
  question: {identity: question-1, relative_key: inputs/question.json, sha256: "0000000000000000000000000000000000000000000000000000000000000000", media_type: application/json, schema_version: null}
  design: {identity: design-1, relative_key: inputs/design.json, sha256: "0000000000000000000000000000000000000000000000000000000000000000", media_type: application/json, schema_version: null}
  graph: {identity: graph-1, relative_key: inputs/graph.json, sha256: "0000000000000000000000000000000000000000000000000000000000000000", media_type: application/json, schema_version: null}
  dataset: {identity: dataset-1, relative_key: inputs/dataset.parquet, sha256: "0000000000000000000000000000000000000000000000000000000000000000", media_type: application/vnd.apache.parquet, schema_version: null}
  identification: {identity: identification-1, relative_key: upstream/identification.json, sha256: "0000000000000000000000000000000000000000000000000000000000000000", media_type: application/json, schema_version: null}
estimand: {family: ATE, population: specified-target-population, contrast: treatment-versus-control}
method: {id: P1-M08, backend: native, config: {}}
inference: {requested: false, confidence_level: null}
randomness: {seed: 1234}
privacy: {classification: AGGREGATE, row_export_requested: false}
~~~

- `operation` は`DISCOVER / IDENTIFY / ESTIMATE / REFUTE / SENSITIVITY / DIAGNOSE`の**操作型**でありMethod IDの別名ではない。41 Methodは認可済みMethod registryにおける固定IDにより選択し、対応するOperation／Estimand／Backendを別途検証する。
- `analysis_mode` は `EXPLORATORY / CONFIRMATORY`。CONFIRMATORYにはMethod・対象Estimandに適合した認定済み推論方式と、要求する検証Evidenceが必要。点推定が有限であるだけではScience PASSにしない。
- `sha256` はファイルbytesのSHA-256小文字hex64。表現の正規化方法が識別子に影響するJSON等は読み込み時にcanonicalization spec/decoder版を照合する。pathの改名だけで同一内容とすることは許されるが、上流のDesign/Question/Graph identityはhashと別途保持する。
- `identification` はEstimation／下流Refutation等の該当操作で必須。元ResultのGraph/Question/Design/Dataset/Estimand hashを再照合し、旧v2 Manifestを本Versionの識別証拠として無検証受理しない。
- 設定自体のlogical snapshot hashと実効Backend/Method config hashを出力Manifestへ保存する。Overrideは適格なWARNの列挙済みreasonに限定し、識別未成立・Graph未確定・hash不一致を解除できない。

## 4. Port contractとauthority

| Port / Operation | 論理署名／返却 | Authority・拒否条件 |
| --- | --- | --- |
| `LocalConfigDecoder.decode(raw, *, declared_format)` | `ValidatedStudy` | strict version/key/Method Profile、旧v2 fallback禁止 |
| `ContentReferencePort.verify(ref, *, root)` | `VerifiedContent` | Application Port: `ariadne.capabilities.causal.ports.content_ref`、Concrete: `ariadne.interfaces.cli.local_causal.content_io.LocalContentReferenceAdapter`。root閉じ込めの実bytes/hash・race/symlink拒否 |
| `MethodCapabilityPort.resolve(request)` | `BackendCapabilityRecord` | Operation/Estimand/Backend/Inferenceと実効API、no fallback |
| `DiscoveryPort.discover(request, *, sink)` | `DiscoveryGraphOutcome` | P1-M06等の検証済Discovery RequestとPAG/CPDAG・科学的negativeを型付き返却。Staging限定 |
| `IdentificationPort.identify(request)` | `IdentificationOutcome` | validated proof・Graph/upstream hash |
| `EstimatorPort.estimate(request, *, sink)` | `EffectOutcome` | validated eligibility、stagingだけに出力 |
| `DiagnosticPort.run(request, *, sink)` | `DiagnosticOutcome` | Validated upstream/Method |
| `LocalPrivacyPolicyPort.authorize(*, study, root, principal, output_shape)` | `PrivacyDecision` | Study内の明示要求・実行UID所有のprivate Root・Method別column/row/byte上限 |
| `LocalPublicationPort.begin/seal/publish` | `StagingArtifactSink / ValidatedStagedBundle / CommittedLocalRun` | atomic no-replace・readback |
| `LocalPublicationPort.abort(*, sink, session, run_id, request_hash, root, reason)` | `None` | Internal same-session, pre-publish abort delegation; no final run cleanup |
| `LocalManifestReaderPort.verify(*, root, run_id)` | `VerifiedLocalRun` | Marker→Manifest→Artifact・Privacy・lineage |
| `LocalManifestFactoryPort.build(*, evidence)` | `ManifestValue` | Application Port; CLI concrete Adapter invokes unchanged P01 Manifest factory; no filesystem I/O or new public wire |

`DiscoveryPort`・`IdentificationPort`・`EstimatorPort`・`DiagnosticPort`は`ariadne.scientific.ports.causal`、`MethodCapabilityPort`は`ariadne.scientific.ports.capability`に配置する。旧Product `ScientificCorePort`の既存v2署名は不変とし、新しい型付きPortと既存ScientificCoreAdapterは共通のScientific Kernelを使う互換Bridgeで接続する。単純alias、複製推定器、Backendのoptional importをProtocol import時に実行することは禁止する。このCLI interfaceの同期実行はContractとし、Product Web Worker/DB lifecycleは本IFの所有範囲外。

### 4.1. Port間の正規署名と相互整合

上表の`Validated*Request`は自己申告型名でなく、factory検証とAdapter直前の再検証を要する。`TrustedLocalRoot`はnonroot EUID/owner/mode・local ext4/XFS・same-FS/dirfdを検証したCapability。UseCaseは`preflight(spec: ValidatedStudy, context: LocalRunContext)`／`run(spec,context)`を受ける。`LocalRunContext(root:TrustedLocalRoot, principal:LocalPrincipal)`はCLI composition rootが検証済みOS Capabilityから生成し、Studyに任意Pathを混入させない。現行CLIでは入力と出力を同一TrustedRoot配下の別相対keyに置く。公開Facade LocalPublicationPort.begin(*,run_id,request_hash,root,session=None)、seal(*,sink,manifest,privacy)、publish(*,bundle,root)をConcrete run-scoped Publisherに委譲する。sealはDecisionを同一Publisher.validate(manifest,*,privacy)へ転送。G01 immutable internal PrivacyDecisionはallowed/run_id/request_hash/VerifiedRootIdentity（同一生きたroot FDのdev/inode/owner/mode/FS）/principal_uid/AGGREGATE/row_export_requested=false/DISCOVER_AGGREGATE_ONLYを保持。Publisherはstaged study.json・現行root/principal・実Inventoryと注入Policy再評価を一致検証し、欠損/別run/root/UID/追加row出力/拒否はMarker・rename前にfail-closed。Reader Facadeの`verify(*,root,run_id)`はConcrete `read_run(root,run_id)`へ委譲する。非公開Portへ外部Backend object/任意最終Pathを渡さない。

### 4.1a. G01/P05 Manifest Factory Port and Adapter boundary

**Owner-adopted internal boundary (DEC-G01-P05-MANIFEST-BOUNDARY-01=A; formal 09/S10/S11 pending).** Add Application Port `ariadne.capabilities.causal.ports.manifest_factory.LocalManifestFactoryPort` with `build(self, *, evidence: ManifestBuildEvidence) -> ManifestValue`. Define immutable `ManifestBuildEvidence` in the same Application Port boundary with fields `study:ValidatedStudy`, `study_payload:Mapping[str,JsonValue]`, `status_payload:Mapping[str,JsonValue]`, `runtime:ManifestRuntimeFacts`, `stochastic:Mapping[str,JsonValue]`, `artifact_descriptors:tuple[ArtifactDescriptorView,...]`, `output_graph_ref:ContentRef|None`, `graph_negative_reason_codes:tuple[str,...]`, `review_science_evidence_ref:ContentRef|None`. `ManifestRuntimeFacts` has `repo_commit:str`, `dirty:bool`, `python_version:str`, `platform:str`, `uv_lock_sha256:str`, `distributions:Mapping[str,JsonValue]`, `api_probes:Mapping[str,JsonValue]`. These JSON mappings must be strict, deeply immutable snapshots; no data is invented or inferred from types. `ArtifactDescriptorView` must have the six existing fields `key/sha256/size_bytes/media_type/privacy_class/visibility` and values returned from P02 staging.

CLI-only concrete `ariadne.interfaces.cli.local_causal.manifest_factory.LocalManifestFactoryAdapter` maps this neutral evidence into P01's unchanged `RuntimeEvidence`, `ArtifactDescriptor` and nominal `ValidatedRunEvidence`, invokes P01 `LocalRunManifest.from_run_evidence`, returns the result as the existing `ManifestValue` Protocol. Factory validation is never bypassed or duplicated; Adapter cannot invent bytes, runtime facts or scientific negatives. Application imports no `ariadne.interfaces.cli.*`; CLI composition root injects `manifest_factory` as twelfth required constructor Port. Sequence: stage validated Study/Status/Graph-or-authentic-negative bytes → collect exact P02 descriptors → build immutable neutral evidence → `manifest_factory.build(evidence=evidence)` → `publisher.seal(sink=sink,manifest=manifest,privacy=same_decision)` → publish → independent Reader. Missing/malformed evidence or factory failure is fail-closed before seal/Marker/rename. Existing P01 ownership, P02 seal/publish signatures and backward-compatible begin calls, published JSON versions and G01_999 obligations stay unchanged.

### 4.1b. Internal publication session and pre-publication abort

The Application-owned module `ariadne.capabilities.causal.ports.local_io` defines nominal `PublicationSessionToken` as an empty identity-equality class (`__slots__ = ()`, no custom equality/hash, no payload). A fresh instance is constructed by the UseCase for each begin attempt, retained independently of the returned sink, and never serialized, logged or used as a public authentication credential.

~~~python
def begin(self, *, run_id: str, request_hash: str, root: TrustedLocalRoot,
          session: PublicationSessionToken | None = None) -> StagingArtifactSink: ...
def abort(self, *, sink: StagingArtifactSink, session: PublicationSessionToken,
          run_id: str, request_hash: str, root: TrustedLocalRoot,
          reason: str) -> None: ...
~~~

The optional begin parameter preserves existing calls and return type; legacy session=None is permitted for existing begin/seal/publish but is ineligible for facade abort. New P05 always supplies a fresh exact nominal token; invalid non-null token types are rejected before staging. At issuance the CLI Adapter binds its own object identity and that token to the original run-scoped Publisher, before calling concrete begin. No registry or second transaction. DD 30_62 §8.2a specifies private binding placement. The caller retains expected run_id/request_hash/root from its validated Study/context, not from the candidate sink.

Before delegating abort, Adapter checks all of: exact _Sink type; sink is its Publisher's original _sink; bound issuer is self; bound non-null token is the independently supplied exact nominal session (identity, not value equality); expected run_id and request_hash match the Publisher's values; expected root is the Publisher's original TrustedLocalRoot object; Publisher's policy is Adapter's injected policy; state is STAGING or VALIDATING. Reject mismatches before any mutation or handle release using existing typed PUBLICATION_FAILED. The reason is a nonsecret operational string. Same-policy different Adapter, same Adapter different run, and concurrent same-run attempts with distinct fresh tokens must be distinguishable. Caller must not reuse a token across attempts; no global token uniqueness registry is required. This protects against accidental substitution in trusted in-process code, not arbitrary private-attribute tampering or replacement of all trusted inputs. Per-session lifecycle calls are sequential; simultaneous calls on the same session are not authorized. Distinct sessions may be interleaved.

Call abort once after successful begin and strictly before invocation of publish on failure. After publish invocation, Application never calls abort, regardless of error; original Publisher owns rename/indeterminate handling. No abort before successful begin, no abort for PUBLISHING/COMMITTED/INDETERMINATE/ABORTED. Existing concrete abort closes handles and quarantines private residue, not secure erasure. A cleanup failure must not mask the primary typed error. No newly committed final run/marker; pre-existing final run untouched. Staged private marker may exist after seal and is not committed proof. Independent Reader remains mandatory.

Existing seal/publish, concrete publication algorithms, scientific StagingArtifactSink, public E11 wire and Product interfaces remain unchanged. Internal source changes are limited to token, optional begin argument, abort, and Publisher issuance binding/initialization. No implementation authorization follows from document preparation; formal approval and execution authorization are separately recorded.

`ContentRef`=`ariadne.shared.content_ref.ContentRef`、CLI wire DTO `LocalStudySpec`=`ariadne.interfaces.cli.local_causal.study.LocalStudySpec`、Application受理型 `ValidatedStudy`=`ariadne.causal.design.study.ValidatedStudy`、`GraphEvidence`=`ariadne.causal.discovery.graph_evidence.GraphEvidence`、`BackendCapabilityRecord`=`ariadne.scientific.capabilities.BackendCapabilityRecord`。各ClassのField/Constructor/Method・検証の7区分は30_60 §11〜12、30_61 §1〜5、30_62 §7が所有する。

**G01/P04 Method policy dispatchの移行契約（DEC-G01-P04-PRODUCT-POLICY-SHARING-01=B）：** Local P1-M06に対する`MethodCapabilityPort.resolve(ValidatedCapabilityRequest)`は新LocalのMethod metadata/pure eligibility authorityを利用し、検証済みMethod/Estimand/Design/Inference/Backend条件を保持する。旧Product v2 `ScientificValidationService`の`validate_submission`は**G01/P04から呼ばず、変更しない**。既存`ESTIMATOR_CAPABILITIES`は旧Product互換実装として存置するが、P1-M06のRegistry情報源または二重の新Method適格性規則ではない。将来の共通pure policyへの旧Product接続は`DEFERRED_PRODUCT_POLICY_BRIDGE`であり、現時点で呼出統合を実施・検証したと記載しない。公共Port署名、Product v2の既存契約、E11 wire Schema Versionは不変。旧ProductへのBridgeは別個のOwner承認と旧Product全Operation/Estimator回帰を経て適用し、未完了状態はG01_999の受入依存として可視化する。

GraphのEDIT/FIXとVersion ID発行は既存Product `GraphVersionService`が所有する。`GraphEvidence`はVersion writerではなく、`make_revision`は定義しない。Domain側のEstimator適格性は既存`ScientificValidationService`の判定を共通pure policyに統合し、Backend availabilityは`MethodCapabilityPort.resolve(request)`で独立検査する。

### 4.3. 既存Classとの再利用・依存方向

| 公開Contract | 再利用する既存Owner | 分離すべき責務 |
|---|---|---|
| CLI Decoder → `ValidatedStudy` | `ariadne.causal.design.schemas.CausalDesign`、既存`AnalysisSpecification` Validator | YAML/JSON構文はCLI、Method/Estimand科学的不変条件はCausal側の共通Policy |
| Scientific typed Ports | 旧`product.ports.scientific_core.ScientificCorePort`と`scientific.core_adapter.ScientificCoreAdapter` | 旧v2の5 Operation署名は維持し、共通Scientific KernelへBridge。別の推定器を二重化しない |
| Method Capability | 既存`ScientificValidationService`とMethod Registry | Method×Estimand/Inferenceと実効Backend probeは分け、唯一のMethod適格性規則を使う |
| Graph Evidence | 既存`GraphVersionService`とGraph意味Validator | ProductのGraphVersion/EDIT/FIXはProduct側。CLI Graph作成時に架空のVersionを発行しない |
| Local Publication/Reader | 既存`ArtifactStorePort`のbyte/hash処理 | 完全run単位のatomic no-clobber・Marker/Manifest/Privacy readbackは独立File Bundle Contract |

### 4.4. Discovery・Port間の呼出経路

- `LocalCausalUseCase.run(spec,context)`は`MethodCapabilityPort.resolve(ValidatedCapabilityRequest)`でOperation/Estimand/Backend/Inference/Method configを確認し、選択済`BackendCapabilityRecord`を`ValidatedDiscoveryRequest`等に結合する。具体Scientific Portは同一Method Registryの`load_adapter(capability)`を利用し、別Methodへのfallbackを禁止する。
- `DISCOVER`は`DiscoveryPort.discover(request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink)->DiscoveryGraphOutcome`へdispatchする。IDENTIFYはIdentificationPort、ESTIMATEはEstimatorPort、REFUTE/SENSITIVITY/DIAGNOSEはDiagnosticPortへdispatchする。Resultの型とOperation別Publication義務は23_42 §2.1に従う。
- G05ではStudyの個票出力要求、実行UIDが所有するprivate ext4/XFS TrustedRoot、Method別出力制限を`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`で確認する。第三者承認や鍵管理は必要としない。G01では個票出力を拒否する。
- `LocalPublicationPort`と`LocalManifestReaderPort`はApplication Portであり、Concrete CLI Publisher/Readerへ委譲する。独立Readerが`VerifiedLocalRun`を返す前にCOMPLETEDへ昇格しない。


### 4.5. Owner決定の現行適用 — OD-01/03/05は維持、G05署名方式のみ限定改訂（2026-11-21）

**P1-M05:** strict Method Requestは`operation=IDENTIFY, estimand.family=LATE_COMPLIER, design_profile=B0_BINARY_IV`を必須とし、二値Z/A単一IV・追加C無し・宣言済みrelevance/independence/exclusion/monotonicity/consistencyのconditional Proofと上流Hashを検査。DoWhy backendの出力labelからTargetを推定せず、有効なIV式とAPIの対応がないときtyped failureとする。IDENTIFYにEffect Result禁止、G08数値推定へ暗黙接続しない。

**G05 local row eligibility:** `LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)` がStudy request∧非root実行UID所有のprivate ext4/XFS TrustedRoot∧Method別ApprovedRowSchema/行列/byte制限を判断。`LocalPolicyVerifierPort`、`TrustedPolicyAnchor`、Ed25519/署名Key/失効は本local intermediate row exportのactive実装対象外。未公開`e11-local-study/1`の`privacy.policy_ref`は削除。初期拒否はexit3でrow iterator呼出0回、row bytes0。

**Row writer（OD-03署名保持）:** `RowEffectsParquetWriter.write(*,source:DeferredRowEffectsSource,study:ValidatedStudy,decision:PrivacyDecision,selection:ColumnSelection,sink:StagingArtifactSink)->ArtifactDescriptor`と`RowEffectsWriterFactory.create(*,serializer:ValidatedParquetSerializer,max_memory_bytes:int)->RowEffectsParquetWriter`を維持。G05でlocal eligibilityの成立後のみ行を遅延反復し、strict row schema/allowlist/limitsを検査してG01 sinkへstage。Writerは独立Publisher・Signer・Readerを持たず、同一run/Study/Source/RootとDecisionを検証。

**Method Profiles（OD-05）:** 40 Methodの専用Config/Question/Design/Output/Inferenceを各Owner Gateで厳格Schemaとして登録する。P1-M06既存schema draftsは実行PASSではない。Method未登録、Backend mismatch、未承認CIは別理由で拒否する。採用済みMethod意味論をBackend defaultsで上書きしない。

**状態:** 独立署名はOwner限定改訂で撤回済み。Method別RowSchema、実ext4/XFS/Parquet、独立Science、Gate FreezeとCoding Authorizationは未了。

## 5. Status／error／exit envelope

制御応答：

~~~json
{
  "schema_version": "e11-local-status/1",
  "run_id": "example",
  "technical_status": "COMPLETED",
  "identification_status": "IDENTIFIED",
  "point_availability": "AVAILABLE",
  "inference_availability": "NOT_REQUESTED",
  "science_acceptance": "NOT_EVALUATED",
  "reason_codes": [],
  "manifest_relative_path": "runs/example/manifest.json"
}
~~~

| Axis | 有効値 | 意味 |
|---|---|---|
| technical | `COMPLETED / VALIDATION_FAILED / CAPABILITY_UNAVAILABLE / EXECUTION_FAILED / PUBLICATION_FAILED` | プログラムとI/Oの状態 |
| identification | `IDENTIFIED / NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED / NOT_APPLICABLE` | 科学的識別の状態 |
| point | `AVAILABLE / NOT_AVAILABLE / NOT_REQUESTED` | 数値点推定の有無 |
| inference | `AVAILABLE / UNSUPPORTED / UNAVAILABLE / FAILED / NOT_REQUESTED` | 妥当な推論証拠の可用性 |
| science_acceptance | `NOT_EVALUATED / PASS / FAIL / INCONCLUSIVE / BLOCKED / NOT_APPLICABLE` | **独立した科学的検証**に基づく証拠状態 |

理由コードは`^[A-Z][A-Z0-9_]*$`を満たす安定した`UPPER_SNAKE_CASE`に正規化し、Machine-readable statusとhuman messageを分ける。Scientific negative（例：NOT_IDENTIFIED、unsupported confirmatory CI、weak-IV warning）は正常にpublishされた**負の分析結果**であって、勝手にtechnical failureや成功Effectへ変換しない。

CLI exit code：`0`＝制御上正常終了（科学的負結果を含む）、`2`＝config/schema/不適格request、**`3`＝input/hash/path/Privacy・Row Export認可拒否**、`4`＝method/backend technical/capability、`5`＝publication/readback failure。`0`はScience PASSを意味しない。stdoutにrun/status/manifest参照を返し、stderrに操作可能なエラーのみ出す。既存CLIのexit codeは遡及変更しない。

## 6. Method別互換と推論契約

全41 MethodのID・Scope・Estimand・DGP／NEG／REF／ACは[10_32 Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)をauthorityとする。対応しないMethod×Operation×Estimand×Backend×Inferenceの組合せは、実行前に `UNSUPPORTED_COMBINATION` として拒否する。

- P1 Frontdoor FD-A：限定線形・単一Mediator、数値ATEの識別・推定分離。DoWhy識別フラグを値の信頼性と同一視しない。
- P2：非IV CATE7方式と別DRIV-AのIV heterogeneous structural slopeを区別する。Method-specific nuisance/fold/seed/inference registryを保持。点推定のみの探索と確認的CI主張を分離。
- P3 B0：二値Z/A無調整complier LATE。B1：単一二値Z/A・事前指定Cの加法線形IV構造係数。通常Wald CIとAR反転集合を区別する。
- P3 Graph：FCI/PAGとPCMCI系の未確定端点・contemporaneous関係・lagの方向を保持。Graphの固定化は科学的真を意味しない。
- P3 Quasi：DiD、Event Study、ITS、Sharp/Fuzzy RD、SCM、SDIDは別Estimand／時刻、誤差相関、donor/cutoff条件を持つ。SCMの本Method contractはpoint-onlyであり、認定されたInference Method Versionへの明示変更なしにCIを主張しない。
- Negative Control NCE/NCOとOLS partial R²/point RV(q=1)は明示opt-inかつ限定モデルで実行し、non-significantを無交絡の証明としない。

Method-specific confidence intervalの欠落は `null + reason`。推論Registryが未承認の方式や外部Backend defaultを採用済みCIとして報告しない。

## 7. Internal scientific runtime capability

| Profile | Eligible extras | Interface上の扱い |
|---|---|---|
| ENV-BASE | coreのみ | optional MethodはUNAVAILABLE。旧v2は動作継続 |
| ENV-DOWHY | `e11-dowhy` | Method別実効DoWhy API／版本照合 |
| ENV-ECONML | `e11-econml` | method-specific CATE/DRIV、CI availability |
| ENV-TIGRAMITE | `e11-temporal` | PCMCI系、端点/lag、科学Backend実効適格性 |
| ENV-COMBINED | 上記3 extras | optional 後続相互運用試験。初期必須の実行Profileではなく未検証combinedをsupported扱いしない |
| ENV-RD | `e11-rdd`（Method別条件付き） | RD Backend/Inference の実効適格性を検証。顧客配布の受領者別判定は行わない |

`pyproject.toml`は宣言、`uv.lock`は解決集合、Runtime Manifestは実効版を記録する。初期必須はENV-BASE/DOWHY/ECONML/TIGRAMITEの各isolated venvと `uv lock --check / uv sync --locked / uv pip check`＋Method API smoke。ENV-COMBINEDは追加optional QAであり、初期に同時共存を保証しない。SBOMや受領者別顧客法務状態は内部CLIのRuntime/Manifest/Gateに含めない。外販は未確定でありE11新規要件を作らず、社内でのOSS利用について既存組織の遵守手順を適用する。未実測版を実効値として出力しない。

## 8. 恒久Interface Contract Test

| ID | Contract test | 負例と判定 |
|---|---|---|
| IF-E11-01 | 新/旧versionの明示dispatchと旧v2 byte-level/semantic readback | versionless、legacy auto-upgrade拒否 |
| IF-E11-02 | Question/Graph/Design/Dataset/IdentificationのhashとSchema | ref改変、wrong upstreamの実行拒否 |
| IF-E11-03 | 41 Methodのmethod/estimand/operation/backend/inference Registry整合 | unsupported combo／silent fallback禁止 |
| IF-E11-04 | 未確定Graph endpoint/lagとLocal親科学provenanceのround-trip（Product GraphVersion親は既存互換Bridge内で別検査） | PAG→DAG、circle消失を拒否 |
| IF-E11-05 | typed Effect/uncertainty/ScienceとAR集合のround-trip | infiniteをnull/finite CIへ丸めない |
| IF-E11-06 | NCE/NCO/RV opt-in、individual exportの拒否／許可境界 | Study未許可時での行レベル情報流出禁止 |
| IF-E11-07 | 4必須Profile、lock/capability、no optional import at core startup | unavailable隔離、選択Backend/Methodと旧v2。ENV-COMBINEDは必須でない |
| IF-E11-08 | technical exitとscientific negative、stderr/stdout非漏洩 | Science FAILをCLI error扱い・Science PASS偽装禁止 |
| IF-E11-09 | manifest/version/effective API/hash/readback | corrupted artifactやpartial publishを成功扱いしない |
| IF-E11-10 | method-specific DGP/NEG/REF/ACの網羅 | 同名別Estimandや未検証CIの自動代替禁止 |

対応要件：FR-185〜203、NFR-029〜036、Scientific AR-028〜044のうち本Interfaceが担う箇所。Interface Contractと独立科学的受入は別の判定である。

### Publication・Privacy・Errorの恒久契約

PublisherはLinux同一FS`renameat2(RENAME_NOREPLACE)`を必要とし、通常renameやcheck-then-rename代替は禁止。rename後fsync/readbackが不確定なら`PUBLICATION_INDETERMINATE`、既存run削除・上書き禁止。個票許可は明示Study request、same-UID private TrustedRoot、Method別column/row/byte制限のANDで、拒否時exit3、暗黙aggregate fallback禁止。Errorはreason codeとphaseを区別し、入力Schema破損=exit2、保存済みBundle readback破損=exit5。Exit0は科学的PASSではない。


### G01/P1-M06 categorical Design input authority — DEC-G01-P04-CATEGORY-DOMAIN-01=A

The authoritative strict **internal** Design profile for `DISCOVER/P1-M06` is `schema_drafts/e11_p1_m06_fci_design_profile_v1.schema.json` (URI `urn:ariadne:e11:p1-m06:fci-design-evidence:1`). The separate earlier `e11_g01_design_evidence_profile.schema.json` is a historical draft, **not an alternative eligible fallback** for this Method. Dispatch must not select it to admit a missing categorical universe. No public `Study`/Graph/Manifest/ContentRef field or version is added.

Within `Design.variables[]`, `CONTINUOUS` variables must have only the existing `name` and `measurement_scale`; `CATEGORICAL` variables additionally **must** declare `category_codes`: at least two distinct integer codes, strictly ascending, noncontiguous/negative allowed, constituting the **complete** possible-category universe (not the observed values). The Draft 2020-12 Schema enforces conditional requiredness, integer elements, uniqueness and cardinality; the validated input reader/semantic validator additionally rejects textual JSON number tokens such as `1.0` or `1e0` (which generic JSON Schema integer typing may accept as integral), booleans, unsorted codes, non-exact/unrepresentable values, unsafe duplicate keys and ambiguous decoding. Do not coerce to integer, remap category values, or infer a domain from `np.unique`.

Cross-reference against the already hash-verified immutable Design ContentRef and Dataset: exact `Design.variables` order/name must equal verified Dataset columns; each categorical observed cell must be a finite exact integer in its declared `category_codes` (no missing/NaN/Inf/bool/decimal/undeclared value). Declared but unobserved values remain in the universe. For `chisq/gsq`, enumerate the full Cartesian category combinations of every conditioning subset and all declared X/Y cell codes, rejecting empty strata or any independence-null expected count below the previously approved threshold 5 before FCI invocation. `fisherz` requires continuous variables and never accepts `category_codes`. This is an internal Design input compatibility tightening: earlier category-free categorical Design bytes are no longer eligible; previous validated continuous Design bytes remain eligible, subject to existing checks. Changed Design bytes must have new actual-file ContentRef SHA and Study JCS request hash; do not reuse a stale digest. This is not a claim that the category declaration or Markov/faithfulness assumptions have been empirically verified.

## 5. Internal strict Method Profile overlays

The public e11-local-study/1 Study.method.id dispatches to a registered strict Config/Question/Design/Output/Inference validator. Per-Method validators apply to existing unversioned Question/Design ContentRef bytes with independent hash check and cross-asset semantic equality; they do not introduce a new public wire version. Method-positive Output is still normalized to canonical Effect/Graph/diagnostic Artifact and G01 Publisher/Reader. Syntactic Study.inference.requested=true does not authorize unavailable finite or AR intervals or confirmatory PASS. Unknown, mismatched, unsupported or unavailable Method/Backend/CI reject with canonical typed reasons; no fallback.

## Local Scientific CLI interface invariants

新CLIの個票出力選択はStudyの`privacy.row_export_requested=true`によって表す。CLIに個票再確認フラグを追加せず、`LocalRunContext(root,principal)`と`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を使用する。未認可出力は個票Sourceへのアクセス前に拒否する。現行Local Studyには`policy_ref`を設けない。選択MethodのOperation/Estimand/Backend/Inference適格性をRuntime/Scientific Portで独立検査し、Profile未登録・未対応のMethod/推論を黙示代替しない。旧Product v2 wire/APIは明示dispatchで区別する。

### Strict Method profile factoring

For 40 non-FCI methods, each of the five internal profile kinds (Method Config, Question, Design, Output, Inference) has one strict **factored** schema bundle. The original 200 schema drafts remain a hash-pinned comparison baseline; the current design-authoritative *draft* is `schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json` with a shared core and per-Method overlays. The strict validator must **reconstruct** the original-equivalent Draft 2020-12 schema as a single JSON Schema object before validation. Combining separate `additionalProperties:false` fragments with `allOf` can reject valid declared fields and is forbidden. Dispatch must use exact Method ID and Profile Kind; missing, unknown, unverified or mismatched schema fails closed. The 200-file referential baseline, 40×5 coverage and reconstruction/parity obligations are governed by the method profile dispatch Registry; active runtime use requires separate Gate validation. Scientific semantics of target, identification assumptions, Backend capability, CI, scalar versus vector artifacts and cross-bundle ContentRef must be independently validated; AST identity is necessary but insufficient for scientific acceptance.


### Local publication PrivacyDecision forwarding and equality (G01)

The public `LocalPublicationPort.seal(*,sink,manifest,privacy)->ValidatedStagedBundle` keeps its signature. Its facade forwards the **same provided immutable PrivacyDecision** to the sink-owned `LocalArtifactPublisher.validate(manifest,*,privacy)`; a caller allow flag alone is insufficient. The decision binds allowed/run ID/JCS request hash/live verified root-dirfd identity/current principal/AGGREGATE/false row request/DISCOVER_AGGREGATE_ONLY. Concrete reopens staged Study, recomputes request hash and policy for actual aggregate inventory/Root/EUID, and rejects denied/stale or cross-run/root/UID/added-row mismatches before Marker/rename. ValidatedBundle and publish preserve the same run/hash/root/inventory and recheck them before rename. No change to public JSON schema or to existing Product API/CLI.


### Local P01 Codec and Graph-negative operation-specific validator

For G01 DISCOVER/P1-M06, `LocalConfigDecoder.decode(raw, declared_format)` strictly maps e11-local-study/1 YAML/JSON into typed validated Study, rejecting duplicate/unknown fields, unsuitable Method Config and no requested inference. `ContentRef.from_payload` validates exactly identity/relative_key/sha256/media_type/schema_version without touching FS; actual-file verification uses ContentReferencePort. `LocalRunManifest.from_run_evidence` checks typed Study/Status and staged ArtifactDescriptor joins. The Status wire `reason_codes` syntax stays generic, but the **G01 semantic operation validator** accepts Graph-negative only with exactly SCI_NO_ADMISSIBLE_PAG singleton and rejects any technical/mixed/unknown/duplicate code (even when repeated consistently in both sources). This pure classification cannot grant independent FCI scientific acceptance or committed publication. The public Port signatures and versions remain unchanged.


### G01 PrivacyDecision validation is structural, not issuer attestation

`LocalPublicationPort.seal(*,sink,manifest,privacy)` accepts a typed immutable **value**. The facade forwards it unchanged in value (no substituted decision). Concrete `LocalArtifactPublisher.validate(manifest,*,privacy)` reads current staged bytes and verified root/UID/inventory, invokes its trusted injected stateless `LocalPrivacyPolicy` independently, requires allowed and exact equality of **all declared decision fields**, and rejects detectable mismatch/denial before sealing. A separate value-identical instance is **not** a security violation by itself and MUST be accepted when all independently recomputed policy and physical conditions pass. No object identity check, trusted-issuer registry, MAC or signature is required. Public Port signature/wire remain unchanged.
