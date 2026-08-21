# G01 Trial01 — Browser Integration and Protected Regression Evidence

- Gate: `G01`
- Trial: `01`
- Test Item ID: `002`
- Candidate SHA: `f62e3e75ba474928d6f2ca886e9992375c6f16e5`
- Result: `BLOCKED`

## Acceptance Criteria

- `G01-AC03`, `G01-AC04`, `G01-AC06`, `G01-AC08`

## Method / command

The frozen Gate 07 command was invoked from the isolated exact-candidate worktree:

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g01_project_return.py
```

## Evidence

- The command built the candidate API, worker, and migration images, then Compose created the dependency containers.
- Before the browser runner started or generated `enh-e8-g01-project-return-evidence.json`, the `migrate` container exited with `sqlalchemy.exc.OperationalError`: `failed to resolve host 'database': [Errno -3] Temporary failure in name resolution`.
- Consequently API/frontend never reached the semantic ready state required by the runner and no Chromium scenario ran.
- The failed bootstrap condition is outside the candidate product diff: the candidate changes no backend, migration, database, Compose, or DNS configuration.
- The protected browser regression runner `tests/browser_e2e/run_enh_e7_project_integration.py` was inspected and is applicable to both Project local navigation and Analysis launch-navigation, but was not run because the same required browser harness was unavailable.

## 判定理由

This is an environment/harness bootstrap failure before the test subject can be exercised. Under frozen Gate 07, it makes the integration criteria indeterminate and therefore `BLOCKED`, not product `FAIL`.
