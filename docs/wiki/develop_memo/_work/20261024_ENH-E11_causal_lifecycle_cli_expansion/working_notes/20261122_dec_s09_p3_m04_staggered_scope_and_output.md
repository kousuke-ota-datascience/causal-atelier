# DEC-S09-P3M04-01 — Staggered DiD初期ScopeとOutput契約のOwner判断（OPEN）

**作成日:** 2026-11-22  
**状態:** `OWNER_DECISION_REQUIRED / NOT_ADOPTED / S10_NOT_FROZEN / S11_CODING_NOT_AUTHORIZED`。本メモだけでは本番要件・06/07・Method JSON Schemaを変更しない。  
**責務:** S09 authorが確認した科学的対象と現行Method profileの不一致をOwnerへ明示し、実装者による無断既定値選択を防ぐ。

## 1. 既知の事実と証拠

1. Owner採用済み `working_notes/20261116_sr04_dec05_quasi_experimental_seven_methods_estimator_inference_decisions.md` のDEC-05-1に、**P3-M04 DiDのInitial target = 2×2 ATT**と記載。staggered `ATT(g,t)`は**別Estimator契約**であり、異質・時差導入データに対して単一TWFE係数を一般ATTとしない。DEC-05-2ではP3-M05 Event Studyを別にcohort×time ATTのevent-time集約として定義する。
2. 現行 `23_api_interface_design/schema_drafts/method_profiles/e11_p3_m04_method_config_v1.schema.json` は `design_variant`に `DID_2X2` と `STAGGERED`を**いずれもSchema上受理**。
3. 現行 `.../e11_p3_m04_output_profile_v1.schema.json` は `positive_artifacts = ["result.json"]` のみ。公共Effect Resultのpointは**単一scalar**。個別の`ATT(g,t)`群、対象cohort×period、aggregation weight、supported cells、推論・reference/lineageのtyped outputはこのMethodには定義されていない。
4. `G07/06_G07_P01_did_event.md` は2×2 ATTとstaggered adoptionを**別Design/Estimatorとして**検証すると指示し、単一TWFE流用を禁止。ただしSTAGGEREDの現行target aggregation、最小成果物、covariance、独立Refと支持域は閉じていない。
5. 前段S09でP3-M05 Event Studyは `event_time_effects.json`、P3-M06 ITSは `its_components.json`、P3-M12 SCMは `scm_gaps.json` をそれぞれ内部schema+実装指示へ反映済み。これらのArtifactをP3-M04 STAGGEREDの科学的成果物に暗黙流用することは別Estimand/Methodを誤認させる。

## 2. 問題構造

`STAGGERED`を正例として実行するなら、Estimatorは一般に一つの普遍的なscalar ATTを返すものではない。cohort×timeの複数 `ATT(g,t)` か、明示的な固定population/weightに対する事前登録済みscalar aggregationなどを含む具体的Estimand/Output/CI契約が必要となる。現在の `positive_artifacts=["result.json"]` を無条件に成功契約とすると、動的/異質効果が消失するか、無断TWFE/任意平均が導入される恐れがある。一方、現行のOwner initial targetを2×2に限定した場合、`STAGGERED`がSchema上validでも科学的に実行可能と宣言してはならない。

これは単純なJSON Schema修正ではなく、**初期提供Scope/Estimand family/MethodごとのScience 07**に影響する判断である。

## 3. Ownerへの採用案

### A案（推奨） — 初期P3-M04は2×2 ATTのみ、STAGGEREDはDEFERRED／fail closed

- P3-M04の初期**実行可能**variantは `DID_2X2`のみ。Scalar `result.json` で、DGP-012、群・時点・unit cluster、parallel trendsとsource/Method/Design検証を要求。
- `STAGGERED`は未来の能力として`DEFERRED / SCIENCE_CONTRACT_NOT_AVAILABLE`のようなtyped capabilityで拒否。Schemaのsyntax上の受理と、Estimatorのscientific availabilityを分離（採用時に必要ならConfig profileを`DID_2X2`限定へ狭めてもよい）。`STAGGERED`の要求を `DID_2X2`に黙示fallbackしない。
- P3-M05 Event StudyをP3-M04 STAGGEREDの代用にしない。P3-M04のMethod IDは維持、全41 Method/10 UCの数は変更しない。
- G07 06/P01/P03/07・G10 Method matrix・Output Profile/Method Registry・23_42等でこのcapability境界と負例を一致させる。将来のSTAGGERED解放には別Estimator/Output/Inference/ReferenceのOwner/独立承認を要求。
- 理由: DEC-05-1の明示 `Initial target=2×2 ATT` に最も忠実で、追加科学Scope/暗黙集約を生じない。

### B案 — P3-M04 STAGGEREDも初期提供する

- P3-M04で `STAGGERED`を正式な正例とする代わりに、group-time `ATT(g,t)`のtyped vector Artifact（案: `did_group_time_effects.json`）、cohort×period support、control/risk-set、reference period、事前固定weightを別のMethod科学契約として規定。
- Unweighted TWFEへの置換は禁止。集約scalarを公開するなら、対象母集団・cohort/time weight・reference targetを**別途明示承認**し、そうでなければ `result.json.point.availability=NOT_AVAILABLE` + typed multi-cell Artifact。
- cluster/trajectory correlation・pointwise/同時CI・DGP/NEG/REF/実効Backendの独立証拠を追加。G07とG10のScope・06/07/Profiles/Schema/Testを改訂し、該当GateをFreeze対象とする。
- 理由: 現行Configの二variant実行想定と整合するが、A案より科学/開発/検証範囲が大きい。Method ID数を変えずともInitial Capabilityの拡張になる。

**不適切な第三案:** `STAGGERED`を黙示的にTWFE scalar、全cohort無条件平均、あるいはP3-M05 event-time vectorへ自動置換する案は科学的に異なるため推奨しない。

## 4. 判断後の自律作業

- Owner **A** 採用: 初期2×2正例とstaggered Deferred負例を含むMethod-by-Method dispatch、06/Pxx/07、Stock IF/DD、profile/crosswalk、G10を即時改訂し、S09独立Review待ちへ進める。
- Owner **B** 採用: vector/aggregation/CIの固有science profileとbackend capabilityは不明な値を補完せず追加の小決定に分解。承認済み部分から下書き・Scope配分・文書を更新。
- どちらもS09 Author修正 ≠ S09 independent PASS、B02 validator ≠ Backend/Science PASS、S10 Freeze/S11 Coding Authorizationは別。

**Ownerが決めること:** **DEC-S09-P3M04-01 = A あるいは B**。現時点の採用状態はOPEN。
