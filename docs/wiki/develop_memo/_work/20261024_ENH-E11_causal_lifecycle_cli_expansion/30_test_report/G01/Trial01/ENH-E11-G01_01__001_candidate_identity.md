# ENH-E11 G01 Trial 01 Test Item 001 — Candidate identity audit

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `001_candidate_identity` |
| 正式判定 | **PASS** |
| 実行層 | META |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

同期後の主作業ツリーと別 checkout の実測 HEAD を照合。承認・契約同一性、チェックポイント、実行対象を確認。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| Candidate identity | AC-06 | Gate 07 §0、§6 と Owner 記録270 | PASS |

## 観測と根拠

`git pull --ff-only causal-atelier feature/ariadne_mvp_e11` は exit 0。開始前 `git status --porcelain` は空でブランチは `feature/ariadne_mvp_e11`。同期後の HEAD、FETCH_HEAD、upstream 追跡 ref は `249bc48433e1472442fdbedfb9b848896e58d648`。前回開始時 `d0fc571c48d2dc3bf02e70ea4786d10db5394aa3` との差は Owner 記録270の追加1件。固定候補の存在、Completion Report の `READY_FOR_TEST` と full SHA を確認した。 [Owner 記録270](../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/270_20261124_g01_trial01_independent_freeze_regression_scope_owner_decision.md) · [Completion Report](../../../20_implementation_reports/G01/Trial01/E11-G01_01__implementation_completion.md)

- 有効 S10 `307404e01c43bb83a286986f8f6d124e53032509` は記録266、S11 `7c15920ab46c46b3a084432736c2c32fbb087e92` は記録267。P05 AMD-001–004 の正式09・再凍結・限定再認可は順に記録250–252、255–257、260–262、265–267で照合。S10→S11 は記録266・267のみ。限定 S11→固定候補は許可された11パスで、既存 Product テスト例外は CLI 分類関数のみ。
- Gate 07 は正本1件。S10・固定候補・同期後 HEAD の Git blob はすべて `6af42b17a403756b237c1b4c4a546bff4ef11381`。G01契約 tree は `c4b8fde6ffaab01077bae2b7cdd1fa672c524cb5`、S10→HEAD の `10_enhance_instruction` は差分なし。Owner 270に基づき承認前の DRAFT/NOT_FROZEN 表示を扱った。
- 固定候補→同期後 HEAD の8件は Owner 記録268–270、Gate/Trial/P05 の状態・報告類。source/test/schema/fixture/lock の差分なし。 `git worktree add --detach` で実行対象を候補そのものに設定し、実行前後に HEAD と空の porcelain を確認。
- `git merge-base --is-ancestor` で P01 → P02 → P03 → P04 → S10 → S11 → P05 → 前回 HEAD → 同期後 HEAD を照合。各 Package 報告の `PACKAGE_COMPLETE` を確認。

| Package | 固定チェックポイント |
| --- | --- |
| P01 | `9bff61f0eae25236f95f31f2cd3e7c81291f0167` |
| P02 | `3a76a0aa1698037354b284ba7b5a875300473ce6` |
| P03 | `858c9f73366036a2d1445e558135cd521f611462` |
| P04 | `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` |
| P05 | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |

## 実行環境・証跡 identity

Linux WSL2 kernel 6.18.58.1、実効 UID 1000、候補と物理試験の root は `/dev/sdd` の ext4。Python 3.12.16、pytest 9.0.3、causal-learn 0.1.4.8、NumPy 2.2.6、pandas 3.0.2、SciPy 1.13.1、PyArrow 24.0.0、PyYAML 6.0.3。117件の installed distributions の名前・版のソート済みハッシュは `1fd46e30fdb9c3af93ba04eb8302f4b4a6c59f8e0c411a51d26b4dca908ba62a`。Node は PATH 上に存在しなかった。完了後 `git status --porcelain` は候補で空。

| 構成 | Git object ID |
| --- | --- |
| `src` | `de1421ebc1899ce1d46c24ead6ddefe32b7a1c12` |
| `tests` | `ceeba201e33bf82a885939636234a0f0d58e832e` |
| G01 tests / fixtures | `4c1911603eb58e52363fa141ea252c567273c1f2` |
| root pytest conftest | `43fd0a0f4cf7e5950d08268496c9f953e457bd67` |
| Product tests | `650663a52557043f628d307ada99a16789b735fb` |
| Product conftest | `b03399ac86895e4606dea823704b7b669296f4f7` |
| Scientific tests | `9d8064a5bd4ef4adabd728bceabb315e953d6a83` |
| Schema/fixture tree | `8f7f4b781ce97c6a54dea2e115ea7b4c31426f9b` |
| `uv.lock` blob | `2b83110e86b26b7969fbddf8f98a727370ae19f7` |

物理 `uv.lock` SHA-256 `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。候補、S10、同期後 HEAD、pre-E11 基準の lock blob は一致。Schema プローブ環境は Python 3.12 に一時ディレクトリの validator を追加し、候補の `.venv` と lock は同一のまま使用した。 [照合コマンド・raw output](independent_raw_evidence.md#candidate-identity) · [Python 実行環境](independent_raw_evidence.md#runtime-identity) · [補助プローブ](independent_probe_inputs.md)

## 実行・再現

発見・照合コマンドの実測 exit 0 と stdout を証跡に収録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
