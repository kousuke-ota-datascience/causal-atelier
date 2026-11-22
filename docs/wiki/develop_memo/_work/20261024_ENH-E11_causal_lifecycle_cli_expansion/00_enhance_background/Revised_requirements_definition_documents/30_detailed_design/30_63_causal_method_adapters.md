# 30_63_causal_method_adapters

---

## 1. Scientific Adapter Class詳細

### 1.1. `NativeIdentificationAdapter`

#### 1.1.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.identification.NativeIdentificationAdapter`。 IdentificationのMethod実行Adapter。担当Method：`P1-M01, P1-M02`。**再利用:** 既存ariadne.scientific.identification.adapter.IdentificationAdapterのrandomized/backdoor処理・証拠表現。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.1.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.1.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.1.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.1.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M01` | randomized identification | 割当機構・target、proofの型付き正規化 |
| `P1-M02` | backdoor ATE | adjustment/backdoor、Graph・Design適格性 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.1.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.1.7. 検証

`DD-E11-METH-P101`（`P1-M01`）、`DD-E11-METH-P102`（`P1-M02`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.2. `DoWhyIdentificationAdapter`

#### 1.2.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.identification.DoWhyIdentificationAdapter`。 IdentificationのMethod実行Adapter。担当Method：`P1-M03, P1-M04, P1-M05`。**再利用:** 既存IdentificationAdapterのDTO・Graph意味を再利用しDoWhy固有識別を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.2.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.2.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.2.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.2.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M03` | backdoor ATE | effective API、method-specific proof、Graph対応 |
| `P1-M04` | frontdoor ATE | 単一Mediator／識別仮定、数値FD-Aとは別 |
| `P1-M05` | IDENTIFY B0_BINARY_IV / conditional `LATE_COMPLIER` | 単一二値Z/A・無調整、relevance/independence/exclusion/monotonicity方向/consistencyの宣言と検査、DoWhy実効IV式をtyped Proofへ。display labelからLATE cast禁止、推定禁止 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。


**P1-M05（OD-01=A Owner採用）の不変実装契約：** `IDENTIFY`のみ。`estimand.family=LATE_COMPLIER`、population=compliers、contrast=A1−A0、`design_profile=B0_BINARY_IV`。単一binary instrument Z・binary endogenous treatment A・outcome Y・無調整C無しを要求し、instrument relevance/nonzero first-stage、independence、exclusion、monotonicity方向、consistency/SUTVAを宣言済み・ref付きDesign仮定として検証する。これら未検証な因果仮定をGraphだけから実証したと扱わない。選択済DoWhy effective library/APIのIV expression/identifierを確認して初めてconditional `IdentificationOutcome`を返し、DoWhy内部の`nonparametric-ate`等の表示から自動LATE castしない。検証済みProof、Estimand/Graph/Question/Design/Dataset hashes、条件付きAssumption refsを保持。B1/DRIV/ATE target・非二値Z/A・欠落IV仮定・API非互換・wrong hashをtyped `IDENTIFICATION_TARGET_UNRESOLVED`/`METHOD_INCOMPATIBLE`/`REQUIRES_REVIEW`/`CAPABILITY_UNAVAILABLE`等でfail closed。弱IVの統計的兆候を「Graph条件と同じ意味の非識別」と混同せず、推定可能な点値/CIを作らない。`IDENTIFY`は`identification.json`を出版し、`result.json`やNumerical Effectを出さない。DGP-006、NEG-006/007、REF-I03/REF-G01にinvalid Target/Graph/monotonicity/weak IV/APIの負例を追加。G08 B0 Wald/2SLS/ARは本Adapterの責務外。Method Config/独立Reference/実効DoWhy APIは実行検証前に明示的に固定する（未作成なら`METHOD_PROFILE_UNAVAILABLE`）。

#### 1.2.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.2.7. 検証

`DD-E11-METH-P103`（`P1-M03`）、`DD-E11-METH-P104`（`P1-M04`）、`DD-E11-METH-P105`（`P1-M05`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.3. `FciDiscoveryAdapter`

#### 1.3.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.discovery.FciDiscoveryAdapter`。 Graph DiscoveryのMethod実行Adapter。担当Method：`P1-M06`。**再利用:** 既存DiscoveryAdapterのGraph意味Validatorとnode/edge変換を共有。PCをFCIとみなさない。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.3.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.3.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.3.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedDiscoveryRequest)` | `CapabilityOrEligibilityResult` | P1-M06固有CI/Data/BK/Backend適格性 |
| `execute(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink)` | `DiscoveryGraphOutcome` | PAG endpoint/lag/latentをlossless保持 |

FCIのAdapter実装署名は`ValidatedDiscoveryRequest`と`DiscoveryGraphOutcome`に統一し、汎用`ValidatedMethodRequest`と同名overloadを作らない。`DiscoveryPort.discover`のConcreteが同一Method Registryの選択済CapabilityでAdapterをロードし、preflight後にexecuteする。旧`ScientificCorePort.run_discovery`はversioned Bridgeで別の公開署名を維持する。

#### 1.3.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M06` | PAG | circle/bidirected/latent・oracle、point estimation不可 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.3.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.3.7. 検証

`DD-E11-METH-P106`（`P1-M06`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.4. `FrontdoorLinearAdapter`

#### 1.4.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.frontdoor.FrontdoorLinearAdapter`。 EstimationのMethod実行Adapter。担当Method：`P1-M07`。**再利用:** 既存CausalDesign・回帰推定器を再利用。数値FD-A固有契約を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.4.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.4.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.4.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.4.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M07` | restricted FD-A ATE | 線形Mediator/Outcomeモデルとno direct path仮定、別Reference・CI |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.4.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.4.7. 検証

`DD-E11-METH-P107`（`P1-M07`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.5. `NativeEffectAdapter`

