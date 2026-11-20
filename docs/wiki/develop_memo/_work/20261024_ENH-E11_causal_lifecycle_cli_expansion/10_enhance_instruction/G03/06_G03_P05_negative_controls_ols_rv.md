# ENH-E11 G03 P05 — negative_controls_ols_rv

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G03 / **Package:** P05 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G03_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G03_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 観測Z/W、事前帰無・opt-in・条件付き関連。OLS RV(q=1)は古典OLS coef/SE/df限定。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**科学/Designの必須制約:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 観測Z/W、事前帰無・opt-in・条件付き関連。OLS RV(q=1)は古典OLS coef/SE/df限定。

### 2A. 現行Source ABIと再利用の明示的な境界（`2cf28f59a324`）
- **実在:** `src/ariadne/scientific/inference/adapter.py`に`EstimationAdapter.run(self, input_: EstimationInput, output_dir: Path) -> list[ScientificResultDescriptor]`、`src/ariadne/causal/inference/estimators/treatment_effect.py`に`TreatmentEffectEstimator.diff_in_means()`/`ols()`/`ipw(estimand: str)`/`aipw(estimand: str)`/`cross_fitted_nuisance(...)`が存在する。Method-specific Target/Variance/Inference互換は自動成立しないので、パラメータ・返却と結果定義を現物で突合し、共通純粋計算Kernelを経由して再利用する。
- **実在:** `src/ariadne/scientific/refutation/adapter.py`の`RefutationAdapter.run(self, input_: RefutationInput, output_dir: Path) -> list[ScientificResultDescriptor]`、`src/ariadne/scientific/sensitivity/adapter.py`の`SensitivityAdapter.run(self, input_: SensitivityInput, output_dir: Path) -> list[ScientificResultDescriptor]`は旧Product公開ABIで変更禁止。新`DiagnosticPort.run(request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink)->DiagnosticOutcome`とは異なる。旧Path出力を新Portから直接起動/無検証castするのではなく、共有する純粋Kernelと型付きBridgeを設ける。
- **Design-only:** `ariadne.scientific.ports.causal`や`ariadne.capabilities.causal.local_execution`等のE11 Typed Port/Local Facadeは現行Source内の存在を前提にしない。G01共通契約を他Packageが複製しない。要求するConcrete BridgeのOwner/署名が未決なら新Classを想像で追加せず`BLOCKED_CONTRACT_AMBIGUITY`。

### 2B. Operation別Artifactと検証規則（外部DDを読まずに判定）
| Operation | 必須Artifact | 禁止・negative/Schema |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, graph成功時は`graph.json` | `result.json`禁止。Graph無しの正当な科学負例は`diagnostics.json`＋reason、`schema_dispatch.graph=null`。Backend技術失敗は成功としない |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | `result.json`禁止。識別否定もtyped結果にしてGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、架空の推定値禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effectの再発行禁止。元Effect/Graph/Design hash、seedと適用条件を検証 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）が必要で、いずれもArtifact inventory外。Inventoryは実在Artifactごとに相対POSIX key・SHA256・size・MediaType・Privacyを保持。`request_hash=SHA256(JCS(validated typed Study JSON))`、Markerの`manifest_sha256`はManifest実bytesのhashであり、Manifest自身には自己hashを持たせない。ReaderはMarker→Manifest→各Artifact→Operation Profile→上流HashをTrustedRoot下で独立検証。stagingから同一FS atomic no-clobber publish、未承認row Parquet禁止。旧Productのpath-based writerを型付きStagingSinkの代用として直接使用しない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `ObservedNceAdapter` | `ariadne.scientific.causal_methods.negative_controls.ObservedNceAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `ObservedNcoAdapter` | `ariadne.scientific.causal_methods.negative_controls.ObservedNcoAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `OlsRvAdapter` | `ariadne.scientific.causal_methods.sensitivity.OlsRvAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約がField/Constructor/公開Method/前後条件/失敗時の一次規範。所有するAdapterだけにMethod-specific preflight/executeを実装し、既存`RefutationAdapter`/`SensitivityAdapter`の公開`run` ABIを維持する。統合専用Packageは新Adapterを作らず、Product Scientific Kernelを共有する。

**Responsibility:** Method Adapterを担当するClassは `ObservedNceAdapter`, `ObservedNcoAdapter`, `OlsRvAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class contracts — normative here

次のField/Constructor/Method/Pre-Post/FailureはこのPxxの実装Contractを構成する。DDは由来情報に限り、実装Agentへの仕様補完委譲は禁止。実在Source/ABIは開始時に照合し、Designed Classを既存と断定しない。

