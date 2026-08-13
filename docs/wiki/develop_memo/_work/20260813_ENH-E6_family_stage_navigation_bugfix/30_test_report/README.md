# 30_test_report — ENH-E6 Independent Verification証跡

**Document class:** Authoring Guide  
**Self-containment:** MUST.

## 1. Purpose

Fixed Trial Candidateに対するIndependent Test/Audit evidenceとG01 final Gate Decisionを保存する。Coding execution evidenceから分離し、07 Acceptance Criteriaに基づく観測を記録する。

## 2. Evidence / decision self-containment

各Test Itemはcandidate SHA、method/command、observed fact、result、AC mapping、evidence pathを本文内に持つ。999 Gate DecisionはTest Item結果を統合しPASS/FAIL/BLOCKED理由をself-containedに記載する。

## 3. Directory

```text
30_test_report/
  G01/
    Trial01/
      README.md
      <001-007 Test Item reports created by Independent Test>
      <999 Gate Decision created after Test Items>
```

Runtime evidenceをTrial開始前にfake生成しない。

## 4. Test Item Report

G01 07が定義したTest Item planに沿い、candidate identityからbrowser/regressionまで個別に観測・判定する。Coding Agent package self-checkをそのままTest Item PASSへコピーしない。

## 5. Gate Decision — 999

999のみがTrialのIndependent PASS/FAIL/BLOCKED decision authority。全mandatory AC、blocking Browser E2E、protected regression、candidate identityを統合する。

## 6. Candidate identity fail-closed rule

Fixed Trial Candidateが一意に監査できない、stale image/別SHAをtestしている、diff scopeが不明などの場合、任意candidateをPASSさせずBLOCKEDとする。
