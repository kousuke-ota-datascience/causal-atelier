"""Enumerated value sets for the product domain."""

from __future__ import annotations

from enum import Enum


class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class ArtifactType(str, Enum):
    DATASET_FILE = "DATASET_FILE"
    GRAPH_JSON = "GRAPH_JSON"
    GRAPH_IMAGE = "GRAPH_IMAGE"
    EFFECT_TABLE = "EFFECT_TABLE"
    DIAGNOSTICS_TABLE = "DIAGNOSTICS_TABLE"
    MANIFEST = "MANIFEST"
    CONFIG_SNAPSHOT = "CONFIG_SNAPSHOT"
    LOG = "LOG"


class ExecutionOperation(str, Enum):
    DISCOVERY = "DISCOVERY"
    ESTIMATION = "ESTIMATION"


class ExecutionStatus(str, Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class GraphVersionStatus(str, Enum):
    DRAFT = "DRAFT"
    FIXED = "FIXED"


class GraphType(str, Enum):
    DAG = "DAG"
    CPDAG = "CPDAG"
    PAG = "PAG"


class ResultType(str, Enum):
    DISCOVERY_GRAPH_RESULT = "DISCOVERY_GRAPH_RESULT"
    IDENTIFICATION_RESULT = "IDENTIFICATION_RESULT"
    TREATMENT_EFFECT_RESULT = "TREATMENT_EFFECT_RESULT"


class ScientificStatus(str, Enum):
    IDENTIFIED = "IDENTIFIED"
    NOT_IDENTIFIED = "NOT_IDENTIFIED"
    ESTIMATION_RELIABLE = "ESTIMATION_RELIABLE"
    ESTIMATION_UNRELIABLE = "ESTIMATION_UNRELIABLE"
    GRAPH_PRODUCED = "GRAPH_PRODUCED"
    GRAPH_EMPTY = "GRAPH_EMPTY"
    SCIENTIFIC_ERROR = "SCIENTIFIC_ERROR"
