# App Launchpad Template

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

Follow [getting started](docs/getting-started.md). Ask Codex to read `AGENTS.md` and apply the bundled app-launchpad skill. The template provides planning and workflow files; choose and build the actual application for its requirements.

## What is included

- Self-contained app-launchpad skill in `.agents/skills/`, plus project agent instructions.
- Project brief, decision, coverage, release-impact and evidence records.
- GitHub change/bug issue forms, PR template and foundation CI.
- Python standard-library validation and bootstrap safety tests.
- Testing, release, security, and Dynatrace adoption procedures with explicit pending states.

No application framework, hosting provider, auth, database, tenant, ingestion credentials, or production deployment has been selected. No app tests or telemetry are claimed by the template's CI.

## Maintenance and scope

GitHub generates a new repository from the template's files; later template changes do not automatically update generated projects. Record the source template revision in `project.json` when adopting it. Bring later changes through an issue and reviewed PR; preserve project-specific choices and existing instructions.

Repository protection, required checks, environments, secrets, webhooks and provider projects require separate configuration in each new repository. Instructions and CI do not enforce branch protection by themselves. Read [delivery](docs/delivery.md).

The source is public. A reuse license has not been selected; visibility alone is not an open-source license grant. Resolve licensing before distributing a generated product.

[GitHub template documentation](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository)
