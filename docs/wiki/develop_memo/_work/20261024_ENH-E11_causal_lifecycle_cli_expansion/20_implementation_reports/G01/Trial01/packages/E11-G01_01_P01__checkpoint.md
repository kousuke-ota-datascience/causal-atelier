# ENH-E11 G01 Trial 01 P01 Implementation Checkpoint Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** この報告に状態・実施内容・観測結果・判断理由を記録する。

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Package: P01
- Package status: PACKAGE_COMPLETE
- Instruction: [P01 06](../../../../10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md) · [AMD-E11-G01-P01-003](../../../../10_enhance_instruction/G01/09_ENH-E11_G01_AMD-E11-G01-P01-003_Gate_Contract_Amendment.md)
- Starting commit: `af304408e6daa37d395e0dc6ca2ba0c173cadd65`
- Implementation checkpoint SHA: `ae40ab9e7a942a4aa97d7cde3c8ea34ba3686c96`
- Report commit SHA: 実行時の handoff に記録
- Timestamp: 2026-11-25T02:02:23+09:00

## 1. Package objective

AMD-E11-G01-P01-003 の S09-JCS-01 を修正し、数値バイト列とダイジェストを呼出側の Decimal context から独立させる。既存 P01 の実装と証拠は元のチェックポイントと報告コミットで参照できる。

## 2. Implementation summary

