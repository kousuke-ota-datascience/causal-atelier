# ENH-E5 G01 Trial 03 Remediation Contract

Document class: Derived Contract  
Self-containment: `CONSOLIDATED` — formal FAIL 後の next Trial rework を本書だけで実行可能にする。

- Gate: `G01`
- New Trial: `03`
- Failed Trial: `02`
- Failed Gate Decision: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G01/Trial02/E5-G01_02__999_gate_decision.md`
- Failed Test Item: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/30_test_report/G01/Trial02/E5-G01_02__003_operation_availability.md`
- Failed candidate: `27e87faecd2b5dac0da6a688201931456c1a6077`
- Original 06: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/06_Ariadne_ENH-E5_G01_implementation_instruction.md`
- Original P02: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/06_G01_P02_navigation_shell_ui.md`
- Original 07: `docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/10_enhance_instruction/G01/07_Ariadne_ENH-E5_G01_test_instruction.md`
- Remediation Mode: `CONSOLIDATED`
- Execution Mode: `SINGLE_EXECUTION`
- Contract status: `APPROVED / FROZEN`

## 1. Contract validity check / existence condition

- Original Gate semantic claim remains valid: `YES`
- Original Acceptance Criteria remain valid: `YES`
- Gate Contract Amendment (`09`) required: `NO`

Trial02 FAIL は Gate contract defect ではなく implementation defect である。

Original 06 / P02 / 07 を書き換えてはならない。

## 2. Verified failure facts

Trial02 independent verification では candidate identity audit は PASS した。

Independent automated suite は `14 passed` だったが、Operation Availability の negative verification が FAIL した。

Failing input:

```text
project_id=p1
resource_type=None
resource_id=None
route=/projects/p1/analysis/causal/unknown-stage
```

Observed result:

```text
{
  "operations": {
    "RUN": {"allowed": false, "reason_code": "RESOURCE_REQUIRED"},
    "EDIT": {"allowed": false, "reason_code": "RESOURCE_REQUIRED"},
    "EXPORT": {"allowed": false, "reason_code": "RESOURCE_REQUIRED"}
  }
}
```

Required result:

```text
HTTP 422 / INVALID_NAVIGATION_ROUTE
```

Root cause in failed candidate:

- Operation Availability route validation uses a regex for structural shape.
- The Stage segment is accepted as an arbitrary non-slash string.
- The implementation does not verify that the Stage slug belongs to the selected Family in the canonical navigation catalog.
- Therefore `unknown-stage` passes structural parsing.
- Because `resource_type` is absent, execution subsequently enters the route-only/resource-missing branch and incorrectly returns `RESOURCE_REQUIRED`.

This is not a Test Agent defect and not a contract ambiguity.

## 3. Effective implementation semantics for Trial03

### 3.1 Canonical route validation

`operation_availability(...)` MUST distinguish:

1. syntactic route shape validation; and
2. semantic canonical navigation validation.

A route is valid only when all applicable route components are canonical.

For:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

the implementation MUST verify:

- `project_id` equals the endpoint project;
- `family_slug` exists in the canonical navigation catalog;
- `stage_slug` exists in that Family's canonical Stage list.

For resource deep routes:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}/resource/{resource_type}/{resource_id}
```

the route MUST additionally use a canonical ENH-E5 resource type.

A malformed route or a route containing an unknown Family / Stage / route resource type MUST fail before operation projection is evaluated.

Required request-level failure:

```text
OperationAvailabilityError
code = INVALID_NAVIGATION_ROUTE
status = 422
```

### 3.2 Canonical authority

The canonical Family / Stage vocabulary MUST come from the existing backend navigation catalog authority:

```text
src/ariadne/product/application/navigation_catalog.py
```

The remediation MUST NOT create a second hard-coded full Family/Stage catalog inside `ProductClosureService`.

A structural regex MAY remain for parsing route shape, but regex acceptance alone MUST NOT establish canonical route validity.

### 3.3 Evaluation ordering

For a request containing `route`, canonical route validation MUST complete before:

- Project READ operation projection;
- resource-required projection;
- structural operation support projection;
- per-operation authorization;
- lifecycle/domain prerequisite projection.

In particular:

```text
valid canonical route + no concrete resource
    -> RESOURCE_REQUIRED may be returned where required

unknown/malformed canonical route
    -> INVALID_NAVIGATION_ROUTE
