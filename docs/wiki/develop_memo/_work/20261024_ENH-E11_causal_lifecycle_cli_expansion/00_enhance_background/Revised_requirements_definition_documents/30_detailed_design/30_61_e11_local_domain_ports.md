# 30_61_e11_local_domain_ports — E11 Local Domain / Scientific Port 物理詳細設計

## 1. モジュール構成・依存方向

以下はENH-E11の新Local laneの実装候補。既存`src/ariadne/product/`のDomain/Portを無制限に複製せず、共通純粋値とAdapterの分担を確認してから着手する。

~~~text
src/ariadne/
  causal/local_contract/                  # E11 Domain value / validation (外部科学library不要)
    references.py                         # ContentRef / CanonicalRef
    study.py                              # LocalStudySpec / EstimandRef
    graph.py                              # GraphEvidence / EndpointEdge
    identification.py                     # IdentificationOutcome / EstimatorRequest
    effect.py                             # EffectOutcome / InferenceEvidence / ARConfidenceSet
    ports.py                              # Protocol definitions
  causal/local_application/                # pure use case flow
    use_case.py                           # E11LocalCausalUseCase
    capability_registry.py                # MethodCapabilityRegistry
  scientific/local_adapters/               # optional backend implementations
    native.py, dowhy.py, econml.py, temporal.py, quasi.py
  interfaces/cli/e11/                       # CLI config / wiring / file I/O
    command.py, config_decoder.py, publication.py, manifest_reader.py
~~~

依存矢印は `CLI→Application→Domain Port←Scientific Adapter`。Domainは `product.domain` や `product.ports.scientific_core` を**直接継承しない**。既存Product側で純粋型を再利用する場合はadapterを明示し、Product/Localの権威、lifecycle、science statusを混ぜない。

Portに外部libraryのModel/Estimator Objectを渡さず、Typed DTO／bytes/content-refのみを通す。Package import時にoptional Backendをロードしない。

## 2. ContentRef（PROPOSED）

### 2.1. 識別とフィールド

配置候補 `causal.local_contract.references.ContentRef`。immutable dataclass：`identity: str`、`relative_key: str`、`sha256: str`、`media_type: str`、`schema_version: str|None`。Data bytesとmetadataの識別子を混同しない。外部入力の絶対pathやaccess tokenを正本値に保持しない。

### 2.2. Constructorと処理

`ContentRef.from_payload(payload: Mapping[str, JsonValue]) -> ContentRef`：
- strict keys、sha256小文字hex64、非空identity、relative keyを確認。
- dotdot、absolute、drive letter、NUL、backslash区切りの混合、不正Unicode正規化、symlink targetの危険な参照を拒否。
- pathの安全性検証は**静的文法のみ**であり、その後の実file openを代替しない。

`ContentReferencePort.verify(ref: ContentRef, trusted_root: Path) -> VerifiedContent`：
- I/O adapterによりroot閉じ込めOpen、同一file descriptorからhashを計算し実際の内容を返す。
- hash mismatch、path race、size policy、read failureをTyped exception。
- 参照解決に基づく科学内容検証は別Domain validatorへ渡す。

### 2.3. 検証

`DD-E11-REF01`：相対／hash valid。`REF02`：traversal/symlink/race。`REF03`：入力差替え/TOCTOU。`REF04`：metadata-only同一IDの別bytes禁止。FR-185、NFR-029、NFR-031に対応。

## 3. LocalStudySpec / LocalConfigDecoder（PROPOSED）

### 3.1. Class/fields

配置候補 `causal.local_contract.study.LocalStudySpec`。immutable：
- `schema_version: Literal["e11-local-study/1"]`
- `run_id: str`、`operation: LocalOperation`、`analysis_mode: AnalysisMode`
- `question: ContentRef`、`design: ContentRef`、`graph: ContentRef|None`、`dataset: ContentRef`、`identification: ContentRef|None`
- `estimand: EstimandRef`、`method: MethodRequest`、`inference: InferenceRequest`
- `randomness: RandomnessSpec`、`privacy: LocalPrivacySpec`

### 3.2. Factory・method

`LocalConfigDecoder.decode_yaml(raw: bytes) -> LocalStudySpec`：
- YAML duplicate key、alias/excessive nesting、構造外のPython Tag・任意オブジェクトを拒否し、strict schema validation。
- `schema_version`を先に判定。unknown/legacyはE11 parserに流さない。
- `LocalStudySpec.validate_local_invariants() -> tuple[Reason,...]`：required refs by Operation、Method/Estimand target、analysis_mode/inference、row export request、Run IDなどの純粋不変条件を収集。
- Result/Manifest bytesを生成せず、副作用は無し。config hashはcanonical encoding後のbytesのdigestから求め、canonicalization versionを記録する。

