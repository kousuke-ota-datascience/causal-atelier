"""Strict in-memory G01 JSON and YAML decoding."""
from __future__ import annotations

from typing import Literal, Protocol

import yaml
from yaml.events import AliasEvent

from ariadne.causal.design.study import ValidatedStudy
from ariadne.interfaces.cli.local_causal.study import LocalStudySpec
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.serialization.jcs import parse_json, unique_object


class LocalConfigDecoder(Protocol):
    def decode(self, raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy: ...


class _UniqueSafeLoader(yaml.SafeLoader):
    def compose_node(self, parent, index):
        if self.check_event(AliasEvent):
            raise ValueError("YAML aliases are disallowed")
        if len(self.resolver_exact_paths) >= 64:
            raise ValueError("YAML nesting limit exceeded")
        return super().compose_node(parent, index)

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, yaml.MappingNode):
            raise ValueError("Expected a YAML mapping")
        pairs = []
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if type(key) is not str:
                raise ValueError("Expected a string YAML key")
            pairs.append((key, self.construct_object(value_node, deep=deep)))
        return unique_object(pairs)


class StrictLocalConfigDecoder:
    def decode(self, raw: bytes, *, declared_format: Literal["yaml", "json"]) -> ValidatedStudy:
        try:
            if declared_format == "json":
                payload = parse_json(raw)
            elif declared_format == "yaml":
                payload = yaml.load(raw.decode("utf-8"), Loader=_UniqueSafeLoader)
            else:
                raise ValueError("Unknown configuration format")
            return LocalStudySpec.from_payload(payload).to_validated_study()
        except ContractViolation:
            raise
        except (ValueError, TypeError, yaml.YAMLError, RecursionError) as error:
            raise ContractViolation("SCHEMA_INVALID", "config_decode", "Invalid local configuration") from error
