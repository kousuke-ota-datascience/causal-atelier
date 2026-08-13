# Ariadne ENH-E6 — Family / Stage Navigation Observable UI Bugfix

**Document class:** Authoring Guide / Enhancement Root Index
**Self-containment:** MUST — このREADMEだけでENH-E6のworkflow semantics、artifact authority、現在地、operator route、監査規則を理解できること。

* Enhancement ID: `ENH-E6`
* Target branch: `bugfix/ariadne_mvp_e6`
* Production baseline SHA: `5a5ced9bd6a0e62027c4058eb66ec487719bde23`
* Instruction freeze / template-compliance audit input SHA: `42df32decaa67b9de8c6cab518d441cf0a2f8fe4`
* Source anomaly: `ENH-E5 / ANOM-E5-001 — Family Tab Observable UI Gap`
* Active Gate: `G01`
* Execution Mode: `WORK_PACKAGE`
* Current workflow state: `G01 06/07 FROZEN; ENH-E6-specific agent entry prompts instantiated; P01 Trial01 ready for execution`
* Canonical requirements/design: `docs/wiki/requirement_definition/**` is READ ONLY for ENH-E6

## 0. このテンプレートの目的

> ENH-E6 instanceでは、本節を「このenhancement bundleに適用するworkflow templateの目的」として具体化する。

ENH-E6は、ENH-E5で契約された3つのAnalysis Family (`EXPLORATORY / PREDICTIVE / CAUSAL`) とFamily-local Navigation Stageが、通常の実ユーザー導線でobservableにならない `ANOM-E5-001` を修正するbugfix enhancementである。

本bundleは、なぜ修正するか、何を成立させるか、どのexecution unitへ分解するか、何を独立検証するか、現在どのevidenceがverifiedかを再構成・監査できるcontrol planeである。ENH-E6は正本の要件・設計を変更しない。正本と実装の不一致を修正する。

### Canonical filename policy

* filename / directory nameはASCII charactersのみを使用する。
* semantic suffixはtechnical Englishを使用する。
* 日本語はdocument title / body textで使用してよい。
* `ENH-E6`, `G01`, `Trial01`, `P01`等のidentifierはcanonical identityとして保持する。
* Humanはidentityを指定し、derived path/nameはworkflow schemaに従う。

## 0.1. Document design principles

ENH-E6の各artifactは、自身の責務についてself-containedである。外部pathはfact/evidence/provenanceとして参照できるが、execution contractの意味を別workflow文書へ委譲しない。

### Document classes

| Document class                                  | ENH-E6での主な対象                   | Self-containment rule       |
| ----------------------------------------------- | ------------------------------ | --------------------------- |
| Authoring Guide                                 | root README, 各directory README | MUST                        |
| Primary Execution Contract                      | Gate 06, Gate 07, P01-P03      | MUST                        |
| Derived Contract                                | 08/09（必要時のみ）                   | CONDITIONAL                 |
| Planning / Evidence / State / Operator Artifact | 00, 20, 30, Current State, 40  | MUST for own responsibility |

### Local normative meaning

現在文書内に、目的、状態の意味、必須条件、禁止事項、判断基準、completion condition、必要なauthority/precedenceを記載する。特にPxxはassigned Coding AgentがPxxだけで実装判断できるeffective contractを持たなければならない。

### Evidence / fact by reference

source code、commit SHA、diff、command output、過去Gate Decision、正本要件・設計は外部参照してよい。ただし、Coding AgentへGate 06/07/P00/他Pxx/00-30を読ませてspecificationを補完させてはならない。

### Remediation exception

G01がIndependent Verificationでformal FAILした場合のみTrial02を作り、08を作成する。Gate semantic claim/AC自体が誤っていた場合は08で緩和せず09を使用する。現時点では08/09とも未発動である。

このbundleから後日最低限次を再構成できることを要求する: objective、requirement/design delta、Gate claim、package execution、candidate identity、independent verification、verified state、protected contract、Transition Debt、preflight、audit trail。

