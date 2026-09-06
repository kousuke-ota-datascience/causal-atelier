# ENH-E9 テストアーキテクチャ移行

**文書種別:** ENH-E9横断 Test Architecture Migration Workstream  
**状態:** `MINIMUM_MIGRATION_ACTIVE / COMPREHENSIVE_DEFERRED`  
**親Workflow:** `20260905_ENH-E9_workflow_stabilization`  
**Scope classification:** `TEST_INFRASTRUCTURE / TEST_ARCHITECTURE STABILIZATION`

## 1. 目的

本ディレクトリは、Ariadneのテストコード体系を以下の直交する2軸で整理するための設計判断、分類inventory、migration plan、実行証跡、移行後verificationを記録する。

1. **test lifecycle / authority** — `regression`, `enhancement`, `characterization`, `benchmark`, `support`, `legacy`
2. **verification layer** — `unit`, `contract`, `integration`, `frontend`, `browser_e2e`

ただしENH-E9でrepository全体のtest estateを完全再編しない。ENH-E9では、今後のE9実行に実際に必要なtestから新体系へ順次移行し、明確にhistoricalであると確認できるtestのみarchive対象とする。その他の既存testは、包括的な再認証が完了するまで現状位置に残してよい。

## 2. ENH-E9で実施するminimum must

ENH-E9で必須とするのは以下である。

- ENH-E9で実際に使用・変更するtestを `tests/enhancement/enh_e9/<gate>/<layer>/...` へ順次移行する;
- moveに伴う `Path(__file__)`、fixture scope、import、Docker/CI/path reference等のdependencyを対象batch単位で修正する;
- 各batchでcollection / targeted testを実行してmigration evidenceを残す;
- 明確にhistorical / supersededと確認できるtestのみ `legacy_archive` へ移す;
- 新規Enhancementでは原則として新test lifecycle architectureを使用する。

## 3. ENH-E9では実施しないこと

以下はENH-E9の必須scope外とし、**Comprehensive Test Code Migration / Repository-wide Test Architecture Reconciliation** としてENH-E12以降で実施する。

- E1-E8を含む既存test全件のfile-by-file再認証;
- current invariant / duplicate / superseded / historicalの完全判定;
- canonical regression suiteの全面再構築;
- `tests/product/`, `tests/browser_e2e/`, `tests/integration/`, `tests/scientific/` 等の旧配置を完全に解消すること;
- shared fixture / conftest体系の全面再編;
- historical Browser runner全件のscenario extractionと統廃合。

延期理由:

1. この包括移行を完了しなくても、各Enhancement自体の実装・verificationは可能である。過渡期にはBrowser E2E等でtest-side driftに遭遇する可能性が残るが、個別に修復可能である。
2. ENH-E10 / ENH-E11を含む他Enhancementを先に区切り、test estate再認証によってfeature roadmapを長期間blockしない。

## 4. 非セマンティック変更としての位置付け

```text
Product semantic change: NONE
Gate Acceptance Criteria change: NONE
Frozen verification contract change: NONE
Requirement/design authority change: NONE
Product candidate remediation: OUT_OF_SCOPE
```

Test Architecture Migrationによって各GateのCandidate、Acceptance Criteria、frozen verification contractを遡及変更してはならない。Migration中にproduct defectを確認した場合は、当該Gate / Enhancementの正式routeへ分離する。

## 5. 基本原則

Enhancement testは新規・変更behaviorのstaging areaとして扱う。安定化後に必要に応じて以下のdispositionを行う。

```text
PROMOTE / REWRITE / MERGE / RETIRE / ARCHIVE
```

Regression testが表現するのはEnhancement履歴ではなく、**現在のauthoritative behavior** である。

## 6. 文書一覧

| File | 役割 |
|---|---|
| `01_classification_inventory.md` | 現行test estateの初期inventory。包括移行時の入力資料 |
| `02_target_test_architecture.md` | 目標filesystem構造とtest lifecycle policy |
| `03_migration_manifest.md` | ENH-E9 minimum migrationのbatch manifest |
| `04_migration_decision_log.md` | migration scope / architecture decision log |
| `05_execution_record.md` | 実際に行ったmigration batch / commitの追記型実行証跡 |
| `06_post_migration_verification.md` | ENH-E9 minimum migrationのverification checklist |
| `07_handoff_to_enh_e10_e11.md` | ENH-E10/E11へ共通で引き継ぐ過渡期test estate運用baseline |
| `08_handoff_to_enh_e10.md` | ENH-E10 planning / 10 / 40 / verification authoringへ直接適用する個別handoff |
| `09_handoff_to_enh_e11.md` | ENH-E11 planning / 10 / 40 / verification authoringへ直接適用する個別handoff |

## 7. Authority boundary

本ディレクトリはtest architecture stabilizationのsupporting design/evidenceであり、canonical requirements/design、各Gate `06`/`07`、`999_gate_decision`をoverrideしない。

また、`docs/wiki/develop_memo/_work/agentic_enhancement_workflow_template/README.md` に「過渡期のtest code体系」である旨を追記しない。本件はAriadne repositoryの現時点のtest estateに固有のmigration debtであり、generic enhancement workflow templateのnormative contractではない。
