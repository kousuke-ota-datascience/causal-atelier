以下2つ、実施せよ。つまりこの修正を反映したtemplateファイル一式を作成せよ

```
したがってworkflow templateに適用するなら、少なくとも以下はセットで変更すべきです。

template内の全nested README.md rename
Markdown link更新
operator prompt内のREADME参照更新
TEMPLATE_STRUCTURE.md 更新
MANIFEST.json がfilenameを保持するなら更新
validator / script内の README.md 固定参照更新
Enhancement instantiation処理の出力名更新
README生成規約の明文化

つまり、これは横断的なschema変更です。
```

`````
私は postfix を手作業で付けるというより、

```
README filename = deterministic function(directory path)
```

と定義することを勧めます。

例えば概念的には、

```
f(00_enhance_background)
    = README_00.md

f(20_implementation_reports/G01/Trial01)
    = README_20_G01_Trial01.md

f(40_operator_workflows/agent_entry_prompts)
    = README_40_agent_entry_prompts.md
```

です。
`````
-----

## READMEへのpostfix適用

現状、各階層にREADMEが存在する。
大量にあるためどの階層のREADMEか、パット見でわからない。特にVS Code 上で見た場合。
トップレベルの README.md のみ「無印」扱いとする

例）現状
```
- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/
    - README.md
    - 00_enhance_background/
        - README.md
    - 20_implementation_reports/
        - G01/
            - Trial01/
                - README.md    
```

例）修正後
```
- docs/wiki/develop_memo/_work/20260813_ENH-E7_project_analysis_workspace_separation/
    - README.md
    - 00_enhance_background/
        - README_00.md
    - 20_implementation_reports/
        - G01/
            - Trial01/
                - README_20_G01_Trial01.md    
```
