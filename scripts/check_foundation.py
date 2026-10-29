#!/usr/bin/env python3
"""Validate foundation structure; --ready additionally checks discovery decisions."""
import argparse
import json
from pathlib import Path
import re
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_catalog import validate_catalog

DECISIONS = ('product', 'stack', 'hosting', 'privacy', 'observability', 'license')
REQUIRED = ('AGENTS.md', 'docs/project-brief.md', 'docs/decisions.md',
            'docs/coverage.md', 'docs/release-plan.md', 'docs/testing.md',
            'docs/delivery.md', 'SECURITY.md', 'qa/evidence.json',
            '.agents/skills/app-launchpad/SKILL.md')

def validate(root, ready=False):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append('Missing required file: ' + name)
    try:
        project = json.loads((root / 'project.json').read_text())
        if not isinstance(project, dict) or project.get('schemaVersion') != 1:
            raise ValueError('Expected schemaVersion 1 object')
        decisions = project.get('decisions')
        if not isinstance(decisions, dict):
            raise ValueError('decisions must be an object')
        for key in DECISIONS:
            decision = decisions.get(key)
            if not isinstance(decision, dict):
                errors.append('Missing decision: ' + key)
                continue
            if decision.get('status') not in ('needs-user-input', 'proposed', 'approved', 'not-applicable'):
                errors.append('Invalid decision status: ' + key)
            if ready:
                if decision.get('status') not in ('approved', 'not-applicable'):
                    errors.append('Unresolved decision: ' + key)
                for field in ('value', 'approval'):
                    if not isinstance(decision.get(field), str) or not decision[field].strip():
                        errors.append(f'{key} needs {field}')
        if ready:
            if not isinstance(project.get('name'), str) or not project['name'].strip():
                errors.append('Project name is required')
            template = project.get('template')
            if not isinstance(template, dict) or not re.fullmatch(r'[0-9a-f]{40}', str(template.get('revision', ''))):
                errors.append('Record the source template commit SHA')
    except (OSError, ValueError, TypeError) as error:
        errors.append('Invalid project.json: ' + str(error))
    try:
        evidence = json.loads((root / 'qa/evidence.json').read_text())
        if not isinstance(evidence, dict) or evidence.get('schemaVersion') != 1 or not isinstance(evidence.get('checks'), list):
            raise ValueError('Expected schemaVersion 1 and checks array')
    except (OSError, ValueError, TypeError) as error:
        errors.append('Invalid evidence record: ' + str(error))
    errors.extend(validate_catalog(root))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--ready', action='store_true')
    args = parser.parse_args()
    errors = validate(args.root, args.ready)
    for error in errors:
        print('ERROR: ' + error)
    if errors:
        raise SystemExit(1)
    print('Discovery gate passed; application/release checks still required.' if args.ready
          else 'Foundation structure passed; application readiness not evaluated.')

if __name__ == '__main__':
    main()