---

## 1. 最初に理解すべきworkflow semantics

### 1.1. Gate — Acceptance Contract

ENH-E6はG01のみを持つ。G01は「どのsupported entry pathからでもcanonical Family/Stage Navigation Contextとobservable shell/presentationが同期する」という一つのsemantic acceptance boundaryである。UI、route、testを作業量だけで別Gateに分けない。

### 1.2. Trial — Candidate Verification Attempt

`Trial01`はP01-P03でcandidateを生成し、Candidate AssemblyでFixed Trial Candidateを固定し、Independent Verificationを受ける一連のtransactionである。Coding Agentのrestartやpackage correctionだけではTrial番号を増やさない。

### 1.3. Work Package — Coding Execution Unit

G01はWork Package Modeを使用する。P01/P02/P03は実装のHOWを安全に分離するexecution unitであり、Package completionはGate PASSではない。

### 1.4. Responsibility matrix

| 観点               | G01 Gate             | Trial01                         | P01-P03                      |
| ---------------- | -------------------- | ------------------------------- | ---------------------------- |
| 主目的              | semantic acceptance  | candidate verification attempt  | bounded coding execution     |
| authority        | frozen 06/07 + 999   | Fixed Candidate + test evidence | assigned Pxx                 |
| completeの意味      | downstream reliance可 | PASS/FAIL/BLOCKED               | next implementation stepへ進める |
| verified state更新 | PASS時のみ              | 直接しない                           | しない                          |
| restart          | contract維持           | formal FAILまでTrial01            | 同Trial内で可能                   |

### 1.5. Workflow invariants

1. G01-local 06/07はfreeze済みで、Trial中にsilent rewriteしない。
2. Gate scopeとAgent execution scopeを分離する。
3. Trial01はcandidate-to-independent-verification transactionである。
4. P01-P03はbounded Coding Agent execution unitである。
5. Package checkpoint、Fixed Trial Candidate、Gate PASSを混同しない。
6. verified state promotionはG01 final PASS時のみ。
7. ENH-E5 passed evidenceはimmutable。
8. authority / precedence / evidence identityを明示する。
9. Browser E2EはANOM-E5-001に直結する少数critical journeyのreal cross-layer proofに限定する。

---

## 2. 作成するdocument layers

```text
Current_State_Control_Sheet.md
00_enhance_background/
10_enhance_instruction/
20_implementation_reports/
30_test_report/
40_operator_workflows/
```

### 2.1. Document authority

* `Current_State_Control_Sheet.md`: final PASS済みverified stateのindex。未検証candidateを昇格しない。
* `00`: why / requirement-design delta / approval / traceability / architecture review provenance。
* `G01/06`: Gate-wide implementation semantic authority。Coding Agentの直接entry sourceではない。
* `G01/07`: Independent VerificationのAcceptance Criteria authority。Coding Agentへ見せない。
* `G01/P00`: Human/operator向けexecution decomposition authority。Coding Agentへ見せない。
* `G01/Pxx`: assigned Coding Agentが読む唯一のnormative implementation contract。
* `20`: implementation evidence / package checkpoint / candidate assembly record。
* `30`: independent test evidence / Gate Decision。
* `40`: Human-controlled agent entry, architecture review, preflight。

---

## 3. エンハンス文書を作成する順序

### Step 1 — Background / requirements / designを作成する

完了。ENH-E6は正本要件を変更せず、implementation realization requirementとdesign deltaを00層で定義した。architecture/lifecycle/authority変更に該当するためArchitecture Reviewを適用済みとして40層にevidenceを保存する。

### Step 2 — Gate decompositionを決める

完了。G01一つ。UI/component/file数ではなく「observable Family/Stage navigation integration」というdownstream-relyable semantic claimで境界を決めた。

### Step 3 — Current State Control Sheetを初期化する

完了。source inspection、ENH-E5 provenance、API READY clean negative-control preflightをverified baselineとして記録し、post-fix behaviorは未verifiedとして分離する。

