# 10_enhance_instruction — ENH-E6 Gate契約・実行指示

**Document class:** Authoring Guide  
**Self-containment:** MUST — このREADMEだけでENH-E6のGate/Trial/Work Packageと06/07/P00/Pxx/08/Rxx/09の作り分けと情報隔離規則を理解できること。

## Canonical filename rule

- canonical filename/directoryはASCII。
- technical English suffixを使用。
- Japaneseはtitle/bodyのみ。

## 1. Purpose

ENH-E6ではG01について、何を成立させるか(06)、何をもってPASSとするか(07)、実装をどうbounded execution unitへ分けるか(P00/P01-P03)、formal FAIL後にどう遷移するか(08/09)を管理する。

## 2. Gate / Trial / Work Package

### Gate — Acceptance Contract

G01はObservable Family/Stage Navigation Integrationというsemantic boundary。PASS後に後続がreal user navigation behaviorへ依存可能になる。

### Trial — Candidate Verification Attempt

Trial01はP01-P03 -> Candidate Assembly -> Independent Verificationのtransaction。Agent restartやsame-package correctionではTrial番号を増やさない。

### Work Package — Coding Execution Unit

P01-P03はimplementation execution unit。Package `PACKAGE_READY`はGate PASS/verified state/downstream unlockを意味しない。

## 3. Document self-containment rule

### Primary Execution Contract — MUST self-contained

- Gate 06: Gate-wide implementation semantics
- Gate 07: Independent acceptance semantics
- P01-P03: assigned Coding Agent execution semantics

**Coding Agent information isolation:** Work Package Coding Agentはcanonical operator promptからassigned Pxxを正確に1件解決し、そのPxxのみをnormative implementation contractとする。Gate06、07、P00、他Pxx、00-30、ADR、過去ENH、issue、external Webをspecification completionのために読まない。Pxxはこの制約下で自己完結しなければならない。

### Derived Contract

08/09は必要時のみ。現Trial開始前は未生成。

## 4. 06 Gate Coding Contract — MUST

G01 objective/downstream result、required semantics、allowed/prohibited scope、Work Package mode、protected E5 contracts、TD、schema/API/runtime policy、Coding-side obligations、Candidate Assembly、outputs/stop conditionsをself-containedに固定する。Package Coding Agentの直接entry documentではない。

## 5. 07 Gate Verification Contract — MUST

G01 Acceptance Claim、AC-E6-G01-001..011、Test Item plan、3 blocking Browser E2E journeys、canonical command、candidate identity、protected regression、evidence、PASS/FAIL/BLOCKEDをself-containedに固定する。Coding Agentへ参照させない。

## 6. Work Package Mode

### 発動条件

transition authority、presentation/legacy binding、browser test harnessのdependency/failure localization/focused verificationが異なるため採用。

### P00 — orchestration plan

Human/operator用。package map/DAG/entry-exit/checkpoint/Candidate Assembly/Trial completionを管理し、Coding Agentには読ませない。

### Pxx — primary execution contract

P01-P03は各自のrequired behavior、constraints、scope、focused verification、completion、stop ruleを本文だけで判断可能にする。parent workflow docsを読ませる参照は禁止。

## 7. 06 / 07 freeze

Human review + API READY negative-control preflight後に`APPROVED / FROZEN`。Trial execution中にimplementation/test都合でsilent rewriteしない。今回のtemplate-compliance correctionはsemantic ACを変更せずschema/self-containmentを補完する。

## 8. 08 Trial Remediation Contract — formal FAIL後のみ

### Step 1 — Contract validity check

Formal FAIL後に06/07 semantic claim/ACが依然正しいか判定。正しければ08、誤りなら09。

### Step 2 — Mode selection

DELTA/CONSOLIDATEDをFAIL evidenceに基づき選ぶ。現在N/A。

### Operational resolution rule — current Trial 08

Trial01には08は存在してはならない。Trial02以降のformal FAIL remediationではcurrent Trial 08をexactly oneへ解決する。0/複数ならBLOCKED。

## 9. Rxx Remediation Work Package — primary execution contract

現時点N/A。Work Package remediationが必要ならRxxはself-containedで作る。

## 10. 09 Gate Contract Amendment

現時点N/A。Gate semantic contract/AC自体のdefectをHuman-approvedで変える場合だけ使用。failed implementationに合わせてACを緩めるために使わない。

## 11. Authority summary

```text
G01 06 = Gate-wide implementation semantics
G01 07 = Independent acceptance authority; Coding Agent non-visible
P00    = Human/operator execution decomposition; Coding Agent non-visible
Pxx    = assigned Coding Agent's only normative implementation contract
20     = implementation evidence
30     = independent evidence/decision
```
