# ENH-E11 G01 Trial 01 Test Item 008 — DISCOVER-only envelope

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `008_discover_only_envelope` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / contract + real ext4 integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

実 FCI 成功の5ファイル、Status の科学未評価と Effect 非生成を確認。合成の scientific-negative 診断は独立の科学的負結果になるための証拠が未充足。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-07 | AC-05, AC-06 | RUN01、MAN03/04、GRAPH01、DISC01–03、AMD-001–003 | BLOCKED |

## 観測と根拠

`LocalCausalUseCase.run` の positive に実 FCI を使用。生成 inventory は `study.json`、`status.json`、`graph.json`、`manifest.json`、`_COMMITTED.json` のみ。Graph に全入力 lineage、Status に Identification NOT_APPLICABLE / Point NOT_REQUESTED / Inference NOT_REQUESTED / Science NOT_EVALUATED。Published Effect なし、実 FCI API と registry selection の一致と fallback 拒否を確認。Manifest factory の必須注入、typed fault は確認した。 [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [実公開 bundle の Schema 照合](independent_raw_evidence.md#b02-実公開-bundle-の-schema-照合) · [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [AMD-001–003 独立プローブ](independent_raw_evidence.md#実-cli--amd-001003-fault-controls--decision-各-field)

負例は synthetic `SCI_NO_ADMISSIBLE_PAG`、空・余剰・誤 Method/コード、Status/Manifest mismatch、型付き backend failure の拒否を確認。独立 B05 の条件を満たした実科学 negative と、全 malformed runtime/descriptor/stage を個別に実証する AMD 残項目は BLOCKED。試験済みの synthetic envelope は形式立証として記録した。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。
