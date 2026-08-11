# Architecture Discovery Prompt

> **Document class:** Planning / Operator Artifact  
> **Self-containment:** MUST for own responsibility — instruction / decision / decompositionの意味を本文内に持ち、source code / designはfact evidenceとして参照する。


対象enhancement: `{{ENHANCE_ID}}`
対象branch / commit: `{{BRANCH_OR_COMMIT}}`

コードと既存設計を調査し、**実装変更は行わず**、現在architectureの事実を特定してください。

最低限確認:

1. runtime entrypoints
2. execution / request lifecycle
3. canonical write paths
4. canonical read paths
5. ownership / authority boundaries
6. persistence tables / models / migrations
7. lineage / result / artifact relations if applicable
8. legacy or duplicate paths and reachability
9. UI/API/background-job divergence if applicable
10. current tests that encode behavior

出力では`Fact / Inference / Unknown`を分離してください。
推測でauthorityを補完しないでください。
最後に、target decisionが必要な論点を列挙してください。
