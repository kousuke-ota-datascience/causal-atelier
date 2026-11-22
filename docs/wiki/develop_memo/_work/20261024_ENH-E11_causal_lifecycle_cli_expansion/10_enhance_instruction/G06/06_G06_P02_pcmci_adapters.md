# ENH-E11 G06 P02 — pcmci_adapters

**Document class:** Primary Execution Contract (self-contained Review DRAFT)  
**Gate:** G06 / **Package:** P02 / **Trial:** NOT_STARTED  
**Depends on Pxx:** P01  
**Status:** DRAFT / NOT_FROZEN / CODING_NOT_AUTHORIZED  
**Parent06:** `06_Ariadne_ENH-E11_G06_implementation_instruction.md` (traceability only)  
**Plan P00:** `06_G06_P00_work_package_plan.md` (traceability only)

## 1. Assigned Purpose / Authority

**目的:** Tigramite lazy import、effective API、PCMCI+/LPCMCI endpoint/latent/lag、DGP oracle。

**Scope:** 本PackageのClass/Methodと、それらが必要とする契約/適格性/Result Evidenceに限定。**Gate全体の保護意味:** Temporal Graphのlag/endpoint不確実性を保持しPCMCI系をMethod別に実行する。

**科学/Designの必須制約:** time index/lag sign、contemporaneous/latentと独立Graph oracle必須。PAGをDAGへ勝手に変換しない。

Assigned Coding AgentのnormativeなCoding責務は**本Pxx**。別Packageや未FreezeのGate07で自分のScopeを拡張せず、当該Gateの06/P00/07は追跡・独立Acceptanceの役割と区別。Working SourceのClass存在とSignatureを確認し、設計上の存在を実装済みと誤認しない。

## 2. Effective Common Contract (Self-contained)

- PREP-02の共通F03/F04/F05/F06/F07は適用基準。JCS RFC8785、Source/Graph/ContentRef/Manifestの異なるhash domain、atomic no-clobber、Trusted Root/independent privacy、typed scientific statusを損なわない。
- 旧Product `causal-analysis-spec/2`、`ScientificCorePort.run_*`、Web/API/Worker/DB、旧CLI、既存Refutation/Sensitivity `run`の公開ABIを変更しない。CLIだけの新Scientific Kernel、別MethodRegistry、別GraphVersion writer、別Publisherを作らない。
- Scientific `Identification/Point/Inference/ScienceAcceptance`とTechnical outcomeは別軸。不適格なMethod、無識別、Unsupported CI、missing optional Backendは型付き負結果またはTechnical error。未実行をPASS、point-onlyをCI有り、Backend自身の出力を独立Oracleにしない。
- `LocalCausalUseCase`はstrict ValidatedStudyから各Portへ委譲し、Fileはstaging→atomic Publisher→independent readback。G05のPolicy認可前は個票禁止。

**This package rules:** Tigramite lazy import、effective API、PCMCI+/LPCMCI endpoint/latent/lag、DGP oracle。

### 2A. 既存Discovery ABIとTemporal Kernel境界（`2cf28f59a324`）
- **既存:** `src/ariadne/scientific/discovery/adapter.py`の`DiscoveryAdapter.run(self, input_: DiscoveryInput, output_dir: Path) -> list[ScientificResultDescriptor]`と`src/ariadne/scientific/core_adapter.py`の`ScientificCoreAdapter.run_discovery(self, input_: DiscoveryInput, output_dir: Path)`は公開Product Path API。E11 `DiscoveryPort.discover(self, request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome`とは入力・出力・Publication契約が異なる。変更・無検証Cast・旧Path writerの直接利用は禁止。
- **新規境界:** Tigramite PCMCI/PCMCI+/LPCMCIの実効API・CI test・Temporal endpointとlag sign/時刻原点をMethod別に検証。既存DiscoveryAdapterの存在だけをTigramite Method実装済み証拠としない。Design-only TemporalGraphEvidenceとTyped Portは§3で所有Class/方法を確定し、G01 GraphVersionService/Publisher/MethodRegistryを複製せず共有する。lag/time index、latent marks、CI kernelが不明なら`BLOCKED_CONTRACT_AMBIGUITY`。

