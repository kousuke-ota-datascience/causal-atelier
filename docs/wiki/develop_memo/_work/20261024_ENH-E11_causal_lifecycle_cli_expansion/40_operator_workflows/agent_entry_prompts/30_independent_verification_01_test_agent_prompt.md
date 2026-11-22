# Independent Test / Audit Agent Prompt

**ENH-E11 Gate別Authorization Preflight（Owner DEC-PREPCODE-01=B、G01のみDEC-G01-EXEC-01追加採用）:** 全Gate402件のSHA索引は独立S09 PASSではない。**G01専用例外**：独立S09・B02/B04実Python3.12・B05 MAG/PAG/BKはCoding Entryの事前PASSを要求せず、G01_999までの必須実測/独立審査として`EXTERNAL_PENDING/NOT_RUN`で保持する。Coding開始に必要なのは、G01/common 06/Pxx/07等のAuthor契約整合、未検証例外の明示、**Ownerが別途発行した暫定G01-S10（対象正本full SHAと07/999 obligationsを固定）**、さらに**Ownerが別途発行した限定G01-S11（許可G01/P01〜P05、source/lock/paths）**の両方。Ownerの方針採用そのものはFreeze・Coding Authorizationではない。G01で実装できるのは許可WPと開発者テストだけ、未知の科学真値・CI/BK/Backend状態をPASSへ昇格しない。non-null BKは有効独立remedyまでFCI呼出前typed deny。G01_999は独立S09、B02/B04、独立Graph/BK B05、実FS/Reader/T2/T3/旧Product回帰/独立07が未完ならBLOCKED。**G02〜G10は従来DEC-PREPCODE-01=BのGate別独立S09→Owner S10→別Owner S11と実上流999 PASSを厳守**。どのGateもOwner承認証拠欠損・SHA不一致・契約変更なら`BLOCKED_CODING_AUTHORIZATION`、Agentを起動しない。現在G01の暫定S10/限定S11は両方未承認。

## 1. Invocation parameters

Human / Orchestrator は実行前に以下を確定して与える。

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=prototype/ariadne_mvp
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
```

本実行では、上記の `GATE_ID` および `TRIAL_NO` を以降の placeholder に代入して実行せよ。

---

## 2. Responsibility boundary

本 Agent の責務は、指定された Gate / Trial について、

1. repository state を確認する
2. freeze 済み Gate 07 を正確に1件特定する
3. Implementation Completion Report から Fixed Trial Candidate identity を取得する
4. Candidate identity audit を行う
5. 07 が要求する independent verification を実行する
6. Test Item ごとの raw evidence と判定を記録する
7. Test Item `999_gate_decision` として Gate Decision を記録する
8. test evidence を commit / push する
9. `PASS` / `FAIL` / 明示的な `BLOCKED_*` 状態を報告する

ことである。

本 Agent は implementation を修正しない。

本 Agent は PASS を得るために Acceptance Criteria、test、production code、migration、dependency 等を変更しない。

---

## 3. Repository preflight

検証開始前に以下を実行せよ。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

以下を確認する。

* current branch が `prototype/ariadne_mvp` であること
* working tree が clean であること
* Test Agent 実行開始時 HEAD を `TEST_START_SHA` として記録すること

current branch が異なる場合、または開始時点で uncommitted change が存在する場合は、既存変更を reset / checkout / restore / stash / commit してはならない。

その場合は verification を開始せず、`BLOCKED_REPOSITORY_STATE` として終了せよ。

---

## 4. Normative verification contract

以下 directory から、指定された `GATE_ID` に対応する freeze 済み Gate 07 を**正確に1件**特定せよ。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
10_enhance_instruction/
  {{GATE_ID}}/
    07_Ariadne_ENH-E11_{{GATE_ID}}_test_instruction.md
```

該当 07 が存在しない、または一意に特定できない場合は verification を開始せず停止せよ。

特定した **07 のみ**を normative verification contract とする。

以下を Acceptance Criteria の補完・修正・解釈のために読んではならない。

* 06
* Pxx
* 00〜30 の planning / analysis 文書
* ADR
* Gate decomposition
* 他 Gate の文書
* 過去 Enhancement の文書
* issue
* commit message
* 外部 Web

