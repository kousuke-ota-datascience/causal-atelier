# FAIL Rework Coding Agent Prompt

**ENH-E11 Gate別Authorization Preflight（Owner DEC-PREPCODE-01=B、G01のみDEC-G01-EXEC-01追加採用）:** 全Gate402件のSHA索引は独立S09 PASSではない。**G01専用例外**：独立S09・B02/B04実Python3.12・B05 MAG/PAG/BKはCoding Entryの事前PASSを要求せず、G01_999までの必須実測/独立審査として`EXTERNAL_PENDING/NOT_RUN`で保持する。Coding開始に必要なのは、G01/common 06/Pxx/07等のAuthor契約整合、未検証例外の明示、**Ownerが別途発行した暫定G01-S10（対象正本full SHAと07/999 obligationsを固定）**、さらに**Ownerが別途発行した限定G01-S11（許可G01/P01〜P05、source/lock/paths）**の両方。Ownerの方針採用そのものはFreeze・Coding Authorizationではない。G01で実装できるのは許可WPと開発者テストだけ、未知の科学真値・CI/BK/Backend状態をPASSへ昇格しない。non-null BKは有効独立remedyまでFCI呼出前typed deny。G01_999は独立S09、B02/B04、独立Graph/BK B05、実FS/Reader/T2/T3/旧Product回帰/独立07が未完ならBLOCKED。**G02〜G10は従来DEC-PREPCODE-01=BのGate別独立S09→Owner S10→別Owner S11と実上流999 PASSを厳守**。どのGateもOwner承認証拠欠損・SHA不一致・契約変更なら`BLOCKED_CODING_AUTHORIZATION`、Agentを起動しない。現在G01の暫定S10/限定S11は両方未承認。

この文書は formal FAIL 後の rework 専用 entry prompt である。

実行時に Operator から以下を受け取る。

```text
GATE_ID=<Gate ID>
TRIAL_NO=<two-digit Trial number>
```

Template / Enhancement 固定値:

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E11
ENHANCE_SHORT_ID=E11
BRANCH_NAME=feature/ariadne_mvp_e11
REMOTE_NAME=causal-atelier
WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion
```

## 1. Current Trial Remediation Contract

current Trial の normative remediation contract は、必ず以下の exact path で解決する。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
10_enhance_instruction/<GATE_ID>/
08_ENH-E11_<GATE_ID>_<TRIAL_NO>_Remediation_Instruction.md
```

この exact file が存在しない場合:

```text
BLOCKED_REMEDIATION_CONTRACT_MISSING
```

旧 Trial の 08、別名の 08、original 06/Pxx/07 を代用してはならない。

current 08 をdirect executionへ使用するため、以下をpreflightで確認する。

```text
Remediation Mode: CONSOLIDATED
Execution Mode: SINGLE_EXECUTION
```

どちらかを満たさない場合、本promptで実装を開始してはならない。

```text
BLOCKED_REMEDIATION_CONTRACT_NOT_SELF_CONTAINED
```

DELTA 08からoriginal 06/07を読んで仕様を補完してはならない。Rxx remediation Work Packageが必要な場合もnormal Pxx promptへfallbackしない。


## 2. Normative Source Isolation

freeze 済み current Trial 08 だけを normative source とする。
repository は implementation substrate として調査してよい。

original 06/Pxx/07、旧 Trial report、ADR、他 Gate、過去 Enhancement、external Web を仕様補完に使わない。

required correction が current 08 だけで一意に決まらない場合:

```text
BLOCKED_CONTRACT_AMBIGUITY
```

## 3. SINGLE_EXECUTION Rework Rule

08 が:

```text
Execution mode: SINGLE_EXECUTION
```

を宣言している場合、original Work Package chain を再実行してはならない。

禁止:

- current Trial P01/P02/P03 の再実行
- old Package checkpoint SHA の再利用
- previous failed candidate の再提出
- normal Work Package Candidate Assembly を rework implementation の代替として使用すること

## 4. Implementation and Verification

Browser E2Eがformal FAILのtriggerである場合、実装開始前にfailed 999 / Test Item evidenceがproduct / contract violationを支持していることを確認する。failure classificationが`TEST_IMPLEMENTATION_DEFECT / TEST_ORCHESTRATION_DEFECT / TEST_ENVIRONMENT_DEFECT / UNKNOWN`のみでproduct violationがverifiedされていない場合、production reworkを開始せず`BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE`として停止する。

