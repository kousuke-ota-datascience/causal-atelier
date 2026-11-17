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

CLI引数契約：`ariadne-causal-local --config STUDY.yaml --output-root ROOT [--check-only] [--json] [--allow-row-level-export]`。
- `--config`：必須。ファイル読取、版識別、schema validationをしてからpath解決を行う。
- `--output-root`：必須。成功時のimmutabilityと公開境界。作業ディレクトリの暗黙採用は禁止。
- `--check-only`：実行・出力publish無しでconfig／path／hash／静的capability／eligibilityを検査。外部Backendが必要な深い科学実行のPASSを主張しない。
- `--json`：stdoutへ機械可読の制御Envelopeのみ。個票・秘匿データをstdoutへ流さない。
- `--allow-row-level-export`：個票CATEの生成を**明示的に要求する一条件**。入力privacy policy、OS主体・出力ディレクトリと別の承認条件を満たさなければ拒否。
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
privacy: {classification: AGGREGATE, row_export_requested: false, policy_ref: null}
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
| `LocalPolicyVerifierPort.verify(*, policy_ref, study, root, anchor)` | `VerifiedStudyPolicyEvidence` | Studyから独立した事前承認Authority |
| `LocalPrivacyPolicyPort.authorize(*, study, cli_row_flag, root, policy, output_shape)` | `PrivacyDecision` | 独立承認・private Root・column/row上限 |
| `LocalPublicationPort.begin/seal/publish` | `StagingArtifactSink / ValidatedStagedBundle / CommittedLocalRun` | atomic no-replace・readback |
| `LocalManifestReaderPort.verify(*, root, run_id)` | `VerifiedLocalRun` | Marker→Manifest→Artifact・Privacy・lineage |

`DiscoveryPort`・`IdentificationPort`・`EstimatorPort`・`DiagnosticPort`は`ariadne.scientific.ports.causal`、`MethodCapabilityPort`は`ariadne.scientific.ports.capability`に配置する。旧Product `ScientificCorePort`の既存v2署名は不変とし、新しい型付きPortと既存ScientificCoreAdapterは共通のScientific Kernelを使う互換Bridgeで接続する。単純alias、複製推定器、Backendのoptional importをProtocol import時に実行することは禁止する。このCLI interfaceの同期実行はContractとし、Product Web Worker/DB lifecycleは本IFの所有範囲外。

### 4.1. Port間の正規署名と相互整合

上表の`Validated*Request`は自己申告型名でなく、factory検証とAdapter直前の再検証を要する。`TrustedLocalRoot`はowner/ACL/mount/dirfdを検証したCapability。UseCaseは`preflight(spec: ValidatedStudy, context: LocalRunContext)`／`run(spec,context)`を受ける。`LocalRunContext(root:TrustedLocalRoot, principal:LocalPrincipal, cli_row_flag:bool)`はCLI composition rootが検証済みOS Capabilityから生成し、StudyにCLI Flag・任意Pathを混入させない。現行CLIでは入力と出力を同一TrustedRoot配下の別相対keyに置く。公開Facade `LocalPublicationPort.begin(*,run_id,request_hash,root)`、`seal(*,sink,manifest,privacy)`、`publish(*,bundle,root)`をConcrete run-scoped Publisherに委譲する。Reader Facadeの`verify(*,root,run_id)`はConcrete `read_run(root,run_id)`へ委譲する。非公開Portへ外部Backend object/任意最終Pathを渡さない。

### 4.2. Class配置・署名のAuthoritative Owner

`ContentRef`=`ariadne.shared.content_ref.ContentRef`、CLI wire DTO `LocalStudySpec`=`ariadne.interfaces.cli.local_causal.study.LocalStudySpec`、Application受理型 `ValidatedStudy`=`ariadne.causal.design.study.ValidatedStudy`、`GraphEvidence`=`ariadne.causal.discovery.graph_evidence.GraphEvidence`、`BackendCapabilityRecord`=`ariadne.scientific.capabilities.BackendCapabilityRecord`。各ClassのField/Constructor/Method・検証の7区分は30_60 §11〜12、30_61 §1〜5、30_62 §7が所有する。

GraphのEDIT/FIXとVersion ID発行は既存Product `GraphVersionService`が所有する。`GraphEvidence`はVersion writerではなく、`make_revision`は定義しない。Domain側のEstimator適格性は既存`ScientificValidationService`の判定を共通pure policyに統合し、Backend availabilityは`MethodCapabilityPort.resolve(request)`で独立検査する。

### 4.3. 既存Classとの再利用・依存方向

| 公開Contract | 再利用する既存Owner | 分離すべき責務 |
|---|---|---|
| CLI Decoder → `ValidatedStudy` | `ariadne.causal.design.schemas.CausalDesign`、既存`AnalysisSpecification` Validator | YAML/JSON構文・CLI FlagはCLI、Method/Estimand科学的不変条件はCausal側の共通Policy |
| Scientific typed Ports | 旧`product.ports.scientific_core.ScientificCorePort`と`scientific.core_adapter.ScientificCoreAdapter` | 旧v2の5 Operation署名は維持し、共通Scientific KernelへBridge。別の推定器を二重化しない |
| Method Capability | 既存`ScientificValidationService`とMethod Registry | Method×Estimand/Inferenceと実効Backend probeは分け、唯一のMethod適格性規則を使う |
| Graph Evidence | 既存`GraphVersionService`とGraph意味Validator | ProductのGraphVersion/EDIT/FIXはProduct側。CLI Graph作成時に架空のVersionを発行しない |
| Local Publication/Reader | 既存`ArtifactStorePort`のbyte/hash処理 | 完全run単位のatomic no-clobber・Marker/Manifest/Privacy readbackは独立File Bundle Contract |

