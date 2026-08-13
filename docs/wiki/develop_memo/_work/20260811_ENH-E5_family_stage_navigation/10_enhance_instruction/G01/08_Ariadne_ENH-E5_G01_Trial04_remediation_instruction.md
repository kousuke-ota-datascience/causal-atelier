# Ariadne ENH-E5 G01 Trial04 Remediation Instruction

- Contract status: `APPROVED / FROZEN`
- GATE_ID: `G01`
- TRIAL_NO: `04`
- PREVIOUS_FAILED_CANDIDATE_SHA: `27e87faecd2b5dac0da6a688201931456c1a6077`
- Remediation mode: `CONSOLIDATED`
- Execution mode: `SINGLE_EXECUTION`

## 1. Failure classification

Trial03 formal FAIL is an implementation defect, not a Gate contract defect.

Original G01 semantic claim and Acceptance Criteria remain unchanged.

Trial03 did not contain the required remediation implementation. Trial04 MUST create a new semantic implementation candidate.

## 2. Required correction

Current Operation Availability route handling accepts:

```text
/projects/p1/analysis/causal/unknown-stage
```

and returns:

```text
RESOURCE_REQUIRED
```

This is incorrect.

Unknown or malformed canonical routes MUST fail before resource / operation projection with:

```text
OperationAvailabilityError
code = INVALID_NAVIGATION_ROUTE
status = 422
```

## 3. Canonical navigation authority

Canonical Family / Stage membership MUST use:

```text
src/ariadne/product/application/navigation_catalog.py
```

Do not duplicate the full Family/Stage catalog inside `ProductClosureService`.

A structural regex may parse route shape, but regex acceptance alone MUST NOT establish canonical route validity.

## 4. Required validation

For:

```text
/projects/{project_id}/analysis/{family_slug}/{stage_slug}
```

validate before resource/authorization/projection:

1. canonical route shape
2. route project ID == endpoint project ID
3. canonical Family exists
4. Stage belongs to that Family

For resource deep routes, also validate route resource type is one of:

```text
analysis-specification
execution
result
graph-version
```

Required ordering:

```text
unknown/malformed route
    -> INVALID_NAVIGATION_ROUTE

valid canonical route + missing concrete resource
    -> existing RESOURCE_REQUIRED behavior where applicable
```

## 5. Required backend regression coverage

Add automated backend regression coverage for:

- valid canonical Family/Stage route
- unknown Stage -> `INVALID_NAVIGATION_ROUTE`
- unknown Family -> `INVALID_NAVIGATION_ROUTE`
- malformed route -> `INVALID_NAVIGATION_ROUTE`
- unknown route resource type -> `INVALID_NAVIGATION_ROUTE`
- endpoint project / route project mismatch -> `INVALID_NAVIGATION_ROUTE`

At least one test MUST directly call `ProductClosureService.operation_availability(...)` and assert:

```text
error.code == "INVALID_NAVIGATION_ROUTE"
error.status == 422
```

Frontend-only parser tests are insufficient.

## 6. Protected behavior

Preserve unrelated G01 semantics, including:

- `RUN / EDIT / EXPORT`
- query resource-pair semantics
- authorization behavior
- lifecycle/domain reason codes
- persistence/schema/migration state
- navigation UI behavior
- predictive regression behavior

Do not weaken/delete/skip/xfail existing tests.

## 7. Expected change surfaces

Expected minimal surfaces:

```text
src/ariadne/product/application/product_closure_service.py
tests/product/
```

## 8. Mandatory verification

Run compileall, affected G00/G01/predictive tests including the new backend Operation Availability regression, and:

```bash
git diff --check
```

All required checks MUST pass.

## 9. New candidate invariant

Trial04 candidate MUST NOT equal:

```text
27e87faecd2b5dac0da6a688201931456c1a6077
```

Before `READY_FOR_TEST`:

```bash
git diff --name-only   27e87faecd2b5dac0da6a688201931456c1a6077..<FIXED_TRIAL_CANDIDATE_SHA>   -- src frontend tests pyproject.toml uv.lock alembic
```

The diff MUST include:

- production source change under `src/`
- automated regression change under `tests/`

Otherwise:

```text
BLOCKED_REMEDIATION_NOT_APPLIED
```

## 10. Execution / handoff

Use only:

```text
fail_rework_coding_agent_prompt.md
GATE_ID=G01
TRIAL_NO=04
```

Do NOT run Trial04 P01/P02/P03 Work Package agents.

The FAIL Rework Coding Agent owns:

```text
implementation correction
-> regression tests
-> implementation checkpoint
-> FIXED_TRIAL_CANDIDATE_SHA
-> canonical Completion Report
-> evidence commit/push
-> READY_FOR_TEST
```

Canonical Completion Report:

```text
docs/wiki/develop_memo/_work/20260811_ENH-E5_family_stage_navigation/
20_implementation_reports/G01/Trial04/
E5-G01_04__implementation_completion.md
```

Trial02/Trial03 evidence remains immutable.
