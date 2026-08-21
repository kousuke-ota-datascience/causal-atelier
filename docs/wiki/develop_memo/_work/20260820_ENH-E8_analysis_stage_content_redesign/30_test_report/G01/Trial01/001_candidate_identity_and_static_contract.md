# G01 Trial01 — Candidate Identity and Static Contract Evidence

- Gate: `G01`
- Trial: `01`
- Test Item ID: `001`
- Candidate SHA: `f62e3e75ba474928d6f2ca886e9992375c6f16e5`
- Result: `PASS` (static/audit scope only)

## Acceptance Criteria

- `G01-AC01`, `G01-AC02`, `G01-AC05`, `G01-AC07`, `G01-AC09`

## Method / command

An isolated detached worktree was created at the fixed SHA because the invoking worktree was at `aba63fb23240177c6e05d622f121d4ce361a946d` and had two unrelated uncommitted workflow-document changes.

```text
git -C /tmp/ariadne-e8-g01-trial01-f62e3e75 rev-parse HEAD
git -C /tmp/ariadne-e8-g01-trial01-f62e3e75 status --short
git diff --name-status 386521d18e9c5cc4d42fb99c97c212430908afc3 f62e3e75ba474928d6f2ca886e9992375c6f16e5
node --check frontend/app.js
python3 -m py_compile tests/browser_e2e/run_enh_e8_g01_project_return.py
```

## Evidence

- The isolated worktree resolved exactly to `f62e3e75ba474928d6f2ca886e9992375c6f16e5` and was clean.
- `frontend/index.html` contains one native button, `#return-to-project-list`, in the shared `project-management-shell-chrome`; the shell encloses all four Project local sections. Its visible and accessible native-button name is `Project Listへ戻る`.
- `frontend/app.js` binds that button to `synchronizeProjectHistory({kind:'collection'}, 'PUSH')` and then activates `projects`. `ProjectNavigation.serialize({kind:'collection'})` is the existing canonical collection route `/projects`; there is no `history.back()` in the handler.
- Candidate product-source changes are limited to `frontend/app.js`, `frontend/index.html`, and `frontend/styles.css`. The other executable changes are the browser-test build inclusion and its runner. No `src/`, migration, API-contract, persistence, or runtime implementation file is changed.
- JavaScript syntax and the candidate browser-runner Python syntax both passed.

## 判定理由

The listed criteria are established by the exact candidate's DOM/code and diff audit. This item does not establish destination rendering, direct-entry behavior, browser history behavior, or protected regression; those require the blocked browser integration item.
