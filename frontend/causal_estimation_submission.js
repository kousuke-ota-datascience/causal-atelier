/* Estimation submission owns its action independently from Identification form validation. */
(function(){
  'use strict';

  function selectedIdentificationResult(){
    const resultId=$('#identification-results').value;
    return state.results.find(result=>
      result.result_type==='IDENTIFICATION_RESULT'&&result.result_id===resultId
    )||null;
  }

  function estimationSpecFromPrefill(prefill,override){
    const spec=structuredClone(prefill.analysis_spec);
    spec.operation_spec={inference_options:{}};
    spec.validation_override=override;
    delete spec.revision_context;
    delete spec.scientific_warnings;
    return spec;
  }

  async function runEstimation(){
    if(!state.project)return notice('Projectを選択してください');
    const form=$('#inference-form');
    const values=new FormData(form);
    const upstream=selectedIdentificationResult();
    const estimators=values.getAll('estimators').map(String);
    const reason=String(values.get('override_reason')||'').trim();
    const override=reason?{reason,actor:'web-user',warning_codes:['ELIGIBILITY_WARN']}:null;
    const baseExecutionId=String(values.get('base_execution_id')||'')||null;
    const changeReason=String(values.get('change_reason')||'').trim()||null;

    if(!upstream)return notice('Identification Resultを選択してください');
    if(!estimators.length)return notice('Estimatorを1件以上選択してください');
    if(!upstream.execution?.execution_id)return notice('Identification ResultのExecution lineageを復元できません');

    try{
      const prefill=await api(`/executions/${upstream.execution.execution_id}/prefill`);
      if(prefill.operation!=='IDENTIFICATION'||!prefill.dataset_version_id||!prefill.input_graph_version_id){
        throw new Error('Identification Resultの入力Lineageを復元できません');
      }
      const response=await api(`/projects/${state.project.project_id}/execution-batches`,{
        method:'POST',
        headers:{'Content-Type':'application/json','Idempotency-Key':idempotencyKey()},
        body:JSON.stringify({
          operation:'ESTIMATION',
          dataset_version_id:prefill.dataset_version_id,
          input_graph_version_id:prefill.input_graph_version_id,
          input_result_id:upstream.result_id,
          objective:'Estimate binary treatment effect',
          rationale:'Compare estimator sensitivity',
          analysis_spec:estimationSpecFromPrefill(prefill,override),
          variants:estimators.map(estimator=>({algorithm_or_estimator:estimator,parameters:{},random_seed:42})),
          code_version:'web-enh-e9',
          runtime_versions:{client:'web'},
          base_execution_id:baseExecutionId,
          change_reason:changeReason,
        }),
      });
      const warnings=response.executions.flatMap(execution=>execution.scientific_warnings||[]);
      $('#scientific-warnings').textContent=warnings.map(item=>`${item.warning_code}: ${item.message}`).join('\n');
      notice(warnings.length?`${estimators.length}件を警告付きで受け付けました`:`${estimators.length}件のEstimationを受け付けました`);
      await loadExecutions();
      saveWorkspaceState({unsaved_draft:false}).catch(error=>notice(error.message));
    }catch(error){
      notice(error.message);
    }
  }

  const form=$('#inference-form');
  const button=$('#estimation-inputs button');
  if(!form||!button)throw new Error('Estimation controls are unavailable');

  // Identification and Estimation share visual context, but no longer share submit ownership.
  // Explicit button ownership bypasses native validation for hidden Identification fields.
  button.type='button';
  button.id='run-estimation';
  form.onsubmit=event=>event.preventDefault();
  button.onclick=runEstimation;
})();