repository / source / automated test / runtime output は、実際の observation / evidence を取得する目的では参照してよい。

ただし、それらを期待仕様の authority として扱ってはならない。

> repository から観測方法を発見してよい。
> repository や上流資料から Acceptance Criteria を発見してはならない。

07 だけでは Acceptance Criteria、PASS / FAIL 条件、protected regression、Transition Debt 等を一意に判断できない場合、他資料へ探索を広げてはならない。

その場合は `BLOCKED_CONTRACT_AMBIGUITY` として停止せよ。

---

## 5. Fixed Trial Candidate identity

以下の current Trial Implementation Completion Report を確認せよ。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      E11-{{GATE_ID}}_{{TRIAL_NO}}__implementation_completion.md
```

Implementation Completion Report は **candidate identity evidence としてのみ**参照してよい。

Implementation Completion Report の内容から Acceptance Criteria を補完・変更してはならない。

report から exact

```text
FIXED_TRIAL_CANDIDATE_SHA
```

を取得せよ。

以下の場合は `BLOCKED_CANDIDATE_IDENTITY` として停止せよ。

* Implementation Completion Report が存在しない
* `FIXED_TRIAL_CANDIDATE_SHA` が記録されていない
* SHA が一意でない
* SHA に対応する commit が repository に存在しない
* test target と candidate identity の対応を監査できない

candidate commit の存在確認を行う。

```bash
git cat-file -e "{{FIXED_TRIAL_CANDIDATE_SHA}}^{commit}"
git show --stat --oneline --decorate --no-renames "{{FIXED_TRIAL_CANDIDATE_SHA}}"
```

---

## 6. Candidate identity audit

07 に定義された Candidate identity audit を**最初の Test Item**として実行せよ。

最低限以下を記録する。

* `TEST_START_SHA`
* `FIXED_TRIAL_CANDIDATE_SHA`
* test 実行対象の actual HEAD / repository state
* `git status`
* candidate と actual test target の関係
* candidate 後に差分が存在する場合、その差分
* test target が Fixed Trial Candidate と同一の semantic implementation state であることの根拠

candidate と actual repository state が異なる場合は、07 の規定に従って diff を audit する。

差分が documentation-only / non-semantic であることを証明できない場合、独自判断で test を続行してはならない。

状況に応じて `BLOCKED_CANDIDATE_IDENTITY` または 07 が要求する判定とする。

formal FAIL remediation Trial で current Remediation Contract に `PREVIOUS_FAILED_CANDIDATE_SHA` が定義されている場合は、product verification 開始前に以下も確認する。

```text
FIXED_TRIAL_CANDIDATE_SHA != PREVIOUS_FAILED_CANDIDATE_SHA
```

同一 candidate が再提出されている場合は `BLOCKED_CANDIDATE_IDENTITY` として停止する。

---

## 7. Independent verification

07 に記載された Test Item 計画、Acceptance Criteria、protected regression、Transition Debt audit を実行せよ。

各 Test Item について最低限以下を記録する。

* Test Item ID
* 対応する Acceptance Criteria / verification purpose
* command / input
* test target identity
* observed output
* evidence
* result

  * `PASS`
  * `FAIL`
  * `BLOCKED`
* 判定理由

自動 assertion が実用的な箇所では自動検証を優先する。

manual observation / screenshot は補助 evidence として利用してよいが、自動検証可能な事項について automation の代替としてはならない。

### Browser E2E Test Item — conditional

07が`BROWSER_E2E`として定義したGate blocking Test Itemのみを実行する。本Agentが詳細仕様証明のためにBrowser E2E scopeを追加しない。

Browser E2Eでは、07が定義するcanonical command / environment bootstrap / semantic synchronization / observable assertionをauthorityとする。URL到達やfixed timeoutだけをworkspace readyの代替にしない。

Browser E2E failure時は修正へ進まず、evidenceに基づき可能な限り次へ分類する。

```text
PRODUCT_INTEGRATION_DEFECT
TEST_IMPLEMENTATION_DEFECT
TEST_ORCHESTRATION_DEFECT
TEST_ENVIRONMENT_DEFECT
UNKNOWN
```

分類はdiagnosisでありGate Decisionそのものではない。product / contract violationをverifiedできた場合のみFAIL候補とし、test implementation / orchestration / environment defectまたはUNKNOWNのためproduct correctnessを判定できない場合はBLOCKED候補とする。

---

### 7.1. ENH-E11 G01〜G10共通 Independent Test Discovery

**Applicability:** `GATE_ID`で指定された正式Gate G01〜G10。Test Agentのnormative WHATはそのGateでFreezeされた07のみであり、他Gateの07/G01のFCI・CLI事情を移植しない。40はWHERE/HOW。二軸はLifecycle (`enhancement/regression/characterization/benchmark/support/legacy`)、Layer (`unit/contract/integration/frontend/browser_e2e`)。`regression-like assertion != tests/regression lifecycle authority`。

1. **現物の探索:** Fixed Trial Candidate SHAのcheckoutで、まず`tests/enhancement/enh_e11/<gate>/`（`GATE_ID`小文字）、次に当該07のprotected invariantsに必要な`tests/product/`、`tests/integration/`、`tests/scientific/`、`tests/browser_e2e/`、昇格済み`tests/regression/`等を探索。物理Path/commandは旧Reportでなくcurrent checkoutから発見し、存在・collection・conftest/fixtures・marker・runner/環境を実行前に確認する。
2. **Gate固有証明:** Layerは当該07のmandatory primary proofに従う。G01ではCLI-onlyでunit/contract/integration、FCI/Graph/実FS/独立PAG referenceが対象でBrowser E2Eは不要。**G02〜G10はG01と同一ではなく**、当該07がfrontend/Browser E2Eをmandatoryとした場合は必要なcurrent critical journeyを実行する。`component/`・`scientific/`は新Gate-local標準Layerとして強制しない。科学的方法の真偽は独立Oracle・実測で確認し、Backendの自己出力を正解としない。
3. **Regression authority:** 対象Gateに関係する旧Product Suiteは現配置のまま実行。新規E11 Testが既存behaviorを検証しても初期Lifecycleはenhancement。`tests/regression/`への昇格は恒久Product invariantの独立PROMOTE承認後のみ。全repo test migrationはE12以降。
4. **証跡:** Gate Test Item / DD ID / AC / Lifecycle / Layer / collected actual Path+command / Source+Fixture+Env SHA / actual OS/FS/Backend/UI条件 / expected vs observed / positive+negative / PASS・FAIL・BLOCKEDを記録。必須テストが収集不能、環境不適格、独立科学Reference欠落なら`BLOCKED`。Mock-onlyを実Fs/科学/BrowserのPASSにしない。
5. **障害分類:** `PRODUCT_DEFECT / TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN`。Product invariant違反の実証時はFAIL候補、Test-side/UNKNOWNで評価不能ならBLOCKED。**Independent Test Agentはproduction/test code、runner、CI、06/07を修理しない。** 別のrepair owner/actionへ渡し、E9 G02用31をE11標準で流用しない。
6. **Fixed Candidate差分:** Test-side-onlyの修正でProduct Candidateを自動Freezeし直さない。`PRODUCT_SEMANTIC_CHANGE / TEST_IMPLEMENTATION_CHANGE / TEST_ORCHESTRATION_CHANGE / TEST_INFRASTRUCTURE_CHANGE / DOCUMENTATION_ONLY`を識別し、Product意味変更の可能性を排除できないときだけCandidate identity BLOCKEDとする。

## 8. Prohibited actions

本 Agent は以下を変更してはならない。

* production code
* automated test code
* migration definition
* dependency definition
* Package implementation
* Acceptance Criteria
* 06 / 07 / Pxx
* architecture / planning contract

以下も禁止する。

* FAIL を回避するための test 修正
* expected value の変更
* assertion の弱体化
* error suppression
* skip / xfail の追加
* Candidate implementation の修正
* Acceptance Criteria の再解釈による PASS 化
* 他資料を参照した仕様補完

implementation defect を発見した場合、本 Agent は修正せず **FAIL evidence として記録する**。

---

## 9. Test evidence reports

以下 directory に current Trial の independent verification evidence を作成せよ。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
30_test_report/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
```

