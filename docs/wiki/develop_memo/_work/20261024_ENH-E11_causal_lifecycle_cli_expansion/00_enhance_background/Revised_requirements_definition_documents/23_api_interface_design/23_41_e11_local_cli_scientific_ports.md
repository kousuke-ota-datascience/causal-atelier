# 23_41_e11_local_cli_scientific_ports — E11 Local CLI / Scientific Port Interface

## 1. 境界・Compatibility

本InterfaceはCLI-firstの追加実行系だけを対象とする。既存ProductのWeb API（/api/v1）、Worker、Product DB、Execution/Result正本、browser navigationを追加・変更しない。既存Ariadneの旧 `ariadne-identify`／`ariadne-estimate`／`ariadne-refute`／`ariadne-sensitivity`、`causal-analysis-spec/2`、`CliManifest(manifest_version="2.0")`のreaderと挙動は独立した旧laneとして保護する。

DomainはQuestion／Design／Graph／Estimandの意味と科学的適格性を所有する。Local applicationはversion dispatch、順序・lineage gateを所有する。Scientific Port/AdapterはMethod-specific executionとBackend evidenceを所有する。CLI/File adapterは入力pathと成果物の安全な公開を所有する。Productの `ScientificCorePort` は既存 `ScientificStatus` のProduct型に依存するため、E11の型付きEffect/AR集合を無検証で同型へキャストしない。

本書に記載する具体的なwire名は改訂版IFの**審査対象契約**であり、実装済みAPIの説明ではない。実装の一致性はContract Testで確認する。

## 2. Versionと入口

| Interface | 新規候補／互換規則 | 禁止する曖昧性 |
|---|---|---|
| E11 CLI | `ariadne-causal-local` | 既存 `ariadne-estimate` の引数をE11解釈に変更しない |
| E11 config | `e11-local-study/1` | `causal-analysis-spec/2` をE11へ自動upgradeしない |
| E11 effect result | `e11-local-effect-result/1` | Product `TREATMENT_EFFECT_RESULT` payloadを無断拡張しない |
| E11 graph evidence | `e11-local-graph/1` | PAG/CPDAGをDAGへ暗黙変換しない |
| E11 run manifest | `e11-local-manifest/1` | 旧 `manifest_version=2.0` に新Fieldを黙示追加しない |
| E11 contract status | `e11-local-status/1` | Technical statusとScientific statusを一軸へ併合しない |

CLI引数契約：`ariadne-causal-local --config STUDY.yaml --output-root ROOT [--check-only] [--json] [--allow-row-level-export]`。
- `--config`：必須。ファイル読取、版識別、schema validationをしてからpath解決を行う。
- `--output-root`：必須。成功時のimmutabilityと公開境界。作業ディレクトリの暗黙採用は禁止。
- `--check-only`：実行・出力publish無しでconfig／path／hash／静的capability／eligibilityを検査。外部Backendが必要な深い科学実行のPASSを主張しない。
- `--json`：stdoutへ機械可読の制御Envelopeのみ。個票・秘匿データをstdoutへ流さない。
- `--allow-row-level-export`：個票CATEの生成を**明示的に要求する一条件**。入力privacy policy、OS主体・出力ディレクトリと別の承認条件を満たさなければ拒否。
- Optionの正式名称・version IDは本契約をOwnerがSnapshot採用するまでは候補とする。未指定versionをE11として推測しない。

## 3. Config request（Schema contract）

次はF06のstrict v1 wire（審査用JSON Schemaドラフト）と整合する説明用YAML例。`ContentRef`は`identity/relative_key/sha256/media_type/schema_version`の5項目を持ち、旧例の`path`省略形をE11 v1で暗黙受理しない。ゼロ埋め`sha256`は**未実測のダミー**であり、実際の入力bytes検証には通らない。

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
- `identification` はEstimation／下流Refutation等の該当操作で必須。元ResultのGraph/Question/Design/Dataset/Estimand hashを再照合し、旧v2 ManifestをE11 proofとして黙認しない。
- 設定自体のlogical snapshot hashと実効Backend/Method config hashを出力Manifestへ保存する。Overrideは適格なWARNの列挙済みreasonに限定し、識別未成立・Graph未確定・hash不一致を解除できない。

## 4. Port contractとauthority

