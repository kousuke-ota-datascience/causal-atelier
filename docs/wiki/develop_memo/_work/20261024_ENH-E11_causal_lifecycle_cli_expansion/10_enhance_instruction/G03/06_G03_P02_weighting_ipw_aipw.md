# ENH-E11 G03 P02 — weighting_ipw_aipw

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G03 / **Package:** P02 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G03_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G03_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 既存IPW/AIPWを共有しATE/ATT weight、ESS、balance、overlap、nuisance/seedを明示。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**科学/Designの必須制約:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 既存IPW/AIPWを共有しATE/ATT weight、ESS、balance、overlap、nuisance/seedを明示。

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
| `WeightingEffectAdapter` | `ariadne.scientific.causal_methods.estimation.WeightingEffectAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `EstimatorPort` | `ariadne.scientific.ports.causal.EstimatorPort` | Port/Value/Facade integration (no duplicate implementation) | estimate(self, request:ValidatedEstimatorRequest, *, sink:StagingArtifactSink) -> EffectOutcome |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約がField/Constructor/公開Method/前後条件/失敗時の一次規範。所有するAdapterだけにMethod-specific preflight/executeを実装し、既存`RefutationAdapter`/`SensitivityAdapter`の公開`run` ABIを維持する。統合専用Packageは新Adapterを作らず、Product Scientific Kernelを共有する。

**Responsibility:** Method Adapterを担当するClassは `WeightingEffectAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class contracts — normative here

次のField/Constructor/Method/Pre-Post/FailureはこのPxxの実装Contractを構成する。DDは由来情報に限り、実装Agentへの仕様補完委譲は禁止。実在Source/ABIは開始時に照合し、Designed Classを既存と断定しない。

### 3.1. `WeightingEffectAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.estimation.WeightingEffectAdapter`。 EstimationのMethod実行Adapter。担当Method：`P1-M10, P1-M11`。**再利用:** 既存IPW/AIPWとpropensity・balance診断。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P1-M10` | IPW ATE/ATT | propensity/overlap/balance/ESS/weights/CI |
| `P1-M11` | AIPW ATE/ATT | nuisance/DR claimの条件、crossfit/variance |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P110`（`P1-M10`）、`DD-E11-METH-P111`（`P1-M11`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `EstimatorPort` — standalone Class/Method contract

#### 識別情報・責務

**Protocol配置：ariadne.scientific.ports.causal.EstimatorPort。** 既存Product `ScientificCorePort`のv2メソッドを保持し、旧APIと型付きPortは共通科学計算を用いる互換Bridgeで接続する。

#### フィールド

N/A：Protocol自身はinstance fieldを所有しない。

#### Constructor / Factory

N/A：Protocolに具体Factoryはない。Concreteの依存関係注入はAdapterの責務。

#### メソッド

```python
class EstimatorPort(Protocol):
    def estimate(self, request: ValidatedEstimatorRequest, *, sink: StagingArtifactSink) -> EffectOutcome: ...
