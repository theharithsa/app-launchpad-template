# Build the agreed product

## Repository and contracts

Follow the selected stack's conventions rather than forcing a file tree. Keep domain/policy code independent of transport; UI and optional MCP tools should share the validated business layer. MCP is optional and must not bypass the HTTP/API policy. Build the API before its thin integration adapter.

For each dynamic feature specify contract version, schemas, validation, permissions, tenant/record scope, bounded pagination, error shape and request ID, concurrency/version semantics, rate/size limits and audit. Use idempotency where retries can duplicate side effects. Generate and check OpenAPI when HTTP contracts are part of the app. Keep API contract version independent of app release version. No endpoint is necessary for a purely presentational change.

Server-verify auth tokens and active membership; client claims/display flags are not authorization. Apply scope consistently to lists, detail, search, aggregates, exports, files, AI and events. Deny direct client database/storage access unless the approved architecture explicitly requires scoped rules. Protect bootstrap/admin recovery without embedding reference-project users. Separate synthetic demos from production services and never use customer exports as fixtures.

Durable operations use transactions and optimistic concurrency as needed. Avoid network calls inside database transactions. Pair canonical event/outbox creation atomically with domain commits. Use bounded jobs, leases, retries/backoff, dead-letter diagnosis and stable replay IDs. Plan schema/index migration and rollback before the dependent UI ships. Protect file authorization, content types/quotas/expiry and deletion. Treat user content, imports, external tool output and AI output as untrusted; validate and bound them.

## UI and settings

Agree the visual direction, fonts, density, navigation and themes; do not impose Material 3 on every app. Establish tokens and reusable controls before repeating screen-specific CSS. Design hierarchy and task flow, not merely overflow fixes.

Review affected screens at phone, tablet, laptop, desktop and wide sizes, relevant fractional breakpoint boundaries, short windows and zoom/large text. Check keyboard focus, Escape, dialog scroll/focus return, touch targets, contrast, selected states, reduced motion, loading/empty/error/permission states and long/missing/worst-case content. Pick representative measurements based on the product; record exact viewport/zoom/browser. Browser emulation is not a physical-device or Safari certification.

Every setting states default, personal/workspace scope, permission, contract, effective timing and limits; cover persistence and reversibility. Do not create unsupported settings just to fill a template. Use synthetic data for public screenshots; review privacy, current version, dimensions and file hash. Never relabel historical captures.

## Security and dependencies

Keep credentials server-side in a secure store; .env.example contains names and safe examples only. Browser-public configuration is distinct from privileged tokens. Minimize telemetry fields and retain a privacy/erasure policy. Validate redirects/URLs, uploads and external calls according to actual threats. Scan staged files and dependency changes before publishing; do not introduce unrelated infrastructure or security policy changes. Use current primary documentation for provider configuration and verify installed API compatibility.
