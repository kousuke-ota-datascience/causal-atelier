"""因果探索・因果推論パイプラインの Sphinx 設定。"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

project = "causal-atelier"
author = "kousuke-ota-datascience"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_ivar = True

autodoc_typehints = "description"
autodoc_member_order = "bysource"
autodoc_class_signature = "separated"

html_theme = "sphinx_rtd_theme"
