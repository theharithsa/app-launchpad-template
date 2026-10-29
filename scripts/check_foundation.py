#!/usr/bin/env python3
"""Validate repository structure and metadata; --ready also checks discovery decisions."""
import argparse
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from contracts import DECISIONS, SEMVER_PATTERN
from schema_validation import load_json, validate_record
from skill_catalog import validate_catalog

REQUIRED = ('TEMPLATE_VERSION', 'README.md', 'CHANGELOG.md', 'docs/template-changelog.md',
            'docs/versioning.md', 'AGENTS.md', 'docs/project-brief.md', 'docs/decisions.md',
            'docs/coverage.md', 'docs/release-plan.md', 'docs/testing.md', 'docs/delivery.md',
            'SECURITY.md', 'LICENSE', 'qa/evidence.json', '.agents/skills/app-launchpad/SKILL.md')


def read_record(root, filename, name, errors):
    try:
        value = load_json(root / filename)
    except (OSError, ValueError) as error:
        errors.append(f'{filename}: {error}')
        return None
    errors.extend(f'{filename}: {error}' for error in validate_record(root, name, value))
    return value


def validate(root, ready=False):
    root = root.resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('Missing required file: ' + name)
    version = None
    try:
        version = (root / 'TEMPLATE_VERSION').read_text().strip()
        if not re.fullmatch(SEMVER_PATTERN, version):
            errors.append('TEMPLATE_VERSION: invalid SemVer (numeric identifiers cannot have leading zeros)')
        if f'Template version: **{version}**' not in (root / 'README.md').read_text():
            errors.append('README template version differs from TEMPLATE_VERSION')
        headings = re.findall(r'^## \[([^\]]+)\]', (root / 'docs/template-changelog.md').read_text(), re.MULTILINE)
        if not headings or headings[0] != version:
            errors.append('Newest template changelog version differs from TEMPLATE_VERSION')
    except (OSError, ValueError) as error:
        errors.append('Invalid template version: ' + str(error))
    project = read_record(root, 'project.json', 'project', errors)
    if isinstance(project, dict):
        template = project.get('template')
        if isinstance(template, dict) and template.get('version') != version:
            errors.append('Project template version differs from TEMPLATE_VERSION')
        if ready:
            if not isinstance(project.get('name'), str) or not project['name'].strip():
                errors.append('Project name is required')
            if not isinstance(template, dict) or not re.fullmatch('[0-9a-f]{40}', str(template.get('revision', ''))):
                errors.append('Record the source template commit SHA')
            decisions = project.get('decisions')
            if isinstance(decisions, dict):
                for key in DECISIONS:
                    decision = decisions.get(key)
                    if not isinstance(decision, dict):
                        continue
                    if decision.get('status') not in ('approved', 'not-applicable'):
                        errors.append('Unresolved decision: ' + key)
                    for field in ('value', 'approval'):
                        if not isinstance(decision.get(field), str) or not decision[field].strip():
                            errors.append(f'{key} needs {field}')
    read_record(root, 'qa/evidence.json', 'evidence', errors)
    errors.extend(validate_catalog(root))
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--ready', action='store_true')
    parser.add_argument('--json', action='store_true', dest='json_output')
    args = parser.parse_args()
    errors = validate(args.root, args.ready)
    if args.json_output:
        print(json.dumps({'ok': not errors, 'errors': errors, 'ready': args.ready}, indent=2))
    else:
        for error in errors:
            print('ERROR: ' + error)
        if not errors:
            print('Discovery gate passed; application/release checks still required.' if args.ready
                  else 'Foundation structure passed; application readiness not evaluated.')
    raise SystemExit(bool(errors))

if __name__ == '__main__':
    main()
