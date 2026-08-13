# ENH-E6 G01 — P00 Work Package Plan

- Status: `DRAFT / ACTIVATION_PROHIBITED_UNTIL_06_07_FREEZE`

## Package DAG

```text
P01 Navigation transition authority
  -> P02 Stage-aware presentation / legacy compatibility
      -> P03 Browser regression / test strengthening
  -> P03
```

## P01 — Navigation transition authority

Scope:

- unify context apply lifecycle
- converge Family click / Stage click / restore / popstate
- shell show/hide lifecycle

Exit evidence:

- focused unit/DOM tests
- no legacy semantics regression

## P02 — Presentation binding / compatibility

Scope:

- `(family, stage)` presentation binding
- Causal discovery/inference boundary
- legacy analytical left-nav shortcut canonical targets
- fail-closed missing binding

Exit evidence:

- focused DOM/integration tests
- Causal representative routes correct

## P03 — Verification strengthening

Scope:

- real Family tab click browser regression
- normal entry without reload
- deep link / reload / back-forward
- update source-only tests so they supplement, not replace, observable proof

Exit evidence:

- blocking browser journeys executable and green on package candidate

## Candidate assembly

P01/P02/P03 checkpointを1 fixed candidateへassemblyし、そのSHAのみをIndependent Verificationへ提出する。Package PASSをGate PASSと表現しない。
