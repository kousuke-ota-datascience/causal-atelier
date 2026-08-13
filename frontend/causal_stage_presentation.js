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
      summary:'Assess the estimand, identification strategy, adjustment set, assumptions, and identification status separately from estimator tuning.',
      resources:Object.freeze(['Causal estimand and question','Identification strategy and adjustment set','Exchangeability, positivity, and consistency','Strategy-specific assumptions','Identification status and warnings']),
    }),
    estimation:Object.freeze({
      title:'Estimation',
      summary:'Select and configure an estimator, uncertainty procedure, and execution using an identified causal question.',
      resources:Object.freeze(['Estimator selection','Nuisance-model configuration','Bootstrap and uncertainty configuration','Execution submission','Estimation result linkage']),
    }),
    effects:Object.freeze({
      title:'Effects',
      summary:'Read saved treatment-effect results, uncertainty, and heterogeneity projections.',
      resources:Object.freeze(['Saved treatment-effect results','ATE, ATT, and CATE projections','Uncertainty']),
    }),
    diagnostics:Object.freeze({
      title:'Diagnostics',
      summary:'Read saved diagnostic results such as balance, overlap, effective sample size, and weights.',
      resources:Object.freeze(['Saved diagnostic results','Balance and overlap','Effective sample size and weights']),
    }),
    sensitivity:Object.freeze({
      title:'Sensitivity',
      summary:'Review saved sensitivity results for alternate assumptions and specification dependence.',
      resources:Object.freeze(['Saved sensitivity results','Alternate assumptions','Specification dependence']),
    }),
  });

  function presentationFor(stageSlug){
    const presentation=STAGES[stageSlug];
    if(!presentation)throw new Error(`Unknown causal presentation stage: ${stageSlug}`);
    return presentation;
  }

  global.CausalStagePresentation=Object.freeze({STAGES,presentationFor});
})(globalThis);
