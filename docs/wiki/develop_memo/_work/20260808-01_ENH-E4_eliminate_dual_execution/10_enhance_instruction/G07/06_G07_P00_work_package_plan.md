# ENH-E4 / G07 P00 — Work Package Plan
## 1. Objective

G07 establishes the final repository-managed boundary for:

```text
legacy runtime / deployment
Product-only migration bootstrap
standalone scientific CLI
shared scientific capability
```

Primary transition debt:

```text
TD-005
exit: Product runtime/bootstrap do not depend on legacy
```

Target state:

```text
canonical Product runtime/deployment/bootstrap
    = only active Product authority

ariadne.causal / ariadne.preprocessing / ariadne.shared
    = retained shared scientific capability

legacy runtime / root migrations
    = retired or history-only, non-authoritative

standalone scientific CLI
    = low-level utility boundary, not a second persistent lifecycle
```

G07 is not a general legacy-source deletion project.

---

## 2. Minimal Authoritative Inputs

Read only these common inputs unless a concrete contradiction requires more history:

```text
40_operator_prompts/architecture_review/
  06_target_architecture_decision_record_result.md
  07_gate_decomposition_result.md

30_test_report/G06/Trial01/
  E4-G06_01_999_gate_decision.md

this P00
current relevant source/tests
```

Approved decisions entering G07:

```text
HD-005: external legacy compatibility is outside ENH-E4 scope
HD-006: Product-only clean rebuild; no historical application-data migration
HD-007: standalone Product scientific CLI is a low-level utility boundary
```

Do not reopen them unless current repository evidence directly contradicts them.

---

## 3. Entry State

```text
G06 = PASS
TD-004 = CLOSED
TD-005 = OPEN

G06 fixed candidate:
9816ed87daec1efcb1c860f0c9c0ebe72fb9bc92

G06 tested/documentation state:
8a4c0042cd766fa182fdc8c5edc346a8e22c807b

Migration head entering G07:
20260809_product_0010
```

Before the first G07 code/test change, record:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
```

The first checkpoint must record the actual G07 entry SHA. Do not assume the G06 fixed candidate is current HEAD; later G06 documentation/test-report commits may exist.

---

## 4. Formal Gate Acceptance Criteria

### AC-001 — Runtime legacy independence

Canonical Product runtime imports no retired `ariadne.legacy` runtime module. Evidence: static import/reachability audit over actual Product runtime/package roots.

### AC-002 — Deployment legacy independence

Repository-managed Product deployment invokes no legacy API/CLI/worker/bootstrap root. Evidence: package/deployment entry-point audit.

### AC-003 — Shared scientific preservation

Shared scientific capability remains usable independently of legacy orchestration. Verify intended retained capability represented by:

```text
ariadne.causal
ariadne.preprocessing
ariadne.shared
Product scientific adapter paths consuming them
```

This is an import/compatibility contract, not an algorithm redesign.

### AC-004 — Product-only bootstrap

Canonical Product bootstrap uses only:

```text
alembic_product.ini -> product_migrations
```

Root:

```text
alembic.ini -> migrations
```

must remain outside Product bootstrap. DB semantics require real PostgreSQL evidence.

### AC-005 — CLI boundary

Standalone Product scientific CLI must not create a second persistent Product lifecycle.

```text
low-level utility CLI
    -> direct scientific operation / files / manifest
    -> no persistent Product Execution lifecycle

user-visible auditable analysis CLI, if one exists/is introduced
    -> canonical Product Execution submission
```

G07 does not need to invent a new auditable CLI merely to satisfy AC-005.

---

## 5. Passed-Gate Preservation Contract

G07 must preserve:

```text
G02: one canonical Product Execution authority
G03: persistent StageExecution processing
G04: canonical Product Result / Artifact authority
G05: Causal / Exploratory / Predictive convergence
G06: typed structural + guarded generic-only lineage authority
```

G06 lineage invariant remains:

```text
structural relation        -> typed canonical authority
generic-only semantic edge -> guarded generic persistence
closure/export             -> derived projection only
```

G07 must not reactivate family/legacy Execution, Result, Artifact, or Lineage authority through compatibility, CLI, migration, or bootstrap code.

Mutation semantics also remain:

```text
retry  = same Execution ID
rerun  = new ID + typed DERIVED_FROM base relation
revise = new ID + typed REVISED_FROM base relation
```

---

## 6. Legacy Classification Vocabulary

Classify by runtime behavior, not by filename/name alone:

```text
ACTIVE_PRODUCT_DEPENDENCY
  Product runtime/deploy/bootstrap reaches it.
  Remove/replace in G07 unless formally blocked.

RETIRED_UNREACHABLE
  Historical implementation remains but Product cannot reach it.
  Source presence alone is not a Gate failure.

HISTORY_ONLY
  Historical migration/config/source retained with no Product invocation.

