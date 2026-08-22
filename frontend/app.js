const API="/api/v1";
const state={projects:[],project:null,datasets:[],analysisViews:[],researchContexts:[],exploratoryResults:[],executions:[],results:[],unifiedResults:[],resultSummary:null,workspaceState:null,graphs:[],graphCandidates:[],graphCandidate:null,editingGraph:null,sourceGraph:null,predictiveCapabilities:null,predictiveSpecifications:[],predictiveExecutions:[],predictiveDetails:null,predictiveDraft:null,pendingArchive:null,navigationCatalog:null,navigationContext:null};
const $=(selector)=>document.querySelector(selector);
const $$=(selector)=>[...document.querySelectorAll(selector)];
const PROJECT_WORKSPACES=Object.freeze({overview:'management',context:'context',data:'data',results:'results'});
const LEGACY_PROJECT_ROUTES=Object.freeze({context:'context',data:'data',explore:'explore',causal:'causal',predictive:'predictive',results:'results'});
const LEGACY_PROJECT_WORKSPACES=Object.freeze({context:'context',data:'data',explore:'explore',causal:'discovery',predictive:'predictive',results:'results'});
const ANALYSIS_HISTORY_MODES=Object.freeze({PUSH:'PUSH',REPLACE:'REPLACE',NONE:'NONE'});
const NAVIGATION_ASYNC_STATES=Object.freeze(['IDLE','LOADING','READY','EMPTY','PARTIAL','ERROR','CANCELLED']);
const PREDICTIVE_RESULT_ORDER=Object.freeze(['SPLIT_RESULT','TRAINING_RESULT','EVALUATION_RESULT','ERROR_ANALYSIS_RESULT','PREDICTIVE_EXPLANATION_RESULT','MODEL_CARD_RESULT']);

