# G02 Trial01 — Frozen Browser E2E

- Gate: `G02`
- Trial: `01`
- Test Item ID: `003`
- Fixed Trial Candidate SHA: `a2399662f4f81ceadf36ae2aa71850d49786cae4`
- Result: `FAIL`

## Acceptance Criteria

`G02-AC02`, `G02-AC04`–`G02-AC09`, `G02-AC14`–`G02-AC15`, `G02-AC17`, `G02-AC19`, `G02-AC22`, and `G02-AC23` require the frozen Chromium journey as cross-layer evidence.

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

- Compose bootstrap completed: database healthy, migration exited `0`, API healthy, frontend and worker started.
- Both commands rebuilt the candidate's `browser-e2e` image successfully.
- The build log shows `Dockerfile.browser-e2e` copies E1A/E3/E6/E7/G01 runners only. It contains no `COPY` instruction for either G02 runner.
- Causal command terminated with:

  ```text
  python: can't open file '/workspace/tests/browser_e2e/run_enh_e8_g02_causal_stage_content.py': [Errno 2] No such file or directory
  ```

- Predictive command terminated with:

  ```text
  python: can't open file '/workspace/tests/browser_e2e/run_enh_e8_g02_predictive_stage_content.py': [Errno 2] No such file or directory
  ```

## 判定理由

The frozen commands fail reproducibly after successful environment bootstrap because the **candidate's own browser-image build definition** excludes both required runner files. This is not an external environment/harness inability: `--build` proves the exact candidate image is missing the required artifacts. Therefore the mandatory Browser E2E acceptance evidence is absent due to a valid-candidate implementation/test-delivery mismatch, and the result is `FAIL`.
