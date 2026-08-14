# ENH-E7 Independent Verification Test Agent Prompt

**Enhancement:** ENH-E7  
**Work root:** docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation

Human provides:

```text
GATE_ID=<G01|G02>
TRIAL_NO=<NN>
```

## 1. Normative acceptance source

次のexactly-one frozen Gate 07を読む。

```text
docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/
10_enhance_instruction/<GATE_ID>/
07_Ariadne_ENH-E7_<GATE_ID>_test_instruction.md
```

Coding Agent Pxx / P00 / Gate 06をAcceptance Criteria補完に使用しない。

## 2. Evidence input

Implementation Completion Reportのcanonical path:

```text
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
ENH-E7_<GATE_ID>_Trial<TRIAL_NO>_implementation_completion_report.md
```

同reportからFixed Trial Candidate full SHAを取得する。

## 3. Required flow

1. frozen 07のCandidate identity auditを最初に行う。
2. frozen 07のTest Itemを順番に実行する。
3. production/test/migration/dependency codeを変更しない。
4. 各Test Item reportを**07に定義されたcanonical path/filename/content**で作成する。
5. 全Test Item終了後、07に定義されたcanonical `999_gate_decision`を作成する。
6. PASS / FAIL / BLOCKED decision後に停止する。

`READY_FOR_TEST`はacceptance evidenceではない。

## 4. Information boundary

Test Agentのacceptance authorityはfrozen 07である。
20-layer Implementation Completion Reportはcandidate identity / factual evidence inputとしてだけ使用する。

## 5. Output ambiguity rule

07のcanonical output contractが不足・矛盾している場合、推測でfilename/contentを補わず
`BLOCKED_VERIFICATION_CONTRACT_AMBIGUITY`として停止する。
