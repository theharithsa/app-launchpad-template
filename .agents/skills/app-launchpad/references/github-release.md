# GitHub, CI/CD and deployment

Apply [authorization and safety](safety.md), [evidence](evidence.md) and [service ownership](services.md).

## Choose the delivery path

| Project setup | Path |
| --- | --- |
| No deployed pre-production environment | Issue → short-lived branch → implementation PR to protected default branch → required checks on the candidate → authorized merge → applicable publish/deploy and verification. Use CI-built previews, local tests or emulators as applicable. The implementation PR is also the release approval point when merge triggers release. |
| Deployed pre-production environment | Issue → implementation PR to the staging branch → required checks → isolated deployment and acceptance → promotion PR to the production branch → verify the tested source/artifact and obtain applicable authorization → merge, deploy and verify production. |

Keep only long-lived branches with a real role. A repository can publish a
versioned package or template without an application deployment. A second PR
only applies where there is a separately verified candidate to promote.

### Solo maintainer and team review

- Solo baseline: require a PR and real CI checks, with zero mandatory independent GitHub approvals. The assistant reviews the diff and reports evidence. The owner supplies the decision to ship within the agreed authority. An assistant review summary is evidence of that review only.
- For changes that can affect production access, private data, migrations or deployment credentials, show the owner the exact candidate, affected boundary, negative test evidence and recovery plan before release. Record their explicit authorization for that scope. If merge triggers deployment, resolve this before merging the release PR.
- When there are independent reviewers, add review and ownership rules the team can satisfy. Apply protections and approval settings only with the owner's authorization. Check the effective rules on GitHub after applying them. [GitHub review requirements](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews)

## Adopt or audit the workflow

Read the existing repo instructions and effective branch rules. Map which PR
targets, CI checks, release triggers, service identities and data stores actually
exist. Record which practices are in place, missing, or inapplicable. Reuse
the working paths. Take the smallest gap through an issue and reviewed PR,
with separately authorized settings or infrastructure changes where needed.
GitHub template generation copies files. Verify repository settings and deployed
resources separately. Keep the audited source revision and adopted template
version with the handoff.