async function api(path,options={}){
  const response=await fetch(API+path,options);
  if(!response.ok){
    let body={};try{body=await response.json()}catch{}
    const error=body.error||{};
    const details=Array.isArray(error.details?.errors)?error.details.errors.map(item=>{
      const location=Array.isArray(item.loc)?item.loc.filter(value=>value!=='body').join('.'):'request';
      return `${location||'request'}: ${item.msg||'invalid value'}`;
    }).join('; '):'';
    const summary=error.code?`${error.code}: ${error.message}`:(error.message||`${response.status} ${response.statusText}`);
    throw new Error(details?`${summary} (${details})`:summary);
  }
  if(response.status===204)return null;
  return response.json();
}
let noticeTimer=null;
function notice(message){const el=$("#notice");el.textContent=message;el.classList.add("show");if(noticeTimer)clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>el.classList.remove("show"),5000)}
function list(value){return value.split(/[,\n]/).map(x=>x.trim()).filter(Boolean)}
function escapeHtml(value){return String(value??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function idempotencyKey(){
  if(typeof globalThis.crypto?.randomUUID==="function")return globalThis.crypto.randomUUID();
  if(typeof globalThis.crypto?.getRandomValues==="function"){
    const bytes=globalThis.crypto.getRandomValues(new Uint8Array(16));
    bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
    const hex=[...bytes].map(value=>value.toString(16).padStart(2,"0"));
    return `${hex.slice(0,4).join("")}-${hex.slice(4,6).join("")}-${hex.slice(6,8).join("")}-${hex.slice(8,10).join("")}-${hex.slice(10).join("")}`;
  }
  // This key prevents duplicate commands; it is not used as a security token.
  return `web-${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}-${Math.random().toString(36).slice(2)}`;
}

function enhanceTooltips(){
  $$('label[data-tooltip]').forEach((label,index)=>{
    if(label.querySelector(':scope > .tooltip-trigger'))return;
    const id=`field-tooltip-${index}`;
    const trigger=document.createElement('button');
    trigger.type='button';trigger.className='tooltip-trigger';trigger.textContent='?';
    trigger.setAttribute('aria-label','入力項目の説明');trigger.setAttribute('aria-describedby',id);
    const content=document.createElement('span');
    content.id=id;content.className='tooltip-content';content.setAttribute('role','tooltip');
    content.textContent=label.dataset.tooltip||'';
    label.prepend(content);label.prepend(trigger);
  });
}
enhanceTooltips();
TopLevelSurfaceActivation.initialize();
TopLevelSurfaceActivation.activateForWorkspace($('.workspace.active')?.id||'projects');

async function activateWorkspace(workspace,{push=true,button=null,retainAnalysisShell=false}={}){
  button=button||$$('nav [data-workspace]').find(item=>item.dataset.workspace===workspace);
  if(button)button.dataset.refreshStatus='pending';
  $$('#project-management-navigation [data-workspace]').forEach(item=>{
    const current=item.dataset.workspace===workspace;
    item.classList.toggle('active',current);
    item.setAttribute('aria-current',current?'page':'false');
  });
  $$('.workspace').forEach(x=>x.classList.remove('active'));$('#'+workspace).classList.add('active');
  TopLevelSurfaceActivation.activateForWorkspace(workspace);
  if(push&&button?.dataset.route){
    const route=state.project
      ? ProjectNavigation.projectRoute(state.project.project_id,button.dataset.route)
      : {kind:'collection'};
    synchronizeProjectHistory(route,'PUSH');
  }
  if(!retainAnalysisShell)clearAnalysisNavigationShell();
  try{await refreshAll();if(button)button.dataset.refreshStatus='done'}catch(error){if(button)button.dataset.refreshStatus='failed';notice(error.message);throw error}
  const heading=$('.workspace.active h1');if(heading){heading.tabIndex=-1;heading.focus()}
}
function synchronizeProjectHistory(route,historyMode){
  const path=ProjectNavigation.serialize(route);
  if(location.pathname===path)return;
  if(historyMode==='PUSH')history.pushState({projectRoute:route},'',path);
  else if(historyMode==='REPLACE')history.replaceState({projectRoute:route},'',path);
  else if(historyMode!=='NONE')throw new Error(`Unknown project history mode: ${historyMode}`);
}
$$('nav [data-workspace]').forEach(button=>button.onclick=()=>{
  if(button.dataset.workspace==='management'&&!state.project){
    synchronizeProjectHistory({kind:'collection'},'PUSH');
    return activateWorkspace('projects',{push:false});
  }
  return activateWorkspace(button.dataset.workspace,{button});
});
$('#return-to-project-list').onclick=()=>{
  synchronizeProjectHistory({kind:'collection'},'PUSH');
  return activateWorkspace('projects',{push:false});
};

function normalizeAnalysisNavigationContext(context){
  if(!state.navigationCatalog)throw new Error('Navigation catalog is unavailable');
  return AnalysisNavigation.navigationContext(state.navigationCatalog,context.projectId,context.familySlug,context.stageSlug,context.resource);
}
function synchronizeAnalysisHistory(context,historyMode){
  const path=AnalysisNavigation.serialize(context);
  if(historyMode===ANALYSIS_HISTORY_MODES.NONE||location.pathname===path)return;
  if(historyMode===ANALYSIS_HISTORY_MODES.PUSH)history.pushState({project_id:context.projectId,navigation:context},'',path);
  else if(historyMode===ANALYSIS_HISTORY_MODES.REPLACE)history.replaceState({project_id:context.projectId,navigation:context},'',path);
  else throw new Error(`Unknown analysis history mode: ${historyMode}`);
}
async function applyAnalysisNavigation(context,{historyMode=ANALYSIS_HISTORY_MODES.NONE,source='unknown'}={}){
  const next=normalizeAnalysisNavigationContext(context);
  const presentation=AnalysisPresentation.resolve(next);
  state.project=await api(`/projects/${next.projectId}`);
  state.navigationContext=next;
  synchronizeAnalysisHistory(next,historyMode);
  renderAnalysisNavigation();
  activateAnalysisPresentation(next);
  await renderOperationAvailability();
  fillProject();await loadProjects();$('#project-select').value=next.projectId;
  await activateWorkspace(presentation.workspace,{push:false,retainAnalysisShell:true});
  return {context:next,source};
}
async function restoreProjectRoute(){
  if(location.pathname==='/'||location.pathname===''){
    synchronizeProjectHistory({kind:'collection'},'REPLACE');
    state.project=null;fillProject();await loadProjects();
    await activateWorkspace('projects',{push:false});
    return true;
  }
  if(state.navigationCatalog){
    let parsed;
    try{parsed=AnalysisNavigation.parse(location.pathname,state.navigationCatalog)}catch(error){
      if(error instanceof AnalysisNavigation.NavigationRouteError&&error.code==='NAVIGATION_ROUTE_NOT_FOUND')parsed=null;else throw error;
    }
    if(parsed?.legacy){
      const projectId=parsed.projectId||state.project?.project_id;
      if(!projectId)return false;
      parsed=AnalysisNavigation.legacyContext(state.navigationCatalog,projectId,parsed.legacy);
      return applyAnalysisNavigation(parsed,{historyMode:ANALYSIS_HISTORY_MODES.REPLACE,source:'legacy-route-normalization'}).then(()=>true);
    }
    if(parsed&&parsed.projectId){
      if(parsed.resource){parsed=await AnalysisNavigation.contextForResource(state.navigationCatalog,api,parsed.projectId,parsed.resource.resourceType,parsed.resource.resourceId,parsed)}
      await applyAnalysisNavigation(parsed,{historyMode:ANALYSIS_HISTORY_MODES.NONE,source:'route-restore'});
      return true;
    }
  }
  let route;
  try{route=ProjectNavigation.parse(location.pathname)}catch(error){
    if(!(error instanceof ProjectNavigation.ProjectRouteError)||error.code!=='PROJECT_ROUTE_NOT_FOUND')throw error;
    const legacy=location.pathname.match(/^\/projects\/([^/]+)\/(context|data|explore|causal|predictive|results)\/?$/);
    if(!legacy)return false;
    const [,projectId,legacyRoute]=legacy;
    const workspace=LEGACY_PROJECT_ROUTES[legacyRoute];
    state.project=await api(`/projects/${projectId}`);
    fillProject();await loadProjects();$('#project-select').value=projectId;
    await activateWorkspace(LEGACY_PROJECT_WORKSPACES[workspace],{push:false});
    return true;
  }
  if(route.kind==='collection'||route.kind==='new'){
    state.project=null;fillProject();await loadProjects();
    await activateWorkspace(route.kind==='collection'?'projects':'project-new',{push:false});
    return true;
  }
  state.project=await api(`/projects/${route.projectId}`);
  fillProject();await loadProjects();$('#project-select').value=route.projectId;
  synchronizeProjectHistory(route,'REPLACE');
  await activateWorkspace(PROJECT_WORKSPACES[route.section],{push:false});
  return true;
}
function clearAnalysisNavigationShell(){
  $('#analysis-family-tabs').replaceChildren();$('#analysis-stage-sidebar').replaceChildren();
  const contents=$('#analysis-stage-contents');if(contents){contents.hidden=true;contents.replaceChildren()}
  const presentation=$('#causal-stage-presentation');if(presentation){presentation.hidden=true;presentation.replaceChildren()}
  $('#analysis-routing-actions').replaceChildren();
  renderCausalStageSurface(null);
}
function renderAnalysisWorkspaceLauncher(){
  const target=$('#analysis-workspace-launcher');
  if(!target)return;
  const catalog=state.navigationCatalog,project=state.project;
  if(!catalog||!project){target.innerHTML='<button type="button" disabled>Projectを選択してください</button>';return}
  target.innerHTML=catalog.families.map(family=>'<button type="button" data-open-analysis-family="'+escapeHtml(family.slug)+'">'+escapeHtml(family.label)+' を開く</button>').join('');
  $$('[data-open-analysis-family]').forEach(button=>button.onclick=()=>{
    const context=AnalysisNavigation.defaultContext(catalog,project.project_id,button.dataset.openAnalysisFamily);
    applyAnalysisNavigation(context,{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'project-analysis-launch'}).catch(error=>notice(error.message));
  });
}
function renderAnalysisNavigation(){
  const catalog=state.navigationCatalog,context=state.navigationContext;if(!catalog||!context)return;
  const current=catalog.families.find(item=>item.slug===context.familySlug);if(!current)throw new Error('Navigation catalog invariant failure: current family missing');
  const currentStage=current.stages.find(item=>item.slug===context.stageSlug);if(!currentStage)throw new Error('Navigation catalog invariant failure: current stage missing');
  $('#analysis-family-tabs').innerHTML=catalog.families.map(f=>'<button type="button" role="tab" aria-selected="'+(f.slug===current.slug)+'" aria-label="Analysis family: '+escapeHtml(f.label)+'" data-family="'+escapeHtml(f.slug)+'">'+escapeHtml(f.label)+'</button>').join('');
  const stagePresentationFamily={...current,stages:current.stages.slice().sort((a,b)=>a.order-b.order)};
  $('#analysis-stage-sidebar').innerHTML=AnalysisStagePresentation.groupedStages(stagePresentationFamily).map(group=>'<section class="analysis-stage-sidebar-group">'+(group.label?'<p class="analysis-stage-sidebar-group-heading">'+escapeHtml(group.label)+'</p>':'')+group.stages.map(s=>'<button type="button" aria-current="'+(s.slug===context.stageSlug?'page':'false')+'" aria-label="Analysis stage: '+escapeHtml(s.label)+'" data-stage="'+escapeHtml(s.slug)+'">'+escapeHtml(s.label)+'</button>').join('')+'</section>').join('');
  const contents=$('#analysis-stage-contents');
  if(contents){
    const metadata=AnalysisStagePresentation.metadataFor(context);
    contents.hidden=false;
    contents.innerHTML='<div class="analysis-semantic-sections"><section class="analysis-semantic-section"><p class="analysis-stage-eyebrow">Stage Contents · '+escapeHtml(current.label)+'</p><h1 class="analysis-stage-heading">'+escapeHtml(currentStage.label)+'</h1><p><b>'+escapeHtml(current.label)+'</b> / '+escapeHtml(currentStage.label)+'</p></section><section class="analysis-semantic-section"><h2>目的</h2><p>'+escapeHtml(metadata.purpose)+'</p></section><section class="analysis-semantic-section"><h2>表示範囲</h2><p>選択中のAnalysis familyとstageを示します。入力resourceの作成・変更は行いません。</p></section></div>';
  }
  const routing=$('#analysis-routing-actions');
  routing.innerHTML='<button id="return-to-project-management" type="button">Project Managementへ戻る</button><button id="open-results-lineage" type="button">Results / Lineageを開く</button>';
  $('#return-to-project-management').onclick=()=>activateWorkspace('management').catch(error=>notice(error.message));
  $('#open-results-lineage').onclick=()=>activateWorkspace('results').catch(error=>notice(error.message));
  $$('#analysis-family-tabs button').forEach(button=>button.onclick=()=>{const family=catalog.families.find(f=>f.slug===button.dataset.family);applyAnalysisNavigation(AnalysisNavigation.defaultContext(catalog,state.project.project_id,family.slug),{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'family-tab-click'}).catch(error=>notice(error.message))});
  $$('#analysis-stage-sidebar button').forEach(button=>button.onclick=()=>applyAnalysisNavigation(AnalysisNavigation.navigationContext(catalog,state.project.project_id,current.slug,button.dataset.stage),{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'stage-sidebar-click'}).catch(error=>notice(error.message)));
}
function activateAnalysisPresentation(context){
  const target=$('#causal-stage-presentation');
  if(!target)return;
  if(!context||context.familySlug!=='causal'){target.hidden=true;target.replaceChildren();renderCausalStageSurface(null);renderExploratoryStageSurface(context?.familySlug==='exploratory'?context.stageSlug:null);renderPredictiveStageSurface(context?.familySlug==='predictive'?context.stageSlug:null);return}
  const presentation=CausalStagePresentation.presentationFor(context.stageSlug);
  target.hidden=false;
  target.innerHTML='<h2>'+escapeHtml(presentation.title)+'</h2><p>'+escapeHtml(presentation.summary)+'</p><ul>'+presentation.resources.map(resource=>'<li>'+escapeHtml(resource)+'</li>').join('')+'</ul>';
  renderCausalStageSurface(context.stageSlug);
  renderExploratoryStageSurface(null);
  renderPredictiveStageSurface(null);
}
function renderCausalStageSurface(stageSlug){
  $$('[data-causal-stage-surface]').forEach(surface=>{
    const stages=surface.dataset.causalStageSurface.split(/\s+/);
    surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);
  });
}
const EXPLORATORY_STAGE_OPERATIONS=Object.freeze({
  profile:['PROFILE'], distribution:['DISTRIBUTION'], relationships:['ASSOCIATION'],
  comparison:['GROUP_SUMMARY','TIME_TREND'], findings:['CHART'],
});
const EXPLORATORY_STAGE_RESULT_TYPES=Object.freeze({
  profile:['DATA_PROFILE_RESULT'], distribution:['DISTRIBUTION_RESULT'], relationships:['ASSOCIATION_RESULT'],
  comparison:['GROUP_SUMMARY_RESULT'], findings:null,
});
function renderExploratoryStageSurface(stageSlug){
  const form=$('#exploration-form'),operation=form?.elements.operation,dataQuality=$('#exploratory-data-quality'),results=$('#exploratory-results-surface');
  if(!form||!operation||!dataQuality||!results)return;
  const isDataQuality=stageSlug==='data-quality',allowed=EXPLORATORY_STAGE_OPERATIONS[stageSlug]||null;
  form.hidden=isDataQuality;
  results.hidden=isDataQuality;
  dataQuality.hidden=!isDataQuality;
  if(allowed){
    const selected=allowed.includes(operation.value)?operation.value:allowed[0];
    operation.innerHTML=allowed.map(value=>`<option value="${value}">${value}</option>`).join('');
    operation.value=selected;
  }
  if(isDataQuality)renderExploratoryDataQuality();
  renderExplorationResults();
}
function renderExploratoryDataQuality(){
  const target=$('#exploratory-data-quality');if(!target)return;
  const profile=state.exploratoryResults.find(result=>result.result_type==='DATA_PROFILE_RESULT');
  if(!profile){
    target.innerHTML='<h2>Data Quality availability</h2><p class="status">NO_PROFILE_RESULT</p><p>Data Qualityは既存Profile resultをread-onlyで表示します。Profileを先に実行してください。</p><button id="open-profile-from-data-quality" type="button">Profileへ戻る</button>';
    $('#open-profile-from-data-quality').onclick=()=>{
      if(!state.project||!state.navigationCatalog)return;
      const context=AnalysisNavigation.navigationContext(state.navigationCatalog,state.project.project_id,'exploratory','profile');
      applyAnalysisNavigation(context,{historyMode:ANALYSIS_HISTORY_MODES.PUSH,source:'data-quality-profile-return'}).catch(error=>notice(error.message));
    };
    return;
  }
  target.innerHTML='<h2>Data Quality availability</h2><p>既存Profile resultをread-onlyで表示します。</p><pre>'+escapeHtml(JSON.stringify({summary:profile.summary,payload:profile.payload,warnings:profile.warnings},null,2))+'</pre>';
}
const PREDICTIVE_STAGE_RESULT_TYPES=Object.freeze({
  train:['TRAINING_RESULT'], metrics:['EVALUATION_RESULT','ERROR_ANALYSIS_RESULT'],
  explainability:['PREDICTIVE_EXPLANATION_RESULT'], 'model-management':['MODEL_CARD_RESULT'],
});
const PREDICTIVE_STAGE_ARTIFACT_TYPES=Object.freeze({
  predict:['PREDICTION'], 'model-management':['FITTED_MODEL','MODEL_CARD'],
});
function renderPredictiveStageSurface(stageSlug){
  $$('[data-predictive-stage-surface]').forEach(surface=>{
    const stages=surface.dataset.predictiveStageSurface.split(/\s+/);
    surface.hidden=Boolean(stageSlug)&&!stages.includes(stageSlug);
  });
  renderPredictiveDetails();
}
async function renderOperationAvailability(){
  const el=$('#operation-availability'),context=state.navigationContext;if(!state.project||!context){el.textContent='IDLE';return}el.textContent='LOADING';
  try{const resource=context.resource,query=new URLSearchParams({route:AnalysisNavigation.serialize(context)});if(resource){query.set('resource_type',resource.resourceType);query.set('resource_id',resource.resourceId)}const data=await api('/projects/'+state.project.project_id+'/operation-availability?'+query);el.innerHTML=Object.entries(data.operations).map(([name,value])=>'<span class="status" aria-label="'+escapeHtml(name)+' '+(value.allowed?'available':'unavailable: '+value.reason_code)+'">'+escapeHtml(name)+': '+(value.allowed?'READY':escapeHtml(value.reason_code))+'</span>').join(' ')}catch(error){el.textContent='ERROR: '+error.message}
}
window.addEventListener('popstate',()=>restoreProjectRoute().catch(error=>notice(error.message)));

async function loadProjects(){
  const data=await api('/projects');state.projects=data.items;const select=$('#project-select');
  select.innerHTML='<option value="">Projectを選択</option>'+data.items.map(p=>`<option value="${p.project_id}">${escapeHtml(p.name)}</option>`).join('');
  if(state.project){select.value=state.project.project_id}
  $('#project-list').innerHTML=data.items.length?`<table><thead><tr><th>Name</th><th>Topic</th><th>Objective</th><th>Status</th></tr></thead><tbody>${data.items.map(p=>`<tr><td><button type="button" class="link-button" onclick="selectProject('${p.project_id}')">${escapeHtml(p.name)}</button></td><td>${escapeHtml(p.topic||'—')}</td><td>${escapeHtml(p.objective||'—')}</td><td><span class="status">${p.status}</span></td></tr>`).join('')}</tbody></table>`:'ACTIVE Projectはありません';
}
$('#new-project').onclick=async()=>{state.project=null;fillProject();synchronizeProjectHistory({kind:'new'},'PUSH');await activateWorkspace('project-new',{push:false})};
$('#cancel-project-register').onclick=async()=>{synchronizeProjectHistory({kind:'collection'},'PUSH');await activateWorkspace('projects',{push:false})};
$('#project-select').onchange=async event=>{state.project=event.target.value?await api(`/projects/${event.target.value}`):null;fillProject();if(state.project){synchronizeProjectHistory(ProjectNavigation.overview(state.project.project_id),'PUSH');await activateWorkspace('management',{push:false})}else{synchronizeProjectHistory({kind:'collection'},'PUSH');await activateWorkspace('projects',{push:false})}};
window.selectProject=async id=>{state.project=await api(`/projects/${id}`);fillProject();await loadProjects();synchronizeProjectHistory(ProjectNavigation.overview(id),'PUSH');await activateWorkspace('management',{push:false})};
function fillProject(){const form=$('#project-form');for(const name of ['name','topic','objective','memo'])form.elements[name].value=state.project?.[name]||'';$('#overview-project-name').textContent=state.project?.name||'Projectを選択してください';$('#overview-project-status').textContent=state.project?.status||'—';$('#project-management-project-name').textContent=state.project?.name||'Project未選択';$('#archive-project').disabled=!state.project;renderAnalysisContext();renderAnalysisWorkspaceLauncher()}

function renderAnalysisContext(){
  const workspace=state.workspaceState;
  $('#analysis-context-project-name').textContent=state.project?.name||'Project未選択';
  $('#analysis-context-project-status').textContent=state.project?.status||'—';
  $('#common-role').textContent=workspace?.current_role||'—';
  $('#unsaved-draft-indicator').textContent=workspace?.unsaved_draft?'UNSAVED DRAFT':'保存済み';
  $('#unsaved-draft-indicator').classList.toggle('unsaved',Boolean(workspace?.unsaved_draft));
  const context=$('#common-context'),dataset=$('#common-dataset'),view=$('#common-view');
  const contextValue=workspace?.research_context_version_id||'';
  const datasetValue=workspace?.dataset_version_id||'';
  const viewValue=workspace?.analysis_view_id||'';
  context.innerHTML='<option value="">未選択</option>'+state.researchContexts.filter(item=>item.status==='FIXED').map(item=>`<option value="${item.research_context_version_id}">${escapeHtml(item.context_key)} / v${item.version_number}</option>`).join('');
  dataset.innerHTML='<option value="">未選択</option>'+state.datasets.map(item=>`<option value="${item.dataset_version_id}">${escapeHtml(item.name)} / ${escapeHtml(item.version_label)}</option>`).join('');
  view.innerHTML='<option value="">未選択</option>'+state.analysisViews.filter(item=>item.status==='FIXED'&&(!datasetValue||item.source_dataset_version_id===datasetValue)).map(item=>`<option value="${item.analysis_view_id}">${escapeHtml(item.name)} / v${item.version_number}</option>`).join('');
  const invalid=[];
  for(const [select,value,label] of [[context,contextValue,'Research Context'],[dataset,datasetValue,'Dataset Version'],[view,viewValue,'Analysis View']]){
    const available=[...select.options].some(item=>item.value===value);
    select.value=available?value:'';
    select.disabled=!state.project;
    if(value&&!available)invalid.push(label);
  }
  const selectionStatus=$('#common-selection-status');
  selectionStatus.textContent=invalid.length?`保存済み選択を復元できません: ${invalid.join(', ')}`:'';
}

async function loadWorkspaceState(){
  if(!state.project){state.workspaceState=null;renderAnalysisContext();return}
  state.workspaceState=await api(`/projects/${state.project.project_id}/workspace-state`);
  renderAnalysisContext();
}

async function saveWorkspaceState(changes){
  if(!state.project)return;
  state.workspaceState=await api(`/projects/${state.project.project_id}/workspace-state`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(changes)});
  renderAnalysisContext();
}

