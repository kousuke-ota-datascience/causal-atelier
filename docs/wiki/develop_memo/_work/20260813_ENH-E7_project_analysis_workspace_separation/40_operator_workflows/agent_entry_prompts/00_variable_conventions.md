# ENH-E7 Agent Entry Variable Conventions

## Enhancement-fixed values

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E7
ENHANCE_SHORT_ID=E7
BRANCH_NAME=feature/ariadne_mvp_e7
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation
WORK_DIR_NAME=20260813_ENH-E7_project_analysis_workspace_separation
REMOTE_NAME=causal-atelier
BASELINE_FULL_SHA=1beea1c9eb3ffa5d01f7c266b826e52136d01e8f
```

`REMOTE_NAME=causal-atelier` と `BASELINE_FULL_SHA=1beea1c9eb3ffa5d01f7c266b826e52136d01e8f` はHumanから提示されたlocal repository observationを基準値として固定済み。

No enhancement-fixed `{...}` placeholders are permitted in this instance.

## Runtime values supplied by Human

```text
GATE_ID=<Gxx>
PACKAGE_ID=<P01..>
TRIAL_NO=<01..>

only when applicable:
REMEDIATION_PACKAGE_ID=<R01..>
AMENDMENT_ID=<A01..>
```

Runtime values must resolve the execution target to exactly one artifact.
