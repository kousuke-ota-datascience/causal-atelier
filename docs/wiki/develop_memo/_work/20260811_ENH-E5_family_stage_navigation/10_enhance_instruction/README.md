# ENH-E5 Gate / Work Package Contracts — Phase K Remediated Candidate

- 状態: `PHASE_K_REMEDIATED / REAUDIT_PENDING`
- Branch: `feature/ariadne_mvp_e5`
- Remediation baseline SHA: `a4d96b33c81b5a263a2e82e6d64475de5085b616`
- Canonical source: `NFR-019 PASS / FROZEN`

## Authority model

```text
SINGLE_EXECUTION Coding
  -> Gate 06 only

WORK_PACKAGE Coding
  -> assigned Pxx only
  -> Gate 06 / P00 / other Pxx are not Package Coding Agent inputs

Test / Audit
  -> Gate 07 only
```

repositoryはimplementation/evidence substrateであり仕様authorityではない。ambiguityは`BLOCKED_CONTRACT_AMBIGUITY`。

## Gate map

| Gate | Mode | Responsibility |
|---|---|---|
| G00 | SINGLE_EXECUTION | Navigation descriptor/catalog/read API |
| G01 | WORK_PACKAGE | route/deep navigation/shell/action state/history/accessibility |
| G02 | WORK_PACKAGE | Predictive compatibility/subgroup evaluation |
| G03 | WORK_PACKAGE | Causal recomposition/Identification-Estimation |
| G04 | WORK_PACKAGE | Exploratory typed filter/handoff/provenance |
| G05 | SINGLE_EXECUTION | comparability/reuse/idempotency/auth/lineage/reproducibility/full convergence |

## Re-audit rule

本changeset適用後は`PHASE_K_REMEDIATED / REAUDIT_PENDING`。35文書のauthority/self-containment/D2/D3/06-Pxx-07 symmetry再監査がall PASSした後にのみ`PHASE_K_CONVERGED / EXECUTION_FREEZE_READY`へ変更する。
