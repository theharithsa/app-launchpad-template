---
name: project-deployment
description: Prepare, execute when authorized, and verify project-specific releases, deployments and rollback.
---

# Project Deployment

Read the affected service skills, release plan, decisions and [delivery procedure](../../.agents/skills/app-launchpad/references/github-release.md). Confirm actual provider/project/environment mapping, permissions, cost, secrets method, commands and deployment trigger; resolve unknowns before dependent actions.

Prepare the linked PR and current-head checks, immutable artifact identity, dependency/migration ordering and rollback. Use existing scoped merge/deployment authorization; missing authorization is resolved only with a concrete reviewable release. Never bypass failing checks or publish from an untested revision.

Record merge, release, deployment, health/version checks and rollback independently in each affected service continuation record. Keep secret values out of these files. If a provider is unconfigured, report blocked/not-run rather than providing invented deployment commands.
