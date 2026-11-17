# 30_61_e11_local_domain_ports — E11 Local Domain / Scientific Port 物理詳細設計

## 1. モジュール構成・依存方向

Local causal laneのDomain/Port配置と依存関係を定義する。既存ProductのDomain/PortとLocalのauthorityを分離し、共通化は意味と検証義務が一致する純粋値に限る。

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

## 2. ContentRef

### 2.1. 識別とフィールド

配置 `causal.local_contract.references.ContentRef`。immutable dataclass：`identity: str`、`relative_key: str`、`sha256: str`、`media_type: str`、`schema_version: str|None`。Data bytesとmetadataの識別子を混同しない。外部入力の絶対pathやaccess tokenを正本値に保持しない。

### 2.2. Constructorと処理

`ContentRef.from_payload(payload: Mapping[str, JsonValue]) -> ContentRef`：
- strict keys、sha256小文字hex64、非空identity、relative keyを確認。
- dotdot、absolute、drive letter、NUL、backslash区切りの混合、不正Unicode正規化、symlink targetの危険な参照を拒否。
- pathの安全性検証は**静的文法のみ**であり、その後の実file openを代替しない。

`ContentReferencePort.verify(ref: ContentRef, trusted_root: TrustedLocalRoot) -> VerifiedContent`：
- I/O adapterによりroot閉じ込めOpen、同一file descriptorからhashを計算し実際の内容を返す。
- hash mismatch、path race、size policy、read failureをTyped exception。
- 参照解決に基づく科学内容検証は別Domain validatorへ渡す。

### 2.3. 検証

`DD-E11-REF01`：相対／hash valid。`REF02`：traversal/symlink/race。`REF03`：入力差替え/TOCTOU。`REF04`：metadata-only同一IDの別bytes禁止。FR-185、NFR-029、NFR-031に対応。

## 3. LocalStudySpec / LocalConfigDecoder

### 3.1. Class/fields

配置 `causal.local_contract.study.LocalStudySpec`。immutable：
- `schema_version: Literal["e11-local-study/1"]`
- `run_id: str`、`operation: LocalOperation`、`analysis_mode: AnalysisMode`
- `question: ContentRef`、`design: ContentRef`、`graph: ContentRef|None`、`dataset: ContentRef`、`identification: ContentRef|None`
- `estimand: EstimandRef`、`method: MethodRequest`、`inference: InferenceRequest`
- `randomness: RandomnessSpec`、`privacy: LocalPrivacySpec`

### 3.2. Factory・method

`LocalConfigDecoder.decode_yaml(raw: bytes) -> LocalStudySpec`：
- `LocalConfigDecoder.decode(raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy`が共通Portとの接点。`decode_yaml`は内部helperであり別公開契約を作らない。YAML/JSON重複key・alias/excessive nesting・Python Tag等を拒否し、strict Schema/Method Profile検証後だけValidatedStudy factoryを呼ぶ。
- `schema_version`を先に判定。unknown/legacyはE11 parserに流さない。
- `LocalStudySpec.validate_local_invariants() -> tuple[Reason,...]`：required refs by Operation、Method/Estimand target、analysis_mode/inference、row export request、Run IDなどの純粋不変条件を収集。
- Result/Manifest bytesを生成せず、副作用は無し。config hashはcanonical encoding後のbytesのdigestから求め、canonicalization versionを記録する。

### 3.3. 検証

`DD-E11-SPEC01`：valid schema／strict unknown field、`SPEC02`：旧v2 dispatch、`SPEC03`：confirmation requires inference、`SPEC04`：Method/estimand mismatch。FR-185、FR-201、NFR-029/036、AR-034。

### 3.4. Operation別Target・Method固有の入力制約