### 2B. Operation別Artifact/Schema契約（このPackage本文が実装規範）
| Operation | 必須Artifact | 禁止・negative条件 |
|---|---|---|
| DISCOVER | `study.json`, `status.json`, Graph成功時`graph.json` | `result.json`禁止。科学的Graph無しは`diagnostics.json`＋nonempty reason、`schema_dispatch.graph=null`。Backend失敗との混同は禁止 |
| IDENTIFY | `study.json`, `status.json`, `identification.json` | Effect `result.json`禁止。識別negativeもtyped、Graph/Design/Estimand/Proof hashを照合 |
| ESTIMATE | `study.json`, `status.json`, `result.json` | `schema_dispatch.result=e11-local-effect-result/1`。point欠落はnull＋理由で表し、非識別への推定値偽装禁止 |
| REFUTE/SENSITIVITY/DIAGNOSE | `study.json`, `status.json`, `diagnostics.json` | Effect再発行禁止。上流Effect/Graph/Design hash、seed・適用条件の検証が必須 |

全Operationに`manifest.json`（`e11-local-manifest/1`）と`_COMMITTED.json`（`e11-commit/1`）を置くが、両者はArtifact Inventory外。Inventoryは実Fileの相対POSIX key・size bytes・SHA256・MediaType・Privacyを列挙。`request_hash=SHA256(JCS(validated typed Study JSON))`、Manifestに自己hashを入れずMarkerがManifestの実bytes SHA256を保持。Readerはmarker→manifest→artifact→Operation Profile→upstream hashをTrustedRoot内で検証。staging→atomic no-clobber publishを既存G01 Publisherで行い、Row Parquetは独立承認証拠の検証前にbytes生成すら禁止。Publication不正・欠損をScience negativeに変換しない。

## 3. Class Placement, Signature, Reuse, Dependency Direction

| Class/Port | Designed module (DD30_61〜63) | Ownership boundary | Exact approved/design signature |
|---|---|---|---|
| `TigramiteTemporalAdapter` | `ariadne.scientific.causal_methods.temporal.TigramiteTemporalAdapter` | Method Adapter ownership | `preflight(self, request: ValidatedMethodRequest)` → `EligibilityOutcome`; `execute(self, request: ValidatedMethodRequest, *, sink: StagingArtifactSink)` → `TypedScientificOutcome` |
| `DiscoveryPort` | `ariadne.scientific.ports.causal.DiscoveryPort` | Port/Value/Facade integration (no duplicate implementation) | discover(self, request:ValidatedDiscoveryRequest, *, sink:StagingArtifactSink) -> DiscoveryGraphOutcome |

**Method Adapter signature policy:** 新Adapterは原則`preflight(self,request:ValidatedMethodRequest)->EligibilityOutcome`／`execute(self,request:ValidatedMethodRequest,*,sink:StagingArtifactSink)->TypedScientificOutcome`。上表で指定された既存`run(self,input_,output_dir)`はその署名を保持。PortはApplication→Scientific kernelへ向かい、CLI Layerに別の科学数値実装を作らない。本Pxx§3.1以降のClass定義がField/Constructor/Methodの規範であり、外部DDはprovenanceのみ。Design未確定箇所や実Backend ABIを補完せずBLOCKEDで停止する。

**Responsibility:** Method Adapterを担当するClassは `TigramiteTemporalAdapter`。 Values/Portsの使い回しとNew Methodの科学Algorithm実装の区別を守る。他Package担当Classに対する変更が必要なら契約修正を申請する。

### 3. Standalone Class/Method contracts

以下をNormative Contractとして本Pxxに展開する。DDはProvenanceのみ、別06/07はCodingの不足判断を補完するSourceにしない。Class存在とLegacy ABIは実Sourceで確認し、設計Classと混同しない。

