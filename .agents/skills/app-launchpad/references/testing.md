# Test suites and evidence

Shared boundaries: [safety](safety.md), [evidence](evidence.md), [service ownership](services.md).

- Build tests for behavior and risk, not counts or generated wording.
- Select commands for the actual stack; do not copy npm commands into a Python/Go project.
- Record exact commands and prerequisites in docs/testing.md.

## Checks by change risk

| Change | Evidence before release |
| --- | --- |
| Copy, docs or presentational UI | Run affected build/link or regression checks. Inspect affected screens at relevant widths for visible changes. |
| Behavior, workflows or API | Exercise the primary path and relevant failures with domain, API and integration checks. Add a regression for the reported failure when existing tests miss it. |
| Permissions, exports, private files, data deletion, migrations, IAM or workflow credentials | Verify permitted and denied access, revocation and cross-scope behavior where relevant. Use synthetic data in an isolated test environment. Show recovery evidence for affected data and configuration, and follow the [owner decision](github-release.md#solo-maintainer-and-team-review). |

Use required CI as the baseline. Missing, skipped and failed checks are distinct.
If a required check could not run, record the gap and resolve it before release.
Treat emulators as evidence of application behavior and query the provider for
effective deployed IAM and configuration.

## Access and recovery

- Verify the intended human, deployment and runtime identities. Include inherited role grants, secret access and resource scope. Where staging exists, use provider policy evaluation or authorized non-destructive checks to prove its identities cannot act on production data or files. Keep production credentials out of staging and PR runs.
- Check that one user, role or tenant cannot browse, export, or retrieve another's data through alternate surfaces such as files or search. Test revocation at the next authorized request and record any client display-cache delay.
- For apps with persistent customer data, record acceptable data loss and restore time. Verify backup coverage and retention, then rehearse a restore into isolated, access-controlled resources. Validate database records and their associated files together. Test with synthetic data by default. Record the actual restore time, integrity results and any uncovered stores. Git and release rollback cover source and artifacts. Data recovery requires its own evidence.

## Coverage layers

- Unit/domain: validation, state transitions/reversals, calculations, idempotency, policy and rollback.
- API/contract: real routes, auth/membership/tenant scope, missing/invalid payload, denial, conflict, pagination, retry and safe errors; verify schema compatibility.
- Integration: actual selected database/auth/storage emulators or isolated real test services, transaction races, outbox atomicity, worker lease/recovery, file rules and migration/index behavior. Mock-only tests do not establish integration correctness.
- UI/browser: primary journeys, loading/empty/error/denied views, keyboard/dialog behavior, themes and responsive stress cases with synthetic data.
- Telemetry: independently decode emitted OTLP where practical, prove real trace/log context, bounded labels/units/temporality, payload allowlists, event identity/retry, transaction rollback, exporter failure/timeout isolation and real queue drops under a controlled bound.
- Release: build/type/lint as relevant, secret/dependency scan, docs/contracts/skills/version checks, fixture exclusion, artifact integrity, postdeploy version/SHA and safe authorization probes.

- Wire CI to real test commands and report missing prerequisites as blocked or not run.
- Avoid tests that merely assert implementation strings.
- Review snapshots visually.
- Avoid rerunning the full matrix after each small reversible UI adjustment: use a targeted check/visual review, then the integrated release gate once.
- Broaden after changed behavior, failure or an unresolved risk.

## Case catalog and results

- [Evidence](evidence.md) owns execution records/statuses and capture boundaries; [safety](safety.md) governs production writes.

- Use stable case IDs and list owner/module, requirement, risk, layer, automated/manual status and real suite/command.
- Include runner-reported leaf cases; preserve skipped outcomes and do not count nested suites as cases.

- Test events export an allowlist: case digest/approved file or catalog ID, status, duration and occurrence time.
- Exclude free-text test names, stdout, error stacks, customer content and environment variables.
- A test name digest is not proof its execution occurred; use actual runner output.
- Keep automated browser/physical/manual evidence separate from unit/API totals.

- Use an installed approved isolated browser for synthetic automation; never attach a personal signed-in profile as a test harness.
