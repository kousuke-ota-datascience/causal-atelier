# Migration後Verification

**状態:** `MINIMUM_SCOPE`  
**目的:** ENH-E9 minimum test migrationのclosure checklist

## 1. Structural verification

- [ ] ENH-E9で実際に使用・変更したtestが `tests/enhancement/enh_e9/<gate>/<layer>/...` に整理されている
- [ ] 移動対象batchでownershipが曖昧になっていない
- [ ] 明確にhistoricalと判断したtestのみ `tests/legacy_archive/` へ移している
- [ ] 未判定既存testを、現時点で使わないという理由だけでarchiveしていない
- [ ] `tests/legacy_archive/` が通常pytest collectionから除外されたままである

## 2. Batch dependency verification

各migration batchについて:

- [ ] `Path(__file__)` 等のpath依存を移動後locationに合わせて修正した
- [ ] fixture / `conftest.py` scope impactを確認した
- [ ] import pathを確認した
- [ ] Docker / CI / docs / operator commandのpath referenceを必要に応じて更新した
- [ ] targeted collectionが成功する
- [ ] targeted testsがPASSする

## 3. ENH-E9 execution continuity

- [ ] E9の今後のGate verificationに必要なtestを新配置から実行可能
- [ ] test migration自体のためにproduct semanticsを変更していない
- [ ] Gate candidate / frozen contractをmigration都合で変更していない
- [ ] migrationでproduct defectを発見した場合は当該Gateの正式routeへ分離している

## 4. 過渡期状態の確認

ENH-E9 closure時点で以下が残っていても、本minimum migrationのFAIL条件とはしない。

- `tests/product/` に未再認証testが残る
- `tests/browser_e2e/` にhistorical Enhancement runnerが残る
- `tests/integration/` / `tests/scientific/` が旧分類のまま残る
- canonical regression suiteが全面再構築されていない
- shared fixture / conftestが旧配置のまま残る

これらはENH-E12以降の Comprehensive Test Code Migration / Repository-wide Test Architecture Reconciliation のscopeである。

## 5. E10/E11 handoff verification

- [ ] `07_handoff_to_enh_e10_e11.md` が存在する
- [ ] E10/E11で新規testを置く推奨pathが明記されている
- [ ] historical Browser E2E failureを即product defectとみなさない注意事項がある
- [ ] 必要なtestだけbatch単位でmigrationしてよいことが明記されている
- [ ] comprehensive migrationがENH-E12以降へdeferされていることが明記されている

## 6. Template non-change verification

- [ ] `docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/README.md` にrepository固有の過渡期test estate説明を追加していない

## 7. Closure record

```text
Minimum migration commit(s):
Migrated ENH-E9 test paths:
Archived historical test paths:
Targeted test result:
Known transitional debt:
Deferred comprehensive migration: ENH-E12 or later
Final status: PASS | BLOCKED | FAIL
```
