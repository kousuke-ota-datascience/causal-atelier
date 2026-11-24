# ENH-E11 G01 Trial 01 Implementation Completion Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Execution Mode: WORK_PACKAGE
- Status: READY_FOR_TEST
- Execution status: READY_FOR_TEST
- Candidate state: READY_FOR_TEST
- Starting commit: `66ba62eff4a19e31a04a9688a00435af0549eb69`
- Fixed Trial Candidate SHA: `72bcd6acaab6caf48827bf2bb6cd5e249afd658b`
- 06 Contract: [正本 G01 06](../../../10_enhance_instruction/G01/06_Ariadne_ENH-E11_G01_implementation_instruction.md)
- P00 Plan: N/A
- Applicable 08 Remediation: NONE
- Previous Failed Candidate SHA: N/A
- Completion responsibility: WORK_PACKAGE_CANDIDATE_ASSEMBLY
- Timestamp: 2026-11-24T10:58:31+09:00

## 1. Candidate summary

G01 の Local DISCOVER 候補を独立検証に引き渡せる状態と判定した。実 ext4 での公開・Reader、Local CLI・FCI、関連する既存 Product と Scientific Core を統合検証し、必須実行集合の268件が通過した。Owner 記録269の条件を確認し、既存依存ガードの実測 FAIL と、変更影響外のナビゲーションテストを必須通過集合から個別に分離した。

## 2. Package checkpoint chain

