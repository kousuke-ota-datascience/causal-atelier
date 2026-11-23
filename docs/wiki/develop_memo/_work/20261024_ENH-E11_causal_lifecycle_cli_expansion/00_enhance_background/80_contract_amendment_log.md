# ENH-E11 — 契約変更履歴（追記専用）

**文書区分:** 計画・証跡・ガバナンス資料  
**状態:** G01/P01凍結後契約欠陥の改訂案あり／Owner A案採用、改訂後のS10/S11再承認待ち

## 1. 目的

正式承認後、またはGate 06/07のfreeze後に発生した契約変更を追記する。従前のBLOCKED/FAILと検証証拠を保持し、変更理由、影響するFR/NFR/AR・設計・Gate、変更前後の意味、SHA、再基準化、次Trialを記録する。

## 2. 現在の記録

**初回凍結後契約変更より前は該当なし。** 2026年9月のNotion `HANDOFF_DRAFT`と2026年10月24日のオーナー方針におけるPhase 1〜3 CLI-firstへの対象拡大は、**承認前の計画変更**である。凍結済みGate契約の修正として遡及記録しない。事前調査`00_01_foundation_gap_reconciliation.md`、構想`01`、承認記録`02`、要件改定案`03`、三資料照合`00_03`、Issue #13で扱う。

### AMD-E11-G01-P01-001 — `CONTRACT_DEFECT`（2026-11-23）

