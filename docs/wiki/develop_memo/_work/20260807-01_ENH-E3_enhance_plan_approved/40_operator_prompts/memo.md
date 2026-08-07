以下の実装指示書を唯一の作業指示として、実装を行うこと。

`docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/00_enhance_plan_documents/06b_Ariadne_ENH-E3_実装再開指示書.md`

実装範囲、作業順序、禁止事項、完了条件、報告方法はすべて当該指示書に従うこと。
当該指示書から明示的に参照を指示されていない旧実装指示書、要件定義書、設計書を作業判断のために参照しないこと。


-----
以下のテスト指示書を唯一の作業指示として、テストおよび監査を行うこと。

`docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`

今回のテスト対象となる実装完了報告書は以下である。

`docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G3_001_implementation_completion_report.md`

テスト・監査範囲、作業順序、禁止事項、完了条件、Gate判定、報告方法はすべてテスト指示書に従うこと。
当該指示書から明示的に参照を指示されていない旧実装指示書、旧テスト指示書、要件定義書、設計書を作業判断のために参照しないこと。


-----
G3 001 のテスト結果が帰ってきた。FAILであったので再実装のこと。
docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/G3_001_001_predictive_spec_contract.md



-----
G3 002 の実装が完了した。下記報告書が作成されている

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/G3_002_implementation_completion_report.md

引き続き。以下のテスト指示書を唯一の作業指示として、テストおよび監査を行うこと。

- `docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/00_enhance_plan_documents/07b_Ariadne_ENH-E3_テスト指示書.md`

-----
G3のテストが完了した。テスト報告書は下記ドキュメントである。

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/G3_002_*.md

問題ないことを確認したあと、G4の開発を開始せよ

-----
G4 001 の実装が完了した。下記報告書が作成されている

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G4_001_implementation_completion_report.md

テストを実施せよ

-----
G4 001 のテストが完了した。FAILである。再実装またはテストコード再作成のこと

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/
    - G4_001_*.md

-----
G4 002 の実装が完了した。下記報告書が作成されている

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G4_002_implementation_completion_report

テストを実施せよ

-----
G4 002 のテストが完了した。FAILである。再実装のこと

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/
    - G4_002_*.md

-----
G4 003 の実装が完了した
- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G4_003_implementation_completion_report.md

-----
G4のテストが完了した。テスト報告書は下記ドキュメントである。

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/G4_003_*.md

問題ないことを確認したあと、G5の開発を開始せよ

-----
G5 001 の実装が完了した

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G5_001_implementation_completion_report.md

テストを開始せよ


-----

G5 002 のテストが完了した。FAIL。再実装を実施せよ
- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/
    - G5_002_999_gate_decision.md


-----
G5 003 の実装が完了した。.dockerignoreへの1行追加のみである。

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G5_003_implementation_completion_report.md

G5_002 のテストでFAILとなった原因となっていたのが

```
| 004 | predictive_browser_e2e | BLOCKED | [G5_002_004_predictive_browser_e2e.md](G5_002_004_predictive_browser_e2e.md) |
```

のみであるため、当該テストのみ実施し、PASSであれば全PASSとして良い。
ただし「G5_002 でのFAIL原因がテスト項目004のみであったため、G5_003 のテストでは当該項目のみ実施した」旨をG5-
  003_999のテストレポートに明記すること

-----
G5 003 のテストが完了した。PASS。内容を確認し、問題なければG6の実装を実施せよ

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/
    - G5_003_999_gate_decision.md

-----
G6 001 の実装が完了した。テストを実施せよ
- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G6_001_implementation_completion_report.md

-----
G6 001 のテストが完了した。FAIL。確認し再実装せよ

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/30_test_report/
    - G6_001_999_gate_decision.md
-----
G6 002 の実装が完了した。テストを実施せよ

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G6_002_implementation_completion_report.md
-----
G6 002 の実装が完了した。テストを実施せよ

- docs/wiki/develop_memo/_work/20260807-01_ENH-E3_enhance_plan_approved/20_implementation_reports/
    - G6_002_implementation_completion_report.md
