# Ariadne ENH-E9 G04 Verification Contract

**Verification contract status:** `DRAFT_NOT_FROZEN`

## Draft Acceptance Criteria

1. Applicable estimatorでdiagnosticsがstable structured Resultとしてpersistされる。
2. IPW等でESSを要求するcontractをfreezeした場合、known weightsから期待値を再計算可能なtestで検証する。
3. Weight diagnosticsはestimatorが実際に使用したweightを対象とし、count/min/mean/quantiles/max/extreme ruleがcontractどおりである。
4. weight scale/normalization semanticsがcontract/document/testで一意に理解できる。
5. balance before/afterが区別され、unweighted valueをweighted-afterとして誤表示しない。
6. estimator applicability matrixに従い、non-applicable diagnosticsを架空値で埋めない。
7. AIPWのweighting component diagnosticをAIPW全体のsingle final weightと表現しない。
8. persisted ResultをFrontendがstructured fieldとして利用でき、string parsing/causal inference再計算を要求しない。
9. existing Treatment Effect / Result / Execution lineageを破壊しない。

## Primary test layers

- scientific/unit: formulas/statistics/applicability
- backend integration/contract: persistence/schema/lineage
- frontend integration: structured Result consumption
- Browser E2E: detailed numeric correctnessのprimary proofにはしない。G05でcritical connectivityを確認する。

Exact expected values / fixtures / schema pathはsource review後のfreeze時に記載する。