| Package | Status | Checkpoint SHA | Checkpoint report | Report-only SHA |
|---|---|---|---|---|
| P01 | COMPLETE (`PACKAGE_COMPLETE`) | `9bff61f0eae25236f95f31f2cd3e7c81291f0167` | [Checkpoint](packages/E11-G01_01_P01__checkpoint.md) · [Status](packages/E11-G01_01_P01__status.md) | `94758d3964eb92fb7df3619f7c5d31d8d996862e` |
| P02 | COMPLETE (`PACKAGE_COMPLETE`) | `3a76a0aa1698037354b284ba7b5a875300473ce6` | [Checkpoint](packages/E11-G01_01_P02__checkpoint.md) · [Status](packages/E11-G01_01_P02__status.md) | `94758d3964eb92fb7df3619f7c5d31d8d996862e` |
| P03 | COMPLETE (`PACKAGE_COMPLETE`) | `858c9f73366036a2d1445e558135cd521f611462` | [Checkpoint](packages/E11-G01_01_P03__checkpoint.md) · [Status](packages/E11-G01_01_P03__status.md) | `94758d3964eb92fb7df3619f7c5d31d8d996862e` |
| P04 | COMPLETE (`PACKAGE_COMPLETE`) | `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` | [Checkpoint](packages/E11-G01_01_P04__checkpoint.md) · [Status](packages/E11-G01_01_P04__status.md) | `94758d3964eb92fb7df3619f7c5d31d8d996862e` |
| P05 | COMPLETE (`PACKAGE_COMPLETE`) | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` | [Checkpoint](packages/E11-G01_01_P05__checkpoint.md) · [Status](packages/E11-G01_01_P05__status.md) | `0fca54747758cf0e02e5a48d8227e6c8759981fe` |

## 3. Candidate Assembly evidence

- Required package set complete: YES（正本 Gate 06 の P01〜P05）
- Dependency chain complete: YES（各チェックポイントから次のチェックポイントと同期後 HEAD への祖先関係を Git で確認）
- Unresolved package blocker: NONE
- Integration check: G01 contract と実 Linux ext4 の統合検証を含む必須集合を実行
- Gate-wide regression: 268 passed / 0 failed / 2 deselected / 11 warnings。2件の実測履歴と処置は §8
- Candidate-affecting uncommitted change: NONE
- Fixed Candidate fixation command / method: `git rev-parse 72bcd6ac^{commit}`、祖先関係、候補から HEAD までの全差分、検証対象ツリーの一致を照合
- Blocker / remaining work: NONE（Candidate Assembly）

同期後のクリーンなブランチ `feature/ariadne_mvp_e11` で HEAD と FETCH_HEAD が `66ba62eff4a19e31a04a9688a00435af0549eb69` に一致した。前回 HEAD `b05be3106341de38ecfe70a3dd58269768078c50` からの差分は記録269の追加のみ。S10 `307404e01c43bb83a286986f8f6d124e53032509` → S11 `7c15920ab46c46b3a084432736c2c32fbb087e92` → P05 → 記録268 → 記録269の祖先関係を確認した。S10 から S11 までは管理記録266・267のみ。正本 Gate 06 は一意で、実行モード・必須 Package を同書から照合し、凍結状態は決定 `DEC-G01-ASSEMBLY-FREEZE-AUTHORITY-01` に従って S10 記録266とその SHA で判定した。 [Owner 記録268](../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/268_20261124_g01_trial01_assembly_freeze_authority_owner_decision.md) · [Owner 記録269](../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/269_20261124_g01_trial01_assembly_regression_baseline_scope_owner_decision.md)

## 4. Fixed Trial Candidate identity

```text
FIXED_TRIAL_CANDIDATE_SHA=72bcd6acaab6caf48827bf2bb6cd5e249afd658b
```

この Git commit が全 Package 実装を包含し、今回テストしたソース・テスト・依存の組合せを固定する。

## 5. Changed files / candidate semantics

P01 着手前 `ff38f2248ed5b6355a0c61ce9a3f575b6db21305` からの実装差分は Python ソース30件、テスト6件、`pyproject.toml` の Local CLI 登録1件。P01 の Study/Config/Manifest/JCS、P02 の Local FS・Publisher・Reader、P03 の PAG/ContentRef、P04 の限定 FCI、P05 の Local CLI・Privacy・Manifest Factory と公開セッションを含む。S10 以降に正本 Gate 契約・公開 Schema の差分はない。AMD-001〜004 を照合し、S11 から P05 の11パスが認可範囲に収まることを確認した。Port の `begin/abort`、`PublicationSessionToken`、Publisher 初期化、Adapter の `begin/abort` を除いた AST は同一。既存 Product 回帰では承認された分類関数以外の全テキストが一致した。 [G01 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md)

## 6. Protected passed-Gate impact

| Passed Gate / protected surface | Preserved semantic | Coding-side regression evidence |
|---|---|---|
| 既存 Product v2・Scientific Core | 旧 CLI 5件と Result v2、因果 Runtime operation stage/input matrix | 必須集合の該当テストが通過。matrix は個別実行も1件通過 |
| 既存 Product Frontend | Navigation、アプリシェル、テストの入力閉包 | frontend tree・対象テストが基準と同一。該当1件の扱いは §8 |
| ENH-E10 predictive extra | 既存 `predictive-advanced` 依存と遅延 Provider の保持 | TOML・lock・ライブラリ到達性を確認。既存ガードの FAIL を §8 に保持 |

## 7. Transition Debt impact

| TD ID | Action | Fact |
|---|---|---|
| `TD-G01-LEGACY-DEPENDENCY-GUARD-01` | preserve | STATUS=OPEN。因果依存の意図と、予測向け optional dependency も検索する既存ガードの整合を、別途承認された保守で扱う |
| `DEFERRED_PRODUCT_POLICY_BRIDGE` | preserve | UNFULFILLED。独立受入の依存として維持 |

## 8. Coding-side self-checks

Linux WSL2、実効 UID 1000、作業領域 ext4、Python 3.12.16、pytest 9.0.3、causal-learn 0.1.4.8。インストール済み distribution の `Name==Version` をソートした改行区切り一覧（末尾改行あり）の SHA-256 は `1fd46e30fdb9c3af93ba04eb8302f4b4a6c59f8e0c411a51d26b4dca908ba62a`。候補の G01 fixture/test tree は `4c1911603eb58e52363fa141ea252c567273c1f2`、`tests/conftest.py` は `43fd0a0f4cf7e5950d08268496c9f953e457bd67`、Product/Scientific Core tree はそれぞれ `650663a52557043f628d307ada99a16789b735fb` / `9d8064a5bd4ef4adabd728bceabb315e953d6a83`。

| 選定対象 | Lifecycle / layer | G01 07 / DD · 実観測 |
|---|---|---|
| `contract/test_local_codec.py` と `contract/test_graph_evidence.py` | enhancement / contract | 07-01/03/04、SPEC・GRAPH・MAN。Study/Graph と JCS の厳密な変換・入力拒否 |
| `integration/test_local_publication.py` と `integration/test_local_cli.py` | enhancement / integration | 07-02/05/06/07/11、REF・PUB・READ・RUN・PRIV。実 ext4 の公開・readback・競合・中断、CLI の Privacy、型付きエラーとセッション照合 |
| `integration/test_fci_discovery.py` | enhancement / integration | 07-08/10、CAP・METH-P106。選定 FCI の実 API と適格性、BK fail-closed |
| `tests/scientific` と選定した `tests/product` | 既存 suite / 当該テストの既存層 | 07-12、RUN06・PUB10・MAN06・READ06・EFF05。CLI、Result v2、Scientific Core、既存因果 Runtime の保護 |

| Command / method | Exit code | Result |
|---|---:|---|
| 下記の必須集合 pytest | 0 | 268 passed、2 deselected、11 warnings（fork の既存警告）、23.99秒 |
| `.venv/bin/python -m pytest -q tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_causal_runtime_operation_stage_and_input_matrix_are_preserved` | 0 | 1 passed |
| `.venv/bin/python -m pytest -q --tb=short tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_no_prohibited_causal_runtime_dependency_is_declared` | 1 | 1 failed。L87 `assert dependency not in project_config` で `lightgbm>=4.7.0,<4.8` を検出 |
| 同じ pytest を pre-P01 Git blob から一時ディレクトリに展開した同一テスト、TOML、因果ソースに対して実行 | 1 | 1 failed。同じ Python/pytest 環境で同じ L87 assertion と依存文字列を検出 |
| Git blob 比較、Python `tomllib`・AST・`importlib.metadata` による §8 の照合、`git diff --check` | 0 | 保護メソッド、依存宣言・lock、変更影響を照合 |

```sh
.venv/bin/python -m pytest -q -ra tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py tests/scientific tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py tests/product/test_enh_e3_causal_workflow_regression.py tests/product/test_estimator_compatibility_e1a.py --deselect=tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_no_prohibited_causal_runtime_dependency_is_declared --deselect=tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_navigation_route_change_has_no_execution_revision_metadata
```

**PRE_EXISTING_FAILURE — 実測 FAIL。** 依存ガードはベースライン・現行とも、ENH-E10 が追加した既存 `predictive-advanced` 内の LightGBM 宣言を拾った。`tomllib` で `project.dependencies` 15件、`project.optional-dependencies`、`dependency-groups` の意味的一致を確認。TOML 全体の差は承認済み Local CLI 登録のみ。lock はベースライン・S10・候補・作業ファイルで blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`、実ファイル SHA-256 `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

元のテストが打ち切った `import X` / `from X` の制約を、同じトップレベルの因果 Runtime ソースに対し `lightgbm`、`dowhy`、`econml` それぞれで確認し、3件すべて該当なし。変更30モジュールを起点に新規 subpackage、親パッケージ初期化、ネストした import を含む87ローカルモジュールを追跡。外部 import は既存の `causal-learn`、NumPy、pandas、PyArrow、SciPy、PyYAML で、実効環境の推移的依存を含む26 distribution の installed version がロックに存在し、禁止3件はその集合に含まれなかった。既存因果 Runtime の48モジュールの閉包は基準と同一。Product domain 初期化から参照される Predictive optional provider のメタデータと遅延ローダーは基準と同一で、現行 Local composition の FCI プローブは成功し、禁止3件は CLI プロセスにロードされなかった。Local の動的境界は選定 FCI factory と固定 worker、Git 実行、既存 libc 参照で、予測用 Provider を選ぶ経路は確認されなかった。債務は §7 のとおり OPEN。

**OUT_OF_SCOPE_FOR_G01 — 前回の実測は FileNotFoundError。** ナビゲーションテストは Node の標準 `fs` / `vm` とテスト内 catalog を用い、`frontend/navigation_state.js` と `frontend/app.js` を読み取る。ベースライン・現行の該当 blob は `66bfddd9c4a1db137a1bcb369025093ab5758` と `a75091db134d236bb6e4067ab9daaa0b4916da82`、frontend 全体の tree は `ab96281278c79c8626e66e72cb9116d24b9f3c1a`、対象テスト blob は `390196f5c77d8dde7481b7169f9334962c6113be` で一致。G01 の影響閉包外として今回の実行を分離した。

前回は狭い選定で226件通過、拡大選定で268件通過・2件失敗・fork 警告11件、ベースライン依存テスト1件失敗。今回の必須集合は記録269が指定した2つの node ID のみを分離した。独立科学・Gate 受入の結果は §10 参照。

## 9. Post-candidate changes

- Changes after Fixed Candidate: DOCUMENTATION_ONLY
- Diff description: P05 の実装報告4件、Owner 記録268・269、本 Completion Report
- Candidate semantics unchanged: YES

## 10. Handoff to Test / Audit Agent

- Fixed Trial Candidate SHA: `72bcd6acaab6caf48827bf2bb6cd5e249afd658b`
- Completion report: this file
- Expected next action: 候補 checkout の identity audit と独立 G01 07 検証
- 独立 S09、B02/B04、B05、実 FS/Reader、T2/T3、独立07および G01_999 の受入は独立工程で判定。記録269の処置は G01 Trial 01 Assembly 限定

## 11. Facts / Interpretation

### Facts

P01〜P05 の実装は祖先鎖に揃い、対象集合268件の実測が通過した。既存 FAIL の再現・依存境界の照合と、変更影響外のテスト入力の同一性を個別に確認した。

### Interpretation

Owner 記録268・269の条件と実測結果から、この候補は独立検証に進める。既存依存ガードは OPEN の債務として追跡する。

## 12. Evidence commit identity

`EVIDENCE_COMMIT_SHA` は本報告の記録後に取得し、実行結果で報告する。
