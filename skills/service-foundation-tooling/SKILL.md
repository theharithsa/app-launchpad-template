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
| `scripts/check_docs_impact.py` | PR event/body documentation decision; visible Updated/No change explanation required |
| `scripts/build_public_docs.py` | Curated site build, safe output and local HTML link/anchor validation |
| `scripts/add_service_skill.py` | Planned skill/continuation/catalog registration; no application source creation |
| `scripts/repository_ruleset.py` | Local preview by default; explicit authorized apply and read-back verification |
| `scripts/check.sh` | Shared CI/local entrypoint: foundation, links, docs decision/build and tests; `PYTHON` selects one executable; stops at first error |
| `.github/workflows/foundation.yml` | Linux/Windows checks with strict encoding; required `foundation` aggregate fails unless both succeed |
| `.github/workflows/product-pages.yml` | Read-only curated docs packaging, followed by default-branch Pages publication when enabled |
| `.github/workflows/project-issue-types.yml` | Metadata-only issue type reconciliation; personal-repo label fallback |
| `.github/workflows/project-milestones.yml` | Metadata-only milestone assignment/reconciliation for issues and PRs |

## Registration and recovery

- Generator preflight rejects unsafe paths, duplicate identities, symlinks and existing output. Exclusive catalog lock coordinates generators; final replacement is atomic; failed generation removes only its newly created directory.
- Avoid concurrent manual catalog edits. After process interruption, inspect active processes, catalog and generated files before removing a stale `.catalog.lock` or `.catalog.next`; never discard external work blindly.
- Planned source directories may be absent. Active-service schema/domain checks require owner, real source/entrypoint paths and test commands. CI cannot infer undeclared services or semantic freshness.
- Path guards reject POSIX and Windows roots/drives on either OS. Text I/O is UTF-8 with LF output. Missing `lastReviewedRevision` commits warn in a Git checkout; fetch missing history or refresh the record after review. Archives without history still validate.

## Verification and delivery

- Run `sh scripts/check.sh`. Tests use synthetic temporary repositories, metadata failures, schema parity, generator failure paths, links, entrypoint behavior and ruleset previews/mocked apply.
- Follow [delivery](../../docs/delivery.md) for source changes and [ruleset procedure](../../docs/repository-ruleset.md) for settings. Consumer upgrades arrive through reviewed PRs; there is no runtime deployment/database rollback for these local commands.
- Template version/provenance follows [versioning](../../docs/versioning.md); app and upstream skill versions are separate. The partial bootstrap was removed in this baseline.
- Documentation routing anchors are exercised by the contract suite. Illustration provenance and the owner-approved upstream-only calibration policy are recorded in [the notice](../ian-xiaohei-illustrations/NOTICE.md); removed PNGs are not part of generated repositories.
- Runtime RUM/OTel/business events are inapplicable. GitHub Actions supplies check execution; no live Dynatrace observer/tenant integration is configured. Apply the [evidence contract](../../.agents/skills/app-launchpad/references/evidence.md) to handoff and reporting.