07 に定義された各 Test Item について、以下の filename convention を使用する。

```text
ENH-E11-{{GATE_ID}}_{{TRIAL_NO}}__<TEST_ITEM_ID>.md
```

例:

```text
ENH-E11-G00_01__001_candidate_identity.md
ENH-E11-G00_01__999_gate_decision.md
```

各 item report は、その Test Item の raw evidence と判定を単独で追跡可能な状態にする。

Browser E2E Test ItemがFAIL / BLOCKEDの場合は、利用可能な範囲で以下も保存・参照する。

* Playwright trace / screenshot / video
* browser console / page errors
* relevant network request / response（URL / method / request body / response status / response body。secretはredact）
* API / worker logs
* Compose / service state
* exact command / timestamp
* failed synchronization point / assertion
* failure classification

HTTP status単体をroot causeとせず、intentional negative responseとactual failing assertionを区別する。

---

## 10. Gate Decision — Test Item 999

すべての必要 Test Item の実行後、07 の Gate Decision semantics に従って、

```text
999_gate_decision
```

を作成せよ。

Gate Decision は以下のいずれかとする。

```text
PASS
FAIL
BLOCKED
```

### PASS

07 が要求するすべての Mandatory Acceptance Criteria、protected regression、Transition Debt audit、candidate identity audit が PASS している場合のみ許可する。

