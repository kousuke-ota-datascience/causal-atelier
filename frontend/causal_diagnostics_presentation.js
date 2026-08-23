/* Human-readable Diagnostics presentation for the causal Diagnostics stage. */
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

  function finiteNumber(value){
    if(value===null||value===undefined||value==='')return null;
    const number=Number(value);
    return Number.isFinite(number)?number:null;
  }

  function formatNumber(value,{digits=4}={}){
    const number=finiteNumber(value);
    if(number===null)return '—';
    if(Number.isInteger(number))return String(number);
    return Number(number.toPrecision(digits)).toString();
  }

  function formatPercent(numerator,denominator){
    const n=finiteNumber(numerator);
    const d=finiteNumber(denominator);
    if(n===null||d===null||d===0)return '—';
    return `${formatNumber((n/d)*100,{digits:3})}%`;
  }

  function diagnosticPayload(result){
    return result.diagnostics||result.payload||{};
  }

  function estimatorName(result){
    const raw=String(firstDefined(
      result.summary?.estimator,
      result.payload?.estimator,
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

  function statusConclusion(result){
    const status=String(result.scientific_status||result.summary?.status||'UNKNOWN');
    if(status==='PASS')return '現在記録されている診断では、重大な失敗は検出されていません。';
    if(status==='WARN')return '推定結果を解釈する前に、以下の警告と診断値を確認してください。';
    if(status==='FAIL')return '推定を支えるデータ条件に重大な問題が検出されています。';
    return `Diagnostic statusは${status}です。詳細な診断値とScientific warningsを確認してください。`;
  }

  function field(label,value){
    return `<div class="diagnostic-field"><dt>${esc(label)}</dt><dd>${esc(value??'—')}</dd></div>`;
  }

  function sampleSection(payload){
    const sample=payload.sample_size||{};
    const design=payload.design||{};
    const nInput=firstDefined(sample.n_input,design.n);
    const nComplete=firstDefined(sample.n_complete,design.n);
    const nTreated=firstDefined(sample.n_treated,design.n_treated);
    const nControl=firstDefined(sample.n_control,design.n_control);
    const sampleLoss=firstDefined(sample.sample_loss,
      finiteNumber(nInput)!==null&&finiteNumber(nComplete)!==null?Number(nInput)-Number(nComplete):null
    );
    const treatedRate=firstDefined(design.treated_rate,
      finiteNumber(nTreated)!==null&&finiteNumber(nComplete)!==null&&Number(nComplete)>0
        ?Number(nTreated)/Number(nComplete):null
    );
    if([nInput,nComplete,nTreated,nControl,sampleLoss,treatedRate].every(value=>value===undefined||value===null)){
      return `<section class="diagnostic-section"><h4>Sample support</h4><p>このResultにはSample supportの構造化診断値がありません。</p></section>`;
    }
    return `<section class="diagnostic-section">
      <h4>Sample support</h4>
      <dl class="diagnostic-fields">
        ${field('Input observations',formatNumber(nInput))}
        ${field('Complete observations',formatNumber(nComplete))}
        ${field('Sample loss',sampleLoss===undefined||sampleLoss===null?'—':`${formatNumber(sampleLoss)} (${formatPercent(sampleLoss,nInput)})`)}
        ${field('Treated',formatNumber(nTreated))}
        ${field('Control',formatNumber(nControl))}
        ${field('Treated rate',treatedRate===undefined||treatedRate===null?'—':`${formatNumber(Number(treatedRate)*100,{digits:3})}%`)}
      </dl>
    </section>`;
  }

  function balanceSection(payload){
    const rows=Array.isArray(payload.balance)?payload.balance:[];
    if(!rows.length){
      return `<section class="diagnostic-section"><h4>Covariate balance</h4><p>このResultにはCovariate balanceの構造化診断値がありません。</p></section>`;
    }
    const ranked=rows.map(row=>({row,smd:finiteNumber(row.standardized_mean_difference)}))
      .filter(item=>item.smd!==null)
      .sort((a,b)=>Math.abs(b.smd)-Math.abs(a.smd));
    const largest=ranked[0]||null;
    return `<section class="diagnostic-section">
      <h4>Covariate balance</h4>
      <p class="diagnostic-note"><b>Unweighted / before weighting.</b> 現行backendが保存しているbalanceは重み付け前の値です。</p>
      <div class="diagnostic-table-wrap"><table class="diagnostic-table">
        <thead><tr><th>Covariate</th><th>Treated mean</th><th>Control mean</th><th>SMD</th><th>Missing rate</th></tr></thead>
        <tbody>${rows.map(row=>`<tr>
          <td>${esc(row.covariate??'—')}</td>
          <td>${esc(formatNumber(row.mean_treated))}</td>
          <td>${esc(formatNumber(row.mean_control))}</td>
          <td>${esc(formatNumber(row.standardized_mean_difference))}</td>
          <td>${esc(row.missing_rate===undefined||row.missing_rate===null?'—':`${formatNumber(Number(row.missing_rate)*100,{digits:3})}%`)}</td>
        </tr>`).join('')}</tbody>
      </table></div>
      <p>${largest?`最大の|SMD|は ${esc(largest.row.covariate)} = ${esc(formatNumber(largest.smd))} です。SMDは0に近いほど、観測共変量のTreatment群とControl群の分布が近いことを示します。`:'SMDを計算できる共変量がありません。'}</p>
    </section>`;
  }

  function overlapSection(payload,prefill){
    const overlap=payload.overlap;
    const estimator=String(prefill?.algorithm_or_estimator||'').toLowerCase();
    const propensityEstimator=['ipw','aipw'].includes(estimator);
    if(!overlap){
      return `<section class="diagnostic-section"><h4>Propensity overlap</h4><p>${propensityEstimator?'このResultにはpropensity overlapの構造化診断値がありません。':'このEstimatorではpropensity overlap診断は適用対象外です。'}</p></section>`;
    }
    const parameters=prefill?.parameters||{};
    const clip=Array.isArray(parameters.propensity_clip)&&parameters.propensity_clip.length===2
      ?parameters.propensity_clip:[0.01,0.99];
    const nBelow=finiteNumber(overlap.n_ps_below_0_01);
    const nAbove=finiteNumber(overlap.n_ps_above_0_99);
    const n=finiteNumber(payload.sample_size?.n_complete)||finiteNumber(payload.design?.n);
    const outside=nBelow!==null&&nAbove!==null?nBelow+nAbove:null;
    return `<section class="diagnostic-section">
      <h4>Propensity overlap</h4>
      <dl class="diagnostic-fields">
        ${field('Configured range',`[${formatNumber(clip[0])}, ${formatNumber(clip[1])}]`)}
        ${field('Min',formatNumber(overlap.ps_min))}
        ${field('P01',formatNumber(overlap.ps_p01))}
        ${field('P05',formatNumber(overlap.ps_p05))}
        ${field('Median',formatNumber(overlap.ps_median))}
        ${field('P95',formatNumber(overlap.ps_p95))}
        ${field('P99',formatNumber(overlap.ps_p99))}
        ${field('Max',formatNumber(overlap.ps_max))}
        ${field('Below lower bound',formatNumber(nBelow))}
        ${field('Above upper bound',formatNumber(nAbove))}
      </dl>
      <p>${outside===null?'範囲外件数を判定できません。':outside===0?'設定されたpropensity範囲外の観測はありません。':`${esc(formatNumber(outside))}件（${esc(formatPercent(outside,n))}）が設定されたpropensity範囲外です。`}</p>
    </section>`;
  }

  function backendGapSection(prefill){
    const estimator=String(prefill?.algorithm_or_estimator||'').toLowerCase();
    const weighted=['ipw','aipw'].includes(estimator);
    if(!weighted)return '';
    return `<section class="diagnostic-section diagnostic-unavailable">
      <h4>Weight stability / post-adjustment balance</h4>
      <p>ESS、weight diagnostics、weighted/post-adjustment balanceは現行backend Resultに構造化保存されていないため、この画面では表示できません。ENH-E9申し送り事項としてbackend改修対象に記録しています。</p>
    </section>`;
  }

  function associatedEffect(result){
    const executionId=result.execution?.execution_id;
    if(!executionId)return null;
    return state.results.find(item=>
      item.result_type==='TREATMENT_EFFECT_RESULT'&&item.execution?.execution_id===executionId
    )||null;
  }

  function effectReferenceSection(result,prefill){
    const effect=associatedEffect(result);
    if(!effect)return `<section class="diagnostic-section"><h4>Associated Treatment Effect</h4><p>同一ExecutionのTreatment Effect Resultを復元できません。</p></section>`;
    const estimate=firstDefined(effect.summary?.estimate,effect.payload?.estimate);
    const estimand=firstDefined(effect.payload?.estimand,prefill?.analysis_spec?.causal_question?.estimand,'—');
    return `<section class="diagnostic-section">
      <h4>Associated Treatment Effect</h4>
      <dl class="diagnostic-fields">
        ${field('Estimand',estimand)}
        ${field('Estimator',estimatorName(result))}
        ${field('Status',effect.scientific_status||'—')}
        ${field('Estimated effect',formatNumber(estimate))}
      </dl>
      <p>効果量そのものの解釈・比較はEffectsページで確認してください。</p>
    </section>`;
  }

  function technicalDetails(result,prefill){
    return esc(JSON.stringify({
      result_id:result.result_id,
      execution_id:result.execution?.execution_id||null,
      summary:result.summary,
      payload:result.payload,
      diagnostics:result.diagnostics,
      warnings:result.warnings,
      analysis_spec:prefill?.analysis_spec||null,
      dataset_version_id:prefill?.dataset_version_id||result.execution?.dataset_version_id||null,
      input_graph_version_id:prefill?.input_graph_version_id||result.execution?.input_graph_version_id||null,
      input_result_id:prefill?.input_result_id||result.execution?.input_result_id||null,
    },null,2));
  }

  async function resultCard(result){
    const prefill=await executionPrefill(result);
    const payload=diagnosticPayload(result);
    const question=prefill?.analysis_spec?.causal_question||{};
    const design=prefill?.analysis_spec?.causal_design||{};
    const adjustment=Array.isArray(design.adjustment_set)&&design.adjustment_set.length
      ?design.adjustment_set.join(', '):'—';
    const status=result.scientific_status||result.summary?.status||'UNKNOWN';
    return `<article class="diagnostic-card" data-result-id="${esc(result.result_id)}">
      <div class="diagnostic-card-heading">
        <div>
          <p class="diagnostic-eyebrow">Diagnostics</p>
          <h3>${esc(estimatorName(result))}</h3>
          <p class="diagnostic-conclusion">${esc(statusConclusion(result))}</p>
        </div>
        <span class="diagnostic-status">${esc(status)}</span>
      </div>
      <section class="diagnostic-section">
        <h4>Analysis context</h4>
        <dl class="diagnostic-fields">
          ${field('Estimand',question.estimand||'—')}
          ${field('Treatment',question.treatment||'—')}
          ${field('Outcome',question.outcome||'—')}
          ${field('Estimator',estimatorName(result))}
          ${field('Adjustment set',adjustment)}
        </dl>
      </section>
      ${sampleSection(payload)}
      ${balanceSection(payload)}
      ${overlapSection(payload,prefill)}
      ${backendGapSection(prefill)}
      <section class="diagnostic-section diagnostic-warnings">
        <h4>Scientific warnings</h4>
        ${warningMarkup(result)}
      </section>
      ${effectReferenceSection(result,prefill)}
      <details class="diagnostic-technical-details">
        <summary>Technical details / Lineage</summary>
        <pre>${technicalDetails(result,prefill)}</pre>
      </details>
    </article>`;
  }

  async function render(){
    const target=document.querySelector('#diagnostics-results');
    if(!target)return;
    const generation=++renderGeneration;
    const results=state.results.filter(result=>result.result_type==='DIAGNOSTICS_RESULT');
    if(!results.length){
      target.textContent='完了Resultはありません';
      return;
    }
    target.innerHTML='<p class="diagnostic-loading">Diagnostics Resultを読み込んでいます…</p>';
    const cards=await Promise.all(results.map(resultCard));
    if(generation!==renderGeneration)return;
    target.innerHTML=`<div class="diagnostic-list">${cards.join('')}</div>`;
  }

  function installStyles(){
    if(document.querySelector('#causal-diagnostics-presentation-styles'))return;
    const style=document.createElement('style');
    style.id='causal-diagnostics-presentation-styles';
    style.textContent=`
      .diagnostic-list{display:grid;gap:18px}
      .diagnostic-card{border:1px solid #d7d9d1;background:#fff;padding:20px}
      .diagnostic-card-heading{display:flex;justify-content:space-between;align-items:start;gap:18px;border-bottom:1px solid #e1e3dd;padding-bottom:14px;margin-bottom:16px}
      .diagnostic-card-heading h3{margin:3px 0;font-size:22px}
      .diagnostic-eyebrow{margin:0;color:#66736c;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.05em}
      .diagnostic-conclusion{margin:5px 0 0;line-height:1.6}
      .diagnostic-status{font-weight:700;border:1px solid #bfc5bf;padding:5px 8px;white-space:nowrap}
      .diagnostic-section{margin:0 0 20px}
      .diagnostic-section h4{margin:0 0 9px}
      .diagnostic-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px 18px;margin:0}
      .diagnostic-field{border-bottom:1px solid #e1e3dd;padding:8px 0}
      .diagnostic-field dt{color:#66736c;font-size:12px;margin-bottom:4px}
      .diagnostic-field dd{margin:0;font-weight:600;overflow-wrap:anywhere}
      .diagnostic-note{background:#f6f7f3;padding:10px 12px}
      .diagnostic-table-wrap{overflow:auto}
      .diagnostic-table{width:100%;border-collapse:collapse}
      .diagnostic-table th,.diagnostic-table td{text-align:left;border-bottom:1px solid #e1e3dd;padding:8px;white-space:nowrap}
      .diagnostic-unavailable{border-left:4px solid #88743a;background:#faf8ef;padding:12px 14px}
      .diagnostic-warnings{border-left:4px solid #9d513f;background:#fbf5f2;padding:12px 14px}
      .diagnostic-warnings ul{margin:6px 0;padding-left:20px}
      .diagnostic-technical-details pre{max-height:300px;overflow:auto}
      @media(max-width:800px){.diagnostic-fields{grid-template-columns:1fr}.diagnostic-card-heading{display:grid}}
    `;
    document.head.append(style);
  }

  function install(){
    installStyles();
    if(typeof renderInference!=='function')throw new Error('Causal Diagnostics presentation requires app.js renderInference');
    const originalRenderInference=renderInference;
    renderInference=function(){
      const result=originalRenderInference();
      void render();
      return result;
    };
    void render();
  }

  global.CausalDiagnosticsPresentation=Object.freeze({render,install});
  install();
})(globalThis);
