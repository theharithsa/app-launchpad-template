# Worked observability patterns

Use these synthetic examples to choose signal boundaries for the target application.

| Application | Signals | Verification |
| --- | --- | --- |
| Static site | Browser RUM with a consented origin-local anonymous identity and build metadata | Verify page and interaction signals. |
| Node service | HTTP and domain spans, structured OTel logs, RED metrics and queue measurements | Match a real request and safe failure to its spans, logs and metric points. |
| Managed store example (Firebase) | Browser SDK operations, authenticated same-origin gateway when needed, committed-change audit and durable business events | Verify access isolation and distinguish browser observations from committed changes. |

- At a telemetry gateway, verify the caller and replace any client identity fields with server-derived values. Bound batch size, queue depth, timeout, and rate. Clear client queues when the account changes.
- Record initial, error and recovery states for long-lived listeners. Use a finite span for each operation boundary.
- Preserve request, transaction, trace/span, event and release identities where each is available. Link a committed-change consumer to its source context when that context exists. Keep the original event ID and occurrence time through outbox retries.
- Verify searchable records, cross-signal correlation, and deployment identity independently of HTTP acceptance.


## Managed store example (Firebase)

When a client SDK writes directly to Firestore, a trusted committed-change
trigger can create the audit/outbox event with an ID derived from the trigger
identity and transition type. Treat trigger replays and ordering explicitly.
When originating request context is unavailable, attach the real consumer
span and document an asynchronous boundary, such as
correlation.origin=firestore-audit. Verify actors through the approved
identity and trigger contract. Normalize vendor error strings to bounded
application codes before recording them.

[Firestore trigger guidance](https://firebase.google.com/docs/functions/firestore-events)
