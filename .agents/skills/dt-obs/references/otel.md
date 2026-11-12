# OTel signals, context and runtime integration

## Transport and configuration

Dynatrace SaaS OTLP base: `https://<environment-id>.live.dynatrace.com/api/v2/otlp`. Signal paths: `/v1/traces`, `/v1/metrics`, `/v1/logs`. The `.apps` UI URL is not the ingestion URL. Direct Dynatrace OTLP requires HTTP binary protobuf; gRPC/JSON require an appropriate intermediary/conversion. Check whether each SDK exporter appends its signal path; do not append twice. Gzip is optional; verify actual exporter/server support.

For platform tokens, use `Authorization: Bearer <secret>` with `openpipeline:traces:ingest`, `openpipeline:metrics:ingest`, and `openpipeline:logs:ingest` as needed. For classic tokens, verify that the target endpoint supports `Authorization: Api-Token <secret>` and the applicable `openTelemetryTrace.ingest`, `metrics.ingest`, or `logs.ingest` scopes. Use explicit auth configuration. Query permissions are separate from ingest permissions.

Configure server-side secret injection, environment, stable service name/namespace and release version. Use placeholders in examples:

```text
OTEL_EXPORTER_OTLP_ENDPOINT=https://<environment-id>.live.dynatrace.com/api/v2/otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
OTEL_SERVICE_NAME=<service>
OTEL_RESOURCE_ATTRIBUTES=service.namespace=<namespace>,deployment.environment.name=<environment>,service.version=<release>
```

Never place authorization in `VITE_*`, public runtime config, Firestore client documents, ZIP artifacts or screenshots. Secret rotation must update all consumers; some serverless providers require redeploying functions bound to a new secret version. Respect existing variable precedence to avoid silently retaining an old token.

## Backend SDK

Initialize instrumentation before instrumented libraries load. For Node, check ESM preload/import ordering, matching SDK/exporter package versions, context manager and propagator. Avoid a second global SDK in warm serverless invocations. Exclude exporter/health/polling endpoints where appropriate to avoid recursive or noisy spans.

Use HTTP/server instrumentation plus semantic domain spans, database/queue boundaries and dependency outcomes. A logical span for a simulated payment/DB stage must be labelled simulated; it does not establish a deployed microservice or trace Google's managed database internals.

Use active OTel context/AsyncLocalStorage rather than a mutable global current user. Extract validated W3C context at ingress. Attach identity only after authentication, to the request and relevant child spans. Log structured severity, bounded message/event name, operation/outcome, error type and domain IDs. Emit through an OTel log SDK with active context; console JSON alone is not proof of OTLP log export. Any platform/console log kept for the hosting provider should still carry the active trace and span IDs so it can be joined from either side.

At the API error boundary, set `error.type` on the server span from the application error code (a finite set such as `UNAUTHENTICATED`, `CONFLICT`, `AI_RATE_LIMIT`, `MAINTENANCE_LOCK`; unknown errors become `INTERNAL`), include it in the completion log, and add it as a dimension on the request counter. Two 503s with different causes must be separable without reading response bodies. Log 4xx rejections at WARN with the code; they are the attempted-but-refused half of the journey.

Dependency spans need semantic attributes, not only a name and duration. Database: `db.system.name`, `db.operation.name`, `db.collection.name` (allowlisted), transaction attempt count. LLM calls: `gen_ai.system`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.response.finish_reasons`, `http.response.status_code`, `server.address`; never prompt or completion text. Normalize vendor errors into the bounded `error.type` set before the generic fallback: Firebase `messaging/…`/`auth/…` strings, gRPC numeric codes (`ABORTED`, `DEADLINE_EXCEEDED`, `RESOURCE_EXHAUSTED`, `UNAVAILABLE`), `AbortSignal` `TimeoutError`, schema/parse failures. Contention, timeouts and quota exhaustion are the signals operators most need and the ones a catch-all hides.

When `autoDetectResources` is off for a serverless/container runtime, set the resource identity explicitly from the platform environment: `cloud.provider`, `cloud.platform`, `cloud.region`, `faas.name`, `faas.version` or revision. Without them a regression cannot be tied to a deployed revision.

| Field | Meaning |
|---|---|
| service.name/version, deployment.environment.name | Resource identity |
| trace_id/span_id | Actual SDK span context; verify tenant mapping to trace.id/span.id |
| request.id | One HTTP attempt; useful in response headers |
| transaction.id | One logical business operation and its downstream events |
| event.id | Stable durable event, unchanged on retry |
| user.id/email or actor.id/email | Verified caller; distinguish affected student/customer |
| order.id / workshop.session.id / entity.id | Domain correlation, not metric labels |

Generate a new request ID per attempt. Preserve the transaction ID through retries and async messages without treating it as authentication or idempotency authorization. Validate length/format of incoming IDs; reject/replace malformed values. Use a distinct idempotency key when the business API needs it.

For async work, persist originating context with the committed outbox/message when available. Start a producer/consumer span or link as appropriate; keep original operation context and delivery-attempt context distinguishable. If Firestore writes lack browser context, create an actual audit-consumer span and mark `correlation.origin=firestore-audit`; do not claim an unbroken browser trace. Sampling may mean a valid ID has no stored span.

## Metrics and operational health

Use counters for requests/outcomes, explicit-bucket histograms for latency with clear units (normally seconds), gauges for current queues/pools/backlog age, and runtime CPU/memory/event-loop metrics where useful. Verify delta temporality and histogram compatibility against the actual Dynatrace exporter path. Resource/runtime metrics do not substitute for VM/host monitoring.

Every scheduled or queued worker (reminders, AI analysis, scoring, cleanup, outbox) needs the same treatment as the telemetry outbox: a counter per outcome (`sent`, `failed`, `cancelled`, `skipped`), a histogram for processing lag (processed time − due time), and gauges for backlog depth and oldest pending age sampled at drain start. Numeric attributes on a `worker.completed` log are not metrics, and attributes outside the log allowlist are dropped without warning; keep the allowlist and the worker result keys in one shared contract. LLM dependencies additionally need request count, duration and token counters dimensioned by model, operation and outcome.

Allow bounded dimensions such as normalized route, method, outcome and error category. Keep emails, UID, event/transaction/order/session IDs, raw URLs and exception text out of dimensions. Record metric outcomes exactly once at the owning layer; do not count browser observations plus backend outcomes as a single total.

Bound span/log queues, batches, export timeouts, concurrency, retries and payloads. Track dropped batches, exporter errors, partial success, queue age and flush failures without recursively instrumenting diagnostics. Flush all enabled providers before serverless invocation completion within a deadline; handle graceful process shutdown. No telemetry exception should mask the original business error or keep requests waiting indefinitely.

Primary reference: https://docs.dynatrace.com/docs/ingest-from/opentelemetry/otlp-api (rechecked 21 October 2026). Verify current native SDK docs for the app's language and version.
