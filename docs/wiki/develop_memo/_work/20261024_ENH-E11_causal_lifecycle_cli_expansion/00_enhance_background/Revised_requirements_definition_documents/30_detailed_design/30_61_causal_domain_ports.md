# 30_61_causal_domain_ports

---

## 1. Graph Evidence

### 1.1. `GraphEvidence`

#### 1.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.discovery.graph_evidence.GraphEvidence`。PAG/CPDAG/DAG/temporal等の科学的Graph Evidenceを保持するimmutable Value。Product `GraphVersion`のVersion作成・編集・FIX権限を持たない。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 1.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `kind` | `GraphKind` | DAG/CPDAG/PAG等の区別 |
| `nodes` | `tuple[Node,...]` | unique identity |
| `edges` | `tuple[EndpointEdge,...]` | endpoint/lag/identityをlossless |
| `temporal` | `TemporalConvention|None` | lagの符号・基準時刻 |
| `source_graph_version_id` | `str|None` | 存在する場合にProduct GraphVersionを参照。自身はVersionを発行しない |
| `provenance, content_hash` | `GraphProvenance, str` | Graph意味射影に一致するdigest |

#### 1.1.3. Constructor / Factory

`from_canonical_json(raw:bytes)->GraphEvidence`：strict Graph Schema＋意味Validator。不可逆PAG→DAG変換、未知node/endpoint/重複edge/lag規約欠落を拒否。

#### 1.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_canonical_json(raw:bytes)` | `GraphEvidence` | pure strict graph decode | schema、endpoint、lag、hash不整合 |
| `canonical_payload()` | `Mapping[str,JsonValue]` | lossless domain serialization | invalid/incomplete Graph |

#### 1.1.5. 処理仕様

`EndpointEdge(source,target,source_mark,target_mark,lag)`のmarkはTAIL/ARROW/CIRCLE。Node順序を反転する場合はendpointも対応させる。PAGのbidirected/circleをDAGへ暗黙確定しない。FIXEDは編集状態であってScientific Truthではない。未確定GraphからのEffect識別は独立のEstimand別識別証拠を要求。

#### 1.1.6. I/O・連携・失敗処理

Graph Valueの純粋操作はI/Oなし。内部`content_hash=SHA256(JCS(Graphからcontent_hash自身を除く意味射影))`、外部`ContentRef.sha256=SHA256(完成Graph File実bytes)`を**別々に検証**。RevisionとFIXはProductの既存GraphVersionServiceが所有する。

#### 1.1.7. 検証

`DD-E11-GRAPH01` FCI PAG circle/arrow/bidirected、`GRAPH02` PCMCI lag、`GRAPH03` silent PAG→DAG拒否、`GRAPH04` Product GraphVersion整合と再識別。FR-186/196、AR-028/036/043。

## 2. Identification / Estimation

### 2.1. `IdentificationOutcome`

#### 2.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.identification.contracts.IdentificationOutcome`。識別状態・対象Estimand・Proof・lineageを保持するValue。DoWhy内部ラベルをDomainの推定対象と混同しない。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 2.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `identification_id` | immutable identity |
| `estimand` | `EstimandRef`。B0/B1/DRIV等の区別 |
| `status` | `IdentificationStatus`。nonidentified/review/partialを型付け |
| `strategy, proof` | Strategy、`IdentificationProof|None` |
| `upstream, reasons` | `UpstreamHashSet, tuple[ScientificReason,...]` |

#### 2.1.3. Constructor / Factory

`from_evidence(evidence:ValidatedIdentificationEvidence)->IdentificationOutcome`。BackendのStatus、assumption、GraphVersion、Estimand、Upstreamを意味検証して正規化。未提供Proofを生成しない。

#### 2.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_evidence(evidence:ValidatedIdentificationEvidence)` | `IdentificationOutcome` | pure status/proof normalization | proof/estimand/upstream不整合 |

#### 2.1.5. 処理仕様

`NOT_IDENTIFIED / REQUIRES_REVIEW / PARTIALLY_IDENTIFIED`を点推定許可へ自動昇格しない。緩和可能な列挙WARNだけに理由付きoverrideを許可。

#### 2.1.6. I/O・連携・失敗処理

外部I/Oなし。実際のBackend識別計算は`IdentificationPort`、Proof/File readbackは別Port。Retry/RollbackはN/A。

#### 2.1.7. 検証

`DD-E11-ID01` B0/B1/DRIV mislabel、`ID02` lineage差、`ID03` nonidentified override拒否、`ID04` GraphVersion再識別。FR-187/194/199、AR-029/039/043。

### 2.2. `EstimatorRequest`

#### 2.2.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EstimatorRequest`。Identification proofが適格な場合だけEstimatorへ渡すRequest Value。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 2.2.2. フィールド

| Field | Type・制約 |
|---|---|
| `method_id, estimand_family` | Method×target一致 |
| `identification_ref` | 上流証拠参照 |
| `question/design/graph/dataset_hashes` | 完全な上流digest集合 |
| `method_config, inference_request` | Method/Inference適格なtyped config |

#### 2.2.3. Constructor / Factory

`validate_against(identification,design,policy)->ValidatedEstimatorRequest`は入力と上流証拠を照合する型付きvalidator。Validation前の生RequestをAdapterへ送らない。

#### 2.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_against(self, identification:IdentificationOutcome, design:CausalDesign, policy:EstimandEligibilityPolicy)` | `ValidatedEstimatorRequest` | pure eligibility check | scientific negative / schema validation区別 |

#### 2.2.5. 処理仕様

Method-specific assumptions、Mediator/Instrument/support、Data Eligibility、Graph/Design/Question/Dataset hash全一致、CI要求を検証。不適格は`ScientificNegativeOutcome`としてBackend未呼出。Path/schema mismatchはtechnical validationとする。

