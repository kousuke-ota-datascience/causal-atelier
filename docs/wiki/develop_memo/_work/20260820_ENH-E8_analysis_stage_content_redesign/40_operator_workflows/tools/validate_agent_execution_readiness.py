from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    p = ROOT / rel
    if not p.exists():
        raise FileNotFoundError(rel)
    return p.read_text(encoding="utf-8")


def validate_gate(gate: str) -> list[str]:
    problems: list[str] = []
    if gate == "G01":
        required = [
            "10_enhance_instruction/G01/06_Ariadne_ENH-E8_G01_implementation_instruction.md",
            "10_enhance_instruction/G01/07_Ariadne_ENH-E8_G01_test_instruction.md",
        ]
    elif gate == "G02":
        required = [
            "10_enhance_instruction/G02/06_Ariadne_ENH-E8_G02_implementation_instruction.md",
            "10_enhance_instruction/G02/07_Ariadne_ENH-E8_G02_test_instruction.md",
            "10_enhance_instruction/G02/06_G02_P01_analysis_stage_presentation_framework.md",
            "10_enhance_instruction/G02/06_G02_P02_causal_stage_surface_separation.md",
            "10_enhance_instruction/G02/06_G02_P03_predictive_stage_surface_separation.md",
        ]
    else:
        return [f"UNKNOWN_GATE {gate}"]

    texts: dict[str, str] = {}
    for rel in required:
        try:
            texts[rel] = _read(rel)
        except FileNotFoundError:
            problems.append(f"MISSING {rel}")

    for rel, text in texts.items():
        if "TBD_BEFORE_FREEZE" in text:
            problems.append(f"{rel}: contains TBD_BEFORE_FREEZE")
        if rel.endswith("_implementation_instruction.md") and "Contract status: `FROZEN`" not in text:
            problems.append(f"{rel}: Contract status is not FROZEN")
        if rel.endswith("_test_instruction.md") and "Verification contract status: `FROZEN`" not in text:
            problems.append(f"{rel}: Verification contract status is not FROZEN")

    snapshot_readme = _read(
        "00_enhance_background/Revised_requirements_definition_documents/README_00_Revised_requirements_definition_documents.md"
    )
    if "BLOCKED_SNAPSHOT_INCOMPLETE" in snapshot_readme:
        problems.append("revised detailed-design snapshot is incomplete")

    if gate == "G02":
        preflight = _read("40_operator_workflows/preflight/AGENT_EXECUTION_READINESS.md")
        if "canonical G01 999 decision = PASS" in preflight and "[x] canonical G01 999 decision = PASS" not in preflight:
            problems.append("G02 dependency G01 PASS is not recorded in preflight")

    return problems


if __name__ == "__main__":
    gate = sys.argv[1] if len(sys.argv) > 1 else "G01"
    issues = validate_gate(gate)
    if issues:
        print("NOT_READY")
        print("\n".join(f"- {x}" for x in issues))
        raise SystemExit(1)
    print("READY_CONTRACT_TEXT")