function saveCommonWorkspaceSelection(changes){
  saveWorkspaceState(changes).catch(async error=>{
    notice(error.message);
    await loadWorkspaceState().catch(restoreError=>notice(restoreError.message));
  });
}
$('#common-context').onchange=event=>saveCommonWorkspaceSelection({research_context_version_id:event.target.value||null});
$('#common-dataset').onchange=event=>saveCommonWorkspaceSelection({dataset_version_id:event.target.value||null,analysis_view_id:null});
$('#common-view').onchange=event=>saveCommonWorkspaceSelection({analysis_view_id:event.target.value||null});
$('#project-register-form').onsubmit=async event=>{event.preventDefault();try{state.project=await api('/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(event.target)))});event.target.reset();await loadProjects();$('#project-select').value=state.project.project_id;fillProject();synchronizeProjectHistory(ProjectNavigation.overview(state.project.project_id),'REPLACE');await activateWorkspace('management',{push:false});notice('Projectを登録しました')}catch(error){notice(error.message)}};
$('#project-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('ACTIVE Projectを選択してください');try{const body=Object.fromEntries(new FormData(event.target));state.project=await api(`/projects/${state.project.project_id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});await loadProjects();$('#project-select').value=state.project.project_id;notice('Project metadataを更新しました')}catch(error){notice(error.message)}};
window.requestArchive=id=>{state.pendingArchive=id;$('#archive-modal').showModal()};
$('#archive-project').onclick=()=>{if(state.project)requestArchive(state.project.project_id)};
$('#confirm-archive').onclick=async()=>{if(!state.pendingArchive)return;try{await api(`/projects/${state.pendingArchive}`,{method:'DELETE'});if(state.project?.project_id===state.pendingArchive){state.project=null;state.workspaceState=null;state.unifiedResults=[];fillProject();state.datasets=[];state.executions=[];state.results=[];state.graphs=[];state.graphCandidates=[];state.researchContexts=[];state.predictiveExecutions=[]}state.pendingArchive=null;$('#archive-modal').close();await loadProjects();$('#project-select').value='';synchronizeProjectHistory({kind:'collection'},'PUSH');await activateWorkspace('projects',{push:false});notice('ProjectをARCHIVEDへ変更しました。既存Lineageは保持されます')}catch(error){notice(error.message)}};

$('#dataset-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');try{const form=new FormData(event.target);await api(`/projects/${state.project.project_id}/dataset-versions`,{method:'POST',headers:{'Idempotency-Key':idempotencyKey()},body:form});event.target.reset();await loadDatasets();notice('Dataset Versionを登録しました')}catch(error){notice(error.message)}};
async function loadDatasets(){
  if(!state.project){state.datasets=[];return}
  state.datasets=(await api(`/projects/${state.project.project_id}/dataset-versions`)).items;
  $('#datasets').innerHTML=state.datasets.length?`<table><thead><tr><th>Name</th><th>Version</th><th>Schema</th><th>Rows × Columns</th><th>Hash</th><th></th></tr></thead><tbody>${state.datasets.map(d=>`<tr><td>${escapeHtml(d.name)}</td><td>${escapeHtml(d.version_label)}</td><td>${escapeHtml(Object.entries(d.schema).map(([name,type])=>`${name}:${type}`).join(', '))}</td><td>${d.row_count} × ${d.column_count}</td><td>${d.content_hash.slice(0,12)}</td><td><button onclick="preview('${d.dataset_version_id}')">Preview</button></td></tr>`).join('')}</tbody></table>`:'Datasetはありません';
  $$('.datasets-select').forEach(select=>{const selected=select.dataset.selectedDatasetVersionId||select.value;select.innerHTML='<option value="">選択</option>'+state.datasets.map(d=>`<option value="${d.dataset_version_id}">${escapeHtml(d.name)} / ${escapeHtml(d.version_label)}</option>`).join('');if(state.datasets.some(d=>d.dataset_version_id===selected)){select.value=selected;select.dataset.selectedDatasetVersionId=selected}});
  refreshPredictiveFeatureSelectorAvailability();renderPredictiveFeatureContext();
  updatePredictiveAvailability();
}
window.preview=async id=>{try{const p=await api(`/dataset-versions/${id}/preview?limit=10`);$('#preview').innerHTML=`<h3>Preview</h3><table><thead><tr>${p.columns.map(c=>`<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>${p.rows.map(row=>`<tr>${p.columns.map(c=>`<td>${escapeHtml(row[c])}</td>`).join('')}</tr>`).join('')}</tbody></table>`}catch(error){notice(error.message)}};
document.addEventListener('change',event=>{const select=event.target;if(select instanceof HTMLSelectElement&&select.classList.contains('datasets-select'))select.dataset.selectedDatasetVersionId=select.value});

async function loadAnalysisViews(){
  if(!state.project){state.analysisViews=[];renderAnalysisViews();return}
  state.analysisViews=(await api(`/projects/${state.project.project_id}/analysis-views`)).items;
  renderAnalysisViews();
}
function renderAnalysisViews(){
  const target=$('#analysis-view-list');if(!target)return;
  target.innerHTML=state.analysisViews.length?`<table><thead><tr><th>Name / Version</th><th>Status</th><th>Rows</th><th>Hash</th><th>Operation</th></tr></thead><tbody>${state.analysisViews.map(view=>`<tr><td>${escapeHtml(view.name)} / v${view.version_number}</td><td><span class="status ${view.status}">${view.status}</span></td><td>${view.manifest.output_row_count??'—'}</td><td>${escapeHtml((view.content_hash||'draft').slice(0,12))}</td><td>${view.status==='DRAFT'?`<button type="button" onclick="fixAnalysisView('${view.analysis_view_id}')">Validate &amp; FIX</button>`:'immutable'}</td></tr>`).join('')}</tbody></table>`:'Analysis Viewはありません';
  const selected=$('#exploration-view')?.value||'';
  if($('#exploration-view')){$('#exploration-view').innerHTML='<option value="">Dataset Version全体</option>'+state.analysisViews.filter(view=>view.status==='FIXED').map(view=>`<option value="${view.analysis_view_id}">${escapeHtml(view.name)} / v${view.version_number}</option>`).join('');$('#exploration-view').value=state.analysisViews.some(view=>view.analysis_view_id===selected)?selected:''}
  const predictiveSelected=$('#predictive-view')?.value||'';
  if($('#predictive-view')){$('#predictive-view').innerHTML='<option value="">Dataset Version全体</option>'+state.analysisViews.filter(view=>view.status==='FIXED').map(view=>`<option value="${view.analysis_view_id}">${escapeHtml(view.name)} / v${view.version_number}</option>`).join('');$('#predictive-view').value=state.analysisViews.some(view=>view.analysis_view_id===predictiveSelected)?predictiveSelected:''}
  updatePredictiveAvailability();
}
$('#analysis-view-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');const form=new FormData(event.target);try{const spec=JSON.parse(String(form.get('spec')));spec.source_dataset_version_id=String(form.get('dataset_version_id'));await api(`/projects/${state.project.project_id}/analysis-views`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({view_key:form.get('view_key'),name:form.get('name'),spec})});await loadAnalysisViews();notice('Analysis View DRAFTを作成しました')}catch(error){notice(error instanceof SyntaxError?'View specification JSONが不正です':error.message)}};
window.fixAnalysisView=async id=>{try{await api(`/projects/${state.project.project_id}/analysis-views/${id}/validate`,{method:'POST'});await api(`/projects/${state.project.project_id}/analysis-views/${id}/fix`,{method:'POST'});await loadAnalysisViews();notice('Analysis Viewを検証してFIXEDにしました')}catch(error){notice(error.message)}};
$('#refresh-analysis-views').onclick=async event=>{event.currentTarget.dataset.refreshStatus='pending';try{await loadAnalysisViews();event.currentTarget.dataset.refreshStatus='done'}catch(error){event.currentTarget.dataset.refreshStatus='failed';notice(error.message)}};

function explorationRequest(){
  const form=new FormData($('#exploration-form')),operation=String(form.get('operation')),columns=list(String(form.get('columns')||'')),grouping=list(String(form.get('grouping')||'')),aggregationColumn=String(form.get('aggregation_column')||'').trim(),x=String(form.get('chart_x')||'').trim(),y=String(form.get('chart_y')||'').trim();
  const familySpec={schema_version:'exploratory-analysis-spec/1',operation,columns,grouping,aggregation:{method:String(form.get('aggregation_method')),column:aggregationColumn||null},chart_encoding:{mark:String(form.get('mark')),x:x||null,y:y||null},filter:null,sampling:operation==='CHART'?{size:1000}:null,expected_output_type:null};
  return {dataset_version_id:String(form.get('dataset_version_id')),analysis_view_id:String(form.get('analysis_view_id')||'')||null,family_spec:familySpec};
}
function renderExplorationResult(result,target=$('#exploration-output')){target.innerHTML=`<div class="badge-row"><span class="family-label">EXPLORATORY</span><span class="status">${escapeHtml(result.analytical_status)}</span><span>${escapeHtml(result.result_type)}</span></div><p>探索的結果です。因果効果または確認的結論ではありません。</p><pre>${escapeHtml(JSON.stringify({summary:result.summary,payload:result.payload,warnings:result.warnings},null,2))}</pre>`}
$('#preview-exploration').onclick=async()=>{if(!state.project)return notice('Projectを選択してください');try{const result=await api(`/projects/${state.project.project_id}/exploration/preview`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(explorationRequest())});renderExplorationResult(result);notice('未保存Previewを生成しました')}catch(error){notice(error.message)}};
async function waitForExploration(executionId){for(let attempt=0;attempt<60;attempt+=1){const execution=await api(`/projects/${state.project.project_id}/exploration/executions/${executionId}`);if(execution.status==='SUCCEEDED')return execution;if(execution.status==='FAILED')throw new Error(execution.last_error?.message||'Exploration execution failed');if(execution.status==='CANCELLED')throw new Error('Exploration execution was cancelled');await new Promise(resolve=>setTimeout(resolve,250))}throw new Error('Exploration execution is still running. 更新ボタンで再確認してください')}
$('#exploration-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');try{const response=await api(`/projects/${state.project.project_id}/exploration/executions`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(explorationRequest())});if(response.status==='QUEUED')notice('探索Executionをキューへ登録しました');await waitForExploration(response.execution_id);await loadExplorationResults();notice('EXPLORATORY Resultを保存しました')}catch(error){notice(error.message)}};
async function loadExplorationResults(){if(!state.project){state.exploratoryResults=[];renderExplorationResults();return}state.exploratoryResults=(await api(`/projects/${state.project.project_id}/exploration/results`)).items;renderExplorationResults()}
function visibleExploratoryResults(){const stage=state.navigationContext?.familySlug==='exploratory'?state.navigationContext.stageSlug:null,types=EXPLORATORY_STAGE_RESULT_TYPES[stage];return types?state.exploratoryResults.filter(result=>types.includes(result.result_type)):state.exploratoryResults}
function renderExplorationResults(){const target=$('#exploration-results');if(!target)return;const results=visibleExploratoryResults();target.innerHTML=results.length?`<table><thead><tr><th>Family</th><th>Result</th><th>Status</th><th>Summary</th><th>Explicit transition</th></tr></thead><tbody>${results.map(result=>`<tr><td><span class="family-label">EXPLORATORY</span></td><td>${escapeHtml(result.result_type)}</td><td>${escapeHtml(result.analytical_status)}</td><td>${escapeHtml(JSON.stringify(result.summary))}</td><td><div class="explore-actions"><button type="button" onclick="showExploration('${result.result_id}')">表示</button><button type="button" onclick="createExplorationDraft('${result.result_id}','CAUSAL')">Causal draft</button><button type="button" onclick="createExplorationDraft('${result.result_id}','PREDICTIVE')">Predictive draft</button></div></td></tr>`).join('')}</tbody></table>`:'保存済み探索Resultはありません'}
window.showExploration=id=>{const result=state.exploratoryResults.find(value=>value.result_id===id);if(result)renderExplorationResult(result)};
window.createExplorationDraft=async(id,family)=>{try{const researchContextVersionId=$('#common-context').value;const draft=await api(`/projects/${state.project.project_id}/exploration/results/${id}/create-analysis-draft`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_family:family,analysis_mode:'EXPLORATORY',research_context_version_id:researchContextVersionId||undefined})});notice(`${family} draftを作成しました: ${draft.source_relation.warning}`)}catch(error){notice(error.message)}};
$('#refresh-exploration').onclick=async event=>{event.currentTarget.dataset.refreshStatus='pending';try{await loadExplorationResults();event.currentTarget.dataset.refreshStatus='done'}catch(error){event.currentTarget.dataset.refreshStatus='failed';notice(error.message)}};

function updatePredictiveAvailability(){
  const button=$('#run-predictive');if(!button)return;
  const backendAvailable=state.predictiveCapabilities?.training_available===true&&state.predictiveCapabilities?.evaluation_available===true&&state.predictiveCapabilities?.explanation_available===true&&state.predictiveCapabilities?.model_card_available===true;
  const fixedContext=state.researchContexts.some(context=>context.status==='FIXED');
  button.disabled=!(backendAvailable&&fixedContext&&state.datasets.length>0);
  button.title=backendAvailable?'':'Backend capabilitiesにより現在のPredictive operationは利用できません';
}

function renderResearchContexts(){
  const fixed=state.researchContexts.filter(context=>context.status==='FIXED');
  const summary=$('#research-context-summary');
  if(summary)summary.innerHTML=fixed.length?fixed.map(context=>`<article><b>${escapeHtml(context.context_key)} / v${context.version_number}</b><p>${escapeHtml(context.problem_statement)}</p><p>${escapeHtml((context.research_questions||[]).join(' / '))}</p><small>${escapeHtml(context.canonical_hash||'')}</small></article>`).join(''):'固定済みResearch Contextはありません。';
  const metadata=$('#context-project-metadata');
  if(metadata)metadata.innerHTML=state.project?`<p><b>Topic</b> ${escapeHtml(state.project.topic||'—')}</p><p><b>Objective</b> ${escapeHtml(state.project.objective||'—')}</p><p><b>Memo</b> ${escapeHtml(state.project.memo||'—')}</p>`:'Projectを選択してください。';
  const history=$('#research-context-history');
  if(history)history.innerHTML=state.researchContexts.length?`<table><thead><tr><th>Key / Version</th><th>Status</th><th>Question</th><th></th></tr></thead><tbody>${state.researchContexts.map(context=>`<tr><td>${escapeHtml(context.context_key)} / v${context.version_number}</td><td><span class="status ${context.status}">${context.status}</span></td><td>${escapeHtml((context.research_questions||[]).join(' / '))}</td><td><button type="button" onclick="editResearchContext('${context.research_context_version_id}')">表示${context.status==='DRAFT'?'・編集':''}</button></td></tr>`).join('')}</tbody></table>`:'Research Contextはありません。';
  const select=$('#predictive-context');if(!select)return;
  const selected=select.value;
  select.innerHTML='<option value="">FIXED Contextを選択</option>'+fixed.map(context=>`<option value="${context.research_context_version_id}">${escapeHtml(context.context_key)} / v${context.version_number}</option>`).join('');
  if(fixed.some(context=>context.research_context_version_id===selected))select.value=selected;
  renderAnalysisContext();
  updatePredictiveAvailability();
}

function contextFormPayload(){
  const form=$('#research-context-form'),values=new FormData(form);
  let decisionContext,relations;
  try{decisionContext=JSON.parse(String(values.get('decision_context')||'{}'));relations=JSON.parse(String(values.get('relations')||'[]'))}catch{throw new Error('Decision contextまたはRelationsのJSONが不正です')}
  if(!decisionContext||Array.isArray(decisionContext)||typeof decisionContext!=='object')throw new Error('Decision contextはJSON objectで指定してください');
  if(!Array.isArray(relations))throw new Error('RelationsはJSON arrayで指定してください');
  return {context_key:String(values.get('context_key')),problem_statement:String(values.get('problem_statement')),research_questions:list(String(values.get('research_questions'))),significance:String(values.get('significance')||'')||null,hypotheses:list(String(values.get('hypotheses')||'')),decision_context:decisionContext,relations};
}

window.editResearchContext=async id=>{
  const context=state.researchContexts.find(item=>item.research_context_version_id===id);if(!context)return;
  const form=$('#research-context-form');form.elements.research_context_version_id.value=id;form.elements.context_key.value=context.context_key;form.elements.problem_statement.value=context.problem_statement;form.elements.research_questions.value=(context.research_questions||[]).join('\n');form.elements.significance.value=context.significance||'';form.elements.hypotheses.value=(context.hypotheses||[]).join('\n');form.elements.decision_context.value=JSON.stringify(context.decision_context||{},null,2);form.elements.relations.value=JSON.stringify(context.relations||[],null,2);$('#update-context').disabled=context.status==='FIXED';$('#fix-context').disabled=context.status==='FIXED';
  try{const usage=await api(`/projects/${state.project.project_id}/research-contexts/${id}/usage`);$('#research-context-usage').innerHTML=`<p>Analysis Specifications: ${usage.analysis_specification_ids.length} / Executions: ${usage.execution_ids.length}</p><pre>${escapeHtml(JSON.stringify(usage,null,2))}</pre>`}catch(error){notice(error.message)}
};

$('#research-context-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');try{const payload=contextFormPayload();await api(`/projects/${state.project.project_id}/research-contexts`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});event.target.reset();await loadPredictiveWorkspace();await saveWorkspaceState({unsaved_draft:false});notice('Research Context DRAFTを作成しました')}catch(error){notice(error.message)}};
$('#update-context').onclick=async()=>{const form=$('#research-context-form'),id=form.elements.research_context_version_id.value;if(!id)return notice('編集するDRAFT versionを選択してください');try{const payload=contextFormPayload();delete payload.context_key;await api(`/projects/${state.project.project_id}/research-contexts/${id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});await loadPredictiveWorkspace();await saveWorkspaceState({unsaved_draft:false});notice('Research Context DRAFTを保存しました')}catch(error){notice(error.message)}};
$('#fix-context').onclick=async()=>{const id=$('#research-context-form').elements.research_context_version_id.value;if(!id)return notice('FIXED化するDRAFT versionを選択してください');try{const context=await api(`/projects/${state.project.project_id}/research-contexts/${id}/fix`,{method:'POST'});await loadPredictiveWorkspace();await saveWorkspaceState({research_context_version_id:context.research_context_version_id,unsaved_draft:false});notice('Research ContextをFIXED化しました。以後は上書きできません')}catch(error){notice(error.message)}};

function predictiveFamilySpec(){
  const form=new FormData($('#predictive-form')),task=String(form.get('task_type')),target=String(form.get('target')).trim(),features=list(String(form.get('feature_columns')||'')),excluded=[...new Set([...list(String(form.get('excluded_columns')||'')),target])],strategy=String(form.get('split_strategy')),seed=Number(form.get('seed'));
  if(task==='REGRESSION'&&strategy==='STRATIFIED')throw new Error('RegressionではSTRATIFIED splitを使用できません');
  let configuredAvailability={};try{configuredAvailability=JSON.parse(String(form.get('feature_availability')||'{}'))}catch{throw new Error('Feature availability JSONが不正です')}
  if(!configuredAvailability||Array.isArray(configuredAvailability)||typeof configuredAvailability!=='object')throw new Error('Feature availability JSONはobjectで指定してください');
  const availability=Object.fromEntries(features.map(column=>[column,configuredAvailability[column]||{column,available_at:'PREDICTION_TIME',allowed:true}]));
  const classification=task==='BINARY_CLASSIFICATION';
  const modelId=String(form.get('model_id'))||(classification?'logistic_regression.v1':'linear_regression.v1');
  const primaryMetric=String(form.get('primary_metric'))||(classification?'ROC_AUC':'RMSE');
  return {schema_version:'predictive-analysis-spec/1',task_type:task,prediction_question:{prediction_unit:String(form.get('prediction_unit')),target,prediction_time:String(form.get('prediction_time')),horizon:String(form.get('horizon')),intended_use:String(form.get('intended_use')),deployment_population:String(form.get('deployment_population'))},feature_spec:{feature_columns:features,availability_cutoff:availability,excluded_columns:excluded},split_spec:{strategy,train_ratio:Number(form.get('train_ratio')),validation_ratio:Number(form.get('validation_ratio')),test_ratio:Number(form.get('test_ratio')),group_column:String(form.get('group_column')||'')||null,time_column:String(form.get('time_column')||'')||null,train_cutoff:String(form.get('train_cutoff')||'')||null,validation_cutoff:String(form.get('validation_cutoff')||'')||null,stratify:strategy==='STRATIFIED',seed},preprocessing_spec:{fit_partition:'TRAIN',numeric_imputation:'MEAN',scale_numeric:form.get('scale_numeric')==='on',categorical_encoding:'ONE_HOT'},model_spec:{model_id:modelId,parameters:modelId==='logistic_regression.v1'?{iterations:800,learning_rate:0.1,l2:0.001}:{l2:0}},tuning_spec:{selection_partitions:list(String(form.get('tuning_selection')||'TRAIN,VALIDATION'))},evaluation_spec:{primary_metric:primaryMetric,secondary_metrics:list(String(form.get('secondary_metrics')||'')),subgroups:list(String(form.get('subgroups')||''))},explanation_spec:{method:String(form.get('explanation_method')),dataset:'TEST',sampling:{strategy:'FIRST_N',size:Number(form.get('explanation_sample_size')),seed},local_explanations:form.get('local_explanations')==='on'}};
}

function capturePredictiveDraft(){
  const form=$('#predictive-form');if(!form)return;
  state.predictiveDraft=Object.fromEntries([...form.elements].filter(element=>element.name).map(element=>[element.name,element.type==='checkbox'?element.checked:element.value]));
}
function restorePredictiveDraft(){
  const form=$('#predictive-form'),draft=state.predictiveDraft;if(!form||!draft)return;
  for(const [name,value] of Object.entries(draft)){const element=form.elements[name];if(!element)continue;if(element.type==='checkbox')element.checked=Boolean(value);else element.value=String(value)}
}
function selectedPredictiveDataset(){const id=$('#predictive-form').elements.dataset_version_id.value;return state.datasets.find(item=>item.dataset_version_id===id)}
function renderPredictiveFeatureContext(){const features=list(String($('#predictive-form').elements.feature_columns.value||''));const target=$('#predictive-train-feature-context');if(target)target.textContent=`Feature columns (read-only): ${features.join(', ')||'—'}`}
function refreshPredictiveFeatureSelectorAvailability(){const dataset=selectedPredictiveDataset(),available=Boolean(dataset&&Object.keys(dataset.schema||{}).length);const trigger=$('#open-predictive-feature-selector'),status=$('#predictive-feature-selector-status');trigger.disabled=!available;status.textContent=available?'選択Datasetのschema列を選択できます。':'Dataset/schema未選択のため利用できません。'}
function reconcilePredictiveFeatures({announce=false}={}){const dataset=selectedPredictiveDataset(),field=$('#predictive-form').elements.feature_columns;if(!dataset){refreshPredictiveFeatureSelectorAvailability();renderPredictiveFeatureContext();return}const schemaColumns=Object.keys(dataset.schema||{}),known=new Set(schemaColumns),current=list(String(field.value||'')),ordered=schemaColumns.filter(column=>current.includes(column));if(ordered.length!==current.length){field.value=ordered.join(', ');if(announce)notice('Dataset Version変更によりschemaに存在しないFeature columnsを解除しました。')}refreshPredictiveFeatureSelectorAvailability();renderPredictiveFeatureContext();capturePredictiveDraft()}
let predictiveFeatureSelectorInvoker=null;
$('#open-predictive-feature-selector').onclick=()=>{const dataset=selectedPredictiveDataset();if(!dataset||!Object.keys(dataset.schema||{}).length){notice('Dataset/schemaを選択してください');return}const current=new Set(list(String($('#predictive-form').elements.feature_columns.value||'')));$('#predictive-feature-options').innerHTML=Object.keys(dataset.schema||{}).map(name=>`<label class="check-row"><input type="checkbox" value="${escapeHtml(name)}" ${current.has(name)?'checked':''}> <span>${escapeHtml(name)}</span><small>${escapeHtml(dataset.schema[name])}</small></label>`).join('');predictiveFeatureSelectorInvoker=$('#open-predictive-feature-selector');$('#predictive-feature-modal').showModal()};
$('#confirm-predictive-features').onclick=()=>{const dataset=selectedPredictiveDataset();if(!dataset)return;const checked=new Set($$('#predictive-feature-options input:checked').map(item=>item.value));$('#predictive-form').elements.feature_columns.value=Object.keys(dataset.schema||{}).filter(name=>checked.has(name)).join(', ');capturePredictiveDraft();renderPredictiveFeatureContext();$('#predictive-feature-modal').close()};
$('#cancel-predictive-features').onclick=()=>$('#predictive-feature-modal').close();
$('#predictive-feature-modal').addEventListener('close',()=>{predictiveFeatureSelectorInvoker?.focus();predictiveFeatureSelectorInvoker=null});
$('#predictive-form').elements.dataset_version_id.addEventListener('change',()=>reconcilePredictiveFeatures({announce:true}));
$('#predictive-form').addEventListener('input',()=>{capturePredictiveDraft();renderPredictiveFeatureContext()});
$('#predictive-form').addEventListener('change',()=>{capturePredictiveDraft();renderPredictiveFeatureContext()});

async function waitForPredictive(executionId){
  for(let attempt=0;attempt<480;attempt+=1){
    const execution=await api(`/projects/${state.project.project_id}/executions/${executionId}`);
    if(execution.status==='SUCCEEDED')return execution;
    if(execution.status==='FAILED')throw new Error(execution.last_error?.message||'Predictive execution failed');
    if(execution.status==='CANCELLED')throw new Error('Predictive execution was cancelled');
    await new Promise(resolve=>setTimeout(resolve,250));
  }
  throw new Error('Predictive execution is still running. 更新ボタンで再確認してください');
}

async function loadPredictiveDetails(executionId){
  const [execution,stages,results,artifacts,lineage]=await Promise.all([api(`/projects/${state.project.project_id}/executions/${executionId}`),api(`/projects/${state.project.project_id}/executions/${executionId}/stages`),api(`/projects/${state.project.project_id}/executions/${executionId}/results`),api(`/projects/${state.project.project_id}/executions/${executionId}/artifacts`),api(`/projects/${state.project.project_id}/executions/${executionId}/lineage`)]);
  const specification=state.predictiveSpecifications.find(item=>item.analysis_specification_id===execution.analysis_specification_id)||null;
  state.predictiveDetails={execution,specification,stages:stages.items,results:results.items,artifacts:artifacts.items,lineage:lineage.items};
  renderPredictiveDetails();
}

function renderPredictiveExecutions(){
  const target=$('#predictive-executions');if(!target)return;
  target.innerHTML=state.predictiveExecutions.length?`<table><thead><tr><th>Execution</th><th>Technical status</th><th>Specification</th><th>Requested</th><th></th></tr></thead><tbody>${state.predictiveExecutions.map(execution=>`<tr><td>${execution.execution_id.slice(0,8)}</td><td><span class="status ${execution.status}">${execution.status}</span></td><td>${escapeHtml((execution.analysis_specification_id||'').slice(0,8))}</td><td>${escapeHtml(execution.requested_at)}</td><td><button type="button" onclick="showPredictiveExecution('${execution.execution_id}')">Result / Artifact</button></td></tr>`).join('')}</tbody></table>`:'Executionはありません。';
}

function renderPredictiveDetails(){
  const targets=['#predictive-results','#predictive-predict-results','#predictive-explainability-results','#predictive-model-results','#predictive-artifacts'];
  const details=state.predictiveDetails;
  if(!details){targets.forEach(selector=>{const target=$(selector);if(target)target.textContent=selector==='#predictive-artifacts'?'Artifactはありません。':'Resultはありません。'});const context=$('#predictive-predict-context');if(context)context.textContent='既存Executionを選択してください。';return}
  const familySpec=details.specification?.family_spec||{},question=familySpec.prediction_question||{},features=familySpec.feature_spec||{},split=familySpec.split_spec||{};
  const specificationSummary=`<article class="predictive-result" data-predictive-specification><h3>Execution inputs</h3><p>Research Context: ${escapeHtml(details.execution.research_context_version_id||'—')} / Dataset Version: ${escapeHtml(details.execution.dataset_version_id||'—')} / Analysis View: ${escapeHtml(details.execution.analysis_view_id||'Dataset Version全体')}</p><p>Task: ${escapeHtml(familySpec.task_type||'—')} / Target: ${escapeHtml(question.target||'—')} / Features: ${escapeHtml((features.feature_columns||[]).join(', ')||'—')} / Split: ${escapeHtml(split.strategy||'—')}</p></article>`;
  const stage=state.navigationContext?.familySlug==='predictive'?state.navigationContext.stageSlug:null,resultTypes=PREDICTIVE_STAGE_RESULT_TYPES[stage],artifactTypes=PREDICTIVE_STAGE_ARTIFACT_TYPES[stage];
  const resultTarget=({predict:'#predictive-predict-results',metrics:'#predictive-results',explainability:'#predictive-explainability-results','model-management':'#predictive-model-results'})[stage];
  const orderedResults=[...details.results].filter(result=>!resultTypes||resultTypes.includes(result.result_type)).sort((left,right)=>PREDICTIVE_RESULT_ORDER.indexOf(left.result_type)-PREDICTIVE_RESULT_ORDER.indexOf(right.result_type));
  if(resultTarget){const target=$(resultTarget);target.innerHTML=`<p><b>Execution ${details.execution.execution_id.slice(0,8)}</b> <span class="status ${details.execution.status}">${details.execution.status}</span></p>`+(orderedResults.length?orderedResults.map(result=>`<article class="predictive-result" data-result-type="${escapeHtml(result.result_type)}"><h3>${escapeHtml(result.result_type)}</h3><pre>${escapeHtml(JSON.stringify({summary:result.summary,payload:result.payload,diagnostics:result.diagnostics,warnings:result.warnings},null,2))}</pre></article>`).join(''):stage==='predict'?'Prediction outputはありません。':'このStageに対応する既存Resultはありません。')}
  const context=$('#predictive-predict-context');if(context)context.innerHTML='<p>このExecution specificationに記録されたFeature columns（read-only）です。</p>'+specificationSummary;
  const artifacts=details.artifacts.filter(artifact=>!artifactTypes||artifactTypes.includes(artifact.artifact_type));
  const artifactTarget=stage==='predict'?$('#predictive-predict-artifacts'):$('#predictive-artifacts');artifactTarget.innerHTML=artifacts.length?artifacts.map(artifact=>`<article><b>${escapeHtml(artifact.artifact_type)}</b><p>Artifact ${artifact.artifact_id}</p><p>Result ${escapeHtml(artifact.result_id||'—')}</p><small>${escapeHtml(artifact.schema_version)} / ${escapeHtml(artifact.media_type)} / ${artifact.size_bytes} bytes / ${artifact.content_hash}</small></article>`).join(''):stage==='predict'?'Prediction outputはありません。':'Artifactはありません。';
}
window.showPredictiveExecution=async id=>{try{await loadPredictiveDetails(id)}catch(error){notice(error.message)}};

async function loadPredictiveWorkspace(){
  if(!state.project){state.researchContexts=[];state.predictiveCapabilities=null;state.predictiveSpecifications=[];state.predictiveExecutions=[];state.predictiveDetails=null;renderResearchContexts();renderPredictiveExecutions();renderPredictiveDetails();updatePredictiveAvailability();return}
  const projectId=state.project.project_id;
  const [capabilities,contexts,specifications,executions]=await Promise.all([api(`/projects/${projectId}/predictive/capabilities`),api(`/projects/${projectId}/research-contexts`),api(`/projects/${projectId}/analysis-specifications`),api(`/projects/${projectId}/executions`)]);
  state.predictiveCapabilities=capabilities;state.researchContexts=contexts.items;state.predictiveSpecifications=specifications.items.filter(specification=>specification.analysis_family==='PREDICTIVE');state.predictiveExecutions=executions.items.filter(execution=>execution.analysis_family==='PREDICTIVE'&&execution.analysis_specification_id);
  $('#predictive-capabilities').innerHTML=`<p><b>${escapeHtml(capabilities.gate)}</b> — Training ${capabilities.training_available?'available':'unavailable'} / Evaluation ${capabilities.evaluation_available?'available':'unavailable'} / Explanation ${capabilities.explanation_available?'available':'unavailable'} / Model Card ${capabilities.model_card_available?'available':'unavailable'}</p><p>Models: ${capabilities.model_registry.map(model=>escapeHtml(model.model_id)).join(', ')}</p>`;
  const method=$('#predictive-explanation-method'),selected=method.value;method.innerHTML=capabilities.explanation_methods.map(item=>`<option value="${escapeHtml(item.method)}">${escapeHtml(item.method)}</option>`).join('');if(capabilities.explanation_methods.some(item=>item.method===selected))method.value=selected;
  restorePredictiveDraft();reconcilePredictiveFeatures();
  renderResearchContexts();renderPredictiveExecutions();updatePredictiveAvailability();
  if(state.predictiveExecutions.length)await loadPredictiveDetails(state.predictiveExecutions[0].execution_id);else{state.predictiveDetails=null;renderPredictiveDetails()}
}

$('#predictive-form').elements.task_type.onchange=event=>{const form=$('#predictive-form');if(event.target.value==='REGRESSION'){if(form.elements.split_strategy.value==='STRATIFIED')form.elements.split_strategy.value='RANDOM';form.elements.model_id.value='linear_regression.v1';form.elements.primary_metric.innerHTML='<option>RMSE</option><option>MAE</option><option>R2</option>';form.elements.primary_metric.value='RMSE'}else{form.elements.model_id.value='logistic_regression.v1';form.elements.primary_metric.innerHTML='<option>ROC_AUC</option><option>PR_AUC</option><option>LOG_LOSS</option><option>BRIER</option><option>ACCURACY</option><option>F1</option>';form.elements.primary_metric.value='ROC_AUC'}};
$('#predictive-form').onsubmit=async event=>{
  event.preventDefault();if(!state.project)return notice('Projectを選択してください');
  const button=$('#run-predictive'),form=new FormData(event.target),projectId=state.project.project_id;button.disabled=true;
  try{
    const familySpec=predictiveFamilySpec(),datasetId=String(form.get('dataset_version_id')),viewId=String(form.get('analysis_view_id')||'')||null;
    const specification=await api(`/projects/${projectId}/analysis-specifications`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({schema_version:'analysis-specification/1',specification_key:`predictive-${Date.now()}`,analysis_family:'PREDICTIVE',research_context_version_id:String(form.get('research_context_version_id')),dataset_version_id:datasetId,analysis_view_id:viewId,analysis_mode:'CONFIRMATORY',family_spec_schema_version:'predictive-analysis-spec/1',family_spec:familySpec,revision_context:null,warnings:[]})});
    await api(`/projects/${projectId}/analysis-specifications/${specification.analysis_specification_id}/validate`,{method:'POST'});
    await api(`/projects/${projectId}/analysis-specifications/${specification.analysis_specification_id}/fix`,{method:'POST'});
    const plan=await api(`/projects/${projectId}/execution-plans`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({analysis_specification_id:specification.analysis_specification_id})});
    await api(`/projects/${projectId}/execution-plans/${plan.execution_plan_id}/validate`,{method:'POST'});
    $('#predictive-split-validation').innerHTML=`<p><span class="status VALID">VALID</span> Execution Plan validated</p><pre>${escapeHtml(JSON.stringify({execution_plan_id:plan.execution_plan_id,analysis_specification_id:specification.analysis_specification_id},null,2))}</pre>`;
    const execution=await api(`/projects/${projectId}/executions`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({analysis_specification_id:specification.analysis_specification_id,execution_plan_id:plan.execution_plan_id,seed:familySpec.split_spec.seed})});
    notice('Predictive Executionをキューへ登録しました');await waitForPredictive(execution.execution_id);await loadPredictiveWorkspace();await loadPredictiveDetails(execution.execution_id);notice('Evaluation、Predictive Explanation、Model Cardを保存しました');
  }catch(error){notice(error.message)}finally{updatePredictiveAvailability()}
};
$('#refresh-predictive').onclick=async event=>{event.currentTarget.dataset.refreshStatus='pending';try{await loadPredictiveWorkspace();event.currentTarget.dataset.refreshStatus='done'}catch(error){event.currentTarget.dataset.refreshStatus='failed';notice(error.message)}};

