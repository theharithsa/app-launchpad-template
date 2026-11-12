---
name: dt-obs
description: Plan, implement and verify Dynatrace observability across browser RUM, OpenTelemetry, canonical business events, GitHub development and release lifecycle, and GitHub Actions execution with Thoth. Use when instrumenting an app, backend, worker, or CI/CD workflow. For telemetry investigation, use the specialized query skills.
metadata:
  version: "1.4.1"
---

# Dynatrace application and development lifecycle observability

Adapt instrumentation to the actual stack and user journeys. Confirm the target tenant, consent, permissions, and service identity before implementation.

## Discover and plan

Read the app handover, observability docs, runtime entrypoints, authentication, deployment configuration and representative business writes. Inspect existing agents/SDKs before adding instrumentation to avoid double spans, duplicate RUM tags and recursive exporter requests. Verify SDK compatibility against installed versions and current primary documentation.

Map request/bug → issue → development → linked PR → review/checks → merge → release/deployment → runtime verification/rollback alongside browser → API → database/queue → worker → committed result. Separate static pages, true backend services, browser SDK calls and simulated dependencies. For each important journey specify actor, attempted action, committed outcome, failure, trace boundary, business event, metric, sensitive fields and verification evidence. Include administrative operations, reversals, account changes and background recovery—not only the happy path.

Use [the plan template](assets/observability-plan.md). Resolve missing tenant/tag/secrets access only where needed. Planning or installing this skill does not authorize deployment, paid resources, role changes or tenant settings edits. Use authorization already established in the active task.

## Select the implementation path

- Browser/static/SPA: read [RUM and identity](references/rum.md).
- API, Node.js, Firebase, serverless, collector or other backend runtime: read [OTel and correlation](references/otel.md). Use the native SDK for the actual runtime; Node is the worked pattern, not a restriction.
- Scores, payments, votes, surveys, certificates or other durable domain outcomes: read [business events](references/business-events.md).
- For sample boundaries in a static app, Node service and Firebase workspace, read the [worked patterns](references/worked-patterns.md).
- Issue intake, development milestones, PRs, reviews, merges, issue resolution and correlation to deployed runtime: read [software development lifecycle](references/sdlc.md).
- GitHub Actions execution telemetry: always use [Thoth](https://github.com/plengauer/Thoth) and follow [GitHub Actions observability](references/github-actions.md) for trust, Dynatrace export, and evidence. Use the same reference for structured test, deployment, and changelog events.
- Auditing an already-instrumented app for what still blocks detection and log/trace/metric/event correlation: read [gap review](references/gap-review.md) and walk the code paths, not the observability document.
- Before declaring completion, follow [verification and release](references/verification.md).

## Preserve these invariants

1. RUM describes browser experience. Browser-reported success does not certify a database commit. Server-confirmed events come from durable domain state/outbox or committed-change capture.
2. Verify backend identity independently. Browser tags and incoming trace headers grant no permission. Email tagging requires the target app's consent/privacy decision; workshop consent is not transferable.
3. Use real OTel context. Keep transaction IDs across the business operation and event delivery; request IDs identify attempts. Continue or link traces only where context is genuinely available. Never invent trace IDs merely to populate a field.
4. Export credentials stay server-side. Use secret references and placeholders in artifacts. Never copy historical chat credentials into a skill, build, report or command log.
5. Logs/spans/events may have bounded entity identifiers; metric dimensions must have bounded cardinality. No raw bodies, tokens, free-text feedback, join codes or uncontrolled error messages by default. Bounded does not mean uninformative: the application error code, dependency model/collection and from/to state are bounded and must reach spans, logs and (where finite) metric dimensions; a status code or catch-all `APPLICATION_ERROR` alone cannot separate failure causes.
6. Telemetry failure must not roll back an otherwise successful business operation. Durable audit delivery is at least once; stable event IDs and deduplication are required. Do not promise lossless browser telemetry or exactly-once ingestion.
7. State evidence precisely: local test, deployed configuration, HTTP acceptance, searchable tenant record and verified cross-signal linkage are different results.

## Deliver

Produce instrumentation, meaningful tests and a maintained `observability.md`/equivalent with coverage, resource identity, signal endpoints, secret names (no values), event/metric contracts, identity and privacy choices, async correlation limits, recovery/rollback and evidence. Update the app handover when appropriate. Summarize actual verification and outstanding access or tenant configuration; do not report a working RUM-to-trace link solely because IDs exist in custom fields.
