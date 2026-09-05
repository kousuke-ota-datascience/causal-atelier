# Ariadne ENH-E9 G02 Verification Contract

**Verification contract status:** `DRAFT_NOT_FROZEN`

## Draft Acceptance Criteria

1. Residual確認済みDiscovery operationに目的/意味が明確なpresentationがある。
2. Graph Candidate listはbaselineで確認されたoverflow defectを解消し、候補identityを失わない。
3. Select All / Clearをscopeに含めた場合、selectionだけを変更しGraph adoption/fixを暗黙実行しない。
4. Graph Comparisonでcurrent comparison candidateを識別できる。
5. algorithm/relevant parameter summaryをscopeに含めた場合、persisted/current authoritative dataだけを表示する。
6. graph adoption feedbackをscopeに含めた場合、modal内でoperation resultを確認できるがadoption semantics自体は変えない。
7. Mermaid exportをscopeに含めた場合、表示/保存済みGraph authorityからsourceを導出しscientific Graphを変更しない。
8. Graph Candidate identity / GraphVersion lineage / DRAFT-FIXED / FIXED immutability / designated Outcome lineageがregressionしない。

## Test strategy

- interaction/unit tests: selection, highlight, tooltip, overflow, export
- API/contract regression: comparison/adoption/fix semantics
- Browser E2E: Discovery -> candidate review/comparison -> adopt/fix のcritical journeyをfreeze時に具体化

Environment/harness defectでproduct correctnessを判定不能な場合は`BLOCKED`。