```

#### 処理仕様

識別・Method適格なRequestのみ実行し、ArtifactをStagingSinkへ限定。科学的PreconditionはWeb/CLI共通であり、CLI optionやHTTP状態ではない。

#### I/O・連携・失敗処理

Protocol自体はI/Oを持たない。ConcreteはこのPxxの§3/§4で所有が指定されたAdapter/Façadeに限定し、MethodCapabilityPortでstrictに選択する。検証済Request→typed outcome＋staging sinkを守り、外部DDを未記載の実装規範として参照しない。Owner/実効ABIが未確定ならBLOCKEDで停止する。

#### 検証

DD-E11-EFF01〜05。

### 3.3. `InferenceEvidence` — standalone Class/Method contract

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

## 4. Required execution — method-specific coding order (G03/P02)

1. **Entry/preflight:** G03/G02 upstream canonical 999、Frozen06/07/Pxx、Owner Coding Authorization、Source/lock SHA、依存Pxx checkpointを確認。Method×Operation×Design×Estimand×Inference×Backendをstrictに検証し、失敗時はtyped negativeまたはtechnical errorを返す。
2. `P1-M10` IPWはe(X)の適格性、0/1のsupport、overlap、重みと正規化、ATE/ATT別weight式、ESS、balanceを別項目として計算。
3. `P1-M11` AIPWはpropensityとoutcome nuisance m0/m1、crossfit fold/seed、Augmented Score、Target populationとCI推論方式を固定。double robustnessの有限標本保証を偽称しない。
4. Clipping/Trimmingによるestimand/target population変化を記録し、無言の閾値採用・古いATEラベル維持を禁止。inference unavailableはpoint-only/typed reasonで出力。
5. **Postconditions:** ATE IPWの例はA/e(X)+(1−A)/(1−e(X))。ATTは対象母集団/正規化別設計。AIPWはm_a(X)とe(X)を分け、Crossfit/Seed/推論を証跡化。
6. **Publication & compatibility:** Kernel結果をtyped portable Effect/Diagnosticに正規化し、G01のStagingSink/Publisherを使用。自己publish、Resultへのraw model/行データ混入、未承認row export、旧v2 API変更、silent Backend fallbackは禁止。
7. **Error boundaries:** illegitimate negative/unsupported CI, invalid config, numerical nonconvergence, missing dependency, FS/Policy denialを別Status/Reasonとし、Technical SUCCESSからScience PASSを推論しない。

### 設計書で定義済みの科学・型契約（このPxxに展開済みの規範）

以下は30_63の確定記述のうち本Packageに該当する部分を**本文へ複製した実装規則**であり、DDへの外部参照によって補完する規則ではない。担当外Methodの記述がある場合は担当Classを追加実装しない。

- IPW：propensity `e(X)`、ATEの重み例 `A/e(X)+(1-A)/(1-e(X))`、ATTには別の標本対象・weight normalization。clip/trimでtargetが変化し得ることをResultへ記録。balance/ESSとoverlap必須。
- AIPW：outcome nuisance `m_a(X)` とpropensityのAugmented scoreを別統計量として実装。double robustnessは必要な推定仮定／十分な推定品質の代わりでない。nuisance/fold/seedと推論方針を記録。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M10` | IPW ATE/ATT | propensity/overlap/balance/ESS/weights/CI |
| `P1-M11` | AIPW ATE/ATT | nuisance/DR claimの条件、crossfit/variance |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**未実測のBackend/Independent Reference/Method固有Schema/定量閾値は上記契約が未定義であることとは異なる。** 採用済みTarget/数理規則をAgent裁量で変更せず、未実測はScience/Freezeの該当判定でBLOCKEDとする。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M10` Native IPW／ATE・ATT（別fixture） | `DD-E11-METH-P110` | DGP-002, DGP-003; NEG-010, NEG-018 | REF-E02 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M11` Native AIPW／ATE・ATT（別fixture） | `DD-E11-METH-P111` | DGP-002, DGP-003; NEG-010, NEG-011, NEG-012 | REF-E03 | AC-D03, AC-P01, AC-P03, AC-P05, AC-I01, AC-I02 | PLAN:G03 / BLOCKED / NOT_GENERATED |

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
- **Required test semantics:** `P1-M10` IPWはe(X)の適格性、0/1のsupport、overlap、重みと正規化、ATE/ATT別weight式、ESS、balanceを別項目として計算。 `P1-M11` AIPWはpropensityとoutcome nuisance m0/m1、crossfit fold/seed、Augmented Score、Target populationとCI推論方式を固定。double robustnessの有限標本保証を偽称しない。 Clipping/Trimmingによるestimand/target population変化を記録し、無言の閾値採用・古いATEラベル維持を禁止。inference unavailableはpoint-only/typed reasonで出力。
- Schema+Method validation（unit）、Class.Port/Result provenance（contract）、実有効Backend/CLI/Publisher/旧v2（integration）を区別。Independent scientific DGP/Oracleは適格な真値から導出し、Estimator自己出力をReferenceにしない。
- Evidenceにsource/lock/fixture SHA、Method/Estimand/Inference、positive+negativeのexpected/observed、実効Backend/API/config/seed、collect済path/command/Resultを残す。Filesystem/科学証拠が未取得ならBLOCKED、期待値緩和によるPASSは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03,P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、Optional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。G05 Row Writer/Trust Anchor等の設計不在、G02 IV target、G08 AR独立reference等を推測で解決しない。


## 8. Self-contained freeze review boundary

- 本文§3で必要なClassのConstructor・Field・公開Method・処理責務、§4で実装順序/分岐、§5〜6でMethod別のScience/Testを保持する。外部DDやGate06を読ませて不足仕様を推測させない。
- **未確定事項:** AIPW推論/finite sample・nuisance/crossfit/CI・Policyの明文化。 未解決のBackend API、Method Config、DGP/NEG/Reference/quantitative Science、Owner Decisionは該当MethodをBLOCKEDとし、Freeze前に閉じる。
