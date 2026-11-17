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
G01/
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
10_enhance_instruction/G01/
  08_ENH-E11_G01_{{TRIAL_NO}}_Remediation_Instruction.md
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


## 12. G02-G10 implementation draft review register (2026-11-17)

**状態:** PREP-03 review DRAFT。G01〜G10はいずれもCODING_NOT_AUTHORIZED。G02〜G10の06/P00/Pxxと07は作成済みだが未Freeze、未承認、試験未実施。各Gateの依存/Required PackagesはOwner未承認の提案で、現行Pxxの実装着手を許可しない。正本`docs/wiki/requirement_definition/`への昇格は行わない。

**受入Authority:** Gate 06=Implementation WHAT、Gate 07=Independent Verification WHAT、P00=計画、各Pxx=実装Execution Unit、40 Operator=テスト実配置/発見/Command、999=正式独立判定。後続Gateの06/07とPxxは同じGate IDを使用する。

| Gate | Functional boundary | Method count | Gate 06 | Gate 07 | P00 | Previous 06 package proposal | Current Pxx count |
|---|---|---:|---|---|---|---:|---:|
| G02 | Identification / DoWhy / FD-A | 6 | [06](G02/06_Ariadne_ENH-E11_G02_implementation_instruction.md) | [07](G02/07_Ariadne_ENH-E11_G02_test_instruction.md) | [P00](G02/06_G02_P00_work_package_plan.md) | 4 | 4 |
| G03 | Native Effects / Refutation / Sensitivity | 13 | [06](G03/06_Ariadne_ENH-E11_G03_implementation_instruction.md) | [07](G03/07_Ariadne_ENH-E11_G03_test_instruction.md) | [P00](G03/06_G03_P00_work_package_plan.md) | 5 | 6 |
| G04 | CATE / EconML / DRIV | 8 | [06](G04/06_Ariadne_ENH-E11_G04_implementation_instruction.md) | [07](G04/07_Ariadne_ENH-E11_G04_test_instruction.md) | [P00](G04/06_G04_P00_work_package_plan.md) | 5 | 4 |
| G05 | HTE Diagnostics / Privacy / authorized row | 0 | [06](G05/06_Ariadne_ENH-E11_G05_implementation_instruction.md) | [07](G05/07_Ariadne_ENH-E11_G05_test_instruction.md) | [P00](G05/06_G05_P00_work_package_plan.md) | 4 | 4 |
| G06 | Temporal Discovery / PCMCI | 3 | [06](G06/06_Ariadne_ENH-E11_G06_implementation_instruction.md) | [07](G06/07_Ariadne_ENH-E11_G06_test_instruction.md) | [P00](G06/06_G06_P00_work_package_plan.md) | 4 | 3 |
| G07 | DiD / Event Study / ITS | 3 | [06](G07/06_Ariadne_ENH-E11_G07_implementation_instruction.md) | [07](G07/07_Ariadne_ENH-E11_G07_test_instruction.md) | [P00](G07/06_G07_P00_work_package_plan.md) | 4 | 3 |
| G08 | RDD / IV / AR | 5 | [06](G08/06_Ariadne_ENH-E11_G08_implementation_instruction.md) | [07](G08/07_Ariadne_ENH-E11_G08_test_instruction.md) | [P00](G08/06_G08_P00_work_package_plan.md) | 5 | 4 |
| G09 | SCM / SDID | 2 | [06](G09/06_Ariadne_ENH-E11_G09_implementation_instruction.md) | [07](G09/07_Ariadne_ENH-E11_G09_test_instruction.md) | [P00](G09/06_G09_P00_work_package_plan.md) | 4 | 3 |
| G10 | Full Replay / Science / Compatibility | All 41 | [06](G10/06_Ariadne_ENH-E11_G10_implementation_instruction.md) | [07](G10/07_Ariadne_ENH-E11_G10_test_instruction.md) | [P00](G10/06_G10_P00_work_package_plan.md) | 4 | 5 |

### 12.1. Review重点（先行06との差分）

- **旧提案の保存/差分Authority:** G02〜G10の先行06/P00/07案は[Git commit `9ec6e198`](https://github.com/kousuke-ota-datascience/causal-atelier/commit/9ec6e198d3d621a27fe8210adf8bf5808ed434f2)、今回の54件Gate06/P00/Pxx具体化は[Git commit `4bf03058`](https://github.com/kousuke-ota-datascience/causal-atelier/commit/4bf03058382203e94059624111958017660ae950)。06とP00は両案の差分をOwner Review対象とし、新Package数を自動承認済みと扱わない。
- **Work Package数の変更:** G03=5→6、G04=5→4、G06=4→3、G07=4→3、G08=5→4、G09=4→3、G10=4→5。G02/G05=4のまま。各案の実装Class ownership、DAG、DoD、Science受入と互換性を比較し、最終06/P00/Pxxを確定する。
- **Gate07は既存DRAFT:** 全9 Gateに07は存在するが未Freeze。Method ID・DD・positive/negative・Science条件の整合は形式的作成では完了しない。今回作成したPxx/06に追随させて独立照合する。
- **G07/G08依存修正:** 両07の依存先`G01 PASS, G02 PASS`に合わせ、今回06/P00も修正済み。先行G01の実装確定や999 PASSを意味しない。
- **未決の明示対象:** G02 P1-M05 IV target、G03 AIPW/NCE/NCO/RV実測Science、G04 EconML Inference/DRIV、G05独立Policy Authority・row Writer Class、G06 Temporal Oracle、G07 DiD/ITS Covariance、G08 AR HC1独立Reference、G09 SCM point-only/SDID、G10全41科学BenchmarkとLicense境界。

### 12.2. Review・Freeze・Coding Authorizationの順序

1. 全Gateの06/P00/Pxxと既存07のMethod/DGP/NEG/REF/AC/依存/実装Class/Source再利用をまとめて監査・Owner判断する。
2. 対象Gateの06/07/PxxにOwner判断を反映し、正本ではなくEnhancement worktree内で正式Freezeする。
3. 対象Gateのupstream canonical 999、実装Source/lock full SHA、依存環境、40 preflightを確認し、**対象Gateごとに**Coding Authorizationを明示する。
4. Authorized GateでのみCoding Agent→Candidate Assembly→Independent Test→999。文書作成や静的整合確認をScience PASSとしない。
