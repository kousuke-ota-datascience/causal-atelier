# Ariadne ENH-E9 G04 Verification Contract

**Document class:** Primary Execution Contract / Acceptance Authority  
**Verification contract status:** `FROZEN`

## Entry identity audit

Trial Implementation Completion Reportに記録されたexact `FIXED_TRIAL_CANDIDATE_SHA`だけを検証する。mutable/uncommitted candidate、candidate identity不明、candidate-affecting post-freeze diffが分類不能な場合はBLOCKED。

## Acceptance Criteria

1. `DIAGNOSTICS_RESULT`はexisting sample/design/overlapに加え、stable structured `balance.before/after` と `weighting` applicability contractを保存する。
2. IPWではeffect calculationに用いるarm-specific actual positive analysis weightsからweight statisticsとtreated/control ESSを生成する。
3. IPW ATE weight semanticsはtreated=`1/e(x)`、control=`1/(1-e(x))`であり、`e(x)`はconfigured clipping後propensityである。
4. IPW ATT weight semanticsはtreated=`1`、control=`e(x)/(1-e(x))`である。
5. IPW ESSは各armについてindependent expected calculation `(sum w)^2 / sum(w^2)` と数値一致する。
6. weight statistics `count,min,mean,p50,p95,p99,max` はknown fixture actual arm weightsからindependently再計算した値と一致する。QuantileはNumPy-compatible linear semanticsとする。
7. `extreme_rule`はexactly `weight > 10.0`、`extreme_count`はそのruleをactual un-normalized arm weightsへ適用した件数である。`weight == 10.0`は含めない。Propensity clipping countを代用しない。
8. `weighting.definition`はIPWについて `arm-specific IPW analysis weights computed from clipped propensity scores; weighted means normalize by each arm's weight sum` のsemanticsを一意に表す。
9. `balance.before`はunweighted、IPW `balance.after`はactual arm-specific IPW weightsによる値であり、beforeをafterとして複製しない。
10. OLS/difference-in-meansは`NOT_APPLICABLE`としてweight/ESSを架空生成せず、`balance.after = null`を許容する。
11. AIPWは`PROPENSITY_COMPONENT`として扱い、estimator全体のsingle final weightと表現しない。whole-estimator treated/control ESSをfabricateしない。component after-balanceが科学的に一意でない場合`balance.after = null`を許容する。
12. Frontendはpersisted structured fieldsを直接consumeし、ESS/weights/quantiles/extreme count/weighted balanceを再計算せず、notes/definition string parsingでscientific valuesを復元しない。
13. Treatment Effect value/uncertainty、Result/Execution lineage、API route grammar、Effects/Diagnostics Stage ownershipをregressionさせない。
14. legacy top-level `balance` compatibility projectionを残す場合、それをnew after-weighting authorityとして使用しない。
15. Stable structured numeric fieldへNaN/Infinityをpersistせず、undefined/non-applicableはnullで表現する。

## Primary verification layers and mandatory order

1. candidate identity / post-candidate diff audit
2. static / syntax
3. scientific/unit
   - actual IPW ATE/ATT weights
   - ESS formula
   - statistics/quantiles
   - `10.0` extreme-rule boundary
   - weighted balance
   - estimator applicability
4. backend integration/contract
   - DIAGNOSTICS_RESULT payload/persistence
   - Result/Execution lineage
   - backward compatibility
5. frontend integration
   - structured consumption
   - null/not-applicable/unavailable rendering
   - no string parsing/recomputation
6. protected regression evaluation
7. Gate decision

**G04ではBrowser E2Eを実行しない。** Numeric/scientific correctnessは上記non-browser verificationがprimary authorityであり、cross-layer Browser E2EはG05 final verificationへ委譲する。

## Required independent fixtures

最低限:

- IPW ATE known fixture
- IPW ATT known fixture
- weight exactly `10.0` と `>10.0` を含むextreme boundary fixture
- OLSまたはdifference-in-means NOT_APPLICABLE case
- AIPW PROPENSITY_COMPONENT case
- before/afterが非自明に異なるweighted-balance fixture
- frontend ESTIMATOR_WEIGHT / PROPENSITY_COMPONENT / NOT_APPLICABLE / legacy payload cases

Expected weights/ESS/statisticsはproduction helperをexpected authorityとして呼ばずtest側で独立計算する。

## PASS / FAIL / BLOCKED

- 全blocking ACとprotected regressionがPASSした場合のみG04 PASS。
- valid candidateのproduct contract mismatchはFAIL。
- scientific semanticsが曖昧で期待値を一意に定義できない、candidate identity不明、environment/harness defectで判定不能の場合はBLOCKED。
- test failureを理由にACを緩和しない。
