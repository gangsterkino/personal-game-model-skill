"""Check package metadata, Python/JSON syntax, local links and source-lock hashes."""
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SKILL=ROOT/'skills/build-reference-scene'
errors=[]
files=[f for f in ROOT.rglob('*') if f.is_file() and '__pycache__' not in str(f) and '.git' not in f.parts]
for f in files:
    if f.suffix=='.py':
        try:ast.parse(f.read_text(encoding='utf-8-sig'))
        except Exception as e:errors.append(f'{f.relative_to(ROOT)}: {e}')
    if f.suffix=='.json':
        try:json.loads(f.read_text())
        except Exception as e:errors.append(f'{f.relative_to(ROOT)}: {e}')
    if f.suffix=='.md':
        for url in re.findall(r'\]\(([^)\s]+)\)',f.read_text()):
            if url.startswith(('http:','https:','mailto:','#','data:')):continue
            target=url.split('#')[0]
            if target and not (f.parent/target).exists():errors.append(f'Broken local link {f.relative_to(ROOT)} -> {url}')
text=(SKILL/'SKILL.md').read_text()
if not text.startswith('---\nname: build-reference-scene\ndescription: '):errors.append('Invalid primary skill metadata')
lock=json.loads((SKILL/'references/source-lock.json').read_text())
for source in lock['sources']:
    for entry in source['files']:
        f=SKILL/entry['path']
        if entry['status']=='excluded':
            if f.exists():errors.append('Excluded file still exists '+entry['path'])
        elif not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=entry['sha256']:
            errors.append('Source hash mismatch '+entry['path'])
print(json.dumps({'files':len(files),'python_files':sum(f.suffix=='.py' for f in files),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
