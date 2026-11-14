# App Launchpad Template

Template version: **1.14.0** · [changelog](docs/template-changelog.md) · [MIT license](LICENSE)

See the [production documentation checklist](docs/release-plan.md#production-documentation-review). [SalesDrone](https://github.com/theharithsa/SalesDrone) is an existing app that uses App Launchpad delivery practices.

A stack-neutral, **Dynatrace-opinionated** foundation for building and enhancing apps. Choose each product's stack and hosting deliberately; Dynatrace is the chosen observability platform. No tenant or application deployment is preconfigured.

## Create a project

Confirm the new owner, name, visibility and empty local destination, then use **Use this template → Create a new repository**, or:

```sh
gh repo create OWNER/PROJECT --template theharithsa/app-launchpad-template --private --clone
cd PROJECT
sh scripts/check.sh
```

Use public visibility only when approved. Follow [getting started](docs/getting-started.md): record source template version/revision, complete discovery decisions and register each actual service before implementation. Then run the discovery gate:

```sh
python3 scripts/check_foundation.py --ready --json
```

The gate checks decisions, not application/release readiness. Add real stack-specific build, test and deployment checks for the selected app.

## What is included

- [Agent entrypoint](AGENTS.md), tool-specific pointer files and [policy ownership map](docs/policy-map.md).
- [Visible skills catalog](skills/README.md): design, implementation, tests, deployment, Dynatrace observability, documentation and handoff.
- Per-service skills/continuation, safe registration tooling and [JSON Schemas](schemas/README.md).
- [Synthetic worked examples](examples/README.md) for decisions, execution evidence, continuation and a service skill.
- Issue/agent-brief forms, PR checklist, CI, CODEOWNERS and an opt-in [repository ruleset procedure](docs/repository-ruleset.md).
- [Ian Xiaohei Illustrations](skills/ian-xiaohei-illustrations/SKILL.md) for useful explanatory images under the [illustration policy](docs/illustrations.md).

## Prepare a public product launch

Use the [product README example](examples/product-readme.md), [contribution guide](CONTRIBUTING.md), [security guide](SECURITY.md), and [landing page starter](site/index.html). Follow the [launch procedure](.agents/skills/app-launchpad/references/product-launch.md) to capture real screenshots with synthetic data, make a short `/brag` video, and publish through GitHub Pages.

Build the starter and its five public guides with `python3 scripts/build_public_docs.py --output dist/public-docs` (use an empty output directory). Preview with `python3 -m http.server 8080 --directory dist/public-docs`. Configure GitHub Pages in the generated repository when the content is ready. See the [documentation workflow](.agents/skills/app-launchpad/references/product-launch.md#documentation-on-every-pr).

## Checks and maintenance

Run **`sh scripts/check.sh`** locally and in CI: metadata validation, local Markdown links and safety/contract tests. For machine-readable diagnostics use `python3 scripts/check_foundation.py --json`; `--ready` adds discovery checks. Foundation success does not certify an application's behavior, deployment or tenant signals.

GitHub template generation copies files, not repository settings or future updates. Adopt upgrades through reviewed PRs and retain project-specific choices. See [versioning and migration](docs/versioning.md), [delivery](docs/delivery.md) and [service inventory](docs/services.md). The partial planning bootstrap was removed; use GitHub template generation or record adoption pending.

## Licensing

The template is MIT-licensed by Vishruth Harithsa. Bundled Ian Xiaohei Illustrations retains its own [MIT license](skills/ian-xiaohei-illustrations/LICENSE) and [attribution](skills/ian-xiaohei-illustrations/NOTICE.md).

A generated application's license is a separate `needs-user-input` decision. Preserve the template and third-party copyright/license notices for inherited material; when selecting the app's license, retain those notices (for example under `LICENSES/`) and document the app's chosen terms separately. Copying the template does not record an approved license choice for new application code.

[GitHub template documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
