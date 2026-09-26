# Ariadne ENH-E10 G02 実装指示書 — Predictive Explanation Backend Contract

**Document class:** Primary Execution Contract
**Contract status:** `FROZEN`
**Execution mode:** `WORK_PACKAGE`
**Required packages:** `NOT_MATERIALIZED`
**First executable package:** `NONE`
**Depends on:** `G01 PASS`
**Self-containment:** MUST — this frozen contract is the Gate implementation authority
**Execution eligibility:** **BLOCKED_PREREQUISITE / BLOCKED_PACKAGE_MATERIALIZATION** — requires G01 PASS and materialized required Pxx execution contracts.

- Project: Ariadne
- Enhancement: ENH-E10
- Active Gate: G02
- Gate name: Predictive Explanation Backend Contract
- Branch: `feature/ariadne_mvp_e10`
- Accepted pre-E10 code baseline: `c56a8809dea688380b113210bef12c30b50ca7f6`
- Mutable Control Sheet: N/A

## 1. Gate definition / acceptance claim

### Gate objective

existing `LINEAR_COEFFICIENT_CONTRIBUTION` を保護したまま、model capabilityに基づいてSHAP / LIMEを明示的に選択できるPredictive Explanation backendを成立させる。global/local capability、model-method compatibility、output scale、background/reference data、sampling、reproducibility、provenanceをmethod-specific contractとして扱う。

### Contract claim established by PASS

G02 PASS後、G03は次へ依存してよい。

- explanation method registry/capabilityから、modelに適用可能なmethodを機械可読に解決できる。
- existing coefficient explanationは既存linear modelで引き続き利用できる。
- SHAPはfrozen contractで定義されたmodel/taskに対しglobal/local explanationを生成できる。
- LIMEはfrozen contractで定義されたmodel/taskに対しlocal explanationを生成でき、global非対応をcapabilityとして明示する。
- unsupported model-method combinationとoptional dependency absenceは明示errorとなり、coefficient/他methodへのsilent fallbackはない。
- explanation artifact/resultはmethod、model identity、feature identity、sample identity、output scale、background/reference、seed、library version等のprovenanceを再構成可能にする。
- Predictive Explanationをcausal explanation / treatment effectとして表現しない。

### Why this is one Gate

SHAP/LIMEの価値は個々のlibrary wrapperではなく、model-method compatibility、global/local capability、method-specific semantics、artifact/provenanceを共通Explanation contractの下で扱えることにあるため、一つのacceptance boundaryとする。

## 2. Effective current context

Accepted baselineでは以下を確認済み。

- `explanation_runner.py` は `SUPPORTED_EXPLANATION_METHOD = "LINEAR_COEFFICIENT_CONTRIBUTION"`。
- unsupported methodではapproximate fallbackせず `NOT_APPLICABLE` + `EXPLANATION_METHOD_NOT_APPLICABLE` を返す。
- explanation datasetとmodelの `feature_order` mismatchを拒否する。
- coefficient global explanationはcoefficient/absolute coefficient、local explanationはfeature value × coefficientを出力する。
- binary modelのcoefficient explanation `model_output_scale` は `LOG_ODDS`、prediction outputは `PROBABILITY`。
- Predictive Explanation result/artifactとModel Cardは既に存在し、predictive-not-causal diagnostics/limitationsを保持する。
- `explanation_dataset` はTEST partition由来で `explanation_only=True` として分離されている。
- SHAP/LIMEはbaseline dependencyに存在しない。

## 3. Frozen execution-precondition decisions — MUST resolve by explicit amendment before coding

1. explanation capability interface / registry entry schema
2. model × method compatibility matrix
3. SHAP supported model/task set
4. SHAP global/local definition
5. Binary Classification SHAP output scale
6. expected value / base value / additivity informationのschema
7. background/reference dataset selectionとprovenance
8. SHAP sampling policyとdeterministic behavior
9. LIME local-onlyを正式contractとするか
10. LIME discretization / kernel / sample size / feature representation defaults
11. LIME seed/reproducibility guarantee
12. optional dependency group/version bounds for SHAP/LIME
13. explanation result/artifact schema revision要否
14. model cardへのexplanation provenance格納範囲
15. failure taxonomy: method unavailable / not compatible / not supported / computation failure

本書は `FROZEN`。未確定preconditionの具体化はexplicit amendmentで行い、execution開始後のsilent contract rewriteは禁止。

## 4. Expected execution-mode decomposition

`WORK_PACKAGE` を第一候補とする。

- explanation capability/compatibility registry
- SHAP adapter + global/local result normalization
- LIME adapter + local result normalization
- explanation artifact/provenance + protected coefficient regression

P00/PxxはArchitecture Review後に作る。

## 5. Required implementation semantics

1. **Capability-driven selection**
   - methodはstring branchの積み増しではなく、model capabilityとの互換性を明示できるregistry/capability contractから解決する。
   - capability metadataは少なくともmethod identity/version、global/local support、required model interface、dependency availabilityを表現する。
   - G01 model registryとのauthority重複を避け、model-side capabilitiesとexplanation-side method requirementsを明示的に照合する。

