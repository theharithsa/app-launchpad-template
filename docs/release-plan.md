# Release impact and verification plan

Status: pending decisions and implementation. This is not deployment authorization.

Record the maintainer model and [delivery path](../.agents/skills/app-launchpad/references/github-release.md#choose-the-delivery-path).
When the owner chooses a weekly cadence, record the window and time zone,
version policy, milestone, candidate revision and urgent-patch path.
See [weekly release cadence](../.agents/skills/app-launchpad/references/github-release.md#weekly-production-releases-with-frequent-staging).

Record issue URL/acceptance criteria, verified issue-to-PR relationship and resolution state, version, source revision, PR/checked head/merge SHA, workflow/run/attempt, target environment and authorized scope. List affected UI, modules/contracts/policies, settings, data/indexes/migrations, secret bindings, telemetry, docs/screenshots and rollback consequences. Define executable predeploy gates and separate postdeploy checks for the chosen stack.

Record the applicable [risk-based checks](../.agents/skills/app-launchpad/references/testing.md#checks-by-change-risk),
approval and release/restore evidence. Record explicit exclusions for layers the project does not use.
After an app deployment, verify version/SHA, service revisions, public/protected routes, and docs separately. For a template release, verify the published tag, commit and release page. For enabled telemetry, record transport and tenant evidence separately. Do not write customer data for verification without authorization.

Track SDLC events from intake/development through review/checks/merge, release/deployment, runtime verification and rollback. Document source authority, stable IDs, safe fields, delivery/recovery, and source-to-tenant proof separately from application signal evidence.