Study wireの`estimand`フィールドは必須だが、`DISCOVER`の`{family: GRAPH_STRUCTURE, population: OBSERVED_VARIABLES, contrast: NOT_APPLICABLE}`は効果Estimandではなく**非効果の探索Target**を表すタグ付き値である。Effect Estimatorに渡さず、ダミーATE/ATTも生成しない。DISCOVERでは未作成のInput Graph/Identificationを要求しない。ESTIMATE等では実際の効果Estimandと識別証拠を要求する。Operation×Method×Targetに応じてvalidatorを分ける。

P1-M06の[Question Profile](../23_api_interface_design/schema_drafts/e11_g01_question_evidence_profile.schema.json)、[Design Profile](../23_api_interface_design/schema_drafts/e11_g01_design_evidence_profile.schema.json)は**FCIに対するMethod固有の内部検証**であって全Discovery Method共通の機能制限ではない。Question/Design/Studyのidentity、Design variablesとDataset列名・順序、Design/Method BackgroundKnowledge、CI familyとmeasurement scaleを照合する。Markov/faithfulness等のassumptionsは研究者の宣言であり、成立の証明ではない。

## 4. GraphEvidence / GraphVersion

### 4.1. フィールド

`GraphEvidence(kind: GraphKind, nodes: tuple[Node,...], edges: tuple[EndpointEdge,...], temporal: TemporalConvention|None, version_id: str, parent_version_id: str|None, provenance: GraphProvenance, content_hash: str)`。
`EndpointEdge`は `source, target, source_mark, target_mark, lag`。端点markはTAIL/ARROW/CIRCLE、lagは符号・基準時刻のConventionと組で扱う。

### 4.2. Factory・メソッド

- `GraphEvidence.from_canonical_json(raw: bytes) -> GraphEvidence`：Graph Schema厳格照合、endpoint/temporal domain検証。隠れた潜在交絡情報の喪失を拒否。
- `GraphEvidence.make_revision(edit: GraphEdit, rationale: str, assumptions: tuple[str,...]) -> GraphEvidence`：元を不変に保ち、新version ID／parent／edit rationaleを必須。DAGへの変換は新仮定の科学レビューが必要。
- `GraphEvidence.canonical_payload() -> Mapping[str, JsonValue]`：Node/Edge/lag/endpointとprovenanceのlossless round-trip。Graphの「FIXED」は編集状態でありScientific Truthとは別。
- 未確定Graphから点推定へ進むには、対象Estimandに対する独立した識別証明を必要とする。DAGへの形式変換はその証明を代替しない。

### 4.3. 検証

`DD-E11-GRAPH01`：FCI PAGのcircle/arrow/bidirected round-trip、`GRAPH02`：PCMCI系lag/contemporaneous、`GRAPH03`：PAG→DAG silent変換拒否、`GRAPH04`：版の不変性/再識別。FR-186/196、AR-028/036/043。

### 4.4. PAG endpoint・GraphVersion・二種類のDigest

PAGのTAIL/ARROW/CIRCLE、双方向矢印、Node identity、lagとTemporalConventionはlosslessに保存する。node順を反転するときendpoint markも対応して入れ替える。未定義node/不正mark/重複unordered edgeとsilent PAG→DAG変換を拒否する。`make_revision`は旧Graphを変更せず、新しいversion ID、parent version、rationale、assumptionsを保持する。

内部`GraphEvidence.content_hash = SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256 = SHA256(完成Graph Fileの実bytes)`。両者を別々に検証し、一方だけで信用しない。

## 5. IdentificationOutcome / EstimatorRequest

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

## 6. ARConfidenceSet / InferenceEvidence

### 6.1. フィールド

`ARConfidenceSet`：`confidence_level: float`、`components: tuple[ExtendedRealInterval,...]`、`topology: SetTopology`、`inversion_evidence: ContentRef`。`ExtendedRealInterval`は下上端 `FINITE(value) / NEG_INFINITY / POS_INFINITY` + closed flags。
`InferenceEvidence`：`availability: InferenceAvailability`、`kind`、`interval: FiniteInterval|None`、`confidence_set: ARConfidenceSet|None`、`reason: ScientificReason|None`、`method_config`。

