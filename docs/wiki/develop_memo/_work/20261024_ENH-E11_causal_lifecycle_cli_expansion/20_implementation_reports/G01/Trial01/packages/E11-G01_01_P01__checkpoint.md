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
- Instruction: [06_G01_P01_local_contract_codec.md](../../../../10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md)
- Starting commit: `ff38f2248ed5b6355a0c61ce9a3f575b6db21305`
- Implementation checkpoint SHA: `9bff61f0eae25236f95f31f2cd3e7c81291f0167`
- Report commit SHA: PENDING
- Timestamp: 2026-11-24T08:30:26+09:00

## 1. Package objective

厳密な Study・ContentRef・JCS・Manifest を実装する。

## 2. Implementation summary

厳密な Study・ContentRef・JCS・Manifest を実装した。

## 3. Changed files

| Path | Change | Reason |
|---|---|---|
| `src/ariadne/shared/content_ref.py` | add | 五フィールド参照と型付き検証。 |
| `src/ariadne/shared/serialization/jcs.py` | add | RFC 8785 用バイト列と SHA-256。 |
| `src/ariadne/causal/design/study.py` | add | 不変の Study と非 Effect の Estimand。 |
| `src/ariadne/causal/inference/contracts.py` | add | 不変の Study と非 Effect の Estimand。 |
| `src/ariadne/interfaces/cli/local_causal/study.py` | add | JSON/YAML Study の検証と G01 Method のディスパッチ。 |
| `src/ariadne/interfaces/cli/local_causal/config_decoder.py` | add | JSON/YAML Study の検証と G01 Method のディスパッチ。 |
| `src/ariadne/interfaces/cli/local_causal/manifest.py` | add | 不変の証拠と Manifest の組み立て、成果物照合、AMD-002 の理由コード制約。 |
| `tests/enhancement/enh_e11/g01/contract/test_local_codec.py` | add | P01 focused tests。 |

## 4. Observable implementation facts

Owner 承認 190・191・193 とハンドオフ 194 を照合し、凍結 SHA `bcc1d797e1406e8816d12b725eeace07a181c702` の [P01 契約](../../../../10_enhance_instruction/G01/06_G01_P01_local_contract_codec.md) を適用した。開始ブランチは `feature/ariadne_mvp_e11` で作業ツリーはクリーンだった。凍結後の差分は管理記録に限られ、正式な G01 FAIL・08 remediation・既存 P01 チェックポイントは見つからなかった。

凍結時と実行時の `uv.lock` の Git blob は `2b83110e86b26b7969fbddf8f98a727370ae19f7`。実ファイルの SHA-256 は `1d92a472fc3c750c90458a40ae5a09ba3feefbd3d99eee61b0cdbff00d31cffb`。

元の証拠コミット SHA `4248ca24204ed8ede27527191b1a53d9ced1ff5a`（コミット時刻 2026-11-23T11:13:18+09:00）。 Timestamp は報告の再編時刻。

## 5. Focused verification

| Command | Exit code | Result summary |
|---|---:|---|
| `.venv/bin/python -m pytest -q tests/enhancement/enh_e11/g01/contract/test_local_codec.py tests/product/test_cli_contract.py tests/product/test_enh_e4_g07_p03_cli_boundary.py` | 0 | 76 件通過。 |

Python 3.12.16 で 76 passed（P01 69 件、Product 回帰 7 件）。別プロセスで Decoder を import し、`causallearn` と `lingam` がロードされないことを確認した。

| DD / Gate Test | Lifecycle / Layer | 観測結果 | 判定 |
| --- | --- | --- | --- |
| REF01/04 / 07-01/02 | enhancement / contract | Study に五フィールドの参照を保持し、不正な相対キーを拒否した。 | PASS |
| SPEC01–04 / 07-01 | enhancement / contract | JSON/YAML で同じ Study を復元し、不正なキー、版、Method 設定、Estimand、inference、privacy を拒否した。 | PASS |
| MAN01–03 / 07-04 | enhancement / contract | JCS の固定正例 7 件のバイト列とダイジェストが一致した。不正入力を拒否し、4 種のダイジェストを区別した。 | PASS |
| MAN04–06 / 07-07/12 | enhancement / contract | Graph-positive と合成 Graph-negative の Manifest が往復し、不正な参照、成果物構成、理由コード、科学承認状態を拒否した。 | PASS |
| Product CLI | Product / regression | 既存 CLI contract および boundary テストが通過した。 | PASS |

`e11_jcs_golden_vectors.json` は実装前のコミット `b5d2f9cf` で追加され、実行時 SHA-256 は `ba1e4349d3bf2ff6a055eab1f802762164e3ef05ff4873c6cabfdf883dd9eaec`。PREP-02 記録 107 に、固定正例のバイト列が別実装の ECMAScript 参照で再現されたと記録されている。

P02 の実ファイル、FD、公開と Reader、実 Backend の科学検証、P05 の統合、および独立 G01 の受入は保留。合成 Graph-negative は P01 の構造検証に使用した。

## 6. Dependency / handoff state

- Dependencies satisfied: YES
- Next package(s): P02・P03
- Handoff facts: 先行 Package なし。 [Package Execution Status](E11-G01_01_P01__status.md)

## 7. Protected contract / Transition Debt impact

Product 回帰の観測結果は §5 に記録した。DEFERRED_PRODUCT_POLICY_BRIDGE の未完了依存は維持される。

## 8. Known limitations / unresolved observations

P02 以降の実 FS・Backend・統合と独立受入は当時保留。


## 9. Semantic warning

チェックポイントは Package 単位の実装証跡。Fixed Trial Candidate と Gate PASS は別の成果物で確定する。
