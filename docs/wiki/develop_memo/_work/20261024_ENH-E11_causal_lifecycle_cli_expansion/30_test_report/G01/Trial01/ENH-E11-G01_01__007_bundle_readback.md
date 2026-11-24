# ENH-E11 G01 Trial 01 Test Item 007 — Bundle readback / validation

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `007_bundle_readback` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / contract + real ext4 integration |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

実 Marker→Manifest→Study/Status/Graph の読戻し、hash を整合させた不正 Status の exit 5、型付き provenance・診断・upstream bytes の拒否を確認。全負例の独立実測は未完。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-06 | AC-03, AC-05, AC-06 | MAN01–05、READ01–05/07、PUB07–09、AMD-001 | BLOCKED |

## 観測と根拠

実 CLI で FCI fit → staging → seal/rename → `LocalManifestReader.read_run` を実施。Manifest 本体・Marker・3 artifact の byte/size/SHA と型、全入力の ref の一致、base status と実 bundle Schema を確認した。実 Run の Status を `SUCCESS` に置換し、Manifest Descriptor と Marker SHA を再計算しても CLI は exit 5、`SCHEMA_INVALID`。こうした合成負例は検証用の private ext4 fixture で実施した。 [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [実公開 bundle の Schema 照合](independent_raw_evidence.md#b02-実公開-bundle-の-schema-照合)

既存の実 Reader で missing/altered Marker、旧 Manifest、不正 diagnostics（整合済み hash）、不正 Graph provenance・upstream bytes の拒否を確認。Manifest Factory の既存 positive/negative と欠損・不正 Graph descriptor を pure 層で実行。AMD-001 の正規 Adapter が original P01 factory を呼ぶことを候補テストと実 CLI で確認。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest) · [AMD-001–003 独立プローブ](independent_raw_evidence.md#実-cli--amd-001003-fault-controls--decision-各-field)

READ/MAN の BLOCKED は、実 Reader で未実測の独立 cross-wire 変種（全 duplicate inventory・Status・link 組合せ）と AMD-001 の malformed Factory evidence 全変種。実 FS positive と上記個別負例の実行は PASS。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。

## 2026-11-25 追補 — AMD-E11-G01-ACCEPTANCE-001

**追補判定 — PASS。** 実 ext4 で seal→rename→Reader の正常読戻しを確認してから各変種を1箇所ずつ変更。duplicate inventory、Status/Manifest 不一致、unsafe ContentRef の各表記、symlink に置き換えた Status、余剰 private row、digest を更新した技術 code の diagnostics を Reader が型付き拒否した。既存の stale hash、Marker、provenance、実 Graph-positive 証拠を再利用。

実 stage の six-field descriptor を基に `ManifestBuildEvidence` を構築し、入力 Status を後から変更しても Factory の正規出力は元の Manifest bytes と一致した。malformed descriptor、fabricated SHA、Graph の bare key / MIME、runtime 欠損 / 不正、Status ID 不一致、技術 code の科学理由化を拒否し、stage の Marker と final run は0。

[追補の exact commands・実測出力・再現コード](independent_acceptance_001_supplement.md)