### 4.4. Discovery・Port間の呼出経路

- `LocalCausalUseCase.run(spec,context)`は`MethodCapabilityPort.resolve(ValidatedCapabilityRequest)`でOperation/Estimand/Backend/Inference/Method configを確認し、選択済`BackendCapabilityRecord`を`ValidatedDiscoveryRequest`等に結合する。具体Scientific Portは同一Method Registryの`load_adapter(capability)`を利用し、別Methodへのfallbackを禁止する。
- `DISCOVER`は`DiscoveryPort.discover(request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink)->DiscoveryGraphOutcome`へdispatchする。IDENTIFYはIdentificationPort、ESTIMATEはEstimatorPort、REFUTE/SENSITIVITY/DIAGNOSEはDiagnosticPortへdispatchする。Resultの型とOperation別Publication義務は23_42 §2.1に従う。
- `LocalPolicyVerifierPort.verify(*,policy_ref,study,root,anchor)`はStudy外の事前承認Authorityで証拠を検証する。`LocalPrivacyPolicyPort.authorize(*,study,cli_row_flag,root,policy,output_shape)`は実効主体・許可範囲も照合する。G01では行出力要求またはFlag単独でも拒否。
- `LocalPublicationPort`と`LocalManifestReaderPort`はApplication Portであり、Concrete CLI Publisher/Readerへ委譲する。独立Readerが`VerifiedLocalRun`を返す前にCOMPLETEDへ昇格しない。

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

理由コードは安定したsnake_case等に正規化し、Machine-readable statusとhuman messageを分ける。Scientific negative（例：NOT_IDENTIFIED、unsupported confirmatory CI、weak-IV warning）は正常にpublishされた**負の分析結果**であって、勝手にtechnical failureや成功Effectへ変換しない。

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

## 7. Environment capabilityとLicense

| Profile | Eligible extras | Interface上の扱い |
|---|---|---|
| ENV-BASE | coreのみ | optional MethodはUNAVAILABLE。旧v2は動作継続 |
| ENV-DOWHY | `e11-dowhy` | Method別実効DoWhy API／版本照合 |
| ENV-ECONML | `e11-econml` | method-specific CATE/DRIV、CI availability |
| ENV-TIGRAMITE | `e11-temporal` | PCMCI系、端点/lag、顧客配布Legalは別判定 |
| ENV-COMBINED | 上記3 extras | universal lock、共存、旧CLI回帰 |
| ENV-RD | `e11-rdd`（法務・配布条件付き） | RD Backend・GPLの配布可否を受領者単位で判定 |

`pyproject.toml`は宣言、`uv.lock`は解決集合、Runtime Manifestは実効版、SBOMは成果物集合、Legal Reviewは受領者別の配布可否。全Profileはfresh isolated venvで `uv lock --check / uv sync --locked / uv pip check` とMethod API smokeを実施する。未実測版を実効値として出力しない。GPLに係る特定顧客へのDeliveryは法務承認前 `CUSTOMER_DELIVERY_BLOCKED` とする。

## 8. 恒久Interface Contract Test

| ID | Contract test | 負例と判定 |
|---|---|---|
| IF-E11-01 | 新/旧versionの明示dispatchと旧v2 byte-level/semantic readback | versionless、legacy auto-upgrade拒否 |
| IF-E11-02 | Question/Graph/Design/Dataset/IdentificationのhashとSchema | ref改変、wrong upstreamの実行拒否 |
| IF-E11-03 | 41 Methodのmethod/estimand/operation/backend/inference Registry整合 | unsupported combo／silent fallback禁止 |
| IF-E11-04 | 未確定Graph endpoint/lag/parent GraphVersionのround-trip | PAG→DAG、circle消失を拒否 |
| IF-E11-05 | typed Effect/uncertainty/ScienceとAR集合のround-trip | infiniteをnull/finite CIへ丸めない |
| IF-E11-06 | NCE/NCO/RV opt-in、individual exportの拒否／許可境界 | CLI flag単独での行レベル情報流出禁止 |
| IF-E11-07 | 全Profile、lock/capability、no optional import at core startup | unavailable隔離、Combined経路と旧v2 |
| IF-E11-08 | technical exitとscientific negative、stderr/stdout非漏洩 | Science FAILをCLI error扱い・Science PASS偽装禁止 |
| IF-E11-09 | manifest/version/effective API/hash/readback | corrupted artifactやpartial publishを成功扱いしない |
| IF-E11-10 | method-specific DGP/NEG/REF/ACの網羅 | 同名別Estimandや未検証CIの自動代替禁止 |

対応要件：FR-185〜203、NFR-029〜036、Scientific AR-028〜044のうち本Interfaceが担う箇所。Interface Contractと独立科学的受入は別の判定である。

### Publication・Privacy・Errorの恒久契約

PublisherはLinux同一FS`renameat2(RENAME_NOREPLACE)`を必要とし、通常renameやcheck-then-rename代替は禁止。rename後fsync/readbackが不確定なら`PUBLICATION_INDETERMINATE`、既存run削除・上書き禁止。個票許可は明示Study request、CLI flag、独立事前Policy、same-UID private TrustedRoot、column/row制限のANDで、拒否時exit3、暗黙aggregate fallback禁止。Errorはreason codeとphaseを区別し、入力Schema破損=exit2、保存済みBundle readback破損=exit5。Exit0は科学的PASSではない。
