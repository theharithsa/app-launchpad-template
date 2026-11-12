# Canonical business events and audit delivery

Define an event catalog from actual committed schemas and lifecycle transitions. Include creation, changes, reversals, deletion/completion/reopening and administrative decisions. Preserve the difference between caller and affected entity. Decide which event owns a numerical total; snapshots, grading, ledger deltas and browser observations may describe the same outcome.

Distinguish two event classes and emit both. Committed-write summaries (`records.written`, `records.stage_changed=1` per transaction) are integrity and audit evidence: they prove a transaction committed and how much it touched. Semantic business events (`leads.stage_changed` with `stage.from`/`stage.to`/`lead.source`, `activities.logged` with `activity.type`/`outcome`, `tasks.completed` with `task.kind`/`overdue`/lateness, `imports.completed` with totals) are what funnel, conversion, outcome-mix and time-in-stage analytics require. Their dimension values come from the domain's finite option lists (defaults or admin-configured), never free text, and they carry the entity ID and verified actor so an event joins to the trace and logs of the same transaction. Summaries alone force consumers to reconstruct business meaning from write counts, which they cannot.

Refused attempts are part of the journey. Version conflicts, capability denials, rate limits and maintenance locks should surface as bounded events or WARN logs with the application error code and the same transaction/request IDs, so "attempted but rejected" is distinguishable from "never attempted" and from "committed".

Preferred capture:
- Backend-owned mutations: write domain state and outbox entry atomically in the same transaction. Do not make external ingestion calls inside a retried database transaction.
- Direct Firebase SDK writes: capture committed changes with trusted triggers and deterministic IDs derived from source event identity plus semantic event index/type. Triggers are asynchronous, can repeat and arrive out of order. Their capture is separate from the original commit; document that gap and recovery options.

Derive attribution from verified backend callers, trusted server fields or provider-supported trigger metadata. Do not turn arbitrary client actor/email fields into server-confirmed identity. When attribution is unavailable, record system/unknown explicitly without inventing an actor.

## Contract

Use CloudEvents or the target API's supported schema. Keep stable id/source/type/specversion, original occurrence time and a versioned bounded data contract. If the tenant routes or segments by `service.namespace`, `service.name` or `event.provider`, carry those fields on every event class, including deployment and CI events, so nothing falls back to default buckets. Example shape (metavariables must be populated from real context):

```json
{
  "specversion": "1.0",
  "id": "<stable-event-id>",
  "source": "<service-provider>",
  "type": "com.example.credits.awarded",
  "time": "<original-UTC-occurrence-time>",
  "data": {
    "event.id": "<same-stable-event-id>",
    "event.provider": "<canonical-provider>",
    "event.authority": "server-confirmed",
    "schema.version": 1,
    "transaction.id": "<logical-operation-id>",
    "trace_id": "<real-origin-or-audit-span-trace-id>",
    "span_id": "<real-origin-or-audit-span-id>",
    "correlation.origin": "backend-request",
    "actor.id": "<verified-caller>",
    "participant.id": "<affected-student>",
    "credits.delta": 100
  }
}
```

Never send this placeholder example as live evidence. Use `traceparent` where supported for actual context; custom trace fields alone do not create linkage. Distinguish source trace from subsequent delivery spans. Every new canonical event should have a transaction ID and real capture/operation trace context; missing browser context is an explicit async boundary, not a reason to generate a fake historical trace.

Use explicit field extraction. Export bounded numerical answers only when approved; omit free-text feedback/submissions, names where unnecessary, credentials, invite codes and private answer keys. Privacy deletion of app records does not delete existing telemetry; document retention and erasure boundaries separately.

## Delivery

Endpoint: `https://<environment-id>.live.dynatrace.com/api/v2/bizevents/ingest`, separate from OTLP. Classic token: `Api-Token`, scope `bizevents.ingest`. Platform/OAuth: Bearer with current `openpipeline:bizevents:ingest` permission (verify tenant policy).

Use server-owned outbox records, delivery leases with expiry/ownership checks, bounded scheduled draining, retained attempt/status/nextAttemptAt fields and backoff with jitter. Only a documented full-acceptance response marks delivered (currently 202). A batch 400 may partially accept valid events: reconcile per-record results or retry with stable IDs and consumer deduplication; never mark the entire batch delivered. Treat 429/5xx/timeouts as recoverable and honor Retry-After; repeated 400/401/403 require repair rather than a tight retry loop. Retain failures and an operator recovery path.

Acceptance followed by a lost response can duplicate delivery. Preserve event IDs; consumers deduplicate before aggregation. Never delete pending records as a troubleshooting shortcut. Apply agreed retention to delivered records; outbox access is server-write-only and operator reads are authorized. Do not expand app roles just to read the queue.

## Analytics correctness

- Award totals: sum committed signed deltas, including reversals, once per event ID.
- Score snapshots: latest appropriate snapshot, not the sum of snapshots.
- Survey comparisons: latest response per unique participant and stage; report denominators and missing pairs. NPS, confidence scales and workshop rating are distinct measures.
- Votes: latest valid choice per voter/team/activity, according to the domain contract.
- Browser events: engagement/funnel observations, never authoritative award totals.

For DQL, use installed dt-dql-essentials/dt-obs query skills when available and relevant. Validate field types and actual tenant data before saving queries; do not assume custom trace strings have the same type as native trace.id.

Primary references (rechecked 21 October 2026):
- https://docs.dynatrace.com/docs/dynatrace-api/environment-api/business-analytics-v2
- https://docs.dynatrace.com/docs/observe/business-observability/bo-events-capturing/web-and-mobile-rum
- https://firebase.google.com/docs/functions/firestore-events
