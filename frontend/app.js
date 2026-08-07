const API="/api/v1";
const state={projects:[],project:null,datasets:[],analysisViews:[],researchContexts:[],exploratoryResults:[],executions:[],results:[],graphs:[],graphCandidates:[],graphCandidate:null,editingGraph:null,sourceGraph:null,predictiveCapabilities:null,predictiveSpecifications:[],predictiveExecutions:[],predictiveDetails:null,pendingArchive:null};
const $=(selector)=>document.querySelector(selector);
const $$=(selector)=>[...document.querySelectorAll(selector)];
const PROJECT_ROUTES=Object.freeze({context:'context',data:'data',explore:'explore',causal:'causal',predictive:'predictive',results:'results'});
const ROUTE_WORKSPACES=Object.freeze({context:'context',data:'data',explore:'explore',causal:'discovery',predictive:'predictive',results:'results'});
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

async function activateWorkspace(workspace,{push=true,button=null}={}){
  button=button||$$('nav [data-workspace]').find(item=>item.dataset.workspace===workspace);
  if(!button)return;
  button.dataset.refreshStatus='pending';
  $$('nav button').forEach(x=>x.classList.remove('active'));button.classList.add('active');
  $$('.workspace').forEach(x=>x.classList.remove('active'));$('#'+workspace).classList.add('active');
  if(push&&state.project&&button.dataset.route){
    const path=`/projects/${state.project.project_id}/${PROJECT_ROUTES[button.dataset.route]}`;
    if(location.pathname!==path)history.pushState({project_id:state.project.project_id,workspace},'',path);
  }
  try{await refreshAll();button.dataset.refreshStatus='done'}catch(error){button.dataset.refreshStatus='failed';notice(error.message);throw error}
}
$$('nav [data-workspace]').forEach(button=>button.onclick=()=>activateWorkspace(button.dataset.workspace,{button}));

async function restoreProjectRoute(){
  const match=location.pathname.match(/^\/projects\/([^/]+)\/(context|data|explore|causal|predictive|results)\/?$/);
  if(!match)return false;
  const [,projectId,route]=match;
  state.project=await api(`/projects/${projectId}`);
  fillProject();await loadProjects();$('#project-select').value=projectId;
  await activateWorkspace(ROUTE_WORKSPACES[route],{push:false});
  return true;
}
window.addEventListener('popstate',()=>restoreProjectRoute().catch(error=>notice(error.message)));

