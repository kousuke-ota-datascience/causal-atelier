# Ariadne ENH-E9 G01 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `FROZEN`

## Acceptance Criteria

1. Saved Analysis Viewの内容をread-onlyで確認できる明示的なUI actionが存在する。
2. 表示操作でAnalysis View resourceの更新/複製/version作成が発生しない。
3. Active Research Contextの意味をUI help/tooltipから確認できる。
4. Current Projectはroute/project authorityを維持し、Research Context / Dataset Version / Analysis Viewの既存resource ownership/restore/invalidation semanticsがregressionしない。
5. new Analysis View schema/API/persistent resourceを導入しない。

## Verification

frontend unit/integrationでAC1–3、existing architecture/contract testsでAC4–5をblocking verificationする。Browser E2Eはtooltip presenceのprimary proofにはしない。baselineが既にACを満たす場合も、evidenceを記録して判定する。

全blocking AC PASSのみG01 PASS。environment/harness failureでproduct correctnessを判定不能ならBLOCKEDとする。
