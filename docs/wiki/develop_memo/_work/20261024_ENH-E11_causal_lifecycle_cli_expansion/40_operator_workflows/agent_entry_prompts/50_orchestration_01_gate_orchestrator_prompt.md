# Gate Orchestrator Prompt

**ENH-E11 Gate別Authorization Preflight（Owner DEC-PREPCODE-01=B、2026-11-22採用）:** 全Gate402 source inventoryのSHA一致は全Gate独立S09 PASSではない。対象`GATE_ID`に対する共通E11不変条件＋対象06/Pxx/07・Method/Profile・実際の上流依存閉包の**独立S09 verdict**、Owner**当該Gate S10 Contract Freeze（full reviewed SHA）**、Owner**当該Gate S11 Coding Authorization**を別々の証拠で確認する。G02以降は実際の依存Gate **999 PASS**と不変closureをS11起動条件に加える（S09文書レビュー準備自体は先行Gate999を待たなくてもよい）。証拠欠損・違うSHA・dirty/変化した共通契約・未Freezeなら`BLOCKED_CODING_AUTHORIZATION`、実装/テスト再実行/修復/Orchestrationを開始しない。G01は先行999なし、対象P1-M06 FCI/ENV-BASE/共通Wire+Publicationのみ。候補依存T2/T3・FS・実Backend統合はS11後のIndependent 07/999で必須。**現在、全Gate S10/S11は未承認。**

この文書は、通常 `WORK_PACKAGE` Gate 全体を Human が `GATE_ID + TRIAL_NO` で起動するための control-plane entry prompt である。

Gate Orchestrator は実装内容を決めない。各 Agent の normative contract を増やさない。

## 1. Invocation parameters

```text
GATE_ID={{GATE_ID}}
TRIAL_NO={{TRIAL_NO}}
```

固定値は `00_variable_conventions.md` に従う。

## 2. Responsibility boundary

責務:

1. repository preflight を行う。
2. Gate の execution mode と required Package list を一意に解決する。
3. required Package を規定順に1つずつ Work Package Coding Agent へ割り当てる。
4. `PACKAGE_READY` / `BLOCKED_*` を監視する。
5. Package failure / BLOCKED 時に無条件で次 Package へ進まない。
6. retry / stop / Human escalation を行う。
7. 全 required Package 完了後、Candidate Assembly Agent を起動する。
8. `READY_FOR_TEST` または blocker を Human へ報告する。

責務外:

- Package implementation
- Package checkpoint の意味変更
- candidate semantic validation
- independent verification
- Gate PASS / FAIL Decision
- formal FAIL remediation の通常 Work Package route への差し戻し

## 3. Execution flow

```text
P01 Coding Agent
  -> PACKAGE_READY
P02 Coding Agent
  -> PACKAGE_READY
...
Pn Coding Agent
  -> PACKAGE_READY
Candidate Assembly Agent
  -> READY_FOR_TEST
```

各 Package は1回の Agent execution につき1 Package とする。

### 3.1. ENH-E11 G01〜G10共通 Routing / Test Readiness

**実行範囲:** 正式Gate IDはG01〜G10。`GATE_ID`ごとに当該GateのFreeze済み06から`Execution mode`、Required Package Set、依存関係を解決する。**G01はWORK_PACKAGE/P01〜P05だが、G02〜G10が同じPackage数・Mode・検証対象であるとは推定しない。** 当該Gateの06/07/Packageが未作成・未Freeze、Owner Coding Authorization未発行なら`BLOCKED_EXECUTION_UNRESOLVABLE`で停止し、G01の契約を流用しない。

テスト分類はLifecycle (`enhancement/regression/characterization/benchmark/support/legacy`)とLayer (`unit/contract/integration/frontend/browser_e2e`)の二軸。`regression-like assertion != tests/regression lifecycle authority`。各Gateの06/Pxx/07がWHAT、40がWHERE/HOW。

- 本Gate Orchestrator自身はWORK_PACKAGE mode専用。対象Gate06がSINGLE_EXECUTIONを指定したら、**このOrchestratorでは起動せず** `BLOCKED_EXECUTION_MODE_MISMATCH`で停止し、Humanに単一実行用の`10_normal_execution_01_single_execution_coding_agent_prompt.md`を指定するよう報告する。WORK_PACKAGEなら対象Gate06のRequired Packagesのみassigned Pxxに割り当てる。各Coding AgentのPromptが`tests/enhancement/enh_e11/<gate>/<layer>/`（GATE_ID小文字）を初期配置とし、現行RepositoryからTestと既存Product Suiteをdiscover/collectする規則を内包していることを確認する。G01のCLI-only/no Browser制約はG01限定。G02〜G10のfrontend/Browser E2E要否は各Gate07に従う。
- Candidate AssemblyとIndependent Testに当該Gateの固定SHA/実行Evidencesを渡す。historical test Path/commandを受入Authorityにせず、Test-side不具合はBLOCKED/Repair ownerとして切り出し、独立Test Agentに修理させない。
- 旧Suiteの無条件移動・archive・`tests/regression/`PROMOTEを禁止。昇格はProduct invariantの別semantic決定、全repo migrationはE12以降。Gate Orchestrator自身はGate PASS/FAILを出さず、形式的なG01 Gate完了を他Gate完了と混同しない。