```

`RESOURCE_REQUIRED` MUST NOT mask an invalid route.

### 3.4 Scope preservation

The remediation MUST preserve the existing canonical Operation Availability contract outside this defect:

- canonical operation keys remain exactly `RUN / EDIT / EXPORT`;
- existing resource-pair query semantics remain unchanged;
- existing role / authorization behavior remains unchanged;
- existing resource resolution / project-boundary behavior remains unchanged;
- existing lifecycle/domain reason codes remain unchanged;
- Stage visibility and action availability remain separate;
- no persistence/schema/migration change is required.

## 4. Required automated regression coverage

Trial03 MUST add automated coverage that exercises Operation Availability route validation itself.

At minimum verify:

1. canonical route-only request is accepted and can reach the existing route-only projection behavior;
2. unknown Stage route is rejected with `INVALID_NAVIGATION_ROUTE`;
3. malformed canonical route is rejected with `INVALID_NAVIGATION_ROUTE`;
4. unknown Family route is rejected;
5. a route with noncanonical resource type is rejected before resource projection.

The required regression MUST call the backend Operation Availability implementation or its HTTP endpoint. A frontend-only navigation parser test is insufficient.

The existing frontend navigation-state negative tests MUST remain intact.

## 5. Required verification

The rework Coding Agent MUST run at least:

```bash
PYTHONDONTWRITEBYTECODE=1 UV_CACHE_DIR=/tmp/ariadne-uv-cache \
uv run python -m compileall -q src
```

```bash
UV_CACHE_DIR=/tmp/ariadne-uv-cache PYTHONDONTWRITEBYTECODE=1 \
uv run pytest -q \
  tests/product/test_enh_e5_g01_navigation_shell.py \
  tests/product/test_enh_e5_g01_navigation_state.py \
  tests/product/test_enh_e5_g00_navigation.py \
  tests/product/test_enh_e5_g01_history_accessibility.py \
  tests/product/test_predictive_frontend_contract_e3.py
```

The added Operation Availability negative regression test MUST be included in the executed suite.

Also run:

```bash
git diff --check
```

All required checks MUST pass before candidate handoff.

## 6. Allowed remediation scope

Expected implementation/test surfaces include:

```text
src/ariadne/product/application/product_closure_service.py
src/ariadne/product/application/navigation_catalog.py
tests/product/test_enh_e5_g01_navigation_shell.py
```

A different minimal location is allowed when repository structure makes it more appropriate, provided the effective semantics in this 08 remain exact.

Changes outside the route-validation defect and its regression coverage require explicit justification.

## 7. Explicitly forbidden workaround

The following are prohibited:

- accepting unknown Stage and changing Test expectations;
- weakening, deleting, skipping, or xfail-ing the failing assertion;
- rewriting original 06 / P02 / 07 to permit the current behavior;
- treating `RESOURCE_REQUIRED` as valid for an unknown Stage;
- hard-coding only the literal string `unknown-stage` as a rejection;
- duplicating the complete canonical Family/Stage catalog inside `ProductClosureService`;
- frontend-only validation used as a substitute for backend validation;
- changing unrelated Operation Availability semantics to make the test green.

## 8. Acceptance Criteria invariance

- 07 silently rewritten: `NO`
- Acceptance Criteria relaxed: `NO`
- Gate semantic claim changed by this 08: `NO`
- AC-G01-003 remains unchanged.
- AC-G01-007 remains unchanged.

## 9. Remediation decomposition

- Remediation packages required: `NO`
- Rxx required: `NO`
- Execution is a single bounded rework.

The rework Coding Agent uses this 08 as the normative remediation contract.

Repository source and failed Test evidence may be inspected as implementation/evidence substrate, but must not be used to redefine required semantics.

## 10. Completion / handoff condition

Trial03 implementation remediation is complete only when:

1. unknown Stage no longer reaches the `RESOURCE_REQUIRED` projection;
2. canonical navigation membership is validated by backend Operation Availability;
3. required negative regression coverage exists;
4. all required Coding-side verification passes;
5. working tree is clean after implementation evidence is committed;
6. a new Trial03 candidate is assembled;
7. a new `FIXED_TRIAL_CANDIDATE_SHA` is recorded in the Trial03 Implementation Completion Report.

Trial02 candidate and Test evidence remain immutable historical evidence.

A new Fixed Trial Candidate SHA MUST be generated and independently verified under G01 Trial03.