async function loadProjects(){
  const data=await api('/projects');state.projects=data.items;const select=$('#project-select');
  select.innerHTML='<option value="">Projectを選択</option>'+data.items.map(p=>`<option value="${p.project_id}">${escapeHtml(p.name)}</option>`).join('');
  if(state.project){select.value=state.project.project_id}
  $('#project-list').innerHTML=data.items.length?`<table><thead><tr><th>Name</th><th>Topic</th><th>Objective</th><th>Status</th><th></th></tr></thead><tbody>${data.items.map(p=>`<tr><td><button type="button" class="link-button" onclick="selectProject('${p.project_id}')">${escapeHtml(p.name)}</button></td><td>${escapeHtml(p.topic||'—')}</td><td>${escapeHtml(p.objective||'—')}</td><td><span class="status">${p.status}</span></td><td><button type="button" class="danger" onclick="requestArchive('${p.project_id}')">削除</button></td></tr>`).join('')}</tbody></table>`:'ACTIVE Projectはありません';
}
$('#new-project').onclick=()=>activateWorkspace('management');
$('#project-select').onchange=async event=>{state.project=event.target.value?await api(`/projects/${event.target.value}`):null;fillProject();if(state.project)await activateWorkspace('data');else await refreshAll()};
window.selectProject=async id=>{state.project=await api(`/projects/${id}`);fillProject();await loadProjects();await activateWorkspace('data')};
function fillProject(){const form=$('#project-form');for(const name of ['name','topic','objective','memo'])form.elements[name].value=state.project?.[name]||''}
$('#project-register-form').onsubmit=async event=>{event.preventDefault();try{state.project=await api('/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(event.target)))});event.target.reset();await loadProjects();$('#project-select').value=state.project.project_id;fillProject();notice('Projectを登録しました')}catch(error){notice(error.message)}};
$('#project-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('ACTIVE Projectを選択してください');try{const body=Object.fromEntries(new FormData(event.target));state.project=await api(`/projects/${state.project.project_id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});await loadProjects();$('#project-select').value=state.project.project_id;notice('Project metadataを更新しました')}catch(error){notice(error.message)}};
window.requestArchive=id=>{state.pendingArchive=id;$('#archive-modal').showModal()};
$('#confirm-archive').onclick=async()=>{if(!state.pendingArchive)return;try{await api(`/projects/${state.pendingArchive}`,{method:'DELETE'});if(state.project?.project_id===state.pendingArchive){state.project=null;fillProject();state.datasets=[];state.executions=[];state.results=[];state.graphs=[];state.graphCandidates=[];state.researchContexts=[];state.predictiveExecutions=[]}state.pendingArchive=null;$('#archive-modal').close();await loadProjects();$('#project-select').value='';history.pushState({},'', '/');await activateWorkspace('management',{push:false});notice('ProjectをARCHIVEDへ変更しました。既存Lineageは保持されます')}catch(error){notice(error.message)}};

$('#dataset-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');try{const form=new FormData(event.target);await api(`/projects/${state.project.project_id}/dataset-versions`,{method:'POST',headers:{'Idempotency-Key':idempotencyKey()},body:form});event.target.reset();await loadDatasets();notice('Dataset Versionを登録しました')}catch(error){notice(error.message)}};
async function loadDatasets(){
  if(!state.project){state.datasets=[];return}
  state.datasets=(await api(`/projects/${state.project.project_id}/dataset-versions`)).items;
  $('#datasets').innerHTML=state.datasets.length?`<table><thead><tr><th>Name</th><th>Version</th><th>Schema</th><th>Rows × Columns</th><th>Hash</th><th></th></tr></thead><tbody>${state.datasets.map(d=>`<tr><td>${escapeHtml(d.name)}</td><td>${escapeHtml(d.version_label)}</td><td>${escapeHtml(Object.entries(d.schema).map(([name,type])=>`${name}:${type}`).join(', '))}</td><td>${d.row_count} × ${d.column_count}</td><td>${d.content_hash.slice(0,12)}</td><td><button onclick="preview('${d.dataset_version_id}')">Preview</button></td></tr>`).join('')}</tbody></table>`:'Datasetはありません';
  $$('.datasets-select').forEach(select=>select.innerHTML='<option value="">選択</option>'+state.datasets.map(d=>`<option value="${d.dataset_version_id}">${escapeHtml(d.name)} / ${escapeHtml(d.version_label)}</option>`).join(''));
  updatePredictiveAvailability();
}
window.preview=async id=>{try{const p=await api(`/dataset-versions/${id}/preview?limit=10`);$('#preview').innerHTML=`<h3>Preview</h3><table><thead><tr>${p.columns.map(c=>`<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>${p.rows.map(row=>`<tr>${p.columns.map(c=>`<td>${escapeHtml(row[c])}</td>`).join('')}</tr>`).join('')}</tbody></table>`}catch(error){notice(error.message)}};

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
function renderExplorationResults(){const target=$('#exploration-results');if(!target)return;target.innerHTML=state.exploratoryResults.length?`<table><thead><tr><th>Family</th><th>Result</th><th>Status</th><th>Summary</th><th>Explicit transition</th></tr></thead><tbody>${state.exploratoryResults.map(result=>`<tr><td><span class="family-label">EXPLORATORY</span></td><td>${escapeHtml(result.result_type)}</td><td>${escapeHtml(result.analytical_status)}</td><td>${escapeHtml(JSON.stringify(result.summary))}</td><td><div class="explore-actions"><button type="button" onclick="showExploration('${result.result_id}')">表示</button><button type="button" onclick="createExplorationDraft('${result.result_id}','CAUSAL')">Causal draft</button><button type="button" onclick="createExplorationDraft('${result.result_id}','PREDICTIVE')">Predictive draft</button></div></td></tr>`).join('')}</tbody></table>`:'保存済み探索Resultはありません'}
window.showExploration=id=>{const result=state.exploratoryResults.find(value=>value.result_id===id);if(result)renderExplorationResult(result)};
window.createExplorationDraft=async(id,family)=>{try{const draft=await api(`/projects/${state.project.project_id}/exploration/results/${id}/create-analysis-draft`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_family:family})});notice(`${family} draftを作成しました: ${draft.source_relation.warning}`)}catch(error){notice(error.message)}};
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
  const select=$('#predictive-context');if(!select)return;
  const selected=select.value;
  select.innerHTML='<option value="">FIXED Contextを選択</option>'+fixed.map(context=>`<option value="${context.research_context_version_id}">${escapeHtml(context.context_key)} / v${context.version_number}</option>`).join('');
  if(fixed.some(context=>context.research_context_version_id===selected))select.value=selected;
  updatePredictiveAvailability();
}

function predictiveFamilySpec(){
  const form=new FormData($('#predictive-form')),task=String(form.get('task_type')),target=String(form.get('target')).trim(),features=list(String(form.get('feature_columns')||'')),excluded=[...new Set([...list(String(form.get('excluded_columns')||'')),target])],strategy=String(form.get('split_strategy')),seed=Number(form.get('seed'));
  if(task==='REGRESSION'&&strategy==='STRATIFIED')throw new Error('RegressionではSTRATIFIED splitを使用できません');
  const availability=Object.fromEntries(features.map(column=>[column,{column,available_at:'PREDICTION_TIME',allowed:true}]));
  const classification=task==='BINARY_CLASSIFICATION';
  return {schema_version:'predictive-analysis-spec/1',task_type:task,prediction_question:{prediction_unit:String(form.get('prediction_unit')),target,prediction_time:String(form.get('prediction_time')),horizon:String(form.get('horizon')),intended_use:String(form.get('intended_use')),deployment_population:String(form.get('deployment_population'))},feature_spec:{feature_columns:features,availability_cutoff:availability,excluded_columns:excluded},split_spec:{strategy,train_ratio:Number(form.get('train_ratio')),validation_ratio:Number(form.get('validation_ratio')),test_ratio:Number(form.get('test_ratio')),group_column:null,time_column:null,train_cutoff:null,validation_cutoff:null,stratify:strategy==='STRATIFIED',seed},preprocessing_spec:{fit_partition:'TRAIN',numeric_imputation:'MEAN',scale_numeric:true,categorical_encoding:'ONE_HOT'},model_spec:{model_id:classification?'logistic_regression.v1':'linear_regression.v1',parameters:classification?{iterations:800,learning_rate:0.1,l2:0.001}:{l2:0}},tuning_spec:{selection_partitions:['TRAIN','VALIDATION']},evaluation_spec:{primary_metric:classification?'ROC_AUC':'RMSE',secondary_metrics:[],subgroups:[]},explanation_spec:{method:String(form.get('explanation_method')),dataset:'TEST',sampling:{strategy:'FIRST_N',size:Number(form.get('explanation_sample_size')),seed},local_explanations:form.get('local_explanations')==='on'}};
}

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
  const resultTarget=$('#predictive-results'),artifactTarget=$('#predictive-artifacts'),details=state.predictiveDetails;
  if(!details){resultTarget.textContent='Resultはありません。';artifactTarget.textContent='Artifactはありません。';return}
  const familySpec=details.specification?.family_spec||{},question=familySpec.prediction_question||{},features=familySpec.feature_spec||{},split=familySpec.split_spec||{};
  const specificationSummary=`<article class="predictive-result" data-predictive-specification><h3>Execution inputs</h3><p>Research Context: ${escapeHtml(details.execution.research_context_version_id||'—')} / Dataset Version: ${escapeHtml(details.execution.dataset_version_id||'—')} / Analysis View: ${escapeHtml(details.execution.analysis_view_id||'Dataset Version全体')}</p><p>Task: ${escapeHtml(familySpec.task_type||'—')} / Target: ${escapeHtml(question.target||'—')} / Features: ${escapeHtml((features.feature_columns||[]).join(', ')||'—')} / Split: ${escapeHtml(split.strategy||'—')}</p></article>`;
  const orderedResults=[...details.results].sort((left,right)=>PREDICTIVE_RESULT_ORDER.indexOf(left.result_type)-PREDICTIVE_RESULT_ORDER.indexOf(right.result_type));
  resultTarget.innerHTML=`<p><b>Execution ${details.execution.execution_id.slice(0,8)}</b> <span class="status ${details.execution.status}">${details.execution.status}</span></p><p>Stages: ${details.stages.map(stage=>`${escapeHtml(stage.stage_key)}=${escapeHtml(stage.status)}`).join(' → ')}</p>${specificationSummary}`+orderedResults.map(result=>`<article class="predictive-result" data-result-type="${escapeHtml(result.result_type)}"><div class="badge-row"><span class="family-label">PREDICTIVE</span><span class="status">${escapeHtml(result.analytical_status)}</span></div><h3>${escapeHtml(result.result_type)}</h3><pre>${escapeHtml(JSON.stringify({summary:result.summary,payload:result.payload,diagnostics:result.diagnostics,warnings:result.warnings},null,2))}</pre></article>`).join('');
  artifactTarget.innerHTML=details.artifacts.length?details.artifacts.map(artifact=>`<article><b>${escapeHtml(artifact.artifact_type)}</b><p>Artifact ${artifact.artifact_id}</p><p>Result ${escapeHtml(artifact.result_id||'—')}</p><small>${escapeHtml(artifact.schema_version)} / ${escapeHtml(artifact.media_type)} / ${artifact.size_bytes} bytes / ${artifact.content_hash}</small></article>`).join(''):'Artifactはありません。';
}
window.showPredictiveExecution=async id=>{try{await loadPredictiveDetails(id)}catch(error){notice(error.message)}};

async function loadPredictiveWorkspace(){
  if(!state.project){state.researchContexts=[];state.predictiveCapabilities=null;state.predictiveSpecifications=[];state.predictiveExecutions=[];state.predictiveDetails=null;renderResearchContexts();renderPredictiveExecutions();renderPredictiveDetails();updatePredictiveAvailability();return}
  const projectId=state.project.project_id;
  const [capabilities,contexts,specifications,executions]=await Promise.all([api(`/projects/${projectId}/predictive/capabilities`),api(`/projects/${projectId}/research-contexts`),api(`/projects/${projectId}/analysis-specifications`),api(`/projects/${projectId}/executions`)]);
  state.predictiveCapabilities=capabilities;state.researchContexts=contexts.items;state.predictiveSpecifications=specifications.items.filter(specification=>specification.analysis_family==='PREDICTIVE');state.predictiveExecutions=executions.items.filter(execution=>execution.analysis_family==='PREDICTIVE'&&execution.analysis_specification_id);
  $('#predictive-capabilities').innerHTML=`<p><b>${escapeHtml(capabilities.gate)}</b> — Training ${capabilities.training_available?'available':'unavailable'} / Evaluation ${capabilities.evaluation_available?'available':'unavailable'} / Explanation ${capabilities.explanation_available?'available':'unavailable'} / Model Card ${capabilities.model_card_available?'available':'unavailable'}</p><p>Models: ${capabilities.model_registry.map(model=>escapeHtml(model.model_id)).join(', ')}</p>`;
  const method=$('#predictive-explanation-method'),selected=method.value;method.innerHTML=capabilities.explanation_methods.map(item=>`<option value="${escapeHtml(item.method)}">${escapeHtml(item.method)}</option>`).join('');if(capabilities.explanation_methods.some(item=>item.method===selected))method.value=selected;
  renderResearchContexts();renderPredictiveExecutions();updatePredictiveAvailability();
  if(state.predictiveExecutions.length)await loadPredictiveDetails(state.predictiveExecutions[0].execution_id);else{state.predictiveDetails=null;renderPredictiveDetails()}
}

$('#predictive-form').elements.task_type.onchange=event=>{if(event.target.value==='REGRESSION'&&$('#predictive-form').elements.split_strategy.value==='STRATIFIED')$('#predictive-form').elements.split_strategy.value='RANDOM'};
$('#predictive-form').onsubmit=async event=>{
  event.preventDefault();if(!state.project)return notice('Projectを選択してください');
  const button=$('#run-predictive'),form=new FormData(event.target),projectId=state.project.project_id;button.disabled=true;
  try{
    const familySpec=predictiveFamilySpec(),datasetId=String(form.get('dataset_version_id')),viewId=String(form.get('analysis_view_id')||'')||null;
    const split=await api(`/projects/${projectId}/predictive/split-validations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({dataset_version_id:datasetId,analysis_view_id:viewId,family_spec:familySpec})});
    $('#predictive-split-validation').innerHTML=`<p><span class="status VALID">${escapeHtml(split.status)}</span> ${escapeHtml(split.strategy)}</p><pre>${escapeHtml(JSON.stringify({partition_counts:split.partition_counts,source_snapshot:split.source_snapshot,artifact:split.partition_artifact},null,2))}</pre>`;
    const specification=await api(`/projects/${projectId}/analysis-specifications`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({schema_version:'analysis-specification/1',specification_key:`predictive-${Date.now()}`,analysis_family:'PREDICTIVE',research_context_version_id:String(form.get('research_context_version_id')),dataset_version_id:datasetId,analysis_view_id:viewId,analysis_mode:'CONFIRMATORY',family_spec_schema_version:'predictive-analysis-spec/1',family_spec:familySpec,revision_context:null,warnings:[]})});
    await api(`/projects/${projectId}/analysis-specifications/${specification.analysis_specification_id}/validate`,{method:'POST'});
    await api(`/projects/${projectId}/analysis-specifications/${specification.analysis_specification_id}/fix`,{method:'POST'});
    const plan=await api(`/projects/${projectId}/execution-plans`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({analysis_specification_id:specification.analysis_specification_id})});
    await api(`/projects/${projectId}/execution-plans/${plan.execution_plan_id}/validate`,{method:'POST'});
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
$('#adopt-graph').onclick=async()=>{const candidate=state.graphCandidate,rationale=$('#graph-rationale').value.trim();if(candidate?.candidate_kind!=='DISCOVERY_RESULT')return notice('Algorithm Outputだけを直接採用できます');if(!rationale)return notice('選定理由を入力してください');try{const graph=await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({source_result_id:candidate.candidate_id,parent_graph_version_id:null,graph_origin:'DISCOVERED',name:`Selected graph ${new Date().toISOString()}`,graph_type:candidate.graph_type,graph:candidate.graph,designated_outcome_node:candidate.designated_outcome_node,provenance:{algorithm_output:true,selection_rationale:rationale},edit_rationale:rationale,fix_immediately:true})});await loadGraphs();await inspectCandidate('GRAPH_VERSION',graph.graph_version_id);notice('Algorithm Outputを変更せずDISCOVERED FIXED Versionとして採用しました')}catch(error){notice(error.message)}};
$('#save-direct-graph').onclick=async()=>{if(!state.project)return notice('Projectを選択してください');const origin=$('#direct-graph-origin').value,note=$('#direct-graph-note').value.trim(),name=$('#direct-graph-name').value.trim(),outcome=$('#direct-graph-outcome').value.trim();if(!note||!name||!outcome)return notice('Name、Designated Outcome、Source / import noteを入力してください');let graph;try{graph=JSON.parse($('#direct-graph-json').value)}catch{return notice('Graph JSONが不正です')}try{await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:null,parent_graph_version_id:null,graph_origin:origin,name,graph_type:graph.graph_type,graph,designated_outcome_node:outcome,provenance:{source_note:note},edit_rationale:null,fix_immediately:false})});await loadGraphs();notice('Direct GraphをDRAFT Versionとして保存しました')}catch(error){notice(error.message)}};

