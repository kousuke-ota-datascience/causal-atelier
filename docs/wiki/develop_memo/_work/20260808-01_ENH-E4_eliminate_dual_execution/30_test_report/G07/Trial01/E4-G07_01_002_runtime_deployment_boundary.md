# E4-G07 Trial01 — 002 Runtime / Deployment Boundary

## Result

`PASS`

## Evidence

Command:

```text
uv run pytest -q tests/product/test_architecture.py tests/product/test_enh_e4_g07_p01_runtime_boundary.py
6 passed in 4.31s
```

The independent source/config inspection and P01 guard establish that canonical Product/API/worker roots cannot reach `ariadne.legacy`; the worker entry point is `ariadne.interfaces.worker.runner:main`; compose invokes `ariadne-worker`; Product images exclude the legacy package; and deployment migration wiring is Product-only. Physical `src/ariadne/legacy/` remains but is non-authoritative and unreachable.

## AC mapping

- AC-001: PASS — Product runtime legacy reachability is zero.
- AC-002: PASS — repository-managed deployment has no legacy API/CLI/worker invocation.

## Facts / Interpretation / Unknown

- Fact: both required tests passed.
- Interpretation: runtime/deployment boundary satisfies the G07 contract.
- Unknown: none material to this item.

