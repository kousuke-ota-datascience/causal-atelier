# G02 Trial02 — Environment Recovery and Frozen Browser E2E Rerun

- Gate: `G02`
- Trial: `02`
- Test Item ID: `004`
- Fixed Trial Candidate SHA: `7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a`
- Prior BLOCKED report commit: `d9d325512fb90463a2f5200897ba3c23db220845`
- Result: `PASS`

## Acceptance Criteria

Recovery proof for the frozen Browser E2E portions of `G02-AC02`, `G02-AC04`–`G02-AC09`, `G02-AC14`–`G02-AC15`, `G02-AC17`, `G02-AC19`, `G02-AC22`, and `G02-AC23`.

## Prior BLOCKED cause

The prior Trial02 verification was `BLOCKED` because its root-squashed worktree mounted `./test-results/browser_e2e` at `/evidence` without write permission for the browser runner. Causal screenshot/evidence JSON and Predictive evidence JSON writes raised `PermissionError` after environment bootstrap.

## Recovery environment and identity audit

```bash
git -C /var/tmp/ariadne-e8-g02-trial02-retry-20260821231603 rev-parse HEAD
git -C /var/tmp/ariadne-e8-g02-trial02-retry-20260821231603 status --porcelain=v1
findmnt -T /var/tmp/ariadne-e8-g02-trial02-retry-20260821231603
ls -ld /var/tmp/ariadne-e8-g02-trial02-retry-20260821231603/test-results/browser_e2e
```

- The recovery worktree is `/var/tmp/ariadne-e8-g02-trial02-retry-20260821231603` on local ext4 and resolves exactly to `7e1bbab9f4509a7ef139b0660bc7d8976ab84f4a`.
- Its evidence directory is owned by the browser runner identity (`uid=1000`, `gid=1000`) with mode `0770`.
- The successful generated evidence files below are the container `/evidence` write probe/result: the runner created JSON evidence and a Causal screenshot without a permission error.
- The rebuilt image copied both required G02 runners, as shown by the successful frozen commands.

## Frozen Causal command and result

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py
```

Result: `PASS` (`{"evidence": "/evidence/enh-e8-g02-causal-stage-content-evidence.json", "status": "PASS"}`). Compose database became healthy, migration exited `0`, API became healthy, and frontend/worker started. Generated evidence records PASS for Identification, Estimation, Effects, Diagnostics, and Sensitivity, including the required Back/Forward transition.

## Frozen Predictive command and result

```bash
docker compose -f compose.yaml -f compose.e1a.yaml -p ariadne-e8 \
  --profile e2e run --build --rm --entrypoint python browser-e2e \
  tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py
```

Result: `PASS` (`{"status": "PASS", "evidence": "/evidence/enh-e8-g02-predictive-stage-content-evidence.json"}`). Compose bootstrap again completed successfully. Generated evidence records PASS for Setup, Train, Predict, Metrics, Explainability, and Model Management, including history Back/Forward.

## Generated Browser E2E evidence

- `/var/tmp/ariadne-e8-g02-trial02-retry-20260821231603/test-results/browser_e2e/enh-e8-g02-causal-stage-content-evidence.json`: `status: PASS`; five Causal stages all `PASS`.
- `/var/tmp/ariadne-e8-g02-trial02-retry-20260821231603/test-results/browser_e2e/enh-e8-g02-causal-stage-content.png`: generated successfully.
- `/var/tmp/ariadne-e8-g02-trial02-retry-20260821231603/test-results/browser_e2e/enh-e8-g02-predictive-stage-content-evidence.json`: `status: PASS`; six Predictive stages all `PASS`.

## Classification rationale

No product mismatch was observed. The prior harness blocker is resolved in the local recovery worktree, both exact frozen commands exit successfully and emit their required evidence, and their logs show healthy Compose bootstrap. Therefore this retry is `PASS`, not `FAIL` or `BLOCKED`.
