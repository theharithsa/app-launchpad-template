---
name: app-launchpad
description: Build or enhance apps using the project template, issue-linked delivery and Dynatrace observability.
metadata:
  version: "1.13.0"
---

# App Launchpad

## Start or resume

1. Inspect AGENTS.md, Git status/remotes, handoff and current issue/PR; read affected service skills.
2. Apply [safety and decision authority](references/safety.md). Read [discovery](references/discovery.md) before dependent implementation.
3. For new repositories use [app-launchpad-template](https://github.com/theharithsa/app-launchpad-template) by default after confirming owner/name/visibility and empty local destination. Inspect its README/revision, generate through GitHub, and record source version/commit in project metadata. Apply [automatic branch cleanup](references/github-release.md#automatic-branch-cleanup) during authorized repository setup.
4. For existing apps adopt applicable files through a reviewed PR, preserving project instructions/history. GitHub templates copy files, not settings or later updates; bring upgrades through PRs. Explicit user-selected alternatives take precedence.
5. If GitHub is unavailable or local-only, continue authorized discovery and record template adoption pending. The partial planning bootstrap has been removed; never claim equivalent adoption from incomplete copies.
6. Select and link the repository's [GitHub Project](references/github-projects.md). Set up its roadmap and Kanban views, classify issues, and verify milestone and Project membership for issues and PRs, including Dependabot.
7. Select the task's [owning references](#task-routing). In template projects read `skills/catalog.json`, use the documented discovery gate, then build one real vertical slice with actual stack-specific checks.
8. Apply [completion](references/completion.md); use existing authorization to finish delivery or report the concrete remaining dependency.

## Task routing

| Task | Owner |
| --- | --- |
| Product, stack, architecture decisions | [Discovery](references/discovery.md) |
| UI, API, auth, data and dependencies | [Build](references/build.md) |
| Test suites and real execution | [Testing](references/testing.md) |
| Dynatrace RUM/OTel/events/SDLC | [Observability](references/observability.md) |
| GitHub Project, issue types, roadmap, Kanban, milestones and sprints | [Project tracking](references/github-projects.md) |
| Issues, PRs, checks, merge, release, rollback | [Delivery](references/github-release.md) |
| Public README, launch media, and GitHub Pages | [Product launch](references/product-launch.md) |
| Trust, secrets, cost, authorization, delegation | [Safety](references/safety.md) |
| Evidence states and signal authority | [Evidence](references/evidence.md) |
| Per-service skills and continuation | [Services](references/services.md) |
| Useful Ian/Xiaohei images in docs/sites/app content | [Illustrations](references/illustrations.md) |

The stack is project-specific. Use the bundled [dt-obs skill](../dt-obs/SKILL.md) for Dynatrace instrumentation and Thoth for GitHub Actions telemetry. Verify current official runtime and provider documentation before choosing APIs, versions or scopes.