## 4. Stop / retry rule

`PACKAGE_READY` 以外の場合、次 Package へ進んではならない。

同一 Package の retry が適切か、Human escalation が必要かを blocker evidence に基づき判断する。
contract ambiguity、repository state、仕様 authority 不足を Orchestrator 自身が補完してはならない。

## 5. formal FAIL guard

current Trial が `FORMAL_FAIL_REMEDIATION` の場合、本 Orchestrator の通常 Work Package sequence を開始しない。
`40_fail_remediation_01_fail_rework_coding_agent_prompt.md` route を要求する。

## 6. Final status

正常時:

```text
READY_FOR_TEST
GATE_ID
TRIAL_NO
completed Package list
FIXED_TRIAL_CANDIDATE_SHA
Implementation Completion Report path
Candidate Assembly evidence commit SHA
```

停止時:

```text
BLOCKED_*
GATE_ID
TRIAL_NO
current PACKAGE_ID（該当する場合）
blocker
last completed Package
report / evidence path
required Human action
```

Gate Orchestrator は `PASS` / `FAIL` を出してはならない。

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

<!-- BEGIN MANAGED: V004_CONTRACT_SIMPLIFICATION -->
## 4. v0.04 Gate routing authority

Normal-path routing authorityを次に固定する。

```text
Gate dependency declaration -> Gate 06 `Depends on`
Gate dependency evidence    -> upstream canonical 999
Execution mode              -> Gate 06 `Execution mode`
Required package set        -> Gate 06 `Required packages`
Package dependency          -> each Pxx `Depends on` + canonical package reports / 999
Verification authority      -> Gate 07
Final Gate route            -> current canonical 999
```

Gate local README / P00 / planning / Architecture Review artifactをexecution eligibilityのauthorityにしない。これらはHuman traceability / optional authoring inputとして扱う。

Phase Fではcurrent Gateのcanonical `999_gate_decision`だけを読み、PASSならcurrent Gateをcompleteとして終了する。next Gateの06/07/freeze/preflightは読まず、downstream Gateを開始する場合はそのGateのPhase Aへ遷移する。Phase Fでstate / transition / promotion artifactを書かない。
<!-- END MANAGED: V004_CONTRACT_SIMPLIFICATION -->


## ENH-E11 S02 Owner承認8項目：Operator実行時の統一保護（2026-11-22）

この40はAgent運用・Discovery/WHERE/HOW・Evidenceのauthorityであり、担当Gateの凍結済み06/Pxx（Coding WHAT）や07（Independent Test WHAT）の科学Methodの意味を変更しない。実行前に最新のOwner `combined_review/137_20261122_dec_s02_eight_simplifications_owner_approval.md`、G01〜G10 06/07/Pxxの同一固定SHA、該当Gateの正式Freeze/Coding Authorizationを照合し、まだDRAFT/未承認ならCoding/Test Agentを起動せず`BLOCKED_CONTRACT_NOT_FROZEN`を報告。実装指示書の署名やMethod権限が矛盾する場合、Agentが外部資料で勝手に補完してはならない。

保護するS02条件：①Local row出力はStudy `privacy.row_export_requested=true`が唯一の実行者明示opt-in。追加`--allow-row-level-export`、`cli_row_flag`、Study`policy_ref`、第三者署名PolicyVerifier/Anchorを生成しない。false/省略は個票なし。G05のみnonroot same-UID private ext4/XFS Verified Root/Method ApprovedRowSchema/row-column-byte-memory caps/G01 stagingに適合した場合にbounded Parquetを生成し、未認可時row Source反復0・row bytes0、aggregateやlogsへ漏洩なし。②40 Method×5 Profileはstrict common schema＋exact Method overlay・200 SHA/parity＋Method独自科学適格性で検証し、未検証ならfail-closed。③G10は全41 Methodの有効な独立Science evidenceを照合し、共有Kernel、schema、Lock、Backend、fixture、Reference、AC、Policy等の推移的なbehavior dependency closureが完全不変と立証できる証拠だけ再利用。変更/不明な対象Methodは再実行またはBLOCK。最終Fixed Candidateのcross-Gate integrationと旧v2保護は毎回必要。④共通bounded RowWriter/RowSchema。⑤E11 Local Graphは科学content hashで識別しProduct GraphVersion DBへの新規lookup/write/edit/FIXは行わず、Product Version IDs=nullを保つ。⑥G01 FS proofは重要不変条件の有界正負例であり障害全順列や電源断保証は不要。⑦新テストはGate/Pxxに対応し、Product回帰・既存ABIテストは変更影響閉包で選択。影響不明なら実行またはBLOCK、無関係なProduct全SuiteやE2Eを機械的に強制しない。⑧NFR-034の将来顧客配布は`DEFERRED`、社内OSS義務は継続。Backendの4つの分離ENVは実Python3.12/lock/API/fit/CIで照合し、未実行・unknownをPASSと呼ばない。

**Control/Assembly/Remediation固有：** 影響差分とprotected Product invariantの根拠、固定full SHA、独立RunnerとReviewer's責務分離を持つ。証拠が不完全ならReady/Passを捏造せず適切にBLOCK。