function selectedDiscoveryDataset(){const id=$('#discovery-form').elements.dataset_version_id.value;return state.datasets.find(item=>item.dataset_version_id===id)}
$('#open-feature-selector').onclick=()=>{const dataset=selectedDiscoveryDataset();if(!dataset)return notice('Datasetを先に選択してください');const current=new Set(list($('#discovery-form').elements.features.value));$('#feature-options').innerHTML=Object.keys(dataset.schema||{}).map(name=>`<label class="check-row"><input type="checkbox" value="${escapeHtml(name)}" ${current.has(name)?'checked':''}> <span>${escapeHtml(name)}</span><small>${escapeHtml(dataset.schema[name])}</small></label>`).join('');$('#feature-modal').showModal()};
$('#confirm-features').onclick=()=>{const dataset=selectedDiscoveryDataset();if(!dataset)return;const checked=new Set($$('#feature-options input:checked').map(item=>item.value));const ordered=Object.keys(dataset.schema||{}).filter(name=>checked.has(name));$('#discovery-form').elements.features.value=ordered.join(', ');syncOutcomeOptions();$('#feature-modal').close()};
function syncOutcomeOptions(){const features=list($('#discovery-form').elements.features.value),select=$('#discovery-outcome'),old=select.value;select.innerHTML='<option value="">Outcomeを選択</option>'+features.map(name=>`<option value="${escapeHtml(name)}">${escapeHtml(name)}</option>`).join('');select.value=features.includes(old)?old:''}
$('#discovery-form').elements.dataset_version_id.onchange=()=>{$('#discovery-form').elements.features.value='';syncOutcomeOptions()};

