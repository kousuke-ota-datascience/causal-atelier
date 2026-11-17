# PREP-02 → PREP-03 | ENH-E11 Common Design Baseline

**状態:** `PREP02_COMPLETE_FOR_GATE_PLANNING / COMMON_DESIGN_BASELINE_FROZEN / PER_GATE_SCHEMA_AND_TESTS_OPEN / PREP03_STARTED / CODING_NOT_AUTHORIZED`
**基準日:** 2026-11-17 JST
**Owner意思:** 独立レビュー完了・承認（Owner申告）を工程上の承認として受け入れる。別途GitHub上の詳細なレビュー証跡をPREP-03の開始条件にしない。
**参照実装前Snapshot:** `13d6c08021b56e86373dc4912d5a6d734bcde7db` / `prototype/ariadne_mvp`（本記録と06/07の追加直前）
**区分:** この記録だけがPREP-02→PREP-03境界の最新の工程判断。過去のcombined_reviewにある`NOT_FROZEN`は作成当時の履歴であり、本書の**範囲限定のFreeze**を打ち消さない。過去の自己レビューを独立PASSと偽称しない。

## 1. 今回Freezeする共通設計契約

以下は設計・interface contractの**変更基準**として確定。実行試験の合格を意味しない。

| 区分 | Freezeする不変条件 | 設計参照 |
|---|---|---|
| F03 Local publish | TrustedLocalRoot/dirfd制約、同一FS、`renameat2(RENAME_NOREPLACE)`のみでno-clobber、durable staging→manifest→marker→parent fsync→readback、post-rename結果不定ならCOMPLETED禁止。既存の正常runを上書き・削除しない | [104](104_20261117_prep02_f03_atomic_publish_contract.md)、DD [30_62](../30_detailed_design/30_62_e11_local_execution_publication.md) |
| F04 Port | CLI Decoder→ValidatedStudy→Application→Local typed Ports→Scientific Adapters。Product Port/ScientificStatus/legacy v2とは別authority。ContentReferencePort/Capability/Identification/Estimator/Diagnostic/Policy/Publication/Readerの責務および [112](112_20261117_prep02_f03_f07_shared_port_signature_contract.md) §2のProtocol**論理署名**を共通設計基準とする | IF [23_41](../23_api_interface_design/23_41_e11_local_cli_scientific_ports.md)、DD [30_61](../30_detailed_design/30_61_e11_local_domain_ports.md) |
| F05 Privacy | 非委譲・effective UID=private root owner、root ACL/mount/namespaceはfail-closed。個票はStudy要求∧CLI flag∧**独立の事前承認authority**∧OS適格∧行・列制限を全件AND。self-authored bool/PolicyRefは認可ではない。拒否時はrow bytesを作成しない | [105](105_20261117_prep02_f05_trusted_root_privacy_contract.md)、[113](113_20261117_prep02_f05_policy_trust_anchor_candidate.md) |
| F06 Codec/Version | `e11-local-study/1`, `e11-local-graph/1`, `e11-local-effect-result/1`, `e11-local-manifest/1`, `e11-local-status/1`; marker `e11-commit/1`。E11の独立Codecの**実装規範をRFC8785 JCS**とする（PREP02技術設計選択）。`default=str`/未知v2の暗黙変換禁止。UTF8 bytes→SHA256、ContentRefはraw file bytesのSHA256。Graph内`content_hash`は当該fieldを除くJCS意味射影hash、外部ContentRefは全Graph実file bytes。Manifest self hashは禁止、Markerが実Manifest bytesを参照 | [106](106_20261117_prep02_f06_dispatch_codec_error_contract.md)、[107](107_20261117_prep02_jcs_codec_vectors.md)、[114](114_20261117_prep02_f06_schema_semantic_invariants.md) |
| F06 Error/Bundle | CLI exit `0`=技術完了（科学的負結果もあり得る）、`2`=入力Schema、`3`=path/hash/Privacy認可、`4`=実行/Backend、`5`=publish/readback。入力`SCHEMA_INVALID`と保存Bundle破損をphaseで区分。`DISCOVER/IDENTIFY`に偽のEffect Resultを生成しない（Manifest result discriminator `null`とOperation validator）。 | [112](112_20261117_prep02_f03_f07_shared_port_signature_contract.md)、[114](114_20261117_prep02_f06_schema_semantic_invariants.md) |
| F07 Science semantics | Identification/Point/Inference/Science acceptance/Technical outcomeは独立軸。AR集合は`EMPTY/ALL_REAL/DISCONNECTED/UNBOUNDED/BOUNDED`を損失なく保持。数理EMPTY≠計算FAILED。B0 complier LATE／B1加法線形IV構造係数を混同しない。 | [111](111_20261117_prep02_b0_b1_ar_science_method_contract.md)、DD [30_63](../30_detailed_design/30_63_e11_method_adapters.md) |