### 3.1. `ObservedNceAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.negative_controls.ObservedNceAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M18`。**再利用:** 既存Design/Outcome/Inference検証を共通化してNCEを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M18` | negative control exposure | 実在Z・事前帰無・opt-in、条件付き関連/負結果 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P118`（`P1-M18`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `ObservedNcoAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.negative_controls.ObservedNcoAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M19`。**再利用:** 既存Design/Outcome/Inference検証を共通化してNCOを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M19` | negative control outcome | 実在W・事前帰無・opt-in、条件付き関連/負結果 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P119`（`P1-M19`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.3. `OlsRvAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.sensitivity.OlsRvAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M20`。**再利用:** 既存OLS推定の係数・SE・dfを再利用。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M20` | OLS partial R²、point RV(q=1) | 古典OLS係数/SE/df、非OLS拒否 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P120`（`P1-M20`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.4. `DiagnosticPort` — standalone Class/Method contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.DiagnosticPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class DiagnosticPort(Protocol):
    def run(self, request: ValidatedDiagnosticRequest, *, sink: StagingArtifactSink) -> DiagnosticOutcome: ...
```

#### 処理仕様

診断結果を型付きで正規化し、未検証Science PASSにしない。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol自体はI/Oを持たない。ConcreteはこのPxxの§3/§4で所有が指定されたAdapter/Façadeに限定し、MethodCapabilityPortでstrictに選択する。検証済Request→typed outcome＋staging sinkを守り、外部DDを未記載の実装規範として参照しない。Owner/実効ABIが未確定ならBLOCKEDで停止する。

#### 検証

DD-E11-METH-P101〜P313。

### 3.5. `InferenceEvidence` — standalone Class/Method contract

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.InferenceEvidence`。Inferenceの可用性と実際のFinite CI／AR集合を型付きで保持する。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `availability` | `InferenceAvailability` | AVAILABLE/UNAVAILABLE/FAILED/NOT_REQUESTED等 |
| `kind` | Method-specific enum | 実効推論方式 |
| `interval, confidence_set` | `FiniteInterval|None, ARConfidenceSet|None` | AVAILABLEなら正当な片方ちょうど1つ |
| `reason` | `ScientificReason|None` | nonAVAILABLEでは必須 |
| `method_config` | typed config | Backend/Method/Estimandに適合 |

#### Constructor / Factory

