# ENH-E7 Agent Entry Variable Conventions

## Enhancement-fixed values

```text
PROJECT_NAME=Ariadne
ENHANCE_ID=ENH-E7
ENHANCE_SHORT_ID=E7
BRANCH_NAME=feature/ariadne_mvp_e7
WORK_ROOT=docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation
WORK_DIR_NAME=20260813_ENH-E7_project_analysis_workspace_separation
REMOTE_NAME=REQUIRES_LOCAL_VERIFICATION
BASELINE_FULL_SHA=REQUIRES_LOCAL_VERIFICATION
```

`REMOTE_NAME` and `BASELINE_FULL_SHA` are deliberately unresolved sentinels because they require local repository observation. They must be replaced with verified concrete values before execution.

No enhancement-fixed `{...}` placeholders are permitted in this instance.

## Runtime values supplied by Human

```text
GATE_ID=<G01|G02>
PACKAGE_ID=<P01..>
TRIAL_NO=<01..>

only when applicable:
REMEDIATION_PACKAGE_ID=<R01..>
AMENDMENT_ID=<A01..>
```

Runtime values must resolve the execution target to exactly one artifact.
