/* URL-authoritative navigation state for the analysis workspace. */
(function (global) {
  "use strict";

  const RESOURCE_TYPES = Object.freeze([
    "analysis-specification", "execution", "result", "graph-version",
  ]);

  class NavigationRouteError extends Error {
    constructor(code, message) {
      super(message);
      this.name = "NavigationRouteError";
      this.code = code;
    }
  }

  function routeError(code, message) {
    return new NavigationRouteError(code, message);
  }

  function familyForSlug(catalog, slug) {
    const family = catalog.families.find((item) => item.slug === slug);
    if (!family) throw routeError("NAVIGATION_FAMILY_NOT_FOUND", `Unknown analysis family: ${slug}`);
    return family;
  }

  function stageForSlug(family, slug) {
    const stage = family.stages.find((item) => item.slug === slug);
    if (!stage) throw routeError("NAVIGATION_STAGE_NOT_FOUND", `Unknown stage '${slug}' for ${family.slug}`);
    return stage;
  }

  function navigationContext(catalog, projectId, familySlug, stageSlug, resource) {
    const family = familyForSlug(catalog, familySlug);
    const stage = stageForSlug(family, stageSlug);
    if (resource && !RESOURCE_TYPES.includes(resource.resourceType)) {
      throw routeError("NAVIGATION_RESOURCE_TYPE_UNSUPPORTED", `Unsupported resource type: ${resource.resourceType}`);
    }
    return Object.freeze({
      projectId,
      familySlug: family.slug,
      stageSlug: stage.slug,
      resource: resource ? Object.freeze({ resourceType: resource.resourceType, resourceId: resource.resourceId }) : null,
    });
  }

  function serialize(context) {
    const base = `/projects/${encodeURIComponent(context.projectId)}/analysis/${encodeURIComponent(context.familySlug)}/${encodeURIComponent(context.stageSlug)}`;
    return context.resource
      ? `${base}/resource/${encodeURIComponent(context.resource.resourceType)}/${encodeURIComponent(context.resource.resourceId)}`
      : base;
  }

  function parse(pathname, catalog) {
    const path = pathname.replace(/\/+$/, "") || "/";
    const legacy = path.match(/^\/(?:projects\/([^/]+)\/)?(explore|predictive|causal)$/);
    if (legacy) return { legacy: legacy[2], projectId: legacy[1] ? decodeURIComponent(legacy[1]) : null };
    const match = path.match(/^\/projects\/([^/]+)\/analysis\/([^/]+)\/([^/]+)(?:\/resource\/([^/]+)\/([^/]+))?$/);
    if (!match) throw routeError("NAVIGATION_ROUTE_NOT_FOUND", `Unknown navigation route: ${pathname}`);
    const [, rawProjectId, rawFamilySlug, rawStageSlug, rawResourceType, rawResourceId] = match;
    const projectId = decodeURIComponent(rawProjectId);
    const familySlug = decodeURIComponent(rawFamilySlug);
    const stageSlug = decodeURIComponent(rawStageSlug);
    const resourceType = rawResourceType && decodeURIComponent(rawResourceType);
    const resourceId = rawResourceId && decodeURIComponent(rawResourceId);
    return navigationContext(catalog, projectId, familySlug, stageSlug,
      resourceType ? { resourceType, resourceId } : null);
  }

  function legacyContext(catalog, projectId, route) {
    const targets = Object.freeze({
      explore: ["exploratory", "profile"],
      predictive: ["predictive", "setup"],
      causal: ["causal", "setup"],
    });
    const target = targets[route];
    if (!target) throw routeError("NAVIGATION_ROUTE_NOT_FOUND", `Unknown legacy route: ${route}`);
    return navigationContext(catalog, projectId, target[0], target[1], null);
  }

  function defaultContext(catalog, projectId, familySlug, resource) {
    const family = familyForSlug(catalog, familySlug);
    return navigationContext(catalog, projectId, family.slug, family.default_stage_id, resource);
  }

  async function resourceFamily(api, projectId, resourceType, resourceId) {
    if (!RESOURCE_TYPES.includes(resourceType)) {
      throw routeError("NAVIGATION_RESOURCE_TYPE_UNSUPPORTED", `Unsupported resource type: ${resourceType}`);
    }
    if (resourceType === "analysis-specification") {
      return (await api(`/projects/${projectId}/analysis-specifications/${resourceId}`)).analysis_family.toLowerCase();
    }
    if (resourceType === "execution") {
      return (await api(`/executions/${resourceId}`)).analysis_family.toLowerCase();
    }
    if (resourceType === "result") {
      const result = await api(`/results/${resourceId}`);
      return (await api(`/executions/${result.execution_id}`)).analysis_family.toLowerCase();
    }
    await api(`/projects/${projectId}/graph-versions/${resourceId}`);
    return "causal";
  }

  async function contextForResource(catalog, api, projectId, resourceType, resourceId, explicit) {
    const actualFamilySlug = await resourceFamily(api, projectId, resourceType, resourceId);
    if (explicit && explicit.familySlug !== actualFamilySlug) {
      throw routeError("NAVIGATION_RESOURCE_FAMILY_MISMATCH", `Resource family ${actualFamilySlug} does not match route family ${explicit.familySlug}`);
    }
    const resource = { resourceType, resourceId };
    return explicit
      ? navigationContext(catalog, projectId, explicit.familySlug, explicit.stageSlug, resource)
      : defaultContext(catalog, projectId, actualFamilySlug, resource);
  }

  global.AnalysisNavigation = Object.freeze({
    RESOURCE_TYPES, NavigationRouteError, navigationContext, serialize, parse, legacyContext,
    defaultContext, contextForResource,
  });
})(globalThis);