### 6.2. メソッド・不変条件

- `ARConfidenceSet.from_components(level, components, evidence) -> ARConfidenceSet`：有限性、順序、重複と接触するintervalの正規化、topology分類（ALL_REAL > DISCONNECTED > UNBOUNDED > BOUNDED）を行う。
- `ARConfidenceSet.contains(beta: float) -> bool`：endpoint open/closedと∞を尊重。ALL_REALは任意有限betaを含む。
- `ARConfidenceSet.to_payload() / from_payload()`はJSON Infinity/NaNを使わず同じ数学集合に往復。
- 汎用AR Setは`EMPTY`（成分0）もlosslessに表現する。B0/B1でjust-identifiedかつ採用Methodの前提により非空集合が数学的に保証される場合のみ、**Method-specific validator**でEMPTYを科学的不整合として検出する。未確認の識別条件へ一律に非空を仮定しない。反転失敗は `FAILED + typed reason`、数学的EMPTYは `AVAILABLE + inversion_evidence`で区別する。
- `InferenceEvidence.validate_for(mode, method)`：EXPLORATORYのpoint-onlyとCONFIRMATORYの有効推論要件を区別。SCM初期point-onlyを確証的CIありと報告しない。

### 6.3. 検証

`DD-E11-AR01`：EMPTY、ALL_REAL、two-ray DISCONNECTED、片側非有界、有限BOUNDED、`AR02`：generic EMPTYの成功出力とMethod別just-identified EMPTY拒否を分離、`AR03`：round-trip、`AR04`：CI unavailable reason、`AR05`：CONFIRMATORY fail-closed。FR-202、AR-040、NFR-036。

### 6.4. Lossless AR集合・Method別非退化条件

ARConfidenceSetは`confidence_level∈(0,1)`を要し、`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`の5 topologyを持つ。`EMPTY`はcomponentsが0、ALL_REALは(-∞,+∞)の一成分。EndpointのNEG_INFINITYは下端、POS_INFINITYは上端のみで無限端点はopen。接触する2成分が共に端点を除けば1点のgapが残るため結合しない。成功した数学的EMPTYは`AVAILABLE + inversion_evidence`、反転失敗は`FAILED + typed reason`として別の状態にする。

B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件を満たすと`T_AR(βhat)=0`なので非空となる。Method固有validatorはこの条件下のEMPTYを科学的不整合として拒否し、first-stage/rank/分散退化や数値失敗はそれぞれ別typed reasonを返す。`InferenceEvidence.availability=AVAILABLE`では承認されたFiniteInterval又はARConfidenceSetちょうど1つ、それ以外は両方nullかつ理由必須。JSON数値としてNaN/Infinityを使用しない。

## 7. EffectOutcome / BackendCapabilityRecord

### 7.1. フィールド

`EffectOutcome`：`result_id`、`estimand`、`point_availability`、`point_value: float|None`、`inference: InferenceEvidence`、`science_acceptance`、`diagnostics: tuple[DiagnosticRef,...]`、`method_evidence`、`upstream_hashes`。
`BackendCapabilityRecord`：`method_id, backend_id, distribution_version, adapter_version, api_signature_hash, extra, profile, available, reason`。

### 7.2. メソッド

- `EffectOutcome.validate_consistency()`：nonfinite point拒否、null reason必須、point≠Science acceptance、CI/AR型とEstimand不一致を拒否。
- `BackendCapabilityRecord.check(request)`：実効Backend・Method・推論API・Versionを静的Registry＋runtime probeと照合し、変更時はfail-closed。optional depsのimportはresolve時のみ。
- `EffectOutcome.to_canonical_result()`：Projectの `ScientificResultDescriptor` や旧v2 manifestへ強制転換しない。

### 7.3. 検証