function renderGraphCandidates(){const target=$('#graph-candidates');if(!target)return;target.innerHTML=state.graphCandidates.length?`<table><thead><tr><th></th><th>Kind / FIXED</th><th>Source / Parent</th><th>Type / Origin</th><th>Status</th><th>Outcome</th><th>Summary</th><th>操作</th></tr></thead><tbody>${state.graphCandidates.map(c=>`<tr><td><input class="candidate-check" type="checkbox" data-kind="${c.candidate_kind}" value="${c.candidate_id}"></td><td>${c.candidate_kind}<br><span class="status">${c.fixed?'FIXED':'—'}</span></td><td>${escapeHtml(c.parent_graph_version_id||c.source_result_id||'root')}</td><td>${c.graph_type}<br>${c.graph_origin}</td><td>${escapeHtml(c.version_status||c.scientific_status||'—')}</td><td>${escapeHtml(c.designated_outcome_node||'未指定')}</td><td>${c.summary.node_count} nodes / ${c.summary.edge_count} edges<br>${escapeHtml(c.warnings.join?.(', ')||'')}</td><td><button type="button" onclick="inspectCandidate('${c.candidate_kind}','${c.candidate_id}')">グラフを確認/編集する</button></td></tr>`).join('')}</tbody></table>`:'Graph Candidateはありません';$$('.candidate-check').forEach(item=>item.onchange=()=>{$('#compare-discovery').disabled=$$('.candidate-check:checked').length<2})}
window.inspectCandidate=inspectCandidate;
async function inspectCandidate(kind,id){try{const candidate=await api(`/projects/${state.project.project_id}/graph-candidates/${kind}/${id}`);state.graphCandidate=candidate;state.sourceGraph=structuredClone(candidate.graph);state.editingGraph=structuredClone(candidate.graph);$('#graph-meta').innerHTML=`<div class="badge-row"><span class="status">${candidate.graph_type}</span><span class="status">${candidate.graph_origin}</span><span class="status">${candidate.version_status||candidate.scientific_status}</span></div><p>Source: ${escapeHtml(candidate.source_result_id||'—')} / Parent: ${escapeHtml(candidate.parent_graph_version_id||'—')}</p><p>Outcome: ${escapeHtml(candidate.designated_outcome_node||'未指定')}</p>`;$('#graph-outcome').value=candidate.designated_outcome_node||'';$('#graph-rationale').value=candidate.summary.edit_rationale||'';$('#adopt-graph').hidden=candidate.candidate_kind!=='DISCOVERY_RESULT';$('#save-graph').disabled=!(candidate.allowed_actions.can_edit||candidate.allowed_actions.can_create_child);$('#fix-graph').disabled=!candidate.allowed_actions.can_fix;$('#add-edge').disabled=!(candidate.allowed_actions.can_edit||candidate.allowed_actions.can_create_child);$('#save-graph').textContent=candidate.allowed_actions.can_edit?'DRAFTを更新':'子DRAFTを作成';renderGraphEditor();$('#graph-modal').showModal()}catch(error){notice(error.message)}}
$('#close-graph-modal').onclick=()=>$('#graph-modal').close();
async function compareGraphCandidates(){const refs=$$('.candidate-check:checked').map(item=>({candidate_kind:item.dataset.kind,candidate_id:item.value}));if(refs.length<2)return notice('2件以上選択してください');try{const comparison=await api(`/projects/${state.project.project_id}/graph-candidate-comparisons/query`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({candidate_refs:refs})});$('#comparison-tabs').innerHTML=comparison.candidates.map((candidate,index)=>`<button type="button" data-index="${index}">${escapeHtml(candidate.summary.name||candidate.candidate_id.slice(0,8))}</button>`).join('');const show=index=>{const candidate=comparison.candidates[index];renderGraphVisual(candidate.graph,$('#comparison-graph'),candidate.designated_outcome_node);$('#comparison-summary').innerHTML=`<p><b>${candidate.graph_type}</b> / ${candidate.graph_origin} / ${candidate.summary.node_count} nodes / ${candidate.summary.edge_count} edges / Outcome: ${escapeHtml(candidate.designated_outcome_node||'未指定')}</p><h3>Compatibility</h3><p>${comparison.compatibility.compatible?'比較可能':`比較不能: ${escapeHtml(comparison.compatibility.reasons.join(', '))}`}</p><h3>Structure diff</h3>${comparison.compatibility.compatible?`<pre>${escapeHtml(JSON.stringify(comparison.differences,null,2))}</pre>`:'個別タブのGraph表示は利用できます。'}`};$$('#comparison-tabs button').forEach(button=>button.onclick=()=>show(Number(button.dataset.index)));show(0);$('#graph-comparison-modal').showModal()}catch(error){notice(error.message)}}
$('#close-comparison-modal').onclick=()=>$('#graph-comparison-modal').close();
function renderGraphVisual(graph,target,outcome){if(!graph){target.innerHTML='Graphはありません';return}const nodes=[...graph.nodes].sort((a,b)=>a===outcome?1:b===outcome?-1:a.localeCompare(b)),columns=Math.min(6,Math.max(1,nodes.length)),rows=Math.max(1,Math.ceil(nodes.length/columns)),width=Math.max(480,columns*140),height=rows*180+100,positions=new Map(nodes.map((node,index)=>{const row=Math.floor(index/columns),column=node===outcome?columns-1:index%columns;return [node,{x:70+column*(width-140)/Math.max(1,columns-1),y:80+row*180+(column%2)*90}]}));target.innerHTML=`<svg class="graph-svg" width="100%" viewBox="0 0 ${width} ${height}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${escapeHtml(graph.graph_type)} graph">${graph.edges.map(edge=>{const a=positions.get(edge.source),b=positions.get(edge.target);return a&&b?`<line x1="${a.x}" y1="${a.y}" x2="${b.x}" y2="${b.y}" class="graph-edge"/><text x="${(a.x+b.x)/2}" y="${(a.y+b.y)/2-5}" class="edge-label">${edge.endpoint_source}→${edge.endpoint_target}</text>`:''}).join('')}${nodes.map(node=>{const p=positions.get(node);return `<g class="graph-node ${node===outcome?'outcome':''}"><circle cx="${p.x}" cy="${p.y}" r="32"/><text x="${p.x}" y="${p.y+4}">${escapeHtml(node)}</text></g>`}).join('')}</svg>`}

