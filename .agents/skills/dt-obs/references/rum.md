# Browser RUM and identity

Install the app-approved Dynatrace JavaScript tag in every HTML entrypoint, before app modules. Use a placeholder when a tag is not yet supplied. Ensure CDN/beacon URLs are permitted by CSP, shared helper modules are published, and static routes and hash routes are covered. Inspect the installed RUM generation and its supported APIs rather than assuming Classic APIs apply to every agent.

For the Classic agent:
- `dtrum.identifyUser(value)` has a capital U. Handle agent readiness with a bounded retry and cancellation on identity changes. Failure cannot block sign-in.
- On restored/new authenticated sessions, identify by a stable UID or approved email. Clear the former identity on account switch/sign-out. When approved, use `browser:<random UUID>` for anonymous visits and restore it after sign-out. Persist per origin with a page-lifetime fallback when storage fails. It is a pseudonymous browser identifier, not a hardware/device fingerprint or cross-site identity.
- Keep monitoring consent and session capture settings intact. An anonymous Firebase UID and the anonymous RUM browser ID are different concepts.
- Use bounded semantic action names, meaningful completion/error actions, and route names without query secrets. Pair every manual enter/leave action on success, failure and cancellation; avoid duplicating automatically captured actions.
- Capture safe control type/ID and normalized operation outcomes. Do not scrape labels/DOM/form values or capture every keystroke. Broad click events can be noisy; use them only for a defined coverage need.
- Define the outcome vocabulary once and import it in both the caller and the recorder; test that each caller literal reaches the exported property unchanged. A recorder allowlist that differs from the caller's strings silently exports `other` for every request. Add the HTTP status class and the bounded application error code to failed request actions so a browser failure can be matched to its server span.
- Declare every custom action/session property name the code sends in the RUM application's session and user action property settings; undeclared properties are discarded with no client-side error. Record that declaration as a provisioning step and verify a property appears in the tenant before relying on it.
- Report caught failures to RUM: render error boundaries and global `error`/`unhandledrejection` handlers call `dtrum.reportError`; API failures (network error, 5xx, selected 4xx) call `dtrum.reportCustomError(<bounded code>, <bounded message>, <request.id as hint>)`. Feature-detect and never block the UI. Disabling automatic action detection also disables automatic error attribution, so manual error reporting becomes mandatory, not optional.
- When automatic actions are off, wrap the user's intent (`Archive lead`, `Commit import`) as the parent action and the API calls as children so the journey is readable as intent, not as a list of endpoints.
- `window.dynatrace.sendBizEvent(type, attributes)` is the native business-event API for this implementation. `sendEvent` is not an equivalent BizEvents API. Feature-detect and fail safely. Only monitored sessions produce these events; no guaranteed delivery on unload/offline.

Browser event fields should use a distinct provider and `event.authority=client-observed`, stable schema version, event ID, transaction ID, safe page/control/operation and applicable domain IDs. Attach real trace/span IDs only for instrumented operations. A click is an attempt; distinguish it from response completion and committed server outcome.

For browser-to-server OTel forwarding, use an authenticated same-origin gateway; never ship Dynatrace ingestion secrets. Validate Firebase/OIDC tokens, replace claimed actor identity with verified identity, allowlist operations/attributes, bound payload/timestamp/duration/span counts and rate-limit. Origin checks supplement authentication. Flush queues or partition them on account changes so users cannot inherit each other's queued telemetry. Anonymous RUM may remain enabled even when this gateway deliberately requires sign-in.

Propagate W3C context only to approved first-party endpoints. Verify CORS, RUM frontend/backend-linking settings and sampling; do not enable broad propagation to Google/Firebase or arbitrary third parties. Explicit browser OTel traces are not automatically children of a RUM action. Confirm the ingress extracts the header the deployed agent actually sends (W3C `traceparent` versus vendor headers such as `x-dtc`) and that same-origin propagation covers the API path; otherwise the backend accepts a header the browser never sets.

Primary references (rechecked 21 October 2026; reverify for the target agent):
- https://docs.dynatrace.com/javascriptapi/doc/types/dtrum.html
- https://docs.dynatrace.com/docs/observe/business-observability/bo-events-capturing/web-and-mobile-rum
