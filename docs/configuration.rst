Configuration
=============

The integrated pipeline is configured by
``configs/causal/inference/pipeline.yaml``.

Stage-specific settings live in:

* ``configs/causal/discovery.yaml``
* ``configs/preprocessing/discovery_features.yaml``
* ``configs/causal/inference/defaults.yaml``
* ``configs/preprocessing/inference_features.yaml``
* ``configs/preprocessing/feature_semantics.yaml``
* ``configs/causal/inference/designs/completejourney_household.yaml``

The integrated CLI exposes explicit prefix overrides such as
``--discovery-alpha`` and ``--inference-outcome``. These are resolved into an
``ExecutionPlan`` and then forwarded to stage runners.

Discovery-to-inference artifact transfer uses
``artifacts/pipelines/causal_discovery/manifest.yaml``. The
inference CLI accepts ``--discovery-manifest`` rather than a raw discovery
directory.