async function loadGraphs(){if(!state.project){state.graphs=[];state.graphCandidates=[];renderGraphCandidates();return}const [graphs,candidates]=await Promise.all([api(`/projects/${state.project.project_id}/graph-versions`),api(`/projects/${state.project.project_id}/graph-candidates`)]);state.graphs=graphs.items;state.graphCandidates=candidates.items;const fixed=state.graphs.filter(g=>g.status==='FIXED'&&g.designated_outcome_node);$('#fixed-graphs').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin} / ${escapeHtml(g.designated_outcome_node)}</option>`).join('');$('#graph-parent').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin}</option>`).join('');renderGraphCandidates()}
function selectedInferenceGraph(){return state.graphs.find(graph=>graph.graph_version_id===$('#fixed-graphs').value)}
$('#fixed-graphs').onchange=()=>{const graph=selectedInferenceGraph(),outcome=graph?.designated_outcome_node;$('#inference-outcome').textContent=outcome||'Outcome未指定のため使用できません';$('#run-identification').disabled=!outcome;$('#inference-form').dispatchEvent(new Event('input',{bubbles:true}))};
$('#inference-form').oninput=event=>{const f=new FormData(event.currentTarget),strategy=f.get('strategy'),difference=$('#inference-form input[value="difference_in_means"]'),outcome=selectedInferenceGraph()?.designated_outcome_node;difference.disabled=strategy!=='RANDOMIZED';if(difference.disabled)difference.checked=false;const compatible=strategy==='RANDOMIZED'?'difference_in_means, ols, ipw, aipw':'ols, ipw, aipw';$('#preflight').textContent=`Preflight: treatment=${f.get('treatment')||'—'}, outcome=${outcome||'Graphで指定が必要'}, adjustment=[${list(f.get('adjustment')).join(', ')}], FIXED graph=${f.get('graph_version_id')?'selected':'required'}, compatible estimators=${compatible}`};
function inferenceSpec(f,operation_spec,override=null){const outcome=selectedInferenceGraph()?.designated_outcome_node;return {schema_version:'causal-analysis-spec/2',analysis_mode:f.get('analysis_mode')||'EXPLORATORY',research_context:{problem_statement:null,research_question:null,significance:null,hypothesis:null},causal_question:{population:f.get('population'),treatment:f.get('treatment'),comparator:f.get('comparator'),outcome,analysis_unit:f.get('analysis_unit'),treatment_time:f.get('treatment_time'),outcome_window:f.get('outcome_window'),estimand:f.get('estimand'),decision_use:null},causal_design:{assignment_assumption:null,time_zero:f.get('treatment_time'),eligibility_criteria:[],identification_strategy:f.get('strategy'),adjustment_set:list(f.get('adjustment')),assumptions:list(f.get('assumptions'))},operation_spec,validation_override:override}}
$('#run-identification').onclick=async()=>{const form=$('#inference-form'),f=new FormData(form);try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'IDENTIFICATION',dataset_version_id:f.get('dataset_version_id'),input_graph_version_id:f.get('graph_version_id'),input_result_id:null,objective:'Identify causal effect',rationale:'Identification-first gate',analysis_spec:inferenceSpec(f,{allow_partial_identification:false}),variants:[{algorithm_or_estimator:'GRAPHICAL_IDENTIFICATION',parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Identificationを受け付けました');await loadExecutions()}catch(error){notice(error.message)}};
$('#inference-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');const f=new FormData(event.target),estimators=f.getAll('estimators'),reason=String(f.get('override_reason')||'').trim(),override=reason?{reason,actor:'web-user',warning_codes:['ELIGIBILITY_WARN']}:null,base=String(f.get('base_execution_id')||'')||null,changeReason=String(f.get('change_reason')||'').trim()||null;try{const response=await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'ESTIMATION',dataset_version_id:f.get('dataset_version_id'),input_graph_version_id:f.get('graph_version_id'),input_result_id:f.get('identification_result_id'),objective:'Estimate binary treatment effect',rationale:'Compare estimator sensitivity',analysis_spec:inferenceSpec(f,{inference_options:{}},override),variants:estimators.map(x=>({algorithm_or_estimator:x,parameters:{},random_seed:42})),code_version:'web-enh-e1',runtime_versions:{client:'web'},base_execution_id:base,change_reason:changeReason})});const warnings=response.executions.flatMap(x=>x.scientific_warnings||[]);$('#scientific-warnings').textContent=warnings.map(x=>`${x.warning_code}: ${x.message}`).join('\n');notice(warnings.length?`${estimators.length}件を警告付きで受け付けました`:`${estimators.length}件のEstimationを受け付けました`);await loadExecutions()}catch(error){notice(error.message)}};
function renderInference(){const ids=state.results.filter(r=>r.result_type==='IDENTIFICATION_RESULT');$('#identification-results').innerHTML='<option value="">選択</option>'+ids.map(r=>`<option value="${r.result_id}">${r.scientific_status} / ${r.result_id.slice(0,8)}</option>`).join('');$('#identification-panel').innerHTML=state.results.filter(r=>['IDENTIFICATION_RESULT','DATA_ELIGIBILITY_RESULT'].includes(r.result_type)).map(r=>`<p><b>${r.result_type}</b> <span class="${r.scientific_status}">${r.scientific_status}</span> ${escapeHtml(JSON.stringify({summary:r.summary,inferred_types:r.payload?.inferred_types,checks:r.payload?.checks,warnings:r.warnings}))}</p>`).join('')||'Resultはありません';resultRows('ESTIMATION',$('#inference-results'));const effects=state.results.filter(r=>r.result_type==='TREATMENT_EFFECT_RESULT');$$('.effect-results').forEach(select=>select.innerHTML='<option value="">選択</option>'+effects.map(r=>`<option value="${r.result_id}">${r.scientific_status} / ${r.result_id.slice(0,8)}</option>`).join(''))}
$('#refresh-inference').onclick=event=>refreshExecutions(event.currentTarget);$('#compare-inference').onclick=()=>compareChecked('#inference-results','#inference-comparison',2);

