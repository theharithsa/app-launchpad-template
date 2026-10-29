#!/usr/bin/env python3
"""Check local Markdown links (including hidden agent files); never access the network."""
import argparse
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


def check_links(root):
    errors = []
    files = sorted(p for p in root.rglob('*') if p.is_file() and p.suffix in ('.md', '.mdc')
                   and not any(part in ('.git', 'node_modules', '.venv', '__pycache__') for part in p.parts))
    for file in files:
        content = re.sub(r'^```.*?^```[^\n]*$', '', file.read_text(), flags=re.MULTILINE | re.DOTALL)
        inline = re.findall(r'\]\(\s*(<[^>]+>|[^\s)]+)', content)
        definitions = re.findall(r'^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)', content, re.MULTILINE)
        for value in inline + definitions:
            target = value.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            decoded = unquote(parsed.path)
            destination = root / decoded.lstrip('/') if decoded.startswith('/') else file.parent / decoded
            if not destination.exists():
                errors.append(f'{file.relative_to(root)}: missing local link {target}')
    return sorted(set(errors))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_links(args.root.resolve())
    for error in errors:
        print('ERROR: ' + error)
    if not errors:
        print('Local Markdown links passed.')
    raise SystemExit(bool(errors))