function discoveryRequest(form){
  const datasetId=String(form.get('dataset_version_id')||'');
  const dataset=state.datasets.find(item=>item.dataset_version_id===datasetId);
  if(!dataset)throw new Error('Datasetを選択してください');

  const features=list(String(form.get('features')||''));
  if(!features.length)throw new Error('Feature columnsを1件以上指定してください');
  if(new Set(features).size!==features.length)throw new Error('Feature columnsに重複があります');
  const knownColumns=new Set(Object.keys(dataset.schema||{}));
  const unknown=features.filter(name=>!knownColumns.has(name));
  if(unknown.length)throw new Error(`Datasetに存在しないFeature columns: ${unknown.join(', ')}`);
  const outcome=String(form.get('designated_outcome_node')||'');
  if(!outcome||!features.includes(outcome))throw new Error('OutcomeをFeature columnsから1件選択してください');

  const algorithms=form.getAll('algorithms').map(String);
  if(!algorithms.length)throw new Error('Algorithmを1件以上選択してください');
  const variants=[];
  if(algorithms.includes('pc')){
    const alphaTokens=list(String(form.get('alpha')||''));
    if(!alphaTokens.length)throw new Error('PCを選択した場合はalphaを1件以上指定してください');
    const invalid=alphaTokens.filter(token=>{
      const value=Number(token);return !Number.isFinite(value)||value<=0||value>=1;
    });
    if(invalid.length)throw new Error(`PC alphaは0より大きく1より小さい数値にしてください: ${invalid.join(', ')}`);
    for(const token of alphaTokens)variants.push({algorithm_or_estimator:'pc',parameters:{alpha:Number(token)},random_seed:42});
  }
  if(algorithms.includes('ges'))variants.push({algorithm_or_estimator:'ges',parameters:{},random_seed:42});
  if(variants.length>20)throw new Error(`Executionは一度に20件までです（現在${variants.length}件）`);

  return {operation:'DISCOVERY',dataset_version_id:datasetId,input_graph_version_id:null,input_result_id:null,objective:form.get('objective')||null,rationale:form.get('rationale')||null,analysis_spec:{schema_version:'causal-analysis-spec/2',analysis_mode:'EXPLORATORY',research_context:{problem_statement:null,research_question:null,significance:null,hypothesis:null},causal_question:{},causal_design:{adjustment_set:[],assumptions:[]},operation_spec:{feature_columns:features,designated_outcome_node:outcome,constraints:{required_edges:[],forbidden_edges:[],temporal_tiers:[]},expected_graph_type:null},validation_override:null},variants,code_version:'web-enh-e2',runtime_versions:{client:'web'}};
}
$('#discovery-form').onsubmit=async event=>{
  event.preventDefault();
  if(!state.project)return notice('Projectを選択してください');
  try{
    const body=discoveryRequest(new FormData(event.target));
    await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify(body)});
    notice(`${body.variants.length}件のDiscoveryを受け付けました`);
    await loadExecutions();
  }catch(error){notice(error.message)}
};
async function loadExecutions(){if(!state.project){state.executions=[];state.results=[];return}state.executions=(await api(`/projects/${state.project.project_id}/executions`)).items.filter(execution=>execution.operation);state.results=[];for(const execution of state.executions){if(execution.status==='SUCCEEDED'){const values=(await api(`/executions/${execution.execution_id}/results`)).items;values.forEach(value=>value.execution=execution);state.results.push(...values)}}const bases=$('#base-executions');if(bases)bases.innerHTML='<option value="">新規分析</option>'+state.executions.filter(e=>e.operation==='ESTIMATION').map(e=>`<option value="${e.execution_id}">${escapeHtml(e.algorithm_or_estimator)} / ${e.execution_id.slice(0,8)}</option>`).join('');renderDiscovery();renderInference();renderResultOptions()}
function resultRows(operation,target){const values=state.results.filter(r=>r.execution.operation===operation);target.innerHTML=values.length?`<table><thead><tr><th></th><th>Method</th><th>Status</th><th>Summary</th></tr></thead><tbody>${values.map(r=>`<tr><td><input type="checkbox" value="${r.result_id}"></td><td>${escapeHtml(r.execution.algorithm_or_estimator)}</td><td class="${r.scientific_status}">${r.scientific_status}</td><td>${escapeHtml(JSON.stringify(r.summary))}</td></tr>`).join('')}</tbody></table>`:'完了Resultはありません';return values}
function renderDiscovery(){resultRows('DISCOVERY',$('#discovery-results'));renderGraphCandidates()}
async function refreshExecutions(button){button.dataset.refreshStatus='pending';try{await loadExecutions();button.dataset.refreshStatus='done'}catch(error){button.dataset.refreshStatus='failed';notice(error.message);throw error}}
$('#refresh-discovery').onclick=async event=>{const button=event.currentTarget;button.dataset.refreshStatus='pending';try{await loadExecutions();await loadGraphs();button.dataset.refreshStatus='done'}catch(error){button.dataset.refreshStatus='failed';notice(error.message);throw error}};
$('#compare-discovery').onclick=compareGraphCandidates;
async function compareChecked(container,output,minimum=2){const ids=$$(`${container} input:checked`).map(x=>x.value);if(ids.length<minimum)return notice(`${minimum}件以上選択してください`);try{$(output).textContent=JSON.stringify(await api('/comparisons/query',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({project_id:state.project.project_id,result_ids:ids})}),null,2)}catch(error){notice(error.message)}}
$('#graph-source').onchange=()=>{const result=state.results.find(r=>r.result_id===$('#graph-source').value);if(result)$('#graph-parent').value='';state.sourceGraph=result?structuredClone(result.payload):null;state.editingGraph=result?structuredClone(result.payload):null;renderGraphEditor()};
$('#graph-parent').onchange=()=>{const graph=state.graphs.find(g=>g.graph_version_id===$('#graph-parent').value);if(graph)$('#graph-source').value='';state.sourceGraph=graph?structuredClone(graph.graph):null;state.editingGraph=graph?structuredClone(graph.graph):null;renderGraphEditor()};
function renderGraphEditor(){const graph=state.editingGraph,editable=Boolean(state.graphCandidate?.allowed_actions?.can_edit)||state.graphCandidate?.candidate_kind==='DISCOVERY_RESULT'||state.graphCandidate?.fixed;$('#graph-editor').innerHTML=!graph?'Graph Candidateを選択してください':`<p>Type: <b>${graph.graph_type}</b> / Nodes: ${graph.nodes.length}</p>${graph.edges.map((edge,index)=>`<div class="edge"><span>${escapeHtml(edge.source)} ${edge.endpoint_source} — ${edge.endpoint_target} ${escapeHtml(edge.target)}</span>${editable?`<button type="button" onclick="removeEdge(${index})">削除</button>`:''}</div>`).join('')}`;renderGraphVisual(graph,$('#graph-visual'),state.graphCandidate?.designated_outcome_node)}
window.removeEdge=index=>{state.editingGraph.edges.splice(index,1);renderGraphEditor()};
$('#add-edge').onclick=()=>{if(!state.editingGraph)return;const source=$('#edge-source').value.trim(),target=$('#edge-target').value.trim();if(!state.editingGraph.nodes.includes(source)||!state.editingGraph.nodes.includes(target)||source===target)return notice('既存の異なるnodeを指定してください');state.editingGraph.edges.push({source,target,endpoint_source:'TAIL',endpoint_target:'ARROW'});renderGraphEditor()};
$('#save-graph').onclick=async()=>{const candidate=state.graphCandidate,rationale=$('#graph-rationale').value.trim();if(!candidate||!state.editingGraph)return notice('Graph Candidateを選択してください');if(!rationale)return notice('選定・編集理由を入力してください');try{let graph;if(candidate.candidate_kind==='GRAPH_VERSION'&&candidate.version_status==='DRAFT'){graph=await api(`/projects/${state.project.project_id}/graph-versions/${candidate.graph_version_id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({graph:state.editingGraph,designated_outcome_node:$('#graph-outcome').value.trim()||null,edit_rationale:rationale,expected_content_hash:candidate.summary?.content_hash||null})})}else{graph=await api(`/projects/${state.project.project_id}/graph-edit-drafts`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({base_candidate_kind:candidate.candidate_kind,base_candidate_id:candidate.candidate_id,change_kind:$('#graph-transform').value,name:`Edited graph ${new Date().toISOString()}`,edit_rationale:rationale})});if(JSON.stringify(state.editingGraph)!==JSON.stringify(state.sourceGraph)||$('#graph-outcome').value.trim()!==String(graph.designated_outcome_node||'')){graph=await api(`/projects/${state.project.project_id}/graph-versions/${graph.graph_version_id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify({graph:state.editingGraph,designated_outcome_node:$('#graph-outcome').value.trim()||null,edit_rationale:rationale})})}}await loadGraphs();await inspectCandidate('GRAPH_VERSION',graph.graph_version_id);notice('元Graphを保持し、編集内容をDRAFTへ保存しました')}catch(error){notice(error.message)}};
$('#fix-graph').onclick=async()=>{const candidate=state.graphCandidate;if(candidate?.candidate_kind!=='GRAPH_VERSION'||candidate.version_status!=='DRAFT')return notice('FIXできるのはDRAFT Graph Versionだけです');try{const graph=await api(`/projects/${state.project.project_id}/graph-versions/${candidate.graph_version_id}/fix`,{method:'POST'});await loadGraphs();await inspectCandidate('GRAPH_VERSION',graph.graph_version_id);notice('Graph VersionをFIXEDにしました。以後は直接更新できません')}catch(error){notice(error.message)}};
$('#adopt-graph').onclick=async()=>{const candidate=state.graphCandidate,rationale=$('#graph-rationale').value.trim();if(candidate?.candidate_kind!=='DISCOVERY_RESULT')return notice('Algorithm Outputだけを直接採用できます');if(!rationale)return notice('選定理由を入力してください');try{const graph=await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:candidate.candidate_id,parent_graph_version_id:null,graph_origin:'DISCOVERED',name:`Selected graph ${new Date().toISOString()}`,graph_type:candidate.graph_type,graph:candidate.graph,designated_outcome_node:candidate.designated_outcome_node,provenance:{algorithm_output:true,selection_rationale:rationale},edit_rationale:rationale,fix_immediately:true})});await loadGraphs();await inspectCandidate('GRAPH_VERSION',graph.graph_version_id);notice('Algorithm Outputを変更せずDISCOVERED FIXED Versionとして採用しました')}catch(error){notice(error.message)}};
$('#save-direct-graph').onclick=async()=>{if(!state.project)return notice('Projectを選択してください');const origin=$('#direct-graph-origin').value,note=$('#direct-graph-note').value.trim(),name=$('#direct-graph-name').value.trim(),outcome=$('#direct-graph-outcome').value.trim();if(!note||!name||!outcome)return notice('Name、Designated Outcome、Source / import noteを入力してください');let graph;try{graph=JSON.parse($('#direct-graph-json').value)}catch{return notice('Graph JSONが不正です')}try{await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:null,parent_graph_version_id:null,graph_origin:origin,name,graph_type:graph.graph_type,graph,designated_outcome_node:outcome,provenance:{source_note:note},edit_rationale:null,fix_immediately:false})});await loadGraphs();notice('Direct GraphをDRAFT Versionとして保存しました')}catch(error){notice(error.message)}};

