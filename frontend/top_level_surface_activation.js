/* Exclusive presentation authority for Projects, Project Management, and Analysis. */
(function(global){
  const SURFACE_KINDS=Object.freeze({PROJECTS:'projects',PROJECT_MANAGEMENT:'project-management',ANALYSIS:'analysis'});
  const WORKSPACE_SURFACES=Object.freeze({
    projects:SURFACE_KINDS.PROJECTS,
    'project-new':SURFACE_KINDS.PROJECTS,
    management:SURFACE_KINDS.PROJECT_MANAGEMENT,
    context:SURFACE_KINDS.PROJECT_MANAGEMENT,
    data:SURFACE_KINDS.PROJECT_MANAGEMENT,
    results:SURFACE_KINDS.PROJECT_MANAGEMENT,
    explore:SURFACE_KINDS.ANALYSIS,
    discovery:SURFACE_KINDS.ANALYSIS,
    inference:SURFACE_KINDS.ANALYSIS,
    predictive:SURFACE_KINDS.ANALYSIS,
  });
  const ROOT_CONTENT=Object.freeze({
    [SURFACE_KINDS.PROJECTS]:Object.freeze({contentGroups:Object.freeze([Object.freeze({contentIds:Object.freeze(['projects','project-new'])})])}),
    [SURFACE_KINDS.PROJECT_MANAGEMENT]:Object.freeze({contentGroups:Object.freeze([Object.freeze({targetId:'project-management-section-content',contentIds:Object.freeze(['management','context','data','results'])})])}),
    [SURFACE_KINDS.ANALYSIS]:Object.freeze({contentGroups:Object.freeze([
      Object.freeze({targetId:'analysis-context-region',contentIds:Object.freeze(['analysis-context-header'])}),
      Object.freeze({targetId:'analysis-stage-main-area',contentIds:Object.freeze(['explore','discovery','inference','predictive'])}),
    ])}),
  });

  function surfaceForWorkspace(workspace){
    const surface=WORKSPACE_SURFACES[workspace];
    if(!surface)throw new Error(`Missing top-level surface for workspace: ${workspace}`);
    return surface;
  }

  function classifyRoute(pathname,catalog){
    try{
      const projectRoute=global.ProjectNavigation.parse(pathname);
      return projectRoute.kind==='project'?SURFACE_KINDS.PROJECT_MANAGEMENT:SURFACE_KINDS.PROJECTS;
    }catch(error){
      if(!(error instanceof global.ProjectNavigation.ProjectRouteError)||error.code!=='PROJECT_ROUTE_NOT_FOUND')throw error;
    }
    const analysisRoute=global.AnalysisNavigation.parse(pathname,catalog);
    if(analysisRoute.legacy||analysisRoute.projectId)return SURFACE_KINDS.ANALYSIS;
    throw new Error(`Unable to classify top-level surface for route: ${pathname}`);
  }

  function initialize(){
    for(const [surface,ownership] of Object.entries(ROOT_CONTENT)){
      const root=document.querySelector(`[data-top-level-surface-root="${surface}"]`);
      if(!root)throw new Error(`Missing top-level surface root: ${surface}`);
      for(const group of ownership.contentGroups){
        const target=group.targetId?document.getElementById(group.targetId):root;
        if(!target)throw new Error(`Missing top-level surface content target: ${group.targetId}`);
        for(const id of group.contentIds){
          const content=document.getElementById(id);
          if(!content)throw new Error(`Missing top-level surface content: ${id}`);
          target.append(content);
        }
      }
    }
  }

  function activate(surface){
    for(const root of document.querySelectorAll('[data-top-level-surface-root]')){
      const active=root.dataset.topLevelSurfaceRoot===surface;
      root.hidden=!active;
      root.setAttribute('aria-hidden',String(!active));
      root.classList.toggle('active',active);
    }
  }

  function activateForWorkspace(workspace){activate(surfaceForWorkspace(workspace));}

  global.TopLevelSurfaceActivation=Object.freeze({
    SURFACE_KINDS, surfaceForWorkspace, classifyRoute, initialize, activate, activateForWorkspace,
  });
})(globalThis);
