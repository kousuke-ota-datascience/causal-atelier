# Ariadne ENH-E9 G03 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `FROZEN`

## Acceptance Criteria

1. Population / Comparatorのcausal-question上の意味をUI helpから確認できる。
2. Treatment selectorはselected Dataset Version schemaをcandidate authorityとする。
3. Dataset Version変更等でinvalid/stale Treatmentをsilent保持しない。
4. Treatment selection後もexisting causal-question serialization/backend validation semanticsを維持する。
5. Identification Outcomeはselected FIXED Graphのdesignated Outcomeから自動継承され、read-onlyかつ独立編集不能である。
6. FIXED Graph requirement、estimand、identification strategy、adjustment set、assumptionsがregressionしない。
7. selected Identification Result → Estimation submission lineage/architectureを変更しない。

## Verification layers and execution order

1. static / syntax checks
2. frontend interaction/unit: help, selector, stale clearing, read-only Outcome
3. integration/contract: serialization and Dataset Version schema candidate authority
4. regression: Graph → Identification → Estimation lineage and protected semantics
5. blocking AC evaluation

G03単独Browser E2Eは実行しない。cross-layer Browser E2EはG05で、G05のnon-browser verification完了後の最後のverification itemとして実行する。

全blocking AC PASSのみG03 PASS。
