# ENH-E10 / ENH-E11 向け Test Architecture Handoff

**状態:** `ACTIVE_HANDOFF`  
**対象:** ENH-E10 / ENH-E11 planning・implementation・verification  
**前提:** Comprehensive Test Code MigrationはENH-E12以降へdefer

## 1. Handoffの目的

ENH-E10 / E11は、repository全体のtest code migration完了を待たずに開始・完了してよい。

ただしtest estateは過渡期であり、新architectureと旧配置が共存する。この文書は、その状態でEnhancementを安全に進めるための最低限の運用ルールを引き継ぐ。

## 2. 新規・変更testの推奨配置

ENH-E10 / E11で新規作成または実質的に再構築するtestは、原則として以下へ配置する。

```text
tests/enhancement/<enhancement>/<gate>/<layer>/
```

例:

```text
tests/enhancement/enh_e10/g01/unit/
tests/enhancement/enh_e10/g02/frontend/
tests/enhancement/enh_e11/g01/integration/
tests/enhancement/enh_e11/g02/browser_e2e/
```

Verification layerは `unit`, `contract`, `integration`, `frontend`, `browser_e2e` を基本とする。

## 3. 既存testの扱い

既存testをENH-E10 / E11で使用する際、repository全体を先に整理する必要はない。

- そのEnhancementで実際に必要なtestだけをbatch単位で新体系へ移してよい;
- moveによりpath / fixture / import dependencyが壊れる場合はtest code側を同一batchで修正する;
- current invariantか未判定の既存testは旧位置に残してよい;
- 「今回使わない」だけを理由に `legacy_archive` へ移さない;
- historical / supersededと確認できるtestだけarchiveする。

## 4. Browser E2Eの注意事項

過去Enhancement由来のBrowser runnerには、stale locator、obsolete navigation、historical runner import等が残っている可能性がある。

そのためBrowser E2E failure時は、直ちにproduct defectと判定せず、少なくとも以下を分類する。

```text
PRODUCT_DEFECT
TEST_IMPLEMENTATION_DEFECT
TEST_ORCHESTRATION_DEFECT
TEST_ENVIRONMENT_DEFECT
```

Historical runnerがcurrent product workflowへ到達できない場合、Acceptance Criteriaを弱めるのではなく、必要に応じてcurrent journeyへrunnerを更新・再構築する。

Browser E2Eはcross-layer connectivity proofを主責務とし、詳細なsemantic/scientific correctnessはlower deterministic layerをprimary proofとする。

## 5. 過渡期に許容するrepository状態

ENH-E10 / E11期間中、以下の共存を許容する。

```text
tests/enhancement/...   # 新architecture
tests/product/...       # 未再認証の既存test
tests/browser_e2e/...   # historical runnerを含み得る
tests/integration/...
tests/scientific/...
tests/legacy_archive/...
```

この共存状態をtarget architecture完成とはみなさない。

## 6. ENH-E10 / E11でやらないこと

Feature scope上必要でない限り、以下をE10/E11のblocking prerequisiteにしない。

- E1-E9 test全件の再分類;
- canonical regression suiteの全面再構築;
- historical Browser runners全件の統廃合;
- `tests/product/` 等の旧directory完全撤去;
- shared fixture / conftest体系の全面再編。

## 7. ENH-E12以降への引き継ぎ

以下を独立Enhancementとして実施する。

**名称候補:** `Comprehensive Test Code Migration` / `Repository-wide Test Architecture Reconciliation`

主要scope:

- E1以降の既存test全件をcurrent requirements / current behaviorと再照合;
- PROMOTE / REWRITE / MERGE / SPLIT / RETIRE / ARCHIVEをfile-by-file確定;
- canonical regression suiteを再構成;
- historical Browser runnerからcurrent critical journeyを抽出;
- fixture / conftest / CI / Docker / marker体系を整理;
- 旧test directoryを段階的に撤去;
- final target architectureへの収束をverificationする。

## 8. Generic workflow templateとの関係

この過渡期運用はAriadne repository固有のtest estate migrationである。

したがって、`docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/README.md` のgeneric enhancement workflow contractへは組み込まない。
