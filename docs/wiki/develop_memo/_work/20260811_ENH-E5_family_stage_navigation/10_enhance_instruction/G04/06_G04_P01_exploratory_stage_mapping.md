# Ariadne ENH-E5 G04 — P01 Exploratory Stage Mapping and Typed Filter Validation

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G04`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `a4d96b33c81b5a263a2e82e6d64475de5085b616`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `assigned Pxx implementation contract`

## 0. Authority / execution isolation

- 本文書は、このPackage Coding Agentに対する**唯一のnormative implementation contract**である。
- Package Coding Agentは仕様補完のためにGate `06`、他`Pxx`、`P00`、Gate `07`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repositoryはcurrent implementation factと実装方法を調査するsubstrateとして参照してよいが、仕様authorityではない。
- 本文書だけでrequired behavior / protected boundary / error semanticsを一意に決定できない場合は、探索を広げず`BLOCKED_CONTRACT_AMBIGUITY`で停止する。
- Test / Audit Agentのnormative verification sourceはGate `07`のみであり、本Pxxを期待挙動の補完に利用しない。


## 1. Outcome

Exploratory 6-stage presentationとtyped AnalysisView filter validationを実装する。

Stages:

```text
profile
data-quality
distribution
relationships
comparison
findings
```

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


## 2. Validation boundaries

POST/PATCH/validate/fixの全AnalysisView boundaryで同じtyped validatorを利用する。

## Prohibited changes

- `Navigation Stage = Execution Stage`となるmapping、alias、inheritanceを導入しない。
- Navigation Stageを`AnalysisSpecification / ExecutionPlan / Execution / StageExecution`へpersistしない。
- CLI / Python library / backend execution use caseへCurrent Navigation Stageを必須inputとして追加しない。
- `AnalysisSpecification.analysis_family`と重複するFamily discriminatorを追加しない。
- Predictive existing fieldの削除、rename、default semantics変更を行わない。
- LightGBM / DoWhy / EconMLを追加しない。
- D3 / `DEFERRED / FUTURE` requirementをENH-E5 implementationまたはmandatory acceptanceへ混ぜない。
- testをgreenにする目的のassertion弱体化、削除、skip、xfailを行わない。


## 4. Package Acceptance Criteria

- six stage route binding。
- type×operator×value matrix exact。
- boolean-as-integer reject、REAL non-finite reject、DATETIME ISO-8601。
- null operators valueなし、membership non-empty list。
- time_cutoff exact。
- mismatch=`FILTER_TYPE_MISMATCH`。

## Completion evidence

- changed production / test / schema / migration files
- focused test commands and results
- relevant regression commands and results
- candidate SHA / checkpoint SHA
- blocker status (`NONE` or explicit blocker)
