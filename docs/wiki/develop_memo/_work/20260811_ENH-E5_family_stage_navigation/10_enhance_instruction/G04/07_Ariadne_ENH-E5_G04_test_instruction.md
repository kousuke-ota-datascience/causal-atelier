# Ariadne ENH-E5 G04 — Exploratory Family Recomposition — Verification

- プロジェクト: Ariadne
- Enhancement: ENH-E5
- Active Gate: `G04`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `83d33f5c981fa1aa5740e91c30bb969dd6097c42`
- 契約状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Canonical convergence source: `10 / 21 / 22 / 23 / 30 = NFR-019 PASS / FROZEN`
- Document role: `Gate 07 verification contract`

## 0. Authority / verification isolation

- 本文書は、このGateを検証する**Test / Audit Agentに対する唯一のnormative verification contract**である。
- Test / Audit Agentは期待挙動を補完するためにGate `06`、`Pxx`、`P00`、`00〜30`、ADR、issue、commit message、外部Webを参照してはならない。
- repository、candidate diff、test output、migration state、API responseはverification evidenceとして参照してよいが、仕様authorityではない。
- 本文書だけでPASS / FAILを一意に判定できない場合は`BLOCKED_CONTRACT_AMBIGUITY`として報告し、仕様を発明しない。


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

Exploratory Result -> downstream request semantics:

```text
source_result_id
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


## Gate Acceptance Criteria

- `AC-G04-001`: Exploratory stages=`profile/data-quality/distribution/relationships/comparison/findings`。
- `AC-G04-002`: visualizationはrepresentation concernでNavigation/runtime Stage taxonomyを増やさない。
- `AC-G04-003`: POST/PATCH/validate/fixのAnalysisView boundaryが同じtyped validatorを利用。
- `AC-G04-004`: filter operator/value semanticsと`FILTER_TYPE_MISMATCH`が本文どおり。
- `AC-G04-005`: AnalysisView handoffはdata-selection semanticsのみ。
- `AC-G04-006`: downstream request field/derivation rules、target Family、DRAFT、MOTIVATED、no auto FIX/Executionが本文どおり。
- `AC-G04-007`: `analysis_mode=CONFIRMATORY`とsame immutable dataset identityをlater reuse guardが判定可能な形で保持。


## Verification architecture

- unit/domain: exact type/operator/value matrix。
- boundary/API: AnalysisView POST/PATCH/validate/fix same validator。
- negative: boolean INTEGER、NaN/Infinity REAL、invalid ISO date、empty IN、source type unknown。
- handoff: exact request fields、lineage-derived dataset/view、context derivation、DRAFT、MOTIVATED、no auto FIX/Execution。
- reuse preparation: `analysis_mode=CONFIRMATORY` + same immutable dataset evidence。
- browser/regression: six stages、visualization-only state separation、current Explore behavior。
