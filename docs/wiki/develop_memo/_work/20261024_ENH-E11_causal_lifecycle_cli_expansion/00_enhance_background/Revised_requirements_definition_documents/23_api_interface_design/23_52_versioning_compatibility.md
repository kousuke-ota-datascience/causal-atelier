# 23_52_versioning_compatibility


---

## 8. Cross-cutting Contract Policy

### 8.3 Contract Versioning

Version axis:

- URL major: `/api/v1`
- Analysis Specification envelope: `analysis-specification/1`
- Family spec: `family_spec_schema_version`
- Execution Plan: `execution-plan/1`
- runtime Stage identity: `namespace / name / version`
- Navigation metadata: `analysis-navigation/1`

Navigation Stageのlabel/order変更をruntime `StageType.version`変更と連動させない。

破壊的persistent/scientific contract変更は新schema versionとして扱う。Presentation-only metadata変更とscientific snapshot versioningを同一version axisへ混在させない。

### 8.4 禁止interface

次のinterfaceを導入しない。

1. `AnalysisSpecification.current_family`
2. `AnalysisSpecification.navigation_stage`
3. `Execution.navigation_stage`
4. `StageExecution.navigation_stage`
5. Navigation Stage IDを`StageType`として流用するcontract
6. Navigation Stageごとの機械的なExecution endpoint増設
7. public `claim_token` resource/API
8. Family/Stage route changeをruntime lifecycle eventへ変換するevent contract
9. Findings / Model ManagementというUI名だけを理由とする重複Result/Artifact/Annotation resource
10. Navigation metadataをscientific generic `SchemaRegistry`へ登録するinterface
11. persisted `EXECUTE` role / system Operator roleをcurrent project authorizationへ無根拠に追加するinterface
12. Analysis Context専用backend resource/APIをUI都合だけで新設するinterface
13. Project route stateをAnalysis navigation stateへ混在させるinterface
14. UI Stage配置を理由にExploratory/Predictive/Causalのbackend operation/APIを増設するinterface

**当該Interfaceの追加契約（関連Requirement）**

- **`FR-177`**：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- **`FR-113`**：HTTP APIをversioned pathとversioned payloadで提供する
- **`NFR-013`**：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- **`NFR-014`**：`causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ
