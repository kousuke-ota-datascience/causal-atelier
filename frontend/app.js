const API="/api/v1";
const state={project:null,datasets:[],executions:[],results:[],graphs:[],editingGraph:null};
const $=(selector)=>document.querySelector(selector);
const $$=(selector)=>[...document.querySelectorAll(selector)];

async function api(path,options={}){
  const response=await fetch(API+path,options);
  if(!response.ok){let body={};try{body=await response.json()}catch{};throw new Error(body.error?.message||`${response.status} ${response.statusText}`)}
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
  $$('nav button').forEach(x=>x.classList.remove('active'));button.classList.add('active');
  $$('.workspace').forEach(x=>x.classList.remove('active'));$('#'+button.dataset.workspace).classList.add('active');
  await refreshAll();
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

$('#discovery-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');const form=new FormData(event.target);const algorithms=form.getAll('algorithms');const alphas=list(form.get('alpha'));const variants=[];for(const algorithm of algorithms){if(algorithm==='pc'){for(const alpha of alphas)variants.push({algorithm_or_estimator:'pc',parameters:{alpha:Number(alpha)},random_seed:42})}else variants.push({algorithm_or_estimator:algorithm,parameters:{},random_seed:42})}try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'DISCOVERY',dataset_version_id:form.get('dataset_version_id'),input_graph_version_id:null,objective:form.get('objective')||null,rationale:form.get('rationale')||null,analysis_spec:{feature_columns:list(form.get('features')),constraints:{required_edges:[],forbidden_edges:[],temporal_tiers:[]},expected_graph_type:null},variants,code_version:'web-mvp-1',runtime_versions:{client:'web'}})});notice(`${variants.length}件のDiscoveryを受け付けました`);await loadExecutions()}catch(error){notice(error.message)}};
async function loadExecutions(){if(!state.project){state.executions=[];state.results=[];return}state.executions=(await api(`/projects/${state.project.project_id}/executions`)).items;state.results=[];for(const execution of state.executions){if(execution.status==='SUCCEEDED'){const values=(await api(`/executions/${execution.execution_id}/results`)).items;values.forEach(value=>value.execution=execution);state.results.push(...values)}}renderDiscovery();renderInference();renderResultOptions()}
function resultRows(operation,target){const values=state.results.filter(r=>r.execution.operation===operation);target.innerHTML=values.length?`<table><thead><tr><th></th><th>Method</th><th>Status</th><th>Summary</th></tr></thead><tbody>${values.map(r=>`<tr><td><input type="checkbox" value="${r.result_id}"></td><td>${escapeHtml(r.execution.algorithm_or_estimator)}</td><td class="${r.scientific_status}">${r.scientific_status}</td><td>${escapeHtml(JSON.stringify(r.summary))}</td></tr>`).join('')}</tbody></table>`:'完了Resultはありません';return values}
function renderDiscovery(){const values=resultRows('DISCOVERY',$('#discovery-results'));$('#graph-source').innerHTML='<option value="">選択</option>'+values.map(r=>`<option value="${r.result_id}">${r.execution.algorithm_or_estimator} / ${r.result_id.slice(0,8)}</option>`).join('')}
$('#refresh-discovery').onclick=loadExecutions;
$('#compare-discovery').onclick=()=>compareChecked('#discovery-results','#discovery-comparison',3);
async function compareChecked(container,output,minimum=2){const ids=$$(`${container} input:checked`).map(x=>x.value);if(ids.length<minimum)return notice(`${minimum}件以上選択してください`);try{$(output).textContent=JSON.stringify(await api('/comparisons/query',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({project_id:state.project.project_id,result_ids:ids})}),null,2)}catch(error){notice(error.message)}}
$('#graph-source').onchange=()=>{const result=state.results.find(r=>r.result_id===$('#graph-source').value);state.editingGraph=result?structuredClone(result.payload):null;renderGraphEditor()};
function renderGraphEditor(){const graph=state.editingGraph;$('#graph-editor').innerHTML=!graph?'Resultを選択してください':`<p>Type: <b>${graph.graph_type}</b> / Nodes: ${graph.nodes.length}</p>${graph.edges.map((edge,index)=>`<div class="edge"><span>${escapeHtml(edge.source)} ${edge.endpoint_source} — ${edge.endpoint_target} ${escapeHtml(edge.target)}</span><button type="button" onclick="removeEdge(${index})">削除</button></div>`).join('')}`}
window.removeEdge=index=>{state.editingGraph.edges.splice(index,1);renderGraphEditor()};
$('#add-edge').onclick=()=>{if(!state.editingGraph)return;const source=$('#edge-source').value.trim(),target=$('#edge-target').value.trim();if(!state.editingGraph.nodes.includes(source)||!state.editingGraph.nodes.includes(target)||source===target)return notice('既存の異なるnodeを指定してください');state.editingGraph.edges.push({source,target,endpoint_source:'TAIL',endpoint_target:'ARROW'});renderGraphEditor()};
$('#save-graph').onclick=async()=>{const source=$('#graph-source').value,rationale=$('#graph-rationale').value.trim();if(!source||!state.editingGraph)return notice('Source Resultを選択してください');if(!rationale)return notice('選定・編集理由を入力してください');try{const graph=await api(`/projects/${state.project.project_id}/graph-versions`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({source_result_id:source,parent_graph_version_id:null,name:`Selected graph ${new Date().toISOString()}`,graph_type:state.editingGraph.graph_type,graph:state.editingGraph,edit_rationale:rationale,fix_immediately:true})});await api(`/projects/${state.project.project_id}/annotations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_result_id:null,target_graph_version_id:graph.graph_version_id,statement:'Selected as the inference graph',rationale,assumptions:[],limitations:[]})});await loadGraphs();notice('FIXED Graph Versionと選定Annotationを保存しました')}catch(error){notice(error.message)}};

async function loadGraphs(){if(!state.project){state.graphs=[];return}state.graphs=(await api(`/projects/${state.project.project_id}/graph-versions`)).items;$('#fixed-graphs').innerHTML='<option value="">選択</option>'+state.graphs.filter(g=>g.status==='FIXED').map(g=>`<option value="${g.graph_version_id}">${escapeHtml(g.name)}</option>`).join('')}
$('#inference-form').oninput=event=>{const f=new FormData(event.currentTarget);$('#preflight').textContent=`Preflight: treatment=${f.get('treatment')||'—'}, outcome=${f.get('outcome')||'—'}, adjustment=[${list(f.get('adjustment')).join(', ')}], FIXED graph=${f.get('graph_version_id')?'selected':'required'}`};
$('#inference-form').onsubmit=async event=>{event.preventDefault();if(!state.project)return notice('Projectを選択してください');const f=new FormData(event.target);const estimators=f.getAll('estimators');const analysis_spec={treatment:f.get('treatment'),outcome:f.get('outcome'),estimand:f.get('estimand'),target_population:null,adjustment_set:list(f.get('adjustment')),assumptions:list(f.get('assumptions')),inference_options:{}};try{await api(`/projects/${state.project.project_id}/execution-batches`,{method:'POST',headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},body:JSON.stringify({operation:'ESTIMATION',dataset_version_id:f.get('dataset_version_id'),input_graph_version_id:f.get('graph_version_id'),objective:'Estimate binary treatment effect',rationale:'Compare estimator sensitivity',analysis_spec,variants:estimators.map(x=>({algorithm_or_estimator:x,parameters:{},random_seed:42})),code_version:'web-mvp-1',runtime_versions:{client:'web'}})});notice(`${estimators.length}件のEstimationを受け付けました`);await loadExecutions()}catch(error){notice(error.message)}};
function renderInference(){resultRows('ESTIMATION',$('#inference-results'))}
$('#refresh-inference').onclick=loadExecutions;$('#compare-inference').onclick=()=>compareChecked('#inference-results','#inference-comparison',2);

function renderResultOptions(){$('#result-select').innerHTML='<option value="">選択</option>'+state.results.map(r=>`<option value="${r.result_id}">${r.execution.operation} / ${r.execution.algorithm_or_estimator} / ${r.scientific_status}</option>`).join('')}
$('#load-result').onclick=async()=>{const id=$('#result-select').value;if(!id)return;try{const result=await api(`/results/${id}`),lineage=await api(`/results/${id}/lineage`);$('#result-detail').innerHTML=`<h2>${result.result_type}</h2><p class="status ${result.scientific_status}">${result.scientific_status}</p><pre>${escapeHtml(JSON.stringify({summary:result.summary,diagnostics:result.diagnostics,warnings:result.warnings},null,2))}</pre><button id="export-result">Export JSON</button>`;$('#export-result').onclick=async()=>{try{const manifest=await api(`/results/${id}/export`,{method:'POST'}),blob=new Blob([JSON.stringify(manifest,null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download=`ariadne-result-${id}.json`;link.click();URL.revokeObjectURL(url)}catch(error){notice(error.message)}};const artifactNodes=lineage.nodes.filter(n=>n.node_type==='Artifact');$('#artifacts').innerHTML='<h2>Artifacts</h2>'+artifactNodes.map(n=>`<a href="${API}/artifacts/${n.entity_id}/download">${escapeHtml(n.label)} download</a>`).join('<br>');$('#lineage').textContent=JSON.stringify(lineage,null,2)}catch(error){notice(error.message)}};
$('#annotation-form').onsubmit=async event=>{event.preventDefault();const result=$('#result-select').value;if(!result)return notice('Resultを選択してください');const f=new FormData(event.target);try{await api(`/projects/${state.project.project_id}/annotations`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({target_result_id:result,target_graph_version_id:null,statement:f.get('statement'),rationale:f.get('rationale')||null,assumptions:list(f.get('assumptions')),limitations:list(f.get('limitations'))})});event.target.reset();notice('Annotationを記録しました')}catch(error){notice(error.message)}};

async function refreshAll(){if(!state.project)return;await Promise.all([loadDatasets(),loadGraphs(),loadExecutions()])}
(async()=>{try{await fetch('/health/ready').then(r=>{if(!r.ok)throw Error();return r.json()});$('#health').textContent='API READY';await loadProjects()}catch{$('#health').textContent='API UNAVAILABLE'}})();
