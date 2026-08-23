/* Human-readable Treatment Effect presentation for the causal Effects stage. */
(function(global){
  'use strict';

  const prefillCache=new Map();
  let renderGeneration=0;

  function esc(value){
    return String(value??'').replace(/[&<>"']/g,char=>({
      '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;',
    })[char]);
  }

  function firstDefined(...values){
    return values.find(value=>value!==undefined&&value!==null);
  }

  function effectValue(result,key){
    return firstDefined(result.summary?.[key],result.payload?.[key]);
  }

  function finiteNumber(value){
    if(value===null||value===undefined||value==='')return null;
    const number=Number(value);
    return Number.isFinite(number)?number:null;
  }

  function formatNumber(value,{signed=false}={}){
    const number=finiteNumber(value);
    if(number===null)return '—';
    const formatted=Number.isInteger(number)?String(number):Number(number.toPrecision(6)).toString();
    return signed&&number>0?`+${formatted}`:formatted;
  }

  function confidenceInterval(result){
    const value=effectValue(result,'confidence_interval');
    if(Array.isArray(value)&&value.length>=2)return [finiteNumber(value[0]),finiteNumber(value[1])];
    if(value&&typeof value==='object'){
      const lower=firstDefined(value.lower,value.low,value.min,value.left,value['2.5%']);
      const upper=firstDefined(value.upper,value.high,value.max,value.right,value['97.5%']);
      return [finiteNumber(lower),finiteNumber(upper)];
    }
    const lower=firstDefined(effectValue(result,'ci_lower'),effectValue(result,'confidence_interval_lower'));
    const upper=firstDefined(effectValue(result,'ci_upper'),effectValue(result,'confidence_interval_upper'));
    return [finiteNumber(lower),finiteNumber(upper)];
  }

  function formatConfidenceInterval(result){
    const [lower,upper]=confidenceInterval(result);
    if(lower===null||upper===null)return '—';
    return `[${formatNumber(lower)}, ${formatNumber(upper)}]`;
  }

  function estimatorName(result){
    const raw=String(firstDefined(
      effectValue(result,'estimator'),
      result.execution?.algorithm_or_estimator,
      '—',
    ));
    const labels={ols:'OLS',ipw:'IPW',aipw:'AIPW',difference_in_means:'Difference in means'};
    return labels[raw.toLowerCase()]||raw;
  }

  function normalizedWarnings(result){
    const candidates=[result.warnings,result.payload?.warnings,result.summary?.warnings]
      .filter(Array.isArray)
      .flat();
    const seen=new Set();
    return candidates.filter(item=>{
      const key=typeof item==='string'?item:JSON.stringify(item);
      if(seen.has(key))return false;
      seen.add(key);
      return true;
    });
  }

  function warningMarkup(result){
    const warnings=normalizedWarnings(result);
    if(!warnings.length)return '<p>なし</p>';
    return `<ul>${warnings.map(item=>{
      if(typeof item==='string')return `<li>${esc(item)}</li>`;
      const code=item.warning_code||item.code||'WARNING';
      const message=item.message||item.rationale||JSON.stringify(item);
      return `<li><b>${esc(code)}</b>: ${esc(message)}</li>`;
    }).join('')}</ul>`;
  }

  async function executionPrefill(result){
    const executionId=result.execution?.execution_id;
    if(!executionId)return null;
    if(prefillCache.has(executionId))return prefillCache.get(executionId);
    const pending=api(`/executions/${executionId}/prefill`).catch(()=>null);
    prefillCache.set(executionId,pending);
    return pending;
  }

  function interpretation(result,prefill){
    const estimate=finiteNumber(effectValue(result,'estimate'));
    const status=String(result.scientific_status||'UNKNOWN');
    const question=prefill?.analysis_spec?.causal_question||{};
    const treatment=question.treatment||'Treatment';
    const outcome=question.outcome||'Outcome';
    const comparator=question.comparator||'比較対象';

    if(estimate===null){
      return `推定値を利用できません。Statusが${status}の理由とScientific warningsを確認してください。`;
    }
    if(status!=='VALID'){
      return `推定値は${formatNumber(estimate,{signed:true})}ですが、Statusが${status}のため、因果効果として解釈する前にScientific warningsの確認が必要です。`;
    }
    if(estimate>0){
      return `${treatment}のTreatment群では、比較対象（${comparator}）と比べて、${outcome}が平均${formatNumber(estimate)}高いと推定されました。`;
    }
    if(estimate<0){
      return `${treatment}のTreatment群では、比較対象（${comparator}）と比べて、${outcome}が平均${formatNumber(Math.abs(estimate))}低いと推定されました。`;
    }
    return `${treatment}のTreatment群と比較対象（${comparator}）の間で、${outcome}の平均差は0と推定されました。`;
  }

  function availability(result){
    const estimate=finiteNumber(effectValue(result,'estimate'));
    if(estimate===null)return '効果量を解釈できません';
    return result.scientific_status==='VALID'?'解釈可能':'要レビュー';
  }

  function field(label,value){
    return `<div class="effect-field"><dt>${esc(label)}</dt><dd>${esc(value??'—')}</dd></div>`;
  }

  function technicalDetails(result,prefill){
    return esc(JSON.stringify({
      result_id:result.result_id,
      execution_id:result.execution?.execution_id||null,
      summary:result.summary,
      payload:result.payload,
      warnings:result.warnings,
      analysis_spec:prefill?.analysis_spec||null,
      dataset_version_id:prefill?.dataset_version_id||result.execution?.dataset_version_id||null,
      input_graph_version_id:prefill?.input_graph_version_id||result.execution?.input_graph_version_id||null,
      input_result_id:prefill?.input_result_id||result.execution?.input_result_id||null,
    },null,2));
  }

  async function resultCard(result){
    const prefill=await executionPrefill(result);
    const spec=prefill?.analysis_spec||{};
    const question=spec.causal_question||{};
    const design=spec.causal_design||{};
    const adjustment=Array.isArray(design.adjustment_set)&&design.adjustment_set.length
      ?design.adjustment_set.join(', ')
      :'—';
    const status=result.scientific_status||'UNKNOWN';
    const estimate=formatNumber(effectValue(result,'estimate'),{signed:true});
    const standardError=formatNumber(effectValue(result,'standard_error'));

    return `<article class="treatment-effect-card" data-result-id="${esc(result.result_id)}">
      <div class="effect-card-heading">
        <div>
          <p class="effect-eyebrow">Treatment Effect</p>
          <h3>${esc(estimatorName(result))}</h3>
          <p class="effect-availability">${esc(availability(result))}</p>
        </div>
        <label class="effect-compare"><input type="checkbox" value="${esc(result.result_id)}"> 比較対象に選択</label>
      </div>
      <dl class="effect-fields">
        ${field('Status',status)}
        ${field('Estimand',question.estimand||'—')}
        ${field('Treatment',question.treatment||'—')}
        ${field('Outcome',question.outcome||'—')}
        ${field('Estimator',estimatorName(result))}
        ${field('Estimated effect',estimate)}
        ${field('Standard error',standardError)}
        ${field('95% confidence interval',formatConfidenceInterval(result))}
        ${field('Adjustment set',adjustment)}
      </dl>
      <section class="effect-interpretation">
        <h4>Interpretation</h4>
        <p>${esc(interpretation(result,prefill))}</p>
      </section>
      <section class="effect-warnings">
        <h4>Scientific warnings</h4>
        ${warningMarkup(result)}
      </section>
      <details class="effect-technical-details">
        <summary>Technical details / Lineage</summary>
        <pre>${technicalDetails(result,prefill)}</pre>
      </details>
    </article>`;
  }

  async function render(){
    const target=document.querySelector('#treatment-effect-results');
    if(!target)return;
    const generation=++renderGeneration;
    const results=state.results.filter(result=>result.result_type==='TREATMENT_EFFECT_RESULT');
    if(!results.length){
      target.textContent='完了Resultはありません';
      return;
    }
    target.innerHTML='<p class="effect-loading">Treatment Effect Resultを読み込んでいます…</p>';
    const cards=await Promise.all(results.map(resultCard));
    if(generation!==renderGeneration)return;
    target.innerHTML=`<div class="treatment-effect-list">${cards.join('')}</div>`;
  }

  function installStyles(){
    if(document.querySelector('#causal-effects-presentation-styles'))return;
    const style=document.createElement('style');
    style.id='causal-effects-presentation-styles';
    style.textContent=`
      .treatment-effect-list{display:grid;gap:18px}
      .treatment-effect-card{border:1px solid #d7d9d1;background:#fff;padding:20px}
      .effect-card-heading{display:flex;justify-content:space-between;align-items:start;gap:18px;border-bottom:1px solid #e1e3dd;padding-bottom:14px;margin-bottom:16px}
      .effect-card-heading h3{margin:3px 0;font-size:22px}
      .effect-eyebrow{margin:0;color:#66736c;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
      .effect-availability{margin:4px 0 0;font-weight:700}
      .effect-compare{display:flex;grid-template-columns:auto 1fr;align-items:center;gap:7px}
      .effect-compare input{width:auto;min-height:0}
      .effect-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 18px;margin:0 0 18px}
      .effect-field{border-bottom:1px solid #e1e3dd;padding:8px 0}
      .effect-field dt{color:#66736c;font-size:12px;margin-bottom:4px}
      .effect-field dd{margin:0;font-weight:600;overflow-wrap:anywhere}
      .effect-interpretation{border-left:4px solid #2a7254;background:#f6f7f3;padding:14px 16px;margin:0 0 14px}
      .effect-interpretation h4,.effect-warnings h4{margin:0 0 7px}
      .effect-interpretation p{margin:0;line-height:1.6}
      .effect-warnings{margin:0 0 14px}
      .effect-warnings ul{margin:6px 0;padding-left:20px}
      .effect-technical-details pre{max-height:300px;overflow:auto}
      @media(max-width:800px){.effect-fields{grid-template-columns:1fr}.effect-card-heading{display:grid}}
    `;
    document.head.append(style);
  }

  function install(){
    installStyles();
    if(typeof renderInference!=='function')throw new Error('Causal Effects presentation requires app.js renderInference');
    const originalRenderInference=renderInference;
    renderInference=function(){
      const result=originalRenderInference();
      void render();
      return result;
    };
    void render();
  }

  global.CausalEffectsPresentation=Object.freeze({render,install});
  install();
})(globalThis);
