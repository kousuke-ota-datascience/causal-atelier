Usage
=====

Validate the integrated pipeline without running stages:

.. code-block:: bash

   uv run ariadne-pipeline \
     --validate-only

Inspect the resolved execution plan:

.. code-block:: bash

   uv run ariadne-pipeline \
     --dry-run

Run discovery and inference:

.. code-block:: bash

   uv run ariadne-pipeline

Run treatment-effect mode through the integrated entrypoint:

.. code-block:: bash

   uv run ariadne-pipeline \
     --inference-mode treatment_effect \
     --inference-treatment treated \
     --inference-outcome outcome_sales_value
