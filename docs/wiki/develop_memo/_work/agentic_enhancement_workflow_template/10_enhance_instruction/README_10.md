# 10_enhance_instruction — Gate契約・実行指示の作成ガイド

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでGate / Trial / Work Packageと06 / 07 / P00 / Pxx / 08 / Rxx / 09の作り分けが分かること。

## Canonical filename rule

- canonical filename / directory nameはASCII charactersのみを使用する。
- semantic filename suffixはtechnical Englishとする。
- 日本語はdocument title / body textにのみ使用してよい。


## 1. Purpose

`10_enhance_instruction/`には、各Gateについて**何を成立させるか、何をもってPASSとするか、実装作業をどのexecution unitへ分けるか、formal FAIL後にどうremediateするか**を定義する。

```text
{{GATE_ID}}/
  06 = Gate Coding Contract
  P00 = Work Package Plan (conditional)
  06_Gxx_Pxx = planned Coding execution package (conditional)
  07 = Gate Verification Contract
  08 = Trial Remediation Contract (formal FAIL後のみ; DELTA / CONSOLIDATED)
  08_Gxx_Rxx = remediation Coding execution package (conditional)
  09 = Gate Contract Amendment record (contract defect時のみ)
```

## 2. Gate / Trial / Work Package

### Gate — Acceptance Contract

Gateは、**作業結果が後続工程から契約上依存可能になったか**を判定するsemantic acceptance boundaryである。実装量・難易度・Agentが一度に扱える量だけを理由にGateを分割しない。

### Trial — Candidate Verification Attempt

Trialは、同一Gate contractに対してcandidateを作り、Fixed Trial Candidateとして固定し、Independent Verificationの正式判定を受けるtransactionである。Agent restartやpackage correctionだけでTrial番号を増やさない。

### Work Package — Coding Execution Unit

Work Packageは、Gateを成立させる実装をbounded execution unitへ分割したものである。Package COMPLETEはGate PASS、verified-state derivation、downstream unlockを意味しない。

## 3. Document self-containment rule

### Primary Execution Contract — MUST self-contained

以下はAgentへ直接与えるprimary contractなので、担当責務に必要なnormative semanticsを本文内に持つ。

- `06 Gate Coding Contract`
- `07 Gate Verification Contract`
- `Pxx planned Work Package instruction`
- `Rxx remediation Work Package instruction`

外部pathはfact / evidence / source / provenance / observation targetとして参照してよい。**別workflow文書を読まなければ実装規則・Acceptance Criteria・completion conditionが分からない状態を作らない。**

### Derived Contract

`08`と`09`は既存contractから派生するため、外部contractへのtraceabilityを保持する。ただし用途は異なる。

- `08` — formal FAIL後のnext Trial remediation。`DELTA` / `CONSOLIDATED`をFAIL evidence確定後に選ぶ。
- `09` — original Gate semantic contract / Acceptance Criteria自体の欠陥をHuman-approved changeとして記録する。09で直接実行を継続するのではなく、承認後にaffected primary contractsをre-baselineする。

## 4. 06 Gate Coding Contract — MUST

06はGate implementation semanticsの一次契約である。最低限以下を本文内に記載する。

- Gate objective / downstream usable result after PASS
- required implementation semantics
- allowed / prohibited scope
- Execution Mode: `SINGLE_EXECUTION` or `WORK_PACKAGE`
- protected passed-Gate contracts
- Transition Debt constraints
- schema / migration / API / runtime policy
- Coding-side verification obligations
- Candidate Assembly requirement
- required outputs / stop condition

Control Sheet、requirements、design、previous Gate Decision等へのpathはprovenance / verified fact取得用であり、06のnormative implementation semanticsを外部へ委譲しない。

## 5. 07 Gate Verification Contract — MUST

07はGate Acceptance Criteriaの一次契約である。最低限以下を本文内に記載する。

- Gate acceptance claim
- Acceptance Criteria
- Test Item plan / primary test layer allocation
- Browser E2E critical journey plan（applicableな場合。canonical Gate blocking suite全体は原則3〜5本程度、各Gateはrelevant subsetのみ）
- Browser E2E canonical command / hermetic environment / synchronization / failure evidence requirements（applicableな場合）
- Fixed Trial Candidate identity rule
- protected passed-Gate regression requirement
- Transition Debt acceptance expectation
- evidence requirements
- PASS / FAIL / BLOCKED semantics
- Test Agent prohibited work
- required outputs

06を読まなければACが分からない構造にしない。Completion Report、source、runtime、previous test evidence等はobservation / evidenceとして参照してよい。

Test planningでは各requirement / ACへ最適なtest layerを割り当てる。Browser E2Eはdetailed correctnessの一次証明ではなく、少数のcritical user journeyがreal system boundaryを跨いで成立することの最終確認に使う。共通authoring policyは`40_operator_workflows/BROWSER_E2E_GATE_POLICY.md`を参照してよいが、Gate固有のblocking E2E item、command、environment、synchronization、assertion、evidence、decision semanticsは07本文へ具体化する。

## 6. Work Package Mode

### 発動条件

次のいずれかが成立し、1 execution unitではfailure localization / restart / focused verificationが不安定になる場合に使用する。

- execution scopeが大きい
- semantic implementation boundaryが複数ある
- dependency DAGがある
- intermediate checkpointが必要
- subsystem / authority boundaryを跨ぐ
- packageごとにfocused verificationが必要