### 3.1. `TigramiteTemporalAdapter` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Class/Module:** `ariadne.scientific.causal_methods.temporal.TigramiteTemporalAdapter`。 Graph DiscoveryのMethod実行Adapter。担当Method：`P3-M01, P3-M02, P3-M03`。**再利用:** 既存Graph endpoint意味とlag規約の共通Validatorを再利用。入口がCLIであることを科学的な別実装の根拠にしない。

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
| `P3-M01` | PCMCI | CI test/lag window、time-series order、graph |
| `P3-M02` | PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| `P3-M03` | LPCMCI | PAG/latent/endpoint fidelity、lag |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本Pxx固有のMethod/Science contractに保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

#### I/O・連携・失敗処理

Backend importはMethod load時だけ。AdapterはResult/Graph/Diagnosticsをtyped evidenceとして返し、File書込みは`StagingArtifactSink`へ限定。旧`ScientificCoreAdapter`経路との共通計算、Model Object不露出、version/API/seed/fold provenanceを検証する。

#### 検証

`DD-E11-METH-P301`（`P3-M01`）、`DD-E11-METH-P302`（`P3-M02`）、`DD-E11-METH-P303`（`P3-M03`） に対応するpositive DGP、invalid config/Method、Method固有negative、独立Scientific Reference、Regression/Codec testを要求する。IDの正式照合には本PxxのMethod別DGP/NEG/REF/AC obligationsを優先し、この7区分の記載だけで科学的PASSとはしない。

### 3.2. `DiscoveryPort` — inline Field/Constructor/Method contract

#### 識別情報・責務

**Protocol配置：** `ariadne.scientific.ports.causal.DiscoveryPort`。PAG/CPDAG等の科学的Graph Discovery実行を型付きで抽象化する。既存Productの`ScientificCorePort.run_discovery(input_,output_dir)`は旧APIとして維持し、共通純粋Scientific Kernelへの互換Bridgeを通す。

#### フィールド

N/A：Protocol自身のInstance Fieldは持たない。

#### Constructor / Factory

N/A：具体Adapterは同一Method RegistryのCapabilityとFactoryから構築し、選択済Method/Backendに対してのみ実行する。

#### メソッド

```python
class DiscoveryPort(Protocol):
    def discover(self, request: ValidatedDiscoveryRequest, *, sink: StagingArtifactSink) -> DiscoveryGraphOutcome: ...
```

#### 処理仕様

`ValidatedDiscoveryRequest`はVerified Study/Question/Design/Dataset、選択済`BackendCapabilityRecord`、CI適格性、seedとInput Hashを保持する。Graph生成成功か、理由付き科学的negativeのいずれかを`DiscoveryGraphOutcome`で返す。P1-M06では`FciDiscoveryAdapter.preflight/execute`へ委譲する。Backend例外・schema不正を科学的negativeへ変換しない。

#### I/O・連携・失敗処理

Graph/DiagnosticsのFile出力先は`StagingArtifactSink`のみ。Product GraphVersion writer、DB/UoW、旧`Path`直接書込はこのPortの責務にしない。

#### 検証

`DD-E11-DISC01`：Registry→Port→Adapterの正例と異Method不一致拒否。`DISC02`：Graph成功と科学的negativeの排他性・dummy Effect禁止。`DISC03`：Staging限定と旧Product run_discovery署名回帰。独立PAG Science Oracleは`DD-E11-METH-P106`の責務。

## 4. Required implementation steps — G06/P02

1. **Entry:** Current G06のFrozen06/07/Pxx、Owner Coding Authorization、Source/lock full SHA、当該06のupstream 999とPxx依存Checkpointを確認してから実装。Valid Study/Method/Design/Data/Estimand/Backendを境界で検証。
2. `P3-M01` PCMCIはCI test family/positive lag/window/data measurement適格性を確認し、time series index・missing/noisy/constant observationsを無断補完しない。
3. `P3-M02` PCMCI+はcontemporaneous endpoint/CPDAG-like uncertainty、`P3-M03` LPCMCIはlatent/PAG endpointをlosslessに保持。Model出力のEdge markを既知真DAGで上書きしない。
4. Tigramite実効distribution/API/return object/symbolic endpointをlazy-loadでProbeし、列名/lag sign/Edge endpoint mappingをDataset順序に照合。invalid CIやMethod switchへのfallbackは禁止。
5. 独立Temporal Graph OracleはDGP-009〜011とNEG-021/028/REF-G02/G03に対応し、Backend自己出力を正解としない。
6. **I/O/Failure:** Approved Method Adapter preflight→selected Backend（必要時lazy import）→typed Scientific Outcome→G01 Staging Publisher/Reader。Invalid config、合法的Scientific negative、不確定CI、Backend failureを分離し、Resultにeffective Method/Backend/Seed/Time/Design Evidenceを保存。
7. **Non-goals:** 旧v2 Public ABI、Web/API/DB/Worker、G01 GraphVersion/Publisherの再実装、未承認row export、Backend実測なしのScience PASSを禁止。

