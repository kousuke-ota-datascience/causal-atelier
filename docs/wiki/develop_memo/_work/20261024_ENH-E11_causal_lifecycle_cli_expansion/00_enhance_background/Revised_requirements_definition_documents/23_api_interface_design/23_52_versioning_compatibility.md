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


## 98. RD-04：IF契約の要求起源・Trace

**Status:** `RD04_INTERFACE_CONSTRAINT_MIGRATED / OWNER_CONTENT_REVIEW_PENDING`。抽象化前のAPI／CLI／Navigationのwire・resource・state契約を失わないための移管記録。現在の実効Implementationを確認したことを意味しない。

### 98.1. FR-177（SPLIT）

- 旧要件に含まれるIF固有情報：UI / IA再編だけを理由に既存API contract、persistence schema、backend analysis/domain semanticsを変更しない
- RDの要求核／Legacy Trace：UI・IA再編によって既存API契約・永続化Schema・分析の意味を変更しない
- `FR-177`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.2. FR-113（SPLIT）

- 旧要件に含まれるIF固有情報：HTTP APIをversioned pathとversioned payloadで提供する
- RDの要求核／Legacy Trace：互換性を管理した版付きAPIを提供できる
- `FR-113`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../95_rd04_fr_application_review.md)

### 98.3. NFR-013（SPLIT）

- 旧要件に含まれるIF固有情報：schema versionはversioned Spec/Plan/payload/descriptor等のcontract boundaryで識別し、全persistent Result/Artifact entityへgeneric schema_version fieldを要求しない
- RDの要求核／Legacy Trace：変化するデータ契約を識別し後方互換を制御できる
- `NFR-013`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)

### 98.4. NFR-014（SPLIT）

- 旧要件に含まれるIF固有情報：`causal-analysis-spec/2`の正規contractおよび保存済みCausal Resultをschema versionに従って読取可能に保つ
- RDの要求核／Legacy Trace：既存v2の因果分析仕様と保存済み結果を継続して読み取れる
- `NFR-014`；Status=`ACTIVE`；Implementation=`IMPLEMENTED`；[RD-04逐条レビュー](../96_rd04_nfr_ar_application_review.md)
