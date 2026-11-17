# ENH-E11 G08 P03 — two_sls_ar

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G08 / **Package:** P03 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G08_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G08_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** B0 Q=[1], B1 Q=[1,C]。Y−βA~Q+ZのHC1 χ²(1)全実数AR反転、EMPTY数学集合とFAILEDは別。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Sharp/Fuzzy RDDとB0/B1 IV/2SLSを局所Estimand・弱IV AR集合付きで提供する。

**科学/Designの必須制約:** B0 complier LATEとB1 structural slopeを区別。HC1 AR集合をfinite gridだけで判定しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** B0 Q=[1], B1 Q=[1,C]。Y−βA~Q+ZのHC1 χ²(1)全実数AR反転、EMPTY数学集合とFAILEDは別。

### 2A. Existing Source verified vs E11 RDD/IV API（`2cf28f59a324`）
- **現行ABI:** `src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_estimation(self, input_: EstimationInput, output_dir: Path)->list[ScientificResultDescriptor]`は旧Product Path API。 `src/ariadne/causal/inference/estimators/treatment_effect.py`の`TreatmentEffectEstimator`は既存diff/OLS/IPW/AIPW数値Kernelだが、Sharp/Fuzzy RD、Wald、B0/B1 2SLS、Anderson–Rubinの実装済み証拠ではない。旧APIを変更・無検証castせず新Typed EstimatorPortへ共有純粋Kernelを接続する。
- **新規科学境界:** `RddAdapter/WaldRatioAdapter/TwoSlsAdapter`は§3/§4の設計Class。P3-M09/M10のB0 binary Z/A complier LATE、P3-M11のB1 C調整付きstructural IV slopeを混同しない。HC1 Anderson–Rubinは各候補βの`Y-βA ~ [Q,Z]`でZ係数のzero testを反転し、全実数/非有界/非連結/退化を含む集合をlossless保存。有限gridは全実数tailの証明でない。Independent REF、分散/退化処理・推論受入の未決は`BLOCKED_SCIENCE_REFERENCE_UNRESOLVED`、Agent独断で閾値を選択しない。
- **Ownership:** G01 Registry/GraphVersion/Publisher/Reader、G03 Scientific Coreを二重実装しない。既存Method内の共通計算が新Estimandと一致しない場合は使い回さない。

### 2B. Standalone Operation/Result/Manifest契約
| Operation | 必須Artifact | 禁止・Negative |
|---|---|---|
| DISCOVER | `study.json`・`status.json`・Graph成功なら`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`と理由必須、`schema_dispatch.graph=null`。Backend失敗との混同禁止 |
| IDENTIFY | `study.json`・`status.json`・`identification.json` | Effect `result.json`禁止。非識別もtypedでGraph/Design/Estimand/Proofのhash照合 |
| ESTIMATE | `study.json`・`status.json`・`result.json` | `schema_dispatch.result=e11-local-effect-result/1`。Point無しはnull＋reason、科学PASSと混同禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`・`status.json`・`diagnostics.json` | Effectの再発行禁止、元Effect/Graph/Design hash、seed/適用条件の照合 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）、ただし両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key、実bytes SHA256/size/MediaType/Privacyを網羅。 `request_hash=SHA256(JCS(validated typed Study JSON))`。Manifestに自己hashを格納せず、Markerの`manifest_sha256`にManifest実bytes hashを保存。ReaderはMarker→Manifest→実File→Operation/Profile→上流hashをTrustedRootで検証し、一致しない未コミット/破損データを拒否。Outputは既存G01のStaging→同一FS atomic no-clobber publish、個票bytesはG05独立承認以前に生成禁止。各Methodのpoint/uncertainty/science_acceptance/statusを別軸で保持し、計算成功はScience PASSでない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `TwoSlsAdapter` | `ariadne.scientific.causal_methods.iv.TwoSlsAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `ARConfidenceSet` | `ariadne.causal.inference.confidence_sets.ARConfidenceSet` | Port/Value/Facade integration (no duplicate implementation) | from_components(level,components,evidence) / contains(beta:float) / to_payload()/from_payload(payload) |
| `InferenceEvidence` | `ariadne.causal.inference.contracts.InferenceEvidence` | Port/Value/Facade integration (no duplicate implementation) | validate_for(mode,method) |
| `EffectOutcome` | `ariadne.causal.inference.contracts.EffectOutcome` | Port/Value/Facade integration (no duplicate implementation) | validate_consistency() / to_result_payload() |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。Constructor/Field/公開MethodとARConfidenceSetの境界は本Pxx§3.1以降の埋込Class契約が規範。外部DDはProvenanceのみ、未知のConcrete型を推測しない。

