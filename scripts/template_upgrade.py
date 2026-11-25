"""Report template changes and local overlap from already-fetched Git revisions."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess

from contracts import SEMVER_PATTERN


TEMPLATE_PATHS = (
    '.agents/skills', '.claude/skills', '.github/ISSUE_TEMPLATE', '.github/workflows',
    '.github/pull_request_template.md', 'AGENTS.md', 'CLAUDE.md', 'README.md',
    'TEMPLATE_VERSION', 'CONTRIBUTING.md', 'SECURITY.md', 'docs', 'evals',
    'pyproject.toml', 'schemas', 'scripts', 'site', 'skills', 'tests',
)


def git(root, *arguments):
    result = subprocess.run(
        ['git', '--no-optional-locks', *arguments], cwd=root, check=True, timeout=30,
        capture_output=True, encoding='utf-8', env={**os.environ, 'GIT_TERMINAL_PROMPT': '0'},
    )
    return result.stdout


def resolve_target(root, tag):
    for ref in (f'refs/app-launchpad/{tag}', f'refs/tags/{tag}'):
        try:
            return git(root, 'rev-parse', '--verify', f'{ref}^{{commit}}').strip()
        except subprocess.CalledProcessError:
            continue
    raise ValueError(f'{tag} is unavailable locally. Fetch the published tag using docs/upgrading.md.')


def report(root, target_tag):
    if not target_tag.startswith('v') or not re.fullmatch(SEMVER_PATTERN, target_tag[1:]):
        raise ValueError('Target must be a version tag such as v1.14.3')
    data = json.loads((root / 'project.json').read_text(encoding='utf-8'))['template']
    previous = data.get('revision', '')
    if not isinstance(previous, str) or not re.fullmatch(r'[0-9a-f]{40}', previous):
        raise ValueError('Record the exact template source revision in project.json first.')
    try:
        recorded_version = git(root, 'show', f'{previous}:TEMPLATE_VERSION').strip()
    except subprocess.CalledProcessError as error:
        raise ValueError('Recorded template revision is unavailable locally. Fetch the source tag first.') from error
    if recorded_version != data['version']:
        raise ValueError('Recorded template revision and version disagree.')
    target = resolve_target(root, target_tag)
    if git(root, 'show', f'{target}:TEMPLATE_VERSION').strip() != target_tag[1:]:
        raise ValueError('Target version metadata does not match the requested tag.')

    compare = ('--no-ext-diff', '--no-textconv', '--no-renames')
    upstream = git(root, 'diff', *compare, '--name-status', '-z', previous, target,
                   '--', *TEMPLATE_PATHS).split('\0')
    customized = set(git(root, 'diff', *compare, '--name-only', '-z', previous,
                         '--', *TEMPLATE_PATHS).split('\0'))
    tracked = set(git(root, 'ls-files', '-z', '--', *TEMPLATE_PATHS).split('\0'))
    changes = []
    for change, name in zip(upstream[0::2], upstream[1::2]):
        local_path = root / name
        overlap = name in customized or (name not in tracked and (local_path.exists() or local_path.is_symlink()))
        changes.append({'path': name, 'change': change, 'localChanges': overlap})
    return {'from': {'version': recorded_version, 'revision': previous},
            'to': {'version': target_tag[1:], 'revision': target}, 'changes': changes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--to', required=True, help='a published version tag available locally')
    parser.add_argument('--root', type=Path, default=Path.cwd())
    args = parser.parse_args()
    try:
        print(json.dumps(report(args.root.resolve(), args.to), indent=2))
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
