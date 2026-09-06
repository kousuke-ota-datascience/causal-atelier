"""ENH-E9 G03 P01 contract checks for Identification input ergonomics."""

import json
import subprocess
from pathlib import Path


def _repository_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "pyproject.toml").is_file():
            return parent
    raise RuntimeError("repository root not found")


REPOSITORY = _repository_root()


def _identification_surface() -> str:
    html = (REPOSITORY / "frontend" / "index.html").read_text(encoding="utf-8")
    start = html.index('<form id="inference-form"')
    return html[start : html.index('<div data-causal-stage-surface="estimation">', start)]


def _reconcile_treatment(dataset: dict[str, object] | None, current: str, announce: bool) -> dict[str, object]:
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    start = app.index("function selectedInferenceDataset()")
    end = app.index("\n$('#fixed-graphs').onchange", start)
    functions = app[start:end]
    datasets = [] if dataset is None else [dataset]
    selected_id = "dataset-a" if dataset is not None else ""
    script = f"""
const state={{datasets:{json.dumps(datasets, ensure_ascii=False)}}};
const field={{value:{json.dumps(current)},innerHTML:'',disabled:false}};
const form={{elements:{{dataset_version_id:{{value:{json.dumps(selected_id)}}}}}}};
const notices=[];
const $=selector=>selector==='#inference-form'?form:field;
const escapeHtml=value=>String(value).replace(/[&<>\"']/g,character=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}}[character]));
const notice=message=>notices.push(message);
{functions}
reconcileInferenceTreatment({{announce:{str(announce).lower()}}});
console.log(JSON.stringify({{value:field.value,html:field.innerHTML,disabled:field.disabled,notices}}));
"""
    result = subprocess.run(["node", "-e", script], check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def test_population_and_comparator_explain_their_causal_question_meaning() -> None:
    surface = _identification_surface()

    assert 'name="population"' in surface
    assert "分析対象集団・対象範囲" in surface
    assert 'name="comparator"' in surface
    assert "反実仮想の基準条件" in surface


def test_treatment_selector_is_schema_backed_and_clears_stale_values() -> None:
    html = _identification_surface()
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")

    assert '<select name="treatment" id="inference-treatment" required disabled>' in html
    assert "reconcileInferenceTreatment({announce:true})" in app

    dataset_a = {"dataset_version_id": "dataset-a", "schema": {"coupon": "integer", "sales": "number"}}
    retained = _reconcile_treatment(dataset_a, "coupon", announce=False)
    assert retained["value"] == "coupon"
    assert 'value="coupon"' in retained["html"]
    assert 'value="sales"' in retained["html"]
    assert 'value="invented"' not in retained["html"]

    unavailable = _reconcile_treatment(None, "coupon", announce=False)
    assert unavailable == {
        "value": "",
        "html": '<option value="">Dataset/schemaを選択してください</option>',
        "disabled": True,
        "notices": [],
    }

    dataset_b = {"dataset_version_id": "dataset-a", "schema": {"sales": "number"}}
    invalidated = _reconcile_treatment(dataset_b, "coupon", announce=True)
    assert invalidated["value"] == ""
    assert 'value="coupon"' not in invalidated["html"]
    assert invalidated["notices"] == ["Dataset Version変更によりschemaに存在しないTreatmentを解除しました。"]


def test_outcome_remains_read_only_graph_projection_and_estimation_lineage_is_unchanged() -> None:
    html = _identification_surface()
    app = (REPOSITORY / "frontend" / "app.js").read_text(encoding="utf-8")
    estimation = (REPOSITORY / "frontend" / "causal_estimation_submission.js").read_text(
        encoding="utf-8"
    )

    assert '<output id="inference-outcome" class="readonly-field">' in html
    assert 'name="outcome"' not in html
    assert "const outcome=selectedInferenceGraph()?.designated_outcome_node;" in app
    assert "causal_question:{population:f.get('population'),treatment:f.get('treatment'),comparator:f.get('comparator'),outcome," in app
    assert "dataset_version_id:prefill.dataset_version_id" in estimation
    assert "input_graph_version_id:prefill.input_graph_version_id" in estimation
    assert "input_result_id:upstream.result_id" in estimation
