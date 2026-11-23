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

### AMD-E11-G01-P01-002 — Graph-negative reason code contract defect (2026-11-23)

- **発生:** G01/P01/Trial01の3回目の実装前停止 BLOCKED_CONTRACT_AMBIGUITY。START_SHA=f33a6a614881f69cc8db4216ce295072ff87b58c、PACKAGE_CHECKPOINT_SHAなし。前回の暫定S10 SHA=707f6aaac1df5393dbf762448c41db2f1c9dbf35、185/186/187承認は確認されていた。原因は同じ技術的エラー文字列がgraph_negative_reason_codesとStatusに入っても旧P01が受理し得た、科学的理由コード判別の欠落。
- **修正種別:** CONTRACT_DEFECT。G01/P01 §6.5.1aの閉集合 SCI_NO_ADMISSIBLE_PAG 以外は科学的Graph-negative候補として拒否。G01/P04では科学的不存在のMethod別証拠なしに負結果を発行禁止、P05では真正P04 outcomeとdiagnosticsを別途照合。P04による現実の科学的Graph-negative生成が可能と実証したわけではない。汎用公開Schema/lock/コードは未変更。
- **影響:** G01/P01・P04・P05の06、G01 07、stock 23_42/30_62、09新規契約変更、既存Ledger・運用ハンドオフ。P02/P03/P00、G02〜G10、旧Product v2・科学的受入条件に変更なし。
- **証跡:** 09_ENH-E11_G01_AMD-E11-G01-P01-002_Gate_Contract_Amendment.md および combined_review/189_20261123_g01_p01_negative_reason_contract_defect_impact.md。Author作業だけでは独立S09や実テストPASSを証明しない。
- **現時点:** AMENDMENT_PROPOSED / NEW_OWNER_09_RE_S10_RE_S11_PENDING。従前185/186/187は旧凍結契約の承認履歴として保存するが、今回の改訂WHATへのCoding許可として流用禁止。旧Trial01の3件のBLOCKED停止記録は保持し、正式FAIL/08がなければTrial増番しない。


### AMD-E11-G01-P01-002 — Owner正式09承認・改訂G01-S10再Freeze（2026-11-23追記）

