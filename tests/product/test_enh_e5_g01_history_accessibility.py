from pathlib import Path


def test_e5_navigation_has_keyboard_focus_and_non_color_accessibility_evidence() -> None:
    repository = Path(__file__).parents[2]
    html = (repository / 'frontend/index.html').read_text(encoding='utf-8')
    javascript = (repository / 'frontend/app.js').read_text(encoding='utf-8')
    css = (repository / 'frontend/styles.css').read_text(encoding='utf-8')
    assert 'id="main-content" tabindex="-1"' in html
    assert 'heading.focus()' in javascript
    assert 'Analysis family:' in javascript
    assert 'Analysis stage:' in javascript
    assert 'unavailable:' in javascript
    assert ':focus-visible{outline:3px solid #ad6d22' in css