08 の required correction と protected behavior を実装し、mandatory Coding-side verification をすべて実行する。Browser E2Eを再検証する場合も、未検証仮説をroot causeとして修正を反復せず、failure point / actual observable state / expected state / evidenceを確定してからscope内修正を行う。

禁止:

- failing test の削除
- assertion の弱体化
- skip / xfail
- original contract の改変
- literal input だけを hard-code して拒否する workaround

### 4.1. ENH-E11 G01〜G10共通 Remediation Test Policy

本Promptは`GATE_ID`で特定された正式Gate G01〜G10の**正式FAILと承認済みcurrent 08**がある場合のみ適用する。Test-side-only BLOCKEDならproduction remediationを実行しない。08がWHAT、本40がWHERE/HOW。Lifecycle (`enhancement/regression/characterization/benchmark/support/legacy`)とLayer (`unit/contract/integration/frontend/browser_e2e`)は独立。`regression-like assertion != tests/regression lifecycle authority`。

- 承認08のScope内で新規/materially rebuiltしたTestは`tests/enhancement/enh_e11/<gate>/<layer>/`（GATE_IDをlowercase）へ置き、Layerは当該08/06/07で要求された証明対象に従う。`component/`・`scientific/`を新Gate-local標準Layerにしない。G01ではCLI/実FS/FCIが対象だが、**G02〜G10ではそれを強制しない**。UI Gateで必要なfrontend/Browser E2Eは当該Gateのcritical journeyに限定する。
- 当該Gateの旧Product invariantsを保護する`tests/product/`等の現存Suiteを現配置で実行。`tests/regression/`への無断PROMOTE、archive、全repo Test migrationは禁止。昇格は恒久Invariantの別semantic判断、全件整理はE12以降。必要なTest移動ではimport/fixture/collection/CI/Docker/evidence pathをAtomicに更新する。
- 08/DD/ACと現行Checkoutのcollected Testを照合し、実Path、Command、Lifecycle、Layer、Source/Fixture SHAとObserved結果を記録。Test-side defectやUNKNOWNでProduct違反未証明なら`BLOCKED_REMEDIATION_HANDOFF_INCOMPLETE`。独立Test Agentは修理しない。Test-only差分でProduct Candidateを自動再Freezeしない。

## 5. Semantic Implementation Checkpoint

semantic change を commit し、exact SHA を implementation checkpoint として固定する。

08 に `PREVIOUS_FAILED_CANDIDATE_SHA` が定義されている場合:

```bash
git diff --name-only   <PREVIOUS_FAILED_CANDIDATE_SHA>..<IMPLEMENTATION_CHECKPOINT_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

を必ず実行する。

08 が要求する semantic remediation が diff に存在しない場合:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

previous failed candidate と同一 SHA を採用してはならない。

## 6. Fixed Trial Candidate

required verification が PASS し required semantic remediation diff が存在する場合のみ:

```text
FIXED_TRIAL_CANDIDATE_SHA=<IMPLEMENTATION_CHECKPOINT_SHA>
```

として freeze する。

formal FAIL / SINGLE_EXECUTION Trial では FAIL Rework Coding Agent 自身が candidate freeze を行う。

## 7. Canonical Implementation Completion Report

以下の exact path に生成する。

```text
docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/
20_implementation_reports/<GATE_ID>/Trial<TRIAL_NO>/
E11-<GATE_ID>_<TRIAL_NO>__implementation_completion.md
```

最低限以下を記録する。

```text
GATE_ID
TRIAL_NO
Execution status
PREVIOUS_FAILED_CANDIDATE_SHA
FIXED_TRIAL_CANDIDATE_SHA
changed production files
changed automated test files
executed verification
Blocker / remaining work
```

`READY_FOR_TEST` の場合:

- fixed candidate != previous failed candidate
- required semantic diff != empty
- required verification = PASS
- blocker = NONE

を満たす。

## 8. Evidence Commit / Push

Completion Report を evidence-only commit として commit / push する。

Completion Report commit 後 `HEAD != FIXED_TRIAL_CANDIDATE_SHA` は許容するが、candidate から evidence HEAD まで semantic implementation change がないことを確認する。

## 9. Final Status

成功時:

```text
## READY_FOR_TEST

