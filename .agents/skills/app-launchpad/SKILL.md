---
name: app-launchpad
description: Build a new application or website from an idea through clarified requirements, stack selection, API and UI implementation, test suites, GitHub issue-to-PR-to-merge delivery and Dynatrace lifecycle/runtime observability. Use for greenfield projects, adopting this foundation, or feature/bug/maintenance delivery under this workflow; standalone telemetry investigation belongs to observability query skills.
---

# App Launchpad

Turn the user's idea into a maintainable, testable app and a reviewable release. This is a stack-neutral development skill, not permission to create paid infrastructure, publish, merge, or change tenant access. Preserve authorization already given in the conversation. Never copy another project's cloud IDs, people, domain model, consent, credentials or deployment approval.

## Ask instead of inventing

**For any doubt about requirements, intended behavior, scope, stack, identity, design, integrations, GitHub, hosting, costs, privacy or deployment: ask the user directly. Do not invent special features, business rules, accounts, tenant IDs, secrets, permission scopes, data, branding or success evidence.** Inspect available project context first so the user need not repeat known answers. Recommend options and explain the tradeoff, but an unselected recommendation is not a decision.

Bundle the few questions that unblock the next slice. Continue independent work while answers are pending. Record unresolved items as `needs-user-input`; never silently convert them into defaults. Routine implementation mechanics within an agreed design can use engineering judgment. Distinguish a proposal from an approved requirement. Do not demand an exhaustive questionnaire before doing useful work.

## Default GitHub project template

For new application or website repositories, use [`theharithsa/app-launchpad-template`](https://github.com/theharithsa/app-launchpad-template) by default. This is the user's chosen foundation; still confirm the new repository's owner, name, visibility and local destination. The template is stack-neutral and does not preselect hosting, auth, data storage, tenant, license, costs or deployment approval.

- Inspect the current template README/AGENTS and revision before creating the project. Generate from the GitHub template using the connected tool or `gh repo create OWNER/NAME --template theharithsa/app-launchpad-template` with the confirmed visibility. Clone into the confirmed empty destination; never overwrite an existing application.
- Record the template source revision in `project.json` and complete its brief/decisions. Run the documented foundation validation and safety tests. The `--ready` discovery gate must pass before dependent implementation, with irrelevant decisions explicitly justified. Foundation tests are not application or deployment tests; add real stack-specific checks for the agreed vertical slice.
- Follow the repository's bundled skill and instructions as the project evolves. Existing repositories adopt applicable workflow files through an issue-linked PR without replacement or history reset. Do not create a new repository merely to apply the template to existing work.
- GitHub template generation copies files, not future updates or repository settings. Bring later template changes through reviewed PRs. Configure project-specific checks/protection/environments/secrets, provider deployment and approved telemetry separately.
- If the template is unavailable or an explicit local-only hold applies, record that dependency and continue authorized local discovery. The planning-only bootstrap below is a fallback, not an equivalent completed GitHub template adoption; record the remaining adoption work. An explicit user-selected alternative overrides this default.

## Start or resume

1. Inspect working directory, AGENTS.md, Git status/remote, handover and current app. Preserve uncommitted work. Never scaffold over an existing application.
2. Read [discovery and architecture](references/discovery.md). Establish a minimal product brief, decisions and boundaries; distinguish static site, interactive client and backend system. Ask only missing consequential questions.
3. For a new project, prefer the default GitHub template above. For a documented planning-only fallback, optionally run `python3 <skill-dir>/scripts/bootstrap.py --target <confirmed-project-dir> --name <confirmed-app-name>`. It adds planning/agent/evidence templates only, never application code or dependencies. Inspect `--dry-run` first. Existing output files cause an all-or-nothing refusal. For an existing project, adapt/merge individual templates without replacing instructions.
4. Before implementation, follow [issue-to-merge delivery](references/github-release.md): find or create the GitHub issue for each actionable feature, bug or maintenance request, then carry its identity through branch, linked PR, checks, merge and release. If GitHub access is unavailable or a local-only hold applies, record the issue draft and pending sync explicitly; continue authorized local work. Read [build and UI](references/build.md); implement one real vertical slice using the selected stack. Verify current official provider/runtime documentation and installed versions before choosing versions, auth, CI actions or SDK APIs. Never claim a universal best stack.
5. Read [testing](references/testing.md) and create the actual executable suites alongside the slice. Keep planned, automated and manual coverage distinct.
6. Read [Dynatrace observability](references/observability.md) before instrumentation, and [GitHub and release](references/github-release.md) before repository automation. If `$dt-obs` is available, read its full entrypoint and applicable RUM/OTel/business-event/GitHub/verification references. The bundled guidance remains usable without that installed skill. Discover available GitHub and Dynatrace tools rather than inventing MCP names or tenant endpoints.
7. Apply [completion and handoff](references/completion.md). Keep docs and repository module skills current as behavior changes. Stop only at completion or a concrete dependency needing user input; do not label a blocked integration working.

## Expected project foundation

Adapt to scope; omit irrelevant components with a recorded reason. A static website does not need a database, auth service or cosmetic APIs. A dynamic domain feature needs a versioned API, server-side authorization and observable committed outcomes. Do not generate a monorepo or microservices without a reason.

- Brief, architecture decisions, security/privacy policy, design system and local setup.
- Thin UI over shared domain/policy logic where a backend exists; synthetic demo isolated from production.
- Relevant unit, API/contract, real integration and browser suites, with safe result artifacts.
- GitHub repository details, branch workflow, PR checks, least-privilege release automation and rollback.
- RUM where approved; backend OTel logs/metrics/traces; committed business events where applicable; runtime/export/outbox health; GitHub issue/development/review/check/merge/release/deployment events correlated with runtime signals.
- Release impact plan, changelog, version metadata, user guide and honest pre/post-deployment evidence.
- Visible repository `skills/` with design, implementation, testing, deployment, observability and handoff workflow skills, plus a separate skill and continuation record for every real service or independently maintained module. Maintain `skills/catalog.json` with skill routing/dependencies and service owner, source paths, entrypoints, contracts, actual test commands, state and last reviewed revision. Register services before implementation; update skills/metadata/continuation alongside code and review architecture coverage for undeclared services. Read the catalog and affected continuation records on resume, verifying stored notes against current source/CI. Logical skills do not authorize agent delegation.

## Delivery boundaries

Every actionable feature, bug, refactor, documentation, dependency, security or infrastructure change needs a GitHub issue; reuse the existing issue rather than duplicating it. Link the implementing PR and complete the verified merge when authorized and checks/approvals pass. Always create a PR before merging code into main. Do not direct-push main, force-push shared history or bypass failing checks. Creating this skill or an app locally is not deployment approval. Ask for missing authorization only once there is a concrete reviewable release; never infer approval from time passing. A user-imposed local-only hold remains in effect until explicitly lifted.

Keep credentials out of browser builds, source, artifacts and screenshots. Use secret stores and provider-supported short-lived identity/OIDC where available; do not invent credentials. No production customer edits for verification without explicit authorization. No agents unless the user or applicable instructions authorize delegation.

Report what changed, why, actual checks, release identity and remaining limits. Distinguish local tests, deployed configuration, HTTP ingest acceptance, tenant searchability and native cross-signal navigation. Never fabricate passing tests, screenshots, metrics, traces or business events.