### 3.3. 検証

`DD-E11-SPEC01`：valid schema／strict unknown field、`SPEC02`：旧v2 dispatch、`SPEC03`：confirmation requires inference、`SPEC04`：Method/estimand mismatch。FR-185、FR-201、NFR-029/036、AR-034。

## 4. GraphEvidence / GraphVersion（PROPOSED）

### 4.1. フィールド

`GraphEvidence(kind: GraphKind, nodes: tuple[Node,...], edges: tuple[EndpointEdge,...], temporal: TemporalConvention|None, version_id: str, parent_version_id: str|None, provenance: GraphProvenance, content_hash: str)`。
`EndpointEdge`は `source, target, source_mark, target_mark, lag`。端点markはTAIL/ARROW/CIRCLE、lagは符号・基準時刻のConventionと組で扱う。

### 4.2. Factory・メソッド

- `GraphEvidence.from_canonical_json(raw: bytes) -> GraphEvidence`：Graph Schema厳格照合、endpoint/temporal domain検証。隠れた潜在交絡情報の喪失を拒否。
- `GraphEvidence.make_revision(edit: GraphEdit, rationale: str, assumptions: tuple[str,...]) -> GraphEvidence`：元を不変に保ち、新version ID／parent／edit rationaleを必須。DAGへの変換は新仮定の科学レビューが必要。
- `GraphEvidence.canonical_payload() -> Mapping[str, JsonValue]`：Node/Edge/lag/endpointとprovenanceのlossless round-trip。Graphの「FIXED」は編集状態でありScientific Truthとは別。
- 未確定Graphからの点推定は、別証明が独立受入されない限り不許可。D06将来の一般化識別自動実装は初期範囲外。

### 4.3. 検証

`DD-E11-GRAPH01`：FCI PAGのcircle/arrow/bidirected round-trip、`GRAPH02`：PCMCI系lag/contemporaneous、`GRAPH03`：PAG→DAG silent変換拒否、`GRAPH04`：版の不変性/再識別。FR-186/196、AR-028/036/043。

## 5. IdentificationOutcome / EstimatorRequest（PROPOSED）

### 5.1. フィールド

`IdentificationOutcome`：`identification_id`、`estimand: EstimandRef`、`status: IdentificationStatus`、`strategy`、`proof: IdentificationProof|None`、`upstream: UpstreamHashSet`、`reasons: tuple[ScientificReason,...]`。
`EstimatorRequest`：`method_id`、`estimand_family`、`identification_ref`、`question/design/graph/dataset_hashes`、`method_config`、`inference_request`。

### 5.2. メソッドと実行前ゲート

- `IdentificationOutcome.from_adapter(raw: AdapterIdentification) -> IdentificationOutcome`：Backend独自StatusをDomainの証拠・Reasonに正規化し、method／assumptions／GraphVersion／対象Estimandの裏付けを要求。DoWhyの内部ATE labelからLATE等を推測しない。
- `EstimatorRequest.assert_eligible(identification: IdentificationOutcome, design: CausalDesignEvidence, capability: BackendCapability) -> ValidatedEstimatorRequest`：上流hash全一致、対象Estimand、Method専用assumptions、必要Instrument/Mediator/support、Data Eligibility、confidence policyを検査。
- `NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED` は新E11の点推定に自動通過させない。緩和可能な列挙WARNのみoverride理由を受理。B0/B1/DRIVを別Estimand familyとしてvalidateする。
- 不適格なら `ScientificNegativeOutcome` の型付き結果を返し、外部Backendを呼ばない。Schema/path mismatchはtechnical validation failureへ分離する。

### 5.3. 検証

`DD-E11-ID01`：B0/B1/DRIVの誤label拒否、`ID02`：graph/design/hash差、`ID03`：nonidentified/review override拒否、`ID04`：新GraphVersionで再識別。FR-187/194/199、AR-029/039/043。

## 6. ARConfidenceSet / InferenceEvidence（PROPOSED）

### 6.1. フィールド

