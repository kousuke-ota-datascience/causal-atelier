# G02 P01 — Analysis Stage Presentation Framework

- Status: `FROZEN`
**Assigned Coding Agent normative context: この文書のみ。**

## Objective

canonical navigation/backend semanticsを変更せず、Stage-specific surfaceを成立させる共通frontend presentation mechanismを整備する。

## Required changes

1. current canonical StageをStage Contentsのprimary heading/identityとしてrenderする。
2. 日本語の目的説明とoptional visual groupingを表現できるpresentation metadataを用意する。
3. Causal sidebar groupingを実装する場合、group headerはnon-interactive / non-routableとし、`active` / selected Stage stateを持たせない。
4. vertical semantic-section layout primitiveを整備し、独立sectionをpage-level horizontal compositionへ強制しない。
5. canonical Family/Stage route/catalog resolutionとexisting history behaviorを維持する。

## Likely files

- `frontend/app.js`
- `frontend/analysis_presentation.js`
- `frontend/index.html`
- `frontend/styles.css`
- presentation metadata module

## Forbidden

- new stage slug / backend navigation catalog item
- new API/DB/runtime StageType
- scientific/backend semantic change
- P02/P03で扱うCausal/Predictive Stage-specific contentをP01で先回り実装すること

## Focused self-check

- 全existing Family/Stage routeでheading resolutionが正しい
- sidebar groupがroute authorityでない
- navigation regressionがない

package checkpointのみ記録し、Gate PASSを宣言しない。
