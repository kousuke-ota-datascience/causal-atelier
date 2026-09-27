# G01 Trial 01 — 050 negative_contracts

## Scope

AC-02 and AC-06: incompatible model/task, invalid parameter, feature-order and preprocessor mismatches are distinguishable failures.

## Method / raw evidence

Target HEAD: `77f4c74601a4fd518f307542ae10730e1f8eb903`; fixed candidate: `936aebc9ac773cd9621ec8bf9b34fcc1b7f6324c`.

The independent P01/P02/P03 test commands in items 010 and 030 completed successfully (7 + 15 tests, exit code 0). Their asserted error taxonomy includes `MODEL_NOT_REGISTERED`, `MODEL_TASK_MISMATCH`, `MODEL_PARAMETER_INVALID`, `MODEL_FEATURE_MISMATCH`, and `PREPROCESSOR_MODEL_MISMATCH`; parameter cases include zero rounds, out-of-range values, and unsupported keys.

## Result

**PASS.** The contract tests exercised each required negative boundary with distinct error codes.
