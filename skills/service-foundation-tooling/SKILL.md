---
name: service-foundation-tooling
description: Maintain the foundation validators, service registration and opt-in ruleset tooling.
---

# Foundation tooling

Owner: theharithsa. Scope: Python standard-library repository tooling; no application runtime/cloud deployment. Read [catalog](../catalog.json), [continuation](continuation.md) and the [service contract](../../.agents/skills/app-launchpad/references/services.md).

| Entry/module | Contract and extension point |
| --- | --- |
| `scripts/check_foundation.py` | Structure, SemVer/provenance and optional discovery gate; text or JSON diagnostics; nonzero on failure |
| `scripts/schema_validation.py`, `contracts.py` | [Schemas](../../schemas/README.md) and required/status constants; synchronize schema/validator/test changes |
| `scripts/skill_catalog.py` | Accumulated sorted path, inventory and graph diagnostics; reads metadata without executing commands |
| `scripts/check_links.py` | Local Markdown links in regular/hidden docs; no network; fenced examples excluded |
| `scripts/add_service_skill.py` | Planned skill/continuation/catalog registration; no application source creation |
| `scripts/repository_ruleset.py` | Local preview by default; explicit authorized apply and read-back verification |
| `scripts/check.sh` | The shared CI/local/catalog entrypoint: foundation, links, tests; fails before later steps after error |

## Registration and recovery

- Generator preflight rejects unsafe paths, duplicate identities, symlinks and existing output. Exclusive catalog lock coordinates generators; final replacement is atomic; failed generation removes only its newly created directory.
- Avoid concurrent manual catalog edits. After process interruption, inspect active processes, catalog and generated files before removing a stale `.catalog.lock` or `.catalog.next`; never discard external work blindly.
- Planned source directories may be absent. Active-service schema/domain checks require owner, real source/entrypoint paths and test commands. CI cannot infer undeclared services or semantic freshness.

## Verification and delivery

- Run `sh scripts/check.sh`. Tests use synthetic temporary repositories, metadata failures, schema parity, generator failure paths, links, entrypoint behavior and ruleset previews/mocked apply.
- Follow [delivery](../../docs/delivery.md) for source changes and [ruleset procedure](../../docs/repository-ruleset.md) for settings. Consumer upgrades arrive through reviewed PRs; there is no runtime deployment/database rollback for these local commands.
- Template version/provenance follows [versioning](../../docs/versioning.md); app and upstream skill versions are separate. The partial bootstrap was removed in this baseline.
- Runtime RUM/OTel/business events are inapplicable. GitHub Actions supplies check execution; no live Dynatrace observer/tenant integration is configured. Apply the [evidence contract](../../.agents/skills/app-launchpad/references/evidence.md) to handoff and reporting.