`ARConfidenceSet`：`confidence_level: float`、`components: tuple[ExtendedRealInterval,...]`、`topology: SetTopology`、`inversion_evidence: ContentRef`。`ExtendedRealInterval`は下上端 `FINITE(value) / NEG_INFINITY / POS_INFINITY` + closed flags。
`InferenceEvidence`：`availability: InferenceAvailability`、`kind`、`interval: FiniteInterval|None`、`confidence_set: ARConfidenceSet|None`、`reason: ScientificReason|None`、`method_config`。

### 6.2. メソッド・不変条件

- `ARConfidenceSet.from_components(level, components, evidence) -> ARConfidenceSet`：有限性、順序、重複と接触するintervalの正規化、topology分類（ALL_REAL > DISCONNECTED > UNBOUNDED > BOUNDED）を行う。
- `ARConfidenceSet.contains(beta: float) -> bool`：endpoint open/closedと∞を尊重。ALL_REALは任意有限betaを含む。
- `ARConfidenceSet.to_payload() / from_payload()`はJSON Infinity/NaNを使わず同じ数学集合に往復。
- 正常なB0/B1 Anderson–Rubin反転にEMPTYは出さない。閾値/探索失敗なら `FAILED + reason`、有界区間へ捏造しない。
- `InferenceEvidence.validate_for(mode, method)`：EXPLORATORYのpoint-onlyとCONFIRMATORYの有効推論要件を区別。SCM初期point-onlyを確証的CIありと報告しない。

### 6.3. 検証

`DD-E11-AR01`：ALL_REAL、two-ray DISCONNECTED、片側非有界、有限BOUNDED、`AR02`：normal EMPTY拒否、`AR03`：round-trip、`AR04`：CI unavailable reason、`AR05`：CONFIRMATORY fail-closed。FR-202、AR-040、NFR-036。

## 7. EffectOutcome / BackendCapabilityRecord（PROPOSED）

### 7.1. フィールド

`EffectOutcome`：`result_id`、`estimand`、`point_availability`、`point_value: float|None`、`inference: InferenceEvidence`、`science_acceptance`、`diagnostics: tuple[DiagnosticRef,...]`、`method_evidence`、`upstream_hashes`。
`BackendCapabilityRecord`：`method_id, backend_id, distribution_version, adapter_version, api_signature_hash, extra, profile, available, reason`。

### 7.2. メソッド

- `EffectOutcome.validate_consistency()`：nonfinite point拒否、null reason必須、point≠Science acceptance、CI/AR型とEstimand不一致を拒否。
- `BackendCapabilityRecord.check(request)`：実効Backend・Method・推論API・Versionを静的Registry＋runtime probeと照合し、変更時はfail-closed。optional depsのimportはresolve時のみ。
- `EffectOutcome.to_canonical_result()`：Projectの `ScientificResultDescriptor` や旧v2 manifestへ強制転換しない。

### 7.3. 検証

`DD-E11-EFF01`：point-only・CI-null reason、`EFF02`：Science status独立、`EFF03`：wrong backend versionとfallback拒否、`EFF04`：Canonical JSON finite、`EFF05`：old Product result/CLI regression。FR-202、NFR-030/032/036、AR-034/040。

## 8. Port interface signatures（候補）

~~~python
class IdentificationPort(Protocol):
    def identify(
        self, request: ValidatedIdentificationRequest
    ) -> IdentificationOutcome: ...

class EstimatorPort(Protocol):
    def estimate(
        self, request: ValidatedEstimatorRequest,
        sink: StagingArtifactSink
    ) -> EffectOutcome: ...

class MethodCapabilityPort(Protocol):
    def resolve(
        self, method_id: str, backend_id: str, profile: str
    ) -> BackendCapabilityRecord: ...

class DiagnosticPort(Protocol):
    def run(
        self, request: ValidatedDiagnosticRequest,
        sink: StagingArtifactSink
    ) -> DiagnosticOutcome: ...
~~~

型はこのLocal lane内部のDomain DTOとProtocolであり、外部ライブラリを戻り値にしない。Port adapterは契約上認定したMethodごとに実効APIを検証する。同一 `MethodID` でも別のEstimandやInferenceを暗黙選択しない。Port実装に生成されるArtifactは必ずstaging sinkに出力し、Backendが勝手に最終dirへ書くことは禁止。

## 9. 実装時の順序と検証マッピング