#### 2.2.6. I/O・連携・失敗処理

Value自身はI/Oなし。ScientificValidationServiceの既存適格性規則を共通pure policyとして再利用する。実Estimator I/O/Artifactは`EstimatorPort.estimate(...,sink)`を通す。

#### 2.2.7. 検証

`DD-E11-ID01〜04`およびMethod固有Negative Tests。

## 3. Inference Values

### 3.1. `ARConfidenceSet`

#### 3.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.confidence_sets.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 3.1.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### 3.1.3. Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### 3.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 3.1.5. 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### 3.1.6. I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 3.1.7. 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。

### 3.2. `InferenceEvidence`

#### 3.2.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 3.2.2. フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### 3.2.3. Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### 3.2.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 3.2.5. 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### 3.2.6. I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 3.2.7. 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

## 4. Effect Outcome

### 4.1. `EffectOutcome`

#### 4.1.1. 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。**実装状態：PROPOSED（Source未実装）。配置先を定義する設計契約。**

#### 4.1.2. フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### 4.1.3. Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### 4.1.4. メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | incompatible schema/estimand |

#### 4.1.5. 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### 4.1.6. I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 4.1.7. 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

## 5. Scientific Ports

### 5.1. `IdentificationPort`

#### 5.1.1. 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.IdentificationPort（PROPOSED）。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### 5.1.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 5.1.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 5.1.4. メソッド

```python
class IdentificationPort(Protocol):
    def identify(self, request: ValidatedIdentificationRequest) -> IdentificationOutcome: ...
```

#### 5.1.5. 処理仕様

IdentificationとEvidenceの意味を守り、非識別をIDENTIFIEDと偽装しない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 5.1.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 5.1.7. 検証

DD-E11-ID01〜04。実装未完・runtime/science verification未実施。

### 5.2. `EstimatorPort`

#### 5.2.1. 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.EstimatorPort（PROPOSED）。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### 5.2.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 5.2.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 5.2.4. メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 5.2.5. 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 5.2.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 5.2.7. 検証

DD-E11-EFF01〜05。実装未完・runtime/science verification未実施。

### 5.3. `MethodCapabilityPort`

#### 5.3.1. 識別情報・責務

**Protocol配置：ariadne.scientific.ports.capability.MethodCapabilityPort（PROPOSED）。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### 5.3.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 5.3.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 5.3.4. メソッド

```python
class MethodCapabilityPort(Protocol):
    def resolve(self, request: ValidatedCapabilityRequest) -> BackendCapabilityRecord: ...
```

#### 5.3.5. 処理仕様

Method/Estimand/Backend/Inferenceを検証し、silent fallbackをしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 5.3.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 5.3.7. 検証

DD-E11-CAP01〜06。実装未完・runtime/science verification未実施。

### 5.4. `DiagnosticPort`

#### 5.4.1. 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.DiagnosticPort（PROPOSED）。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### 5.4.2. フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### 5.4.3. Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### 5.4.4. メソッド

```python
class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...
```

#### 5.4.5. 処理仕様

診断結果を型付きで正規化し、未検証Science PASSにしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### 5.4.6. I/O・連携・失敗処理

Protocol本体はI/Oなし。具体Adapterは[30_63](30_63_e11_method_adapters.md)、Runtime/Publicationは[30_62](30_62_e11_local_execution_publication.md)参照。

#### 5.4.7. 検証

DD-E11-METH-P101〜P313。実装未完・runtime/science verification未実施。

## 6. 既存Class再利用と単一Authority

Product `GraphVersionService`はGraph Versionの唯一のWriter。`GraphEvidence`は科学的GraphのpureなValueであり、`make_revision`は定義しない。Product `ScientificCorePort`の旧v2公開署名は維持し、型付きScientific Portsと旧Adapterの共通科学実装への互換Bridgeを設ける。CLI入口だけを理由に新たな科学Domainを作らない。

| 科学Class/Port | 確定したModule | 既存再利用・禁止する重複 |
|---|---|---|
| `GraphEvidence` | `ariadne.causal.discovery.graph_evidence.GraphEvidence` | 既存graph_semanticsのPAG validator再利用。GraphVersion writerを複製しない |
| `IdentificationOutcome` | `ariadne.causal.identification.contracts.IdentificationOutcome` | 既存IdentificationAdapterの結果を型付き変換。Product Resultと同一化しない |
| `EstimatorRequest` | `ariadne.causal.inference.contracts.EstimatorRequest` | ScientificValidationServiceのrulesを共通policyとして共有 |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets.ARConfidenceSet` | 有限CIに還元できないAR集合は専用Value |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | 既存Finite CIから拡張しAvailability/Reasonを分離 |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | TreatmentEffectResult/ScientificResultDescriptorとのversioned変換 |
| `IdentificationPort` | `ariadne.scientific.ports.causal.IdentificationPort` | ScientificCorePort.run_identification互換Bridge |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | ScientificCorePort.run_estimation互換Bridge |
| `MethodCapabilityPort` | `ariadne.scientific.ports.capability.MethodCapabilityPort` | Method Registry唯一のauthority。StageRunnerRegistryはStage登録専用 |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | 既存Refutation/Sensitivity/DesignDiagnosticsを再利用 |

`ContentRef`および`LocalStudySpec`は[30_60](30_60_cli_adapters.md) §11/12、`BackendCapabilityRecord`は[30_62](30_62_e11_local_execution_publication.md) §8のClass仕様をOwnerとする。共通JCS Encoderは`ariadne.shared.serialization.jcs`へ新設し、既存Product `canonical_bytes`/`hash_mapping(default=str)`をRFC8785と同一視しない。