#### 1.5.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.estimation.NativeEffectAdapter`。 EstimationのMethod実行Adapter。担当Method：`P1-M08, P1-M09`。**再利用:** 既存EstimationAdapterとcausal.inference.estimators.treatment_effectの計算。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.5.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.5.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.5.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.5.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M08` | randomized diff-in-means ATE | randomization、variance、seedとpopulation |
| `P1-M09` | OLS adopted ATE/ATT | linear model/contrast、robust varianceの採否 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.5.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.5.7. 検証

`DD-E11-METH-P108`（`P1-M08`）、`DD-E11-METH-P109`（`P1-M09`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.6. `WeightingEffectAdapter`

#### 1.6.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.estimation.WeightingEffectAdapter`。 EstimationのMethod実行Adapter。担当Method：`P1-M10, P1-M11`。**再利用:** 既存IPW/AIPWとpropensity・balance診断。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.6.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.6.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.6.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.6.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M10` | IPW ATE/ATT | propensity/overlap/balance/ESS/weights/CI |
| `P1-M11` | AIPW ATE/ATT | nuisance/DR claimの条件、crossfit/variance |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.6.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.6.7. 検証

`DD-E11-METH-P110`（`P1-M10`）、`DD-E11-METH-P111`（`P1-M11`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.7. `RefutationAdapter`

#### 1.7.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.refutation.adapter.RefutationAdapter`。 共通Field/Constructor表はtyped Bridge側の依存候補であり、既存Classに未実装Fieldを既成事実として追加しない。 DiagnosticのMethod実行Adapter。担当Method仕様：`P1-M12, P1-M13, P1-M14, P1-M15`。**既存Sourceの実装済みはP1-M12（PLACEBO_TREATMENT）とP1-M13（DATA_SUBSET）のみ。P1-M14（RANDOM_COMMON_CAUSE）とP1-M15（BOOTSTRAP）は本Class/Facadeでの新規実装が必要で、既存機能と称さない。 **再利用:** 既存RefutationAdapter.runはそのまま維持。必要ならMethod用typed façadeから共有処理を呼ぶ。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.7.2. フィールド

**既存ABI契約:** 現行Classに宣言済みのInstance Fieldはない。MethodDescriptor/BackendFactory/ScientificContextは既存実装の属性ではなく、型付きPortから呼び出す新規Facade／Bridgeの依存として定義する。既存Classへの無断Field追加を前提にしない。

#### 1.7.3. Constructor / Factory

**既存ABI契約:** ariadne.scientific.refutation.adapter.RefutationAdapter に明示的`__init__`はない。公開`run(input_, output_dir)`は変更しない。typed Facadeは別Classに配置し、旧ClassのConstructor ABIにDescriptorを注入しない。

#### 1.7.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `run(self, input_: RefutationInput, output_dir: Path)` | `list[ScientificResultDescriptor]` | **既存v2公開API**。互換維持。typed façadeは既存runを無検証castせず検証済み中間表現へ変換する |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.7.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M12` | placebo treatment | 事前指定置換ルール、null診断、再現seed |
| `P1-M13` | data subset | Subset規則、sample/support、差分の解釈 |
| `P1-M14` | random common cause | 摂動DGP/seed、条件付き安定性 |
| `P1-M15` | bootstrap refutation | resampling unit/CI可用性、同一DGP |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.7.6. I/O・連携・失敗処理

既存`run(input_,output_dir)`のPath I/O/DTOはv2専用。Local型付き実行は共通の純粋計算Kernelを抽出する互換Bridgeから再利用し、新Portが旧Path writerを直接呼んでStaging制約を迂回してはならない。旧v2は従来のPath出力、新型付きAdapterは`StagingArtifactSink`だけに書く。旧DTOからの無検証CASTは禁止。Scientific Negativeとtechnical errorを分離。

#### 1.7.7. 検証

`DD-E11-METH-P112`（`P1-M12`）、`DD-E11-METH-P113`（`P1-M13`）、`DD-E11-METH-P114`（`P1-M14`）、`DD-E11-METH-P115`（`P1-M15`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.8. `SensitivityAdapter`

#### 1.8.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.sensitivity.adapter.SensitivityAdapter`。 共通Field/Constructor表はtyped Bridge側の依存候補であり、既存Classに未実装Fieldを既成事実として追加しない。 DiagnosticのMethod実行Adapter。担当Method仕様：`P1-M16, P1-M17`。既存SourceはADJUSTMENT_SETとPROPENSITY_CLIPPINGの実装を持つが、新契約で必要な適格性・実効推論・Codecの再検証は別途必要。**再利用:** 既存SensitivityAdapter.runを維持。必要ならtyped façadeから共有処理を呼ぶ。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.8.2. フィールド

**既存ABI契約:** 現行Classに宣言済みのInstance Fieldはない。MethodDescriptor/BackendFactory/ScientificContextは既存実装の属性ではなく、型付きPortから呼び出す新規Facade／Bridgeの依存として定義する。既存Classへの無断Field追加を前提にしない。

#### 1.8.3. Constructor / Factory

**既存ABI契約:** ariadne.scientific.sensitivity.adapter.SensitivityAdapter に明示的`__init__`はない。公開`run(input_, output_dir)`は変更しない。typed Facadeは別Classに配置し、旧ClassのConstructor ABIにDescriptorを注入しない。

#### 1.8.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `run(self, input_: SensitivityInput, output_dir: Path)` | `list[ScientificResultDescriptor]` | **既存v2公開API**。互換維持。typed façadeは既存runを無検証castせず検証済み中間表現へ変換する |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.8.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M16` | adjustment set | Graph/Design/追加変数・post treatment適格性 |
| `P1-M17` | propensity clipping | trim threshold、estimand変化、ESS/sample loss |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.8.6. I/O・連携・失敗処理

既存`run(input_,output_dir)`のPath I/O/DTOはv2専用。Local型付き実行は共通の純粋計算Kernelを抽出する互換Bridgeから再利用し、新Portが旧Path writerを直接呼んでStaging制約を迂回してはならない。旧v2は従来のPath出力、新型付きAdapterは`StagingArtifactSink`だけに書く。旧DTOからの無検証CASTは禁止。Scientific Negativeとtechnical errorを分離。

