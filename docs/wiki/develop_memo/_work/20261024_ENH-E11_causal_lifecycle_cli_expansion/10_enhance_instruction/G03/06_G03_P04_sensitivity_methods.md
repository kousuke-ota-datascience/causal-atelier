# ENH-E11 G03 P04 — sensitivity_methods

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G03 / **Package:** P04 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01,P02  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G03_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G03_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** 既存SensitivityAdapter.run公開ABI不変。Adjustment Set妥当性とPropensity Clippingによるtarget変化を保持。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Native推定と4 Refutation・2 Sensitivity・NCE/NCO/RVをEffect lineage付きで実行する。

**科学/Designの必須制約:** 非有意NCE/NCOは無交絡証明ではない。RVは古典OLS限定。P1-M11のScience未確定を黙認しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** 既存SensitivityAdapter.run公開ABI不変。Adjustment Set妥当性とPropensity Clippingによるtarget変化を保持。

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
| `SensitivityAdapter` | `ariadne.scientific.sensitivity.adapter.SensitivityAdapter` | Method Adapter ownership | `run(self, input_: SensitivityInput, output_dir: Path)` → `list[ScientificResultDescriptor]` |
| `DiagnosticPort` | `ariadne.scientific.ports.causal.DiagnosticPort` | Port/Value/Facade integration (no duplicate implementation) | run(self, request:ValidatedDiagnosticRequest, *, sink:StagingArtifactSink) -> DiagnosticOutcome |

**Class/Method signature authority:** 本Pxx §3.1以降の埋込契約がField/Constructor/公開Method/前後条件/失敗時の一次規範。所有するAdapterだけにMethod-specific preflight/executeを実装し、既存`RefutationAdapter`/`SensitivityAdapter`の公開`run` ABIを維持する。統合専用Packageは新Adapterを作らず、Product Scientific Kernelを共有する。

**Responsibility:** Method Adapterを担当するClassは `SensitivityAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Embedded Class contracts — normative here

次のField/Constructor/Method/Pre-Post/FailureはこのPxxの実装Contractを構成する。DDは由来情報に限り、実装Agentへの仕様補完委譲は禁止。実在Source/ABIは開始時に照合し、Designed Classを既存と断定しない。

### 3.1. `SensitivityAdapter` — standalone Class/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.sensitivity.adapter.SensitivityAdapter`。 共通Field/Constructor表はtyped Bridge側の依存候補であり、既存Classに未実装Fieldを既成事実として追加しない。 DiagnosticのMethod実行Adapter。担当Method仕様：`P1-M16, P1-M17`。既存SourceはADJUSTMENT_SETとPROPENSITY_CLIPPINGの実装を持つが、新契約で必要な適格性・実効推論・Codecの再検証は別途必要。**再利用:** 既存SensitivityAdapter.runを維持。必要ならtyped façadeから共有処理を呼ぶ。入口がCLIであることを科学的な別実装の根拠にしない。

#### フィールド

**既存ABI契約:** 現行Classに宣言済みのInstance Fieldはない。MethodDescriptor/BackendFactory/ScientificContextは既存実装の属性ではなく、型付きPortから呼び出す新規Facade／Bridgeの依存として定義する。既存Classへの無断Field追加を前提にしない。

#### Constructor / Factory

**既存ABI契約:** ariadne.scientific.sensitivity.adapter.SensitivityAdapter に明示的`__init__`はない。公開`run(input_, output_dir)`は変更しない。typed Facadeは別Classに配置し、旧ClassのConstructor ABIにDescriptorを注入しない。

#### メソッド

| Signature | Return | Contract |
|---|---|---|
| `run(self, input_: SensitivityInput, output_dir: Path)` | `list[ScientificResultDescriptor]` | **既存v2公開API**。互換維持。typed façadeは既存runを無検証castせず検証済み中間表現へ変換する |

公開Portの`identify/estimate/run`とAdapter Methodは混同しない。FactoryとFacadeは検証済みRequestを渡し、数理・Backend結果を直接Domainへcastしない。