Coding Agent の、

```text
READY_FOR_TEST
PACKAGE_READY
self-verification PASS
```

を Gate PASS evidence として扱ってはならない。

### FAIL

Fixed Trial Candidate の product / contract behavior が、有効な 07 Acceptance Criteria に違反している場合。

FAIL の場合、failure を implementation defect として evidence 化する。Browser E2E failureではproduct / contract violationをsupportするevidenceとdiagnostic classificationを併記する。

Test Agent 自身で修正してはならない。

### BLOCKED

candidate identity、contract ambiguity、environment / prerequisite 等により Acceptance を判定できない場合。Browser E2Eのtest implementation / orchestration / environment defectまたはUNKNOWNによりproduct correctnessを判定できない場合もここに含む。

BLOCKED を product FAIL に自動変換してはならない。

可能な場合は blocker code を明記する。

例:

```text
BLOCKED_CONTRACT_AMBIGUITY
BLOCKED_CANDIDATE_IDENTITY
BLOCKED_REPOSITORY_STATE
BLOCKED_PREREQUISITE
```

---

## 11. Test evidence commit and push

Test Item report 作成後、current Trial の test evidence のみを stage せよ。

```bash
git add docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/30_test_report/{{GATE_ID}}/Trial{{TRIAL_NO}}/
git status
git diff --cached --stat
git diff --cached
```

production / test / migration / dependency / implementation file が staged されている場合は commit してはならない。

問題がなければ test evidence commit を作成する。

```bash
git commit -m "ENH-E11 Gate {{GATE_ID}} Trial {{TRIAL_NO}} independent verification evidence"
git push -u causal-atelier prototype/ariadne_mvp
git rev-parse HEAD
git status
```

取得した exact SHA を、

```text
TEST_EVIDENCE_COMMIT_SHA
```

として記録する。

---

## 12. Verified state promotion boundary

Gate Decision が `PASS` の場合のみ、verified state promotion を許可する。

`FAIL` または `BLOCKED` の場合、verified state promotion を許可してはならない。

本 Agent は、別途明示的な workflow instruction がない限り 等を自律的に変更してはならない。

Gate Decision と promotion eligibility を report するところまでを責務とする。

---

## 13. Final status

最終応答では、Gate Decision または BLOCKED reason を明示せよ。

PASS の場合:

```text
PASS
GATE_ID
TRIAL_NO
FIXED_TRIAL_CANDIDATE_SHA
TEST_EVIDENCE_COMMIT_SHA
999_gate_decision report path
verification summary
PROMOTION_ALLOWED
```

FAIL の場合:

```text
FAIL
GATE_ID
TRIAL_NO
FIXED_TRIAL_CANDIDATE_SHA
TEST_EVIDENCE_COMMIT_SHA
failed Test Item / Acceptance Criteria
Browser E2E failure classification（該当時）
999_gate_decision report path
PROMOTION_NOT_ALLOWED
```

BLOCKED の場合:

