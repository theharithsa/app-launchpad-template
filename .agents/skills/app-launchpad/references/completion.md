# Completion and handoff

For every meaningful feature, review the agreed behavior, contract/policy, permissions/data scope, migration, UI states/settings, telemetry and tests. Record why any layer is inapplicable. Maintain relevant module skills as behavior changes; do not add empty version notes or universal modules with no owner. Shared logic should have one owner.

Maintain README/local setup, SECURITY, architecture/API docs, settings reference, design system, testing/case catalog, observability contracts/recovery, release procedure, changelog and release impact/evidence as applicable. User-facing docs explain workflows, limits and troubleshooting; implementation internals stay in engineering docs. Any new setting documents default/scope/permission/API/timing/limits.

A repository observability skill must name actual service/runtime entrypoints, approved environment mapping, safe secret names, event/metric conventions, instrumentation/test commands, DQL/store caveats and failure recovery without credentials. Repository release skill must state real branch/CI/provider commands, gates, OIDC setup references, index/migration ordering, artifact identity, PR/approval requirements, postdeploy proof and rollback. Until details are known, mark pending rather than writing invented commands.

Evidence statuses are passed/failed/skipped/not-run/blocked with timestamp, exact revision, command/tool, measured environment and safe artifact reference. Plans are not evidence. Don't bundle raw production logs or private images in Git. Synthetic captures require review, viewport, version, hash and asset list. Local evidence can stay ignored while safe CI artifacts retain release proof; retention and expiry should be known.

Before final handoff verify issue URL, PR relationship, latest-head checks/reviews, actual merge SHA and issue resolution (or explicit pending dependency), plus SDLC event delivery/searchability and deployment-to-runtime correlation. Inspect Git status/branch/diff and untracked/staged artifacts. Summarize the usable outcome, completed tests, PR/release/deployment identities when actually created, setup or secrets still needed and verification limits. Never say published if only local. Provide the user a concise next action only for a concrete unresolved dependency, not a generic offer to continue.

## Behavioral walkthroughs for this skill

Validate skill changes against these scenarios without external side effects:

1. “Build a booking app” with no stack/repo/tenant: ask about actors, booking/payment rules and platform constraints; recommend choices, no invented inventory/payments/cloud resources.
2. “Static portfolio, no login, deploy later”: build static content with confirmed brand/assets; no database/business outbox; local validation only until deployment is authorized.
3. “Use Firebase and our Dynatrace tenant” without IDs: proceed on independent UI/domain work; ask exact project/tenant/region/privacy and secure config method before connection.
4. Local tests green, exporter 202, MCP unavailable: report local/transport evidence and tenant verification pending, never all-green.
5. Deploy succeeded but telemetry failed: keep customer outcome, diagnose/retry reporting only; preserve IDs and original test execution attempt.
6. Existing repo dirty with a local-only version hold: preserve changes, use existing conventions, no scaffold overwrite, push, merge or deployment; resolve only the missing permission when a reviewable release is ready.

7. New bug in chat with an existing matching issue: reuse that issue, link the PR, require current-head checks and permitted merge; verify remote merge and closure. No duplicate issue or premature success event.
8. PR addresses half an issue, targets a release branch, or is closed unmerged: retain the relationship without claiming resolution; no auto-close assumption or merged event.
9. Reopened issue, squash merge, repeated webhook and failed observer: preserve distinct source transitions, deduplicate retries, map checked head to merge/artifact/runtime, and replay telemetry without repeating merge/deployment.
10. GitHub or tenant access unavailable: continue authorized local work, retain issue/milestone drafts and pending verification, and report the exact gap. No invented issue URL or tenant evidence.
