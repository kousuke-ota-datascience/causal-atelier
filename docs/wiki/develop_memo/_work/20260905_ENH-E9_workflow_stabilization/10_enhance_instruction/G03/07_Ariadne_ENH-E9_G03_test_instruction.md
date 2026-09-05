# Ariadne ENH-E9 G03 Verification Contract

**Verification contract status:** `DRAFT_NOT_FROZEN`

## Draft Acceptance Criteria

1. Population / Comparator helpをscopeに含めた場合、causal question上の意味をUIから確認できる。
2. Treatment selectorをscopeに含めた場合、selected Dataset Version schemaをcandidate authorityとし、invalid/stale candidateをsilent保持しない。
3. Treatment selection後もexisting causal-question serialization/backend validation semanticsを維持する。
4. OutcomeはGraphVersion designated outcome由来のread-only inputであり、独立編集できない。
5. FIXED Graph requirement、estimand、identification strategy、adjustment set、assumptionsがregressionしない。
6. Estimation submission architectureを変更しない。

## Primary test layers

- frontend interaction/unit: help/selector/read-only Outcome
- integration/contract: causal question serialization, dataset schema candidate authority
- regression: Graph -> Identification -> Estimation lineage

Browser E2Eを使う場合はG05 critical journeyとの重複を避け、G03固有blocking valueがある場合だけfreezeする。
