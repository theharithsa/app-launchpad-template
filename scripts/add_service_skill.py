#!/usr/bin/env python3
"""Register a service skill and continuation record without creating application code."""
import argparse
import json
from pathlib import Path
import re
import shutil
from skill_catalog import safe_path, validate_catalog


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument('--id', required=True)
    p.add_argument('--source-path', required=True)
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    root = a.root.resolve()
    if not re.fullmatch('[a-z][a-z0-9-]{0,55}', a.id):
        p.error('Service id must be lowercase letters/digits/hyphens, starting with a letter, max 56 characters')
    try:
        safe_path(root, a.source_path)
        errors = validate_catalog(root)
        if errors:
            raise ValueError('; '.join(errors))
        registry = root / 'skills/catalog.json'
        if registry.is_symlink():
            raise ValueError('Catalog must not be a symlink')
        before = registry.read_text()
        data = json.loads(before)
        name = 'service-' + a.id
        destination = safe_path(root, 'skills/' + name)
        if destination.exists() or destination.is_symlink() or any(s['id'] == a.id for s in data['services']) or any(s['id'] == name for s in data['skills']):
            raise ValueError('Refusing duplicate service or existing output')
        data['skills'].append({'id': name, 'kind': 'service', 'path': f'skills/{name}/SKILL.md',
                              'description': f'Maintain the {a.id} service; read its implementation and continuation context.',
                              'dependsOn': ['project-implementation', 'project-testing', 'project-deployment', 'project-observability']})
        data['services'].append({'id': a.id, 'skillId': name, 'sourcePaths': [a.source_path],
                                 'entrypoints': [], 'owner': None, 'status': 'planned', 'dependsOn': [],
                                 'contracts': [], 'testCommands': [], 'continuation': f'skills/{name}/continuation.md',
                                 'lastReviewedRevision': None})
        print(json.dumps({'dryRun': a.dry_run, 'service': a.id, 'directory': str(destination)}, indent=2))
        if a.dry_run:
            return
        # Exclusive lock coordinates this tool; never replace external edits detected during generation.
        lock = root / 'skills/.catalog.lock'
        with lock.open('x'):
            created = False
            try:
                if registry.read_text() != before:
                    raise ValueError('Catalog changed; retry after reviewing it')
                destination.mkdir()
                created = True
                (destination / 'SKILL.md').write_text(f'''---
name: {name}
description: Maintain the {a.id} service using its source, contracts, operations and continuation record.
---

# {a.id} service

Status: planned. Read [continuation](continuation.md) and this service's entry in [catalog](../catalog.json). Verify current source and Git/CI before trusting old notes. Apply the relevant shared workflow skills in the catalog.

## Purpose, boundaries and owner

Needs implementation context. Define responsibilities, exclusions, source paths (`{a.source_path}`), actual runtime entrypoints and accountable owner. Keep catalog metadata consistent.

## Design, contracts and data

Pending: approved user journeys/UI states; API/schema versions; authorization/tenant scope; data ownership, concurrency, migrations; dependencies and failure behavior. Link real contracts and architecture decisions. Mark irrelevant layers with reasons.

## Code and safe enhancement

Pending: entrypoints, important modules and invariants, extension points and compatibility constraints. Inspect actual code before documenting these. Update this skill in the same PR as behavior changes.

## Tests

Pending: actual test files, commands, prerequisites and coverage gaps. Register real commands in the catalog; documentation is not execution evidence.

## Deployment and rollback

Pending: approved provider/environment/resource mapping, secure secret names, build/deploy commands, artifact identity, migration ordering, health verification and rollback. No deployment authorization is implied.

## Observability and recovery

Pending: service identity, initialization and signal paths, safe field contracts, runtime/SDLC correlation, telemetry tests, delivery/export health and recovery. Distinguish acceptance, tenant searchability and native linkage.

## Continuation

Update continuation.md with verified revision, issue/PR, actual check/deployment evidence, known gaps and next action before handoff. Never include credentials or customer data.
''')
                (destination / 'continuation.md').write_text(f'''# {a.id} continuation

Status: planned; no service implementation or deployment has been verified.

- Issue / PR: pending.
- Last verified source revision: pending.
- Current behavior and completed work: service skill registered only.
- Actual tests / safe evidence links: not-run.
- Source merge / release / deployment: not-run.
- Telemetry acceptance / searchability / native linkage: not-run.
- Blockers and unresolved decisions: inspect approved scope and architecture.
- Next action: implement the agreed service slice, populate the skill from real code and register entrypoints, owner, tests and dependencies. Mark active only when those fields are valid.
''')
                if registry.read_text() != before:
                    raise ValueError('Catalog changed; generated files rolled back')
                temporary = root / 'skills/.catalog.next'
                with temporary.open('x') as output:
                    output.write(json.dumps(data, indent=2) + '\n')
                try:
                    temporary.replace(registry)
                finally:
                    temporary.unlink(missing_ok=True)
            except Exception:
                if created:
                    shutil.rmtree(destination)
                raise
            finally:
                lock.unlink(missing_ok=True)
    except (OSError, ValueError) as error:
        p.error(str(error))

if __name__ == '__main__':
    main()