### 設計で定義済みのGraph／Quasi意味論（自己完結した実装規範）

以下は既存の詳細設計に記載された規則を本Packageへ直接展開したもの。Designの決定済み部分を不明事項としてAgentに再判断させない。実効Backend/API probe、独立Graph/Counterfactual Oracle、推論可用性の未実測は別にBLOCKEDとする。

- FCIはPAG circle、bidirected、ambiguous orientationを保持し、そこからDAGを想像してpoint estimateへ通さない。
- PCMCI/PCMCI+/LPCMCIはCI test family、max lag、contemporaneous link、endpoint mark、時間方向規約をserializeする。MetaDataの `lag=-1` 等は明示Convention無しには意味を持たせない。
- GraphOracleは構造上の同値類／可識別方向／adjacency・endpointを比較し、学習したGraphの不確定な向きを真DAGへ罰則無しに変換しない。

| Method ID | 科学的対象 | Method固有のpreflight・Result契約 |
|---|---|---|
| `P3-M01` | PCMCI | CI test/lag window、time-series order、graph |
| `P3-M02` | PCMCI+ | contemporaneous endpoint、CPDAG-like oracle |
| `P3-M03` | LPCMCI | PAG/latent/endpoint fidelity、lag |

Method別の定量的仮定・CI/AR/Graph/Negative Controlの意味と受入条件は本書§4〜§7に保持する。Method display nameからATE/ATT/LATE/CATE等を推測しない。

## 5. Method-by-Method DGP/Negative/Reference Obligations

| Method | DD ID | Positive/Negative | Independent Reference | AC | 10_32 Readiness |
|---|---|---|---|---|---|
| `P3-M01` PCMCI／time-lagged graph | `DD-E11-METH-P301` | DGP-009; NEG-021 | REF-G03 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G05 | PLAN:G06 / CONFIG_AND_AC_PENDING / NOT_GENERATED |
| `P3-M02` PCMCI+／time-series CPDAG | `DD-E11-METH-P302` | DGP-009, DGP-010; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |
| `P3-M03` LPCMCI／time-series PAG | `DD-E11-METH-P303` | DGP-011; NEG-021, NEG-028 | REF-G03, REF-G02 | AC-D01, AC-G01, AC-G02, AC-G03, AC-G04, AC-G06 | PLAN:G06 / OWNER_ORACLE_PRINCIPLE_ACCEPTED_ORACLE_BLOCKED / NOT_GENERATED |

**Proof boundary:** §5のDGP/NEG/REF/ACは独立に実証すべき義務であり、Fixture/Oracleの実在やPASSを意味しない。Backend出力を自己正解にせず、時系列Graph/Quasi Methodごとの独立Referenceと実測で検証する。FWER=.05/K/R/CI coverage/MC-SE未確定はBLOCKED。外部資料から推測して決めない。

## 6. Focused Verification Contract — WHAT, not physical filename

| Layer | Required behavior |
|---|---|
| unit | Value/Estimand/Method schema、negative、Hash/Status/No-False-PASS、pure Algorithm。 |
| contract | `Class.Method`入出力、Port/Backend Registry選択、typed evidence/Lineage、Version+Codec。 |
| integration | 必要な実Backend/CLI/FS/Atomic readback、optional Profile、既存Product v2回帰。 |
| scientific evidence | Method別DGP/NEG/independent reference、定量Simulation/coverage/MC-SE。 |

