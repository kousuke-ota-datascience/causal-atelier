# ENH-E9 テストアーキテクチャ移行

**文書種別:** ENH-E9横断 Test Architecture Migration Workstream  
**状態:** `PLANNING / INVENTORY`  
**親Workflow:** `20260905_ENH-E9_workflow_stabilization`  
**Scope classification:** `TEST_INFRASTRUCTURE / TEST_ARCHITECTURE STABILIZATION`

## 1. 目的

本ディレクトリは、Ariadneのテストコード体系を以下の直交する2軸で再編するための設計判断、分類inventory、migration plan、実行証跡、移行後verificationを記録する。

1. **test lifecycle / authority** — `regression`, `enhancement`, `characterization`, `benchmark`, `support`, `legacy`
2. **verification layer** — `unit`, `contract`, `integration`, `frontend`, `browser_e2e`

本作業の対象はENH-E9内の特定Gateに限定されない。ENH-E9全体を通じて使用されるテストコード、および過去Enhancementから継承された既存テストを対象に、恒久regressionとEnhancement固有verificationの責務を整理する。

本作業は、ENH-E9 workflow stabilizationの過程で、過去Enhancement由来のtest identity、後続Enhancementによる仕様・UI drift、verification layerとlifecycle分類の混在が確認されたことを受けて開始した。個別Gateで観測されたテスト不整合は調査契機になり得るが、本workstreamのscope定義やauthorityではない。

## 2. 非セマンティック変更としての位置付け

本workstream自体はproduct semanticsを変更しない。

```text
Product semantic change: NONE
Gate Acceptance Criteria change: NONE
Frozen verification contract change: NONE
Requirement/design authority change: NONE
Product candidate remediation: OUT_OF_SCOPE
```

Test Architecture Migrationによって、特定GateのCandidate、Acceptance Criteria、frozen verification contractを遡及変更してはならない。移行作業中にproduct defectが見つかった場合は、当該Gate/Enhancementの正式なremediation routeへ分離する。

## 3. 基本原則

Enhancement testは、新規・変更behaviorを検証するためのstaging areaとして扱う。GateまたはEnhancementの安定化後、各テストに明示的なdispositionを与える。

```text
Enhancement-specific test
        |
        v
PROMOTE / REWRITE / MERGE / RETIRE / ARCHIVE
        |
        v
Current authoritative regression suite
```

Regression testが表現するのは、当該behaviorを最初に導入したEnhancementの歴史的実装形状ではなく、**現在のauthoritative behavior** である。

## 4. 文書一覧

| File | 役割 |
|---|---|
| `01_classification_inventory.md` | 現行テストのbaseline inventoryと初期分類 |
| `02_target_test_architecture.md` | 目標filesystem構造とtest lifecycle policy |
| `03_migration_manifest.md` | source-to-target migration manifestとdisposition定義 |
| `04_migration_decision_log.md` | 非自明なmigration判断のdecision log |
| `05_execution_record.md` | 実際に行ったmigration batch / commitの追記型実行証跡 |
| `06_post_migration_verification.md` | 移行後verification checklistとclosure evidence |

## 5. 現在状態

- Classification principle: **定義済み**
- Repository初期inventory: **directory / test-family単位で完了**
- File-by-file final target mapping: **未完了**
- Physical filesystem migration: **未開始**
- Migration後test execution: **未開始**

## 6. Authority boundary

本ディレクトリはtest architecture stabilizationのためのsupporting design/evidenceであり、以下をoverrideしない。

- canonical requirements / design documents
- 各Gate `06` implementation semantic authority
- 各Gateのfrozen `07` verification authority
- canonical `999_gate_decision` terminal authority

Migration判断が既存のfrozen Gate contractと競合する場合、Gate contractを弱めるのではなくmigrationを停止し、競合を明示的に解消する。
