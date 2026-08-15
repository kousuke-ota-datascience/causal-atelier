# Template Schema Change History

**Document class:** Historical Reference  
**Self-containment:** SHOULD — 各schema差分を理解できるよう記載するが、通常executionのnormative dependencyにはしない。


## Purpose

このdirectoryは、**エンハンス計画の作成手順ではなく、テンプレートschema自体の変更履歴**を保存する。

通常のenhancement planning / implementation / verificationでは参照不要である。以下の場合に参照する。

- template schemaを更新するとき
- 旧schemaで作成されたenhancement artifactをmigrationするとき
- historical workflow decisionを監査するとき

## Files

- `schema_v2.md` — v2で導入されたschema changes
- `schema_v3.md` — v3で導入されたschema changes
- `schema_v11.md` — canonical filenameをASCII / technical Englishへ統一したschema changes

現行workflowの使い方はroot `README_90.md`をauthorityとする。Change Historyは現行contractをoverrideしない。