#### 処理仕様

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M16` | adjustment set | Graph/Design/追加変数・post treatment適格性 |
| `P1-M17` | propensity clipping | trim threshold、estimand変化、ESS/sample loss |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本PackageのMethod固有契約に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

既存`run(input_,output_dir)`のPath I/O/DTOはv2専用。Local型付き実行は共通の純粋計算Kernelを抽出する互換Bridgeから再利用し、新Portが旧Path writerを直接呼んでStaging制約を迂回してはならない。旧v2は従来のPath出力、新型付きAdapterは`StagingArtifactSink`だけに書く。旧DTOからの無検証CASTは禁止。Scientific Negativeとtechnical errorを分離。

#### 検証

`DD-E11-METH-P116`（`P1-M16`）、`DD-E11-METH-P117`（`P1-M17`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PackageのMethod別DGP/NEG/REF一覧とFocused Verificationを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `DiagnosticPort` — standalone Class/Method contract

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

## 4. Required execution — method-specific coding order (G03/P04)

1. **Entry/preflight:** G03/G02 upstream canonical 999、Frozen06/07/Pxx、Owner Coding Authorization、Source/lock SHA、依存Pxx checkpointを確認。Method×Operation×Design×Estimand×Inference×Backendをstrictに検証し、失敗時はtyped negativeまたはtechnical errorを返す。
2. 既存`SensitivityAdapter.run(input_,output_dir)`のv2署名・返却を変更せず、DiagnosticPort経由でtyped resultに整合させる。
3. `P1-M16` Adjustment Set SensitivityはGraph/Design上許可された調整集合だけを比較し、post-treatment/colliderの混入を拒否。変更時はEstimandとProofの同一性を再検証。
4. `P1-M17` Propensity Clippingは閾値/有効標本/ESS/target population変化を必ず出力。thresholdを科学的な都合で事後最適化して無条件PASSとしない。
5. **Postconditions:** Adjustmentは許されたGraph-valid setのみ。Clip/Trimは標本とEstimandに影響する。
6. **Publication & compatibility:** Kernel結果をtyped portable Effect/Diagnosticに正規化し、G01のStagingSink/Publisherを使用。自己publish、Resultへのraw model/行データ混入、未承認row export、旧v2 API変更、silent Backend fallbackは禁止。
7. **Error boundaries:** illegitimate negative/unsupported CI, invalid config, numerical nonconvergence, missing dependency, FS/Policy denialを別Status/Reasonとし、Technical SUCCESSからScience PASSを推論しない。

### 設計書で定義済みの科学・型契約（このPxxに展開済みの規範）

以下は30_63の確定記述のうち本Packageに該当する部分を**本文へ複製した実装規則**であり、DDへの外部参照によって補完する規則ではない。担当外Methodの記述がある場合は担当Classを追加実装しない。

- Placebo/Data subset/Random Common Cause/Bootstrapは同一base Effectのhash、変更条件・seed・resampling unitを固定。Refutationの統計的検定と因果識別自体を同一視しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P1-M16` | adjustment set | Graph/Design/追加変数・post treatment適格性 |
| `P1-M17` | propensity clipping | trim threshold、estimand変化、ESS/sample loss |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