| Port / Operation | 主なRequest | Response | Fail-closed条件 |
|---|---|---|---|
| `LocalConfigDecoder.decode(bytes, expected_version)` | schema_version、YAML bytes | 構造化 `LocalStudySpec` | Unknown/versionless、余剰critical fields |
| `ContentReferencePort.verify(ref, root)` | relative path、宣言hash | verified bytes/hash、安定入力descriptor | traversal、symlink、missing、TOCTOU/hash差 |
| `MethodCapabilityPort.resolve(method_id, requested_backend, profile)` | Method registry／extra／環境 | `BackendCapability`、effective API/version | unsupported・missing extra・silent fallback |
| `IdentificationPort.identify(request)` | versioned Question/Design/Graph/Estimand/metadata | normalized `IdentificationOutcome`、proof／reason | unvalidated backend label、invalid endpoints |
| `EstimatorPort.estimate(request)` | IDENTIFIED proof・eligible design・method config・dataset | `EffectOutcome`、diagnostics・inference metadata | NONIDENTIFIED/REVIEW、estimand mismatch、invalid support |
| `DiagnosticPort.run(request)` | valid upstream Result + Method | typed refutation/sensitivity/quality result | missing upstream/prohibited method |
| `LocalPublicationPort.publish(bundle)` | staged immutable artifacts + manifest metadata | committed run reference | non-atomic path、integrity・privacy failure |
| `LocalManifestReader.verify(run_ref)` | committed run directory | verified schema+provenance+artifact inventory | marker無し、checksum不一致、不完全bundle |

`IdentificationPort`や`EstimatorPort`のinterface型はE11 Domainから定義する。既存Product `ScientificCorePort`への単純aliasは禁止し、backendのoptional importをProtocol／Port import時に実行しない。sync実行は初期仕様とし、E11のWeb Worker/DB lifecycleは対象外。

## 5. Status／error／exit envelope

制御応答候補：

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

| Axis | 有効値（審査対象） | 意味 |
|---|---|---|
| technical | `COMPLETED / VALIDATION_FAILED / CAPABILITY_UNAVAILABLE / EXECUTION_FAILED / PUBLICATION_FAILED` | プログラムとI/Oの状態 |
| identification | `IDENTIFIED / NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED / NOT_APPLICABLE` | 科学的識別の状態 |
| point | `AVAILABLE / NOT_AVAILABLE / NOT_REQUESTED` | 数値点推定の有無 |
| inference | `AVAILABLE / UNSUPPORTED / UNAVAILABLE / FAILED / NOT_REQUESTED` | 妥当な推論証拠の可用性 |
| science_acceptance | `NOT_EVALUATED / PASS / FAIL / INCONCLUSIVE / BLOCKED / NOT_APPLICABLE` | **該当Gateの07独立科学検証**に基づく証拠状態 |

理由コードは安定したsnake_case等に正規化し、Machine-readable statusとhuman messageを分ける。Scientific negative（例：NOT_IDENTIFIED、unsupported confirmatory CI、weak-IV warning）は正常にpublishされた**負の分析結果**であって、勝手にtechnical failureや成功Effectへ変換しない。

CLI exit code候補：`0`＝制御上正常終了（科学的負結果を含む）、`2`＝config/schema/不適格request、`3`＝input/hash/path、`4`＝method/backend technical/capability、`5`＝publication/readback failure。`0`はScience PASSを意味しない。stdoutにrun/status/manifest参照を返し、stderrに操作可能なエラーのみ出す。既存CLIのexit codeは遡及変更しない。

## 6. Method別互換と推論契約

全41 MethodのID・Scope・Estimand・DGP／NEG／REF／ACは[10_32 Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)をauthorityとする。対応しないMethod×Operation×Estimand×Backend×Inferenceの組合せは、実行前に `UNSUPPORTED_COMBINATION` として拒否する。

- P1 Frontdoor FD-A：限定線形・単一Mediator、数値ATEの識別・推定分離。DoWhy識別フラグを値の信頼性と同一視しない。
- P2：非IV CATE7方式と別DRIV-AのIV heterogeneous structural slopeを区別する。Method-specific nuisance/fold/seed/inference registryを保持。点推定のみの探索と確認的CI主張を分離。
- P3 B0：二値Z/A無調整complier LATE。B1：単一二値Z/A・事前指定Cの加法線形IV構造係数。通常Wald CIとAR反転集合を区別する。
- P3 Graph：FCI/PAGとPCMCI系の未確定端点・contemporaneous関係・lagの方向を保持。Graphの固定化は科学的真を意味しない。
- P3 Quasi：DiD、Event Study、ITS、Sharp/Fuzzy RD、SCM、SDIDは別Estimand／時刻、誤差相関、donor/cutoff条件を持つ。初期SCMはpoint-only。
- Negative Control NCE/NCOとOLS partial R²/point RV(q=1)は明示opt-inかつ限定モデルで実行し、non-significantを無交絡の証明としない。

Method-specific confidence intervalの欠落は `null + reason`。推論Registryが未承認の方式や外部Backend defaultを採用済みCIとして報告しない。

## 7. Environment capabilityとLicense