TestはLifecycle（enhancement/regression/characterization/benchmark/support/legacy）とLayer（unit/contract/integration/frontend/browser_e2e）を独立分類。新規は`tests/enhancement/enh_e11/g06/<layer>/`に原則配置、実Path/command/pytest collectionは40 Operatorがcurrent checkoutからdiscover。受入07をpathの文字列で置き換えない。Mock-onlyでreal Backend/FS/ScienceをPASSにしない。

### 6.1. Method-specific independent verification obligations

- §5のDGP/NEG/REF/DD IDを、Science/Status/Method-config/Source-hashに対応させる。ID一覧はFixture実在や科学的PASSの証拠ではない。
- **Positive and negative matrix:** `P3-M01` PCMCIはCI test family/positive lag/window/data measurement適格性を確認し、time series index・missing/noisy/constant observationsを無断補完しない。 `P3-M02` PCMCI+はcontemporaneous endpoint/CPDAG-like uncertainty、`P3-M03` LPCMCIはlatent/PAG endpointをlosslessに保持。Model出力のEdge markを既知真DAGで上書きしない。 Tigramite実効distribution/API/return object/symbolic endpointをlazy-loadでProbeし、列名/lag sign/Edge endpoint mappingをDataset順序に照合。invalid CIやMethod switchへのfallbackは禁止。 独立Temporal Graph OracleはDGP-009〜011とNEG-021/028/REF-G02/G03に対応し、Backend自己出力を正解としない。
- Pure Value/Graph/Design→unit、Port/Codec/typed Reason→contract、実Backend/Tigramite/Quasi/CLI/Pub-Readback/legacy v2→integration。科学Graph/EffectのReferenceはBackend出力とは別に事前固定する。
- Effective backend API/version, Test fixture/Source/lock SHA, seed, Data/Time ordering, CI/SE handling, observed outcome, actual test collection/command, FAIL/BLOCKED causeをEvidenceへ記録。必須RuntimeやOracleが未確定ならBLOCKED。

## 7. Checkpoint / Handoff / Stop

**Package Done:** 実SourceのClass/Method追加・Reuse・正例/負例/typed result/被影響Product Regression、focused test actual command/result、DD/Method coverage、Diff/Checkpoint full SHA、20 Package Status Reportを完備。科学的実測が未完ならScience PASSと報告しない。

**Next:** P03。Pxx完了をGate 999 PASSにしない。

**STOP:** 本文はまとめReview前のDRAFT。担当Pxx/06/07のFreeze、上流canonical Gate PASS、実行SHA、当該PxxのOptional Backend/Privacy/Design gap、Owner Coding Authorizationのいずれか欠ける場合は実装開始禁止（`BLOCKED_CONTRACT_AMBIGUITY`等、具体原因をEvidence化）。本Pxxの依存契約・科学的Referenceが未解決なら当該ScopeだけをBLOCKEDとする。他Gateの未決を全Packageの一律停止条件にせず、Agentによる推測補完を禁止する。


## 8. Freeze-only review: unresolved decisions

**Self-contained:** §3は全ClassのField/Constructor/Public Method/I-Oを、§4は実装分岐を、§5〜6は必要なMethod/DGP/NEG/REFと検証を本文で保持する。**BLOCKED before Freeze:** Tigramite実効API・independent Temporal Oracle・Method別CI/lag boundariesの確定。 他文書の参照をCoding Agentに必須とせず、設計空白はOwner決定まで止める。

## 9. OD-05 Owner-adopted Method Profile construction obligation

**Accepted authoring allocation (2026-11-19 JST):** G06/P02 is responsible for strict versioned Config/Question/Design/Output/Inference Profile authoring/registration for P3-M01–M03. Scientific constraints: CI-test/temporal lag/zero-lag/PCMCI+/LPCMCI endpoint, latent uncertainty. Retain the existing §§3–6 Class/Method/algorithm/DGP/NEG/REF/AC semantics. A profile must declare mandatory and conditional fields, type domains, effective Backend/API/Version, analysis_mode/inference eligibility, output status/artifact shape, and no implicit Backend defaults.