function followupSpec(operation_spec){return {schema_version:'causal-analysis-spec/2',analysis_mode:'EXPLORATORY',research_context:{},causal_question:{},causal_design:{adjustment_set:[],assumptions:[]},operation_spec,validation_override:null}}
$('#refutation-form').onsubmit=async event=>{event.preventDefault();const f=new FormData(event.target),base=state.results.find(r=>r.result_id===f.get('result_id'));if(!base)return notice('Treatment Effect Resultを選択してください');const method=f.get('method'),operation_spec=method==='PLACEBO_TREATMENT'?{method,repetitions:Number(f.get('repetitions'))}:{method,subset_fraction:Number(f.get('subset_fraction'))};try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'REFUTATION',dataset_version_id:base.execution.dataset_version_id,input_graph_version_id:base.execution.input_graph_version_id,input_result_id:base.result_id,objective:'Refute treatment effect',rationale:'ENH-E1 minimum refutation',analysis_spec:followupSpec(operation_spec),variants:[{algorithm_or_estimator:method,parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Refutationを受け付けました')}catch(error){notice(error.message)}};
$('#sensitivity-form').onsubmit=async event=>{event.preventDefault();const f=new FormData(event.target),base=state.results.find(r=>r.result_id===f.get('result_id'));if(!base)return notice('Treatment Effect Resultを選択してください');const dimension=f.get('dimension'),operation_spec=dimension==='PROPENSITY_CLIPPING'?{dimension,values:list(f.get('values')).map(Number)}:{dimension,adjustment_sets:String(f.get('adjustment_sets')||'').split(';').filter(Boolean).map(list)};try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'SENSITIVITY',dataset_version_id:base.execution.dataset_version_id,input_graph_version_id:base.execution.input_graph_version_id,input_result_id:base.result_id,objective:'Assess sensitivity',rationale:'ENH-E1 minimum sensitivity',analysis_spec:followupSpec(operation_spec),variants:[{algorithm_or_estimator:dimension,parameters:{},random_seed:42}],code_version:'web-enh-e1',runtime_versions:{client:'web'}})});notice('Sensitivityを受け付けました')}catch(error){notice(error.message)}};