function renderGraphCandidates(){const target=$('#graph-candidates');if(!target)return;target.innerHTML=state.graphCandidates.length?`<table><thead><tr><th></th><th>Kind / FIXED</th><th>Source / Parent</th><th>Type / Origin</th><th>Status</th><th>Outcome</th><th>Summary</th><th>操作</th></tr></thead><tbody>${state.graphCandidates.map(c=>`<tr><td><input class="candidate-check" type="checkbox" data-kind="${c.candidate_kind}" value="${c.candidate_id}"></td><td>${c.candidate_kind}<br><span class="status">${c.fixed?'FIXED':'—'}</span></td><td>${escapeHtml(c.parent_graph_version_id||c.source_result_id||'root')}</td><td>${c.graph_type}<br>${c.graph_origin}</td><td>${escapeHtml(c.version_status||c.scientific_status||'—')}</td><td>${escapeHtml(c.designated_outcome_node||'未指定')}</td><td>${c.summary.node_count} nodes / ${c.summary.edge_count} edges<br>${escapeHtml(c.warnings.join?.(', ')||'')}</td><td><button type="button" onclick="inspectCandidate('${c.candidate_kind}','${c.candidate_id}')">グラフを確認/編集する</button></td></tr>`).join('')}</tbody></table>`:'Graph Candidateはありません';$$('.candidate-check').forEach(item=>item.onchange=()=>{$('#compare-discovery').disabled=$$('.candidate-check:checked').length<2})}
window.inspectCandidate=inspectCandidate;
async function inspectCandidate(kind,id){try{const candidate=await api(`/projects/${state.project.project_id}/graph-candidates/${kind}/${id}`);state.graphCandidate=candidate;state.sourceGraph=structuredClone(candidate.graph);state.editingGraph=structuredClone(candidate.graph);$('#graph-meta').innerHTML=`<div class="badge-row"><span class="status">${candidate.graph_type}</span><span class="status">${candidate.graph_origin}</span><span class="status">${candidate.version_status||candidate.scientific_status}</span></div><p>Source: ${escapeHtml(candidate.source_result_id||'—')} / Parent: ${escapeHtml(candidate.parent_graph_version_id||'—')}</p><p>Outcome: ${escapeHtml(candidate.designated_outcome_node||'未指定')}</p>`;$('#graph-outcome').value=candidate.designated_outcome_node||'';$('#graph-rationale').value=candidate.summary.edit_rationale||'';$('#adopt-graph').hidden=candidate.candidate_kind!=='DISCOVERY_RESULT';$('#save-graph').disabled=!(candidate.allowed_actions.can_edit||candidate.allowed_actions.can_create_child);$('#fix-graph').disabled=!candidate.allowed_actions.can_fix;$('#add-edge').disabled=!(candidate.allowed_actions.can_edit||candidate.allowed_actions.can_create_child);$('#save-graph').textContent=candidate.allowed_actions.can_edit?'DRAFTを更新':'子DRAFTを作成';renderGraphEditor();$('#graph-modal').showModal()}catch(error){notice(error.message)}}
$('#close-graph-modal').onclick=()=>$('#graph-modal').close();
async function compareGraphCandidates(){const refs=$$('.candidate-check:checked').map(item=>({candidate_kind:item.dataset.kind,candidate_id:item.value}));if(refs.length<2)return notice('2件以上選択してください');try{const comparison=await api(`/projects/${state.project.project_id}/graph-candidate-comparisons/query`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({candidate_refs:refs})});$('#comparison-tabs').innerHTML=comparison.candidates.map((candidate,index)=>`<button type="button" data-index="${index}">${escapeHtml(candidate.summary.name||candidate.candidate_id.slice(0,8))}</button>`).join('');const show=index=>{const candidate=comparison.candidates[index];renderGraphVisual(candidate.graph,$('#comparison-graph'),candidate.designated_outcome_node);$('#comparison-summary').innerHTML=`<p><b>${candidate.graph_type}</b> / ${candidate.graph_origin} / ${candidate.summary.node_count} nodes / ${candidate.summary.edge_count} edges / Outcome: ${escapeHtml(candidate.designated_outcome_node||'未指定')}</p><h3>Compatibility</h3><p>${comparison.compatibility.compatible?'比較可能':`比較不能: ${escapeHtml(comparison.compatibility.reasons.join(', '))}`}</p><h3>Structure diff</h3>${comparison.compatibility.compatible?`<pre>${escapeHtml(JSON.stringify(comparison.differences,null,2))}</pre>`:'個別タブのGraph表示は利用できます。'}`};$$('#comparison-tabs button').forEach(button=>button.onclick=()=>show(Number(button.dataset.index)));show(0);$('#graph-comparison-modal').showModal()}catch(error){notice(error.message)}}
$('#close-comparison-modal').onclick=()=>$('#graph-comparison-modal').close();
function renderGraphVisual(graph,target,outcome){if(!graph){target.innerHTML='Graphはありません';return}const nodes=[...graph.nodes].sort((a,b)=>a===outcome?1:b===outcome?-1:a.localeCompare(b)),columns=Math.min(6,Math.max(1,nodes.length)),rows=Math.max(1,Math.ceil(nodes.length/columns)),width=Math.max(480,columns*140),height=rows*180+100,positions=new Map(nodes.map((node,index)=>{const row=Math.floor(index/columns),column=node===outcome?columns-1:index%columns;return [node,{x:70+column*(width-140)/Math.max(1,columns-1),y:80+row*180+(column%2)*90}]}));target.innerHTML=`<svg class="graph-svg" width="100%" viewBox="0 0 ${width} ${height}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${escapeHtml(graph.graph_type)} graph">${graph.edges.map(edge=>{const a=positions.get(edge.source),b=positions.get(edge.target);return a&&b?`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" class="graph-edge"/><text x="${(a.x+b.x)/2}" y="${(a.y+b.y)/2-5}" class="edge-label">${edge.endpoint_source}→${edge.endpoint_target}</text>`:''}).join('')}${nodes.map(node=>{const p=positions.get(node);return `<g class="graph-node ${node===outcome?'outcome':''}"><circle cx="${p.x}" cy="${p.y}" r="32"/><text x="${p.x}" y="${p.y+4}">${escapeHtml(node)}</text></g>`).join('')}</svg>`}

async function loadGraphs(){if(!state.project){state.graphs=[];state.graphCandidates=[];renderGraphCandidates();return}const [graphs,candidates]=await Promise.all([api(`/projects/${state.project.project_id}/graph-versions`),api(`/projects/${state.project.project_id}/graph-candidates`)]);state.graphs=graphs.items;state.graphCandidates=candidates.items;const fixed=state.graphs.filter(g=>g.status==='FIXED'&&g.designated_outcome_node);$('#fixed-graphs').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin} / ${escapeHtml(g.designated_outcome_node)}</option>`).join('');$('#graph-parent').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin}</option>`).join('');renderGraphCandidates()}
function selectedInferenceGraph(){return state.graphs.find(graph=>graph.graph_version_id===$('#fixed-graphs').value)}
$('#fixed-graphs').onchange=()=>{const graph=selectedInferenceGraph(),outcome=graph?.designated_outcome_node;$('#inference-outcome').textContent=outcome||'Outcome未指定のため使用できません';$('#run-identification').disabled=!outcome;$('#inference-form').dispatchEvent(new Event('input',{bubbles:true}))};
$('#inference-form').oninput=event=>{const f=new FormData(event.currentTarget),strategy=f.get('strategy'),difference=$('#inference-form input[value="difference_in_means"]'),outcome=selectedInferenceGraph()?.designated_outcome_node;difference.disabled=strategy!=='RANDOMIZED';if(difference.disabled)difference.checked=false;const compatible=strategy==='RANDOMIZED'?'difference_in_means, ols, ipw, aipw':'ols, ipw, aipw';$('#preflight').textContent=`Preflight: treatment=${f.get('treatment')||'—'}, outcome=${outcome||'Graphで指定が必要'}, adjustment=[${list(f.get('adjustment')).join(', ')}], FIXED graph=${f.get('graph_version_id')?'selected':'required'}, compatible estimators=${compatible}`};
function inferenceSpec(f,operation_spec,override=null){const outcome=selectedInferenceGraph()?.designated_outcome_node;return {schema_version:'causal-analysis-spec/2',analysis_mode:f.get('analysis_mode')||'EXPLORATORY',research_context:{problem_statement:null,research_question:null,significance:null,hypothesis:null},causal_question:{population:f.get('population'),treatment:f.get('treatment'),comparator:f.get('comparator'),outcome,analysis_unit:f.get('analysis_unit'),treatment_time:f.get('treatment_time'),outcome_window:f.get('outcome_window'),estimand:f.get('estimand'),decision_use:null},causal_design:{assignment_assumption:null,time_zero:f.get('treatment_time'),eligibility_criteria:[],identification_strategy:f.get('strategy'),adjustment_set:list(f.get('adjustment')),assumptions:list(f.get('assumptions'))},operation_spec,validation_override:override}}
$('#run-identification').onclick=async()=>{const form=$('#inference-form'),f=new FormData(form);try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'IDENTIFICATION',dataset_version_id:f.get('dataset_version_id'),input_graph_version_id:f.get('graph_version_id'),input_result_id:null,objective:'Identify causal effect',rationale:'Identification-first gate',analysis_spec:inferenceSpec(f,{allow_partial_identification:false}),variants:[{algorithm_or_estimator:'GRAPHICAL_IDENTIFICATION',parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Identificationを受け付けました');await loadExecutions()}catch(error){notice(error.message)}};
$('#inference-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');const f=new FormData(event.target),estimators=f.getAll('estimators'),reason=String(f.get('override_reason')||'').trim(),override=reason?{reason,actor:'web-user',warning_codes:['ELIGIBILITY_WARN']}:null,base=String(f.get('base_execution_id')||'')||null,changeReason=String(f.get('change_reason')||'').trim()||null;try{const response=await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'ESTIMATION',dataset_version_id:f.get('dataset_version_id'),input_graph_version_id:f.get('graph_version_id'),input_result_id:f.get('identification_result_id'),objective:'Estimate binary treatment effect',rationale:'Compare estimator sensitivity',analysis_spec:inferenceSpec(f,{inference_options:{}},override),variants:estimators.map(x=>({algorithm_or_estimator:x,parameters:{},random_seed:42})),code_version:'web-enh-e1',runtime_versions:{client:'web'},base_execution_id:base,change_reason:changeReason})});const warnings=response.executions.flatMap(x=>x.scientific_warnings||[]);$('#scientific-warnings').textContent=warnings.map(x=>`${x.warning_code}: ${x.message}`).join('\n');notice(warnings.length?`${estimators.length}件を警告付きで受け付けました`:`${estimators.length}件のEstimationを受け付けました`);await loadExecutions()}catch(error){notice(error.message)}};
function causalResultRows(resultTypes,target){const values=state.results.filter(result=>resultTypes.includes(result.result_type));target.innerHTML=values.length?`<table><thead><tr><th></th><th>Result</th><th>Status</th><th>Summary</th></tr></thead><tbody>${values.map(result=>`<tr><td><input type="checkbox" value="${result.result_id}"></td><td>${escapeHtml(result.result_type)}</td><td class="${result.scientific_status}">${escapeHtml(result.scientific_status)}</td><td>${escapeHtml(JSON.stringify({summary:result.summary,payload:result.payload,warnings:result.warnings}))}</td></tr>`).join('')}</tbody></table>`:'完了Resultはありません';return values}
function renderInference(){const ids=state.results.filter(r=>r.result_type==='IDENTIFICATION_RESULT');$('#identification-results').innerHTML='<option value="">選択</option>'+ids.map(r=>`<option value="${r.result_id}">${r.scientific_status} / ${r.result_id.slice(0,8)}</option>`).join('');$('#identification-panel').innerHTML=state.results.filter(r=>['IDENTIFICATION_RESULT','DATA_ELIGIBILITY_RESULT'].includes(r.result_type)).map(r=>`<p><b>${r.result_type}</b> <span class="${r.scientific_status}">${r.scientific_status}</span> ${escapeHtml(JSON.stringify({summary:r.summary,inferred_types:r.payload?.inferred_types,checks:r.payload?.checks,warnings:r.warnings}))}</p>`).join('')||'Resultはありません';resultRows('ESTIMATION',$('#estimation-results'));causalResultRows(['TREATMENT_EFFECT_RESULT'],$('#treatment-effect-results'));causalResultRows(['DIAGNOSTICS_RESULT'],$('#diagnostics-results'));const effects=state.results.filter(r=>r.result_type==='TREATMENT_EFFECT_RESULT');$$('.effect-results').forEach(select=>select.innerHTML='<option value="">選択</option>'+effects.map(r=>`<option value="${r.result_id}">${r.scientific_status} / ${r.result_id.slice(0,8)}</option>`).join(''))}
$('#refresh-inference').onclick=event=>refreshExecutions(event.currentTarget);$('#refresh-effects').onclick=event=>refreshExecutions(event.currentTarget);$('#refresh-diagnostics').onclick=event=>refreshExecutions(event.currentTarget);$('#compare-effects').onclick=()=>compareChecked('#treatment-effect-results','#effects-comparison',2);

