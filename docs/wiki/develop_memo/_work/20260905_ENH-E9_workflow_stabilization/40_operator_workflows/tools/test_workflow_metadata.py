#!/usr/bin/env python3
from __future__ import annotations

import unittest

from workflow_metadata import (
    DependencySyntaxError,
    MetadataAmbiguityError,
    ExecutionModeSyntaxError,
    RequiredPackagesSyntaxError,
    metadata_field,
    parse_dependencies,
    parse_execution_mode,
    parse_gate_dependencies,
    parse_required_packages,
    parse_dependency_reference,
    validate_dependency_ids,
)


class MetadataFieldTests(unittest.TestCase):
    def test_depends_on_bold(self):
        self.assertEqual(metadata_field("**Depends on:** P01\n", "Depends on"), "P01")

    def test_depends_on_plain(self):
        self.assertEqual(metadata_field("Depends on: P01\n", "Depends on"), "P01")

    def test_depends_on_bullet(self):
        self.assertEqual(metadata_field("- Depends on: P01\n", "Depends on"), "P01")

    def test_gate_dependency_bold(self):
        self.assertEqual(metadata_field("**Depends on:** G03 PASS\n", "Depends on"), "G03 PASS")

    def test_empty_is_not_repaired(self):
        self.assertEqual(metadata_field("Depends on:\n", "Depends on"), "")

    def test_missing_is_not_inferred(self):
        self.assertEqual(metadata_field("Dependency maybe P01\n", "Depends on"), "")

    def test_other_labels_use_same_tolerance(self):
        cases = {
            "Contract status": "FROZEN",
            "Verification contract status": "FROZEN",
            "Self-containment": "MUST",
            "Information isolation": "MUST",
            "Reporting contract": "REQUIRED",
            "Gate": "G03",
            "Package": "P01",
            "Status at issuance": "DRAFT_NOT_FROZEN",
            "Execution mode": "WORK_PACKAGE",
            "Required packages": "P01, P02",
        }
        for label, expected in cases.items():
            with self.subTest(label=label):
                self.assertEqual(metadata_field(f"- {label}: {expected}\n", label), expected)

    def test_duplicate_same_value_is_tolerated(self):
        text = "Depends on: P01\n**Depends on:** P01\n"
        self.assertEqual(metadata_field(text, "Depends on"), "P01")

    def test_conflicting_duplicate_is_rejected(self):
        with self.assertRaises(MetadataAmbiguityError):
            metadata_field("Depends on: P01\n- Depends on: P02\n", "Depends on")


class DependencyTests(unittest.TestCase):
    def test_none(self):
        self.assertEqual(parse_dependencies("NONE"), ())

    def test_package(self):
        refs = parse_dependencies("P01")
        self.assertEqual((refs[0].kind, refs[0].identifier), ("package", "P01"))

    def test_gate_pass(self):
        refs = parse_dependencies("G03 PASS")
        self.assertEqual((refs[0].kind, refs[0].identifier, refs[0].required_state), ("gate", "G03", "PASS"))

    def test_multiple(self):
        refs = parse_dependencies("P01, G02 PASS")
        self.assertEqual([r.identifier for r in refs], ["P01", "G02"])

    def test_empty_fails(self):
        with self.assertRaises(DependencySyntaxError):
            parse_dependencies("")

    def test_unclear_fails(self):
        with self.assertRaises(DependencySyntaxError):
            parse_dependencies("something unclear")

    def test_noncanonical_ids_fail(self):
        for value in ("P1", "G3 PASS", "G03 maybe"):
            with self.subTest(value=value), self.assertRaises(DependencySyntaxError):
                parse_dependencies(value)

    def test_repository_identity_validation(self):
        refs = parse_dependencies("P02, G03 PASS")
        self.assertEqual(
            validate_dependency_ids(refs, known_package_ids={"P01", "P02"}, known_gate_ids={"G02", "G03"}),
            [],
        )
        self.assertTrue(validate_dependency_ids(refs, known_package_ids={"P01"}, known_gate_ids={"G02"}))

    def test_compatibility_single_reference(self):
        ref = parse_dependency_reference("P01", known_package_ids={"P01"})
        self.assertIsNotNone(ref)
        self.assertEqual(ref.identifier, "P01")


class Gate06MetadataTests(unittest.TestCase):
    def test_execution_modes(self):
        self.assertEqual(parse_execution_mode("WORK_PACKAGE"), "WORK_PACKAGE")
        self.assertEqual(parse_execution_mode("single-execution"), "SINGLE_EXECUTION")
        with self.assertRaises(ExecutionModeSyntaxError):
            parse_execution_mode("maybe")

    def test_required_packages_none(self):
        self.assertEqual(parse_required_packages("NONE"), ())

    def test_required_packages_list(self):
        self.assertEqual(parse_required_packages("P01, p02"), ("P01", "P02"))

    def test_required_packages_invalid(self):
        for value in ("", "P1", "P01,", "P01, P01", "P00 and P01"):
            with self.subTest(value=value), self.assertRaises(RequiredPackagesSyntaxError):
                parse_required_packages(value)

    def test_gate_dependencies_gate_only(self):
        refs = parse_gate_dependencies("G01 PASS, G02 PASS")
        self.assertEqual([r.identifier for r in refs], ["G01", "G02"])
        self.assertEqual(parse_gate_dependencies("NONE"), ())
        with self.assertRaises(DependencySyntaxError):
            parse_gate_dependencies("P01")


if __name__ == "__main__":
    unittest.main()
