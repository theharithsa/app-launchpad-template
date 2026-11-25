# Browser RUM and identity

Identify the deployed generation before choosing an API. Bind the approved
tag to the correct Classic application or latest frontend. Use one injection
method, check CSP and beacon reachability, and verify that each UI entrypoint
and route has the expected coverage.

## Classic RUM

| Task | Classic API or setting |
| --- | --- |
| Enable | Provision the application and its approved RUM JavaScript tag. Apply the app's consent mode and CSP settings. |
| Actions and errors | Use `dtrum.enterAction` and `dtrum.leaveAction` for bounded manual intent, including failure and cancellation. Feature-detect `dtrum.reportError` or `dtrum.reportCustomError` for sanitized errors. |
| Identity | Apply the approved pseudonym through `dtrum.identifyUser(value)` after consent and verified sign-in. Check the session reset boundary on sign-out and account switch. |
| Properties | Define Classic user action and session properties in application settings, then use the matching JavaScript API. Verify actual tenant capture of each property. |
| Cross-origin linking | Use the supported Classic linking mode. Confirm the actual request header or cookie, allowed first-party origins and backend instrumentation. |

Open the synthetic session in the Classic RUM experience. Follow the captured
action to its server-side trace where supported, and check the selected action
property and sanitized failure. [Classic JavaScript API](https://docs.dynatrace.com/javascriptapi/doc/types/dtrum.html) · [Classic cross-origin linking](https://docs.dynatrace.com/docs/observe/digital-experience-classic/rum-classic/web-applications/initial-setup/link-cross-origin-xhrs)

## Latest RUM

| Task | Latest RUM API or setting |
| --- | --- |
| Enable | Configure the intended frontend in Experience Vitals. Use the approved injection method and opt-in behavior for that frontend. |
| Events and actions | Use `sendEvent` from `@dynatrace/rum-javascript-sdk/api` for a custom event. Use the installed SDK's User Actions or Interactions APIs when those event types fit. |
| Identity | Use the SDK's `identifyUser` with an approved pseudonym. Check `isEnabled()` before opt-in-dependent work. Use the supported session/identity boundary and verify guest and account-switch behavior. |
| Properties | Submit approved event fields with the `event_properties.` prefix and set up session properties in the intended frontend. Test capture and visibility with the tenant audience. |
| Backend linking | Confirm the agent propagates W3C trace context to the approved endpoint and the backend extracts it. When manually reporting a request, the SDK Native HTTP API accepts a real W3C `traceParent`. |

Check a synthetic event and its session in `user.events` and `user.sessions`.
Use the [latest RUM recipes](dql-verification.md#latest-rum-event-and-session)
for exact IDs. Verify native trace navigation for the same request in the
tenant UI when supported. A custom request-property join establishes
application correlation. [Latest RUM SDK](https://docs.dynatrace.com/javascriptapi/doc-latest/documents/rum-javascript-sdk_Documentation.RUM_JavaScript_SDK_Overview.html)

## Consent, identity and propagation

Choose a pseudonym appropriate to the app. Enable real-person identifiers and
replay only under their own approved privacy decisions. Check masking at
capture and property visibility in the tenant. Test guest, restored session,
sign-in, sign-out, account switch and a late or absent tag. Verify that a
transition leaves no previous user's identity or queued events behind.
Anonymous identity, when approved, can use a per-origin random value with a
page-lifetime fallback. Avoid device fingerprinting and cross-site identity.

Keep event names and outcomes bounded. Use safe request identifiers for
correlation and avoid DOM text, auth credentials and form values. Track an
observed attempt separately from the committed server outcome. Follow the
[documented RUM business-event API](https://docs.dynatrace.com/docs/observe/business-observability/bo-events-capturing/web-and-mobile-rum)
for the chosen version.

For browser OTLP forwarding use an authenticated, rate-limited first-party
gateway. Validate identity and replace client-supplied actor fields from
verified auth. Limit attributes, payload size, timestamps and event counts.
Keep ingest credentials server-side. Allow propagation only to approved
endpoints, check CORS and capture the actual header on a synthetic request.
The deploying app owns authentication. The tracing header carries context.
