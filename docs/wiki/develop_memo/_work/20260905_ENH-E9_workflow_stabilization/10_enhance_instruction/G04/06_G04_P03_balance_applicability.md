# ENH-E9 G04 P03 — Before/After Balance and Estimator Applicability

**Document class:** Work Package Execution Contract  
**Self-containment:** `MUST`  
**Assigned Coding Agent normative context:** `THIS DOCUMENT ONLY`  
**Status:** `FROZEN`  
**Gate:** `G04`  
**Package:** `P03`  
**Depends on:** G04 P02 canonical package report `State: PACKAGE_COMPLETE`

## 1. Objective

`DIAGNOSTICS_RESULT`のbalanceをunweighted before / scientifically applicable afterへ分離し、IPW / AIPW / OLS / difference-in-meansのapplicabilityを偽装なく表現する。

P03はpost-weight balanceを「存在する場合だけ」保存する。beforeをafterへコピーして見かけ上のcomplete payloadを作らない。

## 2. Entry criteria

- branch=`bugfix/ariadne_mvp_e9`
- clean working tree
- P02 canonical package reportがexactly one存在し`State: PACKAGE_COMPLETE`
- 本P03がexactly one解決されFROZEN
- current Trialにformal 08 remediation contractなし

## 3. Required balance contract

```text
balance:
  before: <balance row list>
  after: <balance row list | null>
  after_applicability: ESTIMATOR_WEIGHT | PROPENSITY_COMPONENT | NOT_APPLICABLE
```

`balance.before`:

- unweighted covariate balance
- current adjustment-set covariatesを対象
- existing balance row schemaを互換維持

`balance.after`:

- actual estimator weightまたはscientifically defined propensity componentによるweighted balanceのみ
- scientifically undefined/non-applicableなら`null`
- beforeのcopyは禁止

## 4. IPW semantics

IPWは`ESTIMATOR_WEIGHT`。

`e(x)` = configured propensity clipping後のpropensity score。

```text
ATE:
  treated observed rows: 1 / e(x)
  control observed rows: 1 / (1 - e(x))

ATT:
  treated observed rows: 1
  control observed rows: e(x) / (1 - e(x))
```

Weighted balanceへ渡すobservation weightは、各observed rowについて自身のarmに対応するactual positive analysis weightを持つsingle aligned Seriesとして構築してよい。これはcombined final estimator weightを意味せず、balance計算用にarm-specific actual weightsをrow alignmentしたものとする。

IPW:

```text
balance.after_applicability = ESTIMATOR_WEIGHT
balance.after = weighted balance using actual arm-specific IPW analysis weights
```

## 5. AIPW semantics

AIPWは`PROPENSITY_COMPONENT`。

- estimator全体のsingle final weightとして表現しない。
- whole-estimator treated/control ESSを捏造しない。
- propensity-derived component balanceをscientifically一意に定義・説明できる場合のみ`balance.after`を保存する。
- E9でcurrent AIPW scoreに対する「final weighting balance」を一意に定義できない場合、`balance.after = null`を正とする。
- `balance.after_applicability = PROPENSITY_COMPONENT`は、afterがnullでもapplicability classificationとして保持できる。

AIPWについてIPW after-balanceを機械的に再利用しない。

## 6. OLS / difference-in-means semantics

```text
balance.after_applicability = NOT_APPLICABLE
balance.before = <unweighted balance rows>
balance.after = null
```

weight/ESS/weighted balanceを架空生成しない。

## 7. Weighting companion contract expectations

P03はbalanceとweighting classificationの不整合を作らない。

Expected mapping:

| Estimator | weighting.applicability | balance.after_applicability |
|---|---|---|
| IPW | ESTIMATOR_WEIGHT | ESTIMATOR_WEIGHT |
| AIPW | PROPENSITY_COMPONENT | PROPENSITY_COMPONENT |
| OLS | NOT_APPLICABLE | NOT_APPLICABLE |
| difference-in-means | NOT_APPLICABLE | NOT_APPLICABLE |

AIPW `balance.after = null`は許容する。

## 8. Protected invariants

- Treatment Effect numeric semantics
- existing unweighted balance row meaning
- Result/Execution lineage
- API route grammar / ResultType
- propensity clipping semantics
- AIPW score semantics
- frontendはpersisted diagnosticsをauthorityとする

## 9. Explicitly forbidden

- beforeをafterへ複製
- IPW weightをAIPW whole-estimator final weightとして扱う
- OLS/diff-in-meansへweight/ESS/after balanceをfabricate
- frontend側でweighted balanceを再計算
- balance改善のためestimator calculationを変更
- unrelated refactor

## 10. Implementation substrate hints

Likely responsibility（仕様authorityではない）:

- `src/ariadne/causal/inference/diagnostics/balance.py`
- `src/ariadne/scientific/inference/adapter.py`
- estimator-side exposed actual/component weights
- scientific/unit/integration fixtures

Existing `compute_balance_table`がoptional aligned weightsを受けられる場合、そのbehaviorを再利用してよいが、weighted/unweighted semanticsをtestで明示する。

## 11. Focused verification — mandatory

Browser E2Eは実行しない。

Required cases:

1. same known fixtureで`balance.before`がunweighted expected valuesと一致。
2. IPW ATE `balance.after`がactual ATE weightsによるindependent expected weighted balanceと一致。
3. IPW ATT `balance.after`がactual ATT weightsによるexpected weighted balanceと一致。
4. IPW before/afterが非自明fixtureで同一copyになっていない。
5. OLS NOT_APPLICABLE + after=null。
6. difference-in-means NOT_APPLICABLE + after=null。
7. AIPW PROPENSITY_COMPONENT。whole-estimator final weight/ESSを表現しない。
8. AIPW afterを実装しない場合after=nullでclassificationが保持される。
9. existing balance/overlap/Treatment Effect regression PASS。
10. persisted payloadがNaN/Infinity等invalid JSON scientific valuesを含まない。

## 12. Completion boundary

P03 completeは、before/after/applicability semanticsが上記mappingどおりpersistされ、mandatory non-browser testsがPASSし、Treatment Effect/lineage regressionがなく、checkpoint/reportが存在する場合のみ。

## 13. Stop rule

- AIPW component after-balanceを一意に定義できないならnullを選び、推測値を作らない。
- existing balance row semanticsを変更しないと実装できない場合はBLOCKED。
- Gate claim/AC変更が必要なら09 amendmentへ戻す。