**Responsibility:** Method Adapterを担当するClassは `TwoSlsAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class-level contracts (normative)

Class Fields/Constructor/Method/Pre/Post/Failureは以下で本Package内に定義する。外部DDはprovenanceに限り、Agentが参照しなければ実装できない仕様を残さない。Designed Module≠Source実装済み。ABIはSource照合する。

### 3.1. `TwoSlsAdapter` — full fields/constructor/methods

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.iv.TwoSlsAdapter`。 EstimationのMethod実行Adapter。担当Method：`P3-M10, P3-M11`。**再利用:** 共通IV適格性を再利用、B0/B1識別対象・AR反転を追加。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P3-M10` | B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| `P3-M11` | B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Package内の数理定義とMethod別科学契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P310`（`P3-M10`）、`DD-E11-METH-P311`（`P3-M11`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本Packageの各Method DGP/NEG/REF一覧を優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `ARConfidenceSet` — full fields/constructor/methods

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.confidence_sets.ARConfidenceSet`。Anderson–Rubin反転の損失ない数学集合を表すValue。

#### フィールド

| Field | Type | 制約 |
|---|---|---|
| `confidence_level` | `float` | 0 < level < 1 |
| `components` | `tuple[ExtendedRealInterval,...]` | EMPTYは0件。finite/±∞をtagged endpointsで表現 |
| `topology` | `SetTopology` | EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED |
| `inversion_evidence` | `ContentRef` | 成功した数学的反転の証拠 |

#### Constructor / Factory

`from_components(level,components,evidence)->ARConfidenceSet`：finite endpoint、順序、open/closed、重複/接触区間の数学的正規化。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `from_components(level,components,evidence)` | `ARConfidenceSet` | pure set normalization | invalid endpoint/topology |
| `contains(beta:float)` | `bool` | endpoint条件で判定 | NaN/invalid β |
| `to_payload() / from_payload(payload)` | JSON / Value | Lossless roundtrip | malformed topology / JSON非有限数値 |

#### 処理仕様

Topology分類はEMPTY→ALL_REAL→DISCONNECTED→UNBOUNDED→BOUNDED。ALL_REALは(-∞,+∞)一成分。∞端点はopen、双方openで接触する2区間は1点gapを残すため結合しない。数学的EMPTYは`AVAILABLE + inversion_evidence`と両立、計算失敗`FAILED+reason`とは別。B0/B1 just-identified HC1 ARで`g_A≠0`かつ`Var_HC1(βhat)>0`等の非退化条件が成立する場合`T_AR(βhat)=0`により非空が必要となり、**Method別validator**でEMPTYを拒否。

#### I/O・連携・失敗処理

Valueはpure。JSONのNaN/Infinity数値は禁止、tagged endpointで表現。実AR反転・HC1・coverageはMethod Adapterと独立科学検証に委譲。

#### 検証

`DD-E11-AR01` 5分類、`AR02` generic EMPTYとjust-identified条件分離、`AR03` lossless roundtrip、`AR04` null reason、`AR05` confirmatory fail-closed。FR-202、AR-040、NFR-036。

### 3.3. `InferenceEvidence` — full fields/constructor/methods

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

### 3.4. `EffectOutcome` — full fields/constructor/methods

#### 識別情報・責務

**Class / module:** `ariadne.causal.inference.contracts.EffectOutcome`。点推定・Inference・ScienceAcceptance・lineageを別軸で保持する。Productの既存`ScientificResultDescriptor`へ無検証castしない。

#### フィールド

| Field | Type・制約 |
|---|---|
| `result_id, estimand` | immutable result/target |
| `point_availability, point_value` | finite value または null + reason |
| `inference` | `InferenceEvidence` |
| `science_acceptance` | 推論可用性とは独立した審査状態 |
| `diagnostics` | `tuple[DiagnosticRef,...]`。Method別typed診断参照 |
| `method_evidence, upstream_hashes` | typed Backend evidenceとlineage |

#### Constructor / Factory

Constructor/Factoryはtyped statusと上流lineageを持つEvidenceから生成。不正なEffect/Estimand一致やfalse PASSを拒否。

#### メソッド

| Signature | Return | 処理と副作用 | 例外 |
|---|---|---|---|
| `validate_consistency()` | typed validation result | pure point/CI/science consistency | nonfinite point、null reason欠落 |
| `to_result_payload()` | typed Result payload | pure typed result projection。JCS byte encodingは共通Codec | incompatible schema/estimand |

#### 処理仕様

Pointの存在≠Science PASS。Technical、Identification、Point、Inference、ScienceAcceptanceの状態を混同せず、Method固有estimand/CIを検査。

#### I/O・連携・失敗処理

ValueのI/Oなし。request hashは`SHA256(JCS(validated typed Study JSON))`、Graph内部hash、ContentRef実bytes hash、Manifest bytes hashを分離。Codec`e11-json-jcs-rfc8785/1`、Productの`hash_mapping(default=str)` fallback禁止。

#### 検証

`DD-E11-EFF01` point-only、`EFF02` Science独立、`EFF03` backend mismatch、`EFF04` canonical finite、`EFF05` old Product regression。FR-202、NFR-030/032/036、AR-034/040。

## 4. G08/P03 required scientific and code execution

1. **Preconditions:** G08 Frozen06/07/Pxx、G01/G02 upstream canonical 999、Owner Coding Authorization、fixed candidate Source/lock、Pxx checkpointsを照合。Method/Design/IV assumptions/Estimand/Inference/Backend selectionをpreflightで検証。
2. `P3-M10` B0はQ=[1]、single binary Z/A、just-identified no-adjustment complier LATE。`P3-M11` B1はQ=[1,C]（事前指定covariates C）、single excluded binary Z、single endogenous Aのadditive linear IV structural slope。
3. 2SLSはfirst-stage/reduced form/2nd-stageとinstrument support/partial rankを検証し、推定値のVarianceは採用されたheteroskedasticity-robust methodを使用。通常Wald CIをweak-IV-robustと偽称しない。
4. ARのH0(β)は各βでY−βA ~ Q+ZのZ係数=0をHC1/χ²(1)で検定。残差化と全実数のquadratic inversion/bracketing/無限tail判定を実装し、有限GridだけでALL_REAL/UNBOUNDED/DISCONNECTED/EMPTYを宣言しない。
5. Q Full Rank、HC1 varianceと退化を分離。非退化B0/B1 just-identified（gA≠0, Var_HC1(βhat)>0）ではβhatでAR test=0となり集合は非空。見かけのEMPTYはSCIENCE_INCONSISTENTを疑い、数値失敗やrank不足と数学的EMPTYを混同しない。
6. AR setの`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`と端点Infinity/開閉/Confidence levelをARConfidenceSetがlosslessに保持。Invalid IV仮定はARを実行しただけで検証済みとしない。
7. **Dataflow:** Typed ValidatedMethodRequest→Method Adapter eligibility→selected numeric kernel/effective Backend→EffectOutcome/ARConfidenceSet→G01 StagingSink/Atomic Publisher/Reader。外部Backend model objectやRaw row/SecretsをResultへ含めない。
8. **Typed failure:** Zero denominator, rank/HC1 variance degeneracy, unsupported CI, invalid design, optional backend unavailable, numerical FAILED, legitimate scientific weak IVを明確に区別。Technical exit0はScience PASSでない。

### 設計書の採用済み意味論（独立した本Package実装規範）

以下は30_62/30_63に明文化された数理・Port・互換性の契約をこのPxxへ取り込んだもの。Scopeは本Packageの§3/4に限り、他PackageのClassを再実装しない。

- B0（P3-M09/M10）：単一二値Z/A、無調整、単一内生Aのcomplier LATE。Wald ratioは縮約形Outcome差/First-stage Treatment差。分母0/弱い場合にfinite CIを強制しない。
- B1（P3-M11）：単一二値Z/A、事前指定C、additive linear IV構造の2SLS slope。一般ATE/ATTやB0と同一complier LATEと呼ばない。
- B0/B1の2SLSはfirst-stage/2nd-stage、heteroskedasticity-robust covariance、Instrument support/first-stage diagnosticsを保存。通常Wald区間はweak-IV robustでないことを明示。
- Anderson–Rubin：H0(β)の下で`Y - β A`のZとの関係を（B1では指定Cを条件付けて）検定、反転集合を作る。初期契約は独立観測・単一excluded Z・単一endogenous A・異分散頑健漸近推論の範囲。任意のcluster/HAC版へ自動拡張しない。β探索は有界gridだけではALL_REAL/非有界/非連結を判定できないためtail/bracketing/数値精度を検証。数学的にEMPTYなAR集合は汎用Codecで表現可能。ただし、非退化なB0/B1 just-identified HC1 AR反転では gA≠0、Var_HC1(βhat)>0 の条件からT_AR(βhat)=0で非空性が従う。そこでEMPTYが観測された場合はMethod別SCIENCE_INCONSISTENTとして検査する。first-stage=0、非正分散、rank欠損は別途型付き分岐にし、数値的な失敗と数学的EMPTYを混同しない。
- AR testがIVのexclusion/independence/monotonicityを証明すると解釈しない。CI coverageは独立Simulationで計測する。

**AR具体化（共通Source設計拘束）：** `Q=[1]`（B0）または`Q=[1,C]`（B1）をFull Rankで保持し、各βについて`Y−βA ~ Q+Z`のZ係数=0を**HC1・χ²(1)漸近検定**する方式を対象実装方式とする。残差化・quadratic inversionは全実数で行い、有限gridから非有界・空集合を断定しない。公式の数値/科学受入では独立reference・有効な分散・条件付きIV仮定を評価する。統計量、二次式、退化条件、Negative Matrixは本節のAR定義に従い、Method固有の独立Referenceと照合する。これはB0/B1の科学的な統計量・推論前提を規定するものであり、独立ReferenceとCoverage実測とは別である。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M10` | B0 just-identified LATE | zero controls、single Z/A、robust covariance、AR |
| `P3-M11` | B1 additive linear IV slope | single binary Z/A、predeclared C、robust AR |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**実際のBackend適格性・Config Schemaの未生成・独立OracleやCoverage証跡の不足は、上記Target/数理契約の未決とは区別する。** 実行後のScience判定を未検証のままPASSにしない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M10` B0 just-identified 2SLS／binary Z/A | `DD-E11-METH-P310` | DGP-006, DGP-024; NEG-006, NEG-025 | REF-E07, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M11` B1-A／LINEAR_IV_STRUCTURAL_COEFFICIENT | `DD-E11-METH-P311` | DGP-007, DGP-024; NEG-008, NEG-025 | REF-E08, REF-U01 | AC-D03, AC-P01, AC-P03, AC-P05, AC-A01, AC-A02, AC-A03, AC-A04, AC-A05, AC-I01, AC-I02 | PLAN:G08 / OWNER_TARGET_ACCEPTED_SCIENCE_BLOCKED / NOT_GENERATED |

