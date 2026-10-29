# Getting started

1. Read [AGENTS.md](../AGENTS.md), the [catalog](../skills/README.md) and the task's [policy owner](policy-map.md).
2. Generate from the confirmed GitHub template destination; the partial bootstrap no longer exists. Record source TEMPLATE_VERSION and exact source commit in `project.json`.
3. Complete the brief and [decisions](decisions.md). See [synthetic examples](../examples/README.md) for shape, never actual facts. Run `sh scripts/check.sh` and the `--ready` discovery gate documented in README.
4. Review licensing: root LICENSE covers inherited template material; keep that notice and all third-party notices. Choose the new application's license separately before distribution; `project.json.decisions.license` starts needs-user-input. An app-specific root license must not discard inherited notices.
5. Replace `.github/CODEOWNERS` with the confirmed owner/team for the new repository and review inherited tooling ownership in the catalog. Template author attribution and current maintenance ownership are separate.
6. Register each real service/module with `scripts/add_service_skill.py`, populate its skill from actual source, and maintain the [inventory](services.md). The [service contract](../.agents/skills/app-launchpad/references/services.md) owns upkeep and continuation requirements.
7. Select current stack/runtime versions from official docs, scaffold the actual app and lock dependencies. Python in this template is tooling, not a selected application backend.
8. Follow [build](../.agents/skills/app-launchpad/references/build.md), [tests](../.agents/skills/app-launchpad/references/testing.md), [Dynatrace](../.agents/skills/app-launchpad/references/observability.md), [illustration](illustrations.md) and [delivery](delivery.md) procedures for the accepted vertical slice.
9. Repository protection, provider configuration and telemetry destinations require their own authorized setup. Use the [opt-in ruleset procedure](repository-ruleset.md); it never runs on generation or in CI.
