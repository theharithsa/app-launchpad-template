# Delivery and deployment

Every actionable change needs a reusable GitHub issue and linked PR. Use `Closes #N` only for full resolution into the default branch. Verify current-head checks, required approvals, remote merge SHA and issue resolution. Preserve failed, cancelled, skipped, partial and reopened states.

Foundation CI is a scaffolding check. Configure required application checks and branch/ruleset protection for each project under authorized repository settings. A template does not transfer those settings. Keep pull-request jobs free of production and ingestion secrets. Pin third-party actions to reviewed full SHAs; Dependabot proposes updates. No `pull_request_target` execution of untrusted code.

Select hosting separately. Before creating a deployment workflow, record provider, account/project, region, cost, environment, deployment trigger, applicable authorization, secret names and OIDC method, actual build/test commands, immutable artifact identity, migration ordering, postdeploy health/version checks and rollback. The template cannot deploy until this work is implemented. No selected provider is implied by GitHub hosting.

Record source merge, release publication, deployment, transport acceptance, tenant searchability, and native RUM linkage separately. An HTTP 202 is acceptance evidence only. Retry failed telemetry reporting without repeating successful deployment.

See [complete GitHub/release procedure](../.agents/skills/app-launchpad/references/github-release.md), [observability contract](../.agents/skills/app-launchpad/references/observability.md), and `docs/release-plan.md`.
