Feature Config
==============

Feature construction settings live in the discovery and inference YAML files
under ``configs/preprocessing``.

Feature semantics are represented separately in
``configs/preprocessing/feature_semantics.yaml``. Runtime validation compares
the discovery-derived semantics with this inference catalog and fails on
mismatches.

Inference feature construction exposes registries for:

* aggregations: ``sum``, ``mean``, ``count``, ``nunique``, ``max``, ``min``
* transforms: ``identity``, ``log1p``, ``signed_log1p``, ``zscore``
* encodings: ``one_hot``, ``ordinal``, ``binary``
