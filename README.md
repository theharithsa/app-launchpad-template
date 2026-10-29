# App Launchpad Template

Template version: **1.09.0** · [versioning policy](docs/versioning.md)

A stack-neutral foundation for building apps with explicit decisions, issue-linked PRs, meaningful tests, and separate source, deployment, and observability evidence.

## Create a project

Use **Use this template → Create a new repository**, or run the following after confirming the new project's owner, name, and visibility:

```sh
gh repo create OWNER/PROJECT --template theharithsa/app-launchpad-template --private --clone
cd PROJECT
python3 scripts/check_foundation.py
python3 -m unittest discover -s tests -v
```

Choose `--public` only when approved. Work on an issue-linked feature branch. Fill in `project.json`, `docs/project-brief.md`, and `docs/decisions.md` with approved choices, then run:

```sh
python3 scripts/check_foundation.py --ready
```

Start agents at the [skills catalog](skills/README.md) and follow [getting started](docs/getting-started.md). Ask Codex to read `AGENTS.md` and apply the bundled app-launchpad skill. The template provides planning and workflow files; choose and build the actual application for its requirements.

## What is included

- Visible [`skills/` catalog](skills/README.md) with design, implementation, testing, deployment, observability and handoff skills.
- Machine-readable skill/service metadata, per-service continuation records, a safe service-skill generator and CI validation.
- Self-contained app-launchpad skill in `.agents/skills/`, plus project agent instructions.
- Project brief, decision, coverage, release-impact and evidence records.
- GitHub change/bug issue forms, PR template and foundation CI.
- Python standard-library validation and bootstrap safety tests.
- Testing, release, security, and Dynatrace adoption procedures with explicit pending states.

No application framework, hosting provider, auth, database, tenant, ingestion credentials, or production deployment has been selected. No app tests or telemetry are claimed by the template's CI.

## Illustrations and documentation

Use the bundled [Ian Xiaohei Illustrations skill](skills/ian-xiaohei-illustrations/SKILL.md) by Ian wherever an explanatory image materially improves docs, websites, onboarding or application content. [Design](skills/project-design/SKILL.md) and [documentation](skills/project-documentation/SKILL.md) skills route agents to it automatically through project instructions. Prefer the smallest useful set; preserve product branding, accurate diagrams and accessible text alternatives. See [illustration policy and attribution](docs/illustrations.md).

## Template version and upgrades

Current template label: **1.09.0**, recorded in [TEMPLATE_VERSION](TEMPLATE_VERSION), [project metadata](project.json) and [template changelog](docs/template-changelog.md). It is separate from application/API versions and from the bundled Ian skill's upstream version. The exact label is preserved as requested; its leading zero means it is not strict SemVer. See [version policy, checks and release procedure](docs/versioning.md).

## Maintenance and scope

GitHub generates a new repository from the template's files; later template changes do not automatically update generated projects. Record the source template revision in `project.json` when adopting it. Bring later changes through an issue and reviewed PR; preserve project-specific choices and existing instructions.

Repository protection, required checks, environments, secrets, webhooks and provider projects require separate configuration in each new repository. Instructions and CI do not enforce branch protection by themselves. Read [delivery](docs/delivery.md).

The source is public. A reuse license for the template itself has not been selected; the bundled Ian skill retains its own MIT license and attribution. Visibility alone is not an open-source license grant. Resolve licensing before distributing a generated product.

[GitHub template documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
