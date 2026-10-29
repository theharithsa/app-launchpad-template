#!/usr/bin/env python3
"""Copy planning-only foundation files; refuse every collision before writing."""
import argparse
import json
import os
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target', required=True)
    p.add_argument('--name', required=True)
    p.add_argument('--dry-run', action='store_true')
    a=p.parse_args()
    if not a.name.strip() or any(ord(c)<32 for c in a.name):
        p.error('App name must be nonempty single-line text')
    target=Path(a.target).expanduser().absolute()
    # Refuse symlink ancestry to avoid copying into an unexpected checkout.
    for ancestor in (target, *target.parents):
        if ancestor.is_symlink():
            p.error('Target ancestry must not contain symlinks')
        if ancestor.exists() and not ancestor.is_dir():
            p.error('Target ancestry must be directories')
    source=Path(__file__).resolve().parent.parent/'assets'/'project-foundation'
    plan=[]
    for f in sorted(source.rglob('*')):
        if not f.is_file() or any(part in ('.DS_Store', '__MACOSX', '__pycache__') or part.startswith('._') for part in f.relative_to(source).parts): continue
        out=target/f.relative_to(source)
        if out.exists() or out.is_symlink():
            p.error('Refusing existing output: '+str(out))
        for parent in out.parents:
            if parent==target: break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                p.error('Unsafe output ancestor: '+str(parent))
        content=f.read_text()
        if f.suffix=='.json':
            obj=json.loads(content)
            obj['application']=a.name
            content=json.dumps(obj,indent=2)+'\n'
        else:
            content=content.replace('{{APP_NAME}}',a.name)
        plan.append((out,content))
    print(json.dumps({'dryRun':a.dry_run,'target':str(target),'files':[str(x.relative_to(target)) for x,_ in plan]},indent=2))
    if a.dry_run: return
    created=[]
    try:
        for out,content in plan:
            out.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive create also protects against a collision after preflight.
            with out.open('x') as h: h.write(content)
            created.append(out)
    except Exception:
        for out in reversed(created): out.unlink()
        raise
if __name__=='__main__': main()
