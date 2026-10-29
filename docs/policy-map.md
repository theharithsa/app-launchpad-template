# Policy ownership map

Read only the owner relevant to the task; entrypoints and workflow skills route here instead of carrying alternate policies.

| Rule or contract | Single owner |
| --- | --- |
| Authority, decisions to ask about, local-only holds, existing work, secrets, trust, delegation, collaboration tone | [Safety](../.agents/skills/app-launchpad/references/safety.md) |
| Product and architecture discovery | [Discovery](../.agents/skills/app-launchpad/references/discovery.md) |
| Issues, PR/check/review, merge, release/deployment, retry and rollback | [Delivery](../.agents/skills/app-launchpad/references/github-release.md) |
| Shared evidence stages and source authority | [Evidence](../.agents/skills/app-launchpad/references/evidence.md) |
| API/policy/data, UI and settings implementation | [Build](../.agents/skills/app-launchpad/references/build.md) |
| Actual test coverage and case/result handling | [Testing](../.agents/skills/app-launchpad/references/testing.md) |
| Dynatrace signal payload, delivery and verification mechanics | [Observability](../.agents/skills/app-launchpad/references/observability.md) |
| Service skills, ownership and continuation upkeep | [Services](../.agents/skills/app-launchpad/references/services.md) |
| Illustration selection and integration | [Illustrations](../.agents/skills/app-launchpad/references/illustrations.md) |
| Template versions and consumer upgrades | [Versioning](versioning.md) |
| Machine-readable field shapes | [Schemas](../schemas/README.md) |

Technical procedures link to these shared boundaries; they may add task-specific mechanics, not redefine them. The bundled app-launchpad references are canonical so an installed copy remains self-contained. Root docs and tool-specific pointer files route into that same tree.
