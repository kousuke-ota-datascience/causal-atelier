"""Numeric JCS regression and physical Local bundle readback for S09-JCS-01."""

from decimal import Clamped, Context, Inexact, ROUND_DOWN, ROUND_UP, Rounded, localcontext
from hashlib import sha256
import json
from pathlib import Path
import struct
from tempfile import TemporaryDirectory

import pytest

from ariadne.interfaces.cli.local_causal import command
from ariadne.interfaces.cli.local_causal.config_decoder import StrictLocalConfigDecoder
from ariadne.interfaces.cli.local_causal.manifest_reader import LocalManifestReader
from ariadne.shared.content_ref import ContractViolation
from ariadne.shared.local_fs import TrustedLocalRoot
from ariadne.shared.serialization import jcs
from tests.enhancement.enh_e11.g01.contract.test_local_codec import VECTORS, study_payload
from tests.enhancement.enh_e11.g01.integration.test_local_cli import REPO, RUN, _inputs


ALPHA = 0.123456789
EXPECTED_ALPHA = b'{"alpha":0.123456789}'


def _restricted_context():
    context = Context(prec=1, rounding=ROUND_UP, Emin=-2, Emax=2, clamp=1)
    context.traps[Inexact] = True
    context.traps[Rounded] = True
    context.flags[Clamped] = True
    return context


@pytest.mark.parametrize("context", [
    Context(prec=6),
    _restricted_context(),
    Context(prec=28),
    Context(prec=80, rounding=ROUND_DOWN),
], ids=["precision-6", "restricted", "ordinary", "high-precision"])
def test_numeric_bytes_digest_and_parse_do_not_depend_on_decimal_context(context):
    # IEEE-754 inputs and independent outputs from RFC 8785 Appendix B.
    vectors = {
        "0000000000000000": b"0",
        "8000000000000000": b"0",
        "0000000000000001": b"5e-324",
        "8000000000000001": b"-5e-324",
        "7fefffffffffffff": b"1.7976931348623157e+308",
        "ffefffffffffffff": b"-1.7976931348623157e+308",
        "4430000000000000": b"295147905179352830000",
        "44b52d02c7e14af5": b"9.999999999999997e+22",
        "44b52d02c7e14af6": b"1e+23",
        "44b52d02c7e14af7": b"1.0000000000000001e+23",
        "444b1ae4d6e2ef4f": b"999999999999999900000",
        "444b1ae4d6e2ef50": b"1e+21",
        "3eb0c6f7a0b5ed8c": b"9.999999999999997e-7",
        "3eb0c6f7a0b5ed8d": b"0.000001",
        "41b3de4355555554": b"333333333.33333325",
        "43143ff3c1cb0959": b"1424953923781206.2",
    }
    with localcontext(context) as active:
        before = active.copy()
        assert jcs.canonical_bytes({"alpha": ALPHA}) == EXPECTED_ALPHA
        assert jcs.digest({"alpha": ALPHA}) == sha256(EXPECTED_ALPHA).hexdigest()
        assert jcs.parse_json(EXPECTED_ALPHA) == {"alpha": ALPHA}
        for bits, expected in vectors.items():
            number, = struct.unpack(">d", bytes.fromhex(bits))
            assert jcs.canonical_bytes(number) == expected, bits
            assert jcs.digest(number) == sha256(expected).hexdigest(), bits
            # Large fixed-form tokens parse as Python ints, which retain the
            # existing exact-integer restriction. Use an explicit float token
            # to verify their binary64 parse path.
            token = expected if b"e" in expected or b"." in expected else expected + b".0"
            assert jcs.parse_json(token) == number, bits
        for value in (float("nan"), float("inf"), -float("inf"), 2**53 + 1):
            with pytest.raises(ValueError):
                jcs.canonical_bytes(value)
        for raw in (b"NaN", b"Infinity", b"-Infinity", b"1e999", b"9007199254740993",
                    b'{"x":1,"x":2}', b"["):
            with pytest.raises(ValueError):
                jcs.parse_json(raw)
        settings = ("prec", "rounding", "Emin", "Emax", "capitals", "clamp", "traps", "flags")
        assert all(getattr(active, field) == getattr(before, field) for field in settings)


