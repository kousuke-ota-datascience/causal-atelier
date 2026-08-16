/* URL-authoritative navigation state for project management workspaces. */
(function (global) {
  "use strict";

  const PROJECT_SECTIONS = Object.freeze(["overview", "context", "data", "results"]);

  class ProjectRouteError extends Error {
    constructor(code, message) {
      super(message);
      this.name = "ProjectRouteError";
      this.code = code;
    }
  }

  function routeError(code, message) {
    return new ProjectRouteError(code, message);
  }

  function normalizePath(pathname) {
    return pathname.replace(/\/+$/, "") || "/";
  }

  function projectRoute(projectId, section) {
    if (!PROJECT_SECTIONS.includes(section)) {
      throw routeError("PROJECT_SECTION_NOT_FOUND", `Unknown project section: ${section}`);
    }
    return Object.freeze({kind: "project", projectId: String(projectId), section});
  }

  function serialize(route) {
    if (route.kind === "collection") return "/projects";
    if (route.kind === "new") return "/projects/new";
    if (route.kind === "project") {
      return `/projects/${encodeURIComponent(route.projectId)}/${route.section}`;
    }
    throw routeError("PROJECT_ROUTE_NOT_FOUND", "Unknown project route");
  }

  function parse(pathname) {
    const path = normalizePath(pathname);
    if (path === "/projects") return Object.freeze({kind: "collection"});
    if (path === "/projects/new") return Object.freeze({kind: "new"});
    const overview = path.match(/^\/projects\/([^/]+)$/);
    if (overview) return projectRoute(decodeURIComponent(overview[1]), "overview");
    const match = path.match(/^\/projects\/([^/]+)\/(overview|context|data|results)$/);
    if (!match) throw routeError("PROJECT_ROUTE_NOT_FOUND", `Unknown project route: ${pathname}`);
    return projectRoute(decodeURIComponent(match[1]), match[2]);
  }

  function overview(projectId) {
    return projectRoute(projectId, "overview");
  }

  global.ProjectNavigation = Object.freeze({
    PROJECT_SECTIONS, ProjectRouteError, parse, serialize, overview, projectRoute,
  });
})(globalThis);
