# Ariadne 初期価値検証版 設計文書 — Revision 2

基本設計、API・インターフェース設計、詳細設計の粒度を分離した文書セット。

## 文書一覧

1. `00_プロダクトコンセプトメモ.md`
   - プロダクト価値、対象利用者、初期境界、設計思想
2. `10_要件定義.md`
   - 業務、シナリオ、機能要件、非機能要件、受入れ条件
3. `21_論理データ設計.md`
   - 正本Entity、ER、属性、Cardinality、状態、導出モデル
4. `22_プロダクト基本設計.md`
   - システム境界、コンポーネント責務、Workspace、画面遷移、論理処理フロー
5. `23_API・インターフェース設計.md`
   - Endpoint、DTO、validation、error model、Scientific Core / CLI契約
6. `30_詳細設計.md`
   - package、class、repository、transaction、worker sequence、例外処理、test

## Revision 1からの主な変更

- `22`からDTOフィールド、Endpoint、package / class、transaction、例外処理を分離
- `22`には画面間で引き渡す論理情報だけを保持
- DTOとAPI契約を`23`へ移動
- class、repository、worker claim、transaction、compensationを`30`へ移動
- 上位3文書の関連文書参照を6文書構成へ更新
