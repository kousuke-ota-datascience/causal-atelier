Reproducibility
===============

Each integrated run builds an ``ExecutionPlan`` with resolved config paths,
child stage arguments, output paths, and validation checks.

Discovery and inference stages write ``manifest.yaml`` files containing
config hashes, output directories, artifact paths, run ID, and random seed.

Use ``--dry-run`` to inspect the plan and ``--validate-only`` to check configs,
feature semantics, causal design, adjustment sets, and artifact contracts
without running stage code.
