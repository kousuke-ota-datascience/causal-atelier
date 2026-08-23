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
      summary:'保存済みTreatment Effect Resultから、処置によってOutcomeが平均的にどの程度変化したと推定されたか、その不確実性を含めて解釈・比較します。',
      purpose:'このページでは、保存済みTreatment Effect Resultを読み、ATE / ATT等の推定対象について「処置によってOutcomeがどの程度変化したと推定されたか」「その推定値をどの程度の不確実性とともに読むべきか」を確認します。推定値が利用できないResultでは、効果量を無理に解釈せず、scientific statusとwarningから理由を確認します。',
      displayScope:'Treatment / Outcome / Estimand / Estimator / Adjustment set、Estimated effect、Standard error、Confidence interval、scientific status / warning、およびResultを生成したExecution lineageを表示します。Effectの支持条件を詳しく検査するbalance / overlap / ESS / weight diagnosticsはDiagnosticsページで確認します。',
      resources:Object.freeze(['Saved treatment-effect results','ATE / ATT and available effect projections','Estimated effect and uncertainty','Scientific status and warnings','Execution lineage']),
    }),
    diagnostics:Object.freeze({
      title:'Diagnostics',
      summary:'保存済みDiagnostics Resultから、推定を支えるデータ条件・比較可能性・数値的安定性に問題がないかを確認します。',
      purpose:'このページでは、推定値そのものの大きさではなく、その推定を支える条件を診断します。具体的には「推定に十分な観測が残っているか」「Treatment / Controlを比較できるsupportがあるか」「観測共変量のbalanceに大きな偏りがないか」「propensity overlapに問題がないか」「scientific warningが残っていないか」を確認し、Effectを解釈する前に注意すべき点を把握します。Diagnosticsは未観測交絡が存在しないことや因果推論の正しさそのものを証明するものではありません。',
      displayScope:'Estimatorとcausal context、Sample loss、Treated / Control count、Covariate balance（現行Resultではunweighted / before weighting）、propensity系EstimatorでのOverlap、Scientific warnings、同一ExecutionのTreatment Effect Resultへのreferenceを表示します。ESS、weight diagnostics、weighted / post-adjustment balanceは現行backend Resultに構造化保存されていないため未表示であり、ENH-E9のbackend申し送り事項として扱います。',
      resources:Object.freeze(['Saved diagnostic results','Sample support and sample loss','Treated / Control counts','Unweighted covariate balance','Propensity overlap where applicable','Scientific warnings','Associated Treatment Effect reference']),
    }),
    sensitivity:Object.freeze({
      title:'Sensitivity',
      summary:'保存済み（saved）のTreatment Effect Resultを対象に、Refutationと感度分析を実行・確認します。',
      resources:Object.freeze(['Saved sensitivity results','Alternate assumptions','Specification dependence']),
    }),
  });

  function applyStageGuidance(presentation){
    const sections=[...document.querySelectorAll('#analysis-stage-contents .analysis-semantic-section')];
    const purposeSection=sections.find(section=>section.querySelector('h2')?.textContent==='目的');
    const scopeSection=sections.find(section=>section.querySelector('h2')?.textContent==='表示範囲');
    if(presentation.purpose&&purposeSection){
      const paragraph=purposeSection.querySelector('p');
      if(paragraph)paragraph.textContent=presentation.purpose;
    }
    if(presentation.displayScope&&scopeSection){
      const paragraph=scopeSection.querySelector('p');
      if(paragraph)paragraph.textContent=presentation.displayScope;
    }
  }

  function presentationFor(stageSlug){
    const presentation=STAGES[stageSlug];
    if(!presentation)throw new Error(`Unknown causal presentation stage: ${stageSlug}`);
    applyStageGuidance(presentation);
    return presentation;
  }

  global.CausalStagePresentation=Object.freeze({STAGES,presentationFor,applyStageGuidance});

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
    loadRuntimeScript('/causal_diagnostics_presentation.js','causal-diagnostics-presentation');
  },{once:true});
})(globalThis);