**Port/Schema Freezeの正確な意味:** 共通Version・型境界・Field意味・Error/Hash/Privacy/Publish不変条件を**Architecture baselineとしてFreeze**。Schemaファイルの全プロパティと41 Methodのconfigを実装済み・完全Freezeとみなさない。各Methodの詳細Config・Operation別Bundle検証・backend capabilityは**該当Gnnの06/07で閉じる**。この境界なら、未実施のRuntimeテストを前倒し強制せず、コード実装で使う共通契約を安定させられる。

## 2. 保留を該当するGateへ振り分ける

| 残りの具体化・実証 | 配分 | Gate前に必要な判断 / 実施時のテスト |
|---|---|---|
| F03 no-replace/kernel/mount/fault injection、JCS/JSON Schema実装互換、Graph/Marker readback | **G01基盤（06/07）**、G10で再統合 | G01 06にテスト実装条件を固定し、G01 07で実FS・厳格Schema・v2回帰を実測 |
| FCI/PAGのedge endpoint・latent/同値類oracle、Local Graph Context/Version、CI test | **G01（P1-M06）06/07** | 多変数Graphで独立PAG oracleを選び、単純な2 node latent識別を正解として捏造しない |
| Method別`config_schema`・Backend/API・Dataset eligibility・結果型 | **該当G01〜G09の06/07** | Method41を勝手に減らさない。未実装を成功偽装しない |
| F05 independent preauthorization署名/鍵/失効・ACL/secret/row leak | **G05個票発行前の06/07**（G01〜G04にrow exportを含めない） | Ed25519＋管理者鍵Storeは候補。実装までに現実のApproval authority/管理者運用を確定し、偽造／不適格輸出を拒否する |
| F07 HC1 ARの独立reference・全実数反転・弱IV/invalid IV・coverage | **G08（P3-M10/M11）06/07** | 具体HC1統計量は設計候補。科学的referenceと退化例を受入仕様に固定する |
| Optional dependency version/lock、license、5 Env Profile | **各Method初回Gateの06**、G10全体統合 | lock/CI/実効APIの検証。未認可ライブラリを黙ってimportしない |
| ENH-E11正本`docs/wiki/requirement_definition/`へ反映 | **全E11試験PASS後のOwner判断** | 現時点では一切移行しない |

## 3. PREP-03の着手条件と現在地

- **着手承認:** Ownerが「次進めて」と指示。PREP-02のレビュー結果はOwner承認済みとして扱い、Issue #25は完了クローズ。レビュー証跡追跡を前提にしない。
- **PREP-03 Scope:** G01〜G10の作業分割、依存/共通基盤の負担範囲、最初のG01**06実装指示書／07テスト指示書**を完成させる。各Gateの`06`はCoding Contract、`07`はIndependent Verification Contract、`999`はGate Verdict。G01〜G10番号と各Gate文書の06/07を混同しない。
- **PREP-01:** 既存RD/IF/Class全数レビューの残項目は並行管理するが、G01計画**策定そのもの**を阻害しない。PREP-04 Coding Authorization前に、実装対象へ影響する重大な不整合を閉じる。
- **現在の次の作業:** [G01 06/07作成先](../../../../10_enhance_instruction/G01/) を参照して内容・適格性/negative/old v2回帰を校正し、実装着手前にそのGate固有の条件を確定する。
- **このCommitは実装許可ではない:** `PREP03_IN_PROGRESS / G01_06_07_DRAFT / E11_CODING_NOT_AUTHORIZED / NO_RUNTIME_OR_SCIENCE_PASS`。