function followupSpec(operation_spec){return {schema_version:'causal-analysis-spec/2',analysis_mode:'EXPLORATORY',research_context:{},causal_question:{},causal_design:{adjustment_set:[],assumptions:[]},operation_spec,validation_override:null}}
$('#refutation-form').onsubmit=async event=>{event.preventDefault();const f=new FormData(event.target),base=state.results.find(r=>r.result_id===f.get('result_id'));if(!base)return notice('Treatment Effect Resultを選択してください');const method=f.get('method'),operation_spec=method==='PLACEBO_TREATMENT'?{method,repetitions:Number(f.get('repetitions'))}:{method,subset_fraction:Number(f.get('subset_fraction'))};try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'REFUTATION',dataset_version_id:base.execution.dataset_version_id,input_graph_version_id:base.execution.input_graph_version_id,input_result_id:base.result_id,objective:'Refute treatment effect',rationale:'ENH-E1 minimum refutation',analysis_spec:followupSpec(operation_spec),variants:[{algorithm_or_estimator:method,parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Refutationを受け付けました')}catch(error){notice(error.message)}};
$('#sensitivity-form').onsubmit=async event=>{event.preventDefault();const f=new FormData(event.target),base=state.results.find(r=>r.result_id===f.get('result_id'));if(!base)return notice('Treatment Effect Resultを選択してください');const dimension=f.get('dimension'),operation_spec=dimension==='PROPENSITY_CLIPPING'?{dimension,values:list(f.get('values')).map(Number)}:{dimension,adjustment_sets:String(f.get('adjustment_sets')||'').split(';').filter(Boolean).map(list)};try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'SENSITIVITY',dataset_version_id:base.execution.dataset_version_id,input_graph_version_id:base.execution.input_graph_version_id,input_result_id:base.result_id,objective:'Assess sensitivity',rationale:'ENH-E1 minimum sensitivity',analysis_spec:followupSpec(operation_spec),variants:[{algorithm_or_estimator:dimension,parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Sensitivityを受け付けました')}catch(error){notice(error.message)}};

function filteredUnifiedResults(){const family=$('#result-family-filter').value,type=$('#result-type-filter').value,status=$('#result-status-filter').value;return state.unifiedResults.filter(item=>(!family||item.analysis_family===family)&&(!type||item.result_type===type)&&(!status||item.analytical_status===status))}
function renderResultOptions(){
  const families=[...new Set(state.unifiedResults.map(item=>item.analysis_family))].sort(),types=[...new Set(state.unifiedResults.map(item=>item.result_type))].sort(),statuses=[...new Set(state.unifiedResults.map(item=>item.analytical_status))].sort(),oldFamily=$('#result-family-filter').value,oldType=$('#result-type-filter').value,oldStatus=$('#result-status-filter').value;
  $('#result-family-filter').innerHTML='<option value="">すべて</option>'+families.map(value=>`<option ${value===oldFamily?'selected':''}>${value}</option>`).join('');$('#result-type-filter').innerHTML='<option value="">すべて</option>'+types.map(value=>`<option ${value===oldType?'selected':''}>${value}</option>`).join('');$('#result-status-filter').innerHTML='<option value="">すべて</option>'+statuses.map(value=>`<option ${value===oldStatus?'selected':''}>${value}</option>`).join('');
  const values=filteredUnifiedResults();$('#result-select').innerHTML='<option value="">選択</option>'+values.map(item=>`<option value="${item.result_id}">${item.analysis_family} / ${item.result_type} / ${item.analytical_status}</option>`).join('');
  $('#unified-result-list').innerHTML=values.length?`<table><thead><tr><th></th><th>Family</th><th>Result Type</th><th>Analytical status</th><th>Warnings / limitations</th></tr></thead><tbody>${values.map(item=>`<tr><td><input class="result-compare-check" type="checkbox" value="${item.result_id}"></td><td><span class="family-label">${item.analysis_family}</span></td><td>${escapeHtml(item.result_type)}</td><td><span class="status ${item.analytical_status}">${escapeHtml(item.analytical_status)}</span></td><td>${escapeHtml(JSON.stringify(item.warnings||[]))}</td></tr>`).join('')}</tbody></table>`:'Resultはありません。';
}
$('#result-family-filter').onchange=renderResultOptions;$('#result-type-filter').onchange=renderResultOptions;$('#result-status-filter').onchange=renderResultOptions;

async function loadUnifiedResults(){
  if(!state.project){state.unifiedResults=[];state.resultSummary=null;renderResultOptions();return}
  const [results,summary]=await Promise.all([api(`/projects/${state.project.project_id}/results`),api(`/projects/${state.project.project_id}/results/summary`)]);state.unifiedResults=results.items;state.resultSummary=summary;renderResultOptions();$('#result-summary').innerHTML=`<p><b>${summary.result_count}</b> Results</p><p>Family: ${escapeHtml(JSON.stringify(summary.by_family))}</p><p>Analytical status: ${escapeHtml(JSON.stringify(summary.by_analytical_status))}</p><p class="semantic-warning">${escapeHtml(summary.warning)}</p>`;
}

async function renderAnnotations(resultId){const values=(await api(`/projects/${state.project.project_id}/workspace-annotations?target_type=Result&target_id=${encodeURIComponent(resultId)}`)).items;$('#annotations').innerHTML=values.length?values.map(item=>`<article><b>${escapeHtml(item.decision||'ANNOTATION')}</b><p>${escapeHtml(item.statement)}</p><p>${escapeHtml(item.rationale||'')}</p><small>Revisions: ${item.revision_history.length}</small></article>`).join(''):'Annotationはありません。'}

$('#load-result').onclick=async()=>{const id=$('#result-select').value;if(!id)return;try{const [result,lineage]=await Promise.all([api(`/projects/${state.project.project_id}/results/${id}`),api(`/projects/${state.project.project_id}/results/${id}/lineage`)]);$('#result-detail').innerHTML=`<h2><span class="family-label">${result.analysis_family}</span> ${escapeHtml(result.result_type)}</h2><p class="status ${result.analytical_status}">${escapeHtml(result.analytical_status)}</p><h3>Summary</h3><pre>${escapeHtml(JSON.stringify(result.summary,null,2))}</pre><h3>Warnings / Limitations</h3><pre>${escapeHtml(JSON.stringify(result.warnings,null,2))}</pre><button id="export-result">Manifest Exportを作成</button>`;$('#export-result').onclick=async()=>{try{const exported=await api(`/projects/${state.project.project_id}/exports`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({result_ids:[id]})});const link=document.createElement('a');link.href=`${API}/projects/${state.project.project_id}/exports/${exported.export_id}/download`;link.download=`ariadne-export-${exported.export_id}.json`;link.click();notice('Export Manifestを作成しました')}catch(error){notice(error.message)}};const artifacts=result.artifact_ids||[];$('#artifacts').innerHTML='<h2>Artifacts</h2>'+(artifacts.length?artifacts.map(artifactId=>`<a href="${API}/projects/${state.project.project_id}/artifacts/${artifactId}/download">Artifact ${escapeHtml(artifactId)} download</a>`).join('<br>'):'Artifactはありません。');$('#lineage').textContent=JSON.stringify(lineage,null,2);await renderAnnotations(id)}catch(error){notice(error.message)}};

$('#compare-results').onclick=async()=>{const ids=$$('.result-compare-check:checked').map(item=>item.value);if(ids.length<2)return notice('比較するResultを2件以上選択してください');try{const comparison=await api(`/projects/${state.project.project_id}/comparisons`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({result_ids:ids})});$('#result-comparison').innerHTML=`<h2>Compatible comparison</h2><p>${comparison.analysis_family} / ${comparison.result_type}</p><p>Ranking: ${comparison.ranking===null?'実施しない':escapeHtml(comparison.ranking)}</p><pre>${escapeHtml(JSON.stringify({common:comparison.common_summary,differences:comparison.differences,warnings:comparison.warnings},null,2))}</pre>`}catch(error){notice(error.message)}};
$('#show-project-lineage').onclick=async()=>{try{$('#lineage').textContent=JSON.stringify(await api(`/projects/${state.project.project_id}/lineage`),null,2)}catch(error){notice(error.message)}};

$('#annotation-form').onsubmit=async event=>{event.preventDefault();const result=$('#result-select').value;if(!result)return notice('Resultを選択してください');const f=new FormData(event.target);try{await api(`/projects/${state.project.project_id}/workspace-annotations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_type:'Result',target_id:result,statement:f.get('statement'),rationale:f.get('rationale')||null,assumptions:list(String(f.get('assumptions')||'')),limitations:list(String(f.get('limitations')||'')),decision:f.get('decision')||null,next_actions:list(String(f.get('next_actions')||''))})});event.target.reset();await renderAnnotations(result);notice('Annotationを記録しました')}catch(error){notice(error.message)}};

async function refreshAll(){if(!state.project){state.workspaceState=null;state.unifiedResults=[];renderAnalysisContext();renderResultOptions();updatePredictiveAvailability();return}await Promise.all([loadDatasets(),loadGraphs(),loadExecutions(),loadAnalysisViews(),loadExplorationResults(),loadPredictiveWorkspace()]);await Promise.all([loadWorkspaceState(),loadUnifiedResults()])}
let draftStateTimer=null;
document.addEventListener('input',event=>{if(!state.project||!event.target.closest('form'))return;state.workspaceState={...(state.workspaceState||{}),unsaved_draft:true};renderAnalysisContext();if(draftStateTimer)clearTimeout(draftStateTimer);draftStateTimer=setTimeout(()=>saveWorkspaceState({unsaved_draft:true}).catch(error=>notice(error.message)),250)});
document.addEventListener('submit',()=>{if(!state.project)return;if(draftStateTimer)clearTimeout(draftStateTimer);saveWorkspaceState({unsaved_draft:false}).catch(error=>notice(error.message))});
// ENH-E1 contract references retained for traceability after the modal migration:
// target_graph_version_id:graph.graph_version_id
// parent_graph_version_id:parent||null
// origin=parent?$('#graph-transform').value:'DISCOVERED'
(async()=>{try{await fetch('/health/ready').then(r=>{if(!r.ok)throw Error();return r.json()});state.navigationCatalog=await api('/navigation/analysis');$('#health').textContent='API READY';await loadProjects();await restoreProjectRoute()}catch(error){$('#health').textContent='API UNAVAILABLE';notice(error.message)}})();
