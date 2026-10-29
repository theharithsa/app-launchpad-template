# Test suites and evidence

Build tests for behavior and risk, not counts or generated wording. Select commands for the actual stack; do not copy npm commands into a Python/Go project. Record exact commands and prerequisites in docs/testing.md.

## Coverage layers

- Unit/domain: validation, state transitions/reversals, calculations, idempotency, policy and rollback.
- API/contract: real routes, auth/membership/tenant scope, missing/invalid payload, denial, conflict, pagination, retry and safe errors; verify schema compatibility.
- Integration: actual selected database/auth/storage emulators or isolated real test services, transaction races, outbox atomicity, worker lease/recovery, file rules and migration/index behavior. Mock-only tests do not establish integration correctness.
- UI/browser: primary journeys, loading/empty/error/denied views, keyboard/dialog behavior, themes and responsive stress cases with synthetic data.
- Telemetry: independently decode emitted OTLP where practical, prove real trace/log context, bounded labels/units/temporality, payload allowlists, event identity/retry, transaction rollback, exporter failure/timeout isolation and real queue drops under a controlled bound.
- Release: build/type/lint as relevant, secret/dependency scan, docs/contracts/skills/version checks, fixture exclusion, artifact integrity, postdeploy version/SHA and safe authorization probes.

Add real test commands before wiring CI. Missing prerequisites mean blocked/not-run; never create an always-green placeholder workflow. Avoid tests that merely assert implementation strings. Review snapshots visually. Avoid rerunning the full matrix after each small reversible UI adjustment: use a targeted check/visual review, then the integrated release gate once. Broaden after changed behavior, failure or an unresolved risk.

## Case catalog and results

Use stable case IDs and list owner/module, requirement, risk, layer, automated/manual status and real suite/command. A catalog describes intended coverage; it cannot mark execution passed. A result records actual execution/run/attempt, source revision, start/end/duration, status, tool/browser and safe artifact reference. Use passed/failed/skipped/not-run/blocked distinctly. Include runner-reported leaf cases; preserve skipped outcomes and do not count nested suites as cases.

Test events export an allowlist: case digest/approved file or catalog ID, status, duration and occurrence time. Exclude free-text test names, stdout, error stacks, customer content and environment variables. A test name digest is not proof its execution occurred; use actual runner output. Keep automated browser/physical/manual evidence separate from unit/API totals.

Use an installed approved isolated browser for synthetic automation; never attach a personal signed-in profile as a test harness. Keep raw logs/captures ignored and publish only reviewed synthetic assets. Do not create production customer records to make a verification report green.