### Step 4 — Gateごとの06 / 07を作成してfreezeする

完了。Human owner reviewとpreflight後にG01 06/07を`APPROVED / FROZEN`とした。template compliance修正はschema/情報隔離/監査性の補正であり、Gate semantic claim/ACを緩和しない。

### Step 5 — Execution Modeを選択する

`WORK_PACKAGE`。transition authority、presentation/legacy binding、browser regressionは依存順序とfocused verificationが異なるため。

### Step 6 — Work Packageを使う場合はP00 / Pxxを作成する

P00、P01、P02、P03を作成済み。本template-compliance revisionでPxxをPrimary Execution Contractとしてself-contained化し、Coding Agentの情報隔離規則を明示する。

### Step 7 — Coding Agentを起動する

次の実行単位は`G01 / P01 / Trial01`。Coding Agentへ直接Gate 06/07/P00を渡してはならない。

ENH-E6では、template側のparameterized entry promptをそのまま実行せず、Enhancement固定値を展開済みのinstance-specific operator promptを `40_operator_workflows/agent_entry_prompts/` に保持する。

#### Operator Quick HowToUse

Human operatorがCoding Agentへ与えるentry instructionは次だけとする。

```text
下記文書に記載の指示を実行すること。

- docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix/40_operator_workflows/agent_entry_prompts/
    - 10_normal_execution_02_work_package_coding_agent_prompt.md

今回の指示は

- GATE_ID=G01
- PACKAGE_ID=P01
- TRIAL_NO=01

である。
```

参照先のENH-E6-specific operator promptには、少なくとも以下のEnhancement固定値が事前展開されていることを前提とする。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E6
ENHANCE_SHORT_ID=E6
BRANCH_NAME=bugfix/ariadne_mvp_e6
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix
WORK_DIR_NAME=20260813_ENH-E6_family_stage_navigation_bugfix
```

これによりHuman operatorは実行時変数のみを指定し、ENH-E6 / G01 / P01 / Trial01を一意に解決する。

Coding AgentはP01だけをnormative implementation contractとして扱う。Gate 06、Gate 07、P00、他Pxx、00-30、過去enhancement/ADR/issue/Webをspecification completion目的で読んではならない。

template directory配下の未展開operator promptを直接Agent executionへ使用してはならない。

### Step 8 — Candidate Assemblyを行う

P01-P03のrequired checkpointが揃った後、別のCandidate Assembly routeでFixed Trial Candidateを作る。Coding Agentが自己判断でGate candidateをassembleしない。

### Step 9 — Independent Test / Auditを実行する

Fixed Trial Candidateを固定後、Test/Audit Agentへ07をacceptance authorityとして与える。Coding AgentとVerification contractを分離する。

### Step 10 — Gate Decisionに従って遷移する

* PASS: Current Stateをpromotionし、ANOM-E5-001をresolution conditionに従ってclose可能。
* FAIL: Trial02へ。original 06/07はimmutable、08を作成。
* BLOCKED: prerequisite/verification blocking reasonを解消し、contractを勝手に変更しない。

---

## 4. Gate vs Work Packageの判定規則

G01 PASSが一つのdownstream-relyable semantic contractを成立させるためGateは1つ。P01-P03の分割理由はdependency/failure localization/focused verificationでありWork Package理由である。

## 5. Canonical identifiers and naming

* `ENHANCE_ID=ENH-E6`
* `GATE_ID=G01`
* `TRIAL_NO=01`（最初のformal verification attempt）
* planned package: `P01`, `P02`, `P03`
* remediation package: `Rxx`（formal FAIL後のみ）
* canonical filenames/directoriesはASCII。

### 5.1. Enhancement-fixed, runtime-supplied, and derived variables

ENH-E6のoperator promptをinstance化する時点で、以下はEnhancement固定値として展開済みでなければならない。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E6
ENHANCE_SHORT_ID=E6
BRANCH_NAME=bugfix/ariadne_mvp_e6
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix
WORK_DIR_NAME=20260813_ENH-E6_family_stage_navigation_bugfix
```

