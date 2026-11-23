# Work Package Coding Agent Prompt

**ENH-E11 Gate別Authorization Preflight（Owner DEC-PREPCODE-01=B、G01のみDEC-G01-EXEC-01追加採用）:** 全Gate402件のSHA索引は独立S09 PASSではない。**G01専用例外**：独立S09・B02/B04実Python3.12・B05 MAG/PAG/BKはCoding Entryの事前PASSを要求せず、G01_999までの必須実測/独立審査として`EXTERNAL_PENDING/NOT_RUN`で保持する。Coding開始に必要なのは、G01/common 06/Pxx/07等のAuthor契約整合、未検証例外の明示、**Ownerが別途発行した暫定G01-S10（対象正本full SHAと07/999 obligationsを固定）**、さらに**Ownerが別途発行した限定G01-S11（許可G01/P01〜P05、source/lock/paths）**の両方。Ownerの方針採用そのものはFreeze・Coding Authorizationではない。G01で実装できるのは許可WPと開発者テストだけ、未知の科学真値・CI/BK/Backend状態をPASSへ昇格しない。non-null BKは有効独立remedyまでFCI呼出前typed deny。G01_999は独立S09、B02/B04、独立Graph/BK B05、実FS/Reader/T2/T3/旧Product回帰/独立07が未完ならBLOCKED。**G02〜G10は従来DEC-PREPCODE-01=BのGate別独立S09→Owner S10→別Owner S11と実上流999 PASSを厳守**。どのGateもOwner承認証拠欠損・SHA不一致・契約変更なら`BLOCKED_CODING_AUTHORIZATION`、Agentを起動しない。現在G01の暫定S10/限定S11は両方未承認。

## 1. Invocation parameters

Human / Orchestrator は実行前に以下を確定して与える。

```text
GATE_ID={{GATE_ID}}
PACKAGE_ID={{PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=feature/ariadne_mvp_e11
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
```

本実行では、上記の `GATE_ID`、`PACKAGE_ID`、`TRIAL_NO` を以降の placeholder に代入して実行せよ。

---

## 2. Responsibility boundary

本 Agent の責務は、指定された Work Package について、

1. repository state を確認する
2. assigned freeze 済み Pxx contract を正確に1件特定する
3. assigned Package scope のみを実装する
4. assigned Pxx が要求する focused verification を実行する
5. Package checkpoint を commit として固定する
6. Package checkpoint/status report を作成する
7. evidence を commit / push する
8. `PACKAGE_READY` または明示的な `BLOCKED_*` 状態で終了する

ことである。

本 Agent は以下を行わない。

* 他 Package の実行
* 次 Package の選択
* Gate orchestration
* Fixed Trial Candidate の assembly
* Gate PASS / FAIL Decision

ただし assigned Pxx が明示的に別の責務を要求する場合は、その Pxx の記載を優先する。

---

## 3. Repository preflight

実装開始前に以下を実行せよ。

```bash
git branch --show-current
git status --porcelain
git rev-parse HEAD
```

以下を確認する。

* current branch が `feature/ariadne_mvp_e11` であること
* working tree が clean であること
* 実行開始時 HEAD を `START_SHA` として記録すること

current branch が異なる場合、または開始時点で uncommitted change が存在する場合は、既存変更を reset / checkout / restore / stash / commit してはならない。

その場合は実装を開始せず `BLOCKED_REPOSITORY_STATE` として終了せよ。


### Formal FAIL remediation route guard

current Trial に current Trial 用の frozen Remediation Contract が存在する場合、その Trial を通常 Work Package execution として実行してはならない。

formal FAIL 後の remediation Trial では `40_fail_remediation_01_fail_rework_coding_agent_prompt.md` を使用する。通常 Work Package execution を続行せず、以下で停止せよ。

```text
BLOCKED_EXECUTION_MODE_MISMATCH
```

old Package checkpoint を再利用して current Trial を完了扱いにしてはならない。

---

## 4. Assigned Work Package contract

以下 directory から、指定された `GATE_ID` および `PACKAGE_ID` に対応する freeze 済み Work Package contract を**正確に1件**特定せよ。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
10_enhance_instruction/
  {{GATE_ID}}/
    06_{{GATE_ID}}_{{PACKAGE_ID}}_*.md
