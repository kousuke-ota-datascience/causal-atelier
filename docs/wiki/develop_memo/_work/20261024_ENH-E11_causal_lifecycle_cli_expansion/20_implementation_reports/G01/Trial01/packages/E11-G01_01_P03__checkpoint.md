# ENH-E11 G01 Trial 01 P03 Implementation Checkpoint Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** この報告に状態・実施内容・観測結果・判断理由を記録する。

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Package: P03
- Package status: PACKAGE_COMPLETE
- Instruction: [06_G01_P03_pag_graph_version.md](../../../../10_enhance_instruction/G01/06_G01_P03_pag_graph_version.md)
- Starting commit: `ad6fdda04f3b6a5dd561ab15bbc7d05b5d7680da`
- Implementation checkpoint SHA: `858c9f73366036a2d1445e558135cd521f611462`
- Report commit SHA: PENDING
- Timestamp: 2026-11-24T08:30:26+09:00

## 1. Package objective

PAG endpoint、型付き GraphProvenance、Reader の来歴照合を実装する。

## 2. Implementation summary

PAG endpoint、型付き GraphProvenance、Reader の来歴照合を実装した。

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `src/ariadne/causal/discovery/graph_evidence.py` | add | 不変の GraphEvidence と六フィールド GraphProvenance、ソース ContentRef、初回 Graph の null 親、意味ハッシュの検証。 |
| `src/ariadne/shared/graph_semantics.py` | add | Product の既存グラフ検証器への endpoint 名の明示的な変換。E11 round trip では入力のノード・辺の配列順と矢印の向きを保持する。 |
| `src/ariadne/interfaces/cli/local_causal/manifest_reader.py` | modify | 承認 221 の readback 経路で型付き来歴を検証し、Study と Manifest へ照合。既存の同一 FD による参照先バイト検証を引き続き実行する。Publisher が使う既存の staging/seal 検証経路は従前のまま。 |
| `tests/enhancement/enh_e11/g01/contract/test_graph_evidence.py` | add | P03 focused tests と承認済み Reader 回帰。 |
| `tests/enhancement/enh_e11/g01/integration/test_local_publication.py` | modify | P03 focused tests と承認済み Reader 回帰。 |

## 4. Observable implementation facts

Owner 承認 221・222・224・226 とハンドオフ 227 を照合した。凍結 SHA は `52e5c60176d6b72c91f839ef267f46657bd380b5`。[P03 契約](../../../../10_enhance_instruction/G01/06_G01_P03_pag_graph_version.md) と AMD-E11-G01-P03-001 を適用した。指定リポジトリへの remote、`feature/ariadne_mvp_e11`、クリーンな作業ツリー、凍結後の管理記録の差分を確認した。Trial 01 の正式な FAIL・08・既存 P03 チェックポイントは見つからなかった。

P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` と P02 `3a76a0aa1698037354b284ba7b5a875300473ce6` は HEAD の祖先で、既存のチェックポイントと当時の報告を保持した。`uv.lock` の Git blob は凍結時・HEAD・作業ツリーとも `2b83110e86b26b7969fbddf8f98a727370ae19f7`。実ファイルの SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

従来の `provenance={}` の Graph bundle は、改訂後の Reader で明示的に拒否する。非 null 親は初回 G01 DISCOVER で拒否する。将来の科学的 successor を今回の P03 で発行していない。

元の証拠コミット SHA `748deb4ba6287bbd1b71e233504c36c6f430e5b7`（コミット時刻 2026-11-23T13:41:00+09:00）。 Timestamp は報告の再編時刻。

## 5. Focused verification

| Command | Exit code | Result summary |
|---|---:|---|
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py` | 0 | 177 件通過。 |

**177 passed**。P03 契約 48 件、P02/Reader 実 FS 43 件、P01 契約 69 件、Product 17 件。Linux 6.18.58.1-microsoft-standard-WSL2、Python 3.12.16、実 ext4。Python 3.12 の fork に関する非推奨警告 11 件。

合成 Graph 契約テストの SHA-256 は `0e9dc2e37624cce4384e0541eeab03c1313225b57a46c78014725a9726424b32`。Reader fixture を含む実 FS テストの SHA-256 は `35c707a011948b24a54fdd0aef648337db20c4c73087b813fb31faa813047e88`。

| DD / Gate Test | Lifecycle / Layer | 観測結果 | 判定 |
| --- | --- | --- | --- |
| GRAPH01 / 07-03/04 | enhancement / contract | 全 9 endpoint 組み合わせの各 2 向きを正確に往復。意味ハッシュとファイルバイトの SHA-256 を分離。 | PASS |
| GRAPH03 / 07-03 | enhancement / contract | 自己ループ、重複・反転重複、未知ノード、無効な mark、lag、temporal、非 PAG を拒否。 | PASS |
| GRAPH04 / 07-03/06 | enhancement / contract + integration | 初回 null 親と null Product ID を適用。不正な来歴や ContentRef を拒否。Reader は CI・参照の不一致、親参照、実ソースバイトの改変を拒否。 | PASS |
| MAN03/04 / 07-07 | enhancement / integration | Graph-positive と合成診断 negative の既存公開・readback 回帰を再実行。 | PASS |
| Product CLI / Graph / Artifact | product | CLI、既存 Graph endpoint 往復、Artifact 契約の回帰を実行。 | PASS |

Graph fixture は構造検証に使用した。実 P04 の独立 MAG/PAG 科学検証と G01_999 の受入は保留。

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): P04
- Handoff facts: P01 と Reader 互換修正の対象である P02 を照合した。 [Package Execution Status](E11-G01_01_P03__status.md)

## 7. Protected contract / Transition Debt impact

Product 回帰の観測結果は §5 に記録した。DEFERRED_PRODUCT_POLICY_BRIDGE の未完了依存は維持される。

## 8. Known limitations / unresolved observations

実 P04 の独立 MAG/PAG 科学検証と G01_999 は保留。


## 9. Semantic warning

チェックポイントは Package 単位の実装証跡。Fixed Trial Candidate と Gate PASS は別の成果物で確定する。
