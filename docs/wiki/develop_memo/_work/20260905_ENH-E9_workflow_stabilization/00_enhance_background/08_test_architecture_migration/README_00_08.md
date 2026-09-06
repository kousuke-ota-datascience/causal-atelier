# ENH-E9 Test Architecture Migration

**Document class:** Cross-cutting Test Architecture Migration Workstream  
**Status:** `PLANNING / INVENTORY`  
**Parent workflow:** `20260905_ENH-E9_workflow_stabilization`  
**Scope classification:** `TEST_INFRASTRUCTURE / TEST_ARCHITECTURE STABILIZATION`

## 1. Purpose

This directory records the design decisions, classification inventory, migration plan, execution evidence, and post-migration verification for restructuring Ariadne tests around two orthogonal axes:

1. **test lifecycle / authority** — `regression`, `enhancement`, `characterization`, `benchmark`, `support`, `legacy`
2. **verification layer** — `unit`, `contract`, `integration`, `frontend`, `browser_e2e`

The work was initiated after ENH-E9 G02 Trial01 independent verification was blocked before the product workflow because the historical Browser E2E runner had drifted from the current Project / Analysis navigation model.

## 2. Non-semantic classification

This workstream does **not** change product semantics.

```text
Product semantic change: NONE
G02 Fixed Trial Candidate mutation: PROHIBITED
G02 Acceptance Criteria change: NONE
Frozen 07 change: NONE
Requirement/design authority change: NONE
```

G02 Trial01 Fixed Candidate remains:

```text
8cf70523093efa53b59a7de2c655f9755dbceb8d
```

The Browser E2E blocker is treated as a test implementation / test architecture problem until independent verification establishes a product defect.

## 3. Target principle

Enhancement tests are a staging area for newly introduced or modified behavior. After a Gate / Enhancement stabilizes, each test is explicitly dispositioned:

```text
Enhancement-specific test
        |
        v
PROMOTE / REWRITE / MERGE / RETIRE / ARCHIVE
        |
        v
Current authoritative regression suite
```

Regression tests represent **current authoritative behavior**, not the historical implementation shape of the Enhancement that originally introduced the behavior.

## 4. Document index

| File | Purpose |
|---|---|
| `01_classification_inventory.md` | Baseline inventory and initial classification of current tests |
| `02_target_test_architecture.md` | Target filesystem and lifecycle architecture |
| `03_migration_manifest.md` | Source-to-target migration manifest and disposition vocabulary |
| `04_migration_decision_log.md` | Decision log explaining non-obvious migration choices |
| `05_execution_record.md` | Append-only record of actual migration batches and commits |
| `06_post_migration_verification.md` | Verification checklist and final closure evidence |

## 5. Current status

- Classification principles: **defined**
- Initial repository inventory: **completed at directory / test-family level**
- File-by-file final target mapping: **pending**
- Physical filesystem migration: **not started**
- Test execution after migration: **not started**

## 6. Authority boundary

This directory is supporting design/evidence for test architecture stabilization. It does not override:

- canonical requirements/design documents;
- Gate `06` implementation semantic authority;
- frozen Gate `07` verification authority;
- canonical `999_gate_decision` terminal authority.

If a migration decision conflicts with any frozen Gate contract, the migration must stop and the conflict must be resolved explicitly rather than weakening the Gate contract.
