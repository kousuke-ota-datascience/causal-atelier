# ENH-E11 G01 Trial 01 Test Item 009 — FCI API / CI eligibility

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `009_fci_api_eligibility` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / contract + real Python 3.12 backend |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

実 Python 3.12 の署名と `fisherz/chisq/gsq` の fit、厳密 Design、独立に算出した E=5/E<5、float64 の all-S を確認。数値境界の全独立負例は未完。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-08 | AC-01, AC-04 | CAP01/04/05、DD-E11-METH-P106、B02/B04 | BLOCKED |

## 観測と根拠

B02 は G01 の実効 Python 3.12で正本 Draft 2020-12 validator の G01 対象 Question/Design/Method Config/diagnostics、実公開 Study/Status/Graph/Manifest/Marker の正例・版負例を実行。厳密 Design parser で `1.0`/`1e0`、boolean、文字列、範囲外、欠落、順序違反を拒否。B04 は Python 3.12.16、causal-learn 0.1.4.8 で `fci` の `node_names` を実測し、署名 SHA `fb317b20b82d6490b5765b808de14b8847157b10698cd34683e47eba0b63f5d1`。3 CI の正例 fit を実行し、型指定と非連続コードの `chisq/gsq` を実 CLI でも確認。独立に数えた期待度数5で exit 0、4と空の宣言域で exit 2。 [Schema/JCS/FCI プローブ](independent_raw_evidence.md#b02-draft-2020-12--strict-parser--jcs--b04-api) · [実公開 bundle の Schema 照合](independent_raw_evidence.md#b02-実公開-bundle-の-schema-照合) · [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls)

Fisher Z は実 float64 の3列6組で相関 submatrix、2-norm condition × eps、左右残差の最大行和、partial r を独立算出。ランク落ち・near singular は fit 0、NaN 入り実 Parquet は exit 2、fit 0。既存テストの残差片側・条件数の閾値注入、不完全 scan、実 API の node order mismatch は通過。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [Fisher Z 独立プローブ](independent_raw_evidence.md#fisher-z-数値nan--no-fit-controls)

B02/B04 の上記実行は PASS。G01-07-08 の独立数値負例全体は BLOCKED。逆行列演算の個別障害、`abs(partial_r)>=1` の独立制御と追加境界例の完全な観測は未充足。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
