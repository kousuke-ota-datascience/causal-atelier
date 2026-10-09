# G02 Trial 01 — 050 lime_binary_local (reverification 03)

## Scope / method

AC-05: binary local LIME on the preprocessed feature space. The independent G02 suite executed provider-backed `explain_lime_local` and runner integration using a fixed seed/fixture.

## Facts / raw result

```text
G02 suite: 13 passed, 1 warning in 14.24s
exit code: 0
```

The binary provider test asserts `output_scale == PROBABILITY`, non-empty signed provider contributions, and `reference.partition == TRAIN`. The runner integration asserts `PREDICTIVE_EXPLANATION_RESULT` is `GENERATED`, local output is non-empty, and the reference is explicitly TRAIN while the explained rows originate from the TEST explanation dataset.

The implementation records per-row effective seed, frozen parameters (`num_samples=2000`; `num_features=min(10,n_features)`; no continuous discretization; euclidean distance; `0.75*sqrt(n_features)` kernel; no sample-around-instance), feature order, instance values, output, contribution mapping, and reference hash/count/seed.

## Interpretation / result

The binary provider/local-output criterion is satisfied in this runtime. Target/candidate identities are in item 001. **Result: PASS.**

This item does not establish Model Card provenance; that distinct AC-09 failure is recorded in item 080.
