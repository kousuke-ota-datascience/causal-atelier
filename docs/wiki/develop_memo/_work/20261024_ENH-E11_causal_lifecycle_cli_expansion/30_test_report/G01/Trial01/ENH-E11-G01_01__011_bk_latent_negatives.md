# ENH-E11 G01 Trial 01 Test Item 011 — BK / latent negatives

| 項目 | 記録 |
| --- | --- |
| Test Item ID | `011_bk_latent_negatives` |
| 正式判定 | **BLOCKED** |
| 実行層 | enhancement / real backend boundary + independent science |
| Fixed Trial Candidate / actual tested HEAD | `72bcd6acaab6caf48827bf2bb6cd5e249afd658b` |
| TEST_START_SHA | `249bc48433e1472442fdbedfb9b848896e58d648` |
| 実行日 | 2026-11-24（JST） |
| Acceptance authority | [凍結 Gate 07](../../../10_enhance_instruction/G01/07_Ariadne_ENH-E11_G01_test_instruction.md) |

空 BK と矛盾 BK の CLI exit 4、BACKEND_SEMANTICS_UNVERIFIED、1行 JSON と無漏洩を確認。BK を有効化する独立科学的 remedy の証跡は未成立。

| 検証項目 | AC | DD ID / 検証目的 | 判定 |
| --- | --- | --- | --- |
| G01-07-10 | AC-04 | DD-E11-METH-P106、GRAPH03、B05 | BLOCKED |

## 観測と根拠

`ScientificEligibilityPolicy.check` / CLI の B05 fail-closed 要件を観測。空配列 BK と required/forbidden に同じ `[source,target]` を持つ矛盾 BK を、Study と Design の両方に設定し、Design file SHA を更新。実 CLI は双方に `BACKEND_SEMANTICS_UNVERIFIED`、exit 4、stdout JSON 1行、stderr は型付き code / phase のみ。staging、Graph、Marker、node名漏洩0。候補テスト `test_preflight_rejection_never_calls_backend` の BK ケースも通過。 [独立 CLI/Reader プローブ](independent_raw_evidence.md#独立実-cli--reader--amd-004-controls) · [G01 の全 node ID と実測出力](independent_raw_evidence.md#独立-g01-pytest)

2変数の latent 観測同値性は共分散一致を実行して確認。Issue #266 に関する独立 motif の expected vs observed、科学的 BK remedy と正式独立審査は未充足。運用上の fail-closed の観測は PASS、B05 の受入として BLOCKED。

## 実行・再現

固定候補 checkout で上記の各テスト/プローブを再実行できる。正負例の exact command、node ID、fixture、exit、実 stdout と必要な故障注入は実測出力を参照。候補・fixture・環境 identity は [001](ENH-E11-G01_01__001_candidate_identity.md) に記録した。

[実測出力](independent_raw_evidence.md) · [再実行用資料](independent_probe_inputs.md)

検証対象に対する production code、repo tests、migration、依存定義、凍結契約の変更は0件。

## 2026-11-25 追補 — AMD-E11-G01-ACCEPTANCE-001

**追補判定 — 改訂範囲の hazard／refusal は PASS。** latent common cause と直接効果の2変数 Gaussian の共分散を同じ `[[2,1],[1,2]]` と独立に確認。BK hazard は完全3点 skeleton の selection-free ancestral MAG を列挙。Y→Z の禁止下でも Z→Y の DAG と Z↔Y の MAG が可能で、観測 CI から Z 側の TAIL は強制されない。実 causal-learn 0.1.4.8 の BK orientation 関数に isolated `Z o→Y` を与えると、禁止条件で Z を TAIL に確定し、stdout を3行出力した。これはオリエンテーション段階の hazard 実測。

G01 CLI では空 BK と矛盾 BK を fixture の Study/Design に設定し、双方で exit 4、`BACKEND_SEMANTICS_UNVERIFIED`、JSON 1行、node 名漏洩なし、FCI fit 0、stage 0。BK-positive 利用可能化は延期。包括的な独立 B05 受入は010で引き続き BLOCKED。

[追補の exact commands・実測出力・再現コード](independent_acceptance_001_supplement.md)
