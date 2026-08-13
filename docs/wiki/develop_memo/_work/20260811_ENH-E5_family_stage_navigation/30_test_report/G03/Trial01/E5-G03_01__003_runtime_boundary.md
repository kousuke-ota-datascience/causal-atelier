# ENH-E5 G03 Trial 01 — Test Item 003: Runtime boundary and prerequisites

## Scope and result

| Acceptance criterion | Result |
| --- | --- |
| `AC-G03-002` — current operation, StageType, and prerequisite matrix unchanged | PASS |
| `AC-G03-004` — Estimation preserves graph and upstream-result prerequisites | PASS |
| `AC-G03-005` — navigation does not generate a runtime execution revision | PASS |

Test target: `1a80c1cec740126f66e21e251ee2d0204819cfd9`.

## Raw evidence

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q \
  tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py \
  tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py
```

Observed output:

```text
......                                                                   [100%]
6 passed in 1.08s
```

The executed runtime test asserts one Stage per operation with these observed expected mappings and input contracts:

```text
DISCOVERY      causal.discovery.v1       dataset_path, output_dir
IDENTIFICATION causal.identification.v1  dataset_path, output_dir, graph_path
ESTIMATION     causal.estimation.v2      dataset_path, output_dir, graph_path, upstream_result, upstream_execution
REFUTATION     causal.refutation.v1      dataset_path, output_dir, graph_path, upstream_result, upstream_execution
SENSITIVITY    causal.sensitivity.v1     dataset_path, output_dir, graph_path, upstream_result, upstream_execution
```

It also asserts a navigation-stage change has no execution revision metadata.

## Judgment

**Fact:** all assertions passed.

**Inference:** the frozen operation/StageType/input-prerequisite contract is preserved, including Estimation's graph and upstream-result prerequisites.
