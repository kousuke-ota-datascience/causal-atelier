# 23_00_overall_IF

**Status:** `RD02_STRUCTURAL_WORKING_COPY / E11_NOT_PUBLISHED`. Original source section numbering retained; document numbering is by interface responsibility.  
**Source blob:** `131467f02222f105a49e6dfdbcec0f49cadb0f41`.

---

## 1. 文書の設計粒度

本書は、Ariadneを構成する**interface contract**を、実装内部ではなく利用者・component間の境界として定義する。

本書で確定する事項:

- Browser Navigation Context / route contract
- Web API endpoint、request / response DTO、resource boundary
- Authentication / AuthorizationおよびProject境界
- Worker / Runtime内部interface
- CLI / Python Library interface
- validation / error contract
- idempotency contract
- contract versioning
- interface間で引き渡すidentifier、state、payloadの責務境界

各interface contractでは、該当する範囲で次を明示する。

1. interfaceの目的とauthority
2. endpoint / route / command / callable identity
3. input / request contract
4. output / response contract
5. authentication / authorizationまたはscope boundary
6. state / lifecycle上のprecondition
7. validation / error semantics
8. idempotency / versioning semantics
9. 他interfaceへ引き渡すcontextと、引き渡してはならないstate

本書はDB Entityの属性定義、ORM mapping、class内部構造、algorithm実装詳細を定義しない。それらは`21_logical_data_design.md`、`30_detailed_design.md`またはScientific Core側の詳細contractをauthorityとする。

`Navigation Context`はWeb Appのbrowser interface contractであり、`Web API Endpoint`と同じ種類の設計項目ではない。このため本書では、interface種別を上位階層に置き、Browser / Web API / Runtime / CLIを同一粒度で整理する。

## 2. Interface構成と責務境界

本書のinterface architectureは次のとおりである。

```text
Ariadne Interface Contracts
├─ Browser Navigation Interface
│  └─ route / Navigation Context / browser restoration
├─ Web API Interface
│  ├─ Project / Research Context
│  ├─ Dataset / Analysis View
│  ├─ Analysis Specification
│  ├─ Family-specific analytical interface
│  ├─ Execution
│  ├─ Result / Comparison / Lineage
│  ├─ Annotation / Artifact
│  └─ Frontend Support API
├─ Worker / Runtime Internal Interface
├─ CLI / Library Interface
└─ Cross-cutting Contract Policy
   ├─ Error Model
   ├─ Idempotency
   ├─ Contract Versioning
   └─ Forbidden Interface
```

| Interface種別 | 主な利用者 | Authority / 責務 | 非責務 |
| --- | --- | --- | --- |
| Browser Navigation | Web App / Browser | Project/Analysis route、Navigation Context、deep link、reload/Back/Forward | Domain Resource persistence、Execution lifecycle |
| Web API | Web App / external client | Project-scoped resource/query/command contract | Browser history、UI-local navigation state |
| Worker / Runtime Internal | Worker / Application runtime | Execution claim、lease、Stage runtime、Runner boundary | Public browser/API route |
| CLI / Library | headless user / backend use case | headless scientific execution | Browser navigation metadataへの依存 |
| Cross-cutting policy | 上記すべて | error、idempotency、versioning、禁止境界 | 個別domain operationの意味 |

## 90. この文書種別の目的・責務・規範性

- **目的:** Browser/Web API/Worker/CLI/Portの利用者と提供者の間の互換性契約を、観測可能な入出力・検証・失敗として定義する。
- **含む:** Command/operation、request/response、schema version、status/error、backward compatibility、serialization、path/security、timeout/availability、contract test。
- **含まない:** Application内部のclass layout、DB storage実装、推定器の統計手順。
- **E11境界:** 追加はlocal CLIとScientific Port/Artifact Interfaceのみ。既存`/api/v1`に新E11 endpointを追加しない。旧v2 spec/read-backを暗黙更新しない。