#### 1.8.7. 検証

`DD-E11-METH-P116`（`P1-M16`）、`DD-E11-METH-P117`（`P1-M17`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.9. `ObservedNceAdapter`

#### 1.9.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.negative_controls.ObservedNceAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M18`。**再利用:** 既存Design/Outcome/Inference検証を共通化してNCEを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.9.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.9.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.9.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.9.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M18` | negative control exposure | 実在Z・事前帰無・opt-in、条件付き関連/負結果 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.9.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.9.7. 検証

`DD-E11-METH-P118`（`P1-M18`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.10. `ObservedNcoAdapter`

#### 1.10.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.negative_controls.ObservedNcoAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M19`。**再利用:** 既存Design/Outcome/Inference検証を共通化してNCOを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.10.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.10.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.10.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.10.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M19` | negative control outcome | 実在W・事前帰無・opt-in、条件付き関連/負結果 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.10.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.10.7. 検証

`DD-E11-METH-P119`（`P1-M19`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.11. `OlsRvAdapter`

#### 1.11.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.sensitivity.OlsRvAdapter`。 DiagnosticのMethod実行Adapter。担当Method：`P1-M20`。**再利用:** 既存OLS推定の係数・SE・dfを再利用。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.11.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.11.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.11.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.11.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M20` | OLS partial R²、point RV(q=1) | 古典OLS係数/SE/df、非OLS拒否 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.11.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.11.7. 検証

`DD-E11-METH-P120`（`P1-M20`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.12. `EconmlCateAdapter`

#### 1.12.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.heterogeneity.EconmlCateAdapter`。 EstimationのMethod実行Adapter。担当Method：`P2-M01, P2-M02, P2-M03, P2-M04`。**再利用:** 既存CausalDesign・propensity/overlap検証を再利用しEconML固有APIを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.12.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.12.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.12.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.12.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P2-M01` | LinearDML CATE | X/W/treatment/outcome、inference registry、fold |
| `P2-M02` | CausalForestDML CATE | leaf/support/nuisance/CI API、row privacy |
| `P2-M03` | DRLearner CATE | binary treatment/propensity、inference method |
| `P2-M04` | ForestDRLearner CATE | propensity+forest inference/support |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.12.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.12.7. 検証

`DD-E11-METH-P201`（`P2-M01`）、`DD-E11-METH-P202`（`P2-M02`）、`DD-E11-METH-P203`（`P2-M03`）、`DD-E11-METH-P204`（`P2-M04`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.13. `MetaLearnerAdapter`

#### 1.13.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.heterogeneity.MetaLearnerAdapter`。 EstimationのMethod実行Adapter。担当Method：`P2-M05, P2-M06, P2-M07`。**再利用:** 既存CausalDesignとOutcome modelを再利用しS/T/X適格性を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.13.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.13.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.13.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.13.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P2-M05` | S-Learner CATE | counterfactual prediction、point/CI制限 |
| `P2-M06` | T-Learner CATE | treated/control support、point/CI制限 |
| `P2-M07` | X-Learner CATE | cross-model weights、point/CI制限 |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.13.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.13.7. 検証

`DD-E11-METH-P205`（`P2-M05`）、`DD-E11-METH-P206`（`P2-M06`）、`DD-E11-METH-P207`（`P2-M07`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.14. `EconmlDrivAdapter`

#### 1.14.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.heterogeneity.EconmlDrivAdapter`。 EstimationのMethod実行Adapter。担当Method：`P2-M08`。**再利用:** 共通IV/Estimandの識別検証を再利用しDRIV固有APIを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.14.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.14.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.14.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.14.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P2-M08` | IV heterogeneous structural slope | Z/A/X/W、IV relevance/exclusion、inference |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.14.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.14.7. 検証

`DD-E11-METH-P208`（`P2-M08`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.15. `TigramiteTemporalAdapter`

#### 1.15.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.temporal.TigramiteTemporalAdapter`。 Graph DiscoveryのMethod実行Adapter。担当Method：`P3-M01, P3-M02, P3-M03`。**再利用:** 既存Graph endpoint意味とlag規約の共通Validatorを再利用。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.15.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.15.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.15.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.15.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M01` | PCMCI | CI test/lag window、time-series order、graph |
| `P3-M02` | PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| `P3-M03` | LPCMCI | PAG/latent/endpoint fidelity、lag |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.15.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.15.7. 検証

`DD-E11-METH-P301`（`P3-M01`）、`DD-E11-METH-P302`（`P3-M02`）、`DD-E11-METH-P303`（`P3-M03`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.16. `PanelQuasiAdapter`

#### 1.16.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.PanelQuasiAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M04, P3-M05`。**再利用:** 共通Estimand/Design/Time validationを再利用しDiD/Event Study推定を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.16.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.16.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.16.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.16.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M04` | DiD ATT | 2x2 vs staggered、parallel trends、SE/cluster |
| `P3-M05` | Event Study | cohort/event time、pretrend、reference periods |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.16.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.16.7. 検証

`DD-E11-METH-P304`（`P3-M04`）、`DD-E11-METH-P305`（`P3-M05`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.17. `InterruptedTsAdapter`

#### 1.17.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.InterruptedTsAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M06`。**再利用:** 共通Time/Design検証を再利用しITS HAC推論を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.17.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.17.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.17.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.17.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M06` | level/slope change | intervention date、seasonality/autocorrelation/HAC |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.17.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.17.7. 検証

`DD-E11-METH-P306`（`P3-M06`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.18. `RddAdapter`

#### 1.18.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.RddAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M07, P3-M08`。**再利用:** 共通IV/EstimandとScientific CIを再利用しSharp/Fuzzyを明示区別。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.18.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.18.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.18.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.18.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M07` | Sharp RD local effect | bandwidth、kernel/order、density manipulation、CI |
| `P3-M08` | Fuzzy RD local complier effect | First stage、discontinuity ratio、local IV inference |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.18.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.18.7. 検証

