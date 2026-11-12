# Observable software development lifecycle

Read this for lifecycle instrumentation from work intake through runtime outcomes. GitHub is authoritative for repository facts; runners own actual execution/test results; deployment systems own deployment facts; app telemetry owns runtime behavior. Development milestones require explicit trusted records. A commit timestamp does not prove when coding started, and a green PR does not prove merge or production health.

## Coverage and event ownership

Adopt a versioned project contract such as the types below. These are custom event names, not built-in Dynatrace semantics. Emit one event per observed transition; preserve source facts and multiple review rounds, PRs and deployments.

| Stage | Example event types | Authoritative evidence |
|---|---|---|
| Intake/triage | `sdlc.issue.created`, `.triaged`, `.updated` | GitHub issue/timeline or verified webhook; work kind and safe scope |
| Development | `sdlc.development.started`, `.blocked`, `.resumed` | Explicit agent/developer milestone or supported project-state transition, with source identity |
| PR relationship | `sdlc.pr.opened`, `.updated`, `.ready`, `.issue_linked`, `.issue_unlinked` | GitHub PR state, head/base SHA and verified issue relationship |
| Review | `sdlc.review.submitted`, `.dismissed`, `.changes_requested` | GitHub review ID, decision and reviewed head SHA; exclude comment text |
| Execution | `sdlc.check.completed`, `sdlc.test.completed` | Actual check/run/attempt/report, including failure, cancellation, timeout, skip or missing evidence |
| Integration | `sdlc.pr.merged`, `.closed`, `.reopened` | Remote merged flag/time/merge SHA; closed without merge stays distinct |
| Resolution | `sdlc.issue.closed`, `.reopened` | Issue state/reason and relation to completed acceptance criteria; partial fixes remain open |
| Delivery | `sdlc.release.published`, `sdlc.deployment.completed`, `sdlc.runtime.verified`, `sdlc.rollback.completed` | Immutable release/artifact/revision, real environment and actual verification/rollback evidence |

Track rejected approvals, blocked merges, failed deployment and unsuccessful runtime verification explicitly with bounded status/reason codes. Report planned/not-run work as coverage state, not invented completed events. Do not export every edit/keystroke or private developer conversation. Define which material issue/PR updates warrant events and rate/cost limits.

## Event and correlation contract

Use a dedicated provider such as `<project>.sdlc` and a separate observer `service.name`. Choose the tenant's supported event ingest/store and verify routing before implementation. Structured BizEvents are suitable for lifecycle facts; reserve native deployment events/markers for actual deployments. Keep application business outcomes under their own provider. See [official ingest documentation](https://docs.dynatrace.com/docs/observe/business-observability/bo-events-capturing/bo-events-capturing-external-sources).

Define allowlisted fields and types, for example:

- `event.type`, `event.provider`, `sdlc.schema.version`, stable `sdlc.event.id`, `sdlc.occurred_at`, `sdlc.observed_at`, bounded `sdlc.status`, `sdlc.source` and `sdlc.authority`.
- GitHub repository ID/name/URL and applicable issue IDs/URLs, PR number/URL, relationship type, head/base/merge SHA and source transition/review ID. Preserve many-to-many relationships in validated fields or separate relationship events; do not force one issue per PR or assume every linked issue was resolved.
- Workflow/run ID, original execution attempt, distinct reporting attempt, check/test identity, actual result and measured duration where available.
- Release/version, immutable artifact digest, deployment ID/environment, deployed commit and applicable application service identity. Runtime resources expose the same actual build/version identity; map CI head SHA through merge SHA to the deployed artifact, especially for squash/rebase merges.
- Safe evidence/source URLs and explicit unknown/pending correlation state. Include real trace/span context only for operations actually instrumented. Cross-lifecycle joins by commit/artifact are not parent-child traces or proof of native RUM linkage.