```

semantic match が0件または複数存在する場合、任意のファイルを選択してはならない。

その場合は実装を開始せず停止せよ。

特定した **assigned Pxx のみ**を normative implementation contract とする。

以下を仕様補完のために読んではならない。

* Gate-level 06 Contract
* 07
* P00
* 他 Pxx
* 00〜30 の planning / analysis 文書
* ADR
* 過去 Enhancement
* issue
* 外部 Web

current repository の source / test / configuration / migration 等は、**implementation substrate を理解する目的では調査してよい**。

ただし repository の現状を仕様 authority として扱ってはならない。

> 実装方法を repository から発見してよい。
> required behavior を repository や別文書から発見してはならない。

assigned Pxx だけでは entry condition、scope、protected invariant、required behavior、acceptance criteria のいずれかを一意に判断できない場合、他資料へ探索を広げてはならない。

その場合は `BLOCKED_CONTRACT_AMBIGUITY` として停止せよ。

---

## 5. Package implementation

assigned Pxx に記載された Package scope のみを実装せよ。

以下を行ってはならない。

* 他 Package scope の実装
* contract に要求されない refactoring
* contract に要求されない architecture 変更
* protected invariant の変更
* unrelated cleanup
* speculative fix
* contract に存在しない仕様の補完
* verification を通すための期待値緩和
* failure の握り潰し

他 Package に関係する問題を発見しても、assigned Pxx が要求しない限り変更してはならない。

Package scope 内の実装を完了できない場合は `BLOCKED_IMPLEMENTATION` とする。

---

## 6. Focused verification

assigned Pxx が要求する focused verification をすべて実行せよ。

実行した command と結果を記録すること。

verification が失敗した場合は原因を調査し、assigned Package scope 内で修正可能なら修正して再実行してよい。

Browser E2E failureの場合、修正前に最低限 `failure point / actual observable state / expected state / candidate cause / supporting evidence` を確定する。未検証仮説をroot causeとして修正を反復しない。test implementation / orchestration / environment defectがassigned Package scope外なら、他Packageやtest harnessを便乗修正せず適切な`BLOCKED_*`として停止する。

以下によって verification failure を隠してはならない。

* test の削除
* assertion の弱体化
* expected value の恣意的変更
* error suppression
* skip / xfail 等の追加
* 他 Package scope の変更による回避

assigned Pxx の acceptance criteria を満たす状態に到達できない場合は `BLOCKED_IMPLEMENTATION` とする。

---

### 6.1. ENH-E11 G01〜G10共通 Test Architecture — Assigned Package

本PromptはG01〜G10のうち**当該Gate06がWORK_PACKAGE方式で、assigned Pxxが一意かつFreeze済み**の場合のみ使う。`GATE_ID`と`PACKAGE_ID`から当該GateのPxxを解決し、他Gateの06/Pxx/07から実装条件を推測しない。Assigned PxxがWHAT（Method、DD ID、正/負例、DoD）、本40はWHERE/HOWを所有する。独立テストの07をCoding Agentの仕様補完に使わない。

TestはLifecycle (`enhancement/regression/characterization/benchmark/support/legacy`) とLayer (`unit/contract/integration/frontend/browser_e2e`) の二軸で分類する。`regression-like assertion != tests/regression lifecycle authority`。

1. **配置:** 新規/materially rebuiltした担当Gate/Pxx Testは`tests/enhancement/enh_e11/<gate>/<layer>/`へ初期配置する。`<gate>`は実行時`GATE_ID`の小文字（G01→g01、G10→g10）。Layerは**担当Pxxが要求する証明対象**で選択し、`component/`と`scientific/`をGate-local標準Layerとして増設しない。`frontend`と`browser_e2e`はGate06/PxxがUI検証を要求する場合だけ使い、Browser E2Eはcritical connectivityに限定。
2. **Gate依存:** G01の場合はCLI-onlyでunit/contract/integration、FCI/Graph/Atomic FSが適用対象でありBrowser E2E不要。**G02〜G10で同じ制約や同じ科学的Method/Filesystemテストを要求してはならない**。他Gateは対応するassigned PxxにあるRequirement/DD/受入条件に従う。科学的Oracleが必要な場合も、Backendの自己出力を独立正解としない。
3. **既存Suite:** 担当Gateのprotected Product invariantを保護する`tests/product/`等の既存Suiteを現物から発見・実行し、関係のない旧Testを移動・archive・大量再編しない。新E11 Testの初期Lifecycleはenhancementで、`tests/regression/`に昇格するには明示的に恒久Product invariantを認定するPROMOTE decisionが必要。E11終了時Dispositionは`PROMOTE/REWRITE/MERGE/SPLIT/RETIRE/ARCHIVE/KEEP_ENHANCEMENT`、repo-wide整理はE12以降。
4. **実行:** Assigned Pxxの必要DD/Test IDごとに、current checkoutでFile存在・pytest collection・fixtures/conftest・marker・runner/依存/必要環境を確認して実行commandを確定する。過去のfilename/commandは受入Authorityではない。必須の実FS/Backend/Browser確認がmock-onlyや故障Runnerで実証できなければPASSとしない。
5. **変更境界:** Test moveはPxx scopeで許されたときだけpath/import/fixture/conftest/pytest/CI/Docker/build context/evidence pathを同一Batchで更新。Expectation緩和、skip/xfail、Scope外migration、独立Test Agentの修復権限代行は禁止。
6. **Evidence:** DD ID・Gate Test ID・Lifecycle・Layer・実Path/command・implementation/fixture/env SHA・正例/負例の観測結果・PASS/FAIL/BLOCKEDを記録。必須証拠が不足する場合は`BLOCKED_*`を記録し、Package completeをGate PASSやScience PASSと混同しない。

## 7. Package checkpoint commit

Package implementation と focused verification が完了したら、変更内容を確認する。

```bash
git status
git diff --stat
git diff
```

今回の assigned Package scope に属する変更だけを stage せよ。

`git add .` または scope 外変更を含む一括 stage を行ってはならない。

stage 後、以下を確認する。

```bash
git diff --cached --stat
git diff --cached
git status
```

問題がなければ Package checkpoint を commit する。

```bash
git commit -m "ENH-E11 Gate {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} implementation checkpoint"
git rev-parse HEAD
```

取得した exact SHA を、

```text
PACKAGE_CHECKPOINT_SHA
```

として記録する。

`PACKAGE_READY` とする場合、未commitの Package implementation change を残してはならない。

---

## 8. Package checkpoint/status report

以下に Package checkpoint/status report を作成せよ。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
20_implementation_reports/
  {{GATE_ID}}/
    Trial{{TRIAL_NO}}/
      packages/
        E11-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}__status.md
```

