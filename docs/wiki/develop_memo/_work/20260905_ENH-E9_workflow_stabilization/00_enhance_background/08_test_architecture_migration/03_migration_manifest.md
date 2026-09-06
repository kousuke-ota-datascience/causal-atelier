# テストMigration Manifest

**状態:** `BATCH_SCOPED / ACTIVE`  
**目的:** ENH-E9 minimum test migrationにおけるsource-to-target authority

## 1. Manifest rule

Physical migrationはrepository全体のclassification完了を待たず、**batch単位**で開始してよい。

各batchでは対象fileについてのみ、以下を事前確定する。

- source path
- target pathまたはtarget family
- action
- rationale
- path/import/fixture/Docker/CI dependency
- migration後verification

許可するaction vocabulary:

```text
KEEP
MOVE
RENAME
PROMOTE
REWRITE
MERGE
SPLIT
ARCHIVE
RETIRE
REVIEW_SUPERSEDED
```

## 2. ENH-E9 minimum migration開始条件

対象batchについて以下を満たせばphysical moveを開始できる。

1. batch対象fileのdispositionが確定している;
2. batch対象fileのpath/import/fixture dependencyを調査済み;
3. move後のtargeted test / collection verificationを定義済み;
4. archiveの場合、historical / supersededであることを十分確認している;
5. Gate contract / product candidate remediationを含まない。

**全active test fileの分類完了はENH-E9 migrationの開始条件としない。**

## 3. ENH-E9で優先するmigration

ENH-E9で実際に使用・変更するtestを優先し、以下へ移行する。

```text
tests/enhancement/enh_e9/<gate>/<layer>/...
```

現在確認済みの例:

| Source | Target | Action | Notes |
|---|---|---|---|
| `tests/product/test_enh_e9_g02_p01_discovery_copy_help_overflow.py` | `tests/enhancement/enh_e9/g02/frontend/test_discovery_copy_help_overflow.py` | `MOVE + RENAME + REWRITE_AS_NEEDED` | path resolutionを移動後locationに合わせる |
| `tests/product/test_enh_e9_g02_p02_selection_comparison_clarity.py` | `tests/enhancement/enh_e9/g02/frontend/test_selection_comparison_clarity.py` | `MOVE + RENAME + REWRITE_AS_NEEDED` | 同上 |
| `tests/product/test_enh_e9_g02_p03_adoption_feedback_export.py` | `tests/enhancement/enh_e9/g02/frontend/test_adoption_feedback_export.py` | `MOVE + RENAME + REWRITE_AS_NEEDED` | 同上 |

G02は具体的file pathが確定している例として記載している。ENH-E9のminimum migrationはG02限定ではなく、今後E9で使用するG01-G05各Gateのtestへ同じbatch ruleを適用する。

## 4. 明確なhistorical testの扱い

Historical / supersededと十分確認でき、current invariantの唯一coverageではないtestは `tests/legacy_archive/` へ移動できる。

一方、現在使用していないだけでcurrent invariantか未判定のtestはarchiveしない。ENH-E9では既存位置に残置してよい。

## 5. ENH-E12以降へdeferするcomprehensive migration

以下はENH-E9では実施しない。

- E1-E8を含む既存test全件のfile-by-file再分類;
- Browser runner全件のcanonical journeyへの統合;
- generic product / integration / scientific testsの全面移動;
- shared fixture / conftest体系の全面再編;
- old test directoryの完全撤去;
- canonical regression suiteのrepository-wide再構築。

これらは **Comprehensive Test Code Migration / Repository-wide Test Architecture Reconciliation** としてENH-E12以降で実施する。

## 6. 過渡期の許容状態

ENH-E10 / E11を含む移行完了前のEnhancementでは、以下の新旧共存を許容する。

```text
tests/enhancement/...   # 新規/変更testの推奨配置
tests/product/...       # 未再認証の既存testが残り得る
tests/browser_e2e/...   # historical runnerが残り得る
tests/integration/...
tests/scientific/...
```

この共存はtarget architecture完成を意味しない。各Enhancementは必要なtestのみbatch単位で新体系へ移し、既存未判定testを無理に動かさない。