**未実測のBackend/Independent Reference/Method固有Schema/定量閾値は上記契約が未定義であることとは異なる。** 採用済みTarget/数理規則をAgent裁量で変更せず、未実測はScience/Freezeの該当判定でBLOCKEDとする。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P1-M16` Adjustment Set Sensitivity／設計変更 | `DD-E11-METH-P116` | DGP-021, DGP-002; NEG-002 | REF-G01, REF-R01 | AC-D01, AC-D02, AC-R02 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P1-M17` Propensity Clipping Sensitivity／tr | `DD-E11-METH-P117` | DGP-002, DGP-023; NEG-010, NEG-018 | REF-E02, REF-R01 | AC-D03, AC-R05 | PLAN:G03 / CONFIG_AND_AC_PENDING / NOT_GENERATED |

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
- **Required test semantics:** 既存`SensitivityAdapter.run(input_,output_dir)`のv2署名・返却を変更せず、DiagnosticPort経由でtyped resultに整合させる。 `P1-M16` Adjustment Set SensitivityはGraph/Design上許可された調整集合だけを比較し、post-treatment/colliderの混入を拒否。変更時はEstimandとProofの同一性を再検証。 `P1-M17` Propensity Clippingは閾値/有効標本/ESS/target population変化を必ず出力。thresholdを科学的な都合で事後最適化して無条件PASSとしない。
- Schema+Method validation（unit）、Class.Port/Result provenance（contract）、実有効Backend/CLI/Publisher/旧v2（integration）を区別。Independent scientific DGP/Oracleは適格な真値から導出し、Estimator自己出力をReferenceにしない。
- Evidenceにsource/lock/fixture SHA、Method/Estimand/Inference、positive+negativeのexpected/observed、実効Backend/API/config/seed、collect済path/command/Resultを残す。Filesystem/科学証拠が未取得ならBLOCKED、期待値緩和によるPASSは禁止。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P06。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Self-contained freeze review boundary

- 本文§3で必要なClassのConstructor・Field・公開Method・処理責務、§4で実装順序/分岐、§5〜6でMethod別のScience/Testを保持する。外部DDやGate06を読ませて不足仕様を推測させない。
- **未確定事項:** 既存SensitivityAdapter Bridgeと各感度分析のestimand保存。 未解決のBackend API、Method Config、DGP/NEG/Reference/quantitative Science、Owner Decisionは該当MethodをBLOCKEDとし、Freeze前に閉じる。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G03/P04 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P1-M16,M17. Scientific constraints: OLS/IPW/AIPW contrast/variance/overlap/cross-fitting、Refutation・NCE/NCO・RV q=1. Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.


## PREP-04.1 owner Method contracts (DRAFT / NOT_FROZEN)

### P1-M16 — strict Method contract (PREP-04.1 DRAFT)
- Operation: SENSITIVITY; target: 10_32 semantic target (not assigned canonical enum); owner: P04. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED candidate_adjustment_sets, design_check_rule_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, graph_evidence_ref, candidate_adjustment_sets plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-021, DGP-002; NEG-002; REF-G01, REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.


### P1-M17 — strict Method contract (PREP-04.1 DRAFT)
- Operation: SENSITIVITY; target: 10_32 semantic target (not assigned canonical enum); owner: P04. Study/Question/Design/Estimand/Graph and content hashes must match.
- Config: REQUIRED clip_lower, clip_upper, diagnostic_spec_ref; strict no unknown keys, no implicit defaults, config={} rejected. Exact type/const/domain constraints in its versioned method_config Schema.
- Question: question_id/research_question/population/analysis_goal/estimand_family/contrast all mandatory, typed, Study-consistent.
- Design: REQUIRED base_effect_hash, propensity_evidence_ref, overlap_assumption_ref plus design_id/question_id/design_kind; explicit roles, assumptions and support validated semantically, never inferred from label. Exact field types in its versioned design_profile Schema.
- Output positive: diagnostics.json; no numeric effect result.json; G01 Publisher/Reader/Manifest/Hash and privacy required. Typed scientific negative can omit positive artifact.
- Inference: requested=false; confidence_level=null; confirmatory requires independently supported method and coverage, else INFERENCE_UNAVAILABLE.
- Independent positive/negative obligations: DGP-002, DGP-023; NEG-010, NEG-018; REF-E02, REF-R01; additionally config omitted/unknown/malformed, operation/target mismatch, upstream-hash mismatch, missing backend, unsupported inference, no silent fallback. SCIENCE DGP/NEG/REF are not generated.
- BLOCKED: actual backend API/version/licence, nuisance/variance algorithm where unsettled, exact K/R/MC-SE/FWER=.05/threshold and oracle. NOT_FROZEN, REGISTRY_NOT_IMPLEMENTED.