- **Owner承認:** `DEC-G01-P01-REBASELINE-02=APPROVED`。新しい09 `AMD-E11-G01-P01-002` は `combined_review/190_20261123_g01_p01_negative_reason_09_owner_approved.md` で正式承認し、新しい暫定S10は `combined_review/191_20261123_g01_p01_negative_reason_revised_provisional_s10_refreeze.md` で**Owner再Freeze済み**。上記の申請時 `PENDING` は履歴として保存し、この追記が現在の09/S10承認状態のauthorityとなる。
- **固定完全Git SHA:** `bcc1d797e1406e8816d12b725eeace07a181c702`。Frozen `uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、公開Schema不変。190/191、本追記、後続の申請DocketはFreeze後の運用管理記録であり新しい規範WHATではない。
- **残る唯一のHuman Coding Entry判断:** `DEC-G01-P01-S11-REAUTH-02` — 改訂後S10に対する**別個のG01-S11限定Coding Authorization**。旧Owner承認187は前版契約の履歴として残すが新WHATには適用不可。新S11判断資料：`combined_review/192_20261123_g01_p01_negative_reason_limited_s11_reauthorization_docket.md`。
- **現在状態:** `AMD-002=APPROVED` / `G01-S10=RE_FROZEN` / `G01-S11=NOT_AUTHORIZED_FOR_AMD-002` / `G01-P01-Trial01=BLOCKED_CODING_AUTHORIZATION` until new Owner S11 and actual runtime preflight. G01_999未達、G02以降未許可。三件の停止記録は維持。

### AMD-E11-G01-P01-002 — 限定G01-S11の新規Owner承認（2026-11-23追記）

- **Owner判断:** `DEC-G01-P01-S11-REAUTH-02=APPROVED`。Ownerは「改訂後の暫定G01-S10凍結SHA `bcc1d797e1406e8816d12b725eeace07a181c702` を対象に、G01/P01〜P05の限定Coding Authorizationを発行せよ」と明示。正式09記録190→改訂S10記録191→**別個の新S11記録193**の順序で承認。先行行にある`S11_NOT_AUTHORIZED`は記載時点の履歴であり、現在状態は本追記を優先。
- **新Authorizations:** `combined_review/193_20261123_g01_p01_negative_reason_limited_s11_owner_authorization.md`; 現行再開指示は `combined_review/194_20261123_g01_p01_trial01_restart_handoff_amd002.md`。旧187および188は以前の凍結WHATの履歴として保持。
- **凍結基準:** 全長S10 SHA `bcc1d797e1406e8816d12b725eeace07a181c702`、uv.lock Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、branch `feature/ariadne_mvp_e11`、G01/P01〜P05のみ。GitHub上の事後承認管理記録は凍結後の変更として許容し、Coding Agentは実環境で全差分・lock・clean tree/Trial状態を必ず再Preflight。
- **最新状態:** `AMD-002=OWNER_APPROVED`、`S10=RE_FROZEN`、`S11=AUTHORIZED_LIMITED_G01`、`P01/Trial01=AUTHORIZED_TO_START_AFTER_RUNTIME_PREFLIGHT`。コーディング・focused verification・チェックポイント実績は未観測。G01_999の独立S09/B02/B03/B04/B05/T2/T3/07およびProduct v2回帰は未免除、他Gate未承認。

### AMD-E11-G01-P02-001 — P02 PrivacyDecision authority and resource binding (2026-11-23)

- **停止:** G01/P02 Trial01 `BLOCKED_CONTRACT_AMBIGUITY`, START_SHA `4248ca24204ed8ede27527191b1a53d9ced1ff5a`、P02 checkpointなし。Facade sealのPrivacyDecisionとConcrete validate(manifest)の判断権威、run/TrustedRoot/UID/成果物拘束が未定義だった。
- **既存依存:** P01 PACKAGE_READY checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`をGitHub status reportで確認。P01 WHAT/sourceを変更せず保持。
- **補完:** Concrete `validate(manifest,*,privacy)`へFacadeがDecisionを渡し、P02 Publisherがstage済みStudyの厳密hash、実際のRoot FD/EUID、Artifact inventoryと注入Policyを再評価して一致検証。不適切なDecisionやrow出力はrename前拒否。公開Port/Schema/旧Product/lock不変更。
- **変更管理:** 新09 `AMD-E11-G01-P02-001`、影響レビュー`combined_review/195_20261123_g01_p02_privacy_decision_binding_contract_impact.md`。
- **承認境界:** `PROPOSED / OWNER_09_RE_S10_SEPARATE_RE_S11_PENDING`。旧S10 `bcc1d797e1406e8816d12b725eeace07a181c702` とS11記録193は旧P02契約への歴史的承認。独立S09/B02/B03/B04/B05/T2/T3/07/999義務不変更。

### AMD-E11-G01-P02-001 — RD/LDD/BD/IF/DD/06/07階層整合（2026-11-23追加）

- **Owner追加指示:** 要件定義・基本設計・論理データ定義・API仕様・詳細設計・06コーディング指示・07テスト指示を一貫して修正。
- **正本候補の改訂:** RD `10_21/10_22/10_91`、LDD `21_23/21_40`、BD `22_09/22_12`、IF `23_41/23_42`、DD `30_62`、G01 P02/P05 `06`、G01 `07`。Author audit `combined_review/196_20261123_g01_p02_rd_ldd_bd_if_dd_06_07_parity_audit.md`。
- **不変:** P01実装・Checkpoint、P03/P04 WHAT、Status/Manifest public Schema、旧Product v2、G01個票禁止、lock blob、独立科学・FS受入要件。
- **依然として未許可:** AMD-001およびAMD-002時代のOwner S10/S11を今回の実装変更へ流用しない。今回の全階層の改訂後full SHAを対象に、新09→新暫定G01-S10→別個のS11のOwner明示承認が必要。

### P01 実装後の例外的上位文書逆方向整合（2026-11-23）