Keep a source-owned `sdlc.event.id` even if ingest assigns or transforms `event.id`; verify the stored mapping. Build IDs from repository plus source transition identity (webhook delivery/timeline/review/run/attempt/deployment ID). Never use only issue+status: reopen/reclose and repeated reviews are distinct occurrences. Collector retries reuse the ID and original occurrence time; reporting retries retain original execution attempt. Define a shared identity/reconciliation rule for webhook and API replay; unmatched snapshots are observations with their own provenance, not fabricated historical transitions. Query/consumer deduplication is required; do not assume Dynatrace enforces uniqueness.

Allow issue/PR/run/commit IDs in events/logs, not metric dimensions. Counts/durations may use bounded stage/status/environment/work-kind labels. Avoid full issue/PR/review bodies, titles, actor emails, secrets, raw test output and private vulnerability details by default. Review repository URLs/names, access controls and retention for private code metadata; metrics/SLOs and dashboards must not expose restricted events.

## Capture, trust and recovery

Prefer trusted GitHub webhooks or independent observers plus bounded API reconciliation; a developer machine alone cannot see changes made by other people. Validate webhook signature against raw bytes using a server-side secret, enforce repository/event/action allowlists, replay/delivery checks, payload size/schema limits and least privilege. Persist a sanitized accepted delivery to a durable queue before acknowledging it; process with bounded retry/backoff and a rejected/dead-letter path. Do not trust caller-supplied repository or status without verification. Do not run PR code or artifact content with observer/export credentials. Follow [GitHub Actions](github-actions.md) for forks, trusted definitions and artifact guards.

Record local development started/blocked/resumed through a minimal authenticated milestone path or approved durable job record, then export asynchronously. If no observer/endpoint is configured, keep pending milestones and a coverage gap; do not claim tracking is active. Respect local-only holds and existing remote-write/merge authorization. Installing this skill never authorizes issues, merges, deployment or tenant configuration changes outside the active task.

Handle duplicates, out-of-order delivery, retries, lost responses, rate limits, observer outages and finite source retention. Preserve append-only transition history; reconcile current state using source versions/times instead of latest arrival. Backfill only source-supported history with original timestamps and provenance. Record unrecoverable gaps. Monitor delivery lag, queue age/depth, rejection/drop counts, reconciliation lag and last successful source/tenant verification. Separate telemetry failures from successful GitHub merges/deployments; replay reporting only. A tenant outage cannot silently convert a successful merge to failed or trigger another deployment.

## Verification and useful views

Use authorized synthetic repositories/fixtures and a local receiver first. Exercise issue creation/reuse, multiple issue links, partial/default-branch closure rules, changes requested/approval dismissal, updated PR heads, failed/cancelled checks, merged versus closed PRs, reopen/reclose, webhook forgery, duplicate/out-of-order replay, rate limits and observer recovery. Verify that untrusted inputs cannot execute code or leak secrets. Distinguish fixtures from actual source events; never create dummy production issues/merges solely for proof.

Independently locate expected distinct source event IDs in the tenant and join issue → PR → checked head → merge commit → artifact/deployment → actual runtime version/environment. Verify failure/retry paths and the actual runtime health evidence, with explicit windows/permissions/sampling/retention. Missing stages remain pending. HTTP acceptance does not prove tenant coverage. Use [verification](verification.md) for the application signals.

Maintain a lifecycle timeline, blocked/review/check aging, delivery lead time, deployment outcomes, regression/rollback view and observer health where needed. Define time anchors, eligibility, units and denominators before deriving lead time, deployment frequency, change failure rate or recovery time; do not infer incidents from arbitrary failed CI runs or claim a causal regression from commit coincidence. Exclude synthetic work and deduplicate replay. Record dashboards/alerts as configured and verified only after they actually exist.

## GitHub Projects

GitHub issues, pull requests, and releases own lifecycle facts. Project Status, iterations, and roadmap dates describe planning and execution intent. Correlate through verified repository and issue or PR identifiers. An item moving to Done does not prove a merge, issue resolution, or runtime deployment. Keep issue bodies and public Project updates out of telemetry payloads.
