# 23_52_versioning_compatibility

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

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