2. **Existing coefficient explanation**
   - existing linear model behaviorを保護する。
   - model output scale / prediction scale / feature-order semanticsを維持する。
   - G02導入を理由にcoefficient pathへSHAP/LIME semanticsを混ぜない。

3. **SHAP**
   - globalとlocalを同じraw outputの単純表示違いとして扱わず、それぞれのmeaning/provenanceを明示する。
   - frozen output scale、base/expected value、feature contributions、background/reference data、selected sample identityをresult/artifactへ記録する。
   - classification/regressionのoutput shape差をnormalization layerで明示的に扱う。
   - unsupported shape/task/modelをsilent coercionしない。

4. **LIME**
   - local explanationをinstance-specific artifact/resultとして扱う。
   - local sample/instance identity、feature representation、effective seed、method parametersを記録する。
   - global explanation非対応を採用する場合、capability metadataとvalidationで明示し、global風の擬似aggregateを自動生成しない。

5. **Optional dependency**
   - SHAP/LIME未導入でAriadne core/G01 model flowを壊さない。
   - selected methodのdependency unavailable時はexplicit capability error。
   - package/version availabilityをcapability/provenanceへ露出する。

6. **Isolation / terminology**
   - explanation用dataはmodel selection/trainingへ逆流させない。
   - TEST isolationを維持し、explanation executionがTESTを再学習へ使用しない。
   - `Predictive Explanation is not a Causal Explanation or Treatment Effect.` 相当のsemantic boundaryを維持する。

## 6. Allowed scope

- predictive explanation capability / method registry
- SHAP/LIME adapters
- global/local explanation normalization
- compatibility validation
- explanation artifact/result/model-card provenance
- optional dependency capability discovery
- G02に必要なdomain/API contract
- G02 tests

## 7. Explicitly prohibited scope

- G01 model backend semanticsの再設計
- G03 product UIの本格統合
- causal explanation / treatment effect / CATE / HTE interpretation
- explanation値をfeature causal importanceと表記
- automatic method fallback
- global LIME風pseudo-summaryをcontractなしに追加
- repository-wide test migration
- unrelated Project/Causal/Graph changes

## 8. Protected passed-Gate/upstream contracts

| Source | Protected semantic | Mandatory regression |
|---|---|---|
| G01 | model registry, artifact/load/predict, optional dependency and provenance contract | G01 protected regression |
| baseline | coefficient explanation semantics | coefficient global/local regression |
| baseline | feature-order validation | mismatch rejection |
| baseline | TEST explanation isolation | no training/selection feedback |
| baseline | predictive-not-causal terminology | result/model-card assertions |

## 9. Schema / API / runtime policy

- existing `predictive-explanation-result/1` / artifact schemaをreuseするかversion-upするかはfreeze decisionとする。
- provider-specific raw SHAP/LIME objectをpublic Result payloadへ無加工で露出しない。canonical normalized structureとprovider provenanceを分離する。
- arbitrary pickled explainerをdurable contractへ混入させる場合はsecurity/portability/versioningを明示reviewし、暗黙導入しない。
- explanation computation failureをmodel training failureへ読み替えない。

## 10. Automated test obligations

新規/materially rebuilt testは `tests/enhancement/enh_e10/g02/<layer>/` を原則とする。

最低限:

- existing coefficient global/local protected regression
- SHAP binary global/local
- SHAP regression global/local
- SHAP frozen output-scale/base-value contract
- SHAP feature contribution shape/name mapping
- LIME binary local fixed-seed reproducibility
- LIME regression local fixed-seed reproducibility
- LIME global unsupported contract（採用時）
- model-method compatibility reject cases
- optional SHAP/LIME dependency unavailable
- feature/sample identity provenance
- background/reference provenance
- TEST isolation
- predictive-not-causal terminology
- Model Card explanation metadata

Browser E2EはG02でblockingにしない。method-specific scientific semanticsはdeterministic Unit/Contract/Integrationをprimary proofとする。

## 11. Candidate Assembly requirement

`READY_FOR_TEST` 前に:

- required packages complete
- G02-wide compatibility matrix self-check complete
- coefficient protected regression complete
- SHAP/LIME optional-dependency absence scenarios complete
- G01 protected regression complete
- unresolved candidate-affecting change = NONE
- Fixed Trial Candidate SHA fixed
- Completion Report created

## 12. Coding Agent prohibited work

- Acceptance Criteria変更
- G01 contractのsilent rewrite
- G03 UI先行実装
- test回避のためのmethod semantics変更
- unsupported methodをfallbackで成功扱い
- causal wordingの追加
- repo-wide test cleanup
- Gate PASS declaration

## 13. Required outputs after execution

- package status/checkpoint reports（WORK_PACKAGE時）
- Fixed Trial Candidate SHA
- implementation completion report
- model-method compatibility evidence
- explanation provenance evidence

## 14. Stop condition

本書は `FROZEN` である。ただしRequired Pxx未materializeまたはupstream prerequisite未達なら `BLOCKED_*`。Coding sideは `READY_FOR_TEST` または明示的 `BLOCKED_*` で停止し、PASSを宣言しない。
