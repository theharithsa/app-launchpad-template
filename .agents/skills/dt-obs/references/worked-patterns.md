# Worked observability patterns

Use these synthetic examples to choose signal boundaries for the target application.

| Application | Signals | Verification |
| --- | --- | --- |
| Static site | Browser RUM with a consented origin-local anonymous identity and build metadata | Verify page and interaction signals. |
| Node service | HTTP and domain spans, structured OTel logs, RED metrics and queue measurements | Match a real request and safe failure to its spans, logs and metric points. |
| Firebase workspace | Browser SDK operations, authenticated same-origin gateway when needed, committed-change audit and durable business events | Verify access isolation and distinguish browser observations from committed changes. |

- At a telemetry gateway, verify the caller and replace any client identity fields with server-derived values. Bound batch size, queue depth, timeout, and rate. Clear client queues when the account changes.
- Record initial, error and recovery states for long-lived listeners. Use a finite span for each operation boundary.
- Preserve request, transaction, trace/span, event and release identities where each is available. Link a committed-change consumer to its source context when that context exists. Keep the original event ID and occurrence time through outbox retries.
- Verify searchable records, cross-signal correlation, and deployment identity independently of HTTP acceptance.
