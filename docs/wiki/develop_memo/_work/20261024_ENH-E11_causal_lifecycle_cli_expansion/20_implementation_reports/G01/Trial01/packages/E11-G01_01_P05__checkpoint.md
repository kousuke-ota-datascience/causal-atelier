# ENH-E11 G01 Trial 01 P05 Implementation Checkpoint Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** 本報告に状態、実施内容、実測結果と判断理由を記録する。

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Package: P05
- Package status: PACKAGE_COMPLETE
- Instruction: [06_G01_P05_cli_use_case_privacy.md](../../../../10_enhance_instruction/G01/06_G01_P05_cli_use_case_privacy.md)
- Starting commit: `94758d3964eb92fb7df3619f7c5d31d8d996862e`
- Implementation checkpoint SHA: `72bcd6acaab6caf48827bf2bb6cd5e249afd658b`
- Report commit SHA: PENDING
- Timestamp: 2026-11-24T10:14:40+09:00

## 1. Package objective

P05 の Local CLI 統合を完了し、AMD-004 に従って既存 Product CLI 分類と新コマンド登録の競合を解消する。

## 2. Implementation summary

前回の Local UseCase、aggregate-only Privacy、Manifest Factory、セッションに結び付いた公開前 abort を保持。Product の対象テスト 1 件のみを変更し、対象 CLI namespace に属する分類と登録先を固定した。

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `pyproject.toml` | modify | Local lifecycle CLI の登録 |
| `src/ariadne/capabilities/causal/local_execution.py` | add | Application orchestration |
| `src/ariadne/capabilities/causal/ports/local_io.py` | modify | 承認済みセッション型と begin/abort 境界 |
| `src/ariadne/capabilities/causal/ports/local_privacy.py` | add | Local Privacy Port |
| `src/ariadne/capabilities/causal/ports/manifest_factory.py` | add | Application 側の Manifest Factory Port と不変の証拠 |
| `src/ariadne/interfaces/cli/local_causal/command.py` | add | CLI composition と exit 分類 |
| `src/ariadne/interfaces/cli/local_causal/manifest_factory.py` | add | 既存の P01 Factory への変換 |
| `src/ariadne/interfaces/cli/local_causal/privacy.py` | add | aggregate-only ポリシー |
| `src/ariadne/interfaces/cli/local_causal/publication.py` | modify | AMD-003 の限定的な発行情報と照合 |
| `tests/enhancement/enh_e11/g01/integration/test_local_cli.py` | add | P05 focused 実 FS と CLI テスト |
| `tests/product/test_enh_e4_g07_p03_cli_boundary.py` | modify | AMD-004 で許可された分類テスト 1 件 |

## 4. Observable implementation facts

同期後の RESUME_BASE_SHA は `7c15920ab46c46b3a084432736c2c32fbb087e92`。S10 `307404e01c43bb83a286986f8f6d124e53032509` が祖先で、S10 以降は管理記録 266・267 のみ。歴史的開始 SHA からの同期差分は AMD-004 関連の P05 06、G01 07、正式 09 と管理記録 263〜267 のみだった。承認は `DEC-G01-P05-004-S11-REAUTH-01`。

同期前に復元用アーカイブ、状態一覧、worktree/index のバイナリ差分を `/tmp/enh-e11-p05-resume-mpmdxgr4` に作成。同期後に 13 パスすべての内容と Git 状態の一致を確認した。前回の停止報告と実装・テスト差分はこの保全に含まれる。凍結時・HEAD・作業ツリーの `uv.lock` blob は `2b83110e86b26b7969fbddf8f98a727370ae19f7`。実ファイル SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

## 5. Focused verification

| Command / method | Exit code | Result |
|---|---:|---|
| `.venv/bin/python -m pytest -q tests/product/test_enh_e4_g07_p03_cli_boundary.py` | 0 | 3 passed |
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01/integration/test_local_cli.py` | 0 | 19 passed |
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py` | 0 | 226 passed、既存 fork 警告 11 件 |
| Python `runpy.run_path` と `patch.object(tomllib, "loads", ...)` によるインメモリ登録変更 | 0 | 追加・欠落・改名・接頭辞内と外への登録先変更の 5 ケースをすべて拒否 |
| `git diff --check`、Product 対象関数を除いた前後テキストの一致確認 | 0 | whitespace エラーなし。定数・他テスト・Helper は一致 |

Python 3.12.16、Linux 6.18.58.1-microsoft-standard-WSL2、実 ext4。P05 focused テストと fixture の SHA-256 は `33e459617fc9e20149480615532de490165d588dc9e2c146844092150b3d00b0`。実公開／Reader、同一要求の再利用、Factory の委譲、別セッション拒否と FD、公開前の abort、publish 開始後の Application abort 禁止を観測した。

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): NONE
- Handoff facts: P01〜P04 の祖先関係、完了と検証記録を照合した。次工程は Candidate Assembly。 [Package Execution Status](E11-G01_01_P05__status.md)

## 7. Protected contract / Transition Debt impact

P01〜P04 のチェックポイント、既存 Product 実装、他の Product テスト、公開 Schema Version、科学的意味、P02 の既存公開アルゴリズムと Adapter の seal/publish を維持した。DEFERRED_PRODUCT_POLICY_BRIDGE は未完了。

## 8. Known limitations / unresolved observations

独立科学検証、T2/T3、独立 G01_999 受入は保留。

## 9. Semantic warning

このチェックポイントは Package 単位の実装証跡。Fixed Trial Candidate と Gate PASS は所定の別成果物で確定する。
