from pathlib import Path

def canonical_readme_name(directory: str) -> str:
    p = Path(directory)
    if str(p) in ('.', ''):
        return 'README.md'
    parts=[x for x in p.parts if x not in ('.','')]
    # instance convention keeps established numeric prefix and concrete IDs
    return 'README_' + '_'.join(parts) + '.md'

if __name__ == '__main__':
    import sys
    print(canonical_readme_name(sys.argv[1] if len(sys.argv)>1 else '.'))