| Profile | Eligible extras（案） | Interface上の扱い |
|---|---|---|
| ENV-BASE | coreのみ | optional MethodはUNAVAILABLE。旧v2は動作継続 |
| ENV-DOWHY | `e11-dowhy` | Method別実効DoWhy API／版本照合 |
| ENV-ECONML | `e11-econml` | method-specific CATE/DRIV、CI availability |
| ENV-TIGRAMITE | `e11-temporal` | PCMCI系、端点/lag、顧客配布Legalは別判定 |
| ENV-COMBINED | 上記3 extras | universal lock、共存、旧CLI回帰 |
| ENV-RD | `e11-rdd`候補（追加・条件付き） | RD Backend・GPLの個別採否と法務Gate必要 |

`pyproject.toml`は宣言、`uv.lock`は解決集合、Runtime Manifestは実効版、SBOMは成果物集合、Legal Gateは受領者別の配布可否。全Profileはfresh isolated venvで `uv lock --check / uv sync --locked / uv pip check` とMethod API smokeを実施する。未実測版を実効値として出力しない。GPLに係る特定顧客へのDeliveryは法務承認前 `CUSTOMER_DELIVERY_BLOCKED` とする。

## 8. 受入契約（IF-01）

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
| IF-E11-10 | method-specific DGP/NEG/REF/ACとG01〜G10追跡 | 同名別Estimandや未検証CIの自動代替禁止 |

対応要件：FR-185〜203、NFR-029〜036、Scientific AR-028〜044のうち本Interfaceが担う箇所。全44件の責務対応は[BD-01 Trace](../bd01_review/91_requirement_architecture_trace.md)で確認する。Implementation ContractとIndependent Science Gateは別判定とする。


## PREP-02 Owner-approved Version/Privacy boundary (2026-11-17)

[DEC-PREP02](../combined_review/decisions/94_20261117_dec_prep02_owner_architecture_choices.md) adopts Options A/A/A. The five literal `e11-local-*/1` identifiers in §2 are **now adopted identifiers**, while CLI signatures, Protocol typing, exact JSON Schema and implementation are still not frozen. Unknown/versionless/legacy-v2 input must fail closed in E11 decoder; legacy reader behavior stays separate. `--allow-row-level-export` does not confer authorization: same-UID, private owner-controlled trusted local root, preauthorized Study policy and explicit flag are jointly required; delegated/shared/CI/container-root-accessible paths are outside initial scope. Publisher is constrained to same-FS Linux atomic no-replace with unsupported platforms rejected. This supersedes the 'candidate until Owner snapshot adoption' qualification **only for version identifiers and three selected policies**.



## 9. F04 Port境界契約の具体化（2026-11-17）

`E11LocalApplication`から見た`ContentReferencePort/MethodCapabilityPort/IdentificationPort/EstimatorPort/DiagnosticPort`はProduct `ScientificCorePort`の子型ではない。新E11のDTOはScientific status・Estimand・Proof・Inferenceの意味を独立に持ち、既存`ResultType`や`ScientificStatus`へ無断で射影しない。Backendに任意最終Pathの書込みを許すことなく`StagingArtifactSink`へ出力する。Local `Publisher/Reader`は既存Product `ArtifactStorePort`の`store/exists/retrieve/delete`では実現できない同一FS immutable multi-file publicationを提供する。E11版と旧`CliManifest(2.0)`は別Readerでstrict dispatchする。

Portの候補署名/Negative case/Regression obligationsは[F04 ADR候補](../combined_review/98_20261117_prep02_f04_port_boundary_adr_candidate.md)、値型とAdapter境界は[30_61](../30_detailed_design/30_61_e11_local_domain_ports.md)`11。**候補Port署名はFreeze未了であり、現行実装のAPIではない。**


## 10. F03/F05/F06共通Port・Version・Error契約（Freeze準備）

- [F03 Atomic no-replace出版契約](../combined_review/104_20261117_prep02_f03_atomic_publish_contract.md)：Linux `renameat2(RENAME_NOREPLACE)`を必須とし、ロックや普通のrenameで代替しない。Producerは`ValidatedStagedBundle`、Readerは`VerifiedLocalRun`を返す。未検証・競合・crash時に成功を主張しない。
- [F05 Trusted Root/Privacy契約](../combined_review/105_20261117_prep02_f05_trusted_root_privacy_contract.md)：Local Principal、ACL/mount、Owner一致と事前承認済みPolicyの証跡を検証。Study自己申告boolのみで個票を許可しない。
- [F06 Dispatch/Codec/Error契約](../combined_review/106_20261117_prep02_f06_dispatch_codec_error_contract.md)：採用済み5種のversionと`e11-commit/1` markerを厳格dispatch。Unknown/legacyはfail-closed。構造は[Schema draft一覧](schema_drafts/)に対応。
- **状態:** `CANDIDATE / OWNER_AAA_ADOPTED / SCHEMAS_NOT_FROZEN / INDEPENDENT_REVIEW_NOT_RUN`。`23_41`内の旧候補表現はA/A/A採用済みversion値を撤回するものではない。
