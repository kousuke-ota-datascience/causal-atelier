# Ariadne ENH-E9 G01 Verification Contract

**Document class:** Primary Execution Contract  
**Verification contract status:** `DRAFT_NOT_FROZEN`

## 1. Acceptance authority

この文書がFROZENになった後、G01 Independent VerificationのAcceptance Criteria authorityとなる。

## 2. Draft Acceptance Criteria

### AC-01 Saved Analysis View observability

Baselineでresidualと確認された場合、利用者はselected/saved Analysis Viewの内容を既存resource authorityから確認できる。表示のためにAnalysis Viewを更新・複製しない。

### AC-02 Active Research Context meaning

Baselineでresidualと確認された場合、Active Research Context inputの意味をUI上で理解できる説明を提供する。tooltip/help presentationはresource ownershipを変更しない。

### AC-03 Context regression

- Current ProjectはAnalysis route `project_id` authority / read-onlyを維持
- Research Context / Dataset Version / Analysis ViewはProject-scoped existing resourceから選択
- incompatible Analysis View invalidation semanticsを維持
- context不足を理由にFamily/Stage routeを書き換えない

### AC-04 Non-regression

new Analysis View schema/API/persistent resourceを導入しない。

## 3. Primary test layers

- frontend unit/integration: AC-01/02/03
- existing contract/architecture tests: AC-03/04
- Browser E2E: G01単独でblockingにするかはfreeze時に判断。単純tooltip presenceだけをE2E primary proofにしない。

## 4. Decision

全blocking AC PASS -> G01 PASS。Product correctnessを判定不能なenvironment/harness failureはFAILへ読み替えずBLOCKEDとして分類する。
