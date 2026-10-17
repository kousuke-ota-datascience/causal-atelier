# G01 Trial 01 — 020 optional_dependency_absence

## Scope

AC-03: core remains usable without LightGBM and LightGBM selection fails explicitly, without fallback.

## Method / raw evidence

Test target: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

The independently run P01 contract suite (recorded in item 010) completed `7 passed`. Its `test_lightgbm_discovery_is_lazy_and_unavailable_models_do_not_fallback` replaces the runtime discovery result with absence before importing LightGBM, verifies the module was not imported, observes `availability.available == False`, and asserts selection raises `PredictiveValidationError` with `MODEL_DEPENDENCY_UNAVAILABLE`.

An additional isolated package-path process was run with Python `-S`, `PYTHONPATH=src:/tmp/e10-g01-no-lightgbm-site`, and a temporary site layer containing symlinks to the current runtime packages except `lightgbm` and `lightgbm-4.7.0.dist-info`. Its raw output was:

```text
lightgbm_spec=None
availability={'available': False, 'version': None, 'reason': 'Optional dependency lightgbm is not installed; install extra predictive-advanced'}
selection_error=MODEL_DEPENDENCY_UNAVAILABLE
exit code: 0
```

An additional fully isolated `uv run --isolated --no-extra predictive-advanced` attempt did not reach product code because the local cache lacked transitive package `mpmath==1.3.0`; uv attempted an external download and DNS resolution failed. This is an environment-cache limitation, not a product assertion or a product failure. It was not used as PASS evidence.

## Result

**PASS.** Both the executable contract test and the isolated package-path runtime observe unavailable LightGBM and explicit non-fallback capability failure. The separate `uv --isolated` bootstrap was unavailable, but is redundant to this successful isolated runtime evidence.
