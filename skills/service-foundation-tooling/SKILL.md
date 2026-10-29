---
name: service-foundation-tooling
description: Maintain the template validation, skill catalog checks and safe service-skill registration CLI.
---

# Foundation tooling

Owner: theharithsa. Scope: repository-local Python standard-library tooling; no network service, application runtime or cloud deployment. See [catalog metadata](../catalog.json) and [continuation](continuation.md).

## Source and contracts

- `scripts/check_foundation.py`: foundation/evidence structure and optional discovery gate, then catalog validation. Errors exit 1. `--ready` intentionally fails for an unconfigured template.
- `scripts/skill_catalog.py`: validates catalog schemaVersion 1, unique identities, internal paths, skill inventory, declared service mappings, active service prerequisites and dependency graphs. It never executes catalog commands. [Metadata contract](../README.md).
- `scripts/add_service_skill.py`: registers a planned service skill and continuation file. Dry run creates nothing; preflight rejects invalid/duplicate identities, unsafe paths and existing output. Exclusive catalog lock coordinates generators; generation rolls back its new directory on failure; catalog replacement is atomic. Concurrent manual edits must be avoided while generating.
- `.agents/skills/app-launchpad/scripts/bootstrap.py`: planning-only fallback, with collision preflight, exclusive output creation and rollback. It does not copy this whole catalog; GitHub template adoption remains pending on that fallback.

## Design and invariants

Preserve existing work and unknown decisions. Do not create application code, dependencies, credentials or cloud resources. Every actual service/module must be declared; automatic inference of missing services and semantic freshness is outside the validator's scope. Dependency cycles, uncataloged SKILL.md files and missing declared service skills fail. Planned service source paths may not exist; active service source/entrypoints must exist and owner/test commands must be populated.

The current catalog is schemaVersion 1. Keep readers, generator, tests, contract docs and sample records compatible when changing it. Values such as lastReviewedRevision are review pointers, not proof of passing tests or deployment.

## Verification and maintenance

Run `python3 scripts/check_foundation.py` and `python3 -m unittest discover -s tests -v`. Tests use isolated temporary repositories and synthetic metadata. Validate changed SKILL.md frontmatter with an available skill validator; do not add a runtime package dependency solely for it. Foundation CI executes structure checks and tests; add targeted negative-path cases for altered generator/validator behavior.

## Release, operation and recovery

Delivery is through an issue-linked PR to the template's main branch after current-head checks. There is no provider deploy command, database migration or runtime rollback. Consumers adopt updated template files through reviewed PRs. Revert a defective template change through a PR; preserve consumer-specific decisions.

A stale `skills/.catalog.lock` after process termination requires checking for an active generator and reviewing the catalog/generated files before removing it. Do not blindly remove a live lock. Preserve external edits if `.catalog.next` exists; inspect it before retrying. Secrets, customer data and raw logs never belong in the catalog or skills.

## Observability and continuation

Runtime RUM/OTel/business events are inapplicable to these local tooling commands. GitHub Actions records actual check execution; no Dynatrace lifecycle observer is configured. Report those limits explicitly. Maintain [continuation](continuation.md), linked issue/PR and exact check revision; never describe template CI as application certification.
