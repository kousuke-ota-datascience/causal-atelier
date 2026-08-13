# Ariadne ENH-E7 G01 Implementation Instruction — Gate Coding Contract

**文書種別:** Primary Execution Contract  
**Self-containment:** MUST（Gate implementation semanticsについて本文内で完結）  
**Project:** Ariadne  
**Enhancement:** ENH-E7  
**Active Gate:** G01  
**Branch:** `feature/ariadne_mvp_e7`  
**Baseline:** `REQUIRES_LOCAL_VERIFICATION`  
**Contract status:** DRAFT_NOT_FROZEN  
**Execution Mode:** WORK_PACKAGE  
**Current State:** `docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/Current_State_Control_Sheet.md`

## 1. Gate定義 / Acceptance claim

### Gate objective

canonical Project Management routingを確立し、Project lifecycle / Research Context / Data・Analysis View / Results・Lineageを明示的Project-local responsibilityへ移設する。domain semanticsは変更しない。

### PASSで成立するcontract claim

Projectの作成・選択・管理が独立したURL-authoritative Project Management surfaceとして成立し、downstreamがProject route、section ownership、analysis input resource ownershipへ安全に依存できる。

### Downstreamが利用できる結果

G02はselected Project routing、Data-owned Analysis View management、Results/Lineage ownership、安定したProject Management return targetへ依存できる。

### この範囲を1 Gateとして扱う理由

このGateのProduct claimは、列挙されたresponsibilityが一体として機能したときに初めてdownstream-relyableになる。
実装量やfile数はWork Packageで分割し、Gate semantic claim自体は分割しない。

## 2. Effective implementation context

- ENH-E7はProject resource managementとAnalysis executionをTop-level IAで分離する。
- 本contractに明記しないdomain semanticsは維持する。
- browser history / direct-linkはProduct semanticsである。
- package completionはGate PASSではない。

## 3. Execution Mode

`WORK_PACKAGE`を使用する。
P00はHuman/operator用orchestration traceabilityであり、Coding Agentは仕様補完目的で読まない。

## 4. 必須implementation semantics

- AC-G01-01: `/projects`がcanonical Project List surfaceである。
- AC-G01-02: `/projects/new`がcanonical Project Register surfaceである。
- AC-G01-03: Project作成後`/projects/<id>/overview`へ遷移する。
- AC-G01-04: `/projects/<id>`がduplicate historyなしで`/overview`へnormalizeする。
- AC-G01-05: Overview / Context / Data / Results local navigationとURLが一致する。
- AC-G01-06: Project metadataとDataset/Analysis View managementが分離される。
- AC-G01-07: Project ArchiveがOverviewに属する。
- AC-G01-08: Analysis View lifecycleがDataに属する。
- AC-G01-09: Analysis ViewがFamily横断inputとして利用可能である。
- AC-G01-10: Results / Lineageのexisting cross-analysis機能が維持される。
- AC-G01-11: Project routeのdirect link/reload/Back/Forwardが成立する。
- AC-G01-12: existing Project/domain semanticsとENH-E6 protected Analysis semanticsがregressionしない。

## 5. Allowed scope

- 当該Gateに必要なfrontend routing / navigation / DOM / styles / presentation / state code。
- frozen 07を満たすためのfocused automated testとrepository-standard Browser E2E。
- existing responsibilityを特定するためのsource discovery。
- domain semanticsを変えないminimal refactoring。

## 6. Explicitly prohibited scope

- UI taxonomyを埋めるための新backend analysis semantics。
- persistence/schema redesign。
- unrelated framework migration / design-system rewrite。
- implementationに合わせたAcceptance Criteria変更。
- entry criteria未充足のnext Gate実装。
- protected upstream contractの破壊。

## 7. Protected passed-Gate contract

| Gate | Protected semantic | 許可するinteraction | Mandatory regression |
|---|---|---|---|
| ENH-E6 G01 | ENH-E6 G01 PASS candidate `575cdd139aea09d4f19b46ab6a6d38545f645c71` が確立したcanonical Analysis Family/Stage navigation / transition semantics。 | presentation/routing integrationのみ | frozen 07のprotected-regression Test Item |

## 8. Transition Debt

Intentional temporary product debtは計画しない。
legacy URL compatibilityはtemporary debtではなくProduct requirementとして扱う。

## 9. Schema / migration / API方針

```text
Persistence migration: NONE EXPECTED
API contract change: NONE EXPECTED
Backend domain semantic change: NOT AUTHORIZED
```

これらが必要とsource factで判明した場合は、affected packageを
`PACKAGE_BLOCKED_CONTRACT_CHANGE_REQUIRED`として停止する。

## 10. Automated test obligation

- 002: project_route_contract（FRONTEND_CONTRACT）
- 003: project_surface_ownership（FRONTEND_CONTRACT）
- 004: project_domain_regression（API_INTEGRATION/UNIT_DOMAIN）
- 005: project_browser_journey（BROWSER_E2E）
- 006: protected_analysis_regression（FRONTEND_CONTRACT）

詳細correctnessは可能な限りlowest deterministic layerで検証する。
Browser E2Eは07のcritical cross-layer journeyに限定する。

## 11. Candidate Assembly条件

- required Pxxがすべて`PACKAGE_COMPLETE`。
- Gate-wide integration self-check PASS。
- protected regression self-check PASS。
- candidate-affecting unresolved changeがNONE。
- Fixed Trial Candidate full SHA固定。
- Implementation Completion Report作成。

## 12. Coding-side prohibited work

- Gate PASS/FAIL判定。
- failure回避目的の07変更。
- Acceptance Criteria変更。
- unapproved passed-Gate semantic変更。
- package scope外convenience変更。

## 13. 必須output

各package:
- package execution status report
- implementation checkpoint report
- checkpoint full SHA

Candidate Assembly:
- Fixed Trial Candidate full SHA
- implementation completion report
- Gate-local implementation detail report

## 14. External reference policy

本06はHuman/operator向けtraceabilityとGate semantic authorityである。
Coding Agentはassigned Pxxをnormative contractとし、本06を仕様補完目的で読まない。

## 15. Stop condition

Coding sideは `READY_FOR_TEST` または明示的 `BLOCKED_*` で停止する。
Gate PASSは宣言しない。
