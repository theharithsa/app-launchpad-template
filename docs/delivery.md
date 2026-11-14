# Delivery

- [Issue-to-merge and release procedure](../.agents/skills/app-launchpad/references/github-release.md)
- [Authorization and safety](../.agents/skills/app-launchpad/references/safety.md)
- [Evidence states](../.agents/skills/app-launchpad/references/evidence.md)
- [Baseline repository ruleset](repository-ruleset.md)
- [Template versions and consumer upgrades](versioning.md)

## App Launchpad template maintenance

Track changes to this template in the [App Launchpad Template Project](https://github.com/users/theharithsa/projects/3). Use its [Milestones](https://github.com/users/theharithsa/projects/3/views/7), [Roadmap](https://github.com/users/theharithsa/projects/3/views/4), and [Kanban](https://github.com/users/theharithsa/projects/3/views/8) views. When generating an application from the template, record that application's own Project and view links here.

The template uses the [delivery path without pre-production](../.agents/skills/app-launchpad/references/github-release.md#choose-the-delivery-path). Track the issue and target milestone, implement on a short-lived branch, then open one PR to protected `main`. GitHub Actions runs `foundation`. After the authorized merge, publish the version tag and release and verify that they point to the merge commit. The template is a versioned GitHub release. The optional Pages starter has its own publishing workflow when enabled.