function renderResultOptions(){const types=[...new Set(state.results.map(r=>r.result_type))].sort(),statuses=[...new Set(state.results.map(r=>r.scientific_status))].sort(),type=$('#result-type-filter').value,status=$('#result-status-filter').value;$('#result-type-filter').innerHTML='<option value="">すべて</option>'+types.map(value=>`<option ${value===type?'selected':''}>${value}</option>`).join('');$('#result-status-filter').innerHTML='<option value="">すべて</option>'+statuses.map(value=>`<option ${value===status?'selected':''}>${value}</option>`).join('');const values=state.results.filter(r=>(!type||r.result_type===type)&&(!status||r.scientific_status===status));$('#result-select').innerHTML='<option value="">選択</option>'+values.map(r=>`<option value="${r.result_id}">${r.result_type} / ${r.execution.algorithm_or_estimator} / ${r.scientific_status}</option>`).join('')}
$('#result-type-filter').onchange=renderResultOptions;
$('#result-status-filter').onchange=renderResultOptions;
$('#load-result').onclick=async()=>{const id=$('#result-select').value;if(!id)return;try{const result=await api(`/results/${id}`),lineage=await api(`/results/${id}/lineage`);$('#result-detail').innerHTML=`<h2>${result.result_type}</h2><p class="status ${result.scientific_status}">${result.scientific_status}</p><pre>${escapeHtml(JSON.stringify({summary:result.summary,diagnostics:result.diagnostics,warnings:result.warnings},null,2))}</pre><button id="export-result">Export JSON</button>`;$('#export-result').onclick=async()=>{try{const manifest=await api(`/results/${id}/export`,{method:'POST'}),blob=new Blob([JSON.stringify(manifest,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=`ariadne-result-${id}.json`;link.click();URL.revokeObjectURL(url)}catch(error){notice(error.message)}};const artifactNodes=lineage.nodes.filter(n=>n.node_type==='Artifact');$('#artifacts').innerHTML='<h2>Artifacts</h2>'+artifactNodes.map(n=>`<a href="${API}/artifacts/${n.entity_id}/download">${escapeHtml(n.label)} download</a>`).join('<br>');$('#lineage').textContent=JSON.stringify(lineage,null,2)}catch(error){notice(error.message)}};
$('#annotation-form').onsubmit=async event=>{event.preventDefault();const result=$('#result-select').value;if(!result)return notice('Resultを選択してください');const f=new FormData(event.target);try{await api(`/projects/${state.project.project_id}/annotations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_result_id:result,target_graph_version_id:null,statement:f.get('statement'),rationale:f.get('rationale')||null,assumptions:list(f.get('assumptions')),limitations:list(f.get('limitations'))})});event.target.reset();notice('Annotationを記録しました')}catch(error){notice(error.message)}};

async function refreshAll(){if(!state.project){updatePredictiveAvailability();return}await Promise.all([loadDatasets(),loadGraphs(),loadExecutions(),loadAnalysisViews(),loadExplorationResults(),loadPredictiveWorkspace()])}
// ENH-E1 contract references retained for traceability after the modal migration:
// target_graph_version_id:graph.graph_version_id
// parent_graph_version_id:parent||null
// origin=parent?$('#graph-transform').value:'DISCOVERED'
(async()=>{try{await fetch('/health/ready').then(r=>{if(!r.ok)throw Error();return r.json()});$('#health').textContent='API READY';await loadProjects();await restoreProjectRoute()}catch(error){$('#health').textContent='API UNAVAILABLE';notice(error.message)}})();
