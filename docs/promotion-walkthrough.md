# From issue to verified release

This walkthrough uses synthetic records for a profile service and a command-line
package. Use the same steps with your own versions, owners and evidence links.

## Intake

Use Feature to capture the user outcome and acceptance checks. Use Bug for the
affected version, observed behavior and regression check. Use Task for the
component and completion evidence. Use [Agent brief](../.github/ISSUE_TEMPLATE/agent-brief.yml)
for delegated work. The form marks required intake fields. Add delivery evidence
as it becomes available.

Use the [Release or promotion form](../.github/ISSUE_TEMPLATE/release.yml) for the
candidate record, or use the promotion PR if it holds the same information. Link
the milestone, included issues and implementation PRs. Name the release owner
and recovery target. Update this record through retries.

| Board status | Entry criteria |
| --- | --- |
| Planned | The outcome has a milestone, an owner when known and one sprint for the expected work. |
| Ready | Acceptance checks are clear and blocking dependencies are resolved. |
| In progress | The owner is implementing or verifying the issue. |
| In review | A reviewable PR links the issue and its current verification. |

Use the board's existing statuses. Keep parent epics as rollups and record
blockers as issue dependencies.

## Staged service example

A maintainer wants signed-in users to rename their profile. Issue 12 records a
synthetic save-and-reload check and a denial check for a different account.
PR 13 targets the staging branch and references issue 12 without closing it.

1. Check PR 13 on its current revision. Deploy that accepted source to an
   isolated pre-production environment with synthetic accounts.
2. Record the source and immutable artifact, successful pre-production run,
   saved-and-reloaded profile, denied write and same-version health evidence in
   the [candidate record](#candidate-record). Run any applicable migration or
   configuration rehearsal and review the recovery target.
3. Open the production promotion PR for that source. The release owner checks
   the candidate against the recorded acceptance and authorizes the rollout.
   Promote the same artifact where possible. For environment-specific builds,
   verify the same source and record both digests.
4. Check the production run, served build revision, the agreed safe critical
   journey and error/latency signals. Close issue 12 when its criteria are met.
   Link the production evidence to the candidate record.

### Candidate record

| Evidence | Synthetic example |
| --- | --- |
| Scope | Milestone 1.4.0, issue 12 and staging PR 13. Release owner is the on-call maintainer. |
| Checked candidate | Source `1111111`, artifact `sha256:111…`, pre-production run 101. Save, reload, denied cross-account write and health checks passed. |
| Decision | Maintainer approved source `1111111` and artifact `sha256:111…` for a small initial rollout in promotion PR 14. |
| Production | Run 102 deployed artifact `sha256:111…`. The version response named source `1111111`. The safe smoke and the agreed error check passed. |
| Recovery | Prior version 1.3.4, artifact `sha256:aaa…`. The owner can restore it and verify the version response and affected journey. |

### Hold or recover a candidate

A retry changes source to `2222222`, and its denied-write check fails in
pre-production. Mark the same release record held. Link the failing run and keep
the issue open. Fix it in a staging PR, recheck the new artifact, then update the
promotion PR and record a fresh approval. A prior green run applies to its own
source only.

If a production smoke fails, stop expansion of the rollout. The release owner
restores the prior verified artifact when compatible with the current data and
configuration. Recheck the served revision, affected journey and health signals.
Record recovery and link the remaining work.

## Package example

For a CLI without a separate staging deployment, issue 31 defines the expected
new `--format json` output. PR 32 targets the default branch. The reviewer builds
and installs that exact candidate in an empty environment and verifies the
command output alongside the required checks.

The maintainer approves the checked source, merges through the PR and publishes
the allowed version. Record the version, tag commit, registry entry and artifact
checksum. Then install that version in a new empty environment, run the command
and compare the output with issue 31. If the new package fails, halt the rollout,
point consumers to the last verified version when authorized and fix forward
under a new version. Preserve the published version and its evidence.

[Prerequisites](getting-started.md) · [Delivery policy](delivery.md) · [Release evidence and recovery](release-plan.md)
