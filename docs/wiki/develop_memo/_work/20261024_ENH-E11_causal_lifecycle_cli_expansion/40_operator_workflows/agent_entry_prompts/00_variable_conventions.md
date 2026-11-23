# Variable規約

**ENH-E11 Gate別Authorization Preflight（Owner DEC-PREPCODE-01=B、G01のみDEC-G01-EXEC-01追加採用）:** 全Gate402件のSHA索引は独立S09 PASSではない。**G01専用例外**：独立S09・B02/B04実Python3.12・B05 MAG/PAG/BKはCoding Entryの事前PASSを要求せず、G01_999までの必須実測/独立審査として`EXTERNAL_PENDING/NOT_RUN`で保持する。Coding開始に必要なのは、G01/common 06/Pxx/07等のAuthor契約整合、未検証例外の明示、**Ownerが別途発行した暫定G01-S10（対象正本full SHAと07/999 obligationsを固定）**、さらに**Ownerが別途発行した限定G01-S11（許可G01/P01〜P05、source/lock/paths）**の両方。Ownerの方針採用そのものはFreeze・Coding Authorizationではない。G01で実装できるのは許可WPと開発者テストだけ、未知の科学真値・CI/BK/Backend状態をPASSへ昇格しない。non-null BKは有効独立remedyまでFCI呼出前typed deny。G01_999は独立S09、B02/B04、独立Graph/BK B05、実FS/Reader/T2/T3/旧Product回帰/独立07が未完ならBLOCKED。**G02〜G10は従来DEC-PREPCODE-01=BのGate別独立S09→Owner S10→別Owner S11と実上流999 PASSを厳守**。どのGateもOwner承認証拠欠損・SHA不一致・契約変更なら`BLOCKED_CODING_AUTHORIZATION`、Agentを起動しない。現在G01の暫定S10/限定S11は両方未承認。

実行ごとにHumanが与える値:
- `GATE_ID` = ENH-E11正式Gate ID（`G01`〜`G10`のいずれか）。Gate別06/07/08/Pxxが存在・Freeze済みかは実行時に検証し、未作成GateへG01の契約を流用しない。
- `TRIAL_NO` = 2桁 Trial number（例: `01`）
- `PACKAGE_ID` = Package ID（例: `P01`。Work Package coding時のみ）

ENH-E11 Enhancement固定値:
- `PROJECT_NAME=Ariadne`
- `ENHANCE_ID=ENH-E11`
- `ENHANCE_SHORT_ID=E11`
- `BRANCH_NAME=feature/ariadne_mvp_e11`
- `REMOTE_NAME=causal-atelier`
- `WORK_ROOT=docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion`

Runtime-derived values:
- `START_SHA`
- `PACKAGE_CHECKPOINT_SHA`
- `FIXED_TRIAL_CANDIDATE_SHA`
- `EVIDENCE_COMMIT_SHA`
- `TEST_START_SHA`
- `TEST_EVIDENCE_COMMIT_SHA`
- `PREVIOUS_FAILED_CANDIDATE_SHA`（formal FAIL remediation時）

導出path:
- `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/10_enhance_instruction/$GATE_ID/06_Ariadne_ENH-E11_$GATE_ID...` — directory listingから正確なfilenameを導出する。semantic matchが0件または複数ならSTOPする。

SHA は実行時の repository state からのみ取得する。架空 SHA を事前生成してはならない。
`PACKAGE_CHECKPOINT_SHA`、`FIXED_TRIAL_CANDIDATE_SHA`、`EVIDENCE_COMMIT_SHA` は意味が異なるため混同しない。

Enhancement-fixed identityは展開済み。Agent実行時にRuntime variableだけを確定する。任意のglob matchを選んではならない。

<!-- BEGIN MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->
## 2. Agent Entry Prompt Variable Conventions

### 2.1. Purpose

`agent_entry_prompts/` はENH-E11用に実体化済みの実行Prompt正本であり、Enhancement-fixed変数は具体値へ展開済みである。実行時に未解決のRuntime変数だけHuman/Orchestratorが指定する。

template directory上のpromptをAgent executionへ直接指定してはならない。

### 2.2. Enhancement-fixed variables

以下はEnhancement-specific prompt instance生成時に必ず具体値へ展開する。

```text
PROJECT_NAME
ENHANCE_ID
ENHANCE_SHORT_ID
BRANCH_NAME
REMOTE_NAME
WORK_ROOT
WORK_DIR_NAME
```

Enhancement-side `agent_entry_prompts/` に上記の未解決placeholderが1件でも残る場合、Agent execution readinessは `BLOCKED_ENHANCEMENT_IDENTITY_UNRESOLVED` とする。

