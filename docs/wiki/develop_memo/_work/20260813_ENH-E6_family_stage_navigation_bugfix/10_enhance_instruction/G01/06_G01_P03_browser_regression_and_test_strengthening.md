# ENH-E6 G01 P03 — Browser Regression and Test Strengthening

- Status: `APPROVED / WAITING_FOR_P01_P02_CHECKPOINTS`

## Outcome

ANOM-E5-001を再発させないobservable acceptance evidenceを実装する。

## Required browser coverage

- normal analysis entry immediately shows actual Family tabs
- actual Family tab click -> default Stage
- actual Stage click -> Family retained
- Causal discovery/inference presentation binding
- legacy shortcut canonical targets
- direct canonical route
- reload
- back/forward

## Existing source-inspection tests

`analysis-family-tabs` stringや`catalog.families.map` stringの検査はsupplemental static protectionとして残してよい。ただしreal-browser blocking proofの代替として扱わない。

## Anti-patterns

- test中にrendererを直接呼んでnormal entry defectを回避
- forced reload before first assertion
- hidden elementのtext existenceだけをvisible扱い

## Canonical runner / harness integration

Create:

- `tests/browser_e2e/run_enh_e6_family_stage_navigation.py`

Ensure executable inside the existing `browser-e2e` image. Review and update as required:

- `Dockerfile.browser-e2e`
- `.dockerignore`

Canonical execution command:

```bash
docker compose \
  -f compose.yaml \
  -f compose.e1a.yaml \
  -p ariadne-e1a \
  --profile e2e \
  run --build --rm \
  --entrypoint python \
  browser-e2e \
  tests/browser_e2e/run_enh_e6_family_stage_navigation.py
```

The runner MUST wait for `#health` = `API READY`, establish a deterministic Project context, and exercise actual Family / Stage elements.
