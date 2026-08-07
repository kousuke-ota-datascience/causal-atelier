# G6 Trial 001 Test 013 — authorization_and_sensitive_output

- Gate: G6
- Trial: 001
- Test item: 013
- Status: FAIL
- Tested implementation commit: `265b69a3317a0b9747cacee457e72b36a62daa7e`
- Handoff report commit / path: `963f1f2` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T12:32:15Z
- Finished at: 2026-08-07T12:38:14Z

## Purpose

Project authorization、controlled download、secret/sensitive output policy、validation error contractを検証する。

## Acceptance Criteria

cross-project access rejection、project role enforcement、controlled Artifact download、logs/artifactsへのsecret非露出、prediction/local explanation policy、validation error path/code。

## Preconditions / Environment

- Relevant tests: `test_cross_analysis_lineage_e3.py`、`test_results_lineage_export_e3.py`。

## Commands Executed

```bash
rg -n 'PROJECT_ACCESS_DENIED|PROJECT_BOUNDARY|VIEWER|download|secret|api_token|prediction_rows|local.explanation|INVALID_REQUEST' tests/product
sed -n '110,210p' tests/product/test_results_lineage_export_e3.py
sed -n '120,160p' tests/product/test_cross_analysis_lineage_e3.py
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 uv run python -c \
  'from ariadne.product.application.product_closure_service import _suppress_sensitive_output; \
   actual=_suppress_sensitive_output({"local_explanation":[{"row_id":"sensitive-row","prediction":0.9}]}); \
   print(actual); raise SystemExit(0 if actual.get("local_explanation")=="[SENSITIVE_OUTPUT_SUPPRESSED]" else 1)'
```

## Exact Result

- coverage audit exit code: 0
- sensitive-output contract probe exit code: 1
- observed output: `{"local_explanation": [{"prediction": 0.9, "row_id": "sensitive-row"}]}`
- duration: coverage audit plus 1.54s deterministic probe

## Log / Evidence

- Existing coverage: cross-project explicit lineage-link reject、VIEWERのworkspace-state write reject、export summary secret redaction、prediction_rows default suppression、unknown-field error code/path。
- 非memberまたはforeign ProjectからResult/Artifact/Exportへaccessする拒否assertionがない。
- Artifact/downloadをrole別に制御し、hash不整合を拒否するassertionがない。
- logへのsecret非露出assertionがない。
- local explanationのdefault suppression/明示取得authorization assertionがない。
- 実際のPredictive Explanation payload keyは`local_explanation`（単数形）だが、`_suppress_sensitive_output`のsensitive setは`local_explanations`（複数形）のみ。probeでrow identifierとpredictionが抑制されず残ることを確認した。

## Findings

- Failure category: REQUIRED_TEST_COVERAGE_MISSING
- Product failure: SENSITIVE_LOCAL_EXPLANATION_NOT_SUPPRESSED
- Missing contract: endpoint-level cross-project authorization; controlled Artifact download/hash; no-secret logs; local explanation sensitive-output policy.
- Expected test scope: direct automated negative/positive assertions over mandatory roles, project boundaries, downloads and sensitive fields.
- Observed existing coverage: partial role/boundary/redaction/validation coverage.
- product defect: default Result detailのsuppression helperが実payloadの`local_explanation` keyを抑制しない
- test infrastructure issue: none

## Required Correction

Default sensitive-output policyに反し、`local_explanation`内のrow-level dataが抑制されない。加えて、欠落しているauthorization/download/log/local-explanation contractsのautomated evidenceが必要。

## Decision Rationale

単一VIEWER write拒否とmanifest redactionだけではG6-013全体を証明しない。さらにdeterministic probeがlocal explanation漏洩を示したため、product defectとcoverage欠落の両方によりFAIL。

## Source Modification by Test Agent

NONE
