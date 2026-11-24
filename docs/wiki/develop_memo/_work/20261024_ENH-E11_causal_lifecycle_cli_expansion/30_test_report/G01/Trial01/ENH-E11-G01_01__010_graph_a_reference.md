# ENH-E11 G01 Trial 01 Test Item 010 — GRAPH-A independent reference

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `010_graph_a_reference` |
| 正式判定 | **BLOCKED** |
| 実行層 | independent science + real backend controls |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

少数変数の空グラフ、collider、潜在の観測同値性を扱う既存実 Backend テストを実行。正式な多変量 latent MAG/PAG の独立参照、T2/T3 プロトコルと実測が不足。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-09 | AC-04 | DD-E11-METH-P106、GRAPH01/03、B05、T2/T3 | BLOCKED |

## 観測と根拠

実 Backend の existing `test_real_backend_empty_graph_against_independent_empty_dag`、`test_real_qualified_collider_matches_independent_dag`、`test_real_fisherz_latent_projection_preserves_uncertainty` を実行。空グラフ、collider の endpoint、単一 marginal adjacency の不確定性の fixture は通過。Gate 07 §4 が要求する固定 DGP、実行可能な独立同値類 MAG/PAG oracle、複数 seed/variant、compelled/uncertain endpoint と事前登録済み定量セルの正式証跡が揃わない。 [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest)

承認記録が保持する G01 独立 B05 と T2→T3 は BLOCKED。T2 の mandatory cell・計算量実測、T3 の K/R/seed/cap・合否基準・定量実測は未確認。候補の Backend 出力から正解を生成する操作は行っていない。 [Owner 記録270](../../../00_enhance_background/Revised_requirements_definition_documents/combined_review/270_20261124_g01_trial01_independent_freeze_regression_scope_owner_decision.md)

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。

## 2026-11-25 追補 — AMD-E11-G01-ACCEPTANCE-001

**追補判定 — BLOCKED。** FCI 出力に依存せず、観測 collider `X→M←Z` と潜在 collider（`L→X,L→M,Z→M`、Lは潜在）を導出した。後者の latent projection は `X↔M←Z`。観測3点の skeleton の唯一の非隣接対 X,Z は周辺 m-separated、M 条件付きで m-connected。中心 M の2 arrowhead が不変。葉端点の TAIL/ARROW 2×2 はすべて ancestral で最大、同じ m-separation をもつため葉は CIRCLE。独立標準正規の線形係数と母集団共分散で非退化・その他の条件付き共分散も確認した。具体的な式・コード・fixture digest は追補資料に収録。

探索的 T2 Pilot は n=512、Fisher Z、BK=null、2 DGP 各100反復（seed 73000–73099）。固定候補の worker の fit を同一プロセスで実行し、正確な skeleton/PAG は観測 collider 93/100、潜在 collider 94/100。各200 true-positive edges、false positive は7と6、false negative と backend error は0。fit の計算量は約0.26秒/100反復・DGP（worker 起動時間を除く）。正式 acceptance や科学 PASS の判定には用いていない。

**T3 事前登録案の残項目。** 独立 Reviewer が参照と DGP 候補の適用性、必須 Hard/conditional/N/A cells、型と層別、独立 seed 範囲、R・計算予算・停止規定を確定する必要がある。凍結07の Bonferroni `alpha_j=.05/K` と replicate-level の事前指定判定を確定し、Pilot seed を除いた別の確定入力で実測する。07の候補しきい値と今回の探索結果を正式判定値へ昇格していない。正式な B05 受領、T3 事前登録確定・定量実測は未完。

[追補の exact commands・実測出力・再現コード](independent_acceptance_001_supplement.md)
