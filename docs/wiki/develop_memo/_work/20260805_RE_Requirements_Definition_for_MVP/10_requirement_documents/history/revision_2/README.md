# Ariadne 初期価値検証版 設計文書 — Review Revision 1

レビュー指摘を反映した4文書を収録する。

- `00_プロダクトコンセプトメモ.md`
- `10_要件定義.md`
- `21_論理データ設計.md`
- `22_プロダクト基本設計.md`

主な反映内容:

- 完成後のプロダクトを初見で理解できる自己完結的な記述へ修正
- Research Contextをフラットに保持し、任意relationからProjectionを生成する方針を明記
- Algorithm要件を完成後のプロダクト仕様として自己完結化
- CLIとWeb/APIのIdentity分離をインターフェース要件の粒度で記述
- ER図、Cardinality、FK、型、NOT NULL、制約を追加
- Comparison / Lineageの導出ロジックを追加
- Execution status、Graph Version status、Scientific statusの意味を分離
- 各システムコンポーネントの存在目的と責務を追加
- 画面間遷移とNavigation / Command / Query / Scientific DTOを追加
- 全文書の見出し階層を統一
