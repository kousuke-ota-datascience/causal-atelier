const AUTH_HEADERS = {
  "X-User-Subject": "local-developer",
  "X-User-Name": "Local analyst",
};

const state = {
  projects: [],
  project: null,
  datasets: [],
  runs: [],
  members: [],
  datasetVersions: [],
  configurations: [],
  configurationVersions: [],
  causalGraphs: [],
  section: "overview",
  graphSources: [],
  activeGraph: 0,
  compareGraphs: false,
  pollers: new Map(),
};

const TERMINAL_STATUSES = new Set(["SUCCEEDED", "FAILED", "CANCELLED"]);
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

async function api(path, options = {}) {
  const headers = {...AUTH_HEADERS, ...(options.headers || {})};
  if (options.body && !(options.body instanceof FormData) && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const response = await fetch(path, {...options, headers});
  const contentType = response.headers.get("content-type") || "";
  let body = null;
  if (response.status !== 204) {
    body = contentType.includes("json") ? await response.json() : await response.text();
  }
  if (!response.ok) {
    const details = body?.error?.details?.issues || body?.error?.details?.detail || body?.detail;
    const suffix = Array.isArray(details) ? `: ${details.map(issue => {
      const location = Array.isArray(issue.loc) ? issue.loc.filter(part => part !== "body").join(".") : "";
      const message = issue.message || issue.msg || issue.code;
      return location ? `${location}: ${message}` : message;
    }).join(", ")}` : "";
    throw new Error(`${body?.error?.message || body?.detail || `HTTP ${response.status}`}${suffix}`);
  }
  return body;
}

function knownVersions() { return state.datasetVersions; }
function savedGraphs() {
  return state.causalGraphs.flatMap(graph =>
    (graph.versions || [])
      .filter(version => version.status === "PUBLISHED")
      .map(version => ({...version, graph_name: graph.name, graph_slug: graph.slug}))
  );
}

function rememberVersion(version, dataset = {}) {
  const entries = knownVersions().filter(item => item.id !== version.id);
  entries.unshift({
    id: version.id,
    dataset_id: version.dataset_id || dataset.id,
    dataset_name: dataset.name || "Dataset",
    dataset_kind: dataset.dataset_kind || "PROCESSED",
    version_number: version.version_number,
    status: version.status,
    tables: version.tables || [],
    created_at: version.created_at || new Date().toISOString(),
  });
  state.datasetVersions = entries.slice(0, 100);
  renderVersionOptions();
}

function clearPollers() {
  for (const timer of state.pollers.values()) clearTimeout(timer);
  state.pollers.clear();
}

async function initialize() {
  bindEvents();
  await checkApi();
  await route();
}

async function checkApi() {
  const badge = $("#api-status");
  try {
    await api("/health/live");
    badge.className = "api-status online";
    badge.innerHTML = "<i></i>API connected";
  } catch {
    badge.className = "api-status offline";
    badge.innerHTML = "<i></i>API offline";
  }
}

function bindEvents() {
  window.addEventListener("hashchange", route);
  $("#new-project").addEventListener("click", () => $("#project-dialog").showModal());
  $$('[data-close-dialog]').forEach(button => button.addEventListener("click", () => $("#project-dialog").close()));
  $$('[data-close-edit]').forEach(button => button.addEventListener("click", () => $("#edit-project-dialog").close()));
  $$('[data-close-delete]').forEach(button => button.addEventListener("click", () => $("#delete-project-dialog").close()));
  $("#project-form").addEventListener("submit", createProject);
  $("#edit-project-form").addEventListener("submit", updateProject);
  $("#edit-project").addEventListener("click", openProjectEditor);
  $("#open-delete-project").addEventListener("click", openDeleteProjectDialog);
  $("#delete-project-confirmation").addEventListener("input", syncDeleteConfirmation);
  $("#delete-project-form").addEventListener("submit", deleteProject);
  $("#workflow-nav").addEventListener("click", event => {
    const link = event.target.closest("[data-section]");
    if (!link) return;
    event.preventDefault();
    if (!state.project) {
      location.hash = "#/projects";
      return;
    }
    location.hash = `#/projects/${state.project.id}/${link.dataset.section}`;
  });
  document.addEventListener("click", delegatedClick);

  $("#dataset-file").addEventListener("change", event => {
    const file = event.target.files[0];
    $("#file-label").textContent = file ? `${file.name} · ${formatBytes(file.size)}` : "CSV / Parquet";
    if (file) {
      const form = $("#upload-dataset-form");
      const stem = file.name.replace(/\.[^.]+$/, "");
      if (!form.elements.name.value) form.elements.name.value = titleCase(stem);
      if (!form.elements.slug.value) form.elements.slug.value = slugify(stem);
      if (!form.elements.logical_name.value) form.elements.logical_name.value = slugify(stem).replaceAll("-", "_");
    }
  });
  $("#upload-dataset-form").addEventListener("submit", uploadDataset);
  $("#semantics-version-select").addEventListener("change", renderSemanticsColumns);
  $("#semantics-form").addEventListener("submit", createFeatureSemantics);
  $("#discovery-run-form").addEventListener("submit", createDiscoveryRun);
  $("#load-discovery-run").addEventListener("click", () => loadDiscoveryFromRun($("#discovery-run-select").value));
  $("#compare-graphs").addEventListener("click", toggleGraphComparison);
  $("#graph-tabs").addEventListener("click", event => {
    const tab = event.target.closest("[data-graph-index]");
    if (!tab) return;
    state.activeGraph = Number(tab.dataset.graphIndex);
    state.compareGraphs = false;
    renderGraphs();
  });
  $("#saved-graph-select").addEventListener("change", selectSavedGraph);
  $$('input[name="analysis_mode"]').forEach(input => input.addEventListener("change", toggleInferenceMode));
  $("#inference-run-form").addEventListener("submit", createInferenceRun);
  $("#load-inference-run").addEventListener("click", () => loadInferenceFromRun($("#inference-run-select").value));
}

async function route() {
  clearPollers();
  const match = location.hash.match(/^#\/projects\/([^/]+)(?:\/([^/]+))?/);
  if (!match) {
    if (location.hash !== "#/projects") history.replaceState(null, "", "#/projects");
    showView("list");
    await loadProjects();
    return;
  }
  const [, projectId, requestedSection = "overview"] = match;
  state.section = ["overview", "data", "discovery", "inference"].includes(requestedSection) ? requestedSection : "overview";
  showView("detail");
  await loadProject(projectId);
}

function showView(name) {
  $("#project-list-view").hidden = name !== "list";
  $("#project-detail-view").hidden = name !== "detail";
  window.scrollTo({top: 0});
}

async function loadProjects() {
  const grid = $("#projects");
  grid.innerHTML = '<div class="skeleton-card"></div><div class="skeleton-card"></div><div class="skeleton-card"></div>';
  try {
    const page = await api("/api/v1/projects");
    state.projects = page.items;
    $("#project-summary").textContent = `${page.total} project${page.total === 1 ? "" : "s"}`;
    grid.innerHTML = page.items.length ? page.items.map(projectCard).join("") : `
      <div class="empty"><div><strong>最初のProjectを作成しましょう</strong><br><small>Dataset、Run、分析結果がProjectに整理されます。</small></div></div>`;
  } catch (error) {
    $("#project-summary").textContent = "APIへ接続できません";
    grid.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

function projectCard(project) {
  const monogram = initials(project.name);
  return `<article class="project-card" data-monogram="${escapeAttr(monogram)}">
    <span class="slug">${escapeHtml(project.slug)}</span>
    <h3>${escapeHtml(project.name)}</h3>
    <p>${escapeHtml(project.description || "説明はまだありません。Project詳細から分析を始められます。")}</p>
    <footer><span>${formatDate(project.created_at)}</span><button type="button" class="card-open" data-open-project="${escapeAttr(project.id)}">Overview →</button></footer>
  </article>`;
}

async function loadProject(projectId) {
  $("#detail-loading").hidden = false;
  $("#detail-loading").innerHTML = '<span class="spinner"></span>Projectを読み込んでいます';
  $$(".workflow-section").forEach(section => section.hidden = true);
  try {
    const encodedProjectId = encodeURIComponent(projectId);
    const project = await api(`/api/v1/projects/${encodedProjectId}`);
    const resourceFailures = [];
    const loadResource = async (label, path, fallback) => {
      try { return await api(path); }
      catch (error) {
        resourceFailures.push(`${label}: ${error.message}`);
        return fallback;
      }
    };
    const [datasets, runs, members, configurations, graphs] = await Promise.all([
      loadResource("Datasets", `/api/v1/datasets?project_id=${encodedProjectId}&limit=200`, {items: []}),
      loadResource("Runs", `/api/v1/runs?project_id=${encodedProjectId}&limit=200`, {items: []}),
      loadResource("Members", `/api/v1/projects/${encodedProjectId}/members`, []),
      loadResource("Configurations", `/api/v1/configurations?project_id=${encodedProjectId}`, []),
      loadResource("Saved Graphs", `/api/v1/causal-graphs?project_id=${encodedProjectId}&limit=200`, {items: []}),
    ]);
    const [versionPages, configurationVersionLists] = await Promise.all([
      Promise.all(datasets.items.map(dataset => loadResource(
        `Dataset ${dataset.name} versions`,
        `/api/v1/datasets/${encodeURIComponent(dataset.id)}/versions?limit=200`,
        {items: []},
      ))),
      Promise.all(configurations.map(config => loadResource(
        `Configuration ${config.name} versions`,
        `/api/v1/configurations/${encodeURIComponent(config.id)}/versions`,
        [],
      ))),
    ]);
    state.project = project;
    state.datasets = datasets.items;
    state.runs = runs.items;
    state.members = members;
    state.datasetVersions = versionPages.flatMap((page, index) =>
      page.items.map(version => ({...version, dataset_name: datasets.items[index].name, dataset_kind: datasets.items[index].dataset_kind}))
    );
    state.configurations = configurations;
    state.configurationVersions = configurationVersionLists.flatMap((versions, index) =>
      versions.map(version => ({...version, configuration_type: configurations[index].configuration_type, configuration_name: configurations[index].name}))
    );
    state.causalGraphs = graphs.items;
    state.graphSources = [];
    renderProjectShell();
    renderAllProjectData();
    showSection(state.section);
    if (resourceFailures.length) {
      toast(`Projectは開きましたが、一部の情報を取得できませんでした: ${resourceFailures.join(" / ")}`, "error");
    }
  } catch (error) {
    state.project = null;
    $("#detail-loading").innerHTML = `<div class="empty">Projectを開けません: ${escapeHtml(error.message)}<br><a href="#/projects">Project一覧へ戻る</a></div>`;
    toast(error.message, "error");
  }
}

function renderProjectShell() {
  const project = state.project;
  const monogram = initials(project.name);
  $("#detail-monogram").textContent = monogram;
  $("#sidebar-project-name").textContent = project.name;
  $("#sidebar-project-slug").textContent = project.slug;
  $("#detail-project-name").textContent = project.name;
  $("#detail-project-description").textContent = project.description || "分析目的やProjectの説明はまだ登録されていません。";
  $("#detail-project-status").textContent = project.status;
  $("#detail-project-status").className = `status-pill status-${project.status}`;
  document.title = `${project.name} — causal atelier`;
}

function renderAllProjectData() {
  renderOverview();
  renderDatasets();
  renderRunTables();
  renderRunSelects();
  renderVersionOptions();
  renderSavedGraphs();
}

function showSection(section) {
  $("#detail-loading").hidden = true;
  $$(".workflow-section").forEach(node => node.hidden = node.id !== `section-${section}`);
  $$("#workflow-nav [data-section]").forEach(link => link.classList.toggle("active", link.dataset.section === section));
  state.section = section;
}

function renderOverview() {
  const completed = state.runs.filter(run => run.status === "SUCCEEDED").length;
  $("#metric-datasets").textContent = state.datasets.length;
  $("#metric-runs").textContent = state.runs.length;
  $("#metric-completed").textContent = completed;
  $("#metric-graphs").textContent = savedGraphs().length;
  $("#project-details").innerHTML = [
    ["Project ID", state.project.id], ["Slug", state.project.slug],
    ["Created", formatDateTime(state.project.created_at)], ["Members", `${state.members.length || 1} member${state.members.length === 1 ? "" : "s"}`],
  ].map(([term, value]) => `<div><dt>${term}</dt><dd>${escapeHtml(value)}</dd></div>`).join("");

  const hasData = state.datasets.length > 0;
  const hasDiscovery = state.runs.some(run => run.run_kind === "DISCOVERY" && run.status === "SUCCEEDED");
  const hasGraph = savedGraphs().length > 0;
  const hasInference = state.runs.some(run => run.run_kind === "INFERENCE" && run.status === "SUCCEEDED");
  const journey = [
    {label: "データを登録・前処理", sub: "分析対象のDataset Versionを準備", done: hasData, section: "data"},
    {label: "因果構造を探索", sub: "複数アルゴリズムでgraphを比較", done: hasDiscovery, section: "discovery"},
    {label: "探索グラフを保存", sub: "推論に利用するedge Artifactを選択", done: hasGraph, section: "discovery"},
    {label: "因果効果を推定", sub: "仮定・信頼区間・診断を確認", done: hasInference, section: "inference"},
  ];
  const firstPending = journey.findIndex(item => !item.done);
  $("#journey-status").innerHTML = journey.map((item, index) => `<div class="journey-item ${item.done ? "done" : index === firstPending ? "current" : ""}">
    <span>${item.done ? "✓" : index + 1}</span><div><b>${item.label}</b><small>${item.sub}</small></div>
    <button class="text-button" data-go-section="${item.section}">${item.done ? "確認" : index === firstPending ? "始める →" : ""}</button>
  </div>`).join("");
  $("#recent-runs").innerHTML = state.runs.length ? state.runs.slice(0, 5).map(runRow).join("") : '<div class="mini-empty">Runはまだありません。</div>';
}

function runRow(run) {
  return `<div class="run-row"><div><b>${escapeHtml(run.run_kind)} · ${shortId(run.id)}</b><small>${formatDateTime(run.submitted_at)}</small></div>${statusPill(run.status)}</div>`;
}

function renderDatasets() {
  const table = $("#dataset-list");
  table.innerHTML = state.datasets.length ? `<table class="data-table"><thead><tr><th>Dataset</th><th>Kind</th><th>Versions</th><th>Readiness</th></tr></thead><tbody>${state.datasets.map(dataset => {
    const versions = knownVersions().filter(version => version.dataset_id === dataset.id);
    const latest = versions.sort((a, b) => b.version_number - a.version_number)[0];
    return `<tr>
    <td><strong>${escapeHtml(dataset.name)}</strong><small>${escapeHtml(dataset.slug)}</small></td>
    <td><span class="kind-pill">${escapeHtml(dataset.dataset_kind)}</span></td><td>${versions.length}</td>
    <td>${latest ? statusPill(latest.analysis_binding?.readiness_status || latest.status) : "—"}</td>
  </tr>`;
  }).join("")}</tbody></table>` : '<div class="mini-empty">Datasetはまだありません。上のフォームから分析用テーブルを登録してください。</div>';
}

function renderVersionOptions() {
  const versions = knownVersions();
  $("#known-version-ids").innerHTML = versions.map(item => `<option value="${escapeAttr(item.id)}">${escapeHtml(item.dataset_name)} v${item.version_number || "?"} · ${escapeHtml(item.dataset_kind)}</option>`).join("");
  const options = versions
    .filter(item => item.status === "READY" && item.analysis_binding?.readiness_status === "READY")
    .map(item => `<option value="${escapeAttr(item.id)}">${escapeHtml(item.dataset_name)} · v${item.version_number}</option>`).join("");
  for (const selector of ["#semantics-version-select", "#discovery-version-id", "#inference-version-id"]) {
    const select = $(selector);
    const current = select.value;
    select.innerHTML = `<option value="">Versionを選択</option>${options}`;
    if (versions.some(version => version.id === current)) select.value = current;
  }
  const semantics = state.configurationVersions.filter(item => item.configuration_type === "FEATURE_SEMANTICS" && item.status === "PUBLISHED");
  const semanticsOptions = semantics.map(item => `<option value="${escapeAttr(item.id)}">${escapeHtml(item.configuration_name)} · v${item.version_number}</option>`).join("");
  for (const selector of ["#discovery-semantics-id", "#inference-semantics-id"]) {
    const select = $(selector);
    const current = select.value;
    select.innerHTML = `<option value="">PUBLISHED Semanticsを選択</option>${semanticsOptions}`;
    if (semantics.some(item => item.id === current)) select.value = current;
  }
}

function renderRunTables() {
  renderRunTable("#discovery-runs", state.runs.filter(run => run.run_kind === "DISCOVERY"), "discovery");
  renderRunTable("#inference-runs", state.runs.filter(run => run.run_kind === "INFERENCE"), "inference");
}

function renderRunTable(selector, runs, kind) {
  $(selector).innerHTML = runs.length ? `<table class="data-table"><thead><tr><th>Run</th><th>Mode</th><th>Status</th><th>Submitted</th><th></th></tr></thead><tbody>${runs.map(run => `<tr>
    <td><strong>${shortId(run.id)}</strong><small>${escapeHtml(run.run_kind)}</small></td><td>${escapeHtml(run.execution_mode)}</td>
    <td>${statusPill(run.status)}</td><td>${formatDateTime(run.submitted_at)}</td>
    <td><button class="text-button" data-load-${kind}-run="${escapeAttr(run.id)}">結果を表示 →</button></td>
  </tr>`).join("")}</tbody></table>` : `<div class="mini-empty">${kind === "discovery" ? "Discovery" : "Inference"} Runはまだありません。</div>`;
}

function renderRunSelects() {
  const discoveryRuns = state.runs.filter(run => run.run_kind === "DISCOVERY");
  const inferenceRuns = state.runs.filter(run => run.run_kind === "INFERENCE");
  $("#discovery-run-select").innerHTML = `<option value="">Runを選択</option>${discoveryRuns.map(runOption).join("")}`;
  $("#inference-run-select").innerHTML = `<option value="">Runを選択</option>${inferenceRuns.map(runOption).join("")}`;
}

function runOption(run) {
  return `<option value="${escapeAttr(run.id)}">${shortId(run.id)} · ${run.status} · ${formatDate(run.submitted_at)}</option>`;
}

async function createProject(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  const data = new FormData(form);
  const payload = {
    slug: String(data.get("slug") || "").trim(),
    name: String(data.get("name") || "").trim(),
    description: String(data.get("description") || "").trim() || null,
  };
  setFormBusy(form, true, message);
  try {
    const project = await api("/api/v1/projects", {method: "POST", body: JSON.stringify(payload)});
    form.reset();
    $("#project-dialog").close();
    toast("Projectを作成しました。", "success");
    location.hash = `#/projects/${project.id}/overview`;
  } catch (error) { message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

function openProjectEditor() {
  const form = $("#edit-project-form");
  form.elements.name.value = state.project.name;
  form.elements.description.value = state.project.description || "";
  const currentMember = state.members.find(member => member.external_subject === AUTH_HEADERS["X-User-Subject"]);
  $("#open-delete-project").hidden = Boolean(currentMember) && currentMember.role !== "PROJECT_ADMIN";
  $("#edit-project-dialog").showModal();
}

async function updateProject(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  setFormBusy(form, true, message);
  try {
    const updated = await api(`/api/v1/projects/${state.project.id}`, {method: "PATCH", body: JSON.stringify({name: form.elements.name.value, description: form.elements.description.value || null})});
    state.project = updated;
    renderProjectShell();
    renderOverview();
    $("#edit-project-dialog").close();
    toast("Projectの情報を更新しました。", "success");
  } catch (error) { message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

function openDeleteProjectDialog() {
  if (!state.project) return;
  $("#edit-project-dialog").close();
  $("#delete-project-name").textContent = state.project.name;
  $("#delete-project-slug").textContent = state.project.slug;
  const form = $("#delete-project-form");
  form.reset();
  $("[data-form-message]", form).textContent = "";
  syncDeleteConfirmation();
  $("#delete-project-dialog").showModal();
  $("#delete-project-confirmation").focus();
}

function syncDeleteConfirmation() {
  const expected = state.project?.slug || "";
  $("#confirm-delete-project").disabled = $("#delete-project-confirmation").value !== expected;
}

async function deleteProject(event) {
  event.preventDefault();
  if (!state.project) return;
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  if (form.elements.confirmation.value !== state.project.slug) {
    message.textContent = "Project slugが一致していません。";
    return;
  }
  const projectId = state.project.id;
  const projectName = state.project.name;
  setFormBusy(form, true, message);
  try {
    await api(`/api/v1/projects/${encodeURIComponent(projectId)}`, {method: "DELETE"});
    clearPollers();
    $("#delete-project-dialog").close();
    state.project = null;
    toast(`${projectName} を論理削除しました。`, "success");
    location.hash = "#/projects";
  } catch (error) {
    message.textContent = error.message;
  } finally {
    setFormBusy(form, false);
    syncDeleteConfirmation();
  }
}

async function uploadDataset(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  const file = form.elements.file.files[0];
  if (!file) return;
  setFormBusy(form, true, message);
  try {
    message.className = "form-message success";
    message.textContent = "1/3 ファイルをObject Storeへ保存しています…";
    const upload = new FormData(); upload.append("file", file);
    const object = await api(`/api/v1/projects/${state.project.id}/objects`, {method: "POST", body: upload});
    message.textContent = "2/3 Datasetを登録しています…";
    const dataset = await api("/api/v1/datasets", {method: "POST", body: JSON.stringify({
      project_id: state.project.id, slug: form.elements.slug.value, name: form.elements.name.value,
      description: form.elements.analysis_unit_description.value || null, dataset_kind: form.elements.dataset_kind.value,
    })});
    message.textContent = "3/3 不変のDataset Versionを作成しています…";
    const version = await api(`/api/v1/datasets/${dataset.id}/versions`, {method: "POST", body: JSON.stringify({
      source_type: "UPLOAD", source_metadata: {filename: file.name, analysis_unit_description: form.elements.analysis_unit_description.value}, profile: true,
      tables: [{logical_name: form.elements.logical_name.value, object}],
    })});
    rememberVersion(version, dataset);
    state.datasets.unshift(dataset);
    renderDatasets(); renderOverview(); renderVersionOptions();
    form.reset(); $("#file-label").textContent = "CSV / Parquet";
    message.textContent = ""; message.className = "form-message";
    $("#semantics-version-select").value = version.id;
    renderSemanticsColumns();
    toast(`Dataset v${version.version_number} を登録しました。`, "success");
  } catch (error) { message.className = "form-message"; message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

function renderSemanticsColumns() {
  const version = knownVersions().find(item => item.id === $("#semantics-version-select").value);
  const root = $("#semantics-columns");
  const table = version?.tables?.[0];
  if (!table?.columns?.length) {
    root.innerHTML = '<p class="field-hint">Versionを選ぶと列一覧が表示されます。</p>';
    return;
  }
  const roles = ["identifier", "treatment", "outcome", "covariate", "mediator", "collider", "post_treatment", "excluded"];
  root.innerHTML = `<table class="data-table semantics-table"><thead><tr><th>Column</th><th>Role</th><th>Categorical</th><th>Discovery</th><th>Adjustment</th></tr></thead><tbody>${table.columns.map(column => {
    const categorical = !/int|float|double|decimal|number/i.test(column.physical_type);
    return `<tr data-semantic-column data-column-id="${escapeAttr(column.id)}" data-column-name="${escapeAttr(column.name)}" data-dtype="${escapeAttr(column.physical_type)}">
      <td><strong>${escapeHtml(column.name)}</strong><small>${escapeHtml(column.physical_type)}</small></td>
      <td><select name="role">${roles.map(role => `<option value="${role}" ${role === "covariate" ? "selected" : ""}>${role}</option>`).join("")}</select></td>
      <td><input name="categorical" type="checkbox" ${categorical ? "checked" : ""}></td>
      <td><input name="discovery" type="checkbox" checked></td>
      <td><input name="adjustment" type="checkbox" checked></td>
    </tr>`;
  }).join("")}</tbody></table>`;
  $$('[name="role"]', root).forEach(select => select.addEventListener("change", event => {
    const row = event.target.closest("[data-semantic-column]");
    const forbiddenDiscovery = ["identifier", "excluded", "post_treatment"].includes(event.target.value);
    const forbiddenAdjustment = event.target.value !== "covariate";
    row.querySelector('[name="discovery"]').checked = !forbiddenDiscovery;
    row.querySelector('[name="adjustment"]').checked = !forbiddenAdjustment;
  }));
}

async function createFeatureSemantics(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  const version = knownVersions().find(item => item.id === form.elements.version_id.value);
  const table = version?.tables?.[0];
  const rows = $$("[data-semantic-column]", form);
  if (!version || !table || !rows.length) { message.textContent = "Dataset Versionと列を選択してください。"; return; }
  setFormBusy(form, true, message);
  try {
    const features = rows.map(row => {
      const role = row.querySelector('[name="role"]').value;
      return {
        name: row.dataset.columnName,
        source_table: table.logical_name,
        source_column: row.dataset.columnName,
        dtype: row.dataset.dtype,
        role,
        categorical: row.querySelector('[name="categorical"]').checked,
        allowed_for_discovery: row.querySelector('[name="discovery"]').checked,
        allowed_for_adjustment: row.querySelector('[name="adjustment"]').checked,
        post_treatment: role === "post_treatment",
      };
    });
    const treatment = features.filter(item => item.role === "treatment");
    const outcome = features.filter(item => item.role === "outcome");
    if (treatment.length !== 1 || outcome.length !== 1) throw new Error("treatmentとoutcomeをそれぞれ1列ずつ指定してください。");
    const published = await createAndPublishConfiguration(
      "FEATURE_SEMANTICS",
      `semantics-${version.id.slice(0, 8)}-${Date.now()}`,
      `${version.dataset_name} semantics`,
      {dataset_version_id: version.id, default_unit_id: "row", features},
    );
    const identifier = features.find(item => item.role === "identifier");
    await api(`/api/v1/dataset-versions/${version.id}/analysis-binding`, {
      method: "PUT",
      body: JSON.stringify({
        analysis_unit_description: version.analysis_binding?.analysis_unit_description || "One row is one analysis unit",
        unit_identifier_column_id: identifier ? rows.find(row => row.dataset.columnName === identifier.name)?.dataset.columnId : null,
      }),
    });
    renderVersionOptions();
    $("#discovery-version-id").value = version.id;
    $("#discovery-semantics-id").value = published.id;
    message.className = "form-message success";
    message.textContent = "Feature Semanticsを検証・publishしました。";
    toast("Feature Semanticsをpublishしました。", "success");
  } catch (error) { message.className = "form-message"; message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

async function createAndPublishConfiguration(type, slug, name, canonicalJson) {
  const configuration = await api("/api/v1/configurations", {
    method: "POST",
    body: JSON.stringify({project_id: state.project.id, configuration_type: type, slug, name, description: "Created from the Web analysis-ready flow"}),
  });
  const version = await api(`/api/v1/configurations/${configuration.id}/versions`, {
    method: "POST",
    body: JSON.stringify({canonical_json: canonicalJson, schema_version: "1"}),
  });
  const validation = await api(`/api/v1/configuration-versions/${version.id}/validate`, {method: "POST"});
  if (validation.status !== "VALID") throw new Error(validation.issues.map(issue => issue.message).join(", "));
  const published = await api(`/api/v1/configuration-versions/${version.id}/publish`, {method: "POST"});
  state.configurations.unshift(configuration);
  state.configurationVersions.unshift({...published, configuration_type: type, configuration_name: name});
  return published;
}

async function createDiscoveryRun(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  const algorithms = $$('input[name="algorithms"]:checked', form).map(input => input.value);
  if (!algorithms.length) { message.textContent = "1つ以上のalgorithmを選択してください。"; return; }
  setFormBusy(form, true, message);
  try {
    const analysisConfig = await createAndPublishConfiguration(
      "DISCOVERY_ANALYSIS",
      `discovery-${Date.now()}`,
      "Web analysis-ready discovery",
      {input_mode: "ANALYSIS_READY", algorithms, alpha: Number(form.elements.alpha.value)},
    );
    const run = await submitRun({
      run_kind: "DISCOVERY", execution_mode: form.elements.execution_mode.value, random_seed: Number(form.elements.random_seed.value),
      stages: [{
        stage_key: "discovery", stage_type: "DISCOVERY", runner_name: "analysis_ready", input_mode: "ANALYSIS_READY",
        dataset_inputs: {analysis_data: form.elements.version_id.value},
        configuration_inputs: {analysis_config: analysisConfig.id, feature_semantics: form.elements.feature_semantics.value},
        parameters: {
          algorithms, alpha: Number(form.elements.alpha.value), bootstrap_samples: Number(form.elements.bootstrap_samples.value), random_seed: Number(form.elements.random_seed.value),
          conditioning: {
            missing_values: form.elements.missing_values.value,
            categorical_encoding: form.elements.categorical_encoding.value,
            standardize: true,
            collinearity_threshold: Number(form.elements.collinearity_threshold.value),
          },
        },
        outputs: {manifest: "MANIFEST", edges: "DISCOVERY_EDGES"},
      }],
      metadata: {ui: "causal-atelier", requested_algorithms: algorithms},
    });
    upsertRun(run); renderOverview(); renderRunTables(); renderRunSelects();
    $("#discovery-run-select").value = run.id;
    showRunMonitor("discovery", run);
    toast("因果探索Runを作成しました。", "success");
    if (!TERMINAL_STATUSES.has(run.status)) pollRun(run.id, "discovery");
    else if (run.status === "SUCCEEDED" && run.execution_mode === "RUN") await loadDiscoveryFromRun(run.id);
  } catch (error) { message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

async function createInferenceRun(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const message = $("[data-form-message]", form);
  const mode = form.elements.analysis_mode.value;
  const graph = savedGraphs().find(item => item.id === form.elements.graph_version_id.value);
  if (!graph) { message.textContent = "PUBLISHED Saved Graphを選択してください。"; return; }
  if (graph.dataset_version_id !== form.elements.version_id.value || graph.feature_semantics_version_id !== form.elements.feature_semantics.value) {
    message.textContent = "Dataset、Semantics、Saved Graphの来歴が一致していません。"; return;
  }
  const parameters = mode === "TREATMENT_EFFECT" ? {
    treatment: form.elements.treatment.value, outcome: form.elements.outcome.value,
    estimand: form.elements.estimand.value, adjustment_strategy: form.elements.adjustment_strategy.value,
    effect_methods: form.elements.effect_methods.value.split(",").map(value => value.trim()).filter(Boolean).map(value =>
      form.elements.estimand.value === "ATT" ? value.replace(/_ate$/, "_att") : value.replace(/_att$/, "_ate")
    ),
    covariates: form.elements.covariates.value.split(",").map(value => value.trim()).filter(Boolean),
  } : {};
  setFormBusy(form, true, message);
  try {
    const analysisConfig = await createAndPublishConfiguration(
      "INFERENCE_ANALYSIS",
      `inference-${Date.now()}`,
      "Web analysis-ready inference",
      {input_mode: "ANALYSIS_READY", analysis_mode: mode},
    );
    const config = {analysis_config: analysisConfig.id, feature_semantics: form.elements.feature_semantics.value};
    if (mode === "TREATMENT_EFFECT") {
      const assumptions = form.elements.assumptions.value.split("\n").map(value => value.trim()).filter(Boolean).map((statement, index) => ({code: `assumption_${index + 1}`, statement, declaration_status: "DECLARED"}));
      const design = await createAndPublishConfiguration(
        "CAUSAL_DESIGN",
        `design-${Date.now()}`,
        `${form.elements.treatment.value} to ${form.elements.outcome.value}`,
        {causal_design: {
          dataset_version_id: form.elements.version_id.value,
          feature_semantics_version_id: form.elements.feature_semantics.value,
          causal_graph_version_id: graph.id,
          estimand: form.elements.estimand.value,
          treatment: {name: form.elements.treatment.value, levels: [0, 1]},
          outcome: {name: form.elements.outcome.value},
          unit: "row",
          target_population: form.elements.target_population.value || null,
          adjustment_strategy: form.elements.adjustment_strategy.value,
          adjustment_set: parameters.covariates,
          assumptions,
        }},
      );
      config.causal_design = design.id;
    }
    const run = await submitRun({
      run_kind: "INFERENCE", execution_mode: form.elements.execution_mode.value, random_seed: Number(form.elements.random_seed.value),
      stages: [{
        stage_key: "inference", stage_type: "INFERENCE", analysis_mode: mode, runner_name: "analysis_ready", input_mode: "ANALYSIS_READY",
        dataset_inputs: {analysis_data: form.elements.version_id.value}, configuration_inputs: config,
        graph_inputs: {causal_graph: graph.id},
        parameters: {...parameters, conditioning: {missing_values: "complete_case", categorical_encoding: "ordinal", standardize: true, collinearity_threshold: 0.995}},
        outputs: {estimates: mode === "EDGE_WEIGHT" ? "EDGE_WEIGHT_ESTIMATES" : "TREATMENT_EFFECT_ESTIMATES", report: "REPORT"},
      }], metadata: {ui: "causal-atelier", causal_graph_version_id: graph.id},
    });
    upsertRun(run); renderOverview(); renderRunTables(); renderRunSelects();
    $("#inference-run-select").value = run.id;
    showRunMonitor("inference", run);
    toast("因果推論Runを作成しました。", "success");
    if (!TERMINAL_STATUSES.has(run.status)) pollRun(run.id, "inference");
    else if (run.status === "SUCCEEDED" && run.execution_mode === "RUN") await loadInferenceFromRun(run.id);
  } catch (error) { message.textContent = error.message; }
  finally { setFormBusy(form, false); }
}

async function submitRun(document) {
  return api("/api/v1/runs", {method: "POST", headers: {"Idempotency-Key": crypto.randomUUID()}, body: JSON.stringify({project_id: state.project.id, ...document})});
}

function upsertRun(run) {
  state.runs = [run, ...state.runs.filter(item => item.id !== run.id)];
}

function showRunMonitor(kind, run) {
  const panel = $(`#${kind}-run-monitor`);
  if (!panel) return;
  panel.hidden = false;
  const active = !TERMINAL_STATUSES.has(run.status);
  const stages = run.stages || [];
  panel.innerHTML = `<div class="run-monitor-header"><div><p class="kicker">${active ? "RUN IN PROGRESS" : "RUN STATUS"}</p><h3>${escapeHtml(run.run_kind)} · ${shortId(run.id)}</h3><p>${escapeHtml(run.execution_mode)} · submitted ${formatDateTime(run.submitted_at)}</p></div>${statusPill(run.status)}</div>
    <div class="stage-track">${(stages.length ? stages : [{status: run.status}]).map(stage => `<i class="${stage.status === "SUCCEEDED" || run.status === "SUCCEEDED" ? "complete" : active ? "active" : ""}"></i>`).join("")}</div>
    <div class="monitor-footer"><span>${stages.map(stage => `${stage.stage_key}: ${stage.status}`).join(" · ") || run.status}</span><button class="text-button" data-copy="${escapeAttr(run.id)}">Run IDをコピー</button></div>
    ${run.error_summary ? `<div class="notice-box">${escapeHtml(run.error_summary)}</div>` : ""}`;
}

function pollRun(runId, kind) {
  const key = `${kind}:${runId}`;
  const check = async () => {
    try {
      const run = await api(`/api/v1/runs/${runId}`);
      upsertRun(run); showRunMonitor(kind, run); renderRunTables(); renderRunSelects(); renderOverview();
      if (TERMINAL_STATUSES.has(run.status)) {
        state.pollers.delete(key);
        toast(`${run.run_kind} Runは ${run.status} で終了しました。`, run.status === "SUCCEEDED" ? "success" : "error");
        if (run.status === "SUCCEEDED" && run.execution_mode === "RUN") {
          if (kind === "discovery") await loadDiscoveryFromRun(run.id);
          if (kind === "inference") await loadInferenceFromRun(run.id);
        }
        return;
      }
      state.pollers.set(key, setTimeout(check, 3500));
    } catch (error) {
      state.pollers.delete(key); toast(error.message, "error");
    }
  };
  state.pollers.set(key, setTimeout(check, 1800));
}

async function loadDiscoveryFromRun(runId) {
  if (!runId) { toast("Discovery Runを選択してください。", "error"); return; }
  setButtonBusy($("#load-discovery-run"), true);
  try {
    const summary = await api(`/api/v1/runs/${runId}/results`);
    const link = summary.items.find(item => item.result_type === "DISCOVERY");
    if (!link) throw new Error("このRunにDiscovery Resultがありません。Runの完了状態を確認してください。");
    const result = await api(link.url);
    state.graphSources = (result.algorithms || []).map(item => ({
      algorithm: item.algorithm,
      edges: item.edges || [],
      artifactId: item.edge_artifact_id,
      algorithmResultId: item.id,
      resultId: result.id,
      featureSemanticsVersionId: result.feature_semantics_version_id,
      datasetVersionId: result.dataset_version_id,
      runId,
    }));
    state.activeGraph = 0; state.compareGraphs = false;
    renderGraphs();
    toast(`${state.graphSources.length}件の探索グラフを読み込みました。`, "success");
  } catch (error) { toast(error.message, "error"); }
  finally { setButtonBusy($("#load-discovery-run"), false); }
}

function renderGraphs() {
  const sources = state.graphSources;
  $("#graph-tabs").innerHTML = sources.map((source, index) => `<button class="graph-tab ${index === state.activeGraph && !state.compareGraphs ? "active" : ""}" data-graph-index="${index}">${escapeHtml(source.algorithm)} <small>${normalizedEdges(source.edges).length}</small></button>`).join("");
  $("#compare-graphs").disabled = sources.length < 2;
  $("#compare-graphs").textContent = state.compareGraphs ? "単体表示" : "並べて比較";
  const stage = $("#graph-stage");
  stage.classList.remove("empty-graph");
  if (!sources.length) {
    stage.innerHTML = '<div class="graph-placeholder"><span>⌁</span><h3>探索結果を選択してください</h3><p>Run完了後、edge Artifactを読み込むとグラフを描画します。</p></div>';
    $("#graph-summary").innerHTML = ""; return;
  }
  if (state.compareGraphs) {
    stage.innerHTML = `<div class="compare-grid">${sources.slice(0, 2).map(source => `<div class="compare-item"><h4>${escapeHtml(source.algorithm)}</h4>${graphSvg(source.edges, 470, 340)}</div>`).join("")}</div>`;
    const comparison = compareEdgeSets(sources[0], sources[1]);
    $("#graph-summary").innerHTML = `<div class="graph-stats"><span>共通edge <b>${comparison.common}</b></span><span>${escapeHtml(sources[0].algorithm)}のみ <b>${comparison.left}</b></span><span>${escapeHtml(sources[1].algorithm)}のみ <b>${comparison.right}</b></span></div>`;
    return;
  }
  const source = sources[state.activeGraph] || sources[0];
  const edges = normalizedEdges(source.edges);
  stage.innerHTML = graphSvg(edges, 760, 380);
  const nodes = new Set(edges.flatMap(edge => [edge.source, edge.target]));
  $("#graph-summary").innerHTML = `<div class="graph-stats"><span>Algorithm <b>${escapeHtml(source.algorithm)}</b></span><span>Nodes <b>${nodes.size}</b></span><span>Edges <b>${edges.length}</b></span></div>
    <button class="button save-graph" data-save-graph="${state.activeGraph}" ${source.algorithmResultId ? "" : "disabled title=\"保存元Resultが必要です\""}>このグラフを保存してpublish →</button>`;
}

function toggleGraphComparison() {
  if (state.graphSources.length < 2) return;
  state.compareGraphs = !state.compareGraphs; renderGraphs();
}

async function saveGraph(index) {
  const source = state.graphSources[index];
  if (!source?.algorithmResultId) { toast("保存元のDiscovery Resultがありません。", "error"); return; }
  try {
    const slug = `graph-${source.algorithm}-${Date.now()}`;
    const graph = await api("/api/v1/causal-graphs", {
      method: "POST",
      body: JSON.stringify({project_id: state.project.id, slug, name: `${source.algorithm.toUpperCase()} selected graph`, description: "Selected from Discovery comparison"}),
    });
    const version = await api(`/api/v1/causal-graphs/${graph.id}/versions`, {
      method: "POST",
      body: JSON.stringify({
        source_discovery_algorithm_result_id: source.algorithmResultId,
        feature_semantics_version_id: source.featureSemanticsVersionId,
        selection_note: "Selected in the Web graph comparison",
      }),
    });
    const published = await api(`/api/v1/causal-graph-versions/${version.id}/publish`, {method: "POST"});
    graph.versions = [published];
    state.causalGraphs.unshift(graph);
    renderSavedGraphs(); renderOverview();
    $("#saved-graph-select").value = published.id;
    selectSavedGraph();
    toast(`${source.algorithm} graph Versionをサーバーへ保存・publishしました。`, "success");
  } catch (error) { toast(error.message, "error"); }
}

function renderSavedGraphs() {
  const graphs = savedGraphs();
  const select = $("#saved-graph-select");
  const current = select.value;
  select.innerHTML = `<option value="">PUBLISHED Graphを選択</option>${graphs.map(item => `<option value="${escapeAttr(item.id)}">${escapeHtml(item.graph_name)} · ${escapeHtml(item.algorithm)} · ${item.edge_count} edges</option>`).join("")}`;
  if (graphs.some(item => item.id === current)) select.value = current;
  selectSavedGraph();
}

function selectSavedGraph() {
  const item = savedGraphs().find(graph => graph.id === $("#saved-graph-select").value);
  const note = $("#selected-graph-note");
  if (!item) { note.className = "selected-graph-note"; note.textContent = "Discovery画面でグラフを保存してください。"; return; }
  note.className = "selected-graph-note ready";
  note.innerHTML = `<b>${escapeHtml(item.algorithm)}</b> · ${item.edge_count} edges<br>Graph Version ${shortId(item.id)} · ${escapeHtml(item.status)}`;
  $("#inference-version-id").value = item.dataset_version_id;
  $("#inference-semantics-id").value = item.feature_semantics_version_id;
}

function toggleInferenceMode() {
  const treatment = $('input[name="analysis_mode"]:checked').value === "TREATMENT_EFFECT";
  $("#treatment-fields").hidden = !treatment;
  const form = $("#inference-run-form");
  for (const name of ["treatment", "outcome"]) form.elements[name].required = treatment;
}

async function loadInferenceFromRun(runId) {
  if (!runId) { toast("Inference Runを選択してください。", "error"); return; }
  setButtonBusy($("#load-inference-run"), true);
  try {
    const summary = await api(`/api/v1/runs/${runId}/results`);
    const link = summary.items.find(item => ["TREATMENT_EFFECT", "EDGE_WEIGHT"].includes(item.result_type));
    if (!link) throw new Error("このRunにInference Resultがありません。Runの完了状態を確認してください。");
    const result = await api(link.url);
    renderInferenceRows(result.estimates || [], link.result_type === "TREATMENT_EFFECT" ? "TREATMENT_EFFECT_ESTIMATES" : "EDGE_WEIGHT_ESTIMATES", result);
    toast("Inference Resultを読み込みました。", "success");
  } catch (error) { toast(error.message, "error"); }
  finally { setButtonBusy($("#load-inference-run"), false); }
}

function renderInferenceRows(rawRows, kind, context = {}) {
  const root = $("#inference-results");
  const rows = rawRows.map(normalizeKeys);
  if (!rows.length) { root.className = "results-empty"; root.innerHTML = "<h3>推定値がありません</h3><p>RunのログまたはResultのstatusを確認してください。</p>"; return; }
  root.className = "result-content";
  const treatment = kind === "TREATMENT_EFFECT_ESTIMATES";
  const first = rows[0];
  const estimate = numberValue(first.estimate ?? first.coefficient);
  const lower = numberValue(first.ci_lower);
  const upper = numberValue(first.ci_upper);
  const pValue = numberValue(first.p_value);
  const method = first.method || first.algorithm || "—";
  const estimand = first.estimand || (treatment ? context.estimand : "Edge coefficient") || "—";
  const title = treatment ? `${context.treatment_name || first.treatment || "Treatment"} → ${context.outcome_name || first.outcome || "Outcome"}` : `${first.source || "Source"} → ${first.target || "Target"}`;
  const scale = confidenceScale(lower, upper, estimate);
  root.innerHTML = `<div class="estimate-hero">
      <div class="primary-estimate"><small>${escapeHtml(estimand)}</small><strong>${formatNumber(estimate)}</strong></div>
      <div><small>95% confidence interval</small><strong>${formatNumber(lower)} — ${formatNumber(upper)}</strong></div>
      <div><small>p-value</small><strong>${formatPValue(pValue)}</strong></div>
      <div><small>Method</small><strong>${escapeHtml(method)}</strong></div>
    </div>
    <div class="confidence-plot"><i class="ci-line" style="left:${scale.lower}%;width:${Math.max(.3, scale.upper - scale.lower)}%"></i><i class="ci-dot" style="left:${scale.estimate}%"></i></div>
    <div class="result-section"><h3>${escapeHtml(title)}</h3>${renderEstimateTable(rows, treatment)}</div>
    ${context.selected_adjustment_variables?.length ? `<div class="result-section"><h3>Selected adjustment variables</h3><div class="chip-list">${context.selected_adjustment_variables.map(item => `<span class="chip">${escapeHtml(item.feature_name)}</span>`).join("")}</div></div>` : ""}
    ${context.diagnostics?.length ? `<div class="result-section"><h3>Diagnostics</h3><div class="chip-list">${context.diagnostics.map(item => `<span class="chip">${escapeHtml(item.diagnostic_type || item.name || "diagnostic")}: ${escapeHtml(item.status || "—")}</span>`).join("")}</div></div>` : ""}
    <div class="notice-box">${escapeHtml(context.scientific_notice || (treatment ? "推定値は宣言された因果仮定と診断の下で解釈してください。サービスは因果識別を自動証明しません。" : "Edge weights are exploratory coefficients and are not identified causal effects."))}</div>`;
}

function renderEstimateTable(rows, treatment) {
  return `<div class="data-table-wrap"><table class="data-table"><thead><tr>${(treatment ? ["Method", "Estimand", "Estimate", "95% CI", "p-value", "N", "Diagnostic"] : ["Algorithm", "Edge", "Coefficient", "95% CI", "p-value", "N", "Status"]).map(value => `<th>${value}</th>`).join("")}</tr></thead><tbody>${rows.map(row => `<tr>${treatment ? `
    <td><strong>${escapeHtml(row.method || "—")}</strong></td><td>${escapeHtml(row.estimand || "—")}</td><td>${formatNumber(numberValue(row.estimate))}</td><td>${formatNumber(numberValue(row.ci_lower))} — ${formatNumber(numberValue(row.ci_upper))}</td><td>${formatPValue(numberValue(row.p_value))}</td><td>${escapeHtml(row.sample_count || row.n || "—")}</td><td>${escapeHtml(row.diagnostic_status || row.status || "—")}</td>` : `
    <td><strong>${escapeHtml(row.algorithm || "—")}</strong></td><td>${escapeHtml(row.source || "—")} → ${escapeHtml(row.target || "—")}</td><td>${formatNumber(numberValue(row.coefficient))}</td><td>${formatNumber(numberValue(row.ci_lower))} — ${formatNumber(numberValue(row.ci_upper))}</td><td>${formatPValue(numberValue(row.p_value))}</td><td>${escapeHtml(row.sample_count || row.n || "—")}</td><td>${escapeHtml(row.status || "—")}</td>`}</tr>`).join("")}</tbody></table></div>`;
}

async function refreshResources() {
  const [datasets, runs, configurations, graphs] = await Promise.all([
    api(`/api/v1/datasets?project_id=${state.project.id}&limit=200`),
    api(`/api/v1/runs?project_id=${state.project.id}&limit=200`),
    api(`/api/v1/configurations?project_id=${state.project.id}`),
    api(`/api/v1/causal-graphs?project_id=${state.project.id}&limit=200`),
  ]);
  const [versionPages, configurationVersionLists] = await Promise.all([
    Promise.all(datasets.items.map(dataset => api(`/api/v1/datasets/${dataset.id}/versions?limit=200`))),
    Promise.all(configurations.map(config => api(`/api/v1/configurations/${config.id}/versions`))),
  ]);
  state.datasets = datasets.items;
  state.runs = runs.items;
  state.datasetVersions = versionPages.flatMap((page, index) => page.items.map(version => ({...version, dataset_name: datasets.items[index].name, dataset_kind: datasets.items[index].dataset_kind})));
  state.configurations = configurations;
  state.configurationVersions = configurationVersionLists.flatMap((versions, index) => versions.map(version => ({...version, configuration_type: configurations[index].configuration_type, configuration_name: configurations[index].name})));
  state.causalGraphs = graphs.items;
  renderAllProjectData();
}

async function delegatedClick(event) {
  const projectButton = event.target.closest("[data-open-project]");
  if (projectButton) {
    location.hash = `#/projects/${encodeURIComponent(projectButton.dataset.openProject)}/overview`;
    return;
  }
  const sectionButton = event.target.closest("[data-go-section]");
  if (sectionButton && state.project) location.hash = `#/projects/${state.project.id}/${sectionButton.dataset.goSection}`;
  const copyButton = event.target.closest("[data-copy]");
  if (copyButton) {
    await navigator.clipboard.writeText(copyButton.dataset.copy);
    toast("IDをクリップボードへコピーしました。", "success");
  }
  const saveButton = event.target.closest("[data-save-graph]");
  if (saveButton) await saveGraph(Number(saveButton.dataset.saveGraph));
  const discoveryButton = event.target.closest("[data-load-discovery-run]");
  if (discoveryButton) { $("#discovery-run-select").value = discoveryButton.dataset.loadDiscoveryRun; await loadDiscoveryFromRun(discoveryButton.dataset.loadDiscoveryRun); }
  const inferenceButton = event.target.closest("[data-load-inference-run]");
  if (inferenceButton) { $("#inference-run-select").value = inferenceButton.dataset.loadInferenceRun; await loadInferenceFromRun(inferenceButton.dataset.loadInferenceRun); }
  const refreshButton = event.target.closest("[data-refresh]");
  if (refreshButton) {
    setButtonBusy(refreshButton, true);
    try { await refreshResources(); toast("最新情報へ更新しました。", "success"); }
    catch (error) { toast(error.message, "error"); }
    finally { setButtonBusy(refreshButton, false); }
  }
}

function graphSvg(rawEdges, width = 760, height = 380) {
  const edges = normalizedEdges(rawEdges);
  const names = [...new Set(edges.flatMap(edge => [edge.source, edge.target]))];
  if (!names.length) return '<div class="graph-placeholder"><h3>edgeがありません</h3><p>このalgorithmは選択された条件で構造を検出しませんでした。</p></div>';
  const cx = width / 2, cy = height / 2, radius = Math.min(width, height) * .34;
  const points = Object.fromEntries(names.map((name, index) => {
    const angle = -Math.PI / 2 + index * Math.PI * 2 / names.length;
    return [name, {x: cx + Math.cos(angle) * radius, y: cy + Math.sin(angle) * radius}];
  }));
  const lineParts = edges.map(edge => {
    const a = points[edge.source], b = points[edge.target];
    const dx = b.x - a.x, dy = b.y - a.y, distance = Math.hypot(dx, dy) || 1;
    const offset = 31, x1 = a.x + dx / distance * offset, y1 = a.y + dy / distance * offset;
    const x2 = b.x - dx / distance * offset, y2 = b.y - dy / distance * offset;
    const orientation = String(edge.orientation || edge.edge_type || "directed").toLowerCase();
    const directed = !orientation.includes("undirected") && !orientation.includes("circle");
    const bidirected = orientation.includes("bidirected") || orientation.includes("<->");
    const confidence = numberValue(edge.stability ?? edge.score);
    const low = Number.isFinite(confidence) && confidence < .5;
    return `<line class="graph-edge ${low ? "low" : ""}" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" ${directed ? 'marker-end="url(#arrow)"' : ""} ${bidirected ? 'marker-start="url(#arrow-start)"' : ""}><title>${escapeHtml(edge.source)} → ${escapeHtml(edge.target)}${Number.isFinite(confidence) ? ` · score ${confidence.toFixed(3)}` : ""}</title></line>`;
  }).join("");
  const nodeParts = names.map(name => {
    const point = points[name], label = name.length > 18 ? `${name.slice(0, 16)}…` : name;
    return `<g class="graph-node" transform="translate(${point.x},${point.y})"><circle r="29"><title>${escapeHtml(name)}</title></circle><text>${escapeHtml(label)}</text></g>`;
  }).join("");
  return `<svg class="causal-graph" viewBox="0 0 ${width} ${height}" role="img" aria-label="${names.length} nodes and ${edges.length} edges causal discovery graph"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="#60736a"></path></marker><marker id="arrow-start" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 10 0 L 0 5 L 10 10 z" fill="#60736a"></path></marker></defs>${lineParts}${nodeParts}</svg>`;
}

function normalizedEdges(edges) {
  return (edges || []).map(normalizeKeys).map(edge => ({...edge, source: edge.source ?? edge.from, target: edge.target ?? edge.to})).filter(edge => edge.source != null && edge.target != null && edge.selected !== false && String(edge.selected).toLowerCase() !== "false");
}

function compareEdgeSets(left, right) {
  const key = edge => `${edge.source}|${edge.endpoint_source || edge.orientation || edge.edge_type || "tail"}|${edge.endpoint_target || "arrow"}|${edge.target}`;
  const a = new Set(normalizedEdges(left.edges).map(key)), b = new Set(normalizedEdges(right.edges).map(key));
  return {common: [...a].filter(value => b.has(value)).length, left: [...a].filter(value => !b.has(value)).length, right: [...b].filter(value => !a.has(value)).length};
}

function parseCsv(text) {
  if (typeof text !== "string" || !text.trim()) return [];
  const records = []; let record = [], field = "", quoted = false;
  for (let index = 0; index < text.length; index++) {
    const char = text[index];
    if (quoted) {
      if (char === '"' && text[index + 1] === '"') { field += '"'; index++; }
      else if (char === '"') quoted = false;
      else field += char;
    } else if (char === '"') quoted = true;
    else if (char === ",") { record.push(field); field = ""; }
    else if (char === "\n") { record.push(field.replace(/\r$/, "")); records.push(record); record = []; field = ""; }
    else field += char;
  }
  if (field || record.length) { record.push(field.replace(/\r$/, "")); records.push(record); }
  const [headers = [], ...rows] = records;
  return rows.filter(row => row.some(value => value !== "")).map(row => Object.fromEntries(headers.map((header, index) => [header.trim(), parseScalar(row[index] ?? "")])));
}

function parseScalar(value) {
  const trimmed = String(value).trim();
  if (trimmed === "") return null;
  if (/^(true|false)$/i.test(trimmed)) return trimmed.toLowerCase() === "true";
  if (/^-?(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?$/i.test(trimmed)) return Number(trimmed);
  return trimmed;
}

function normalizeKeys(object) {
  return Object.fromEntries(Object.entries(object || {}).map(([key, value]) => [key.trim().toLowerCase().replaceAll(" ", "_"), value]));
}

function confidenceScale(lower, upper, estimate) {
  const values = [lower, upper, estimate].filter(Number.isFinite);
  if (!values.length) return {lower: 25, upper: 75, estimate: 50};
  const extent = Math.max(...values.map(Math.abs), 0.001) * 1.2;
  const position = value => Number.isFinite(value) ? Math.max(2, Math.min(98, (value + extent) / (2 * extent) * 100)) : 50;
  return {lower: position(lower), upper: position(upper), estimate: position(estimate)};
}

function setFormBusy(form, busy, message) {
  const button = $('button[type="submit"]', form);
  if (message && busy) { message.textContent = ""; message.className = "form-message"; }
  setButtonBusy(button, busy);
  $$('input,select,textarea,button', form).forEach(control => {
    if (control !== button) control.disabled = busy;
  });
}

function setButtonBusy(button, busy) {
  if (!button) return;
  if (busy) { button.dataset.originalText = button.textContent; button.disabled = true; button.innerHTML = '<span class="spinner"></span> 処理中'; }
  else { button.disabled = false; if (button.dataset.originalText) { button.textContent = button.dataset.originalText; delete button.dataset.originalText; } }
}

function toast(message, type = "success") {
  const node = document.createElement("div");
  node.className = `toast ${type}`; node.textContent = message;
  $("#toast-region").append(node);
  setTimeout(() => node.remove(), 5200);
}

function statusPill(status) { return `<span class="mini-status status-${escapeAttr(status)}">${escapeHtml(status)}</span>`; }
function initials(name) { return String(name || "CA").split(/\s+/).filter(Boolean).slice(0, 2).map(word => word[0]).join("").toUpperCase(); }
function shortId(value) { const text = String(value || "—"); return text.length > 12 ? `${text.slice(0, 8)}…` : text; }
function inferAlgorithm(name) { return String(name || "algorithm").split(/[\\/]/).find(value => /^(pc|ges|lingam|notears)$/i.test(value)) || String(name || "algorithm").replace(/edges|\.csv/gi, "").replace(/[_-]+/g, " ").trim(); }
function slugify(value) { return String(value).toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 120) || `dataset-${Date.now()}`; }
function titleCase(value) { return String(value).replace(/[-_]+/g, " ").replace(/\b\w/g, char => char.toUpperCase()); }
function formatDate(value) { if (!value) return "—"; return new Intl.DateTimeFormat("ja-JP", {year: "numeric", month: "short", day: "numeric"}).format(new Date(value)); }
function formatDateTime(value) { if (!value) return "—"; return new Intl.DateTimeFormat("ja-JP", {month: "short", day: "numeric", hour: "2-digit", minute: "2-digit"}).format(new Date(value)); }
function formatBytes(bytes) { if (!Number.isFinite(bytes)) return ""; const units = ["B", "KB", "MB", "GB"]; const power = Math.min(Math.floor(Math.log(Math.max(bytes, 1)) / Math.log(1024)), units.length - 1); return `${(bytes / 1024 ** power).toFixed(power ? 1 : 0)} ${units[power]}`; }
function numberValue(value) { if (value == null || value === "") return NaN; const parsed = Number(value); return Number.isFinite(parsed) ? parsed : NaN; }
function formatNumber(value) { return Number.isFinite(value) ? new Intl.NumberFormat("ja-JP", {maximumSignificantDigits: 4}).format(value) : "—"; }
function formatPValue(value) { return Number.isFinite(value) ? value < .001 ? "< 0.001" : value.toFixed(3) : "—"; }
function escapeHtml(value) { const node = document.createElement("span"); node.textContent = String(value ?? ""); return node.innerHTML; }
function escapeAttr(value) { return escapeHtml(value).replaceAll('"', "&quot;"); }

initialize();
