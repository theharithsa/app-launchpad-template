---
name: example-web
description: Demonstrate a synthetic single-page web service skill.
---

# Synthetic web service — not implemented

- Owner: example-owner; source: hypothetical `src/web`; entrypoint: hypothetical `src/web/main.ts`.
- Purpose: a static explanatory page at https://example.test/ ; no backend, auth, durable data or business events.
- Design: one primary reading journey, responsive content, keyboard navigation, alt text; loading/error states apply only to actual asset requests.
- Code/contract: hypothetical `renderPage` accepts synthetic copy and renders semantic HTML. No HTTP API is required for static content.
- Tests: hypothetical `npm run test:web` would verify content and keyboard behavior; it does not exist in this repository and has not run.
- Deployment: unselected, not-run. No real provider/resource/secret names. Rollback would use the selected provider's previous immutable artifact once defined.
- Observability: hypothetical approved anonymous browser telemetry; no tenant configured or acceptance/searchability/native-linkage evidence.
- Continuation: [worked record](continuation.md). Apply the real project's policy owners rather than copying this example's facts.
