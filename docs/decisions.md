# Decisions and unresolved questions

For each consequential decision record: question; proposed options/tradeoff; status (proposed/approved/needs-user-input); chosen value; approval source; consequences.

Decision areas: product rules, stack/runtime versions, deployment/cloud/project/region, auth/roles/tenancy, storage/jobs/integrations, design/brand, repository owner/visibility/main, Dynatrace tenant/RUM consent/identity, costs/retention, release/merge permissions.

None are pre-approved by this template. Ask the user directly when the answer is missing. Never paste secret values here.

## Template maintenance decisions — not consumer defaults

| Question | Decision/status | Alternatives and reason | Approval source | Consequence |
| --- | --- | --- | --- | --- |
| Template license | MIT / approved | Apache-2.0 considered; owner explicitly selected MIT | Human answer in this chat, 2026-10-29; issue #14 | Root LICENSE covers inherited template material; each generated application's license stays needs-user-input |
| Template version | 1.9.0 / approved | Replace custom 1.09.0 with valid SemVer for interoperable tooling | Issue #18 and human authorization to resolve all issues | No leading-zero numeric identifiers; tag v1.9.0 matches metadata |
| Partial bootstrap | Remove / approved implementation choice | Synchronizing partial assets still leaves missing catalog/tool references; full GitHub template is the default | Issue #17 alternative and human authorization to resolve all issues | No bundled asset duplicates; unavailable GitHub means adoption pending |
| Main protection | PR + foundation check; no force-push/deletion / approved | Sole-owner workflow uses zero mandatory approvals; actual checks remain required | Issue #13 and human authorization to resolve all issues | Apply opt-in settings procedure; no bypass actors |
