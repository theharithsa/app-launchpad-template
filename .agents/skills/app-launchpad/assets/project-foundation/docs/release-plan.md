# Release impact and verification plan

Status: pending decisions and implementation. This is not deployment authorization.

Record issue URL/acceptance criteria, verified issue-to-PR relationship and resolution state, version, source revision, PR/checked head/merge SHA, workflow/run/attempt, target environment and authorized scope. List affected UI, modules/contracts/policies, settings, data/indexes/migrations, secret bindings, telemetry, docs/screenshots and rollback consequences. Define executable predeploy gates and separate postdeploy checks for the chosen stack.

Postdeploy evidence must include exact version/SHA/service revisions; public/protected-route checks; independent docs checks; per-signal transport and partial rejection counts; tenant queries for events/logs/traces/actual metric samples; actual native RUM linkage status; failures/limits. No customer writes without explicit authorization. Never label these pending checks passed.

Track SDLC events from intake/development through review/checks/merge, release/deployment, runtime verification and rollback. Document source authority, stable IDs, safe fields, delivery/recovery, and source-to-tenant proof separately from application signal evidence.
