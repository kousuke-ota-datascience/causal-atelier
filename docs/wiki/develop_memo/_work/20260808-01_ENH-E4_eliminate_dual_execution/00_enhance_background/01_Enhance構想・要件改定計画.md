# Ariadne / ENH-E4 Enhance構想・要件改定計画

## 1. 基本情報
- Project: Ariadne / causal-atelier
- Enhancement ID: ENH-E4
- Date: 2026-08-09
- Author / Planner: role-based architecture review operator

## 2. 背景
Phase 01〜05は、Product runtimeに複数のpersistent Execution lifecycle、Result/Artifactの複数ownership、typed/derivedとgeneric lineageの重複表現、legacy runtimeの境界不明瞭性を観測した（事実）。Database evidenceは、現時点のpre-productionではProduct-only clean bootstrapを実施でき、root legacy migration chainはcanonicalではないことを示す（事実）。これらを解消するtargetはPhase 06の人間承認済みADRに限定する（方針）。

## 3. 現状課題
- CausalとExploratory/Predictiveでpersistent Execution authorityが分かれている。
- state、claim、persistenceの実装境界がfamilyごとに異なる。
- persistent StageExecutionがworkflow間で非対称である。
- Result/Artifact ownershipが複数表現に分散している。
- lineageのauthorityがtyped/derivedとgenericの間で曖昧である。
- Product runtimeの隣にlegacy orchestration/runtime sourceが残る。
- migration/bootstrapのcanonical ownershipは過去の構成では曖昧だった。

## 4. エンハンス目的
one canonical Product Execution authority、全canonical workflowのpersistent StageExecution、one Result/Artifact ownership contract、relationごとに一つのlineage authority、activeなretired legacy runtime依存の排除、Product-only bootstrap、bounded transition debtを実現する。最終targetはtemporary dual-read/writeを残さない。

## 5. 対象範囲
E4-ADR-001〜012、E4-INV-001〜016、E4-REQ-001〜035、E4-CON-001〜010、およびE4-G01〜G08の文書化・実装分解。Execution、Stage、Result、Artifact、Lineage、worker、legacy boundary、shared scientific capability、migration/bootstrap、standalone CLIのcontractを対象とする。

## 6. 対象外
scientific algorithm/statistical methodology redesign、無関係なfrontend/auth/dataset redesign、無関係なperformance optimization、historical application-data migration、external legacy compatibilityの実装は対象外。shared scientific modules自体は保持する。

## 7. 要件改定方針
E4-REQ-001〜035を既存要件の意味を無関係に変更せず追加・具体化する。IDは変更しない。Current、approved Target、future implementation detailを分離し、unknownは推測で埋めない。

## 8. 設計改定方針
Phase 06 ADRとPhase 07 Gate decompositionをそのまま設計baselineとする。新しいADR、別のExecution authority、別のResult/Artifact/Lineage policyは追加しない。Phase 07のTransition Debt RegisterおよびPhase 06 typoは非semantic normalizationとして記録する。

## 9. 想定影響範囲
Product execution domain/application、persistence、repository/UoW、worker、family adapters、Result/Artifact service、lineage/closure/export、packaging/deployment、shared scientific modules、legacy boundary、CLI、testsに影響する。source code・schema・migration・configurationの変更は本Taskでは行わない。

## 10. リスク
unified aggregateの過度な一般化、migration complexity、retry/output semantics、lineage transition duplication、external legacy consumer、shared scienceの誤削除、artifact orphaning、retention assumption、CLIの第二lifecycle化がリスクである。対応は各Gateのcontract・reconciliation・compatibility decisionに割り当てる。

## 11. 完了条件
G05をProduct Execution convergence、G07をunrelated Enhance workへ進む前のsafe boundary、G08をENH-E4 final closureとする。G08 PASS、open transition debt = 0、G01〜G08のtraceability成立を最終完了条件とする。G01のPASS判定は本materializationでは行わない。
