# Ariadne ENH-E9 G02 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `FROZEN`

## Acceptance Criteria

1. Discovery execution領域のpurpose/titleとObjective/Rationale helpをUIで確認できる。
2. Graph Candidate listはpage-level overflow defectを発生させずcandidate identityを保持する。
3. Select All / Clearはselectionだけを変更しadoption/fixを実行しない。
4. Graph Comparisonでcurrent comparison candidateを識別できる。
5. algorithm/relevant parameter summaryはpersisted/current authoritative dataだけを表示する。
6. graph adoption resultを操作modal内で確認でき、adoption semanticsは変わらない。
7. Mermaid exportはauthoritative Graphからdeterministically生成され、export操作はGraphをmutationしない。
8. Graph Candidate identity / GraphVersion lineage / DRAFT-FIXED semantics / FIXED immutability / designated Outcome lineageがregressionしない。

## Verification layers and mandatory execution order

Independent Verificationは次の順序で行う。Browser E2Eを先行実行しない。

1. static / syntax checks
2. interaction / unit tests: help, selection, highlight, overflow, export
3. API / contract / regression tests: comparison, adoption, fix, identity, lineage, DRAFT/FIXED semantics, FIXED immutability, designated Outcome lineage
4. 上記non-browser blocking verification結果を評価する
5. **Browser E2Eを最後のverification itemとしてのみ実行する**: Discovery execution → candidate review/comparison → adopt/fix のcross-layer connectivityを確認する

Browser E2Eは詳細Graph correctnessや個別scientific semanticsのprimary proofに使用しない。それらはunit/contract/regression testをprimary proofとする。

Browser E2E実行前にnon-browser blocking testがproduct defectとしてFAILした場合、先にそのFAILを記録し、原因切り分けのためにBrowser E2Eを先行・代替実行しない。Browser E2E harness/environment failureはproduct failureと分離してBLOCKED分類する。

全blocking AC PASSのみG02 PASS。
