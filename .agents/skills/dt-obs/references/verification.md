# Verification, deployment and release evidence

Test representative journeys and failure invariants, not string matches against instrumentation source. Use synthetic accounts/data and isolated emulators/collectors. Disable external RUM and production export in rehearsal; a local endpoint is selected only by explicit test/emulator configuration. Do not weaken production auth/rules to manufacture a failure.

## Local verification matrix

| Area | Evidence |
|---|---|
| Export | Independent local OTLP protobuf receiver decodes traces, logs and metrics; resource names, units, temporality, histogram data and log trace context are correct |
| Concurrency | Two overlapping users/requests keep identity and transactions isolated, including awaited work, errors and retries |
| Propagation | Valid W3C context continues or links correctly; malformed headers are bounded; third-party propagation remains restricted |
| Gateway | Unauthenticated, disallowed-origin, spoofed-identity, invalid span IDs/time bounds, oversized batches and rate limits tested |
| RUM | Logged-out, restored login, account switch, sign-out, blocked storage, agent late/missing, route changes, success/error and API-unavailable behavior; each caller outcome literal reaches the exported action property unchanged; declared properties are visible in the tenant; boundary/global errors and API failures appear as RUM errors with the request ID hint |
| Error classification | Each application error code, vendor error (Firebase, gRPC, timeout, parse) and status class maps to a bounded `error.type` on span, log and metric; the catch-all share in exported spans is near zero |
| Dependencies | LLM/database/messaging spans carry their semantic attributes and token/collection/model dimensions; a decoded export shows them populated, not only span names |
| Workers | Every scheduled queue exports outcome counters, lag histogram and backlog/oldest-age gauges; a forced backlog is visible as a metric, not only as a log attribute |
| Canonical events | Commit success/failure, repeated trigger, duplicate delivery, concurrent workers, lost response, expired lease and scheduled retry; no double awards or accidental partial-success marking |
| Lifecycle | Corrections, reversals, removals and background recovery preserve business semantics and sensitive-field exclusions |
| SDLC | Source-confirmed issue/PR/review/merge/resolution events; partial and many-to-many links, reopened issues, duplicates/out-of-order webhooks, observer recovery, and tenant joins through merge/artifact/deployment to runtime; see [SDLC](sdlc.md) |
| CI/CD | Real failed/skipped test reporter, missing/partial reports, untrusted archive guards, source/attempt checks, failed/partial deployment and published tag/revision matching; independently searchable execution/test/release signals |
| Resilience | Disabled/unreachable exporter, rejected token, partial success, queue overflow and bounded flush do not block domain completion |

Inspect actual exported payloads for secrets/free text and uncontrolled metric dimensions. Exercise the app's existing feature/security suite to catch instrumentation-induced changes. Runtime host limits, dependency initialization order and serverless warm starts deserve stack-specific checks.

## Deploy and verify only within authorized scope

Build with intended flags and secret references; inspect artifacts for credential leakage. Deploy only affected hosting/function/service targets and preserve shared Auth, rules, indexes and unrelated codebases. Record commit/build and service.version, verify health/static assets and startup, and retain a rollback source/configuration. Secret updates may require redeployment of all bound functions.

Use an isolated identifiable transaction to verify:
1. Each RUM script/helper loads, consent is respected, identity transitions occur and its beacon succeeds.
2. Each OTLP signal independently passes transport/auth/payload validation, with no partial rejection. Logs working does not prove metrics/traces work.
3. Each canonical event reaches outbox delivered status with stable event ID; duplicates remain safe.
4. Authorized tenant queries locate the exact event/trace/log IDs and expected metrics within the time window; check sampling, retention and pipeline routing.
5. Navigate an actual RUM action to its backend trace if supported/configured. A custom trace field or successful beacon is insufficient proof. Confirm the propagation header the browser sends is the one the server extracts, then join one action to one server span by `request.id` in a tenant query.
6. Rehearse a controlled failure and recovery, then remove only the authorized synthetic source fixtures, preserving audit evidence and excluding that test session from analytics.

Stop blind retries on persistent 400/401/403 and diagnose protocol, scopes/owning-user permissions, endpoint and secret binding. For 404, check `.apps` and duplicated/missing paths. For missing events, check capture settings, outbox state, occurrence time, sampling and query permissions. Do not modify roles or switch credentials merely to conceal an authorization failure.

## Documentation and final report

Use an evidence table with date, environment, scenario, signal, expected result, observed result and safe ID/reference. Mark separately: implemented, locally verified, deployed, ingest accepted, tenant searchable and RUM correlation verified. If query access is absent, say so and leave that stage unverified.

Document signal routing, resource attributes, event authority/dedup rules, metric units/cardinality, identity/consent, secrets by name, flags, queue/retry/retention, pending-event recovery, rollback and known trace boundaries. Dashboards, alerts and SLOs need their own actual configuration/validation; instrumentation alone does not create them. Ensure owners know where export failures and pending queue age are visible.
