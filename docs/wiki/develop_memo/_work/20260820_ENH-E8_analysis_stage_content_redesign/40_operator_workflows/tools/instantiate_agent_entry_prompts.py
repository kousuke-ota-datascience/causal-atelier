from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]

def main(gate, trial='01', package=None):
    if gate=='G01':
        prompt=ROOT/'40_operator_workflows/agent_entry_prompts/10_normal_execution_01_single_execution_coding_agent_prompt.md'
    elif gate=='G02' and package:
        prompt=ROOT/'40_operator_workflows/agent_entry_prompts/10_normal_execution_02_work_package_coding_agent_prompt.md'
    elif gate=='G02':
        prompt=ROOT/'40_operator_workflows/agent_entry_prompts/50_orchestration_01_gate_orchestrator_prompt.md'
    else:
        raise SystemExit('unknown gate')
    print(f'Read and execute: {prompt}')
    print(f'GATE_ID={gate}')
    print(f'TRIAL_NO={trial}')
    if package: print(f'PACKAGE_ID={package}')

if __name__=='__main__':
    main(*sys.argv[1:])
