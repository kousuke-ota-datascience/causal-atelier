# G6 Trial 001 Test 004 — annotation_and_export

- Gate: G6
- Trial: 001
- Test item: 004
- Status: FAIL
- Tested implementation commit: `265b69a3317a0b9747cacee457e72b36a62daa7e`
- Handoff report commit / path: `963f1f2` / `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G6_001_implementation_completion_report.md`
- Branch: `prototype/ariadne_mvp_e3`
- Migration head: `20260807_product_0006`
- Started at: 2026-08-07T12:32:15Z
- Finished at: 2026-08-07T12:32:32Z

## Purpose

Annotation対象・履歴と、再現性情報を含むManifest/Result/Artifact/Lineage export契約を検証する。

## Acceptance Criteria

全supported Annotation targets、rationale/assumptions/limitations/decision/next_actions、history、Manifest、Result summary、Specification、Artifact references、Lineage references、Result payloadとArtifact downloadの分離。

## Preconditions / Environment

- Relevant test: `tests/product/test_results_lineage_export_e3.py`。

## Commands Executed

```bash
sed -n '110,200p' tests/product/test_results_lineage_export_e3.py
rg -n 'target_type|revision_history|manifest|specification|artifact|lineage|download' tests/product/test_results_lineage_export_e3.py
```

## Exact Result

- coverage audit exit code: 0
- relevant tests collected: 1
- tests executed: 0
- duration: within initial 17s coverage/static audit

## Log / Evidence

- Existing test exercises only Annotation target `Result` and checks revision history/semantic fields partially。
- Export fixture has no asserted Specification、source Artifact references、lineage references。
- Export downloadは検証するが、Result payload endpointとsource Artifact downloadを分離する契約の直接assertionがない。

## Findings

- Failure category: REQUIRED_TEST_COVERAGE_MISSING
- Missing contract: supported Annotation target matrix; Specification/Artifact/Lineage manifest contents; Result payload vs source Artifact download separation.
- Expected test scope: direct automated assertions for each mandatory export/annotation contract.
- Observed existing coverage: Result annotation/history、summary redaction、export metadata/download.
- product defect: not established
- test infrastructure issue: none

## Required Correction

次trialでは、欠落しているAnnotation targetおよびexport内容/分離契約のautomated evidenceが必要。

## Decision Rationale

Manifestをdownloadできることだけでは必須内容を証明しないため、07b §17によりFAIL。

## Source Modification by Test Agent

NONE
