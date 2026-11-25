# Observability in App Launchpad

Use the [dt-obs skill](../../dt-obs/SKILL.md) for signal selection, payloads,
privacy, correlation, delivery and verification. Start with the real service
topology and confirm the approved tenant before connecting. Apply the
[authority and privacy policy](safety.md) to new scopes, settings and paid usage.

## Plan with the affected services

- Record intended signals and any exceptions in the affected service
  continuation and coverage document. Link the actual environment and release.
- Use the [dt-obs plan](../../dt-obs/assets/observability-plan.md) to connect app
  journeys to source, runtime, verification and owner.
- Use the [ingestion authentication matrix](../../dt-obs/references/otel.md#ingestion-endpoints-and-authentication)
  and [bounded tenant checks](../../dt-obs/references/dql-verification.md) when implementing or verifying instrumentation.

## Evidence

Carry issue, PR, check, deployment and runtime references through the delivery
record. Apply the [evidence contract](evidence.md) to the actual revision, run,
artifact and verified outcomes. Keep missing access and failed checks visible.
