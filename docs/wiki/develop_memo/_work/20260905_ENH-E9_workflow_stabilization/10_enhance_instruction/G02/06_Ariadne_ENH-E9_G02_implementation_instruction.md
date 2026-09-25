# Ariadne ENH-E9 G02 Implementation Instruction

**Document class:** Primary Execution Contract  
**Contract status:** `FROZEN`  
**Execution mode:** `WORK_PACKAGE`  
**Required packages:** `P01, P02, P03`  
**First executable package:** `P01`  
**P00 role:** `PLANNING_ONLY / NON_EXECUTABLE`  
**Entry:** G01 canonical `999_gate_decision = PASS`

## 1. Gate claim

DiscoveryからGraph比較・選択・採用までの既存workflowを、操作結果と比較対象を明確に把握できるinteractionとして成立させる。

## 2. Required residual behavior

- Discovery execution領域に目的が分かるtitleを持たせる。
- Objective / Rationaleの意味をhelp/tooltipで説明する。
- Graph Candidatesのcomponent-local overflowを修正する。
- Graph CandidatesにSelect All / Clearを提供する。selection変更だけを行いadopt/fixを暗黙実行しない。
- Graph Comparisonで現在の比較対象を視覚的に識別できる。
- 比較対象のalgorithmとrelevant persisted parameter（現行PCならalpha等）をauthoritative dataから簡潔に表示する。
- Algorithm Output採用結果を操作したmodal内で確認できる。
- GraphのMermaid markdown source exportを提供する。exportはcurrent authoritative GraphのprojectionでありGraphをmutationしない。

Baselineで既に成立している項目は再実装せずevidence化してよい。

## 3. Protected semantics

FR-035–FR-039、Graph Candidate identity、DRAFT/FIXED GraphVersion mutability、GraphVersion lineage、designated Outcome lineage、comparison/adoption/fix semantics、E8 Stage separationを維持する。

## 4. Forbidden

new discovery algorithm、new Graph lifecycle、FIXED Graph direct mutation、frontendでGraph scientific semantics再計算、Graph lineageと無関係なOutcome override。

## 5. Work Packages

- P01: Discovery copy/help/overflow
- P02: selection/comparison clarity
- P03: adoption feedback/export

P00は計画表でありCoding Agent実行対象ではない。Pxxは本Gate claim/ACを変更できない。全required package complete後にGate-wide Candidate Assemblyを行う。

Package focused verificationではBrowser E2Eを実行しない。Browser E2Eが必要な場合はG02 Independent Verificationの最後のverification itemとしてのみ実行する。