1. Pure Domain Types/Codec（Graph/Estimand/AR）を実装しContract Round-tripを先にGreen。
2. Version dispatcher／ContentRef I/Oをlegacy v2回帰とセットでGreen。
3. Backend capability adapterをoptional env別にGreen。Runtime actual version/lockを記録。
4. Scientific Method adapterは41 Method Scopeの個別適格性・Oracleを満たす順で実装。未受入Methodを擬似Resultで代用しない。
5. 最後にApplication／Publisherとfault/privacy/Manifest readbackを統合する。

参照：[IF-01 Local CLI/Ports](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、[IF-01 Manifest](../23_api_interface_design/23_42_e11_local_result_manifest_artifact.md)、[Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)、[Existing Product Port](30_50_persistence_artifacts.md)。
## 10. 既存実装とのPort/Manifest静的照合（PREP-02）

固定Source観測ベースライン：af9cb0c51bb6faa55fd4e6fd170e547b5e6dd798。以下はSourceの署名と型の静的確認であり、Backend/Runtime/Science PASSではない。

| Existing Component | Blob SHA / 観測Interface | Proposed E11との差分・対応 |
| --- | --- | --- |
| src/ariadne/product/ports/scientific_core.py | ccf89d307d626e7b4c82fe3f919230bb781d7f6a；ScientificCorePortの5 run_*メソッド、Product ScientificStatusのResultDescriptor | AR集合・部分識別等のtyped科学結果を旧Resultへ無断投影しない。新Portか明示bridgeを設計 |
| src/ariadne/interfaces/cli/manifest.py | 97216eca9d777e97f7a5ebd4e248afd31c6b4de0；CliManifestのsnapshot_schema_version既定はcausal-analysis-spec/2 | E11 Local新Versionへ暗黙変換禁止。明示dispatchとroundtrip／負例 |
| src/ariadne/product/ports/artifact_store.py | e5bb990f9b69ef68df46a1559560ffb67b64caaf；store / retrieve / exists / delete | multi-file Atomic Publishを保証しない。新Local Publisherとcommit-marker、readbackが必要 |
| src/ariadne/product/domain/graph_version.py | 37ff76e001c8e269a00127e18d375f1dbc34c0e3；project-scoped GraphVersion | PAG circle endpoint、temporal lag、partial identificationを同一視しない |
| src/ariadne/interfaces/cli/scientific_stage.py | 0467a56ceb0e95bd8e4e6a99b844d5f56c7f75c3；Product analysis_spec、ScientificCorePortをimport | Product／Localのauthorityを分離。旧v2 regression保護 |

**未閉鎖:** Sourceに存在しないE11 Proposed Portの署名・Schema Version・typed statusの最終Freeze、security/atomic負例、独立Architecture Review。既存Classをこの静的一覧だけでOwnerの7区分完成と認定しない。


## PREP-02 adopted cross-Port invariants (2026-11-17)

[Owner decision](../combined_review/decisions/94_20261117_dec_prep02_owner_architecture_choices.md) is A/A/A. `LocalStudySpec`, `GraphEvidence`, `EffectOutcome`, Manifest and Status have adopted strict `e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1` discriminators. Domain DTOs must never silently read Product legacy v2. File-backed Content Ports must preserve verified same-root boundaries; Publication Port must require a Linux same-filesystem no-replace commit and fail-closed unsupported FS. Privacy-restricted outputs require the non-delegated owner-UID/Study-authorization/CLI-opt-in conjunction. **Unresolved:** formal Port signatures, DTO/JSON Schema, errors, effective FS capability inspection, independent review and verification. Option selection is not freeze.



## 11. F04：Product/Local Port・DTO 互換性境界（設計契約案）

### 11.1 既存Portからの意味変換を禁止する境界

既存Product `ScientificCorePort`は`run_discovery/run_identification/run_estimation/run_refutation/run_sensitivity`から`list[ScientificResultDescriptor]`を返す。ResultType/ScientificStatusはProduct Resourceの型であり、E11のGraphEvidence・IdentificationOutcome・EffectOutcome、及びunbounded/disconnected AR集合の損失ない表現ではない。**E11 Local DomainはProduct Portを直接継承・単純alias・無検証castしない**。既存`ArtifactStorePort.store/retrieve/exists/delete`はmulti-file immutable run publishの代替としない。旧`CliManifest(manifest_version=2.0, snapshot_schema_version=causal-analysis-spec/2)`は新E11 strict decoderへ変換しない。

### 11.2 Local Port/DTO signatures の実装候補

`ContentReferencePort.verify(ref: ContentRef, root: TrustedLocalRoot) -> VerifiedContent`：実効Trusted Rootでsecure open→同一FDからbytes/hash→参照内容を固定。`MethodCapabilityPort.resolve(method_id, backend_id, profile) -> BackendCapabilityRecord`：real API/version/profile/inference supportを記録。`IdentificationPort.identify(request: ValidatedIdentificationRequest) -> IdentificationOutcome`、`EstimatorPort.estimate(request: ValidatedEstimatorRequest, sink: StagingArtifactSink) -> EffectOutcome`、`DiagnosticPort.run(request: ValidatedDiagnosticRequest, sink: StagingArtifactSink) -> DiagnosticOutcome`はE11 Local DTOを使用し、optional library object・Product Result/Status・任意出力Pathを返さない。`LocalPublicationPort.publish(staged: ValidatedStagedBundle, root: TrustedLocalRoot) -> CommittedLocalRun`はF03 no-replace規則の責務でありScientific Portには公開を許さない。`LocalManifestReaderPort.verify(ref: LocalRunRef, root: TrustedLocalRoot) -> VerifiedLocalRun`はmarker→manifest→artifact hashとE11 explicit version dispatchを検査する。

`Validated*Request`はquestion/design/graph/dataset/estimand/method/upstream hashesを検証済みの内部型とする。外部入力から直接インスタンス化された未検証値をeligibleとして扱わない。Method別のEstimator/Inferenceの有効性は41 Methodの独立科学契約がAuthority。外部Calculation Primitiveの共有は、Method/Estimand/inferenceと負例が一致することを示したExplicit Adapterに限る。

### 11.3 F04拒否条件と検証義務

- Product `ESTIMATED`をE11 `science_acceptance=PASS`へ変換しない。DoWhy識別名からLATE/B0/B1/DRIVを推定しない。
- Identificationが未成立またはGraphVersion/Hash不整合ならEstimatorを呼ばない。ScientificNegativeOutcomeを技術障害や偽の点推定へ変換しない。
- Legacy Productの5 run signature・v2 reader・Product Result/Artifact schemaを回帰試験で保持する。Optional backendがないENV-BASEでもE11 Local Domainをimport可能にする。
- 型署名とModule配置、Error code及びABIの最終freezeは独立Architecture Review前には宣言しない。実装後のtests/科学受入PASSとは別。

設計判断候補および各検証項目：[F04 review input](../combined_review/98_20261117_prep02_f04_port_boundary_adr_candidate.md)。Owner採用済みA/A/Aの規則を変更しない。

## 12. F07：AR・Inferenceのlossless DTO規範

`ARConfidenceSet`は`confidence_level∈(0,1)`、非空のcanonical `components: tuple[ExtendedRealInterval,...]`、`topology`および検証可能な`inversion_evidence: ContentRef`で構成する。各Endpointは有限値または`NEG_INFINITY/POS_INFINITY`のタグ付きJSON型とし、裸のNaN/±Infinityやnullへの置換は禁止。負∞はlower専用、正∞はupper専用、無限端点は開区間。二つの成分が端点で接していても両者がその端点を除外する場合、そこに1点のgapが残るためDISCONNECTEDを保つ。

分類はcanonical unionで、全実数なら`ALL_REAL`、成分数が2以上なら`DISCONNECTED`、単一区間でいずれか無限端点なら`UNBOUNDED`、残り`BOUNDED`。通常の成功ARで`EMPTY`を出さず、反転失敗は`InferenceAvailability.FAILED + typed reason`として保持する。これはE11初期契約の結果表現規則であって、一般の統計的反転で空集合が数学的に不可能という主張ではない。

`InferenceEvidence.availability=AVAILABLE`では、承認された推論型と一致する`FiniteInterval`または`ARConfidenceSet`ちょうど1つを持つ。他のAvailabilityでは両方nullかつreason必須。点推定とScienceAcceptanceは独立。CONFIRMATORY結果にはMethod別に受入済み推論証拠を要求し、`NOT_EVALUATED`を`PASS`として表示しない。

Wire shape candidateと証明範囲は[F07 review input](../combined_review/99_20261117_prep02_f07_ar_inference_schema_candidate.md)及び[JSON Schema draft](../23_api_interface_design/schema_drafts/e11_ar_inference_defs.schema.json)。JSON Schemaだけでは成分順序/結合、統計的Coverage、Methodの適格性は証明されない。`F07_DESIGN_REFINED / SCHEMA_NOT_FROZEN / SCIENCE_NOT_RUN`。