During authorized setup, verify the required checks and
[automatic branch cleanup](#automatic-branch-cleanup).

Keep the agreed baseline stable. Revisit it when a concrete failure, a new
maintainer, new data or access risks, or a changed release topology calls for
different controls.

## Automatic branch cleanup

Enable **Automatically delete head branches** in **Settings → General → Pull Requests** during authorized repository setup. GitHub template generation copies files and requires this repository setting to be applied separately.

Run `gh repo edit OWNER/REPO --delete-branch-on-merge` with repository admin access. Confirm `gh api repos/OWNER/REPO --jq .delete_branch_on_merge` returns `true`. Verify the setting after setup with the next eligible same-repository PR merge.

Let GitHub remove eligible merged head branches. Branch protection and rulesets can prevent deletion. For fork PRs, GitHub uses the fork's setting and requires write access to the fork. [GitHub automatic branch deletion](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-the-automatic-deletion-of-branches)

## Issue-to-merge delivery

- Apply this workflow to every actionable feature, bug, maintenance/refactor, documentation, dependency, security or infrastructure report, including requests made in chat.
- Questions requiring no change need no issue.
- Reuse the existing issue on retries and resumed work. Split unrelated deliverables into linked issues. A Dependabot PR can be its own tracked item.
- Never post sensitive vulnerability details to a public issue; use the repository's authorized private reporting route and retain only a safe tracking reference.

1. **Intake:** Reuse or open the issue before implementation. Record the intended outcome, acceptance criteria, risk, and test evidence needed. Follow [Project tracking](github-projects.md) when a board is in use. Add the agreed milestone and reuse appropriate labels. Under a local-only hold or missing access, record a local draft and pending sync.
2. **Development:** Work on an issue-linked branch, preserving existing edits. Record material scope changes and blockers. Review the staged diff for credentials and private artifacts.
3. **PR:** Include the user-visible change, linked issue, test evidence, and applicable data, monitoring and rollback impacts. Use `Closes #123` only when the PR fully resolves the issue and targets the default branch. For partial fixes and staging PRs, use a non-closing reference and track any remaining acceptance work through promotion.
4. **Review and checks:** Capture actual review and check outcomes for the current PR head. Address feedback and rerun affected required checks after changes; previous-head success is insufficient. Wait for required approvals and resolved discussions under repository policy. Keep failed, cancelled, skipped and blocked outcomes visible.
5. **Merge:** Once requirements, checks, approvals and applicable authorization are satisfied, merge through GitHub using the repository's permitted method and verify the remote merged state and resulting commit. Do not stop at a draft/green PR when merging is already authorized. Do not bypass protection. If authorization is missing, present the concrete green PR and state the remaining approval; never treat this skill as blanket merge/deploy permission.
6. **Issue resolution and release:** Verify closure and resolution reason against completed acceptance criteria after merge. Close manually only when appropriate and authorized if automatic closure does not apply; leave partially addressed issues open. Record the merge SHA, release/deployment links and verification result. Merged, released, deployed and runtime-verified are separate states. Track rollback, regression/reopen and follow-up issues without rewriting the original history.

- GitHub's [issue linking rules](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue) govern closing keywords and default-branch behavior.

## CI and deployment safeguards

- Prevent direct pushes, force pushes and failed-check bypasses on release branches. Require [the applicable checks](testing.md#checks-by-change-risk) on the current candidate. A required aggregate job must distinguish an intentional exclusion from a skipped or failed required check.
- Run PR code without production or Dynatrace ingestion credentials. Keep privileged deployments and observers on trusted workflow paths. Pin third-party Actions to verified commits and use least-privilege job permissions and short-lived cloud identity.
- Deploy the checked source or immutable artifact. Recheck after source changes. Set bounded timeouts, retention and concurrency. Avoid cancellation that could leave migrations partially applied.
- For a release involving stored data or identity, use the [access and recovery checks](testing.md#access-and-recovery) before applying sensitive changes.

## Release

- Use SemVer appropriate to the product; keep workspace package versions synchronized when relevant, with API version separate.
- A new app's baseline version needs a recorded choice.
- An explicit local version hold may cover a review cycle, not indefinite reuse of a published tag.
- Keep changelog and versioned impact plan with affected modules/contracts/data/indexes/config/secrets/docs/UI/tests/telemetry and rollback consequences.

- Before publication complete all applicable predeploy gates once for the integrated change.
- Prepare rollback source/config/migrations; no destructive automatic rollback of customer data.
- Deploy prerequisite indexes/schema/rules before queries that rely on them and confirm readiness.
- Deploy all affected services when secret bindings/instrumentation change.
- Publish docs/screenshots only when reviewed, synthetic and current.
- Never reuse or overwrite a release tag.

- After deployment check exact version/SHA/artifact, service revisions/health and safe protected-route denial. Verify docs publication separately. For a package or template, verify the published tag, commit and package or release page as applicable.
- Follow [observability](observability.md#github-signals) for CI, deployment and runtime evidence. Leave a handoff linking the issue, PR, checks, publication and recovery instructions with the known limits.

### Weekly production releases with frequent staging

Use this cadence when the project owner chooses it. Record the release window
and time zone, owner, approval, and urgent-fix criteria in the project SDLC.
Agree on the app version policy separately from the calendar. Strict SemVer
keeps patch increments for fixes and minor increments for compatible features.
A project may instead use the app minor number for each weekly release and
give its public API a separate compatibility version.

1. Plan one versioned production milestone with the issues intended to ship.
   Keep the candidate app version stable through development and testing.
2. If the project has staging, deploy reviewed changes there as often as needed. Record the environment,
   source commit, CI run and attempt, and artifact digest when available. For
   example, `2.14.0 · build 3` shows a build of the `2.14.0` candidate.
   Reserve `2.14.1` for an actual patch release. Separate environment resources,
   access and synthetic test data from production.
3. At the weekly window, use the project’s [delivery path](#choose-the-delivery-path).
   With staging, require evidence for the promoted source or artifact. For
   environment-specific builds, verify the same source and record each artifact
   identity. Without staging, verify the intended release through its checked
   implementation PR and the applicable risk-based checks.
4. Publish one immutable tag, release and changelog entry for the verified
   production release. Skip empty or unready windows and explicitly reschedule
   unfinished issues. Keep pre-release build records in CI and deployment
   history. Attach the app version and run/attempt to delivery telemetry.
5. For an incident that cannot wait, branch from the production release,
   exclude unfinished weekly work, and verify the patch in the project's
   isolated test path. Keep required checks and authorization. Record the
   incident and patch and bring the fix into the next regular candidate.

Treat cadence as an operating policy until workflow checks enforce it. A
calendar trigger alone supplies neither a reviewed candidate nor authorization
to deploy. A staging-only change must leave production untouched until its
approved promotion succeeds.
