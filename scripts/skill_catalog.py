"""Validate repository skill routing and declared service ownership (no commands executed)."""
import json
from pathlib import Path
import re


def safe_path(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError('Expected repository-relative path')
    path = root / value
    if any(p.is_symlink() for p in (path, *path.parents) if p != root.parent):
        # Resolved roots are supplied by callers; no symlink traversal in repository paths.
        raise ValueError('Symlink path is not allowed')
    path.resolve().relative_to(root.resolve())
    return path


def validate_catalog(root):
    errors = []
    try:
        data = json.loads((root / 'skills/catalog.json').read_text())
        if not isinstance(data, dict) or data.get('schemaVersion') != 1:
            raise ValueError('Expected catalog schemaVersion 1')
        skills, services = data.get('skills'), data.get('services')
        if not isinstance(skills, list) or not isinstance(services, list):
            raise ValueError('skills and services must be arrays')
        maps = []
        for label, records in [('skill', skills), ('service', services)]:
            mapping = {}
            for item in records:
                if not isinstance(item, dict) or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', str(item.get('id', ''))):
                    raise ValueError('Invalid ' + label + ' id')
                if item['id'] in mapping:
                    raise ValueError('Duplicate ' + label + ' id: ' + item['id'])
                mapping[item['id']] = item
            maps.append(mapping)
        skill_map, service_map = maps
        listed = set()
        def path(value, exists=True):
            candidate = safe_path(root, value)
            if exists and not candidate.exists():
                raise ValueError('Missing path: ' + str(value))
            return candidate
        for item in skills:
            if item.get('kind') not in ('workflow', 'service') or not item.get('description'):
                raise ValueError('Skill needs kind and description: ' + item['id'])
            target = path(item.get('path'))
            if target.name != 'SKILL.md' or not target.is_file():
                raise ValueError('Skill entry must point to SKILL.md')
            text = target.read_text()
            frontmatter = text.split('---', 2)
            if len(frontmatter) != 3 or frontmatter[0].strip():
                raise ValueError('Skill needs YAML frontmatter: ' + item['id'])
            match = re.search(r'^name:\s*([a-z][a-z0-9-]*)\s*$', frontmatter[1], re.MULTILINE)
            if not match or match.group(1) != item['id'] or not re.search(r'^description:\s*\S', frontmatter[1], re.MULTILINE):
                raise ValueError('Skill frontmatter needs matching name and description: ' + item['id'])
            normalized = target.relative_to(root).as_posix()
            if normalized in listed:
                raise ValueError('Duplicate skill path: ' + normalized)
            listed.add(normalized)
        discovered = {p.relative_to(root).as_posix() for base in ('skills', '.agents/skills')
                      for p in (root / base).rglob('SKILL.md')}
        if discovered != listed:
            raise ValueError('Uncataloged or misplaced skill files: ' + str(sorted(discovered ^ listed)))
        used = set()
        for item in services:
            sid = item.get('skillId')
            if sid not in skill_map or skill_map[sid]['kind'] != 'service' or sid in used:
                raise ValueError('Each service needs its own registered service skill: ' + item['id'])
            used.add(sid)
            if item.get('status') not in ('planned', 'active', 'retired'):
                raise ValueError('Invalid service status')
            active = item['status'] == 'active'
            if not isinstance(item.get('sourcePaths'), list) or not item['sourcePaths']:
                raise ValueError('Service needs sourcePaths')
            for field in ('entrypoints', 'contracts', 'testCommands'):
                if not isinstance(item.get(field), list) or any(not isinstance(v, str) or not v.strip() for v in item[field]):
                    raise ValueError('Invalid service ' + field)
            for field in ('sourcePaths', 'entrypoints', 'contracts'):
                for value in item[field]:
                    path(value, exists=active or field == 'contracts')
            path(item.get('continuation'))
            revision = item.get('lastReviewedRevision')
            if revision is not None and (not isinstance(revision, str) or not re.fullmatch('[0-9a-f]{40}', revision)):
                raise ValueError('Invalid lastReviewedRevision')
            if active and (not isinstance(item.get('owner'), str) or not item['owner'].strip()
                           or not item['entrypoints'] or not item['testCommands']):
                raise ValueError('Active service needs owner, entrypoints and testCommands')
        if used != {s['id'] for s in skills if s['kind'] == 'service'}:
            raise ValueError('Service skill missing its service inventory entry')
        for mapping in maps:
            visited, visiting = set(), set()
            def visit(key):
                if key in visiting:
                    raise ValueError('Dependency cycle: ' + key)
                if key in visited:
                    return
                visiting.add(key)
                dependencies = mapping[key].get('dependsOn')
                if not isinstance(dependencies, list):
                    raise ValueError('dependsOn must be an array')
                for dependency in dependencies:
                    if not isinstance(dependency, str) or dependency not in mapping:
                        raise ValueError('Unknown dependency: ' + str(dependency))
                    visit(dependency)
                visiting.remove(key)
                visited.add(key)
            for key in mapping:
                visit(key)
    except (OSError, ValueError, TypeError, KeyError) as error:
        errors.append('Invalid skill catalog: ' + str(error))
    return errors
