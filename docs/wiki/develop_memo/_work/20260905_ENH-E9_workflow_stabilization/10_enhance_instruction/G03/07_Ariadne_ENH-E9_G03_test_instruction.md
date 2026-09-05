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

## Verification layers

frontend interaction/unitでhelp/selector/read-only Outcome、integration/contractでserialization/schema candidate authority、regressionでGraph → Identification → Estimation lineageを検証する。G03単独Browser E2Eは必須とせず、cross-layer journeyはG05でblocking verificationする。

全blocking AC PASSのみG03 PASS。
