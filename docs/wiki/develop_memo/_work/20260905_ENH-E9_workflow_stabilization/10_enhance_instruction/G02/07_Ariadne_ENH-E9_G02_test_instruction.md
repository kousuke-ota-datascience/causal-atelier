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

## Verification layers

interaction/unit: help, selection, highlight, overflow, export。API/contract regression: comparison/adoption/fix。Browser E2E: Discovery execution → candidate review/comparison → adopt/fix のcross-layer connectivityを確認する。詳細Graph correctnessはunit/contract testをprimary proofとする。

全blocking AC PASSのみG02 PASS。harness failureはproduct failureと分離してBLOCKED分類する。
