# Ariadne ENH-E5 G04 — P02 Exploratory Handoff and Provenance

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G04`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `APPROVED / FROZEN`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = APPROVED`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

Explore data-selection stateとExploratory Resultをcanonical downstream DRAFTへ安全にhandoffする。

### Exploratory Handoff / Provenance Contract

AnalysisView DRAFTへ移すdata-selection semanticsのみ:

```text
row_filter
selected_columns
derived_columns
missing_value_policy
time_cutoff
sampling
```

chart mark/encoding、panel layout、active widget等presentation-only stateはAnalysisViewへ保存しない。

Public operation:

```http
POST /projects/{project_id}/exploration/results/{result_id}/create-analysis-draft
```

`result_id`はsource Exploratory Resultを表すpath resource identityであり、`source_result_id`をrequest bodyのrequired fieldとして重複させない。

Request body:

```text
target_family: CAUSAL | PREDICTIVE
analysis_mode: EXPLORATORY | CONFIRMATORY
research_context_version_id?   # source lineageから一意に解決できない場合のみrequired
family_spec_schema_version?
family_spec?
```

Rules:

1. `dataset_version_id / analysis_view_id`はsource Result lineageからderiveし、request overrideを受け付けない。
2. ResearchContextVersionはsource lineageから一意ならderive。0件/複数件ならrequestで明示。
3. canonical `AnalysisSpecification`を`status=DRAFT`としてpersist。
4. DRAFTではtarget Family `family_spec`未完成を許容。
5. `Result --MOTIVATED--> AnalysisSpecification` semantic lineageを保存。
6. handoffだけでFIX / Executionを開始しない。
7. `analysis_mode=CONFIRMATORY` + same immutable `dataset_version_id`なら`EXPLORATORY_REUSE_SAME_DATA` non-blocking warningとsource Result evidenceを保持可能にする。


## 2. API boundary

Public handoff operationは`POST /projects/{project_id}/exploration/results/{result_id}/create-analysis-draft`。`result_id`はsource Exploratory Resultを表すpath identityであり、`source_result_id`をbodyへ重複要求しない。request bodyでsource dataset/view identityを上書きさせない。

## 3. Scientific provenance

- same-data判定authorityはimmutable `dataset_version_id`。
- `analysis_mode`をDRAFT/Execution snapshotへ伝播可能にする。
- source Exploratory Result IDをwarning evidenceとして失わない。
- DOM/CSS/panel layoutをscientific provenanceへ含めない。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 5. Package Acceptance Criteria

- exact request semantics。
- context unique/ambiguous derivation。
- DRAFT target family incomplete spec許容。
- `MOTIVATED` edge。
- no auto FIX/Execution。
- confirmatory same-data warning判定に必要なdataが保持される。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
