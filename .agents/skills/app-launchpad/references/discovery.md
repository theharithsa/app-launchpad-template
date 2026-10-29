# Discovery and architecture

## First conversation

Extract known answers from the idea and existing sources; ask concise questions about the missing decisions that affect implementation. Useful groups:

- Product: intended users, problem, primary journey, required first release, explicit exclusions, acceptance criteria.
- Experience: public site vs authenticated app, mobile/desktop usage, brand/assets, accessibility, languages/time zones, examples to follow or avoid.
- Data and trust: entities, ownership, roles, tenant boundaries, sensitive data, retention/export/deletion, regulatory constraints, demo policy.
- Platform: preferred stack or constraints, existing repository/organization, hosting/cloud, domain, region, budget, local/offline requirements, integrations.
- Operations: Dynatrace environment and access route, RUM identity/consent, GitHub ownership/visibility, who authorizes merge/deployment, reliability expectations.

Do not ask for secret values in chat. Ask for secret names and the supported secure configuration method. A user may choose to defer an integration: record it disabled/pending, not silently simulated as real.

## Decision record

For each consequential decision record status (proposed/approved/needs-user-input), chosen option, alternatives, rationale, source of approval and consequences. Do not copy a decision from SalesDrone or any reference app. If no preference is known, present a small set of stack options suited to the constraints. Resolve before dependent implementation.

Compare static generation/client SPA/server rendering using SEO, interactivity and deployment needs. Choose backend runtime, database, auth, storage, jobs and AI only if required. Evaluate transaction/query needs, operational burden, region, cost, team familiarity, portability and provider limits. Pin compatible versions based on current official docs and use a lockfile. Explain recurring costs before creating resources.

Map a vertical slice: user action → validated API → policy → durable write → response → visible UI result → telemetry. Define acceptance criteria for success, denial, conflict, empty, retry and failure. For static content map authoring → build → accessible public page → deployment instead.

Design a minimal topology. Separate dev/test/staging/prod resource identities and credentials; never choose a Firebase project, GitHub org or Dynatrace tenant merely because it is accessible. Confirm repository visibility/license rather than defaulting to public publication. Record external resource creation and deployment permissions separately.
