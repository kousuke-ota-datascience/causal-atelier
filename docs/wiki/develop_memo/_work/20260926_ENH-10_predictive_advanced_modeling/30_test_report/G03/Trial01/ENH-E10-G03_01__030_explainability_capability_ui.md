# ENH-E10 G03 Trial 01 — Test Item 030: Explainability Capability UI

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-04, AC-07, AC-08 | **PASS** |

## Method / command

The 58-test command in item 010 includes ENH-E10 G02 capability and explanation integration tests. The frozen browser command in items 100/110 visibly selected `SHAP_TREE` for binary LightGBM and `LIME_TABULAR` for regression LightGBM, then required generated explanation results and the predictive-not-causal UI text.

## Observed facts

- G02 contract tests passed: unknown method is explicit `EXPLANATION_METHOD_NOT_REGISTERED`; SHAP on linear is `EXPLANATION_METHOD_NOT_APPLICABLE`; global LIME is `EXPLANATION_SCOPE_NOT_SUPPORTED` with no pseudo-global fallback.
- scenario 100 selected SHAP global/local and emitted `PREDICTIVE_EXPLANATION_RESULT`; scenario 110 selected local LIME and emitted the same canonical result type.
- browser runner asserted `Predictive Explanation ≠ Causal Explanation`; result/artifact evidence was retrieved after terminal execution.
- optional provider absence behavior is protected by G02 contract tests; installed advanced runtime was verified through the two browser journeys.

## Interpretation

method compatibility, global/local boundaries, explicit unavailable behavior and predictive terminology remain intact from UI selection to persisted result. AC-04/07/08 are **PASS**。
