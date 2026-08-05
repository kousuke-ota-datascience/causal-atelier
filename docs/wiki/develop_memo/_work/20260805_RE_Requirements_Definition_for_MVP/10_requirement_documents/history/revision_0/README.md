# Ariadne 設計成果物ドラフト

作成日: 2026-08-05

## ファイル

1. `00_プロダクトコンセプトメモ.md`
   - プロダクト定義、対象利用者、価値、設計思想、対象範囲

2. `10_要件定義.md`
   - 業務一覧、E2E/AS/CRシナリオ、機能要件、対象アルゴリズム、インターフェース要件、非機能要件

3. `21_論理データ設計.md`
   - 最小論理Entity、関係、Version/Execution/Resultの区別、Comparisonの扱い

4. `22_プロダクト基本設計.md`
   - システム構成、モジュール、Web画面、API/CLI/Worker責務、E2Eフロー、実装優先順位

## 主な設計判断

- Research Context―Experiment―Execution―Result―Interpretationの追跡を維持する
- Question Treeは初期要件にしない
- Research Contextはフラット保持し、任意Relationを許容する
- Comparisonは初期正本EntityではなくProjectionとする
- Identification不能・推定不能を正式な分析Resultとする
- Web/APIとCLIで科学計算を共通化するが、Execution IdentityとControl Plane責務は分離する
- 売上改善をGolden Pathとし、退職者抑制・エンゲージメント向上をTransfer Caseとする

## 状態

討議用ドラフト。正本仕様ではない。