- **Owner指示:** G01/P01は既に実装が完了しているため、**今回限り**G01/P01の`06_G01_P01_local_contract_codec.md`と恒久設計`30_60/30_62`を技術的基準に、要件定義・論理データ・基本設計・IFを後追いで整合化する。通常のRD→設計→実装のAuthority方向を一般に逆転させない。
- **修正:** RD `10_17/10_20/10_91`、LDD `21_25/21_40`、BD `22_06/22_09/22_15`、IF `23_41/23_42`。P01 `06`/G01 `07`/DD `30_60/30_62`/コード・テスト自体を変更せず、MUST/ACを緩和していない。
- **監査:** `combined_review/197_20261123_g01_p01_post_implementation_reverse_trace_alignment.md`。P01 PACKAGE_READY checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`を保持。developerテスト76件の報告は独立G01_999 PASSでない。
- **G01/P02の再承認境界:** `AMD-E11-G01-P02-001`の09正式承認、新暫定S10 Freezeと別S11は依然必要。後追いP01整合化を含む**最新full commit SHA**をOwner判断対象に用いること。

### AMD-E11-G01-P02-001 — Owner正式09承認・改訂S10再Freeze (2026-11-23)

- **Owner decision:** `DEC-G01-P02-REBASELINE-01=APPROVED`; Owner explicitly authorized `AMD-E11-G01-P02-001` formal 09 and revised provisional G01-S10 at the **exact full Git SHA** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`.
- **Sequential records:** `combined_review/198_20261123_g01_p02_formal_09_owner_approved.md` (formal 09 approval, commit `07e2343816e7f95c9e966e5483752d63fbfea37d`); `combined_review/199_20261123_g01_p02_revised_provisional_s10_owner_refreeze.md` (distinct reFreeze, commit `4a7ff7b39e49c5501157bfcc1124fdaae1e9d94a`). Earlier `PROPOSED` / `OWNER_PENDING` lines are historical and the new Owner records set current authority.
- **Preserved predecessor:** G01/P01 Trial01 `PACKAGE_READY` checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` remains intact. No actual source/tests/pyproject/uv.lock changed after the P01 checkpoint in the reFreeze baseline. Frozen `uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`.
- **New S11 remains separate:** `DEC-G01-P02-S11-REAUTH-01 = PENDING` (docket `combined_review/200_20261123_g01_p02_limited_s11_reauthorization_docket.md`). Old S11 record 193 remains valid historical authorization for the earlier P02 contract **but not revised WHAT**. P02 Trial01 cannot implement until new S11 Owner decision; actual runtime preflight still mandatory.
- **Unwaived:** G01 independent science/FS/T2/T3/07/999 and Product v2 regression unaffected; other Gates not authorized.

### Owner指定：Gate 06/07は5階層Stock文書との整合後にのみ改訂（2026-11-23）

- **正規相対path基点:** `docs/wiki/develop_memo/_work/20261024_ENH-E11_causal_lifecycle_cli_expansion/`。対象は`00_enhance_background/Revised_requirements_definition_documents/{10_requirements_definition,21_logical_data_design,22_product_basic_design,23_api_interface_design,30_detailed_design}`、および`10_enhance_instruction/{GATE_ID}/06_*.md`と`07_*.md`。
- **照合記録:** `combined_review/202_20261123_g01_06_07_five_layer_contract_concordance_protocol.md`。G01 P01–P05と07をRD/LDD/BD/IF/DDに責務トレース。現行G01/P01とP02は197/195/196で修正済み。未検出の新契約不整合は捏造しない。
- **Freeze維持:** `6df4b94de72a6ec8619f315e55ba7821e1eb157c`の06/07自体はこの管理追記では改変していない。新たな06/07正規契約改訂は正式09→新S10→別S11を要求。P01逆方向整合化は既承認の一回限り例外。現時点のS11未承認状態を保持。

### G01/P02 別個限定 S11 Owner 承認：DEC-G01-P02-S11-REAUTH-01（2026-11-23）

- **明示Owner承認:** 「`DEC-G01-P02-S11-REAUTH-01` を承認する」。198正式09承認→199暫定S10再Freeze→**201新限定S11承認**の順を維持。
- **権威記録:** `combined_review/201_20261123_g01_p02_revised_limited_s11_owner_authorization.md`。凍結WHAT完全Git SHA `6df4b94de72a6ec8619f315e55ba7821e1eb157c`。参照200は承認前docket、202は5階層整合性監査。
- **再開:** `GATE_ID=G01 PACKAGE_ID=P02 TRIAL_NO=01`。再開ハンドオフ `combined_review/203_20261123_g01_p02_trial01_restart_handoff_after_s11.md`。P01 PACKAGE_READY checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167` を保全。実行Agentの環境preflightは未実施、実FS・G01独立受入はPASS未宣言。
- **条件:** 凍結WHATからの差分は正式承認/管理文書のみ、正本05階層とG01 06/07の意味整合を維持。新たな06/07改訂は別途09/S10/S11、P02本体のコード変更だけが許可範囲。旧193は新P02契約への権限ではない。

