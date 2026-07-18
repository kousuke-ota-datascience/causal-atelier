Usage
=====

Validate the integrated pipeline without running stages:

.. code-block:: bash

   uv run causal-atelier-pipeline \
     --validate-only

Inspect the resolved execution plan:

.. code-block:: bash

   uv run causal-atelier-pipeline \
     --dry-run

Run discovery and inference:

.. code-block:: bash

   uv run causal-atelier-pipeline

Run treatment-effect mode through the integrated entrypoint:

.. code-block:: bash

   uv run causal-atelier-pipeline \
     --inference-mode treatment_effect \
     --inference-treatment treated \
     --inference-outcome outcome_sales_value
