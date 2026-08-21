/* Presentation-only metadata for canonical analysis stages. */
(function(global){
  'use strict';

  const FAMILY_PURPOSES=Object.freeze({
    exploratory:'データの特徴を確認し、次の分析で検討する論点を整理します。',
    causal:'因果に関する問い、設計、推定、検証を段階的に整理します。',
    predictive:'予測モデルの準備、学習、評価、活用を整理します。',
  });
  const CAUSAL_SIDEBAR_GROUPS=Object.freeze({
    setup:'設計と構造', discovery:'設計と構造',
    identification:'同定と推定', estimation:'同定と推定',
    effects:'結果と検証', diagnostics:'結果と検証', sensitivity:'結果と検証',
  });

  function metadataFor(context){
    return Object.freeze({
      purpose:FAMILY_PURPOSES[context.familySlug]||'選択中の分析Stageを確認します。',
      sidebarGroup:context.familySlug==='causal'
        ? (CAUSAL_SIDEBAR_GROUPS[context.stageSlug]||'Causal workflow')
        : null,
    });
  }

  function groupedStages(family){
    const groups=[];
    for(const stage of family.stages){
      const group=metadataFor({familySlug:family.slug,stageSlug:stage.slug}).sidebarGroup;
      const previous=groups.at(-1);
      if(!group){groups.push(Object.freeze({label:null,stages:Object.freeze([stage])}));continue}
      if(previous?.label===group)previous.stages.push(stage);
      else groups.push({label:group,stages:[stage]});
    }
    return groups.map(group=>Object.freeze({label:group.label,stages:Object.freeze(group.stages)}));
  }

  global.AnalysisStagePresentation=Object.freeze({metadataFor,groupedStages});
})(globalThis);
