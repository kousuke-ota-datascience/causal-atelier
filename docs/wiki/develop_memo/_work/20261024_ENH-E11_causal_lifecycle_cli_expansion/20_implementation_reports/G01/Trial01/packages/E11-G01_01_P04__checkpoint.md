# ENH-E11 G01 Trial 01 P04 Implementation Checkpoint Report

> **Document class:** Evidence Artifact
> **Self-containment:** MUST for own responsibility.

> **Evidence self-containment:** この報告に状態・実施内容・観測結果・判断理由を記録する。

- Project: Ariadne
- Enhancement: ENH-E11
- Gate: G01
- Trial: 01
- Package: P04
- Package status: PACKAGE_COMPLETE
- Instruction: [06_G01_P04_fci_backend_oracle.md](../../../../10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md)
- Starting commit: `cbd33c74f60e2eed8e38e5b2bc7ab3c6f7771b96`
- Implementation checkpoint SHA: `7dcf2061dae3c8832b2b3ec9be6900ad6ee7edb6`
- Report commit SHA: PENDING
- Timestamp: 2026-11-24T08:30:26+09:00

## 1. Package objective

Local FCI の選択、全ペア・全条件付け集合の適格性検査、PAG 出力を実装する。

## 2. Implementation summary

Local FCI の選択、全ペア・全条件付け集合の適格性検査、PAG 出力を実装した。

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `src/ariadne/capabilities/causal/method_registry.py` | add | Local Method メタデータ、実環境観測に基づく capability と型付き選択。 |
| `src/ariadne/scientific/capabilities.py` | add | Local Method メタデータ、実環境観測に基づく capability と型付き選択。 |
| `src/ariadne/scientific/ports/capability.py` | add | Local Method メタデータ、実環境観測に基づく capability と型付き選択。 |
| `src/ariadne/causal/discovery/contracts.py` | add | 検証済み入力の参照照合、厳密なカテゴリ領域、Discovery のディスパッチ。Dataset の復号は信頼済みの composition 側から受け取り、復号対象を ContentRef 照合済みバイトに限定する。 |
| `src/ariadne/scientific/ports/causal.py` | add | 検証済み入力の参照照合、厳密なカテゴリ領域、Discovery のディスパッチ。Dataset の復号は信頼済みの composition 側から受け取り、復号対象を ContentRef 照合済みバイトに限定する。 |
| `src/ariadne/scientific/causal_methods/fci_eligibility.py` | add | 全ペア・全条件付け部分集合、Fisher Z の数値条件、宣言済みカテゴリ領域の期待度数、非 null BK の実行前拒否。利用可能な計算資源の確認は呼び出し側から注入し、固定の打ち切り値は設けていない。 |
| `src/ariadne/scientific/causal_methods/discovery.py` | add | 選択済み FCI を標準出力・標準エラーから隔離して実行し、実ノード名、endpoint、来歴を GraphEvidence に保持。出力は staging sink を使用する。 |
| `src/ariadne/scientific/causal_methods/_fci_worker.py` | add | 選択済み FCI を標準出力・標準エラーから隔離して実行し、実ノード名、endpoint、来歴を GraphEvidence に保持。出力は staging sink を使用する。 |
| `tests/enhancement/enh_e11/g01/integration/test_fci_discovery.py` | add | 合成 fixture、独立に定めた期待 Graph、実 Backend と拒否境界の focused tests。 |

## 4. Observable implementation facts

S10 凍結 SHA `3ea759825810e95425a9e7557c3b2cc46b21157d` と正式 09・S10・S11 の記録 244・245・246 を照合した。S11 は `DEC-G01-P04-004-S11-REAUTH-01`。指定リポジトリ・ブランチ、クリーンな作業ツリー、凍結後の承認記録のみの差分を確認した。Trial 01 の正式 FAIL・08 remediation・既存 P04 チェックポイントは見つからなかった。P01 `9bff61f0eae25236f95f31f2cd3e7c81291f0167` と P03 `858c9f73366036a2d1445e558135cd521f611462` は HEAD の祖先だった。 [担当 P04 契約](../../../../10_enhance_instruction/G01/06_G01_P04_fci_backend_oracle.md)

`uv.lock` の凍結時・HEAD・作業ツリーの Git blob は `2b83110e86b26b7969fbddf8f98a727370ae19f7`、実ファイルの SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

元の証拠コミット SHA `93c2fcf71532d87049a8c184670b60c75420ae00`（コミット時刻 2026-11-23T15:12:59+09:00）。 Timestamp は報告の再編時刻。

## 5. Focused verification

| Command | Exit code | Result summary |
|---|---:|---|
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01 tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py tests/product/test_enh_e4_g04_result_artifact_contract.py tests/product/test_domain_and_snapshot.py` | 0 | 207 件通過。 |

**207 passed**。P04 focused tests 30 件と、P01–P03 および Product 回帰 177 件。既存 P02 の fork に関する非推奨警告 11 件。Python 3.12.16、NumPy 2.2.6、`causal-learn` 0.1.4.8。実 FCI シグネチャの SHA-256 は `fb317b20b82d6490b5765b808de14b8847157b10698cd34683e47eba0b63f5d1`。P04 fixture を含むテストファイルの SHA-256 は `c127eb559ca12f07bf932342f6739e0204808ff5b7a27fb560c28344b2b6685c`。新規プロセスで Registry を import し、`causallearn` が import されないことも確認した。

| DD / Gate Test | Lifecycle / Layer | 観測結果 |
| --- | --- | --- |
| CAP01/04/05、DISC01 / 07-08 | enhancement / integration | 実 FCI の版・シグネチャ、選択 Profile、lazy load、未利用 Backend と利用不可時の拒否 |
| METH-P106、DISC02/03 / 07-08 | enhancement / integration | `fisherz`・`chisq`・`gsq` の実 fit。三変数で depth=0 でも全 6 triples を検査。期待度数 5、5 未満、空の層、不正符号、不十分な行数、定数列、悪条件行列、検査未完了、両方向の逆行列残差を検証 |
| GRAPH01/03 / 07-09 | enhancement / integration | 空 DAG、潜在共通原因、観測コライダーから独立に期待 PAG を定め、実 fit と照合。潜在例の circle とコライダーへの arrowhead を保持。出力順序・外部バイトハッシュと意味ハッシュを確認 |
| METH-P106 / 07-10 | enhancement / integration | 2 ノードの潜在共通原因モデルと直接原因モデルで同じ観測共分散を確認。空配列を持つ非 null BK は Backend 呼び出し・staging ともゼロ |

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): P05
- Handoff facts: P01・P03 を照合した。 [Package Execution Status](E11-G01_01_P04__status.md)

## 7. Protected contract / Transition Debt impact

Product 回帰の観測結果は §5 に記録した。DEFERRED_PRODUCT_POLICY_BRIDGE の未完了依存は維持される。

## 8. Known limitations / unresolved observations

独立科学受入、T2/T3、G01_999、および DEFERRED_PRODUCT_POLICY_BRIDGE は保留。

この Graph Oracle は開発用合成 fixture の証拠であり、独立科学受入、T2/T3、G01_999 は保留。承認された `DEFERRED_PRODUCT_POLICY_BRIDGE` も保留で、Product v2 のポリシーへの接続は独立受入条件に残る。

## 9. Semantic warning

チェックポイントは Package 単位の実装証跡。Fixed Trial Candidate と Gate PASS は別の成果物で確定する。
