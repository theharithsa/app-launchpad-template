"""Validate declared skill/service ownership, accumulating deterministic diagnostics."""
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import subprocess
import warnings
from schema_validation import load_json, validate_record


def safe_path(root, value):
    if (not isinstance(value, str) or not value or PurePosixPath(value).is_absolute()
            or PureWindowsPath(value).drive or PureWindowsPath(value).root
            or '..' in Path(value).parts or '\\' in value or any(ord(c) < 32 for c in value)):
        raise ValueError('Expected safe repository-relative path')
    root = root.resolve()
    candidate = root / value
    candidate.relative_to(root)
    cursor = candidate
    while cursor != root and cursor != cursor.parent:
        if cursor.is_symlink():
            raise ValueError('Symlink path is not allowed')
        cursor = cursor.parent
    candidate.resolve().relative_to(root)
    return candidate


def warn_unavailable_revision(root, service, revision):
    """Warn about unavailable history only in this repo, not copied fixtures."""
    if not isinstance(revision, str) or not re.fullmatch('[0-9a-f]{40}', revision):
        return
    try:
        repository = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                                    capture_output=True, text=True, encoding='utf-8', timeout=5)
        if repository.returncode or Path(repository.stdout.strip()).resolve() != root.resolve():
            return
        result = subprocess.run(['git', 'cat-file', '-e', revision + '^{commit}'], cwd=root,
                                capture_output=True, text=True, encoding='utf-8', timeout=5)
    except (OSError, subprocess.TimeoutExpired):
        return  # Git/history availability is not required for generated copies.
    if result.returncode:
        warnings.warn(f'{service}: lastReviewedRevision {revision} does not resolve locally; '
                      'fetch the source history or refresh the continuation after review',
                      RuntimeWarning, stacklevel=2)


def validate_catalog(root):
    errors = []
    try:
        data = load_json(safe_path(root, 'skills/catalog.json'))
    except (OSError, ValueError) as error:
        return [f'Invalid skill catalog: {error}']
    errors.extend('catalog ' + error for error in validate_record(root, 'catalog', data))
    if not isinstance(data, dict):
        return sorted(set(errors))
    maps, lists = [], []
    for label, key in [('skill', 'skills'), ('service', 'services')]:
        records = data.get(key)
        records = records if isinstance(records, list) else []
        mapping = {}
        usable = []
        for index, item in enumerate(records):
            if not isinstance(item, dict):
                continue
            identity = item.get('id')
            valid_id = isinstance(identity, str) and re.fullmatch('[a-z][a-z0-9-]{0,63}', identity)
            usable.append(item if valid_id else {**item, 'id': f'{label}[{index}]'})
            if not valid_id:
                continue  # Continue independent path checks using a deterministic record label.
            if identity in mapping:
                errors.append(f'Duplicate {label} id: {identity}')
            else:
                mapping[identity] = item
        maps.append(mapping)
        lists.append(usable)
    skill_map, service_map = maps
    skills, services = lists

    def check_path(value, label, exists=True, file=False):
        try:
            candidate = safe_path(root, value)
            if exists and not candidate.exists():
                raise ValueError('Missing path: ' + str(value))
            if file and not candidate.is_file():
                raise ValueError('Expected file: ' + str(value))
            return candidate
        except (OSError, ValueError) as error:
            errors.append(f'{label}: {error}')
            return None

    listed = set()
    for item in skills:
        target = check_path(item.get('path'), item['id'], file=True)
        if target is None:
            continue
        normalized = target.relative_to(root.resolve()).as_posix()
        if normalized in listed:
            errors.append('Duplicate skill path: ' + normalized)
        listed.add(normalized)
        try:
            parts = target.read_text(encoding='utf-8').split('---', 2)
            frontmatter = parts[1] if len(parts) == 3 and not parts[0].strip() else ''
            name = re.search(r'^name:\s*[\'"]?([a-z][a-z0-9-]*)[\'"]?\s*$', frontmatter, re.MULTILINE)
            if target.name != 'SKILL.md' or not name or name.group(1) != item['id']:
                errors.append(f'{item["id"]}: SKILL.md needs matching name frontmatter')
            if not re.search(r'^description:\s*\S', frontmatter, re.MULTILINE):
                errors.append(f'{item["id"]}: description frontmatter missing')
        except (OSError, UnicodeError) as error:
            errors.append(f'{item["id"]}: {error}')
    discovered = {p.relative_to(root).as_posix() for base in ('skills', '.agents/skills')
                  for p in (root / base).rglob('SKILL.md')}
    for filename in sorted(discovered - listed):
        errors.append('Uncataloged skill: ' + filename)
    used = set()
    for item in services:
        warn_unavailable_revision(root, item['id'], item.get('lastReviewedRevision'))
        sid = item.get('skillId')
        if not isinstance(sid, str) or sid not in skill_map or skill_map[sid].get('kind') != 'service':
            errors.append(f'{item["id"]}: needs a registered service skill')
        elif sid in used:
            errors.append(f'{item["id"]}: service skill already owned: {sid}')
        else:
            used.add(sid)
        active = item.get('status') == 'active'
        for field in ('sourcePaths', 'entrypoints', 'contracts'):
            values = item.get(field)
            if not isinstance(values, list):
                continue
            for value in values:
                check_path(value, f'{item["id"]}.{field}', exists=active or field == 'contracts',
                           file=active and field == 'entrypoints')
        check_path(item.get('continuation'), item['id'] + '.continuation', file=True)
    for sid in sorted({item['id'] for item in skills if item.get('kind') == 'service'} - used):
        errors.append('Service skill missing inventory entry: ' + sid)
    for label, mapping in zip(('skill', 'service'), maps):
        visited, visiting = set(), set()
        def visit(key):
            if key in visiting:
                errors.append(f'{label} dependency cycle: {key}')
                return
            if key in visited:
                return
            visiting.add(key)
            dependencies = mapping[key].get('dependsOn')
            if isinstance(dependencies, list):
                for dependency in dependencies:
                    if not isinstance(dependency, str) or dependency not in mapping:
                        errors.append(f'{label} {key}: unknown dependency {dependency!r}')
                    else:
                        visit(dependency)
            visiting.remove(key)
            visited.add(key)
        for key in sorted(mapping):
            visit(key)
    return sorted(set(errors))
