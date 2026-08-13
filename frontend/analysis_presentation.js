/* Presentation binding for canonical analysis navigation contexts. */
(function(global){
  'use strict';

  const CAUSAL_WORKSPACES=Object.freeze({
    setup:'discovery', discovery:'discovery', identification:'inference', estimation:'inference',
    effects:'inference', diagnostics:'inference', sensitivity:'inference',
  });

  function resolve(context){
    if(context.familySlug==='exploratory')return Object.freeze({workspace:'explore'});
    if(context.familySlug==='predictive')return Object.freeze({workspace:'predictive'});
    if(context.familySlug==='causal'){
      const workspace=CAUSAL_WORKSPACES[context.stageSlug];
      if(workspace)return Object.freeze({workspace});
    }
    throw new Error(`Missing analysis presentation binding for ${context.familySlug}/${context.stageSlug}`);
  }

  global.AnalysisPresentation=Object.freeze({resolve});
})(globalThis);
