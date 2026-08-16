----
git reset --hard 1beea1c9eb3ffa5d01f7c266b826e52136d01e8f
----
git add . ; \
git commit -m "作業切り戻しのため、 1beea1c9eb3ffa5d01f7c266b826e52136d01e8f まで切り戻した"; \
git push -f causal-atelier feature/ariadne_mvp_e7; \ 
git log -1; \ 
git status
----
cp -apf ~/Document/_work/20260813_ENH-E7_project_analysis_workspace_separation/* ./
-----
git add . ; \
git commit -m "20260813_ENH-E7_project_analysis_workspace_separation_v0.07.zip を適用"; \
git push -f causal-atelier feature/ariadne_mvp_e7; \ 
git log -1; \ 
git status
