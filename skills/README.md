# Project skills catalog

Agents: read [catalog.json](catalog.json), choose the relevant workflow and service skills, then read each service's continuation record. Root AGENTS.md makes this catalog the project entrypoint; tools that only auto-discover `.agents/skills` must still follow that routing. The overall app-launchpad skill remains bundled there.

| Work | Skill |
| --- | --- |
| Overall lifecycle | [App Launchpad](../.agents/skills/app-launchpad/SKILL.md) |
| Product/UI/contracts | [Design](project-design/SKILL.md) |
| Code and enhancements | [Implementation](project-implementation/SKILL.md) |
| Test strategy and execution | [Testing](project-testing/SKILL.md) |
| Releases, deployment, rollback | [Deployment](project-deployment/SKILL.md) |
| Runtime and SDLC telemetry | [Observability](project-observability/SKILL.md) |
| Resume and continuation | [Handoff](project-handoff/SKILL.md) |
| Template tooling module | [Foundation tooling](service-foundation-tooling/SKILL.md) |

## Every service has a skill

Register a real deployable service or independently maintained module before implementing it. A single frontend or static site may be the whole application; service skills do not require microservices. The template has no application services yet; its actual foundation tooling module is registered as a concrete maintained example.

```sh
python3 scripts/add_service_skill.py --id SERVICE_ID --source-path ACTUAL_SOURCE_DIRECTORY --dry-run
python3 scripts/add_service_skill.py --id SERVICE_ID --source-path ACTUAL_SOURCE_DIRECTORY
```

Replace the arguments with the agreed architecture's identity and source directory. The command creates `skills/service-SERVICE_ID/SKILL.md`, `continuation.md` and catalog metadata; it creates no application code. It refuses duplicates, unsafe paths, existing output and symlink destinations. A source directory may be planned during registration; it must exist before marking the service active.

Complete the new service skill using inspected source: purpose/boundaries, owner, entrypoints, contracts/policy/data, dependencies, design, actual test commands, deployment/rollback, telemetry and known limits. Update it in the same PR as service changes. Shared workflows above supply the method; each service skill supplies the real application facts.

## Metadata contract (schemaVersion 1)

`skills` entries have unique `id`, `kind` (`workflow` or `service`), repository-relative `path`, routing `description`, and `dependsOn` skill IDs. Paths must stay inside the repository and refer to existing SKILL.md files. Every skill in `skills/` or `.agents/skills/` must be cataloged. Dependency cycles are invalid.

`services` entries have unique `id`, `skillId`, `sourcePaths`, `entrypoints`, `owner`, `status` (`planned`, `active`, `retired`), `dependsOn` service IDs, `contracts`, `testCommands`, `continuation`, and nullable `lastReviewedRevision`. Paths are repository-relative; commands are documented data, never executed by the catalog checker. Owner and revision start null; do not invent people or evidence. Active services require an owner, existing source/entrypoint files, and documented test commands; architectural boundaries and coverage remain a review responsibility. Retired services keep history and migration context.

`continuation.md` records issue/PR, current revision, work state, actual verification, remaining decisions and next steps. Source files and trusted CI/provider evidence take precedence over stale notes. Catalog metadata is routing and ownership information, not a substitute for execution evidence or authorization.

Run `python3 scripts/check_foundation.py` to validate metadata and references. CI cannot discover undeclared services or prove semantic freshness: declare every service in the architecture inventory below and review skill updates in each implementing PR.
