from ariadne.interfaces.cli.scientific_stage import run_stage
from ariadne.product.domain.enums import ExecutionOperation

def main(argv: list[str] | None = None) -> int:
    return run_stage(ExecutionOperation.REFUTATION, argv)
