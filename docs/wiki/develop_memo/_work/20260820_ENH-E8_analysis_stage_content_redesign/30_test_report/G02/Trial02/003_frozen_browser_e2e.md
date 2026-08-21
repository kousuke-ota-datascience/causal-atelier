# G02 Trial02 — Frozen Browser E2E

- Gate: `G02`
- Trial: `02`
- Test Item ID: `003`
- Fixed Trial Candidate SHA: `7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a`
- Result: `BLOCKED`

## Acceptance Criteria

The frozen Chromium journeys are required cross-layer evidence for `G02-AC02`, `G02-AC04`–`G02-AC09`, `G02-AC14`–`G02-AC15`, `G02-AC17`, `G02-AC19`, `G02-AC22`, and `G02-AC23`.

## Method / command

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py

docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
```

## Evidence

- Both commands rebuilt the exact candidate image and the image copied both G02 runner files to the frozen paths.
- For each command, Compose database health, migration (`Exited (0)`), API health, frontend, and worker startup succeeded.
- The Causal runner proceeded through its interaction path but failed when writing screenshot/evidence under the configured `/evidence` mount. Error: `PermissionError: [Errno 13] Permission denied: '/evidence/enh-e8-g02-causal-stage-content.png'`; its fallback screenshot and evidence JSON writes failed for the same reason.
- The Predictive runner likewise reached final evidence emission but failed with `PermissionError: [Errno 13] Permission denied: '/evidence/enh-e8-g02-predictive-stage-content-evidence.json'`.
- The evidence mount maps `./test-results/browser_e2e` to `/evidence`. On this root-squashed filesystem it was `nobody:nogroup` and not writable by the configured runner. Attempting to change only that ephemeral directory to mode `0777` was rejected with `Operation not permitted`; retrying the Causal command with `ARIADNE_E2E_USER=65534:65534` produced the same error.

## 判定理由

The candidate delivery defect from Trial01 is fixed: both runners are present in the rebuilt image. The remaining non-zero exits are caused solely by the externally hosted, root-squashed evidence-volume permission policy after Compose bootstrap and candidate runner startup. Frozen Gate 07 specifies `BLOCKED` when the environment/harness prevents a determination. No valid-candidate product mismatch was observed, and the required browser evidence could not be emitted; therefore this item is `BLOCKED`.

## Re-execution

The two frozen commands were independently rerun against the same SHA after the initial Trial02 decision. Identity was rechecked in the same detached exact-candidate worktree. Both commands again rebuilt the candidate image, completed Compose bootstrap, and failed only at `/evidence` writes with the identical `PermissionError` paths above. This confirms that the blocker remains an unresolved harness/evidence-volume condition, not a transient candidate product failure.
