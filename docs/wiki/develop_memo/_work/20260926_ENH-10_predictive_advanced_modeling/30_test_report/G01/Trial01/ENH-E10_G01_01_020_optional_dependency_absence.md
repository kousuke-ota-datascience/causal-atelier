# G01 Trial 01 — 020 optional_dependency_absence

## Scope

AC-03: core remains usable without LightGBM and LightGBM selection fails explicitly, without fallback.

## Method / raw evidence

Test target: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

The independently run P01 contract suite (recorded in item 010) completed `7 passed`. Its `test_lightgbm_discovery_is_lazy_and_unavailable_models_do_not_fallback` replaces the runtime discovery result with absence before importing LightGBM, verifies the module was not imported, observes `availability.available == False`, and asserts selection raises `PredictiveValidationError` with `MODEL_DEPENDENCY_UNAVAILABLE`.

An additional fully isolated `uv run --isolated --no-extra predictive-advanced` attempt did not reach product code because the local cache lacked transitive package `mpmath==1.3.0`; uv attempted an external download and DNS resolution failed. This is an environment-cache limitation, not a product assertion or a product failure. It was not used as PASS evidence.

## Result

**PASS.** The executable dependency-absence contract test directly simulates the unavailable distribution boundary and verifies explicit capability failure with no fallback. The separate isolated-environment bootstrap was unavailable, but does not invalidate that deterministic test evidence.
