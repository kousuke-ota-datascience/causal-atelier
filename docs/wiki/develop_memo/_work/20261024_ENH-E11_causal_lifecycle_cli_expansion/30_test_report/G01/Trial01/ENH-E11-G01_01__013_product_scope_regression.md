# ENH-E11 G01 Trial 01 Test Item 013 — Product / scope regression

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `013_product_scope_regression` |
| 正式判定 | **BLOCKED** |
| 実行層 | Product/Scientific Core / contract + integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

必須PASS実行集合268件は実測で通過。LightGBM 依存ガードの既存 FAIL と navigation の対象外判定を独立に裏付けた。共通化 Bridge の完了条件は未充足。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-12 | AC-05, AC-06 | RUN06、PUB10、MAN06、READ06、EFF05、AMD-004、TD-G01-LEGACY-DEPENDENCY-GUARD-01 | BLOCKED |

## 観測と根拠

## 実行集合と旧 Product

依存ガードと navigation の2 node ID を個別に検証した後、Owner 270 に従い必須PASS集合から明示的に除外した。270件を収集し、2 deselected、268 passed、11 warnings、exit 0。G01 209件と Scientific Core/選定 Product 59件。対象ファイルの因果 Runtime operation stage/input matrix は通過。既存 CLI5件・Result v2・Identification/Estimation separation・Scientific adapters・汎用 workflow・estimator 互換性を実行した。Product 実装、DB migrations、frontend、旧 workflow、予測 provider の Git diff は基準からなし。 [必須PASS集合の全 node ID と実測出力](independent_raw_evidence.md#g01--scientific-core--product-必須pass集合)

AMD-004 のテスト差分は許可された分類関数だけ。旧5件+Local 1件・固定登録先 strictly match と CLI namespace の全体 filter、定数と他2件の不変を確認。対象ファイルは必須集合に含めた。候補ファイルは編集せず、loader の in-memory controls で旧/新 name の削除、namespace 内外への redirect、および余剰 in-namespace の7件をすべて拒否。 [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [必須PASS集合の全 node ID と実測出力](independent_raw_evidence.md#g01--scientific-core--product-必須pass集合)

## LightGBM 依存ガード

基準 `ff38f2248ed5b6355a0c61ce9a3f575b6db21305`、固定候補とも Python 3.12.16 / 同じ pytest で同じ node を単独実行。ともに exit 1、L87の `assert dependency not in project_config` が `lightgbm>=4.7.0,<4.8` に対して失敗。実測 FAIL を `PRE_EXISTING_FAILURE` として保持した。 [基準の実測FAIL](independent_raw_evidence.md#依存ガード基準) · [候補の実測FAIL](independent_raw_evidence.md#依存ガード固定候補)

- TOML の `project.dependencies`（実読取14件）、`project.optional-dependencies`（predictive-advanced）、`dependency-groups`（dev/docs）は等しい。意味差は承認済み CLI 登録のみ。 `uv.lock` は blob、実 bytes/SHAとも一致。
- 元 assertion が未到達にした `import X` と `from X` の確認を基準・候補の対象ディレクトリについて3依存すべて実行し、該当0。変更された30 Python module を起点に nested import と親 package を含む87 source module および26実効 distribution/version を確認。全 external distribution version が lock に存在し、禁止3依存は無し。既存 planner の48 module 比較も bytes 一致。動的参照に入る Predictive provider の遅延ローダーは基準と同一。Local composition の実 FCI worker API probe で禁止3 module の import は観測されなかった。
- `TD-G01-LEGACY-DEPENDENCY-GUARD-01` は `OPEN`。同一既存 FAIL の扱いは記録270の限定条件に従った。 [TOML/lock/closure の raw evidence](independent_raw_evidence.md#tomllockclosurefrontend-input) · [provider の保護証跡](independent_raw_evidence.md#provider--legacy-product)

## Navigation

対象テストと frontend tree が基準から byte 同一。Node の標準 fs/vm、テスト内 catalog と2ファイルが実入力。テスト本体 `390196f5c77d8dde7481b7169f9334962c6113be`、frontend tree `ab96281278c79c8626e66e72cb9116d24b9f3c1a`、該当 JS 2件の blob と引用入力の閉包を照合し `OUT_OF_SCOPE_FOR_G01` と判定した。先行 Assembly の Node 未検出 `FileNotFoundError` を履歴として維持。今回は node を再実行せず、PATH 上の Node 不在を別途確認した。 [Frontend 不変性](independent_raw_evidence.md#tomllockclosurefrontend-input) · [Owner 記録270](../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/270_20261124_g01_trial01_independent_freeze_regression_scope_owner_decision.md)

## 残存依存

`DEFERRED_PRODUCT_POLICY_BRIDGE = UNFULFILLED`。Local Registry/FCI の実測は実施し、legacy `ScientificValidationService.validate_submission` の変更なしを確認した。独立 Product 回帰は上記の実行集合で PASS、Gate 07-12 の最終 Bridge 受入は BLOCKED。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。

## 2026-11-25 追補 — AMD-E11-G01-ACCEPTANCE-001

**追補判定 — 改訂範囲で PASS。** Registry の公開 descriptor/factory maps は immutable、選定可能な entry は P1-M06 のみ。実 CLI 正例で Application preflight と registry-selected Adapter が同一実装 `ScientificEligibilityPolicy.check` を呼び、両方が fisherz を許可して実 Graph-positive が成立。非 null BK の負例は同一 Policy が typed 拒否し、fit 0。ソース照合により eligibility 数値・カテゴリ判定の実装を共有することを確認した。

旧 Product の実測268件と AMD-004 の正負例を再利用。候補・テスト・fixture・lock・関連受入条件は同一。LightGBM の既存 FAIL と `TD-G01-LEGACY-DEPENDENCY-GUARD-01 = OPEN`、navigation 対象外判定を維持。`DEFERRED_PRODUCT_POLICY_BRIDGE = UNFULFILLED / DEFERRED_TO_G10_P05`。G10_999 が独立受入を行う。

[追補の exact commands・実測出力・再現コード](independent_acceptance_001_supplement.md)
