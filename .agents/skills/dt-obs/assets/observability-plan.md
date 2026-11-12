# Application observability plan

## Scope and architecture
- Application, repositories, environments and release:
- User journeys and privileged operations:
- Runtime/service map, hosting and async/database boundaries:
- Existing agents/SDKs and duplicate-instrumentation risks:
- Authorized implementation/deployment scope:

## Journey coverage
| Journey | Actor / affected entity | Attempt / committed outcome | Span boundary | Canonical event | Metric | Failure/reversal test |
|---|---|---|---|---|---|---|

## Signal contracts
- RUM application/tag reference, entrypoints/routes, agent version, CSP and declared action/session property names:
- Browser failure reporting: error boundary, global handlers, API failure codes and request-ID hints:
- Identity: signed-in value, anonymous behavior, account-switch handling, consent:
- Resource service/namespace/version/environment:
- Logs: severity, safe message/error fields and trace context:
- Error classification: application error codes, vendor/timeout/parse normalization, catch-all fallback and where `error.type` lands (span, log, metric):
- Dependency semantics: database collection/operation, LLM model/tokens/finish reason, messaging outcome, server address; excluded content:
- Worker/queue health: outcome counters, lag histogram, backlog depth and oldest-age gauges per queue:
- Metrics: name, instrument, unit, bounded labels, temporality, histogram buckets:
- Trace propagation: first-party allowlist, HTTP/queue/context links and known gaps:
- Request / transaction / idempotency / event ID ownership:
- BizEvents: schema, authority, original occurrence time, actor, entity, signed delta/revision:
- Fields explicitly excluded:

## Development lifecycle
- Issue intake/reuse, work kinds, acceptance criteria and partial-resolution rules:
- Development milestones, source authority and pending/offline coverage:
- PR/issue relationships, reviews, checked head, merge SHA and issue closure/reopen:
- Event schema, source-owned IDs, source/observation time and dedup/reconciliation:
- Trusted webhook/observer, signature validation, least privilege and credential boundaries:
- Source → checked head → merge → artifact → deployment → runtime mapping:
- Delivery lag/gaps/queue health, retry/replay/retention and recovery owners:
- Timeline/delivery metrics, denominators, private metadata access and cost limits:
- Synthetic/local tests and actual source-to-tenant chain evidence:

## CI and release signals
- Thoth observer action and SDK pins for GitHub Actions, trusted runs and separate CI service identity:
- Test runner reports, case/scenario granularity, skipped/missing/failed outcomes:
- Deployment owner and verified/partial/failed stage semantics:
- Published changelog/tag revision and notes redaction/limits:
- Secret isolation, artifact parsing limits and PR/fork policy:
- Stable IDs, report retention, replay and tenant verification:

## Transport and operations
- OTLP base and exporter path behavior, protocol:
- BizEvents endpoint:
- Secret names and credential type/scopes (never values):
- Gateway authentication, validation, body/batch/time/rate limits:
- Queues, leases, retry/backoff, partial success, retention and recovery:
- Sampling, cardinality/cost controls, diagnostics and bounded flush:
- Deployment targets, required flags, rollback and shared resources preserved:

## Evidence
| Date / environment | Scenario | Signal | Expected | Observed | Safe evidence reference | Verification stage |
|---|---|---|---|---|---|---|

Stages: local verification; deployed; HTTP accepted; tenant searchable; RUM-to-backend link verified. Do not collapse these into a single success label.

## Remaining work
- Missing access/configuration and exact verification still needed:
- Owners and handover/documentation:
