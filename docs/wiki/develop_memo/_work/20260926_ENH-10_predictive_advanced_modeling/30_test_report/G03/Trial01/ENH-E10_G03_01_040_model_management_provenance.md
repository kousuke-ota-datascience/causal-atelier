# ENH-E10 G03 Trial 01 — Test Item 040: Model Management Provenance

| Candidate | Tested SHA | AC | Result |
| --- | --- | --- | --- |
| `64bd2a18dd583349283cd5745edf63d9b28d61ad` | `df278f76ff476143545d73037fe55f96664dae28` | AC-06, AC-07 | **PASS** |

## Method / evidence

The 58-test independent command includes G01 artifact/load/predict tests and G02 result/artifact/model-card provenance tests. Browser scenarios 100/110 asserted a `MODEL_CARD_RESULT` with model descriptor, the `MODEL_CARD` and `FITTED_MODEL` artifacts, generated explanation result, and predictive terminology at the final UI state.

## Observed facts

- G01 artifact tests preserve `fitted-model/2`, provider/version/runtime identity and load/predict parity.
- G02 tests verify Result → Explanation Artifact → Model Card provenance equality, including model/task/preprocessor/feature identity, provider/runtime version, output scale, and method-specific background/reference facts.
- browser evidence records required result types and artifact types for scenario 100 and 110: `FITTED_MODEL`, `MODEL_CARD`, `PREDICTIVE_EXPLANATION`, `PREDICTION`, `FITTED_PREPROCESSOR`, `PARTITION_INDEX`.

## Interpretation

Model Management’s read-oriented provenance contract is present across API persistence and the user-visible critical journey. AC-06/07 are **PASS**。

## Reproduction / source mutation audit / criterion evaluation

```bash
MPLCONFIGDIR=/tmp/ariadne-mpl UV_CACHE_DIR=/tmp/ariadne-uv-cache uv run --extra predictive-advanced pytest -q tests/enhancement/enh_e10/g01/integration tests/enhancement/enh_e10/g02/integration tests/product/test_predictive_api_worker_e2e_e3.py
```

Observed exit code: `0` within the 58-test suite. Browser reproduction uses the frozen command in item 100/110 and requires `MODEL_CARD_RESULT`, `FITTED_MODEL`, `MODEL_CARD`, and `PREDICTIVE_EXPLANATION`. Candidate mutation audit found no Model Management frontend/API semantic change after candidate; post-candidate state is documentation-only. Result/artifact/model-card equality establishes AC-06 and provenance/terminology establishes AC-07. **PASS**。
