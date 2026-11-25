# Instrumentation coexistence and configuration as code

Inventory existing agents, SDK providers and Collector routes first. Select
one owner for each signal and workload boundary, then verify actual stored data.

| Existing environment | Apply |
| --- | --- |
| VM or supported process monitored by OneAgent | Use supported native instrumentation for platform and automatic spans. Add explicit SDK instrumentation for missing business and dependency boundaries. |
| Kubernetes with Dynatrace Operator | Use the Operator for supported injection and topology. Choose one OTLP destination for each enabled SDK signal and verify the operator's actual injected configuration. |
| Application-owned SDK on serverless or a portable runtime | Initialize a single provider per signal before instrumented libraries and export along the approved route. |
| Shared Collector | Use one supported collector/export path for aggregation, sampling or normalization. Verify TLS, credentials, backpressure and signal ownership. |

When the OneAgent OpenTelemetry Span Sensor handles a provider's spans,
exporting that same span stream over OTLP can duplicate it. Select one
ingestion path for those spans. Existing native OneAgent coverage may still
own separate signals. Run one known synthetic request and compare span
names, counts, trace links and service topology against the expected
boundaries. Inspect metrics and logs separately.

Use `service.version` and the deployment environment for runtime identity.
`build.commit` is an app-defined attribute for the exact built commit. Record
the checked head to merge to deploy mapping explicitly. In SDLC records,
use the [documented VCS and deployment fields](sdlc.md#choose-the-event-route)
where they match those facts.

## Version tenant settings

For each resource record its owner, tenant, stable ID or parent, source path,
required scopes and recovery operation. Version SLOs, dashboards, notebooks,
anomaly detectors and OpenPipeline configuration in the appropriate repo.
Keep secret values outside source.

- Select pinned Terraform, Monaco or dtctl according to each resource's
  supported operations. Use the tenant's effective auth policy.
- Record the current resource identity and create a checked plan or dry run.
  Review apply/delete behavior, data routing and cost implications.
- Apply only approved changes to the named environment. Read back actual
  configuration and verify the expected query, alert, SLO or pipeline behavior.
- Keep previous definitions and artifact/commit IDs. Recheck permissions,
  routing and outcomes after restoring a prior configuration.

[OneAgent and OTel options](https://docs.dynatrace.com/docs/ingest-from/opentelemetry) · [Dynatrace configuration as code](https://docs.dynatrace.com/docs/deliver/configuration-as-code)
