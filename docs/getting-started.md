# Getting started

## Day 0

1. Read [AGENTS.md](../AGENTS.md), the [catalog](../skills/README.md) and the task's [policy owner](policy-map.md).
2. Generate the confirmed GitHub repository from the template, then complete the reset below.
3. Complete the [project brief](project-brief.md) and [decisions](decisions.md). Use the [synthetic examples](../examples/README.md) for structure. Run `sh scripts/check.sh` and use the [discovery gate](../README.md) before scaffolding the app.
4. If the project uses GitHub Projects, follow the [Project setup and permissions check](../.agents/skills/app-launchpad/references/github-projects.md). For an issue-only workflow, use repository issues and delivery milestones and record the chosen workflow in [delivery](delivery.md).
## First 30 minutes after generation

| File or setting | Action |
| --- | --- |
| `project.json` | Record the app name, the source template's version and exact commit, and the app's own decisions. Leave unresolved decisions marked needs-user-input. |
| `.github/CODEOWNERS` | Add the confirmed owner or team for the new repository. |
| `docs/decisions.md` and `docs/delivery.md` | Record only this app's decisions, delivery path, owners and optional Project view links. |
| `skills/catalog.json` and the foundation-tooling continuation | Keep inherited tooling paths and commands. Record a real owner, verification and source revision before activating that inventory entry. |
| `qa/evidence.json` | Record checks for the new project. Start from the inherited pending record until there is evidence. |
| `site/` and `docs/public-guides.json` | Replace the template's product copy and examples with approved project facts before publication. |
| `LICENSE` and third-party notices | Retain inherited license notices. Decide the app's license before distributing it. |
| `docs/maintaining-the-template.md` | Remove this maintainer guide from a generated app as part of its documentation setup. |
| GitHub settings | Check the default branch, milestone/Project setup, labels, ruleset and workflow permissions on the new repository. These settings are configured separately. |

For a known source tag, resolve its commit with the GitHub CLI and copy the
40-character output into `project.json.template.revision`. Set
`project.json.template.version` to the version from that same tag.

```sh
gh api repos/theharithsa/app-launchpad-template/commits/v1.14.3 --jq .sha
```

Replace the example tag with the one used for generation. The new repository's
initial commit has its own SHA. If the generator used an untagged template
revision, record the exact source SHA supplied by the generator.

## Build and deliver

1. Register each actual service with `scripts/add_service_skill.py` and maintain the [service inventory](services.md). Select approved runtime and dependency versions and build the first vertical slice.
2. Choose the [delivery path](delivery.md). Follow the [release walkthrough](promotion-walkthrough.md) to track a staged app or a package from intake through verification. Customize the [public guides and site](../.agents/skills/app-launchpad/references/product-launch.md) before enabling Pages.
3. Confirm the scope and authorization for repository protection, providers and telemetry. The [opt-in ruleset procedure](repository-ruleset.md) is separate from generation.