Constructor/Factoryはavailabilityとevidenceの排他性、およびreason整合を検査。実行済みCIをデフォルト値で捏造しない。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_for(mode,method)` | Validated inference / typed reason | pure Method/analysis-mode適格性検査 | unsupported confirmatory inference |

#### 処理仕様

EXPLORATORY point-onlyとCONFIRMATORY inference要件を分離する。FiniteIntervalとARConfidenceSetを丸め合わせず、SCM point-onlyを確証CIと報告しない。

#### I/O・連携・失敗処理

Value操作I/Oなし。Backend provenance・coverageの計算は30_63へ委譲。

#### 検証

`DD-E11-AR04/AR05`、`DD-E11-EFF01/02`、Method-specific CI availability、independent coverage。

## 4. Required execution — method-specific coding order (G03/P05)

1. **Entry/preflight:** G03/G02 upstream canonical 999、Frozen06/07/Pxx、Owner Coding Authorization、Source/lock SHA、依存Pxx checkpointを確認。Method×Operation×Design×Estimand×Inference×Backendをstrictに検証し、失敗時はtyped negativeまたはtechnical errorを返す。
2. `P1-M18` NCEと`P1-M19` NCOは実在のNegative-Control Exposure Z / Outcome W、事前の帰無仮説、調整Covariates、適用データの条件付きsupportを別々に検証。
3. 各DiagnosticはNullを棄却/非棄却した意味に限定し、p値の大きさを無交絡の証拠としない。未測定NCを偽造しない。
4. `P1-M20`は古典OLSのcoefficient, SE, dfを再現できる場合のpartial R²と指定q=1 RV。非OLS/robust-incompatible inferenceはtyped拒否。
5. **Postconditions:** NCE/NCOは条件付き帰無の診断であり、未棄却≠無交絡。RVは古典OLS q=1 only。
6. **Publication & compatibility:** Kernel結果をtyped portable Effect/Diagnosticに正規化し、G01のStagingSink/Publisherを使用。自己publish、Resultへのraw model/行データ混入、未承認row export、旧v2 API変更、silent Backend fallbackは禁止。
7. **Error boundaries:** illegitimate negative/unsupported CI, invalid config, numerical nonconvergence, missing dependency, FS/Policy denialを別Status/Reasonとし、Technical SUCCESSからScience PASSを推論しない。

### 設計書で定義済みの科学・型契約（このPxxに展開済みの規範）

以下は30_63の確定記述のうち本Packageに該当する部分を**本文へ複製した実装規則**であり、DDへの外部参照によって補完する規則ではない。担当外Methodの記述がある場合は担当Classを追加実装しない。

- NCE/NCOは観測実在のZ/W、事前指定負の対照関係・条件付き帰無、同じDesign covariatesとデータ適格性を要求し、p値が大きいことを無交絡証明と報告しない。
- OLS RVは古典OLSのcoefficient/SE/dfを再現し、指定の `q=1` partial R² / robustness valueのみ対象。他Estimatorへ自動拡張しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M18` | negative control exposure | 実在Z・事前帰無・opt-in、条件付き関連/負結果 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M20` | OLS partial R²、point RV(q=1) | 古典OLS係数/SE/df、非OLS拒否 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**未実測のBackend/Independent Reference/Method固有Schema/定量閾値は上記契約が未定義であることとは異なる。** 採用済みTarget/数理規則をAgent裁量で変更せず、未実測はScience/Freezeの該当判定でBLOCKEDとする。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M18` Observed NCE null diagnostic／条件付き関 | `DD-E11-METH-P118` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M19` Observed NCO null diagnostic／条件付き関 | `DD-E11-METH-P119` | DGP-019; NEG-019, NEG-026 | REF-R02 | AC-D01, AC-T01, AC-T02, AC-T03, AC-R03 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |
| `P1-M20` OLS partial R² / RV sensitivity／指定 | `DD-E11-METH-P120` | DGP-020; NEG-020 | REF-R03 | AC-D01, AC-D03, AC-R04 | PLAN:G03 / OWNER_METHOD_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** 本Pxx§5のDGP/NEG/REF/ACは全件独立科学検証義務である。IDの列挙は実Fixture/独立Reference生成済みやPASSを意味しない。Backend自己出力を真値としない。FWER=.05・K/R/Compute/MC-SE/CI coverageと閾値はFreeze前に決定し、未確定はBLOCKED。別文書を読んで値を推測・補完しない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g03/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Method-specific acceptance and observation

- §5の各Methodに対しDGP/NEG/独立REF/DD IDをすべて実行義務として追跡する。登録IDがあることはTest fixtureが実在・PASSしたことを意味しない。
- **Required test semantics:** `P1-M18` NCEと`P1-M19` NCOは実在のNegative-Control Exposure Z / Outcome W、事前の帰無仮説、調整Covariates、適用データの条件付きsupportを別々に検証。 各DiagnosticはNullを棄却/非棄却した意味に限定し、p値の大きさを無交絡の証拠としない。未測定NCを偽造しない。 `P1-M20`は古典OLSのcoefficient, SE, dfを再現できる場合のpartial R²と指定q=1 RV。非OLS/robust-incompatible inferenceはtyped拒否。
- Schema+Method validation（unit）、Class.Port/Result provenance（contract）、実有効Backend/CLI/Publisher/旧v2（integration）を区別。Independent scientific DGP/Oracleは適格な真値から導出し、Estimator自己出力をReferenceにしない。
- Evidenceにsource/lock/fixture SHA、Method/Estimand/Inference、positive+negativeのexpected/observed、実効Backend/API/config/seed、collect済path/command/Resultを残す。Filesystem/科学証拠が未取得ならBLOCKED、期待値緩和によるPASSは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P06。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Self-contained freeze review boundary

- 本文§3で必要なClassのConstructor・Field・公開Method・処理責務、§4で実装順序/分岐、§5〜6でMethod別のScience/Testを保持する。外部DDやGate06を読ませて不足仕様を推測させない。
- **未確定事項:** Negative Controlの事前null/covariates・RV q=1適格性と独立科学。 未解決のBackend API、Method Config、DGP/NEG/Reference/quantitative Science、Owner Decisionは該当MethodをBLOCKEDとし、Freeze前に閉じる。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G03/P05 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P1-M18–M20. Scientific constraints: OLS/IPW/AIPW contrast/variance/overlap/cross-fitting、Refutation・NCE/NCO・RV q=1. Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.


## PREP-04.1 owner Method contracts (DRAFT / NOT_FROZEN)

### P1-M18 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED negative_control_exposure, explicit_opt_in, null_diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, negative_control_exposure, null_assumption_ref, adjustment_columns plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-019; NEG-019, NEG-026; REF-R02; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M19 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED negative_control_outcome, explicit_opt_in, null_diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, negative_control_outcome, null_assumption_ref, adjustment_columns plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-019; NEG-019, NEG-026; REF-R02; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M20 — strict Method contract (PREP-04.1 DRAFT)
- Operation: DIAGNOSE; target: 10_32 semantic target (not assigned canonical enum); owner: P05. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED q, ols_model_spec_ref, target_coefficient_ref, variance_kind; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED outcome, treatment, ols_fit_evidence_ref, degrees_of_freedom plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-020; NEG-020; REF-R03; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.
