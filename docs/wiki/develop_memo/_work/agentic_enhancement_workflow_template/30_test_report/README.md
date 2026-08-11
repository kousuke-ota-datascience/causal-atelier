# 30_test_report — Independent Verification証跡の作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでTest Item / 999 Gate Decisionの役割・作成規則・authority boundaryが分かること。

## 1. Purpose

`30_test_report/`には、Test / Audit AgentがFixed Trial Candidateを独立検証したevidenceと、final Gate Decisionを保存する。

## 2. Evidence / decision self-containment

各Test Itemは、そのitemだけでtest objective、criterion、method、observed fact、result、reproductionが分かるようにする。

999 Gate Decisionは特に強いself-containmentを要求し、その1文書だけで以下が分かること。

- tested candidate identity
- Gate acceptance claim
- ACごとの結果
- protected regression / TD result
- PASS / FAIL / BLOCKEDの理由
- PASS時のdownstream reliance
- FAIL時のverified failure facts

外部Test Item / log / source / Completion Reportはevidenceとして参照してよいが、`詳細は001-008参照`だけでfinal rationaleを省略しない。

## 3. Directory

```text
30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
  {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_001_*.md
  ...
  {{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_999_gate_decision.md
```

## 4. Test Item Report

最低限:

- Fixed Trial Candidate SHA / Tested Repository State
- AC mapping
- exact command / method
- exit code
- raw relevant evidence
- observed Facts / Interpretation
- criterion evaluation
- source mutation audit
- reproduction procedure
- result rationale

## 5. Gate Decision — 999

`999`だけがfinal PASS / FAIL / BLOCKED authorityを持つ。

PASS:
- required AC / candidate identity / protected regression / blocking TD conditionsが成立。

FAIL:
- valid candidateをtestでき、MUST AC / protected contract不成立がverifiedされた。

BLOCKED:
- prerequisite / candidate identity / contract ambiguity等で妥当な判定ができない。

formal FAIL時、failure factsをnext 08 authoring inputとして本文内に要約する。08のmodeはGate Decisionでは決め打ちせず、FAIL analysis後に選択してよい。
