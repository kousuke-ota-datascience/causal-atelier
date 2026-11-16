# 22_13_deployment


---

## 16. Deployment

現行実装ではFastAPI Web API、polling Worker、Product persistence DB、ArtifactStore Port（default LocalArtifactStore）が分離されている。Family / Navigation Stage導入のために別runtime execution serviceを新設しない。



### 16.1. Optional DependencyとRuntime Profile

- **Dependency declaration:** `pyproject.toml`にOptional Extraを明示し、`uv.lock`は1つのuniversal resolutionとして扱い、Manifestは実効Profileとライブラリversionを記録する。Lock単独ではBackend/Science/LegalのPASSを意味しない。
- **Baseline:** DEC08採用対象はUbuntu 24.04 / CPython 3.12.x / x86_64 / CPU。OS・Python patch・BLAS・native ABIが異なれば暗黙保証しない。
- **Current status:** 現行`uv.lock`へDoWhy/EconML/Tigramite等のE11 extrasを追加したことを本書は主張しない。

| Profile | Scope | Backend / key checks | Status |
|---|---|---|---|
| ENV-BASE | Core-only | E9/v2回帰と未導入Method unavailable | Adopted plan; not tested with new lock |
| ENV-DOWHY | E11 DoWhy | Identification/FD-A実効APIと旧CLI回帰 | Adopted plan; not tested with new lock |
| ENV-ECONML | E11 EconML | CATE/DRIV、nuisance、CI availability | Adopted plan; not tested with new lock |
| ENV-TIGRAMITE | E11 temporal | PCMCI family、CI test、Graph endpoints | Adopted plan; not tested with new lock |
| ENV-COMBINED | DoWhy + EconML + Tigramite | Combined conflict・legacy・Science | Adopted plan; not tested with new lock |
| ENV-RD | RD追加候補（初期5件外） | Sharp/Fuzzy RD実効API、推論、GPL顧客配布 | Conditional / not automatically approved for delivery |

- 各Profileはfresh isolated venvで`uv lock --check`、`uv sync --locked`、`uv pip check`等の適合検証を行い、`--frozen`をlock stale検証と取り違えない。Runtimeでは`--no-dev`等の環境要件を明記する。
- 41 MethodごとにBackend/Version/APIを照合し、選択Methodのincompatible/missing状態は**typed unavailable**として結果・Manifestへ反映する。予期せぬfallbackは認めない。
- Effective environment provenanceとSBOM/LicenseはRelease候補のSource SHA/Lock SHAおよび実効wheel/sourceをTraceする。実測なしにbitwise reproducibleを保証しない。

### 16.2. 配布・OSSライセンスの設計境界

- Internal Science使用、顧客へのwheel/container/sourceのSI納入、クラウドサービス提供で法的評価の対象は異なる。License種別・実配布Artifact・受領者・結合・通知・ソース提供・契約条件を法務とOwnerが審査する。
- DEC08の記録ではTigramiteのGPLv3-or-later、およびrdrobust PythonのGPL-3.0-onlyが審査対象候補として挙げられている。**本書は個別法務判断をしない**。
- Mandatory Science PASS／Environment PASS／Legal Delivery APPROVALは独立状態。GPLをoptional extrasにすることだけでは顧客配布の許可条件を満たさない。

環境適合・科学的妥当性・顧客配布の許可は独立判定とし、いずれかのPASSから別のPASSを推定しない。

**当該機能に適用する設計制約（関連Requirement）**

- **`NFR-010a`**：API processとWorker processを分離するcurrent deployment boundaryを維持する
- **`NFR-010b`（将来拡張・現行提供対象外）**：Worker restart後の明示的resume/recovery semanticsを定義する
