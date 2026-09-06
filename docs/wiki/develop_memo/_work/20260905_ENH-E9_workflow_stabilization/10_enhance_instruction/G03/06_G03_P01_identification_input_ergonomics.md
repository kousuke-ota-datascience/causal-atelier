# ENH-E9 G03 P01 — Identification Input Ergonomics

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G03`  
**Package:** `P01`  
**Depends on:** G02 canonical `999_gate_decision = PASS`

## 1. Objective

Identification causal-question inputを、scientific semanticsやGraph/Result lineageを変更せず、Population / Comparatorの意味とTreatment候補を理解して指定できるinteractionへ改善する。

このPackageは新しいcausal-question modelを作らない。既存入力authorityをUIへ正しく投影するusability/conformance修正である。

## 2. Entry criteria

Coding開始前に次を満たすこと。

1. current branchが`bugfix/ariadne_mvp_e9`。
2. working treeがclean。
3. G02 current canonical Trialの`999_gate_decision`がexactly one存在し、`Gate decision: PASS`である。
4. 本P01 contractがexactly one解決され`FROZEN`である。
5. current Trialにformal 08 remediation contractが存在しない。

G02が`READY_FOR_TEST`、Candidate Assembly完了、package completeだけではentryを満たさない。canonical 999 PASSがなければ`BLOCKED_PRECHECK`として実装しない。

## 3. Baseline facts / existing authority

- causal questionはPopulation / Treatment / Comparator / Outcome / Time / Estimand / Decision Use等のexisting semanticsを持つ。
- Treatment候補のauthorityはselected Dataset Versionのschema/column setであり、frontendが候補を捏造しない。
- causal-question serializationとbackend validationはexisting contractをauthorityとする。
- Identificationはselected FIXED Graphをprerequisiteとする。
- Identification Outcomeはuserが独立入力する値ではなく、selected FIXED Graph / GraphVersionのdesignated Outcomeから自動継承される既存protected behaviorである。
- Estimationはselected Identification Result lineageをauthorityとし、Identification UIとは別のOutcome overrideを持たない。

Source/testsは上記を実装するsubstrate調査に利用してよいが、verified source behaviorがこのP01と矛盾する場合はsourceに合わせてcontractをsilent reinterpretせず停止する。

## 4. Required behavior

### 4.1 Population help

Population inputの近傍に、causal questionのtarget populationとして何を記述する項目か理解できるhelp/tooltipを提供する。

helpは単なるlabel反復ではなく、分析対象集団/対象範囲を表すことが分かる内容とする。Populationのfield type/serialization semantics自体は変更しない。

### 4.2 Comparator help

Comparator inputの近傍に、Treatmentに対するcounterfactual/reference conditionを表すことが理解できるhelp/tooltipを提供する。

Comparatorのfield type/serialization/backend validation semanticsは変更しない。

### 4.3 Treatment selector

Treatmentはselected Dataset Version schemaをcandidate authorityとするselectorで選択できる。

Required state behavior:

1. selected Dataset Version/schemaが利用可能なら、そのschemaに存在するcolumnだけを候補にする。
2. schema/data contextが利用不能なら架空candidateを生成せず、明示的unavailable/empty stateとする。
3. existing valid Treatmentがcurrent candidate内にある場合は保持/復元してよい。
4. Dataset Version/schema変更でcurrent Treatmentがcandidateから消えた場合、そのstale valueをsilent保持しない。clear/invalidateしてuserに再選択を要求する。
5. selector操作はTreatment field selectionだけを変更し、Identification executionやEstimationを暗黙実行しない。
6. submit時はexisting causal-question serialization fieldへ同じTreatment valueを渡す。new schema field/versionを作らない。

### 4.4 Identification Outcome

Identification Outcomeはselected FIXED Graphのdesignated Outcomeをread-only表示する。

```text
Discovery designated Outcome
  -> FIXED Graph / GraphVersion designated_outcome_node
  -> Identification Outcome = automatic / read-only / input不要
  -> Identification Result lineage
  -> Estimation
