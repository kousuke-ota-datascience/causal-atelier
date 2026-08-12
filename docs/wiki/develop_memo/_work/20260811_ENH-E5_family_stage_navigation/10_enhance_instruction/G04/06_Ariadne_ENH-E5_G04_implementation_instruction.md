# Ariadne ENH-E5 G04 — Exploratory Family Recomposition — Gate Integration

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G04`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `acc43f744360e25fc504f608716bed2023817a29`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 06 integration contract`
- Execution Mode: `WORK_PACKAGE`

## 0. Authority / execution isolation

- 本文書は`WORK_PACKAGE` Gate全体の**Operator / Gate Orchestrator向けintegration contract**である。
- Package Coding Agentへ本`06`をnormative sourceとして渡してはならない。Package Coding Agentの唯一のnormative implementation contractはassigned `Pxx` 1文書である。
- Gate Orchestratorはpackage分割、統合candidate、Gate-level protected invariant、completion evidenceの管理に本書を使用する。
- Package Coding Agentがassigned `Pxx`だけで実装を一意に決定できない場合は、他文書を読ませず`BLOCKED_CONTRACT_AMBIGUITY`として停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本`06`や`Pxx`を期待挙動の補完に利用しない。


## 1. Gate outcome

Exploratory 6 Navigation Stage、typed AnalysisView validation、Exploratory Result handoff/provenanceを完成させる。Phase G trace=`PF-D2-01 / PF-D2-02`。

### Typed AnalysisView Filter Contract

Current operator taxonomy is unchanged.

| logical type | allowed operators |
|---|---|
| BOOLEAN | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| INTEGER | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| REAL | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| DATETIME | `EQ, NE, LT, LTE, GT, GTE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| TEXT | `EQ, NE, IN, NOT_IN, IS_NULL, NOT_NULL` |
| OTHER | `IS_NULL, NOT_NULL` |

Value semantics:

- `IS_NULL / NOT_NULL`: valueなし。
- `IN / NOT_IN`: non-empty list。
- scalar/list elementはsource logical typeに一致。
- DATETIME valueはISO-8601。
- INTEGERではbooleanを許容しない。
- REALはfinite numeric only。NaN/Infinity不可。
- `time_cutoff`: DATETIME + `LT / LTE`。
- source type不明をvalidation successにしない。
- mismatch error code=`FILTER_TYPE_MISMATCH`。

Scope exclusions:

- new expression languageを導入しない。
- derived expressionのfull static typing subsystemを導入しない。
- Family-specific filter type systemを導入しない。


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


## 2. Exploratory navigation

```text
profile
data-quality
distribution
relationships
comparison
findings
```

Visualizationはrepresentation concernであり、新runtime Stage taxonomyではない。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## Gate Acceptance Criteria

- `AC-G04-001`: Exploratory stages=`profile/data-quality/distribution/relationships/comparison/findings`。
- `AC-G04-002`: visualizationはrepresentation concernでNavigation/runtime Stage taxonomyを増やさない。
- `AC-G04-003`: POST/PATCH/validate/fixのAnalysisView boundaryが同じtyped validatorを利用。
- `AC-G04-004`: filter operator/value semanticsと`FILTER_TYPE_MISMATCH`が本文どおり。
- `AC-G04-005`: AnalysisView handoffはdata-selection semanticsのみ。
- `AC-G04-006`: downstream request field/derivation rules、target Family、DRAFT、MOTIVATED、no auto FIX/Executionが本文どおり。
- `AC-G04-007`: `analysis_mode=CONFIRMATORY`とsame immutable dataset identityをlater reuse guardが判定可能な形で保持。