**Negative obligations:** unsupported method/profile/estimand, unknown fields, missing conditional fields, invalid Graph/Design/Question/DataRef identity, unavailable optional Backend, unsupported CI or invalid scientific assumptions are typed rejections; missing specific profile ⇒ `METHOD_PROFILE_UNAVAILABLE`. No silent fallback or `config={}` as a claim of support.

**Readiness:** This Owner decision allocates work; it does not assert that schemas, independent DGP/REF, Backend execution, K/R/MC-SE/coverage, Gate07/999, contract Freeze or Coding Authorization are complete. No new mathematical Target is adopted here.


## PREP-04.1 embedded Method contracts (DRAFT)

### P3-M01 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-009; NEG-021; REF-G03. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P3-M02 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha, contemporaneous_rules_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-009, DGP-010; NEG-021, NEG-028; REF-G03, REF-G02. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


### P3-M03 — strict Method contract (PREP-04.1 DRAFT / NOT_FROZEN)
- Method scope: DISCOVER / 10_32 semantic target (not assigned canonical enum); Pxx=P02; preserve 10_32 scientific target, do not cast alternative estimands.
- Config mandatory fields: ci_test_spec_ref, tau_min, tau_max, alpha, latent_assumptions_ref; versioned method_config Schema restricts type/const/range and extra keys, config={} is rejected, no backend defaults.
- Question mandatory: question_id/research_question/population/analysis_goal/estimand_family/contrast; Study target and references cross-validated.
- Design mandatory: design_id/question_id/design_kind plus time_index, sampling_unit, observed_variables, temporal_ordering_ref, lag_convention_ref, endpoint_convention_ref; validated data columns, roles, dataset support and assumption/Graph/temporal provenance. Declarations are not proof of causal truth. Exact types enforced by dedicated design_profile Schema.
- Positive output: graph.json/e11-local-graph/1, no result.json; status/marker/manifest and Reader hash/readback required; negative science typed and no fictitious positive.
- Inference: requested=false, confidence_level=null. CONFIRMATORY is not granted by schema syntax.
- Independent AC: DGP-011; NEG-021, NEG-028; REF-G03, REF-G02. Negative matrix includes empty/unknown/malformed config, wrong operation/target, missing/mismatched upstream hash, unsupported CI, unavailable backend and Method-specific NEG. Real backend and independent DGP/REF/K/R/MC-SE/FWER 0.05 remain NOT_VERIFIED.


## S02簡素化・G06 Temporal GraphとMethod Profileの規範

担当Methodは`P3-M01` PCMCI、`P3-M02` PCMCI+、`P3-M03` LPCMCIの3件。5 Profile kind（method_config/question_profile/design_profile/output_profile/inference_profile）は`23_api_interface_design/schema_drafts/method_profiles/factored/e11_<kind>_factored_v1.json`のshared core＋exact Method ID overlayから再構成し、Dispatch Registry/200 Schema標準Draft202012/正負例/parityの確認が不足すれば`METHOD_PROFILE_UNAVAILABLE`でfail-closed。科学的契約は各Methodで異なり、time-lag端点の向き/ラグ0、PAG/CPDAG同値類、潜在交絡・CIテストの意味を厳格保存し、グラフ方向を自動確定しない。ENV-TIGRAMITEの実効Python3.12 APIと独立時系列Graph Oracleの実測は後続検証事項。

新Local Graphは内容hashとsource/parent科学由来を保持するがProduct GraphVersion DBはlookup/edit/write/FIXしない。`version_id=parent_version_id=null`のみ提供し、non-null importは未対応として拒否。共通`LocalRunContext(root,principal)`、`LocalPrivacyPolicyPort.authorize(*,study,root,principal,output_shape)`を利用し、署名Verifier/Policy Anchorと追加CLI flagを作らない。G06は個票を直接公開せず、旧Product v2のABIと共通Kernelを保護する。独立Testは時系列順序・PAG/CPDAG同値類・Graph hash/Manifest/readback・wrong Method/unsupported CIの負例を確認する。未実測をScience PASSとしない。
