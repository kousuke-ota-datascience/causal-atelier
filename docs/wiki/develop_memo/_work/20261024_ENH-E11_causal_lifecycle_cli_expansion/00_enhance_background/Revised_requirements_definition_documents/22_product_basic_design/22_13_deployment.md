# 22_13_deployment


---

## 16. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。



### 16.1. Optional DependencyとRuntime Profile

- **Dependency declaration:** `pyproject.toml`にOptional Extraを明示し、`uv.lock`は1つのuniversal resolutionとして扱い、Manifestは実効Profileとライブラリversionを記録する。Lock単独ではBackend/ScienceのPASSを意味しない。
- **Baseline:** DEC08採用対象はUbuntu 24.04 / CPython 3.12.x / x86_64 / CPU。OS・Python patch・BLAS・native ABIが異なれば暗黙保証しない。
- **Current status:** 現行`uv.lock`へDoWhy/EconML/Tigramite等のE11 extrasを追加したことを本書は主張しない。

| Profile | Scope | Backend / key checks | Status |
|---|---|---|---|
| ENV-BASE | Core-only | E9/v2回帰と未導入Method unavailable | Adopted plan; not tested with new lock |
| ENV-DOWHY | E11 DoWhy | Identification/FD-A実効APIと旧CLI回帰 | Adopted plan; not tested with new lock |
| ENV-ECONML | E11 EconML | CATE/DRIV、nuisance、CI availability | Adopted plan; not tested with new lock |
| ENV-TIGRAMITE | E11 temporal | PCMCI family、CI test、Graph endpoints | Adopted plan; not tested with new lock |
| ENV-COMBINED | DoWhy + EconML + Tigramite | 任意の後続相互運用検証。初期Gate必須ではない | DEFERRED / NOT_VERIFIED / combined利用保証なし |
| ENV-RD | RD追加候補（初期4必須Profile外） | Sharp/Fuzzy RD実効API・推論適格性と実際のBackend依存確認 | Conditional / not mandatory until Method-specific availability approved |

- 初期必須のENV-BASE／ENV-DOWHY／ENV-ECONML／ENV-TIGRAMITEは個別fresh isolated venvで`uv lock --check`、`uv sync --locked`、`uv pip check`を実施する。全extrasを同時導入するENV-COMBINEDはmandatory Gateではなく、未検証の組合せを利用可能と保証しない。Runtime profileは実測して固定する。
- 41 MethodごとにBackend/Version/APIを照合し、選択Methodのincompatible/missing状態は**typed unavailable**として結果・Manifestへ反映する。予期せぬfallbackは認めない。
- Effective environment provenanceはSource/Lock SHA、実効installed distribution/version/APIを追跡する。内部CLI分析にSBOMの自動生成・受領者別License承認機能を必要としない。顧客配布時は別途手動審査する。実測なしにbitwise reproducibleを保証しない。

### 16.2. 社内OSS利用の既存遵守義務／顧客配布はScope外

- 現行の実行者は社内データサイエンティストであり、外販・顧客納入・受領者別Delivery・SBOM／Legal Release Workflowは本Enhancementの機能・必須受入対象に含まない。将来の顧客納入は未決であり現時点の実装条件にしない。既存社内のOSSライセンス・利用/複製/再配布規程を守ることは引き続き必要で、これはE11が新たに提供する機能ではない。
- DEC08の記録ではTigramiteのGPLv3-or-later、およびrdrobust PythonのGPL-3.0-onlyが審査対象候補として挙げられている。**本書は個別法務判断をしない**。
- Science PASSと選択MethodのEnvironment PASSは独立。顧客Delivery APPROVALは未確定の将来事業判断であり、E11の状態軸、CLI結果、Manifest、Gateに追加しない。GPLをoptional extraとするだけでライセンス義務が消えるわけではない。

内部Scientific CLIのGateは環境適合・科学的妥当性を独立に判定する。未確定の顧客配布可否はE11の実行状態・Gate判定軸に持ち込まない。

**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-010a`**：API processとWorker processを分離するcurrent deployment boundaryを維持する
- **`NFR-010b`（将来拡張・現行提供対象外）**：Worker restart後の明示的resume/recovery semanticsを定義する


### 16.3. Effective Dependency Baselineの読取証拠（PREP-02）

**固定Source:** `pyproject.toml` blob `7c24ed729be1a31c15a173ef4510aa3ed961d0b9`、`uv.lock` blob `2b83110e86b26b7969fbddf8f98a727370ae19f7`。本節は全ファイルの文字列と宣言を読み取った**STATIC BASELINE**であって`uv sync --locked`の実行記録ではない。

| Check | Actual observed | Contract implication |
| --- | --- | --- |
| Python | `requires-python=">=3.12,<3.13"`、Lockの`requires-python="==3.12.*"` | ENV Profileは3.12系列を前提に実効patch/ABIを別途確認 |
| Existing Extra | `predictive-advanced`（LightGBM/SHAP/LIME）のみ | DEC08採用の`e11-dowhy`、`e11-econml`、`e11-temporal`、conditional`e11-rdd`はProject declarationに未登録 |
| DoWhy package | `pyproject` direct dependency無し、`uv.lock`に`name = "dowhy"`無し | 現行Universal Lockから導入済みと認定不可 |
| EconML package | direct無し、Lock package entry無し | 同上 |
| Tigramite package | direct無し、Lock package entry無し | 同上 |
| rdrobust package | direct無し、Lock package entry無し | ENV-RDは科学Backendの実効適格性を個別検証。外販条件は初期Scope外 |
| Existing ML | Lockにcausal-learn、lightgbm、shap、lime package entriesは存在 | E11全Backendを満たす証拠にならない |

**Disposition (Owner SIM-03/04, 2026-11-21):** DEC08 ENV-BASE/DOWHY/ECONML/TIGRAMITEとMethod別API/科学的検証は維持し、ENV-COMBINED全extras CIは初期必須から削除（未検証の同時導入はsupported扱いしない）。Coding Authorization後、`pyproject.toml`/`uv.lock`を同じChangeで更新し、4必須Profileごとにlock check→sync→API smoke→関連旧v2回帰。SBOM/受領者別法務サービスを内部CLIの必須機能にしない。NFR-034は外販未確定のため現行E11の必須受入から除外し、DEFERRED/FUTUREに保持する（134のStatus訂正）。社内ソフトウェア利用の適法性は既存組織規程に従う。Source/Tests/Lock未変更、実効試験NOT_RUN。