### AMD-E11-G01-P02-002 — PrivacyDecision同値再構築の受理判定を確定（2026-11-23）

- **原因:** G01/P02 Trial01再実行`START_SHA=06726b522faf939c8ea34193d1861bd786092776`が`BLOCKED_CONTRACT_AMBIGUITY`。正規発行されたDecisionと全フィールド同値のDecisionを別生成した場合、元の「偽造拒否」が発行証明まで要求するか不明確。P02コード/Checkpointなし、P01開発者テスト76件PASSはAgent報告。
- **修正:** 出所認証ではなくPublisherに注入された信頼済みstateless Policyの実Study/root/UID/inventory上での独立再計算と**構造的全フィールド値一致**を最終権威とする。同値再構築は独立再評価が許可なら**受理**、「forged」の負例は値不一致・拒否Policy・検証迂回のみ。署名/Issuer/nonceは新設しない。
- **変更範囲:** RD `10_22/10_91`; LDD `21_23/21_40`; BD `22_09/22_12`; IF `23_41/23_42`; DD `30_62`; G01 P02/P05 `06`; G01 `07`。実装コード、P01/P03/P04、public JSON、Product v2、独立G01_999は不変。
- **権威:** 提案09 `10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-002_Gate_Contract_Amendment.md`; Author監査 `combined_review/204_20261123_g01_p02_privacy_decision_value_equivalence_impact.md`。元S10凍結SHA `6df4b94de72a6ec8619f315e55ba7821e1eb157c`および既承認198/199/201は歴史記録として維持。
- **Status:** `AUTHOR_CONTRACT_AMENDED / FORMAL_09_OWNER_PENDING / NEW_S10_PENDING / SEPARATE_S11_PENDING`。現行P02の実装を再開しない。P01 Checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`を保持。正式Gate FAILなしにつきTrial01継続。

### AMD-E11-G01-P02-002 — 正式09 Owner承認（2026-11-23）

- **Owner明示承認:** 「AMD-E11-G01-P02-002を承認する」。承認の正確な範囲は**正式09のみ**。記録`combined_review/205_20261123_g01_p02_002_formal_09_owner_approved.md`。
- **承認対象契約SHA:** `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492`。従前のG01-S10 `6df4b94de72a6ec8619f315e55ba7821e1eb157c` は今回の契約変更を含まず、別の新S10再Freeze・新S11が必要。
- **決定待ち:** 新S10判断資料`combined_review/206_20261123_g01_p02_002_revised_provisional_s10_decision_docket.md`。P01 PACKAGE_READY checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`を保全。P02 Trial01は実装許可の再発行まで停止。
- **不変:** NFR-031、G01 07物理/科学的受入、公開JSON/Port、Product v2、個票禁止、`uv.lock`およびP01コード/テスト。判断発行済みをS10/S11 PASSとして扱わない。

### AMD-E11-G01-P02-002 — 新暫定G01-S10 Owner再Freeze（2026-11-23）

