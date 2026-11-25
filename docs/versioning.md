# Template adoption and versioning

`TEMPLATE_VERSION` records the inherited template version. Keep the source
commit in `project.json.template.revision` and retain the application’s own
release numbering. Published template versions follow [SemVer](https://semver.org/).

## Consumer migration

- Use the [worked upgrade](upgrading.md) to compare tags and identify the relevant changes.
- Adopt the chosen files through a reviewed PR. Keep application decisions, ownership, evidence and service data in the app.
- Record an exact source commit for a full upgrade. For a selective adoption, record the upstream revision and included paths in [delivery](delivery.md).
- Keep the application changelog in `CHANGELOG.md` and the upstream template history in [template-changelog.md](template-changelog.md).

## Sync skills across devices

Use the [canonical template repository](https://github.com/theharithsa/app-launchpad-template)
and one checked release tag. Clone it, fetch its tags, then run
`git switch --detach v<VERSION>` with that release version.

| Host | User-wide destination |
| --- | --- |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |

Compare existing local changes before updating. Copy the full canonical
`app-launchpad` and `dt-obs` folders from `.agents/skills/` as siblings in the
chosen destination. For a repo-scoped Claude Code skill, the checked
`.claude/skills/` entries point to those canonical folders. Confirm both
versions and open a new session. [Claude Code skill discovery](https://code.claude.com/docs/en/skills)
