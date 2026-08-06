const API="/api/v1";
const state={project:null,datasets:[],executions:[],results:[],graphs:[],editingGraph:null,sourceGraph:null};
const $=(selector)=>document.querySelector(selector);
const $$=(selector)=>[...document.querySelectorAll(selector)];

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
function notice(message){const el=$("#notice");el.textContent=message;el.classList.add("show");setTimeout(()=>el.classList.remove("show"),5000)}
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

$$('nav [data-workspace]').forEach(button=>button.onclick=async()=>{
  button.dataset.refreshStatus='pending';
  $$('nav button').forEach(x=>x.classList.remove('active'));button.classList.add('active');
  $$('.workspace').forEach(x=>x.classList.remove('active'));$('#'+button.dataset.workspace).classList.add('active');
  try{await refreshAll();button.dataset.refreshStatus='done'}catch(error){button.dataset.refreshStatus='failed';notice(error.message);throw error}
});

async function loadProjects(){
  const data=await api('/projects');const select=$('#project-select');
  select.innerHTML='<option value="">Projectを選択</option>'+data.items.map(p=>`<option value="${p.project_id}">${escapeHtml(p.name)}</option>`).join('');
  if(state.project){select.value=state.project.project_id}
}
$('#new-project').onclick=()=>{state.project=null;$('#project-form').reset();$$('nav [data-workspace]')[0].click()};
$('#project-select').onchange=async event=>{state.project=event.target.value?await api(`/projects/${event.target.value}`):null;fillProject();await refreshAll()};
function fillProject(){const form=$('#project-form');for(const name of ['name','topic','objective','memo'])form.elements[name].value=state.project?.[name]||''}
$('#project-form').onsubmit=async event=>{event.preventDefault();try{const body=Object.fromEntries(new FormData(event.target));state.project=state.project?await api(`/projects/${state.project.project_id}`,{method:'PATCH',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}):await api('/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});await loadProjects();$('#project-select').value=state.project.project_id;notice('Projectを保存しました')}catch(error){notice(error.message)}};

$('#dataset-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');try{const form=new FormData(event.target);await api(`/projects/${state.project.project_id}/dataset-versions`,{method:'POST',headers:{'Idempotency-Key':idempotencyKey()},body:form});event.target.reset();await loadDatasets();notice('Dataset Versionを登録しました')}catch(error){notice(error.message)}};
async function loadDatasets(){
  if(!state.project){state.datasets=[];return}
  state.datasets=(await api(`/projects/${state.project.project_id}/dataset-versions`)).items;
  $('#datasets').innerHTML=state.datasets.length?`<table><thead><tr><th>Name</th><th>Version</th><th>Schema</th><th>Rows × Columns</th><th>Hash</th><th></th></tr></thead><tbody>${state.datasets.map(d=>`<tr><td>${escapeHtml(d.name)}</td><td>${escapeHtml(d.version_label)}</td><td>${escapeHtml(Object.entries(d.schema).map(([name,type])=>`${name}:${type}`).join(', '))}</td><td>${d.row_count} × ${d.column_count}</td><td>${d.content_hash.slice(0,12)}</td><td><button onclick="preview('${d.dataset_version_id}')">Preview</button></td></tr>`).join('')}</tbody></table>`:'Datasetはありません';
  $$('.datasets-select').forEach(select=>select.innerHTML='<option value="">選択</option>'+state.datasets.map(d=>`<option value="${d.dataset_version_id}">${escapeHtml(d.name)} / ${escapeHtml(d.version_label)}</option>`).join(''));
}
window.preview=async id=>{try{const p=await api(`/dataset-versions/${id}/preview?limit=10`);$('#preview').innerHTML=`<h3>Preview</h3><table><thead><tr>${p.columns.map(c=>`<th>${escapeHtml(c)}</th>`).join('')}</tr></thead><tbody>${p.rows.map(row=>`<tr>${p.columns.map(c=>`<td>${escapeHtml(row[c])}</td>`).join('')}</tr>`).join('')}</tbody></table>`}catch(error){notice(error.message)}};

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

  return {operation:'DISCOVERY',dataset_version_id:datasetId,input_graph_version_id:null,input_result_id:null,objective:form.get('objective')||null,rationale:form.get('rationale')||null,analysis_spec:{schema_version:'causal-analysis-spec/2',analysis_mode:'EXPLORATORY',research_context:{problem_statement:null,research_question:null,significance:null,hypothesis:null},causal_question:{},causal_design:{adjustment_set:[],assumptions:[]},operation_spec:{feature_columns:features,constraints:{required_edges:[],forbidden_edges:[],temporal_tiers:[]},expected_graph_type:null},validation_override:null},variants,code_version:'web-enh-e1',runtime_versions:{client:'web'}};
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
async function loadExecutions(){if(!state.project){state.executions=[];state.results=[];return}state.executions=(await api(`/projects/${state.project.project_id}/executions`)).items;state.results=[];for(const execution of state.executions){if(execution.status==='SUCCEEDED'){const values=(await api(`/executions/${execution.execution_id}/results`)).items;values.forEach(value=>value.execution=execution);state.results.push(...values)}}const bases=$('#base-executions');if(bases)bases.innerHTML='<option value="">新規分析</option>'+state.executions.filter(e=>e.operation==='ESTIMATION').map(e=>`<option value="${e.execution_id}">${escapeHtml(e.algorithm_or_estimator)} / ${e.execution_id.slice(0,8)}</option>`).join('');renderDiscovery();renderInference();renderResultOptions()}
function resultRows(operation,target){const values=state.results.filter(r=>r.execution.operation===operation);target.innerHTML=values.length?`<table><thead><tr><th></th><th>Method</th><th>Status</th><th>Summary</th></tr></thead><tbody>${values.map(r=>`<tr><td><input type="checkbox" value="${r.result_id}"></td><td>${escapeHtml(r.execution.algorithm_or_estimator)}</td><td class="${r.scientific_status}">${r.scientific_status}</td><td>${escapeHtml(JSON.stringify(r.summary))}</td></tr>`).join('')}</tbody></table>`:'完了Resultはありません';return values}
function renderDiscovery(){const values=resultRows('DISCOVERY',$('#discovery-results'));$('#graph-source').innerHTML='<option value="">選択</option>'+values.map(r=>`<option value="${r.result_id}">${r.execution.algorithm_or_estimator} / ${r.result_id.slice(0,8)}</option>`).join('')}
async function refreshExecutions(button){button.dataset.refreshStatus='pending';try{await loadExecutions();button.dataset.refreshStatus='done'}catch(error){button.dataset.refreshStatus='failed';notice(error.message);throw error}}
$('#refresh-discovery').onclick=event=>refreshExecutions(event.currentTarget);
$('#compare-discovery').onclick=()=>compareChecked('#discovery-results','#discovery-comparison',3);
async function compareChecked(container,output,minimum=2){const ids=$$(`${container} input:checked`).map(x=>x.value);if(ids.length<minimum)return notice(`${minimum}件以上選択してください`);try{$(output).textContent=JSON.stringify(await api('/comparisons/query',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({project_id:state.project.project_id,result_ids:ids})}),null,2)}catch(error){notice(error.message)}}
$('#graph-source').onchange=()=>{const result=state.results.find(r=>r.result_id===$('#graph-source').value);if(result)$('#graph-parent').value='';state.sourceGraph=result?structuredClone(result.payload):null;state.editingGraph=result?structuredClone(result.payload):null;renderGraphEditor()};
$('#graph-parent').onchange=()=>{const graph=state.graphs.find(g=>g.graph_version_id===$('#graph-parent').value);if(graph)$('#graph-source').value='';state.sourceGraph=graph?structuredClone(graph.graph):null;state.editingGraph=graph?structuredClone(graph.graph):null;renderGraphEditor()};
function renderGraphEditor(){const graph=state.editingGraph;$('#graph-editor').innerHTML=!graph?'Resultを選択してください':`<p>Type: <b>${graph.graph_type}</b> / Nodes: ${graph.nodes.length}</p>${graph.edges.map((edge,index)=>`<div class="edge"><span>${escapeHtml(edge.source)} ${edge.endpoint_source} — ${edge.endpoint_target} ${escapeHtml(edge.target)}</span><button type="button" onclick="removeEdge(${index})">削除</button></div>`).join('')}`}
window.removeEdge=index=>{state.editingGraph.edges.splice(index,1);renderGraphEditor()};
$('#add-edge').onclick=()=>{if(!state.editingGraph)return;const source=$('#edge-source').value.trim(),target=$('#edge-target').value.trim();if(!state.editingGraph.nodes.includes(source)||!state.editingGraph.nodes.includes(target)||source===target)return notice('既存の異なるnodeを指定してください');state.editingGraph.edges.push({source,target,endpoint_source:'TAIL',endpoint_target:'ARROW'});renderGraphEditor()};
$('#save-graph').onclick=async()=>{const source=$('#graph-source').value,parent=$('#graph-parent').value,rationale=$('#graph-rationale').value.trim();if((!source&&!parent)||!state.editingGraph)return notice('Source ResultまたはParent Graphを選択してください');if(!rationale)return notice('選定・編集理由を入力してください');const changed=JSON.stringify(state.sourceGraph)!==JSON.stringify(state.editingGraph),origin=parent?$('#graph-transform').value:'DISCOVERED',provenance=parent&&origin==='CONSTRAINT_ADJUSTED'?{constraint_mode:'POST_HOC',source_note:rationale}:parent?{editor:'web-user',source_note:rationale}:{algorithm_output:true,source_note:rationale};if(!parent&&changed)return notice('Algorithm Outputは上書きせず、先にDISCOVERED Versionを保存してください');try{const graph=await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:parent?null:source,parent_graph_version_id:parent||null,graph_origin:origin,name:`Selected graph ${new Date().toISOString()}`,graph_type:state.editingGraph.graph_type,graph:state.editingGraph,provenance,edit_rationale:parent?rationale:null,fix_immediately:true})});await api(`/projects/${state.project.project_id}/annotations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_result_id:null,target_graph_version_id:graph.graph_version_id,statement:'Selected as the inference graph',rationale,assumptions:[],limitations:[]})});await loadGraphs();notice('FIXED Graph Versionとprovenanceを保存しました')}catch(error){notice(error.message)}};
$('#save-direct-graph').onclick=async()=>{if(!state.project)return notice('Projectを選択してください');const origin=$('#direct-graph-origin').value,note=$('#direct-graph-note').value.trim(),name=$('#direct-graph-name').value.trim();if(!note||!name)return notice('NameとSource / import noteを入力してください');let graph;try{graph=JSON.parse($('#direct-graph-json').value)}catch{return notice('Graph JSONが不正です')}try{await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:null,parent_graph_version_id:null,graph_origin:origin,name,graph_type:graph.graph_type,graph,provenance:{source_note:note},edit_rationale:null,fix_immediately:true})});await loadGraphs();notice('Direct GraphをFIXED Versionとして保存しました')}catch(error){notice(error.message)}};

async function loadGraphs(){if(!state.project){state.graphs=[];return}state.graphs=(await api(`/projects/${state.project.project_id}/graph-versions`)).items;const fixed=state.graphs.filter(g=>g.status==='FIXED');$('#fixed-graphs').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin}</option>`).join('');$('#graph-parent').innerHTML='<option value="">選択</option>'+fixed.map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)} / ${g.graph_origin}</option>`).join('')}
$('#inference-form').oninput=event=>{const f=new FormData(event.currentTarget),strategy=f.get('strategy'),difference=$('#inference-form input[value="difference_in_means"]');difference.disabled=strategy!=='RANDOMIZED';if(difference.disabled)difference.checked=false;const compatible=strategy==='RANDOMIZED'?'difference_in_means, ols, ipw, aipw':'ols, ipw, aipw';$('#preflight').textContent=`Preflight: treatment=${f.get('treatment')||'—'}, outcome=${f.get('outcome')||'—'}, adjustment=[${list(f.get('adjustment')).join(', ')}], FIXED graph=${f.get('graph_version_id')?'selected':'required'}, compatible estimators=${compatible}`};
function inferenceSpec(f,operation_spec,override=null){return {schema_version:'causal-analysis-spec/2',analysis_mode:f.get('analysis_mode')||'EXPLORATORY',research_context:{problem_statement:null,research_question:null,significance:null,hypothesis:null},causal_question:{population:f.get('population'),treatment:f.get('treatment'),comparator:f.get('comparator'),outcome:f.get('outcome'),analysis_unit:f.get('analysis_unit'),treatment_time:f.get('treatment_time'),outcome_window:f.get('outcome_window'),estimand:f.get('estimand'),decision_use:null},causal_design:{assignment_assumption:null,time_zero:f.get('treatment_time'),eligibility_criteria:[],identification_strategy:f.get('strategy'),adjustment_set:list(f.get('adjustment')),assumptions:list(f.get('assumptions'))},operation_spec,validation_override:override}}
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

async function refreshAll(){if(!state.project)return;await Promise.all([loadDatasets(),loadGraphs(),loadExecutions()])}
(async()=>{try{await fetch('/health/ready').then(r=>{if(!r.ok)throw Error();return r.json()});$('#health').textContent='API READY';await loadProjects()}catch{$('#health').textContent='API UNAVAILABLE'}})();
