---
name: app-launchpad
description: Build, improve, or adopt a delivery workflow for an app using App Launchpad, issue-linked PRs, risk-based checks, and Dynatrace observability.
metadata:
  version: "1.14.0"
---

# App Launchpad

## Start or resume

1. Inspect AGENTS.md, Git status/remotes, the handoff and current issue/PR. Apply [safety and decision authority](references/safety.md) and use [discovery](references/discovery.md) for missing decisions.
2. For a new repository, confirm the owner, name, visibility and empty destination. Generate from [app-launchpad-template](https://github.com/theharithsa/app-launchpad-template) by default and record the source version and commit. For an existing repository, follow [adoption](references/github-release.md#adopt-or-audit-the-workflow). Record pending adoption when GitHub is unavailable or the work is local-only.
3. Follow the [delivery path that matches the project](references/github-release.md#choose-the-delivery-path). Use issue-linked PRs and checks sized to the risk. Use the [selected GitHub Project](references/github-projects.md) when the project tracks work there.
4. Select the relevant references below. In template projects, read `skills/catalog.json` and the affected service skills. For new app work, prove an end-to-end slice with real checks for the chosen stack.
5. Use [completion](references/completion.md) to record results and remaining dependencies.

## Task routing

| Task | Owner |
| --- | --- |
| Product, stack, architecture decisions | [Discovery](references/discovery.md) |
| UI, API, auth, data and dependencies | [Build](references/build.md) |
| Test suites and real execution | [Testing](references/testing.md) |
| Dynatrace RUM/OTel/events/SDLC | [Observability](references/observability.md) |
| GitHub Project, issue types, roadmap, Kanban, milestones and sprints | [Project tracking](references/github-projects.md) |
| Solo or team delivery, adoption, PRs, release cadence and recovery | [Delivery](references/github-release.md) |
| PR documentation, public guides, launch media, and GitHub Pages | [Documentation and launch](references/product-launch.md) |
| Trust, secrets, cost, authorization, delegation | [Safety](references/safety.md) |
| Evidence states and signal authority | [Evidence](references/evidence.md) |
| Per-service skills and continuation | [Services](references/services.md) |
| Useful Ian/Xiaohei images in docs/sites/app content | [Illustrations](references/illustrations.md) |
