# GitHub Project tracking

Use the existing primary board when it serves the project. If the owner chooses repository issues without a board, record that choice and track delivery with repository milestones. Keep private details out of public board fields and updates.

## Check access

Use `gh auth status --hostname github.com` to confirm the account and its GitHub CLI OAuth scopes locally. The CLI uses `read:project` for reads and `project` for changes. Verify the selected board with `gh project view NUMBER --owner OWNER`. When using a fine-grained token or another connector, check the selected owner's Projects permission and the board role separately. A successful read does not establish write access.

If the authorized account needs broader scope, the owner can approve `gh auth refresh --hostname github.com --scopes project`. Keep credential values out of the handoff. If access is missing or a step needs an administrator, add a pending entry to the existing issue or handoff with the board, exact operation, required role or scope, owner and a read-back check. Continue available repository-level issue and milestone work.

## Set up the board

| Where | Step and evidence |
| --- | --- |
| API or CLI | With approval for the owner and visibility, reuse or create the board. Add or import existing issues and PRs, including historical items and dependency PRs. Verify membership. |
| GitHub UI | Link the repository, select its default repository for new issues, and configure auto-add for the agreed scope. Auto-add handles new entries. Import earlier work separately. |
| API or CLI | Use native issue types when the owner has them. Otherwise apply the configured fallback labels. Bug covers broken behavior, Feature covers product capability and Task covers research, operations or maintenance. Treat epics as parent rollups. |
| API or CLI | Create milestones for planned outcomes and versions. Give each a scope and acceptance criteria, and a target date where known. Use active triage and dependency maintenance milestones for intake. |
| GitHub UI | Save milestone, sprint planning, roadmap and Kanban views. Show native Milestone, Sprint or Iteration, and execution Status. Check the selected date source in the Roadmap and keep unscheduled work visible. |
| GitHub UI | Verify built-in workflows for item closed, PR merged and item reopened. Keep issue closure tied to issue acceptance or its closing PR. |
| API or CLI | Read back item assignments, issue/PR links, milestone, iteration and status. Record board and view links in the delivery documentation. |

For UI work handed off to the owner, give them the board link, setting or view to open,
expected value, and the check you will use afterward.

## Plan and verify delivery

- Use a milestone for the outcome and an iteration for the work window. Assign current work to one appropriate sprint. Keep cross-sprint epics as rollups and review unfinished work before moving it.
- Record hard gates as native issue dependencies. Schedule dependent pilots after isolation, migration or other prerequisite acceptance. If dates move, reconcile dependent issues, milestones and saved views.
- Link an implementation PR to the issue and its milestone. Use a non-closing reference while acceptance is pending. Verify issue closure against its agreed outcome.
- At release, review issue/PR membership, classification and milestone scope. Backfill only with verified release evidence. Close released milestones after all intended work is resolved and record the destination of any agreed carryover.
- At intake, use the issue forms and [staged delivery walkthrough](https://github.com/theharithsa/app-launchpad-template/blob/main/docs/promotion-walkthrough.md), or open `docs/promotion-walkthrough.md` in the generated app.

## Intake automation

The bundled classification job reads the event issue and fills missing type
metadata. It preserves existing type labels and native types. Automatic repair
scans open work. Use the existing Project fields and classifications for
historical work.

The milestone job uses the event item or the open unassigned list. It preserves
assigned milestones, uses dependency maintenance for Dependabot PRs and reopens
a named intake milestone if required. Reconcile historical releases against
verified evidence separately.

## Keep the Project useful

- Record where to file work, who maintains the board and how often the owner reviews sprint capacity.
- Reuse native assignees, dependencies, issue types, milestones and one field for each planning question. Use priority and estimates where they support a real decision.
- Keep views focused. Use a status limit only when the team has an agreed capacity. Archive completed work when its retention and reporting policy allows it.

[GitHub CLI Project help](https://cli.github.com/manual/gh_project) · [GitHub Projects best practices](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/best-practices-for-projects) · [GitHub Project automation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