- **発端:** G01/P01 Trial01 Coding Agentが`BLOCKED_CONTRACT_AMBIGUITY`で実装前停止。`from_run_evidence(evidence:ValidatedRunEvidence)`の必須構造とArtifact別upstream-ref joinが06/P01単独で未確定。観測開始SHA `6ec2f59fa71b85aeff46daf0e6740b04281e8436`、Package checkpointなし、変更なし。停止報告はユーザー提供の外部Agent記録で、独立検証済みTest報告ではない。
- **Owner方針:** 同日の会話で **A案（既存責務を維持した最小契約補完）採用**、続けて「早急に…ドキュメント修正」を指示。これは修正の承認であり、**変更後のS10 Freeze/S11 Coding Authorizationの再発行ではない**。
- **変更前Freeze / Authorization:** S10 `a05fd072cbb82a7c6e43f45e7208e078f0784a2b`／`uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、Owner記録179/180。両記録を不変の履歴として保持。
- **変更後の設計意味:** P01はtyped Study/Status/Runtime/Stochastic/Artifact/Graph-or-negative evidenceをpureに投影し、各Refの値・Inventory・Method/Statusの照合を拒否条件まで定義。P02は実bytes/hash/FS/Reader、P03はGraph意味、P05は実行・Inputとcross-file validation。出力Graph Refと入力Graph nullを区別。公開E11 JSON version/schemaへの新フィールド追加なし、P1-M06 Science/BK/Privacy/旧v2/07/999要件に変更なし。
- **影響範囲:** G01/P01 §3,§6.5,§7,§10、stock 30_62 §4、IF 23_42 §2、G01/P02・P05 handoff、G01 07検証の明確化。G01/P03・P04本体、G02以降Method契約、code/uv.lockは変更不要。FR-201/202/203・NFR-029/030/032・AR-040の**既存受入意味は不変**。
- **変更管理記録:** `combined_review/183_20261123_g01_p01_manifest_evidence_contract_defect_amendment.md`。本更新を反映するGit commit full SHAは当該commit作成後に操作記録から取得し、正式なOwner再Freeze記録に固定する（自己参照SHAをこのファイル内に捏造しない）。
- **再開条件:** 改訂文書のcross-contract監査→契約変更として09/影響評価→Owner新暫定G01-S10 Freeze→**別個**の限定G01-S11再Authorization→実行環境の最新SHA/lock/クリーンtree再Preflight。Trial01の停止記録を保存し、formal FAILではないためTrialを自動増番しない。**現時点で実装再開許可は未成立**。

### AMD-E11-G01-P01-001 — 09 formal amendment and Owner decision docket

- 2026-11-23：上記改訂に対して正式なDerived Contract `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P01-001_Gate_Contract_Amendment.md`を作成。Authorによる影響確認・再基準候補SHA・AC非緩和・Trial01再実行条件は`combined_review/184_20261123_g01_p01_contract_defect_author_review_and_s10_refreeze_docket.md`に記録する。
- **申請状態:** `PROPOSED / AUTHOR_IMPACT_REVIEW_RECORDED / OWNER_09_AND_RE_FREEZE_PENDING`。Owner A案採用は改訂方針承認であり、具体改訂契約・S10/S11の再承認とは区別。改訂後S10と別個のS11が成立するまで実装開始禁止。
- **厳守:** 旧179/180、旧Trial01の二件のBLOCKED報告を改ざんしない。今後のOwner承認・再凍結full SHAは実際に発行された場合のみ追記・別文書化する。独立S09/科学/FSテストは未実施でありG01_999は依然BLOCKED。

### AMD-E11-G01-P01-001 — Owner正式承認・改訂暫定G01-S10再Freeze（2026-11-23追記）

- **事後の明示承認は上記申請状態を置換する:** Ownerが`DEC-G01-P01-REBASELINE-01`を承認し、正式09契約変更は`combined_review/185_20261123_g01_p01_amendment_09_owner_approved.md`で**APPROVED**、新たな暫定G01-S10は`combined_review/186_20261123_g01_p01_revised_provisional_s10_owner_refreeze.md`で**APPROVED / RE_FROZEN**と記録した。上記の`PENDING`は申請当時の履歴であり現在の09/S10状態ではない。
- **再Freezeの固定full SHA:** `707f6aaac1df5393dbf762448c41db2f1c9dbf35`。`uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`は不変。185/186および本Ledger追記はFreeze後の管理・承認記録であり、凍結した科学・技術WHATを変更しない。
- **唯一の残るCoding EntryのOwner判断:** 新しい改訂S10と同SHAに対する**別個のG01-S11限定Coding Authorization**。S11未承認の間はG01/P01 Trial01実装再開不可。旧179/180は旧Freezeの履歴のみ。G01_999独立S09/B02/B03/B04/B05/T2/T3/07義務は維持。

### AMD-E11-G01-P01-001 — 改訂後限定S11 Owner再承認（2026-11-23追記）

- **Owner決定:** `DEC-G01-P01-S11-REAUTH-01=APPROVED`。09正式承認185 → 新暫定S10再Freeze186 → **別個の新限定S11再承認187** の順序を満たした。承認記録は`combined_review/187_20261123_g01_p01_revised_limited_s11_owner_coding_authorization.md`。
- **固定契約:** 新S10の完全Git SHA `707f6aaac1df5393dbf762448c41db2f1c9dbf35`、lock Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`。旧179/180は歴史的承認。現在の実行ハンドオフは`combined_review/188_20261123_g01_p01_trial01_coding_restart_handoff.md`、旧181には最新参照を追記した。
- **再開状態:** `G01/P01/Trial01=AUTHORIZED_TO_RESTART_SUBJECT_TO_RUNTIME_PREFLIGHT`。対象はG01/P01–P05の実装・開発者テストのみ。Coding Agentの実装、実Linux環境でのpreflight、focused verification、checkpoint、pushは**この承認記録では未観測**。二度のBLOCKED停止記録を保存し、formal FAIL/08がない限りTrial自動増番は行わない。
- **受入義務の不変更:** 独立S09/B02/B03/B04/B05/T2/T3/07/999及びProduct v2回帰は引き続き必要。G01_999=BLOCKED、G02–G10未許可。過去のPENDING行は当時の履歴であり、最新の状態は本追記を優先する。

## 3. 今後の記録必須項目

Amendment ID、状態、発生要因・証跡、影響Gate/Trial、変更種別（`REQUIREMENT_CHANGE / DESIGN_CHANGE / CONTRACT_DEFECT / OTHER`）、適用するGate 09、オーナー承認、変更前後の正規意味、影響06/07/Pxx/Rxx、再基準SHA、旧テスト証跡の保存状況。

**テストをPASSさせるためだけに科学的受入条件を緩めない。**
