# ENH-E7 G03 Trial01 Test Item 006 — obsolete_shell_absence

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: G03 focused pytest suite including `test_enh_e7_g03_p05_obsolete_global_shell_cleanup.py`; source/diff audit; Chromium runtime root/visibility probe.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-08, AC-G03-09, AC-G03-10, AC-G03-11 | PASS |

## Direct assertion / predicate mapping

- source tests assert absence of `<aside`, `selected-project-shell`, `common-workspace-header`, `data-hidden-on-projects-surface`, `renderCommonWorkspaceHeader`, and CSS `aside`.
- one production owner each for `project-management-navigation` and `analysis-routing-actions`; runtime has exactly one visible top-level root.

## Raw relevant evidence

- Focused suite: `15 passed in 1.34s`。
- candidate-after diff is empty; runtime probe returns exactly one active root for each tested route.

## Facts

- obsolete global sidebar/common header/compatibility visibility binding is absent from production sources and no duplicate visible root is retained.

## Interpretation

- old architecture is not preserved as hidden DOM or stale presentation binding.

## Protected contract relation

- replacement ownership is verified by Items 002–004 rather than absence alone。

## Reproduction procedure

1. Item 002 の focused pytest command を実行する。
2. Item 001 の diff audit と browser root query を実行する。

## Browser evidence

- Success screenshots: `enh-e7-g03-p06-projects.png`, `enh-e7-g03-p06-project-management.png`, `enh-e7-g03-independent-direct-analysis.png` under `test-results/browser_e2e/`。
- console/page error: none。network/service log: API READY。