`DD-E11-EFF01`：point-only・CI-null reason、`EFF02`：Science status独立、`EFF03`：wrong backend versionとfallback拒否、`EFF04`：Canonical JSON finite、`EFF05`：old Product result/CLI regression。FR-202、NFR-030/032/036、AR-034/040。

### 7.4. Canonical Codecと科学的状態

`request_hash=SHA256(JCS(validated typed Study JSON))`、Graph semantic hashは自己fieldを除く意味射影、ContentRef/File/Marker参照は実bytesのSHA256で計算する。strict Codec `e11-json-jcs-rfc8785/1`を用い、Productの`hash_mapping(default=str)`へのfallback禁止。Identification/Point/Inference/ScienceAcceptance/technical statusは独立軸で、Product `ScientificStatus`／旧v2 Resultへの無検証castを禁止する。

## 8. Port interface signatures

~~~python
class IdentificationPort(Protocol):
    def identify(
        self, request: ValidatedIdentificationRequest
    ) -> IdentificationOutcome: ...

class EstimatorPort(Protocol):
    def estimate(
        self, request: ValidatedEstimatorRequest,
        *, sink: StagingArtifactSink
    ) -> EffectOutcome: ...

class MethodCapabilityPort(Protocol):
    def resolve(
        self, request: ValidatedCapabilityRequest
    ) -> BackendCapabilityRecord: ...

class DiagnosticPort(Protocol):
    def run(
        self, request: ValidatedDiagnosticRequest,
        *, sink: StagingArtifactSink
    ) -> DiagnosticOutcome: ...
~~~

以下の4つの科学PortはLocalの論理Port群の部分集合であり、ContentRef/Privacy/Publisher/Readerと合わせて境界を構成する。型はこのLocal lane内部のDomain DTOとProtocolであり、外部ライブラリを戻り値にしない。Port adapterは契約上認定したMethodごとに実効APIを検証する。同一 `MethodID` でも別のEstimandやInferenceを暗黙選択しない。Port実装に生成されるArtifactは必ずstaging sinkに出力し、Backendが勝手に最終dirへ書くことは禁止。

### 8.1. 共通論理Port署名とFacade境界

```python
class LocalConfigDecoder(Protocol):
    def decode(self, raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy: ...
class ContentReferencePort(Protocol):
    def verify(self, ref: ContentRef, *, root: TrustedLocalRoot) -> VerifiedContent: ...
class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...
class LocalPolicyVerifierPort(Protocol):
    def verify(self, *, policy_ref: ContentRef, study: ValidatedStudy,
               root: TrustedLocalRoot, anchor: PolicyTrustAnchor) -> VerifiedStudyPolicyEvidence: ...
class LocalPrivacyPolicyPort(Protocol):
    def authorize(self, *, study: ValidatedStudy, cli_row_flag: bool,
                  root: TrustedLocalRoot, policy: VerifiedStudyPolicyEvidence | None,
                  output_shape: PlannedOutputShape) -> PrivacyDecision: ...
class LocalPublicationPort(Protocol):
    def begin(self, *, run_id: RunId, request_hash: Sha256Digest,
              root: TrustedLocalRoot) -> StagingArtifactSink: ...
    def seal(self, *, sink: StagingArtifactSink, manifest: LocalRunManifest,
             privacy: PrivacyDecision) -> ValidatedStagedBundle: ...
    def publish(self, *, bundle: ValidatedStagedBundle,
                root: TrustedLocalRoot) -> CommittedLocalRun: ...
class LocalManifestReaderPort(Protocol):
    def verify(self, *, root: TrustedLocalRoot, run_id: RunId) -> VerifiedLocalRun: ...
```

`TrustedLocalRoot`はOS principal/owner/ACL/mount/dirfdを検証したCapabilityであり生Pathではない。型注釈だけでValidated Requestを信頼せず生成時・Adapter直前に再検証する。Publication Facadeとrun-scoped Publisher、Reader Facadeの`verify`とConcreteの`read_run`は同一アルゴリズムの異なる責務である。