通常のWork Package Coding Agent起動時にHuman operatorが指定するruntime valuesは、当該promptが要求する実行単位識別子のみとする。本ENH-E6 P01 Trial01では次である。

```text
GATE_ID=G01
PACKAGE_ID=P01
TRIAL_NO=01
```

package instruction path、20/30 evidence path、candidate/report filename等は上記固定値とruntime valuesからworkflow schemaに従ってderiveする。

Agentがrepository探索、branch名、会話文脈、近傍directory等から不足したEnhancement identityやpathを推測してはならない。

未解決のEnhancement固定placeholderがoperator promptに残る場合はexecutionを開始せず、Human operatorへBLOCKEDとして返す。

## 6. Gate contract model

### 6.1. 06 = Gate Coding Contract

G01全体のimplementation semantic boundary。何を成立させるか、scope、prohibition、protected semantics、runtime policy、test obligationsを固定する。Package Coding Agentの直接normative sourceではない。

### 6.2. P00 = Work Package Plan — conditional

本ENHでは適用。Human/operatorがpackage DAG、entry/exit、checkpoint、Candidate Assemblyを管理する。implementation packageではない。

### 6.3. P01-P99 = Planned Work Package

P01-P03を適用。各Pxxはself-contained primary execution contract。Parent pathはtraceabilityとして保持しても、Coding Agentへparent workflow documentを読むよう指示しない。

### 6.4. 07 = Gate Verification Contract

G01のAcceptance Criteria一次契約。Coding Agentへ読ませない。Independent VerificationのみがGate PASSを判定する。

### 6.5. 08 = Trial Remediation Contract

現時点N/A。Trial01 formal FAIL後のみ作成する。

### 6.6. 09 = Gate Contract Amendment

現時点N/A。06/07 semantic contract自体の欠陥をHuman ownerが承認した場合のみ作成する。

### 6.7. Browser E2E responsibility policy

G01はBrowser E2E applicable。actual Family tab/Stage click、legacy shortcut、deep link/reload/historyの3 critical journeysをblocking proofとする。source-string existence testはsupplementalでありobservable acceptanceの代替ではない。

## 7. Candidate Assembly and evidence identity

P01/P02/P03 checkpointはそれぞれ独立identityを持つ。それらをassemblyしたFixed Trial Candidate SHAだけがIndependent Verification対象となる。

### 7.1. Evidence hierarchy

`START_SHA -> package checkpoint SHA -> package evidence commit -> Fixed Trial Candidate SHA -> Test Item evidence -> 999 Gate Decision -> Current State promotion` を区別する。

### 7.2. Documentation-only post-candidate changes

Fixed Candidate後のdocumentation-only correctionはproduction candidate identityを勝手に変えず、何がdocumentation-onlyかを明示し、verification evidenceとのtraceabilityを保持する。

## 8. Passed-Gate immutability

ENH-E5のfrozen 06/07、implementation/test reports、Gate DecisionをENH-E6から書換えない。ENH-E6 G01もTrial開始後はfrozen contractをsilent rewriteしない。

## 9. Transition Debt

ENH-E6 source anomalyは`ANOM-E5-001`。G01 final PASS前にRESOLVEDへpromotionしない。legacy left navigationの完全撤去等はE6 scope外follow-upとしてledgerに残す。

## 10. Document authority domains and conflict rule

Gate06=implementation semantics、Gate07=acceptance、P00=decomposition、Pxx=bounded coding execution、20=evidence、30=independent decision、Current State=verified index。

### Conflict rule

Pxxがfrozen Gate semantic boundaryと矛盾するとHuman/contract ownerへBLOCKEDとしてescalateする。Coding Agentが07等を読んで自力で矛盾解消してはならない。正本要件とENH-local designに矛盾を発見した場合も推測で補完しない。

