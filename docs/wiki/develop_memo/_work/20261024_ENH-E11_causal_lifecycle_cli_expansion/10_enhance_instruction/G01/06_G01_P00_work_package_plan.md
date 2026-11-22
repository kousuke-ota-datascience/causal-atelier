# ENH-E11 G01 P00 Work Package Plan

**DEC-G01-EXEC-01（Owner 2026-11-23採用・G01のみの実施順序変更）:** `combined_review/177_20261123_dec_g01_exec01_owner_adopted_evidence_rephasing.md`がG01の従前S09→S10→S11依存を部分的に上書きする。利用不能なPython3.12実測B02/B04、独立S09/B05科学審査は**Coding Entryの必要条件から外し、G01_999 PASSまでの必須受入条件へ移す**。事前Author契約整合と例外Ledgerを材料に、Ownerの**別個の暫定G01-S10 Freeze**、その後Ownerの**別個の限定G01-S11 Coding Authorization**を認める。どちらも現在**未承認**。限定許可はG01/P01–P05の実装・開発者テストのみ。実Python3.12 Schema/FCI、独立MAG/PAG/BK、実FS/Reader、T2/T3、独立07/999、Product v2回帰の要求・合格基準は維持。未検証をPASS扱いせず、non-null BKはFCI呼出前exit4 fail-closed、科学的真値や閾値の自己創作禁止。G01_999がPASSするまで下流Gate依存は解除しない。

**DEC-PREPCODE-01=B（Owner 2026-11-22採用・Gate別Control Plane）:** G01は共通E11 v1のSchema/JCS/ContentRef/Graph、Port/Privacy、Publisher/Reader、安全なFS、既存Product v2互換、P1-M06 FCI専用Config/Question/DesignおよびENV-BASE・独立MAG/PAG科学Oracleを対象に、**G01+共通契約の独立S09監査→Owner G01-S10 Freeze→Owner G01-S11 Coding Authorization**をこの順で取得する。本書の存在・Author静的改訂・全402資料のSHA索引・他GateのS09/S10/S11はG01のCoding許可を意味しない。G02以降40 Method/他Optional Backendの未確定はG01固有の停止条件にしないが、共通依存の不整合は止める。G01完成後もreal FS/FCI Adapter/T2/T3/保護Product回帰は独立07/999の実測必須であり、先行してPASSとしない。現時点は**G01 S09 NOT_RUN / S10 NOT_FROZEN / S11 NOT_AUTHORIZED**。

**Document class:** Planning / Operator Artifact  
**Gate:** G01（Enhance Workflow正式Gate ID）  
**Plan status:** DRAFT / CODING_NOT_AUTHORIZED  
**Parent 06:** [Gate Coding Contract](06_Ariadne_ENH-E11_G01_implementation_instruction.md)  
**Parent 07:** [Gate Verification Contract](07_Ariadne_ENH-E11_G01_test_instruction.md)  
**P00 is not an implementation package.**

## 1. Gate acceptance claim and unresolved boundary
**PREPARATION-03 技術評価：G01単一Gateを維持（Owner承認待ち）。** 対象はstrict Local Study/ContentRef、PAG/GraphEvidence、P1-M06 FCI、Linux Atomic Publication/Reader、non-effect DISCOVER CLIが一体となったrun-scoped垂直スライス。科学的Graphの正当性とFile Publicationの安全性は別個の必須受入軸として、それぞれP04/07-08〜10とP02/07-02/05/06の独立証跡を要求し、P05/07-07/11/12で共通Fixed Candidate SHAの統合動作を証明する。部分完成をGate PASSにしない。この構成で依存循環はなく、G01を分割する技術的必要性はない。Ownerの境界承認・06/07 Freeze・Coding AuthorizationまではPxx着手禁止。

## 2. Required package map
| Package | Purpose | Depends on | Focused verification |
| --- | --- | --- | --- |
| P01 | strict Study/ContentRef、Question/Design/Method Profile、Canonical JCSとManifest Valueを定義する。 | NONE | G01-07-01/02(lexical)/04；REF01/04（pure lexical）、SPEC01〜04、MAN01〜06（pure DTO）。REF02/03物理FS検証はP02 |
| P02 | private TrustedRootとimmutable multi-artifact run publicationを実FSで安全に確立する。 | P01 | G01-07-02/05/06；REF02/03（actual FD/FS）、PUB01〜09、READ01〜07、PRIV03/04/06 |
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

## 5. PREPARATION-04 Coding Authorizationの判定条件

- **技術判定（Owner決裁ではない）：G01をP01→P02/P03→P04→P05とした現行Work Package構成で実装可能。** Graph/FCIの科学的受入とOS/FS Publicationの受入は独立実証するが、G01_999はAND条件で判断する。
- **現時点のCoding AuthorizationはNOT_AUTHORIZEDを維持。** 独立設計監査・06/07追随のGitHub反映はCoding Entry許可ではない。OwnerによるGate境界・06/07 Coding/Verification Contractの承認とFreeze、実装基準full SHA、実行環境/依存の確認を揃えた後にPREPARATION-04で明示的に許可する。
- **Coding EntryとScience Gate PASSは異なる。** T2 Pilot/T3本検証、実Filesystem crash試験、実FCI API適合、独立PAG Oracleの科学的結果はCoding Entry前の実施完了条件ではなく、G01の独立07/999で必要な証拠である。Coding Entry時にはテスト計画・Oracle構築方法・FAIL/BLOCKED/INCONCLUSIVE条件を固定し、科学的PASSを前倒し宣言しない。
- **Scope除外:** G02以降のIDENTIFY/ESTIMATE/REFUTE/SENSITIVITY/DIAGNOSEのMethod固有Schema/Scienceは、G01が全41件の完成を主張しない限りG01の着手阻害ではない。未登録Method Profileはfail-closed。


## S02-01/02/06/07 対象Gateの確定契約（Owner採用・未実装）

G01は`P1-M06`のDISCOVERのみで、個票の出力を常に拒否する。Valid Studyの`privacy.row_export_requested=false`（省略の扱いはstrict Study schemaのdefault/requiredに従う）を要求し、trueはPrivacy exit3。廃止された追加CLI row許可flagを登録せず、渡された場合は不明オプションとしてconfig exit2。Contextは`LocalRunContext(root:TrustedLocalRoot,principal:LocalPrincipal)`、Privacy Portは`authorize(*,study,root,principal,output_shape)`であり、署名Policy/Study policy_refは存在しない。G05のみStudy単独opt-in（true）とOS/Method制約の全件ANDを満たす個票中間出力を担当する。

新Local Graphのimmutable identityは内容hash、parent/source科学証拠とContentRef。Product GraphVersion DBへlookup/write/edit/FIXせず、現行E11 Graph wireの`version_id`と`parent_version_id`はどちらもnullとし、non-nullは未対応importとして拒否する。既存ProductのGraphVersionServiceや旧v2は無変更。

OS/FS受入は有界な不変条件別の正負例（owner EUID・0700/0600・dirfd/O_NOFOLLOW・same FS・symlink/race・rename前後・post-rename indeterminate・Marker/Reader/hash）に限定する。冗長なfault-permutation全順列、statx mount-ID/namespace証明、ACL/xattr digest/コンテナ推測、電源断耐久保証は追加しない。JCS RFC8785 golden bytes、no-clobber、公開後整合性、独立PAG Science Oracleは維持する。Coding Agentが未承認の広いProof強化を推測で復活させない。
