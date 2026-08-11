# Domain Ownership / Lifecycle

> **Non-normative preflight finding.** 実装・検証仕様は正本文書および06/Pxx/07へ収束させる。

## 1. Scope

Project/ResearchContextVersion ownershipとStageExecution cancel transitionのdocument driftを整理する。

## 2. Audit facts

| ID | Alignment | Statement | Audit finding | Source evidence |
|---|---|---|---|---|
| FR-002 | MISMATCH | Projectにtopic、objective、decision contextおよびmemoを保持できる | Project entity/API has topic/objective/memo but no decision_context; decision_context belongs to ResearchContextVersion. | src/ariadne/product/domain/project.py; product/persistence/orm_models.py; interfaces/web_api/routers/projects.py |
| D10-004 | MISMATCH | Stage state diagram is complete | Document omits CANCELLED transitions that implementation supports from PENDING/READY/RUNNING. | product/domain/stage_execution.py; persistence/orm_models.py |

## 3. Confirmed remediation

D1。current implementationを正本として文書を修正する。

| Decision Item | Decision | Substatement | Delivery | TD Ref |
|---|---|---|---|---|
| FR-002 | **D1** | Project / ResearchContextVersion responsibility ownership | BASELINE |  |
| D10-004 | **D1** | StageExecution CANCELLED transitions | BASELINE |  |

## 4. Downstream impact

- D1: current contract記述を10/21/22/23/30へ反映する。
- D2: ENH-E5 targetとして必要なdesign/validation/API/UI/test seamを正本文書へ具体化し、NFR-019 PASS後に06/Pxx・07へ収束する。
- D3: current targetから分離し、`90_technical_debt_and_future_enhancements.md`へtraceする。
