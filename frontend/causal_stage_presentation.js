/* Causal navigation presentation metadata.  This is deliberately read-only UI metadata. */
(function(global){
  'use strict';

  const STAGES=Object.freeze({
    setup:Object.freeze({
      title:'Setup',
      summary:'Prepare the causal question, study design, graph, and analysis specification before drawing conclusions.',
      resources:Object.freeze(['Question and design preparation','Graph and analysis-specification preparation']),
    }),
    discovery:Object.freeze({
      title:'Discovery',
      summary:'Review DAG candidates, confounders, mediators, colliders, temporal ordering, and domain assumptions.',
      resources:Object.freeze(['DAG candidates','Causal-role review','Temporal and domain assumptions']),
    }),
    identification:Object.freeze({
      title:'Identification',
      summary:'因果効果を識別できるかを、FIXED Graph、因果質問、推定対象、仮定、および識別戦略から確認します。',
      resources:Object.freeze(['Causal estimand and question','Identification strategy and adjustment set','Exchangeability, positivity, and consistency','Strategy-specific assumptions','Identification status and warnings']),
    }),
    estimation:Object.freeze({
      title:'Estimation',
      summary:'選択したIdentification Resultを参照し、推定量、不確実性、改訂・override条件を設定して推定を実行します。',
      resources:Object.freeze(['Estimator selection','Nuisance-model configuration','Bootstrap and uncertainty configuration','Execution submission','Estimation result linkage']),
    }),
    effects:Object.freeze({
      title:'Effects',
      summary:'保存済み（saved）の処置効果、信頼区間、不確実性、および異質性を確認・比較します。',
      resources:Object.freeze(['Saved treatment-effect results','ATE, ATT, and CATE projections','Uncertainty']),
    }),
    diagnostics:Object.freeze({
      title:'Diagnostics',
      summary:'保存済み（saved）のdiagnosticsとして、balance、overlap、有効サンプルサイズ、weightsと科学的警告を確認します。',
      resources:Object.freeze(['Saved diagnostic results','Balance and overlap','Effective sample size and weights']),
    }),
    sensitivity:Object.freeze({
      title:'Sensitivity',
      summary:'保存済み（saved）のTreatment Effect Resultを対象に、Refutationと感度分析を実行・確認します。',
      resources:Object.freeze(['Saved sensitivity results','Alternate assumptions','Specification dependence']),
    }),
  });

  function presentationFor(stageSlug){
    const presentation=STAGES[stageSlug];
    if(!presentation)throw new Error(`Unknown causal presentation stage: ${stageSlug}`);
    return presentation;
  }

  global.CausalStagePresentation=Object.freeze({STAGES,presentationFor});

  // Make the Estimation action non-submitting immediately.  Until the runtime
  // handler is attached the disabled state prevents a click from silently
  // falling back to shared-form native validation.
  const estimationButton=document.querySelector('#estimation-inputs button');
  if(estimationButton){
    estimationButton.type='button';
    estimationButton.id='run-estimation';
    estimationButton.disabled=true;
  }

  function loadRuntimeScript(src,datasetKey){
    if(document.querySelector(`script[data-${datasetKey}]`))return;
    const script=document.createElement('script');
    script.src=src;
    script.dataset[datasetKey.replace(/-([a-z])/g,(_,letter)=>letter.toUpperCase())]='true';
    document.head.append(script);
  }

  // app.js executes before DOMContentLoaded and owns runtime state/APIs.
  // Attach causal action/presentation modules as soon as those declarations are available.
  global.addEventListener('DOMContentLoaded',()=>{
    loadRuntimeScript('/causal_estimation_submission.js','causal-estimation-submission');
    loadRuntimeScript('/causal_effects_presentation.js','causal-effects-presentation');
  },{once:true});
})(globalThis);
