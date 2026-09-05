# Ariadne ENH-E9 G04 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `FROZEN`

## Acceptance Criteria

1. `DIAGNOSTICS_RESULT`はexisting sample/design/overlapに加え、stable structured `balance.before/after` と `weighting` applicability contractを保存する。
2. IPWではeffect calculationに用いるarm-specific actual weightsからweight statisticsとtreated/control ESSを生成する。
3. IPW ESSはindependent expected calculation `(sum w)^2 / sum(w^2)` と数値一致する。
4. weight statistics `count,min,mean,p50,p95,p99,max` はknown fixtureのactual weightsからindependently再計算した値と一致する。
5. `extreme_count`は保存された`extreme_rule`に従う。Propensity clipping countをweight extreme countとして代用しない。
6. `weighting.definition`からweight scale/normalization semanticsを一意に理解できる。
7. `balance.before`はunweighted、`balance.after`はapplicable weight/component weightによる値であり、beforeをafterとして複製しない。
8. OLS/difference-in-meansは`NOT_APPLICABLE`としてweight/ESS架空値を生成しない。
9. AIPWは`PROPENSITY_COMPONENT`として扱い、diagnosticsをestimator全体のsingle final weightと表現しない。実装するcomponent diagnosticはそのdefinitionと一致する。
10. Frontendはpersisted structured fieldsを直接consumeし、string parsingやcausal diagnostic再計算を必要としない。
11. Treatment Effect value/uncertainty、Result/Execution lineage、API route grammarをregressionさせない。
12. legacy `balance` compatibility projectionを残す場合、それをnew after-weighting authorityとして使用しない。

## Primary verification layers

- scientific/unit: weight construction, ESS formula, quantiles, extreme-rule boundary, weighted balance, estimator applicability
- backend integration/contract: DIAGNOSTICS_RESULT payload/persistence/lineage/backward compatibility
- frontend integration: structured consumption and unavailable/not-applicable rendering
- Browser E2E: numeric correctnessのprimary proofにせずG05でcross-layer connectivityのみ確認

## Required fixtures

IPW ATEとATTを最低1件ずつ含め、known treatment/propensity/weightsからexpected ESS/statisticsをtest側で独立計算する。OLSまたはdifference-in-meansのNOT_APPLICABLE case、AIPWのPROPENSITY_COMPONENT caseも含める。

全blocking AC PASSのみG04 PASS。scientific semanticsが曖昧で期待値を定義できない場合は推測してPASSせずBLOCKED/contract amendmentへ戻す。