`_number` は binary64 の最短往復表現から桁と小数点位置を取り出し、RFC 8785 の固定・指数表記を文字列操作で生成する。Decimal の正規化を除去し、指数境界と符号付きゼロの扱いを保った。変更前後の AST 照合で、`_number` 本体と Decimal import 以外の同一性を確認した。 [RFC 8785 Appendix B](https://www.rfc-editor.org/rfc/rfc8785.html#appendix-B)

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `src/ariadne/shared/serialization/jcs.py` | modify | Decimal 精度・トラップに依存した丸めを除去 |
| `tests/enhancement/enh_e11/g01/contract/test_jcs_context_independence.py` | add | 数値のバイト列・SHA・parse・context flags、凍結ベクトルと実 ext4 の公開・Reader を検証 |

## 4. Observable implementation facts

作業ブランチ `feature/ariadne_mvp_e11` はリモート同期時点でクリーンで、HEAD と FETCH_HEAD は開始 SHA に一致。S10 `4a355403c2a66a76a6e2965e16fdf7637258e33e` 以降の差分は Owner 記録272・273のみ。独立検証証拠から S10 までの差分は正式09・P01 06・G01 07 の3件。記録273の限定例外を適用し、Trial01 の P01 を再開した。 [Owner 記録272](../../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/272_20261125_g01_p01_003_s10_owner_freeze.md) · [Owner 記録273](../../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/273_20261125_g01_p01_003_s11_owner_authorization.md)

`uv.lock` の Git blob は `2b83110e86b26b7969fbddf8f98a727370ae19f7`、実ファイル SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。修正後の JCS blob は `5c912f63476026dabf0827eb7f3f5aa644009699`、contract テスト tree は `3c495091a93f3198d1da4b4e97e2d3a53ccb5bdb`。凍結 JCS ベクトル SHA-256 は `ba1e4349d3bf2ff6a055eab1f802762164e3ef05ff4873c6cabfdf883dd9eaec`。

追跡ソース・テストと新規テストの計534 Python ファイルを AST で走査し、JCS の直接16、推移のみ7モジュールを確認した。直接経路は Study/Config、Discovery contracts、GraphEvidence、FCI discovery、Manifest と Factory Port、Reader、Publisher、Privacy、Local UseCase と関連テスト。推移経路は Adapter Factory、Method registry、FCI eligibility、Capability/Discovery ports、Local CLI と CLI テスト。公開 schema・lock・Worker/Frontend・既存テスト・独立報告に修正差分はない。

## 5. Focused verification

Linux WSL2、UID 1000、実 ext4、Python 3.12.16、pytest 9.0.3、`causal-learn` 0.1.4.8。インストール済み distribution のソート済み `Name==Version` 行一覧（末尾改行あり）の環境 SHA-256 は `1fd46e30fdb9c3af93ba04eb8302f4b4a6c59f8e0c411a51d26b4dca908ba62a`。

| Command / method | Exit code | Result summary |
|---|---:|---|
| `.venv/bin/python -m pytest -q --tb=short 'tests/enhancement/enh_e11/g01/contract/test_jcs_context_independence.py::test_numeric_bytes_digest_and_parse_do_not_depend_on_decimal_context[precision-6]'`（旧実装） | 1 | `{"alpha":0.123457}` を観測。期待 `{"alpha":0.123456789}` との相違で1件失敗 |
| 以下の必須回帰コマンド | 0 | 274 passed、2 deselected、11 warnings（fork）、40.56秒 |
| Python で seed 8785 の binary64 値と境界近傍を生成し、既存 Playwright 同梱 Node v24.18.1 の `JSON.stringify` と比較 | 0 | 有限106,105件が一致 |
| 旧候補 checkout を `PYTHONPATH` で選択した Python で新規テストの `_configure`・`_invoke` を使用。次に修正版で `_read_and_check` と CLI を実行 | 0 | 旧候補の通常 context で公開。修正版は precision 1・制限 exponent・Inexact/Rounded trap 下で Reader と再利用が成功。異なる alpha は `RUN_ID_CONFLICT` / exit 5。旧バンドル5ファイルの全バイトを照合 |
| 依存ガードの node ID を baseline の Git blob 展開先と現行作業ツリーで個別に実行 | 1 / 1 | 両方で同じ既存 `lightgbm>=4.7.0,<4.8` assertion FAIL |

```sh
.venv/bin/python -m pytest -q -ra tests/enhancement/enh_e11/g01 tests/scientific tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py tests/product/test_enh_e5_g03_p02_identification_estimation_separation.py tests/product/test_enh_e3_causal_workflow_regression.py tests/product/test_estimator_compatibility_e1a.py --deselect=tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_no_prohibited_causal_runtime_dependency_is_declared --deselect=tests/product/test_enh_e5_g03_p03_causal_runtime_regression.py::test_navigation_route_change_has_no_execution_revision_metadata
```

| DD / Gate Test | Lifecycle / Layer | 実観測 |
|---|---|---|
| MAN01–03 / G01-07-04 | enhancement / contract | RFC Appendix B の境界・tie、alpha、凍結7正例・7負例を確認。precision 1/6/28/80、rounding modes、exponent 制限、traps と既存 flags を含む context を保持 |
| SPEC01–04・GRAPH01・MAN01–06 / G01-07-01/03/04/06/07 | enhancement / contract | Study、PAG、Manifest、Unicode・キー順、ダイジェストと不正入力を既存 suite で検証 |
| REF・PUB・READ・RUN・PRIV / G01-07-02/05/06/07/11 | enhancement / 実 FS integration | 修正版で通常と precision 6 相互生成・読取りを実測。同一要求は同一 SHA、変更要求は拒否。丸めた Study で原マーカー・Manifest を保持した不整合バンドルを `ARTIFACT_HASH_MISMATCH` で拒否し、ファイルを変更しなかった |
| CAP・METH-P106 / G01-07-08/10 | enhancement / integration | 実 FCI Adapter、Graph 出力と eligibility の既存テストを再実行 |
| G01-07-12 | 既存 Scientific Core・Product / regression | CLI・結果・stage/input matrix を含む保護回帰を再実行 |

旧候補の物理 SHA-256 は Study/request `0eafa62cb63af7fa6cbe6c8fc82f5a8ce0aa0c9090344d0889ac264fc80cba76`、Graph bytes `f931eb217daab5c292a2d3363873b4d571169925104af9107431506e38f5937b`、Manifest `0d9806b48c81eeefe839c2f5b44f150030f6c78ea16f2ae77f62170fb22429e4`、Marker `d6322bebba881bdd23105587aaa26b68fc623a9d4aa046fb0e54a35f8c23a2c1`。Graph semantic SHA-256 は `be7144ca96823095b33f515dacf8902a13ff869bb6c70ff551631a29e906a1b5`。Reader は旧ファイルの照合を通過し、比較前後でバイトが同一だった。

既存2件の処置は記録269/270に基づく。前回の必須268件は今回も実行した。依存ガードは P01前 `ff38f2248ed5b6355a0c61ce9a3f575b6db21305` と現行で FAIL を再現し、`PRE_EXISTING_FAILURE` を維持。TOML の依存・extras・groups、lock と因果 Runtime の `lightgbm`、`dowhy`、`econml` 直接 import 制約を照合。修正は stdlib `Decimal` import の除去だけで新規 Runtime 依存はない。ナビゲーションは frontend tree `ab96281278c79c8626e66e72cb9116d24b9f3c1a` と対象テスト blob `390196f5c77d8dde7481b7169f9334962c6113be` が基準と一致し、変更の影響外として `OUT_OF_SCOPE_FOR_G01` を維持。以前の `FileNotFoundError` は履歴。指定2 node ID のみを必須集合から分離した。

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): 該当なし。置換候補の Assembly に引き渡す。
- Handoff facts: 旧 P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` → P02 `3a76a0aa1698037354b284ba7b5a875300473ce6` → P03 `858c9f73366036a2d1445e558135cd521f611462` → P04 `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6` → P05/旧候補 `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` → 修正 P01。独立検証証拠 `2e56c2a04f4d11d10fdcb7b3ad5c148ab6747d91` と旧 P01 証拠 `4248ca24204ed8ede27527191b1a53d9ced1ff5a` は履歴に保持。 [Package Execution Status](E11-G01_01_P01__status.md)

## 7. Protected contract / Transition Debt impact

公開 codec VERSION `e11-json-jcs-rfc8785/1`、公開 API、既存テスト・schema・lock は同一。`TD-G01-LEGACY-DEPENDENCY-GUARD-01` は OPEN、`DEFERRED_PRODUCT_POLICY_BRIDGE` は UNFULFILLED。

## 8. Known limitations / unresolved observations

置換候補の Assembly と独立再検証が残る。旧 G01_999 BLOCKED は履歴として維持。T3 正式実行は未認可。

## 9. Semantic warning

このチェックポイントは P01 限定修正の実装証拠。候補の固定と Gate 受入判定は後続工程で扱う。
