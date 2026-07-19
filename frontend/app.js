const headers = {"Content-Type":"application/json", "X-User-Subject":"local-developer", "X-User-Name":"Local analyst"};
const projects = document.querySelector("#projects");
const summary = document.querySelector("#project-summary");
const dialog = document.querySelector("#project-dialog");

async function api(path, options={}) {
  const response = await fetch(path, {...options, headers:{...headers, ...(options.headers||{})}});
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) throw new Error(body?.error?.message || `HTTP ${response.status}`);
  return body;
}

async function loadProjects() {
  try {
    const page = await api("/api/v1/projects");
    summary.textContent = `${page.total} project${page.total === 1 ? "" : "s"}`;
    projects.innerHTML = page.items.length ? page.items.map(project => `
      <article class="project">
        <span class="slug">${escapeHtml(project.slug)}</span>
        <h3>${escapeHtml(project.name)}</h3>
        <p>${escapeHtml(project.description || "説明はまだありません。")}</p>
        <footer><span>${escapeHtml(project.status)}</span><time>${new Date(project.created_at).toLocaleDateString("ja-JP")}</time></footer>
      </article>`).join("") : `<div class="empty">最初のProjectを作成すると、DatasetとRunを整理できます。</div>`;
  } catch (error) {
    summary.textContent = "APIへ接続できません";
    projects.innerHTML = `<div class="empty">${escapeHtml(error.message)}</div>`;
  }
}

document.querySelector("#new-project").addEventListener("click", () => dialog.showModal());
document.querySelector("#close-dialog").addEventListener("click", () => dialog.close());
document.querySelector("#project-form").addEventListener("submit", async event => {
  event.preventDefault();
  const form = new FormData(event.currentTarget);
  const error = document.querySelector("#form-error");
  error.textContent = "";
  try {
    await api("/api/v1/projects", {method:"POST", body:JSON.stringify({slug:form.get("slug"), name:form.get("name"), description:form.get("description") || null})});
    event.currentTarget.reset(); dialog.close(); await loadProjects();
  } catch (cause) { error.textContent = cause.message; }
});

function escapeHtml(value) { const node=document.createElement("span"); node.textContent=String(value); return node.innerHTML; }
loadProjects();
