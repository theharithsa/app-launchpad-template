# Maintaining the App Launchpad template

Use this guide in the canonical template repository. In a generated app, use
the app's [delivery guide](delivery.md) and record its own decisions and evidence.
The app can remove this maintainer guide.

## Classify a change

| Change | Version |
| --- | --- |
| Correct an example, broken link or auth scope within an existing workflow | Patch |
| Add a compatible workflow, issue form or required check to the starter | Minor |
| Replace a contract in a way that requires consumers to migrate | Major |

Group related work in the existing release milestone. A candidate can receive
multiple commits under its proposed version. Leave released changelog sections
frozen. Put clarifications in the next candidate's notes. Canonical PR checks
guard the sections already associated with released tags.

## Prepare and ship

1. Use the issue and milestone to define scope. Implement on a branch and open a PR to the protected default branch.
2. For bundled App Launchpad or dt-obs changes, update `TEMPLATE_VERSION`, README, project metadata, App Launchpad's version and the template changelog together. Advance dt-obs's own version when its content changes.
3. Run `sh scripts/check.sh` and the applicable [skill evaluations](../evals/app-launchpad/README.md). Record the candidate revision and verify its current-head checks.
4. After the authorized merge, tag the verified merge with `v<VERSION>`. Verify the remote tag target and any authorized GitHub Release. Each published tag is immutable.
5. Reconcile the release milestone after the tag and release record are verified. Close it once its scope is resolved. Verify any separately deployed product site from its own release evidence.

[Project](https://github.com/users/theharithsa/projects/3) · [Template releases](https://github.com/theharithsa/app-launchpad-template/releases)