- GATE_ID: <GATE_ID>
- TRIAL_NO: <TRIAL_NO>
- PREVIOUS_FAILED_CANDIDATE_SHA: <SHA>
- FIXED_TRIAL_CANDIDATE_SHA: <new SHA>
- COMPLETION_REPORT: <canonical exact path>
- EVIDENCE_COMMIT_SHA: <SHA>
- Working tree: clean
- Push: completed
```

Gate PASS / FAIL、promotion 可否は判定しない。

<!-- BEGIN MANAGED: EXECUTION_IDENTITY_CONTROL -->
## 3. Execution identity control

This prompt MUST be instantiated under `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/` before Agent execution. The template-side prompt MUST NOT be executed directly.

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
REMEDIATION_PACKAGE_ID={{REMEDIATION_PACKAGE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

If any Enhancement-fixed value remains unresolved in the Enhancement-side prompt, stop with `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED`. If required Runtime values are missing or ambiguous, stop with `BLOCKED_EXECUTION_UNRESOLVABLE`.
<!-- END MANAGED: EXECUTION_IDENTITY_CONTROL -->


## ENH-E11 S02 Owner承認8項目：Operator実行時の統一保護（2026-11-22）

この40はAgent運用・Discovery/WHERE/HOW・Evidenceのauthorityであり、担当Gateの凍結済み06/Pxx（Coding WHAT）や07（Independent Test WHAT）の科学Methodの意味を変更しない。実行前に最新のOwner `combined_review/137_20261122_dec_s02_eight_simplifications_owner_approval.md`、G01〜G10 06/07/Pxxの同一固定SHA、該当Gateの正式Freeze/Coding Authorization（G01ではOwner暫定S10と別Owner限定S11の両記録）を照合し、まだDRAFT/未承認ならCoding/Test Agentを起動せず`BLOCKED_CONTRACT_NOT_FROZEN`を報告。実装指示書の署名やMethod権限が矛盾する場合、Agentが外部資料で勝手に補完してはならない。

保護するS02条件：①Local row出力はStudy `privacy.row_export_requested=true`が唯一の実行者明示opt-in。追加`--allow-row-level-export`、`cli_row_flag`、Study`policy_ref`、第三者署名PolicyVerifier/Anchorを生成しない。false/省略は個票なし。G05のみnonroot same-UID private ext4/XFS Verified Root/Method ApprovedRowSchema/row-column-byte-memory caps/G01 stagingに適合した場合にbounded Parquetを生成し、未認可時row Source反復0・row bytes0、aggregateやlogsへ漏洩なし。②40 Method×5 Profileはstrict common schema＋exact Method overlay・200 SHA/parity＋Method独自科学適格性で検証し、未検証ならfail-closed。③G10は全41 Methodの有効な独立Science evidenceを照合し、共有Kernel、schema、Lock、Backend、fixture、Reference、AC、Policy等の推移的なbehavior dependency closureが完全不変と立証できる証拠だけ再利用。変更/不明な対象Methodは再実行またはBLOCK。最終Fixed Candidateのcross-Gate integrationと旧v2保護は毎回必要。④共通bounded RowWriter/RowSchema。⑤E11 Local Graphは科学content hashで識別しProduct GraphVersion DBへの新規lookup/write/edit/FIXは行わず、Product Version IDs=nullを保つ。⑥G01 FS proofは重要不変条件の有界正負例であり障害全順列や電源断保証は不要。⑦新テストはGate/Pxxに対応し、Product回帰・既存ABIテストは変更影響閉包で選択。影響不明なら実行またはBLOCK、無関係なProduct全SuiteやE2Eを機械的に強制しない。⑧NFR-034の将来顧客配布は`DEFERRED`、社内OSS義務は継続。Backendの4つの分離ENVは実Python3.12/lock/API/fit/CIで照合し、未実行・unknownをPASSと呼ばない。

**Control/Assembly/Remediation固有：** 影響差分とprotected Product invariantの根拠、固定full SHA、独立RunnerとReviewer's責務分離を持つ。証拠が不完全ならReady/Passを捏造せず適切にBLOCK。
