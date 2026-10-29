# Behavioral walkthroughs


Validate skill changes against these scenarios without external side effects:

1. “Build a booking app” with no stack/repo/tenant: ask about actors, booking/payment rules and platform constraints; recommend choices, no invented inventory/payments/cloud resources.
2. “Static portfolio, no login, deploy later”: build static content with confirmed brand/assets; no database/business outbox; local validation only until deployment is authorized.
3. “Use our chosen cloud and Dynatrace tenant” without IDs: proceed on independent UI/domain work; ask exact project/tenant/region/privacy and secure config method before connection.
4. Local tests green, exporter 202, MCP unavailable: report local/transport evidence and tenant verification pending, never all-green.
5. Deploy succeeded but telemetry failed: keep customer outcome, diagnose/retry reporting only; preserve IDs and original test execution attempt.
6. Existing repo dirty with a local-only version hold: preserve changes, use existing conventions, no scaffold overwrite, push, merge or deployment; resolve only the missing permission when a reviewable release is ready.

7. New bug in chat with an existing matching issue: reuse that issue, link the PR, require current-head checks and permitted merge; verify remote merge and closure. No duplicate issue or premature success event.
8. PR addresses half an issue, targets a release branch, or is closed unmerged: retain the relationship without claiming resolution; no auto-close assumption or merged event.
9. Reopened issue, squash merge, repeated webhook and failed observer: preserve distinct source transitions, deduplicate retries, map checked head to merge/artifact/runtime, and replay telemetry without repeating merge/deployment.
10. GitHub or tenant access unavailable: continue authorized local work, retain issue/milestone drafts and pending verification, and report the exact gap. No invented issue URL or tenant evidence.
