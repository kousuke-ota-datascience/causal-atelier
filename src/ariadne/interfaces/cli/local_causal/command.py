"""Explicit G01 DISCOVER CLI and the Local composition root."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from dataclasses import dataclass
from importlib.metadata import version
from pathlib import Path
from time import monotonic

from ariadne.capabilities.causal.local_execution import LocalCausalUseCase, LocalRunContext
from ariadne.capabilities.causal.method_registry import (
    LOCAL_FCI, LocalMethodCapabilityAdapter, MethodCapabilityRegistry,
)
from ariadne.capabilities.causal.ports.manifest_factory import ManifestRuntimeFacts
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.content_io import LocalContentReferenceAdapter
from ariadne.interfaces.cli.local_causal.manifest_factory import LocalManifestFactoryAdapter
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.interfaces.cli.local_causal.privacy import LocalPrivacyPolicy
from ariadne.interfaces.cli.local_causal.publication import LocalPublicationAdapter
from ariadne.interfaces.cli.local_causal.study import safe_run_id
from ariadne.scientific.causal_methods.discovery import FciBackend, FciDiscoveryAdapter
from ariadne.scientific.causal_methods.fci_eligibility import ScientificEligibilityPolicy
from ariadne.scientific.ports.causal import LocalDiscoveryDispatcher
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.local_fs import LocalPrincipal, TrustedLocalRoot, private_directory


class _Parser(argparse.ArgumentParser):
    def error(self, message):
        raise ContractViolation("SCHEMA_INVALID", "configuration", "Invalid Local CLI arguments")


class _Reader:
    """Distinguish a new run from a present but unverifiable run."""

    def verify(self, *, root, run_id):
        if not safe_run_id(run_id):
            raise ContractViolation("SCHEMA_INVALID", "publication", "Invalid Local run identifier")
        identity = root.verify()
        try:
            with private_directory(root.fileno(), "runs", identity) as parent:
                os.stat(run_id, dir_fd=parent, follow_symlinks=False)
        except FileNotFoundError as error:
            raise ContractViolation("RUN_NOT_FOUND", "publication", "No prior run") from error
        except (OSError, ContractViolation) as error:
            raise ContractViolation("NOT_COMMITTED", "publication", "Existing run could not be verified") from error
        return LocalManifestReader().verify(root=root, run_id=run_id)


@dataclass(frozen=True)
class _Runtime:
    repository: Path

    def resources_available(self) -> bool:
        return os.sysconf("SC_AVPHYS_PAGES") > 0

    def snapshot(self, capability):
        def git(*args):
            return subprocess.run(["git", "-C", str(self.repository), *args], check=True, text=True,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.strip()

        try:
            repo = git("rev-parse", "--show-toplevel")
            lock = (Path(repo) / "uv.lock").read_bytes()
            return ManifestRuntimeFacts(
                git("rev-parse", "HEAD"), bool(git("status", "--porcelain")), platform.python_version(),
                platform.platform(), hashlib.sha256(lock).hexdigest(),
                {name: version(name) for name in ("causal-learn", "numpy", "scipy", "pyarrow")},
                {"fci_signature_sha256": capability.api_signature_hash},
            )
        except (OSError, subprocess.SubprocessError, ValueError) as error:
            raise ContractViolation("RUNTIME_EVIDENCE_UNAVAILABLE", "publication",
                                    "Runtime evidence could not be measured") from error


class _Clock:
    monotonic = staticmethod(monotonic)


def _compose() -> LocalCausalUseCase:
    backend = FciBackend()
    runtime = _Runtime(Path(__file__).resolve().parent)
    policy = ScientificEligibilityPolicy(runtime.resources_available)
    registry = MethodCapabilityRegistry(
        {LOCAL_FCI.method_id: LOCAL_FCI},
        {LOCAL_FCI.method_id: lambda: FciDiscoveryAdapter(
            descriptor=LOCAL_FCI, backend_factory=FciBackend, policy=policy,
        )},
        backend.probe(), (),
    )
    privacy = LocalPrivacyPolicy()
    return LocalCausalUseCase(
        refs=LocalContentReferenceAdapter(), capabilities=LocalMethodCapabilityAdapter(registry),
        discovery=LocalDiscoveryDispatcher(registry), identifier=NotImplemented, estimators=NotImplemented,
        diagnostics=NotImplemented, publisher=LocalPublicationAdapter(privacy), reader=_Reader(), privacy=privacy,
        runtime=runtime, clock=_Clock(), manifest_factory=LocalManifestFactoryAdapter(),
    )


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    use_json = "--json" in args
    parser = _Parser(prog="ariadne-causal-local", allow_abbrev=False)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    try:
        options = parser.parse_args(args)
        suffix = options.config.suffix.lower()
        if suffix not in (".json", ".yaml", ".yml"):
            raise ContractViolation("SCHEMA_INVALID", "configuration", "Local Study needs JSON or YAML extension")
        try:
            raw = options.config.read_bytes()
        except OSError as error:
            raise ContractViolation("INPUT_SECURITY", "input", "Could not open Study input") from error
        try:
            spec = StrictLocalConfigDecoder().decode(raw, declared_format="json" if suffix == ".json" else "yaml")
        except ContractViolation as error:
            if error.reason.code == "PRIVACY_POLICY_CONFLICT":
                raise ContractViolation("PRIVACY_DENIED", "privacy", "Local run requires aggregate-only privacy") from error
            raise
        path = options.output_root.absolute()
        with TrustedLocalRoot.open(path, allowed_directory=path) as root:
            context = LocalRunContext(root, LocalPrincipal.current())
            use_case = _compose()
            if options.check_only:
                report = use_case.preflight(spec, context)
                response = {"run_id": spec.to_payload()["run_id"], "technical_status": "PREFLIGHT_OK",
                            "science_acceptance": report.science_acceptance, "manifest_relative_path": None}
            else:
                result = use_case.run(spec, context)
                response = {"run_id": result.verified.run_id, "technical_status": result.technical_status,
                            "science_acceptance": result.science_acceptance,
                            "manifest_relative_path": f"runs/{result.verified.run_id}/manifest.json"}
        print(json.dumps(response) if use_json else response["technical_status"])
        return 0
    except ContractViolation as error:
        reason = error.reason
        if reason.phase in ("privacy", "input", "content_ref"):
            exit_code = 3
        elif reason.phase in ("engine", "graph"):
            exit_code = 4
        elif reason.phase == "publication":
            exit_code = 5
        else:
            exit_code = 2
        phase = {2: "configuration", 3: "privacy" if reason.phase == "privacy" else "input",
                 4: "engine", 5: "publication"}[exit_code]
        if use_json:
            print(json.dumps({"technical_status": "FAILED", "science_acceptance": "NOT_EVALUATED",
                              "reason_code": reason.code, "phase": phase, "manifest_relative_path": None}))
        print(f"{reason.code} phase={phase}", file=sys.stderr)
        return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
