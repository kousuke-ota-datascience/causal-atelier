# ENH-E11 G01 P00 Work Package Plan

**Document class:** Planning / Operator Artifact  
**Gate:** G01（Enhance Workflow正式Gate ID）  
**Plan status:** DRAFT / CODING_NOT_AUTHORIZED  
**Parent 06:** [Gate Coding Contract](06_Ariadne_ENH-E11_G01_implementation_instruction.md)  
**Parent 07:** [Gate Verification Contract](07_Ariadne_ENH-E11_G01_test_instruction.md)  
**P00 is not an implementation package.**

## 1. Gate acceptance claim and unresolved boundary
G01の予定範囲はstrict Local Study/ContentRef、GraphVersion/PAG、P1-M06 FCI、Linux Atomic Publication/Reader、non-effect DISCOVER CLI。これはGraph科学とOS/FS安全性という異なるacceptance authorityを含むため、単一Gateとして適切かは**未確定**。分割再審査とOwner承認・06/07 FreezeまでPxxを開始しない。

## 2. Required package map
| Package | Purpose | Depends on | Focused verification |
| --- | --- | --- | --- |
| P01 | strict Study/ContentRef、Question/Design/Method Profile、Canonical JCSとManifest Valueを定義する。 | NONE | G01-07-01/02(lexical)/04；REF01〜04、SPEC01〜04、MAN01/02 |
| P02 | private TrustedRootとimmutable multi-artifact run publicationを実FSで安全に確立する。 | P01 | G01-07-02/05/06；PUB01〜09、READ01〜07、PRIV03/04/06 |
| P03 | Graphの不確定性と版・同一性を損失なく保持する。 | P01 | G01-07-03/04/07；GRAPH01/03/04、MAN03/04 |
| P04 | FCI/PAG Adapterの技術的・科学的適格性を分離して実証する。 | P01,P03 | G01-07-08/09/10；CAP01/04/05、DD-E11-METH-P106 |
| P05 | DISCOVER-only CLIの全経路を統合し、Product v2を回帰保護する。 | P02,P03,P04 | G01-07-07/11/12；RUN01/03/04/06/07、PRIV01〜06、PUB10/MAN04〜06/READ06 |

## 3. Dependency DAG
```text
P01 ─┬─ P02 ──────────┐
     └─ P03 ─ P04 ────┤
                      └─ P05 → Candidate Assembly → Independent 07 → 999
```

## 4. Checkpoint / restart / candidate semantics
各Pxxはbounded Coding Unit。dependencyのcheckpoint・承認済み06/07と実効Sourceに不整合があればBLOCKED。中断・局所修正ではTrial番号を増やさず、checkpoint full SHA、focused test、Package status/checkpoint reportを残す。Pxx COMPLETEはGate PASSでもFixed Trial Candidateでもない。全required Pxx完了後Candidate Assembly Agentがsource連鎖とGate-wide regressionを検査しFixed SHAと20系Completion Reportを作成する。独立Agentは07をauthorityに30系Test Item/999を記録する。formal FAIL後のみ08、contract defectは09へ。