必要な directory が存在しない場合は作成してよい。

report には最低限以下を記録する。

* `PROJECT_NAME`
* `ENHANCE_ID`
* `GATE_ID`
* `PACKAGE_ID`
* `TRIAL_NO`
* normative Pxx contract path
* `START_SHA`
* Package status
* changed files
* implementation summary
* executed verification commands
* verification results
* `PACKAGE_CHECKPOINT_SHA`
* blocker / remaining work（存在する場合）

`PACKAGE_READY` の場合、`PACKAGE_CHECKPOINT_SHA` は必須である。

BLOCKED の場合、checkpoint が存在しなければ SHA を捏造してはならない。

---

## 9. Evidence commit and push

Package checkpoint/status report 作成後、evidence file のみを stage せよ。

```bash
git add docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/20_implementation_reports/{{GATE_ID}}/Trial{{TRIAL_NO}}/packages/E11-{{GATE_ID}}_{{TRIAL_NO}}_{{PACKAGE_ID}}__status.md
git status
git diff --cached
```

問題がなければ evidence commit を作成する。

```bash
git commit -m "ENH-E11 Gate {{GATE_ID}} Trial {{TRIAL_NO}} {{PACKAGE_ID}} implementation evidence"
git push -u causal-atelier feature/ariadne_mvp_e11
git log -2 --oneline
git status
```

Package checkpoint commit と evidence commit は別 commit でよい。

Package report に記録する checkpoint identity は、**evidence commit ではなく `PACKAGE_CHECKPOINT_SHA`** である。

---

## 10. Fixed Trial Candidate boundary

本 Agent は、assigned Pxx に明示されない限り Fixed Trial Candidate を assemble してはならない。

特に以下を行ってはならない。

* 全 Package 完了を推測する
* 他 Package の checkpoint を検証・統合する
* Gate-wide verification を独自に追加する
* Fixed Trial Candidate SHA を生成する
* implementation completion report を Gate completion として作成する
* Test Agent を起動する
* 次 Package を自律的に開始する

`PACKAGE_READY` は **assigned Package の実装と focused verification が完了したことだけ**を意味する。

`PACKAGE_READY` を Gate PASS、Gate complete、READY_FOR_TEST と表現してはならない。

---

## 11. BLOCKED / interrupted execution

実装開始後に完了不能となった場合も、可能な限り Package checkpoint/status report を作成または更新し、以下を記録せよ。

* どこまで実行したか
* 何を変更したか
* どの verification を実行したか
* failure / blocker
* uncommitted change の有無
* checkpoint SHA が存在するか
* 再開時に必要な情報

BLOCKED 状態で incomplete implementation を Package checkpoint として commit してはならない。

既存変更を破壊して clean state を作ってはならない。

---

## 12. Final status

最終応答では、必ず以下のいずれかを明示せよ。

```text
PACKAGE_READY
BLOCKED_CONTRACT_AMBIGUITY
BLOCKED_REPOSITORY_STATE
BLOCKED_IMPLEMENTATION
BLOCKED_EXECUTION_MODE_MISMATCH
```

`PACKAGE_READY` の場合は最低限以下を報告する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
START_SHA
PACKAGE_CHECKPOINT_SHA
EVIDENCE_COMMIT_SHA
Package report path
verification summary
```

BLOCKED の場合は最低限以下を報告する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
START_SHA
BLOCKED status
blocker
changed / uncommitted files
report path（作成できた場合）
```