### P00 — orchestration plan

P00はimplementation packageではない。P00自身の責務についてself-containedにし、次を記載する。

- Work Package mode採用理由
- Gate semantic boundaryの要約
- package map / dependency DAG
- package entry / exit criteria
- checkpoint / restart policy
- Candidate Assembly rule
- Trial completion condition

### Pxx — primary execution contract

PxxはAssigned Agentへ直接渡せる状態にする。Parent 06 / P00 pathはtraceabilityとして残してよいが、Pxx実行に必要なeffective constraintsはPxx本文へ記載する。

## 7. 06 / 07 freeze

06 / 07はGate execution開始前にfreezeする。implementation failure、package都合、Test FAILを理由に、過去Trialが依拠したcontractをsilent rewriteしない。

## 8. 08 Trial Remediation Contract — formal FAIL後のみ

08の目的は、original 06 / 07をimmutableに保持したままnext Trialのremediationを定義することである。

### Step 1 — Contract validity check

FAIL evidence確定後、まずoriginal Gate semantic claim / Acceptance Criteriaが依然として正しいか確認する。

- 正しい -> 08を作成する。
- 誤っている -> 08で再定義せず09を作成する。

### Step 2 — Mode selection

`08`のheaderに`Remediation Mode: DELTA / CONSOLIDATED`を明記する。

**DELTA**を選ぶ条件:

- 06 / 07の大部分がそのまま有効
- failure / correction scopeが局所的
- required parent sectionsが少ない
- `parent context + 08 delta`の方が小さく明確

DELTAでは、参照必須となる06 / 07 / failed decisionを明示し、failure facts、correction delta、forbidden workaround、追加verification、next candidate ruleを記載する。

**CONSOLIDATED**を選ぶ条件:

- remediationが複数領域へ及ぶ
- Work Package decomposition / execution orderが大きく変わる
- implementation / verification requirementsを多数横断する
- 1文書へ統合した方がcontext fragmentation / ambiguityが小さい

CONSOLIDATEDでは、next Trialに必要なeffective implementation semantics、verification requirements、scope、prohibitions、protected constraints、completion conditionを08内へ統合する。


### Operational resolution rule — current Trial 08

formal FAIL後にAgent executionへ入る場合、`GATE_ID + TRIAL_NO`からcurrent Trialの08を**exactly one**へ解決できなければならない。canonical pathは次とする。

```text
10_enhance_instruction/{{GATE_ID}}/
  08_{{ENHANCE_ID}}_{{GATE_ID}}_{{TRIAL_NO}}_Remediation_Instruction.md
```

0件または複数候補の場合は推測・fallbackせず`BLOCKED_REMEDIATION_CONTRACT_MISSING`または`BLOCKED_CONTRACT_AMBIGUITY`とする。旧Trialの08を代用しない。

`40_fail_remediation_01_fail_rework_coding_agent_prompt.md`へ直接渡す08は、normative-source isolationを成立させるため`CONSOLIDATED`かつ`SINGLE_EXECUTION`とし、current 08だけでrework implementation / verification / completion conditionを一意に判断できる状態にする。`DELTA`またはRxx decompositionを選択する場合は、当該direct entry promptをそのまま使用しない。

## 9. Rxx Remediation Work Package — primary execution contract

Work Package remediation時はoriginal Pxx identityを再利用せず`R01-R99`を使う。RxxはAgentへ直接渡すため**self-contained MUST**とし、Parent 08のmodeにかかわらず、担当Rxxを実行するためのeffective constraintsを本文内に記載する。

## 10. 09 Gate Contract Amendment

09は、original 06 / 07のsemantic contractそのものが不適切と判明した場合のexplicit Human-approved amendment recordである。

最低限:

- contract defect
- why remediation is insufficient
- Before / After semantic change
- affected Acceptance Criteria
- protected passed-Gate impact
- invalidated P00 / package instructions
- Trial handling
- approval evidence
- required re-baseline artifacts

09自体を「失敗したのでACを緩める」手段にしてはならない。承認後はaffected primary contractsを明示的にre-baselineする。

APPROVED / APPLIED amendmentは`00_enhance_background/80_contract_amendment_log.md`にもappend-onlyで記録し、09・re-baseline artifacts・Git traceabilityを相互参照可能にする。80 ledgerはnormative execution authorityではない。

## 11. Authority summary

```text
06 = implementation semantic authority
07 = acceptance authority
P00 = execution decomposition authority
Pxx / Rxx = bounded execution authority; 06/07 semantic contractをsilent overrideしない
08 = next-Trial remediation authority; DELTA / CONSOLIDATED
09 = explicit contract-change decision authority
999 Gate Decision = final independent PASS / FAIL / BLOCKED authority
```

<!-- BEGIN MANAGED: V005_LOCAL_AUTHORITY -->
## v0.05 runtime authority

Gate local READMEはHuman navigation / canonical artifact index専用であり、execution eligibilityを変更しない。

Normal-path routing authority:

```text
Gate dependency declaration = Gate 06 `Depends on`
Execution mode              = Gate 06 `Execution mode`
Required package set        = Gate 06 `Required packages`
Verification authority      = Gate 07
Package dependency          = each assigned Pxx `Depends on`
```

P00は存在してもoptional authoring / audit artifactであり、preflight / Candidate Assembly / Orchestratorのruntime authorityにはしない。
<!-- END MANAGED: V005_LOCAL_AUTHORITY -->
