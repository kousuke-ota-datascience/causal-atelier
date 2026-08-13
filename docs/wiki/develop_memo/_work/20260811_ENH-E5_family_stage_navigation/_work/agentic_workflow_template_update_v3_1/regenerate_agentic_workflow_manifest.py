#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys
root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve()
files=[]
for p in sorted(root.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(root).as_posix()
    if rel=='MANIFEST.json' or rel.startswith('_bkup/'): continue
    b=p.read_bytes()
    files.append({'path':rel,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'lines':b.count(b'\n')+(0 if not b or b.endswith(b'\n') else 1)})
out={'schema_version':2,'manifest_policy':'MANIFEST.json is excluded from its own hash set to avoid self-reference. Regenerate after all template changes are final.','file_count':len(files),'files':files}
(root/'MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(root/'MANIFEST.json')