**Proof boundary:** Method別§5のDGP/NEG/REF/ACは独立検証義務。実数全体のHC1 AR inversion・弱IV退化・LATE/structural slopeの区別は§4で規定。独立Oracleの不在、FWER=.05/K/R/Compute/MC-SE/coverageの未決はBLOCKEDであり、Backend自身の出力や有限GridからScience PASSを作らない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g08/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Deterministic/independent scientific proof matrix

- §5の各Method DGP/NEG/REF/DD/ACを保持。Positive DGPとindependent ReferenceをBackend予測から作らない。
- **Mandatory focused cases:** `P3-M10` B0はQ=[1]、single binary Z/A、just-identified no-adjustment complier LATE。`P3-M11` B1はQ=[1,C]（事前指定covariates C）、single excluded binary Z、single endogenous Aのadditive linear IV structural slope。 2SLSはfirst-stage/reduced form/2nd-stageとinstrument support/partial rankを検証し、推定値のVarianceは採用されたheteroskedasticity-robust methodを使用。通常Wald CIをweak-IV-robustと偽称しない。 ARのH0(β)は各βでY−βA ~ Q+ZのZ係数=0をHC1/χ²(1)で検定。残差化と全実数のquadratic inversion/bracketing/無限tail判定を実装し、有限GridだけでALL_REAL/UNBOUNDED/DISCONNECTED/EMPTYを宣言しない。 Q Full Rank、HC1 varianceと退化を分離。非退化B0/B1 just-identified（gA≠0, Var_HC1(βhat)>0）ではβhatでAR test=0となり集合は非空。見かけのEMPTYはSCIENCE_INCONSISTENTを疑い、数値失敗やrank不足と数学的EMPTYを混同しない。 AR setの`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`と端点Infinity/開閉/Confidence levelをARConfidenceSetがlosslessに保持。Invalid IV仮定はARを実行しただけで検証済みとしない。
- Unit: domain/Estimand/AR set serialization/edge cases; Contract: Class.Method、typed outputs、result discriminator/lineage; Integration: 実Backend、IV instrument/data support、real Publisher/readback、旧Product v2回帰。Weak IV / negative assumptions/HC1 confidence inversionは独立算出Referenceと照合。
- Environment/Backend/API、Source+fixture+lock SHA、DGP/negative、実行Command/Collection、Expected/Observed、Scientific vs Technical outcomeをEvidence化。未確定Oracle/quant K/R/coverageならBLOCKED、Science PASSは出さない。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P04。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-critical standalone gaps

本PackageはClass Field/Constructor/Methodを§3、数理処理順序/分岐を§4、科学的DGP/NEG/REFとAcceptanceを§5〜6で内部定義する。**残課題:** HC1/χ²(1) AR検定反転・全実数集合と退化の分岐は§4および設計書に定義済み。未完了なのは独立数理Reference、数値精度/境界・退化ケースの検証、Pilot coverage判定。 P3-M10/M11で有限gridだけのAR反転を実装することは禁止。OwnerがFreeze時に独立数理/Backend/ConfigとScience受入条件を明示的に判定する。