## 11. Agent boundaries

### 11.1. Coding Agent

assigned Pxxのみをnormative implementation contractとして読む。source/test/config/migrationはimplementation substrateとして調査可。Gate06/07/P00/他Pxx/00-30/過去ENH/ADR/issue/Webでspecificationを補完しない。Package completionをGate PASSと表現しない。

Coding AgentはENH-E6固有のinstantiated operator promptから起動される。template directory上の未展開promptを直接entry pointとして使用してはならない。

### 11.2. Test / Audit Agent

Fixed Candidateと07を基準に独立検証する。production codeを修正しない。Coding Agentのself-checkをGate PASS evidenceへ昇格しない。

## 12. Parameterized operator prompt rules

Human operatorは、template directory上のparameterized promptを直接Agentへ渡さない。

まずEnhancement作へ渡さない。

まずEnhancement作業directory内の

```text
40_operator_workflows/agent_entry_prompts/
```

へoperator prompt一式をinstance化し、Enhancement固定値を具体値へ展開する。

ENH-E6では少なくとも以下が固定済みでなければならない。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E6
ENHANCE_SHORT_ID=E6
BRANCH_NAME=bugfix/ariadne_mvp_e6
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix
WORK_DIR_NAME=20260813_ENH-E6_family_stage_navigation_bugfix
```

その後、Human operatorはENH-E6固有のentry promptを指定し、`GATE_ID/PACKAGE_ID/TRIAL_NO`等のprompt-required runtime variablesだけを渡す。

Agentへ多数のworkflow文書を手動列挙してcontext isolationを破壊してはならない。

未展開のEnhancement固定placeholder、曖昧な`WORK_ROOT`、未確定のbranch/remote identityを含むoperator promptではexecutionを開始してはならない。

## 13. Preflight / prerequisite

実施済み。API READY、UIでProject作成/選択、canonical `/analysis/exploratory/profile` 到達、Family tab container=1、Family buttons=0、Stage buttons=0をclean negative controlとして取得。既存Playwright/Chromium harnessとcanonical compose invocationも確認済み。40層にinstruction/resultを記録する。

## 14. Architecture discovery — conditional workflow

適用済み。ENH-E6はruntime lifecycle、navigation authority、legacy path consolidationを変更するためCONDITIONAL MUSTに該当。current facts、single transition authority decision、1-Gate/3-package decompositionを40層に記録する。

## 15. Requirement levels

* Canonical product requirements/design: `docs/wiki/requirement_definition/**`。READ ONLY、ENH-E6では変更しない。
* ENH-local realization requirements: E6-FR/E6-NFR。正本の変更ではなくbugfix realization/acceptance clarification。
* Gate acceptance: AC-E6-G01-001..011。07 authority。

## 16. Instantiation checklist

* [x] root/background/instruction/state artifactsをinstance化
* [x] canonical requirements/designは変更対象外と明示
* [x] architecture review applicabilityを判定・記録
* [x] G01 semantic boundaryを1文で定義
* [x] Current Stateをverified factsだけで初期化
* [x] G01 06/07をHuman review + preflight後にfreeze
* [x] Work Package Mode理由とP00/P01-P03を作成
* [x] PxxをCoding Agent self-contained contractへ修正
* [x] Coding Agentから07/P00/06等を情報隔離
* [x] Trial01用20/30 namespaceを初期化
* [x] preflight/operator evidence namespaceを作成
* [x] `40_operator_workflows/agent_entry_prompts/` をENH-E6固有値でinstance化
* [x] Enhancement固定値 `PROJECT_NAME / ENHANCE_ID / ENHANCE_SHORT_ID / BRANCH_NAME / REMOTE_NAME / WORK_ROOT / WORK_DIR_NAME` を展開
* [x] Coding Agent entryでtemplate directory上の未展開promptを直接使用しないことを明示
* [x] Work Package Coding Agent起動時にHumanが指定すべきruntime valuesを `GATE_ID / PACKAGE_ID / TRIAL_NO` に限定
* [ ] P01 Coding Agent execution
* [ ] P02/P03 checkpoint
* [ ] Candidate Assembly
* [ ] Independent Verification
* [ ] 999 Gate Decision / Current State promotion

## 17. Human audit checklist

1. [x] Enhancement objectiveは明確か。
2. [x] Current problemとtarget outcomeは区別されているか。
3. [x] canonical requirement/designを変更するか否か明示したか。
4. [x] architecture review applicabilityを判定したか。
5. [x] Gateはsemantic acceptance boundaryか。
6. [x] implementation sizeだけでGate分割していないか。
7. [x] Gate/Trial/Work Packageを区別したか。
8. [x] 06はimplementation semanticsをself-containedに持つか。
9. [x] 07はAcceptance Criteriaをself-containedに持つか。
10. [x] P00はorchestrationのみか。
11. [x] Pxxはassigned Agentが単独で実行可能か。
12. [x] Pxxが別workflow文書を読ませていないか。
13. [x] Coding AgentとTest Agentのauthorityを分離したか。
14. [x] 06/07 freeze pointは明示されているか。
15. [x] Passed-Gate evidenceをimmutableに扱うか。
16. [x] package checkpointとGate PASSを混同していないか。
17. [x] Candidate Assembly responsibilityを分離したか。
18. [x] Fixed Trial Candidate identityを要求したか。
19. [x] Browser E2Eはcritical journeyへ限定したか。
20. [x] Browser E2E canonical command/environment/evidenceを07へ固定したか。
21. [x] static source-existence testをobservable UI proofの代替にしていないか。
22. [x] preflight prerequisiteをGate acceptanceと区別したか。
23. [x] Transition Debtのopen/close条件を明示したか。
24. [x] formal FAIL時の08/Trial transitionを定義したか。
25. [x] contract defect時の09 routeを定義したか。
26. [x] Current StateはPASS-only promotionか。
27. [x] artifact filename/directoryはASCIIか。
28. [x] Humanが後からdecision/evidence/authorityを再追跡できるか。
29. [x] Enhancement固有の`agent_entry_prompts/`をinstance化したか。
30. [x] Enhancement固定値がoperator prompt内で具体値へ展開されているか。
31. [x] 未展開template promptをAgent executionへ直接使用しないか。
32. [x] `WORK_ROOT`から対象Enhancementを一意に解決できるか。
33. [x] Humanのentry instructionがruntime variablesだけを指定する形になっているか。

## 18. 更新履歴

### ENH-E6 local workflow correction — agent entry prompt instantiation

Coding Agent起動時のEnhancement identityを一意にするため、template directory上のparameterized operator promptを直接参照する運用を廃止した。

ENH-E6固有の

```text
40_operator_workflows/agent_entry_prompts/
```

をinstance化し、次のEnhancement固定値を展開した。

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E6
ENHANCE_SHORT_ID=E6
BRANCH_NAME=bugfix/ariadne_mvp_e6
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E6_family_stage_navigation_bugfix
WORK_DIR_NAME=20260813_ENH-E6_family_stage_navigation_bugfix
```

これによりWork Package Coding Agent起動時のHuman instructionは、ENH-E6固有operator promptをentry pointとし、`GATE_ID / PACKAGE_ID / TRIAL_NO`のみをruntime指定する。

この修正はG01のsemantic implementation contractまたはAcceptance Criteriaを変更するものではない。

### Schema v13

本instanceは現行templateのdocument self-containment、Coding Agent normative-source isolation、Work Package operator prompt、Browser E2E責務分離を採用する。

### Schema v12

Trial/Candidate Assembly/evidence identityの分離を適用する。

### Schema v11

Work Package Mode、P00/Pxx execution decompositionを適用する。

### Schema v3

Current State Control Sheetによるverified-state controlを適用する。

### Schema v2

Gate-local 06/07 authority、passed-Gate immutabilityを適用する。