`DD-E11-METH-P307`（`P3-M07`）、`DD-E11-METH-P308`（`P3-M08`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.19. `WaldRatioAdapter`

#### 1.19.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.iv.WaldRatioAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M09`。**再利用:** 共通IV適格性を再利用、Waldとweak-IV negativeを追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.19.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.19.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.19.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.19.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M09` | B0 complier LATE reference | binary Z/A、IV assumptions、first stage |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.19.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.19.7. 検証

`DD-E11-METH-P309`（`P3-M09`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.20. `TwoSlsAdapter`

#### 1.20.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.iv.TwoSlsAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M10, P3-M11`。**再利用:** 共通IV適格性を再利用、B0/B1識別対象・AR反転を追加。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.20.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.20.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.20.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.20.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M10` | B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| `P3-M11` | B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.20.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.20.7. 検証

`DD-E11-METH-P310`（`P3-M10`）、`DD-E11-METH-P311`（`P3-M11`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.21. `SyntheticControlAdapter`

#### 1.21.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.SyntheticControlAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M12`。**再利用:** 共通Panel/Time/Donor適格性とpoint-only inferenceを利用。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.21.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.21.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.21.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.21.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M12` | treated-unit counterfactual gap | donor pretreatment fit/contamination、point-only |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.21.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.21.7. 検証

`DD-E11-METH-P312`（`P3-M12`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。

### 1.22. `SyntheticDidAdapter`

#### 1.22.1. 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.quasi.SyntheticDidAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M13`。**再利用:** 共通Panel/Time/Donor適格性とunit/time weightsを利用。入口がCLIであることを科学的な別実装の根拠にしない。

#### 1.22.2. フィールド

| Field / dependency | Type | 制約 |
|---|---|---|
| `method_descriptor` | `MethodDescriptor` | 実行Method IDとEstimand/Operation/Inferenceを固定。Backendのデフォルトに任せない |
| `backend_factory` | `Callable[..., BackendAdapter]`（必要なMethodだけ） | optional dependencyは遅延導入。外部Estimator Objectを永続化しない |
| `policy` | `ScientificEligibilityPolicy` | 科学的適格性Policyの不変依存。ValidatedScientificContextはInstance Fieldにせずrequestごとに受け渡す |

#### 1.22.3. Constructor / Factory

`__init__(self, *, descriptor: MethodDescriptor, backend_factory: BackendFactory, policy: ScientificEligibilityPolicy)`。`descriptor`引数を不変`method_descriptor` Fieldに保持し、`backend_factory`と`policy`もConstructor依存としてのみ保持する。`ValidatedScientificContext`は`request`のper-run evidenceであり、共有Instance Fieldに保持しない。Constructorは外部ライブラリのimport/数値計算/Artifact書込を行わない。DescriptorのMethod/Operation/Estimand適合を検証し、不一致はtyped error。

#### 1.22.4. メソッド

