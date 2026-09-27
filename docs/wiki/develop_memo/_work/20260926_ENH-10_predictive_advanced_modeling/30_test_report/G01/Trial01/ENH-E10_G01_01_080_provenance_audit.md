# G01 Trial 01 — 080 provenance_audit

## Scope

AC-07: artifact/runtime evidence records model identity, task, effective parameters, seed/determinism, feature/preprocessor identity, and analytical package version.

## Method / raw evidence

The direct binary and regression fixture probe recorded in items 030/040 observed, for both artifacts: model ID and task type; resolved parameter map; feature order `[x, group]`; preprocessor hash; seed `719`; runtime determinism (`deterministic=true`, CPU, `force_col_wise=true`, `num_threads=1`); and provenance `lightgbm_version=4.7.0`, Python `3.12.3`, Ariadne `0.1.0`. The respective serialized artifact hashes are `6690bd3352e51025289db2e218cd1f3482fa4153cafa7624f563251c4da902be` and `b98ea0f06b944e4fb979da617b8571e5a78796809e3a711c37ac250b77b3d6f4`.

The adapter/artifact contract suite also completed `15 passed in 8.36s`, exit code 0.

Target HEAD: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

## Result

**PASS.**
