# ENH-E7 G03 Trial01 Test Item 005 — layout_orientation_runtime

- Result: PASS
- Fixed Trial Candidate full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Tested Repository State full SHA: `cc4fb35b66545af50ed96fd2f80aff7f9a619a5e`
- Exact command / method: Chromium computed CSS and `getBoundingClientRect()` probe on Analysis route.
- Exit code: 0

## AC mapping

| AC | Result |
| --- | --- |
| AC-G03-06, AC-G03-07 | PASS |

## Direct assertion / predicate mapping

- `#analysis-family-tabs` computed `flexDirection == row`。
- `#analysis-stage-sidebar` computed `flexDirection == column`。
- stage box right=301 and main box left=319; therefore Contents main area is right of stage navigation。

## Raw relevant evidence

- Chromium: `familyDirection:"row"`, `stageDirection:"column"`。
- stage bounding box `(left:61,right:301,top:412,bottom:674)`、main `(left:319,right:1219,top:412,bottom:1431)`。

## Facts

- required horizontal and vertical relationships are observed at runtime.

## Interpretation

- CSS/source string onlyではなく、computed layout predicate により AC-G03-06/07 を満たす。

## Protected contract relation

- family/stage navigation is visible only on Analysis route (Item 004)。

## Reproduction procedure

1. Analysis route を Chromium で開く。
2. computed style と bounding boxes を取得し、`row`/`column` と `stage.right < main.left` を確認する。

## Browser evidence

- Success screenshot: `test-results/browser_e2e/enh-e7-g03-independent-direct-analysis.png`。
- computed layout/bounding-box evidence は上記。console/page error: none。network/service log: API READY。