| Signature | Return | Contract |
|---|---|---|
| `preflight(self, request: ValidatedMethodRequest)` | `EligibilityOutcome` | Method/Estimand/Design/Backend Profileの静的適格性を型付きで返す。推定処理・File公開なし |
| `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` | `TypedScientificOutcome` | 適格なMethodだけ実行し、ArtifactはStagingへ。外部Backend Objectを返さない |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 1.22.5. 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M13` | panel average effect | donor and time weights、preperiod/variance method |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### 1.22.6. I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 1.22.7. 検証

`DD-E11-METH-P313`（`P3-M13`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には§2の41 Method tableと§4〜§8を優先し、この7区分の記載だけで科学的PASSとはしない。


## 2. 全41件のAdapter allocation

| Method ID | Adapter / Estimand型 | 必須preflight／Result・Inference |
| --- | --- | --- |
| P1-M01 | `NativeIdentificationAdapter` / randomized identification | 割当機構・target、proofの型付き正規化 |
| P1-M02 | `NativeIdentificationAdapter` / backdoor ATE | adjustment/backdoor、Graph・Design適格性 |
| P1-M03 | `DoWhyIdentificationAdapter` / backdoor ATE | effective API、method-specific proof、Graph対応 |
| P1-M04 | `DoWhyIdentificationAdapter` / frontdoor ATE | 単一Mediator／識別仮定、数値FD-Aとは別 |
| P1-M05 | `DoWhyIdentificationAdapter` / B0 conditional `LATE_COMPLIER` identification | IDENTIFY専用、二値Z/A・追加C無し、明示Design仮定とIV proof、DoWhy labelだけのLATE変換禁止 |
| P1-M06 | `FciDiscoveryAdapter` / PAG | circle/bidirected/latent・oracle、point estimation不可 |
| P1-M07 | `FrontdoorLinearAdapter` / restricted FD-A ATE | 線形Mediator/Outcomeモデルとno direct path仮定、別Reference・CI |
| P1-M08 | `NativeEffectAdapter` / randomized diff-in-means ATE | randomization、variance、seedとpopulation |
| P1-M09 | `NativeEffectAdapter` / OLS adopted ATE/ATT | linear model/contrast、robust varianceの採否 |
| P1-M10 | `WeightingEffectAdapter` / IPW ATE/ATT | propensity/overlap/balance/ESS/weights/CI |
| P1-M11 | `WeightingEffectAdapter` / AIPW ATE/ATT | nuisance/DR claimの条件、crossfit/variance |
| P1-M12 | `RefutationAdapter` / placebo treatment | 事前指定置換ルール、null診断、再現seed |
| P1-M13 | `RefutationAdapter` / data subset | Subset規則、sample/support、差分の解釈 |
| P1-M14 | `RefutationAdapter` / random common cause | 摂動DGP/seed、条件付き安定性 |
| P1-M15 | `RefutationAdapter` / bootstrap refutation | resampling unit/CI可用性、同一DGP |
| P1-M16 | `SensitivityAdapter` / adjustment set | Graph/Design/追加変数・post treatment適格性 |
| P1-M17 | `SensitivityAdapter` / propensity clipping | trim threshold、estimand変化、ESS/sample loss |
| P1-M18 | `ObservedNceAdapter` / negative control exposure | 実在Z・事前帰無・opt-in、条件付き関連/負結果 |
| P1-M19 | `ObservedNcoAdapter` / negative control outcome | 実在W・事前帰無・opt-in、条件付き関連/負結果 |
| P1-M20 | `OlsRvAdapter` / OLS partial R²、point RV(q=1) | 古典OLS係数/SE/df、非OLS拒否 |
| P2-M01 | `EconmlCateAdapter` / LinearDML CATE | X/W/treatment/outcome、inference registry、fold |
| P2-M02 | `EconmlCateAdapter` / CausalForestDML CATE | leaf/support/nuisance/CI API、row privacy |
| P2-M03 | `EconmlCateAdapter` / DRLearner CATE | binary treatment/propensity、inference method |
| P2-M04 | `EconmlCateAdapter` / ForestDRLearner CATE | propensity+forest inference/support |
| P2-M05 | `MetaLearnerAdapter` / S-Learner CATE | counterfactual prediction、point/CI制限 |
| P2-M06 | `MetaLearnerAdapter` / T-Learner CATE | treated/control support、point/CI制限 |
| P2-M07 | `MetaLearnerAdapter` / X-Learner CATE | cross-model weights、point/CI制限 |
| P2-M08 | `EconmlDrivAdapter` / IV heterogeneous structural slope | Z/A/X/W、IV relevance/exclusion、inference |
| P3-M01 | `TigramiteTemporalAdapter` / PCMCI | CI test/lag window、time-series order、graph |
| P3-M02 | `TigramiteTemporalAdapter` / PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| P3-M03 | `TigramiteTemporalAdapter` / LPCMCI | PAG/latent/endpoint fidelity、lag |
| P3-M04 | `PanelQuasiAdapter` / DiD ATT | 2x2 vs staggered、parallel trends、SE/cluster |
| P3-M05 | `PanelQuasiAdapter` / Event Study | cohort/event time、pretrend、reference periods |
| P3-M06 | `InterruptedTsAdapter` / level/slope change | intervention date、seasonality/autocorrelation/HAC |
| P3-M07 | `RddAdapter` / Sharp RD local effect | bandwidth、kernel/order、density manipulation、CI |
| P3-M08 | `RddAdapter` / Fuzzy RD local complier effect | First stage、discontinuity ratio、local IV inference |
| P3-M09 | `WaldRatioAdapter` / B0 complier LATE reference | binary Z/A、IV assumptions、first stage |
| P3-M10 | `TwoSlsAdapter` / B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| P3-M11 | `TwoSlsAdapter` / B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |
| P3-M12 | `SyntheticControlAdapter` / treated-unit counterfactual gap | donor pretreatment fit/contamination、point-only |
| P3-M13 | `SyntheticDidAdapter` / panel average effect | donor and time weights、preperiod/variance method |

**41 Method：** P1=20、P2=8、P3=13。ここでの`P1/P2/P3`はMethod catalogのPhase接頭辞であり、Enhance Workflowの`P01〜Pxx` Work Package IDとは異なる。P1-M05はOwner採用の明示的B0 `LATE_COMPLIER` conditional identificationを対象とする。Method label/DoWhy backendの表示からEstimandを推測せず、要求・前提・Proof未検証なら型付きBLOCKとする。MethodConfig・BackendVersion・Inference可用性・科学ReferenceをMethodに結び付ける。

### 2.1. Method Schemaと受理範囲

41 Method IDは固定Catalog識別子であり、各IDにOperation、Estimand、Backend/Profile、Method Config Schema、Question/Design Evidence Profile、Inference Policy、Output Artifact Profileを登録する。Class割当があることだけでは実行可能性を意味しない。`ValidatedMethodRequest`は登録済みstrict Method Schemaとcross-asset semantic Validatorの双方に成功した場合のみFactoryから生成する。

P1-M06は`e11_p1_m06_fci_method_config_v1.schema.json`、専用Question/Design internal profilesを使用する。他のMethodについてconfig/profile未定義のまま`config={}`やBackend defaultで通すことを禁止し、`METHOD_PROFILE_UNAVAILABLE`等のtyped reasonでfail-closedにする。各Method提供前に対応Gateで正規Schema、条件付き必須項目、negative fixturesを確定し登録する。Gate IDはSchema dispatchのキーにしない。


**OD-05 Gate別Method Profile採用：** P1-M06を除く40 Methodは各Owner Gateでstrict Method Config/Question/Design/Output/Inference Profileを作成してMethodRegistryに登録する（G02=6/G03=13/G04=8/G06=3/G07=3/G08=5/G09=2）。登録の有無と科学的真理・数値的Referenceは区別し、未登録は`METHOD_PROFILE_UNAVAILABLE`。このProfile作成方式のOwner採用は、個々のMethod Schema JSONやCI/Backend/科学Oracleの完成を意味しない。統合G10は41 Methodの有効な独立科学証拠を確認し、依存閉包不変なら再利用し、新規Method IDを追加しない。

## 3. 共通Adapter Contract

### 3.1. Module-level関数とResult処理

`ariadne.scientific.causal_methods.*`：
- `check_design(request) -> EligibilityOutcome`：Method固有のRequired Columns、missing、Temporal/Panel units、instrument support、positivity等のReasonを収集。
- `run(request, *, sink: StagingArtifactSink) -> TypedScientificOutcome`：数値計算。返却するのはportable Result DTO、external library instanceは禁止。日時・randomnessは注入されたContextのみから取得。
- `describe_effective_backend() -> BackendEvidence`：実効Library/distribution、Python API、solver/nuisance/fold/CI config/seedを返す。
- `serialize(result) -> ArtifactBundle`：Graph/Result/Diagnosticsを型付きSchemaに純粋変換する。File I/Oはしない。保存はAdapterが渡された`StagingArtifactSink`を通じて行い、Finite/not-finiteを判定しnull+reasonを記録する。

### 3.2. Failure semantics

- 入力契約違反＝`CONFIG_INVALID / METHOD_INCOMPATIBLE`、Backend unavailable＝`CAPABILITY_UNAVAILABLE`。これらは他手法へのfallback要因にしない。
- 仮定未成立、positivity不足、弱IV、非識別、CI unavailable、negative-control nullは**科学的Status/Reason**。当該Methodに適格なPointやCIがないことを明示。
- Backendの数値例外、収束エラー、非有限推定を成功へ書き換えない。
- Confirmatory ResultはMethod別の妥当な推論がなければScience PASSとしない。

## 4. P1 推定器・Refutation/Negative Control

### 4.1. Estimation formulasと診断

- Diff-in-means：`mean(Y|A=1)-mean(Y|A=0)`。randomized designと割当/分散推論条件を先に検査。
- OLS：OutcomeモデルのTarget Contrastを明示し、係数とATE/ATTの対応はDesign・Model仮定で限定。robust HC variantの採用は事前固定。
- IPW：propensity `e(X)`、ATEの重み例 `A/e(X)+(1-A)/(1-e(X))`、ATTには別の標本対象・weight normalization。clip/trimでtargetが変化し得ることをResultへ記録。balance/ESSとoverlap必須。
- AIPW：outcome nuisance `m_a(X)` とpropensityのAugmented scoreを別統計量として実装。double robustnessは必要な推定仮定／十分な推定品質の代わりでない。nuisance/fold/seedと推論方針を記録。
- FD-A：Frontdoor識別（A→M→Y、適格なバックドア条件等）と線形二段階数値推定を分離。MediatorとOutcomeの条件付き回帰仕様・直接効果項や交互作用の扱いを固定し、`a_to_m * m_to_y`型の制限付き係数積が有効なDGPでのみ利用。一般Frontdoor識別をすべてこの算式へ還元しない。DGP-005/REF-E04と照合して正式化する。

### 4.2. Refutation / negative controls / sensitivity

- Placebo/Data subset/Random Common Cause/Bootstrapは同一base Effectのhash、変更条件・seed・resampling unitを固定。Refutationの統計的検定と因果識別自体を同一視しない。
- NCE/NCOは観測実在のZ/W、事前指定負の対照関係・条件付き帰無、同じDesign covariatesとデータ適格性を要求し、p値が大きいことを無交絡証明と報告しない。
- OLS RVは古典OLSのcoefficient/SE/dfを再現し、指定の `q=1` partial R² / robustness valueのみ対象。他Estimatorへ自動拡張しない。

### 4.3. Tests

`DD-E11-METH-P101`〜`P120`：各Method IDに対応する必須positive、unsupported config、negative（DGP/NEG/REF/ACは10_32に従う）。特にFR-188、FR-189/190/191/192、AR-030/031/032/033/044。

### 4.4. P1-M06 `FciDiscoveryAdapter`のMethod固有契約

`FciDiscoveryAdapter.preflight(request:ValidatedDiscoveryRequest) -> CapabilityOrEligibilityResult`は静的な適格性判定、`execute(request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome`はFCI結果のPAGへの正規化である。Product `ScientificCorePort.run_discovery`やPC Adapterへの単純aliasを禁止。ただし既存のGraph意味検証・PC計算ヘルパーなど科学的に同義の処理は再利用し、別エンジンを重複実装しない。

[FCI Method config schema](../23_api_interface_design/schema_drafts/e11_p1_m06_fci_method_config_v1.schema.json)に従い`fisherz/chisq/gsq`、明示alpha/depth/max_path_length、null/required/forbidden directed BackgroundKnowledgeを検証する。DatasetとDesignの列名・順序、finite complete observations、CI別measurement scale、categorical support、観測独立性・標本規模、BK矛盾を確認し、未承認の欠損補完・離散化・CI代替をしない。特定の`causal-learn`版を科学的Method定義に固定せず、effective distribution/API/signature/endpoint accessorとlockをRuntimeで照合し、不一致は`BACKEND_API_MISMATCH`。

Backend nodeとDataset列を1:1で対応させ、node1/node2に対応するendpoint markの順序を保持する。PAG circle/bidirectedをDAGへ確定せず、重複・不正node/markを拒否し、GraphEvidenceとdual hashを共通科学契約へ渡す（Product GraphVersion IDは自動発行しない）。BKがPAGの不確定endpointを過剰確定する場合は独立motif検証なしに成功としない。2観測変数の潜在交絡を一意識別したとは報告しない。

`DD-E11-METH-P106`は実効API/eligibility、独立MAG/PAG同値類Oracle、BK/latent negativeの検証契約。Backendの出力を自らの正解Oracleにしない。

## 5. P2 CATE / DRIV

### 5.1. Non-IV 7 Method

LinearDML/CausalForestDML/DRLearner/ForestDRLearner/S/T/X-Learnerを単にCATEという名称で同等に扱わない。X=effect modifiers、W=confounders、nuisance models、treatment type、target population、crossfitting/final model、backend/versionをper Method Configとする。

- Result Point CATE(x)、Population summary、support/overlap診断を分離し、個票値は明示的に認可されたParquetのみ。Stdoutや小さなJSONへの個票全件混入を禁止。
- Inference RegistryはMethod/Backend/version/final estimator config別に `POINT_ONLY / SUPPORTED_CI / UNSUPPORTED / UNAVAILABLE / FAILED` を判定。Native bootstrapを統計的妥当性確認なしに汎用適用しない。
- Exploratory point-onlyは許すが、Confirmatoryは事前に宣言したtargetに適合するCIと独立Science Evidenceが必要。Pointwise CIとsimultaneous bandを区別する。

### 5.2. DRIV-A

Instrument Z、Treatment A、Effect modifier X、Control W、識別仮定とheterogeneous structural target `theta_IV(x)`を持つ。Non-IV `CATE(x)`、B0 complier LATE、B1 linear IV slopeと区別。weak IV・invalid IV・poor overlapをtyped negativeにし、一般化の範囲を限定する。

### 5.3. Tests

`DD-E11-METH-P201`〜`P208`：Method別inference availability、effective API、DGP-003/004/008、negative control/misspecification、privacy、CI pointwise coverage、Reference E05/E06。対応FR-193/194/195、AR-034/035。

## 6. P3 Graph / Temporal

### 6.1. Graph semantics

- FCIはPAG circle、bidirected、ambiguous orientationを保持し、そこからDAGを想像してpoint estimateへ通さない。
- PCMCI/PCMCI+/LPCMCIはCI test family、max lag、contemporaneous link、endpoint mark、時間方向規約をserializeする。MetaDataの `lag=-1` 等は明示Convention無しには意味を持たせない。
- GraphOracleは構造上の同値類／可識別方向／adjacency・endpointを比較し、学習したGraphの不確定な向きを真DAGへ罰則無しに変換しない。

### 6.2. Tests

`DD-E11-METH-P301`〜`P303`：DGP-009〜011、Graph Oracle、NEG-021/028、round-trip、sample ordering。対応FR-186/196、AR-028/036。

## 7. P3 Quasi / IV / SCM

### 7.1. DiD / Event / ITS

- DiD：2×2 ATTとstaggered adoptionを別Configuration/Estimandとし、staggeredに単純TWFE係数を普遍的ATTとして流用しない。parallel trendsとcohort support、cluster covarianceのunitを保存。
- Event Study：事前指定reference periodとevent-time vector、cohort composition、lead/pretrend診断を保持。post-intervention windowによる選択が推論に与える影響を記録。
- ITS：level/slope change、intervention date、seasonality/trend、serial covariance（HAC等）を方法別Configに固定。独立残差OLSのSEを無検証で採用しない。

### 7.2. Sharp/Fuzzy RD

- Sharp RD：cutoff周辺のlocal regression、bandwidth、polynomial order、kernel、density manipulation、covariate continuityの診断を出力。
- Fuzzy RD：cutoff近傍のTreatment first-stage jumpとOutcome jumpの比による局所IV効果。weak first stageやinstrument validityに注意。単なるSharp RDにlabelを変えるだけで代用しない。
- `rdrobust` 等の外部BackendはPython APIの実効版とrobust bias correction inferenceの利用可否を確認。GPLの顧客配布Legal approvalとは別。

### 7.3. Wald/B0/B1/AR

- B0（P3-M09/M10）：単一二値Z/A、無調整、単一内生Aのcomplier LATE。Wald ratioは縮約形Outcome差/First-stage Treatment差。分母0/弱い場合にfinite CIを強制しない。
- B1（P3-M11）：単一二値Z/A、事前指定C、additive linear IV構造の2SLS slope。一般ATE/ATTやB0と同一complier LATEと呼ばない。
- B0/B1の2SLSはfirst-stage/2nd-stage、heteroskedasticity-robust covariance、Instrument support/first-stage diagnosticsを保存。通常Wald区間はweak-IV robustでないことを明示。
- Anderson–Rubin：H0(β)の下で`Y - β A`のZとの関係を（B1では指定Cを条件付けて）検定、反転集合を作る。初期契約は独立観測・単一excluded Z・単一endogenous A・異分散頑健漸近推論の範囲。任意のcluster/HAC版へ自動拡張しない。β探索は有界gridだけではALL_REAL/非有界/非連結を判定できないためtail/bracketing/数値精度を検証。数学的にEMPTYなAR集合は汎用Codecで表現可能。ただし、非退化なB0/B1 just-identified HC1 AR反転では gA≠0、Var_HC1(βhat)>0 の条件からT_AR(βhat)=0で非空性が従う。そこでEMPTYが観測された場合はMethod別SCIENCE_INCONSISTENTとして検査する。first-stage=0、非正分散、rank欠損は別途型付き分岐にし、数値的な失敗と数学的EMPTYを混同しない。
- AR testがIVのexclusion/independence/monotonicityを証明すると解釈しない。CI coverageは独立Simulationで計測する。

**AR具体化（共通Source設計拘束）：** `Q=[1]`（B0）または`Q=[1,C]`（B1）をFull Rankで保持し、各βについて`Y−βA ~ Q+Z`のZ係数=0を**HC1・χ²(1)漸近検定**する方式を対象実装方式とする。残差化・quadratic inversionは全実数で行い、有限gridから非有界・空集合を断定しない。公式の数値/科学受入では独立reference・有効な分散・条件付きIV仮定を評価する。統計量、二次式、退化条件、Negative Matrixは本節のAR定義に従い、Method固有の独立Referenceと照合する。これはB0/B1の科学的な統計量・推論前提を規定するものであり、独立ReferenceとCoverage実測とは別である。

### 7.4. SCM / SDID

- SCM：donor poolの介入汚染を拒否し、pre-treatment fitとextrapolation、time-indexとweight optimization objectiveを保存する。初期は**point-only**であり未検証のplacebo intervalを付けない。
- Synthetic DiD：unit/time weights、pre/post period、面積とsupport、Method-specific standard errorを区別。SCMと同一Estimatorにはしない。

### 7.5. Tests

`DD-E11-METH-P304`〜`P313`：DGP-012〜018/024、REF-Q01〜Q05/REF-E07/E08、weak-IV negative、Graph/temporal control、CI/AR shape、donor/pretrend/first stage。対応FR-197〜200、AR-037〜041。Method別実効Backend/InferenceとReferenceは独立検証の対象となる。

## 8. Verification strategy and science boundaries

- `DD-E11-METH-P101〜P120 / P201〜P208 / P301〜P313`は41 Methodに対応する恒久的な受入義務ID。各Methodについてpositive DGP/独立Reference、negative Scenario、Method×Estimand/Backend/CI、canonical Result/Manifest readback、Product regression影響を検証する。
- 独立検証ではDGP version・seed・Method-specific推論・Monte Carlo SE/Coverage/多重性と適格Run分母を定義する。型・Schema一致は科学的Coverageや識別の証明ではない。
- 顧客Deliveryは実際のBundleのSBOM/Licenseと受領者別法務判定を別途必要とする。

参照：[E11 Domain/Ports](30_61_causal_domain_ports.md)、[Execution/Publisher](30_62_local_execution_publication.md)、[CLI Port IF](../23_api_interface_design/23_41_cli_scientific_ports.md)、[Method Scope](../10_requirements_definition/10_32_scientific_method_scope.md)。

## 9. 科学計算の共通実装とVersion付き互換Bridge

Adapterは`ariadne.scientific.causal_methods`に配置し、共通の`ariadne.causal.discovery`・`ariadne.causal.inference`内の既存計算を意味互換で再利用する。新しいFCI/IV/CATE等はMethod固有の新実装が必要な場合のみ追加する。Typed Port=`ariadne.scientific.ports.causal`、Capability Port=`ariadne.scientific.ports.capability`、BackendEvidence=`ariadne.scientific.capabilities`。旧Product `ScientificCorePort.run_*`は公開v2 DTO/Pathの署名を維持し、実装移行時は明示Bridgeから同一科学Kernelを呼ぶ。旧v2の型へAR/PAG/識別状態を損失変換してはいけない。

## 10. Class配置・既存Scientific Coreとの互換契約

22 Adapter Class中、`ariadne.scientific.refutation.adapter.RefutationAdapter`と`ariadne.scientific.sensitivity.adapter.SensitivityAdapter`は既存実装であり、旧`run(input_,output_dir)`署名を変更しない。その他のClassはMethodごとのClass契約として定義し、既存ClassのABIを無条件に変更しない。いずれも入口専用の独立数値実装を持つことは認めず、既存`causal.discovery`/`causal.inference`と`scientific.*`の関数・validationを再利用する。

`MethodDescriptor`の唯一のOwnerは`ariadne.capabilities.causal.method_registry.MethodCapabilityRegistry`。`StageRunnerRegistry`のStageType registryと同一視しない。旧Product `ScientificCorePort`の5 Operation署名を維持し、Method別typed Portが同じ科学的Kernelを利用する明示Bridgeを介する。新しいFCI、LATE/AR、CATE、Temporal、Quasiは既存の科学実装で不足する部分だけを別Method Adapterとして追加する。

22 Classの実装ModuleとMethodの対応は§1、41 Methodの対象と制約は§2〜§8がAuthorityである。Backend distribution/API availability・Optional Dependency・LicenseはMethodRegistryと独立Runtime probeで検証し、未取得EvidenceをAVAILABLEや科学的PASSにしない。


## 11. Method-specific strict Profile dispatch and ownership

Every catalog Method is accepted only after MethodRegistry dispatch and validation of strict Method Config, Question, Design, Output and Inference profiles. The 40 non-FCI draft profile suites reside in Revised IF23 schema_drafts/method_profiles; P1-M06 FCI already has dedicated Config/Question/Design drafts. Draft presence alone is not registry registration, effective backend availability or independent Science evidence.

Sequence: strict Study decoding → Method/Operation/Estimand/backend resolution → required Method Config/no unknown fields/no defaults → Question/Design/Dataset/Graph/Upstream semantic validation and actual hash → backend/version/API/inference preflight → typed computation → G01 staging/publication/Reader verification. No config={} success or method fallback. Public e11-local-*/1 wires and existing Product v2 ABI are invariant. Assumption declarations are conditional evidence, not proof of causal truth; confirmatory CI requires approved method-specific independent scientific coverage. G05 independently authorizes row export.

## Method profile factoring and scientific adapter constraints

各Methodの実行能力はMethod ID/Operation/Estimand/Graph/Design/Eligibility/Backend/Inference/Outputの明示的な適格条件で決定する。共通SchemaまたはAdapterを再利用できるのは、Method固有制約とPositive/Negative検証の同等性が確認できる場合だけである。未登録・科学的未検証・CI未対応の組合せはfail-closedとし、外部Backendの既定値から結果や推論を補完しない。G10は全41 Methodに有効な独立科学証拠を求め、影響依存が変更されたMethodを再検証する。

## Method-specific non-scalar payloads and file authority

Local Effect Result is scalar-only in its `point` member; for a Method whose target is a conditional-effect function, an event-time vector, or SCM time-indexed counterfactual gap, the scalar point is `NOT_AVAILABLE` with a non-scalar reason. The Manifest shall additionally inventory a typed internal artifact, with its own verified SHA, method and input/Study lineage; no cyclic Result→Artifact→Result hashes. For P2-M01–M08 the internal `cate_surface.json` contains evaluated effects only on an explicitly predeclared non-observed design grid; IV conditional structural slopes and non-IV CATE must be separately tagged. Person-level `X_i` or effect values are not written there; the separately approved G05 bounded Parquet policy controls those. For P3-M05, `event_time_effects.json` contains event-time/cohort/vector effects and a reference-period/pretrend contract. For P3-M12, `scm_gaps.json` contains observed, synthetic counterfactual and their difference for each PRE/POST time point, donor/preperiod/objective references, and point-only inference. P1-M01–05 publish typed `identification.json` and no Effect Result; P1-M12–20 publish typed `diagnostics.json` and no fictitious Effect Result. Internal draft shapes are owned by `schema_drafts/internal_scientific/`; cross-file Method/Estimand/Operation/ContentRef/Status consistency, evidence quality and numerical semantics are validated independently of JSON Schema.