**ENH-E11 Gate scope:** GateはG01〜G10の10件。40 Promptは全Gate共通で、対象Gateの実行mode/Required PackageをGate06から解決する。G01〜G10の06/07/Pxxは現行RepositoryにDRAFTとして存在するが、作成済み・レビュー済みはFreezeやCoding Authorizationを意味しない。対象GateのMode/Pxx/依存関係はそのGateのFreeze済み正本をexact full SHAで確認する。

### 2.3. Runtime variables

以下はexecution単位でHuman operatorまたはOrchestratorが指定する。

```text
GATE_ID
PACKAGE_ID
TRIAL_NO
REMEDIATION_PACKAGE_ID
AMENDMENT_ID
```

各promptは必要なRuntime variableだけを要求する。不要なRuntime variableを推測で補完してはならない。

### 2.4. Resolution rule

Enhancement identityはEnhancement-fixed variablesから、execution identityはRuntime variablesから解決する。

```text
Execution identity = Enhancement identity + Runtime identity
```

Human entryだけで対象を一意に解決できない場合は実行を開始せず `BLOCKED_EXECUTION_UNRESOLVABLE` とする。

### 2.5. Template and instance distinction

- template側: `agentic_enhancement_workflow_template/40_operator_workflows/agent_entry_prompts/`
  - authoring source
  - Enhancement-fixed placeholdersを保持してよい
  - Agent executionへ直接使用しない
- Enhancement側: `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/40_operator_workflows/agent_entry_prompts/`
  - execution source
  - Enhancement-fixed placeholdersは0件でなければならない
  - Human Quick HowToUseが参照するcanonical path

### 2.6. Markdown heading numbering

Markdown artifactの見出しは原則として以下に従う。

```text
#       document title: no numeric prefix
##      1. / 2. / 3.
###     1.1. / 1.2.
####    1.1.1.
#####   1.1.1.1.
######  1.1.1.1.1.
```

コードフェンス内の `#` は対象外とする。
<!-- END MANAGED: AGENT_ENTRY_PROMPT_CONTROL -->


## ENH-E11 S02 Owner承認8項目：Operator実行時の統一保護（2026-11-22）

この40はAgent運用・Discovery/WHERE/HOW・Evidenceのauthorityであり、担当Gateの凍結済み06/Pxx（Coding WHAT）や07（Independent Test WHAT）の科学Methodの意味を変更しない。実行前に最新のOwner `combined_review/137_20261122_dec_s02_eight_simplifications_owner_approval.md`、G01〜G10 06/07/Pxxの同一固定SHA、該当Gateの正式Freeze/Coding Authorization（G01ではOwner暫定S10と別Owner限定S11の両記録）を照合し、まだDRAFT/未承認ならCoding/Test Agentを起動せず`BLOCKED_CONTRACT_NOT_FROZEN`を報告。実装指示書の署名やMethod権限が矛盾する場合、Agentが外部資料で勝手に補完してはならない。

保護するS02条件：①Local row出力はStudy `privacy.row_export_requested=true`が唯一の実行者明示opt-in。追加`--allow-row-level-export`、`cli_row_flag`、Study`policy_ref`、第三者署名PolicyVerifier/Anchorを生成しない。false/省略は個票なし。G05のみnonroot same-UID private ext4/XFS Verified Root/Method ApprovedRowSchema/row-column-byte-memory caps/G01 stagingに適合した場合にbounded Parquetを生成し、未認可時row Source反復0・row bytes0、aggregateやlogsへ漏洩なし。②40 Method×5 Profileはstrict common schema＋exact Method overlay・200 SHA/parity＋Method独自科学適格性で検証し、未検証ならfail-closed。③G10は全41 Methodの有効な独立Science evidenceを照合し、共有Kernel、schema、Lock、Backend、fixture、Reference、AC、Policy等の推移的なbehavior dependency closureが完全不変と立証できる証拠だけ再利用。変更/不明な対象Methodは再実行またはBLOCK。最終Fixed Candidateのcross-Gate integrationと旧v2保護は毎回必要。④共通bounded RowWriter/RowSchema。⑤E11 Local Graphは科学content hashで識別しProduct GraphVersion DBへの新規lookup/write/edit/FIXは行わず、Product Version IDs=nullを保つ。⑥G01 FS proofは重要不変条件の有界正負例であり障害全順列や電源断保証は不要。⑦新テストはGate/Pxxに対応し、Product回帰・既存ABIテストは変更影響閉包で選択。影響不明なら実行またはBLOCK、無関係なProduct全SuiteやE2Eを機械的に強制しない。⑧NFR-034の将来顧客配布は`DEFERRED`、社内OSS義務は継続。Backendの4つの分離ENVは実Python3.12/lock/API/fit/CIで照合し、未実行・unknownをPASSと呼ばない。

**Control/Assembly/Remediation固有：** 影響差分とprotected Product invariantの根拠、固定full SHA、独立RunnerとReviewer's責務分離を持つ。証拠が不完全ならReady/Passを捏造せず適切にBLOCK。
