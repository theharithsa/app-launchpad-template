# Adopt the foundation

1. Confirm the product, audience, first journey, scope, GitHub identity/visibility and access. Create or reuse the issue before implementation. Preserve any existing work.
2. Record approved choices in the brief and decision log. Fill `project.json` with a name and a source template commit SHA from GitHub. Each decision has status, value and approval source. `not-applicable` requires a reason in value and an accountable approval source, for example no backend telemetry on a static site. Keep unresolved choices as `needs-user-input`.
3. Run the foundation validator and safety tests from README. The optional `--ready` flag fails until discovery decisions and provenance are recorded; a pass does not prove application or release readiness.
4. Select framework/runtime versions from current official docs, scaffold the actual app in this repository using its conventions, and add the lockfile. Python here is only tooling; it is not a backend choice.
5. Implement a real vertical slice. Add actual domain, contract, integration and browser tests as applicable. Add their commands and CI jobs, preserving failure/skipped/blocked states. Record exclusions for irrelevant layers.
6. Resolve hosting/project/region/cost, environments, secure secret configuration, deployment trigger, approval and rollback before creating cloud resources. Implement provider-specific CI for the tested immutable artifact. The template intentionally ships no deployment workflow.
7. Configure approved Dynatrace instrumentation and lifecycle observation using the bundled skill references. Do not copy another project's identities or emit invented success events. No active telemetry integration is included.
8. Open the linked PR, run current-head checks, satisfy repository review policy, merge when authorized, and verify remote merge/issue closure. Deploy only under the applicable authorization and record exact release evidence.

The bundled `scripts/bootstrap.py` copies planning files only into a confirmed target and refuses collisions. It is optional; generated template repositories already contain those files. Never run it over an existing app to overwrite its instructions.

## Service skills before code

Read `skills/catalog.json` and the relevant shared workflows. Register each actual service or independently maintained module with `scripts/add_service_skill.py` before implementing it. Complete its generated skill, metadata and continuation from inspected code; set it active when implemented. See [skills catalog](../skills/README.md) and [service inventory](services.md). Update those records in every relevant PR so future agents can resume from verified context.