- **Owner決定:** `DEC-G01-P02-002-S10-REFREEZE-01=APPROVED`。正式09は205で承認済み、新しい暫定G01-S10を完全Git SHA `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` に再Freeze。
- **新S10権威記録:** `combined_review/207_20261123_g01_p02_002_revised_provisional_s10_owner_refreeze.md`。旧S10 `6df4b94de72a6ec8619f315e55ba7821e1eb157c` と旧S11 201は改訂前WHATの歴史記録。
- **次の独立判断:** `DEC-G01-P02-002-S11-REAUTH-01` は**未承認**。判断資料 `combined_review/208_20261123_g01_p02_002_limited_s11_reauth_docket.md`。S10記録のみではG01/P02のCoding再開不可。
- **保存条件:** P01 PACKAGE_READY `9bff61f0eae25236f95f31f2cd3e7c81291f0167`、`uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、G01 07・999の独立受入条件を維持。P02実装・実FSテスト未実施。

### AMD-E11-G01-P02-002 — 新限定G01-S11 Owner承認（2026-11-23）

- **明示Owner決定:** `DEC-G01-P02-002-S11-REAUTH-01=APPROVED`。「AMD-E11-G01-P02-002に基づく暫定G01-S10凍結SHA `0e36d5d8ce5a4fb9880c4ecff07f4e2256cde492` を対象に、G01/P01〜P05の限定Coding Authorizationを再発行せよ。次の実行はG01/P02/Trial01」。
- **承認順序:** 205（正式09）→207（暫定G01-S10再Freeze）→**209（新S11限定Coding Authorization）**。旧S11 201は旧WHATのみ。
- **Agent handoff:** `combined_review/210_20261123_g01_p02_002_trial01_restart_handoff_after_s11.md`。依存P01 checkpoint `9bff61f0eae25236f95f31f2cd3e7c81291f0167`、`uv.lock` Git blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`を維持。P02の再実装開始は現地Preflight成功後。
- **維持する未完了:** Linux実FS/P02 tests、P03/P04/P05、独立科学/S09/B02–B05/T2/T3/G01 07/999、Product v2回帰。承認記録は独立テストPASSでない。

### AMD-E11-G01-P02-003 — G01 Graph-negative diagnosticsの内部型・Status照合（2026-11-23）

- Coding Agent STOP: BLOCKED_CONTRACT_AMBIGUITY, START_SHA 86d73c501f83eed2ce79b1fa949d6aacffc3f4a1, no P02 code/checkpoint.
- Cause: P02 and 07 demand a typed diagnostics.json but its G01/P1-M06 DISCOVER schema and run/reason join were unspecified. P1-M12–20 internal diagnostic schema is not applicable.
- Minimal correction: internal exact four-field run_id/operation/method_id/reason_codes profile; required SCI_NO_ADMISSIBLE_PAG exact join to Status and Manifest; Publisher/Reader strict bytes plus semantic verification; no fake scientific negative.
- Changed: RD 10_17/10_91, LDD 21_40, BD 22_09/22_15, IF 23_42/internal schema, DD 30_62, G01 P02/P05 06, G01 07. No src/tests/P01/Product v2/lock/independent AC changes.
- Formal 09 candidate: 10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P02-003_Gate_Contract_Amendment.md ; audit 211_20261123_g01_p02_negative_diagnostics_contract_impact.md.
- Status: AUTHOR_PREPARED / OWNER_FORMAL_09_PENDING / NEW_S10_PENDING / SEPARATE_S11_PENDING. Preserve P01 9bff61f0eae25236f95f31f2cd3e7c81291f0167 and Trial01.

## 3. 今後の記録必須項目

Amendment ID、状態、発生要因・証跡、影響Gate/Trial、変更種別（`REQUIREMENT_CHANGE / DESIGN_CHANGE / CONTRACT_DEFECT / OTHER`）、適用するGate 09、オーナー承認、変更前後の正規意味、影響06/07/Pxx/Rxx、再基準SHA、旧テスト証跡の保存状況。

**テストをPASSさせるためだけに科学的受入条件を緩めない。**
