# Dynatrace foundation

Use the actual product's topology and current official Dynatrace/OTel documentation. If available, apply dt-obs and its relevant references, not project-specific tenant examples. Discover MCP environment information and tools; confirm the environment matches the user's ingest destination before queries or mutations. Do not create IAM/token scopes, processing rules, buckets or paid monitoring without applicable authorization.

## Coverage plan

For each journey map actor/action, attempt, durable outcome, failure, API/dependency/worker boundaries, RUM action, log, metric, canonical event, sensitive fields and proof. Include admin/security/settings, cancellation/reversal/deletion, scheduled recovery and external integration failures. A static site may have browser/build telemetry only: record backend/business-event exclusions instead of inventing services.

Use consistent service.name, namespace, service.version, build.commit and deployment.environment.name; include a per-process instance identifier where appropriate. Maintain a naming/unit/attribute contract. Release identity has bounded operational retention; do not put request/user/case IDs, URLs or arbitrary free text into metric dimensions. Cost/cardinality must be assessed, including commit/resource attributes.

## Browser

Configure the approved RUM tag once; avoid duplicate injection. Choose automatic vs manual actions intentionally, pair every manual action once on success/failure and route change, and prevent error cleanup from leaving open actions. Identity/consent is a user decision: default proposals favor pseudonymous identity; email or replay requires explicit privacy resolution. Keep Session Replay off until separately approved. Handle blocked storage with random per-page fallback, not hardware fingerprinting. Test guest/login/logout transitions without attributing one user to the next.

RUM is client-observed. Browser success cannot certify a committed backend outcome. API incoming trace headers convey context, never identity or permissions. Preserve supported native RUM request tracing; custom IDs alone do not establish native navigation.

## Backend and workers

Inspect existing agents/SDKs before adding a single compatible OTel initialization. Initialize before instrumented modules, use SDK-managed contexts and actual child spans, normalize routes and propagate request/transaction context across genuine boundaries. Instrument real database, storage, queue, AI and third-party calls with explicit safe attributes; do not simulate a missing dependency or fabricate IDs. For asynchronous work choose genuine parent context or span links and distinguish source-operation context from delivery context.

Emit structured allowlisted logs with trace/span correlation; RED request/worker count, errors and duration; runtime memory/CPU/event loop where supported; SDK queue size/capacity/processed/drop metrics; exporter success/failure and bounded flush success/failure/timeout. Runtime metrics describe a process, not host monitoring. Exclude exporter requests from recursive instrumentation. Telemetry failures cannot replace successful customer outcomes. Set bounded queues, export timeout, shutdown/flush and serverless completion behavior. Exercise actual failures; self-observability is best effort during exporter failure, so retain sanitized platform diagnostics as well.

Use server-side secrets, native-runtime SDKs and supported OTLP transport. Resolve tenant auth realm/scopes/endpoint using official docs and existing secure configuration. For Dynatrace SaaS, commonly OTLP /api/v2/otlp/v1/{traces,metrics,logs} and business events /api/v2/bizevents/ingest; verify the actual destination and supported protocol/auth rather than interpolating an unconfirmed tenant. Never ship ingestion credentials in VITE/NEXT_PUBLIC/browser variables.

## Canonical events

Emit durable outcome events from an atomic domain/outbox commit or reliable committed-change capture. Do not publish canonical success before commit. Use stable event ID, event type/schema/provider, occurrence time, transaction ID, version/SHA and safe numeric outcome metadata. Failed/replayed transactions must not create duplicate outcomes. Delivery is at least once: retry with the same ID and consumers deduplicate. Track pending/in-flight/rejected depth, oldest due age, retry/lease health and safe recovery. No network call inside a transaction. Never replay delivered records to restamp a version. UI navigation need not be a canonical business event.

## Software development lifecycle signals

Track intake/issue creation and triage, development started/blocked/resumed, PR/link changes, reviews, checks/tests, merge or close-without-merge, issue close/reopen, release, deployment, runtime verification and rollback as actual events. Include failed/rejected/cancelled transitions and telemetry gaps. Each event carries stable source identity, occurrence/observation times, schema, authority, repository and applicable issue/PR/head SHA/run attempt/release/artifact/environment links. Preserve many-to-many issue/PR mappings. Do not fabricate links or events for unobserved history.

When dt-obs is installed, read its `references/sdlc.md`; the essentials here remain usable independently: trusted GitHub observer, signed-webhook validation, durable delivery/reconciliation, stable source event IDs, deduplication, allowlisted metadata, bounded metrics and source-to-tenant evidence. Use a CI/SDLC-specific provider/service; link to application telemetry through the actual deployed commit/artifact/version and environment, not invented trace ancestry. Development milestones need explicit trusted records because GitHub cannot observe every local action.

Document coverage and ownership, retention/cost/access, delivery lag/rejection/gap health, recovery and safe lifecycle dashboards. Verify a complete authorized synthetic issue → PR → checks → merge → deployment → runtime chain and failed/reopened/retried paths; mark unavailable stages pending. Never create or merge dummy production work just to obtain evidence.

## GitHub signals

Use references/github-release.md for actual workflow/job/check/test/release observations. CI is automation-confirmed, not a domain commit. Keep report-processing spans distinct from original test execution. No fake historical execution span fabricated from timestamps.

## Verification

Separate: code/local tests → deployed configuration → HTTP response with partial rejection checks → tenant queryable records → cross-signal joins → native RUM-to-trace navigation. A 202 response or printed event ID is not searchability. A custom string join is not native navigation.

With MCP: get environment info, generate/refine then verify DQL, use short explicit time windows/scan limits, project only safe fields, filter exact service/version/SHA/run/event ID, and save query/result evidence. Discover metric keys and actual log correlation fields; logs may use trace_id/span_id while spans use trace.id/span.id. Query actual metric values, not just metadata. Compare expected vs distinct event IDs; investigate absent/duplicate records, sampling and ingestion delay without inventing a pass. If metrics are in a different supported store, record the verified store. No query access means explicitly pending tenant verification.

Verify release marker + deployment event; workflow/check/leaf-case statuses; API and workers; matching log/span context; runtime/RED/export/queue/outbox samples as applicable. Record RUM loading separately from tenant UI linkage. Use controlled synthetic nonproduction outcomes for lifecycle mutation tests. Missing live transition evidence remains a limitation, not a reason to edit customer data.
