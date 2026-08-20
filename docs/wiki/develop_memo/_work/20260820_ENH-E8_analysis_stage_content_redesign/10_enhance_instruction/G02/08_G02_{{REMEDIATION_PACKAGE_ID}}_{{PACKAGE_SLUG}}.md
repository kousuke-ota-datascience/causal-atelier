# G02 Remediation Work Package Template

- Document class: Remediation Work Package
- Status: `TEMPLATE`
- Gate: `G02`
- Remediation Package ID: `{{REMEDIATION_PACKAGE_ID}}`
- Package slug: `{{PACKAGE_SLUG}}`

## 目的

formal Gate FAILで特定されたfailureを、frozen 06/07の意味を変更せず修正する。

## Input

- failed candidate SHA
- failing AC / Test Item
- exact failure evidence
- affected implementation area

## Required change

{{REMEDIATION_SCOPE}}

## Forbidden

- frozen Acceptance Criteriaのsilent変更
- unrelated refactor
- new requirement/capability
- contract ambiguityの推測補完

## Exit

focused verificationを実行しpackage checkpointを記録する。Gate PASSは宣言しない。
