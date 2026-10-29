---
name: project-implementation
description: Implement or enhance application code using the affected service skills and verified contracts.
---

# Project Implementation

Read AGENTS.md, the catalog, relevant service skills and continuation records before edits. Inspect source, dirty work, linked issue and current PR/check state; verify handoff claims against Git and code.

Register every new deployable service or independently maintained module with `scripts/add_service_skill.py` before implementing it. Scope follows the actual architecture: a frontend or a single static site can be one service; do not manufacture microservices. Record real source paths, entrypoints, owner, contracts and dependencies as they become known.

Implement one accepted vertical slice using the selected stack and shared server-side policy. Add meaningful tests and approved telemetry with real outcomes. Update the service skill, catalog metadata and continuation record in the same PR as behavior/contract changes. Complete relevant [build requirements](../../.agents/skills/app-launchpad/references/build.md).