```

Required negative behavior:

- editable select/input/free-textを追加しない。
- Treatment selector実装の都合でOutcomeを独立stateへ分離しない。
- Graph lineageと無関係なfallback Outcomeを作らない。
- Estimation側へ独立Outcome overrideを追加しない。

FIXED Graph/designated Outcomeが利用不能な状態では、架空Outcomeを生成せずexisting prerequisite/error semanticsを維持する。

## 5. Protected invariants

- FIXED Graph prerequisite
- GraphVersion designated Outcome lineage
- Population/Treatment/Comparator/Outcome/Time/Estimand/Decision Useのexisting causal-question semantics
- identification strategy / adjustment set / assumptions
- existing causal-question serialization/backend validation authority
- selected Identification Result → Estimation submission lineage
- E8 Stage responsibility / Navigation Stage != Execution operation
- Result / Execution / Graph identity semantics

## 6. Explicitly forbidden

- independent editable Identification Outcome
- selector-local scientific validationでbackend authorityを置換すること
- new Dataset schema API / new causal-question schema version
- Estimation submission architecture変更
- Graph/FIXED lifecycle変更
- source factから推測して新しいproduct obligationを追加すること
- unrelated cleanup/refactor
- G04/G05 scopeの先行実装

## 7. Implementation substrate hints

Likely responsibility areas（仕様authorityではない）:

- `frontend/index.html`
- `frontend/app.js`
- `frontend/styles.css`
- selected Dataset Version / Analysis Contextを扱うexisting frontend state/API integration
- Identification causal-question serialization周辺
- relevant frontend/product contract tests

実装箇所はcurrent source調査で特定してよい。上記pathへ機械的に限定しない。

## 8. Focused verification — mandatory non-browser cases

Browser E2Eは本Packageでは実行しない。

最低限、deterministic testで次を直接検証する。

1. Population helpが存在し、target populationの意味を説明する。
2. Comparator helpが存在し、counterfactual/reference conditionの意味を説明する。
3. Dataset A schemaではAに存在するcolumnだけがTreatment candidateになる。
4. Dataset/schemaなしでは架空candidateを生成しない。
5. valid existing Treatmentはcurrent schema内なら保持できる。
6. Dataset A → Dataset B変更でBに存在しないTreatmentをsilent保持しない。
7. selector選択後のserialized Treatmentがexisting causal-question field semanticsと一致する。
8. backend validation path/contractを置換していない。
9. selected FIXED Graph designated OutcomeがIdentificationへautomatic/read-only投影される。
10. editable Outcome controlが存在しない。
11. selected Identification Result → Estimation lineage/architectureがregressionしない。
12. touched JS等のsyntax/static checkがPASSする。

Testは実装helperそのものをexpected authorityとして再利用せず、state/input/outputを外側から検証する。

## 9. Completion boundary

`PACKAGE_COMPLETE`は以下をすべて満たす場合のみ。

- §4 required behavior完了
- §5 protected invariantsにregressionなし
- §8 mandatory non-browser verification PASS
- scope外変更なし
- unresolved blockerなし
- package checkpoint SHA記録済み
- canonical package report作成済み

Package completionはG03 PASSではない。P01完了後にCandidate Assemblyを行い、Independent Verificationへ渡すFixed Trial Candidateを確定する。

## 10. Stop / ambiguity rule

次の場合は推測実装せず`PACKAGE_BLOCKED_CONTRACT_AMBIGUITY`または適切なBLOCKEDで停止する。

- selected Dataset Version schemaのcandidate authorityをcurrent interfacesから一意に実装できない
- stale Treatmentのclear/invalidateがexisting serialization/backend contractと矛盾する
- FIXED Graph designated Outcome projectionのsource-of-truthが一意に特定できない
- 本P01を満たすためにnew API/schema/persistence semanticsが必要になる
- Gate claim/Acceptance Criteria変更が必要になる

Gate semantic/AC defectなら09 amendmentへ戻す。Coding Agent自身がGate semanticsを補完・変更しない。