```text
BLOCKED_*
GATE_ID
TRIAL_NO
FIXED_TRIAL_CANDIDATE_SHA（取得できた場合）
blocker
Browser E2E failure classification（該当時）
completed Test Items
test report path
PROMOTION_NOT_ALLOWED
```

PASS / FAIL / BLOCKED の判定根拠は、必ず freeze 済み 07 と current Trial の independent evidence に紐付けること。

<!-- BEGIN MANAGED: EXECUTION_IDENTITY_CONTROL -->
## 3. Execution identity control

This prompt MUST be instantiated under `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/` before Agent execution. The template-side prompt MUST NOT be executed directly.

Enhancement-fixed values:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=prototype/ariadne_mvp
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
WORK_DIR_NAME=20261024_ENH-E11_causal_lifecycle_cli_expansion
```

Runtime values for this execution:

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

If any Enhancement-fixed value remains unresolved in the Enhancement-side prompt, stop with `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED`. If required Runtime values are missing or ambiguous, stop with `BLOCKED_EXECUTION_UNRESOLVABLE`.
<!-- END MANAGED: EXECUTION_IDENTITY_CONTROL -->


## ENH-E11 S02 Owner承認8項目：Operator実行時の統一保護（2026-11-22）

この40はAgent運用・Discovery/WHERE/HOW・Evidenceのauthorityであり、担当Gateの凍結済み06/Pxx（Coding WHAT）や07（Independent Test WHAT）の科学Methodの意味を変更しない。実行前に最新のOwner `combined_review/137_20261122_dec_s02_eight_simplifications_owner_approval.md`、G01〜G10 06/07/Pxxの同一固定SHA、該当Gateの正式Freeze/Coding Authorization（G01ではOwner暫定S10と別Owner限定S11の両記録）を照合し、まだDRAFT/未承認ならCoding/Test Agentを起動せず`BLOCKED_CONTRACT_NOT_FROZEN`を報告。実装指示書の署名やMethod権限が矛盾する場合、Agentが外部資料で勝手に補完してはならない。

保護するS02条件：①Local row出力はStudy `privacy.row_export_requested=true`が唯一の実行者明示opt-in。追加`--allow-row-level-export`、`cli_row_flag`、Study`policy_ref`、第三者署名PolicyVerifier/Anchorを生成しない。false/省略は個票なし。G05のみnonroot same-UID private ext4/XFS Verified Root/Method ApprovedRowSchema/row-column-byte-memory caps/G01 stagingに適合した場合にbounded Parquetを生成し、未認可時row Source反復0・row bytes0、aggregateやlogsへ漏洩なし。②40 Method×5 Profileはstrict common schema＋exact Method overlay・200 SHA/parity＋Method独自科学適格性で検証し、未検証ならfail-closed。③G10は全41 Methodの有効な独立Science evidenceを照合し、共有Kernel、schema、Lock、Backend、fixture、Reference、AC、Policy等の推移的なbehavior dependency closureが完全不変と立証できる証拠だけ再利用。変更/不明な対象Methodは再実行またはBLOCK。最終Fixed Candidateのcross-Gate integrationと旧v2保護は毎回必要。④共通bounded RowWriter/RowSchema。⑤E11 Local Graphは科学content hashで識別しProduct GraphVersion DBへの新規lookup/write/edit/FIXは行わず、Product Version IDs=nullを保つ。⑥G01 FS proofは重要不変条件の有界正負例であり障害全順列や電源断保証は不要。⑦新テストはGate/Pxxに対応し、Product回帰・既存ABIテストは変更影響閉包で選択。影響不明なら実行またはBLOCK、無関係なProduct全SuiteやE2Eを機械的に強制しない。⑧NFR-034の将来顧客配布は`DEFERRED`、社内OSS義務は継続。Backendの4つの分離ENVは実Python3.12/lock/API/fit/CIで照合し、未実行・unknownをPASSと呼ばない。

**Independent Test Agent固有：** Test Itemごとに既存accepted reference evidenceを独立検証する。G10では全41証拠の完全性と差分/影響再実行の適否、変更/未知閉包負例、実際のcross-Gate integrationを別判定。被験Sourceの実装変更・新閾値・事後的科学Target変更をしない。独立Review Agent/独立科学Oracleの未実施をmockで置換せずBLOCKED。