def test_frozen_jcs_vectors_keep_their_meaning_under_restricted_context(study_payload):
    with localcontext(_restricted_context()):
        assert len(VECTORS["positive"]) == len(VECTORS["negative"]) == 7
        for vector in VECTORS["positive"]:
            assert jcs.canonical_bytes(vector["input"]) == vector["expected_canonical_utf8_json"].encode()
            assert jcs.digest(vector["input"]) == vector["expected_sha256"]

        # JCS-N01 through N04: invalid constants, keys, Unicode and integers.
        for raw in (b"NaN", b"Infinity", b"-Infinity", b'{"a":1,"a":2}',
                    br'"\ud800"', b"9007199254740993"):
            with pytest.raises(ValueError):
                jcs.parse_json(raw)
        decoder = StrictLocalConfigDecoder()
        with pytest.raises(ContractViolation):
            decoder.decode(b"a: 1\na: 2\n", declared_format="yaml")
        with pytest.raises(ValueError):  # JCS-N05
            jcs.canonical_bytes(object())
        assert jcs.canonical_bytes("é") != jcs.canonical_bytes("e\u0301")  # JCS-N06
        for version in ("causal-analysis-spec/2", "unknown"):  # JCS-N07
            invalid = {**study_payload, "schema_version": version}
            with pytest.raises(ContractViolation) as error:
                decoder.decode(json.dumps(invalid).encode(), declared_format="json")
            assert error.value.reason.code == "VERSION_UNSUPPORTED"


def _configure(root, alpha=ALPHA):
    config = _inputs(root)
    _set_alpha(config, alpha)
    return config


def _set_alpha(config, alpha):
    study = json.loads(config.read_bytes())
    study["method"]["config"]["alpha"] = alpha
    config.write_text(json.dumps(study), encoding="utf-8")


def _invoke(config):
    return command.main(["--config", str(config), "--output-root", str(config.parent), "--json"])


def _bundle_bytes(root):
    return {path.name: path.read_bytes() for path in (root / "runs" / RUN).iterdir()}


def _read_and_check(root, *, context):
    with localcontext(context):
        with TrustedLocalRoot.open(root, allowed_directory=root) as trusted:
            assert LocalManifestReader().verify(root=trusted, run_id=RUN).run_id == RUN
        files = _bundle_bytes(root)
        manifest = json.loads(files["manifest.json"])
        marker = json.loads(files["_COMMITTED.json"])
        graph = json.loads(files["graph.json"])
        graph_hash = graph.pop("content_hash")
        assert b'"alpha":0.123456789' in files["study.json"]
        assert jcs.digest(graph) == graph_hash
        assert marker["manifest_sha256"] == sha256(files["manifest.json"]).hexdigest()
        assert manifest["request_hash"] == marker["request_hash"] == sha256(files["study.json"]).hexdigest()
        assert all(sha256(files[item["key"]]).hexdigest() == item["sha256"] for item in manifest["artifacts"])
        return manifest["request_hash"]


def test_bundle_roundtrip_across_contexts_preserves_hashes_on_ext4(capsys):
    with TemporaryDirectory(dir=REPO, prefix=".jcs-context-") as normal_dir, \
         TemporaryDirectory(dir=REPO, prefix=".jcs-context-") as altered_dir:
        normal, altered = Path(normal_dir), Path(altered_dir)
        config = _configure(normal)
        other_config = _configure(altered)
        with localcontext(Context()):
            assert _invoke(config) == 0
        with localcontext(Context(prec=6)):
            assert _invoke(other_config) == 0
        expected = _bundle_bytes(normal)
        assert _read_and_check(normal, context=_restricted_context()) == _read_and_check(altered, context=Context())
        with localcontext(_restricted_context()):
            assert _invoke(config) == 0
            assert _bundle_bytes(normal) == expected
            _set_alpha(config, 0.123456781)
            assert _invoke(config) == 5
        assert json.loads(capsys.readouterr().out.splitlines()[-1])["reason_code"] == "RUN_ID_CONFLICT"
        assert _bundle_bytes(normal) == expected

        study_path = normal / "runs" / RUN / "study.json"
        rounded = expected["study.json"].replace(b"0.123456789", b"0.123457")
        assert rounded != expected["study.json"]
        study_path.write_bytes(rounded)
        invalid = _bundle_bytes(normal)
        with localcontext(_restricted_context()):
            with TrustedLocalRoot.open(normal, allowed_directory=normal) as trusted:
                with pytest.raises(ContractViolation) as error:
                    LocalManifestReader().verify(root=trusted, run_id=RUN)
        assert error.value.reason.code == "ARTIFACT_HASH_MISMATCH"
        assert _bundle_bytes(normal) == invalid
