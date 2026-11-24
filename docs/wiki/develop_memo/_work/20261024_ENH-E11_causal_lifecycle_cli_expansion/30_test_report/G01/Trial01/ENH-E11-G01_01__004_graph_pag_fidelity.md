# ENH-E11 G01 Trial 01 Test Item 004 — PAG / Graph evidence fidelity

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `004_graph_pag_fidelity` |
| 正式判定 | **PASS** |
| 実行層 | enhancement / contract + real ext4 integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

両方向の全定義 endpoint pair が往復一致し、standalone PAG の Product version IDs と lag は null。自己ループ・重複・未知端点・不正 provenance を拒否。実 Reader は記述子を再計算した不正 provenance も拒否。旧 Product の Version 発行元は変更差分の外。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-03 | AC-02 | GRAPH01/03/04 | PASS |

## 観測と根拠

`GraphEvidence.canonical_payload/from_canonical_json` の往復は全定義 endpoint pair と source/target 反転の試験で一致。NULL Product IDs/lag、重複 pair、自己ループ、未知ノード/端点、typed provenance と ContentRef の負例を確認。Product tree と旧 GraphVersion writer は基準から差分なし。Source ref すり替え等を新しい Graph hash と Descriptor/Marker hash で整合させた Reader 負例も実 ext4 で拒否。実 FCI の正例で実行/保存 Graph の provenance は入力三 Ref と一致した。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [実公開 bundle の Schema 照合](independent_raw_evidence.md#b02-実公開-bundle-の-schema-照合)

科学的 endpoint の妥当性と正式同値類 reference の判断は [010](ENH-E11-G01_01__010_graph_a_reference.md) に記録。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