RETAIN_SHARED_CAPABILITY
  Scientific/preprocessing/shared capability required independently.
  Preserve it.

LOW_LEVEL_UTILITY
  Standalone scientific CLI outside persistent Product lifecycle.

COMPATIBILITY_DATA_CONTRACT
  Legacy-named field/string/value still consumed by Product contract/tests.
  Naming alone is not a runtime dependency.
```

A grep hit is an inspection lead, not a deletion instruction.

---

## 7. Expected Current Facts — Verify Locally

Expected entering state:

```text
pyproject.toml
  Product CLI/API/worker entry points use non-legacy interfaces.
  packaged wheel excludes src/ariadne/legacy/**.

Dockerfile / .dockerignore
  legacy source is excluded from Product container/package surface.
  Product image includes alembic_product.ini + product_migrations.

compose.yaml
  migration service uses alembic_product.ini.
  API/worker use Product entry points.

alembic_product.ini
  script_location = product_migrations

alembic.ini
  script_location = migrations
  retained as historical legacy chain.

src/ariadne/legacy/
  still exists physically; this alone is not active authority.

src/ariadne/interfaces/cli/
  standalone scientific CLIs exist outside persistent Product lifecycle.
```

Local repository evidence wins if different. Record any difference in the relevant checkpoint.

---

## 8. Package Plan

G07 uses four implementation packages after P00.

Current evidence suggests the target boundary is already partly present, so the Gate should emphasize reachability proof, guardrails, and targeted correction rather than broad redesign/deletion.

### P01 — Runtime / deployment / shared-science boundary

Instruction:

```text
06_G07_P01_runtime_deployment_shared_boundary.md
```

Coverage:

```text
AC-001, AC-002, AC-003
INV-013, INV-014
REQ-001, REQ-002, REQ-026..029
```

Required outcomes:

1. identify actual Product runtime/package/deployment roots;
2. classify material legacy references using Section 6;
3. remove active Product dependency on retired legacy runtime if found;
4. preserve shared scientific capability independently;
5. add/strengthen architecture tests that permanently enforce runtime/deployment independence;
6. explicitly record retained retired/history-only source instead of deleting it speculatively.

A verification-only production outcome is valid if the target already holds and the package adds non-vacuous evidence/guardrails.

Checkpoint:

```text
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P01_implementation_checkpoint_report.md
```

### P02 — Product-only migration / bootstrap boundary

Instruction:

```text
06_G07_P02_product_only_migration_bootstrap.md
```

Coverage:

```text
AC-004
INV-015
REQ-030..032
TD-005 bootstrap half
```

Required outcomes:

1. identify the complete repository-managed Product bootstrap path;
2. prove it uses only `alembic_product.ini -> product_migrations`;
3. prove root `alembic.ini -> migrations` is history-only for Product bootstrap;
4. remove accidental legacy bootstrap invocation if found;
5. execute clean Product bootstrap/migration verification on real PostgreSQL;
6. preserve approved pre-production clean-rebuild policy.

Do not create a dual migration chain or rewrite historical migrations merely to remove legacy naming.

Checkpoint:

```text
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P02_implementation_checkpoint_report.md
```

### P03 — CLI / compatibility boundary

Instruction:

```text
06_G07_P03_cli_compatibility_boundary.md
```

Coverage:

```text
AC-005
REQ-033..035
ADR-011, ADR-012
HD-007
```

Required outcomes:

1. inventory repository-managed Product/scientific CLI entry points;
2. classify each as low-level utility or canonical auditable Product entry point;
3. prove low-level scientific CLI does not persist an independent Product Execution lifecycle;
4. ensure any existing auditable persistent CLI path submits through canonical Product Execution authority;
5. retain legacy-named fields/strings only when they remain real compatibility contracts;
6. add focused tests/static contracts preventing a second CLI lifecycle owner.

Do not convert utility CLI into lifecycle orchestration unless an existing contract requires auditability.

Checkpoint:

```text
20_implementation_reports/G07/Trial01/packages/
E4-G07_01_P03_implementation_checkpoint_report.md
```

### P04 — Gate completion / TD-005 closure / test handoff

Instruction:

```text
06_G07_P04_gate_completion_instruction.md
```

Coverage:

```text
AC-001..005
TD-005 exit
G02..G06 protected regressions
Independent Test readiness
```

Required outcomes:

1. Gate-wide runtime/deployment/bootstrap/CLI negative-authority audit;
2. shared scientific import/capability verification;
3. real-PostgreSQL bootstrap evidence;
4. protected regression proving G02–G06 preservation;
5. final residual legacy classification table;
6. explicit G08 residuals, if any;
7. freeze one G07 implementation/test candidate SHA;
8. produce implementation completion report;
9. declare `READY_FOR_TEST` only when every G07 AC has evidence.

Completion report:

```text
20_implementation_reports/G07/Trial01/
E4-G07_01_implementation_completion_report.md
```

Independent Test instruction, authored after candidate freeze:

```text
10_enhance_instruction/G07/
07_Ariadne_ENH-E4_G07_テスト指示書.md
```

---

## 9. Why Four Packages

The independent failure surfaces are:

```text
P01: runtime/package/deployment reachability + shared capability
P02: migration/bootstrap authority
P03: CLI lifecycle + compatibility semantics
P04: Gate-wide closure + fixed-candidate handoff
```

This is sufficient separation for coherent checkpoints without reproducing G06-level fragmentation.

Add another package only if implementation evidence reveals an independent change surface that cannot safely fit P01–P03.

---

## 10. Common Rules for P01–P04

Package instructions reference this section instead of repeating it.

### Trial

```text
Current Trial = Trial01
```

Trial increments only after formal Independent Test FAIL. Package implementation/self-test rework stays in the same Trial.

### Evidence precedence

```text
1. current local repository behavior/tests
2. latest passed Gate decision / fixed-candidate evidence
3. approved ADR + Gate decomposition
4. current package instruction / P00
5. older review snapshots/control-sheet state
```

### Test discipline

Tests encode approved architecture. Fix production behavior when a real violation is found; do not weaken tests merely to preserve legacy behavior.

### Scope

G07 owns repository-managed legacy runtime/deployment/bootstrap/CLI boundary. Preserve unrelated code and scientific algorithms. Broad physical deletion of legacy source is not required for PASS.

### PostgreSQL

For DB/bootstrap semantics:

```bash
scripts/test/run_product_postgres_tests.sh \
  <pytest-path-or-node> \
  [pytest-options]
```

Mocks/in-memory substitutes are not sufficient bootstrap evidence.

### Checkpoint

Each package records:

```text
status: COMPLETE | BLOCKED
entry SHA / checkpoint SHA
files changed
facts established
commands/tests + outcomes
remaining residuals
next-package entry conditions
```

A package checkpoint never declares Gate PASS.

### Fixed candidate

Only P04 freezes the G07 implementation/test candidate. Later documentation-only commits must not replace candidate identity.

### Verification-only package

If the approved invariant already holds, this is valid:

```text
no production diff
+ non-vacuous verification/test hardening
+ explicit evidence
```

Do not manufacture a production change.

---

## 11. Residual Legacy Inventory Contract

P01 starts this inventory; P04 finalizes it.

Each material surface must record:

```text
path/surface
classification
Product runtime reachable? yes/no
Product deployment reachable? yes/no
Product bootstrap reachable? yes/no
persistent authority? yes/no
shared capability required? yes/no
G07 action
G08 residual, if any
verification evidence
```

Purpose:

```text
legacy source presence != active dual architecture
```

and to avoid repeating the same reachability analysis in G08.

---

## 12. TD-005 Closure Rule

TD-005 closes only if final evidence proves:

```text
Product runtime does not depend on legacy runtime
AND
Product bootstrap does not depend on legacy migration chain
```

Also prove CLI is not a hidden second persistent lifecycle.

Historical source/config/migrations may remain when explicitly classified as retired/history-only/non-authoritative. Archive/source-cleanup residuals belong to G08/TD-006 when the G07 authority boundary is already satisfied.

---

## 13. BLOCKED Conditions

Mark the current package `BLOCKED` instead of improvising if repository evidence shows:

1. Product runtime genuinely requires legacy runtime and replacement would alter a passed G02–G06 contract;
2. clean Product bootstrap actually requires root legacy migrations/historical data migration despite HD-006;
3. an existing user-visible/auditable CLI persistently bypasses canonical Execution and needs a new product decision;
4. Product-required shared science can only be retained by preserving legacy orchestration or redesigning scientific algorithms;
5. local branch state contradicts the passed G06 authority model.

A desire to delete more legacy source is not a blocker.

---

## 14. Next Instruction

After P00 is committed, create:

```text
10_enhance_instruction/G07/
06_G07_P01_runtime_deployment_shared_boundary.md
```

P01 must stay compact and delegate Trial/report/PG/fixed-candidate/classification rules to this P00.

Recommended P01 structure:

```text
1. Objective
2. Minimal inputs
3. Entry state
4. Current expected facts
5. Required implementation / audit
6. Focused verification
7. Acceptance criteria
8. Checkpoint
9. P02 handoff
```

---

## 15. P00 Completion

P00 is complete when the implementation agent records the actual G07 entry SHA and adopts:

```text
AC-001..005
HD-005..007
P01..P04 decomposition
TD-005 closure rule
G02..G06 preservation contract
legacy source presence != active authority
common-rule delegation to P00
```

P00 itself changes no production behavior and satisfies no Gate AC by itself.