本 Agent は Package complete を Gate PASS と表現してはならない。

<!-- BEGIN MANAGED: EXECUTION_IDENTITY_CONTROL -->
## Execution identity control

This template-side prompt is an authoring source and MUST NOT be executed directly. Before execution it MUST be instantiated under `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/`.

Enhancement-fixed values:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=feature/ariadne_mvp_e11
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
WORK_DIR_NAME=20261024_ENH-E11_causal_lifecycle_cli_expansion
```

Runtime values for this execution:

```text
GATE_ID={{GATE_ID}}
PACKAGE_ID={{PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

If any Enhancement-fixed value remains unresolved in the Enhancement-side prompt, stop with `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED`. If any required Runtime value is missing or ambiguous, stop with `BLOCKED_EXECUTION_UNRESOLVABLE`.
<!-- END MANAGED: EXECUTION_IDENTITY_CONTROL -->

<!-- BEGIN MANAGED: PACKAGE_REPORT_CANONICAL_STATE -->
### Canonical package completion metadata

`PACKAGE_READY` is the Coding Agent terminal outcome label. Canonical dependency/candidate semantics use the package report fields instead of the literal outcome label.

```text
Gate: {{GATE_ID}}
Package: {{PACKAGE_ID}}
Trial: {{TRIAL_NO}}
State: PACKAGE_COMPLETE
```

Markdown decoration is non-semantic. The dependency resolver / Candidate Assembly / preflight MUST use these semantic fields and MUST NOT use `PACKAGE_READY` as a workflow cursor.
<!-- END MANAGED: PACKAGE_REPORT_CANONICAL_STATE -->


## ENH-E11 S02 Owner承認8項目：Operator実行時の統一保護（2026-11-22）

この40はAgent運用・Discovery/WHERE/HOW・Evidenceのauthorityであり、担当Gateの凍結済み06/Pxx（Coding WHAT）や07（Independent Test WHAT）の科学Methodの意味を変更しない。実行前に最新のOwner `combined_review/137_20261122_dec_s02_eight_simplifications_owner_approval.md`、G01〜G10 06/07/Pxxの同一固定SHA、該当Gateの正式Freeze/Coding Authorization（G01ではOwner暫定S10と別Owner限定S11の両記録）を照合し、まだDRAFT/未承認ならCoding/Test Agentを起動せず`BLOCKED_CONTRACT_NOT_FROZEN`を報告。実装指示書の署名やMethod権限が矛盾する場合、Agentが外部資料で勝手に補完してはならない。

保護するS02条件：①Local row出力はStudy `privacy.row_export_requested=true`が唯一の実行者明示opt-in。追加`--allow-row-level-export`、`cli_row_flag`、Study`policy_ref`、第三者署名PolicyVerifier/Anchorを生成しない。false/省略は個票なし。G05のみnonroot same-UID private ext4/XFS Verified Root/Method ApprovedRowSchema/row-column-byte-memory caps/G01 stagingに適合した場合にbounded Parquetを生成し、未認可時row Source反復0・row bytes0、aggregateやlogsへ漏洩なし。②40 Method×5 Profileはstrict common schema＋exact Method overlay・200 SHA/parity＋Method独自科学適格性で検証し、未検証ならfail-closed。③G10は全41 Methodの有効な独立Science evidenceを照合し、共有Kernel、schema、Lock、Backend、fixture、Reference、AC、Policy等の推移的なbehavior dependency closureが完全不変と立証できる証拠だけ再利用。変更/不明な対象Methodは再実行またはBLOCK。最終Fixed Candidateのcross-Gate integrationと旧v2保護は毎回必要。④共通bounded RowWriter/RowSchema。⑤E11 Local Graphは科学content hashで識別しProduct GraphVersion DBへの新規lookup/write/edit/FIXは行わず、Product Version IDs=nullを保つ。⑥G01 FS proofは重要不変条件の有界正負例であり障害全順列や電源断保証は不要。⑦新テストはGate/Pxxに対応し、Product回帰・既存ABIテストは変更影響閉包で選択。影響不明なら実行またはBLOCK、無関係なProduct全SuiteやE2Eを機械的に強制しない。⑧NFR-034の将来顧客配布は`DEFERRED`、社内OSS義務は継続。Backendの4つの分離ENVは実Python3.12/lock/API/fit/CIで照合し、未実行・unknownをPASSと呼ばない。

**Coding Agent固有：** 担当06/Pxxで決められたstrict signatures、Method共通化・個別overlay、Operation/Estimand/Output/Inferenceを変更せず実装する。許可されないMethodは`METHOD_PROFILE_UNAVAILABLE`等のtyped fail-closed。自前のScience PASS、Gate999、フラグ/ポート/Factoryの復活は禁止。
