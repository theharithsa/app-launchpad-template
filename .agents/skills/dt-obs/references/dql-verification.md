# Bounded DQL verification

Start with the approved environment, an exact candidate identity and a short
window that covers the scenario. Replace the synthetic values in these examples.
Keep results limited to safe fields. Increase the window only to cover an
explained ingestion delay or a recorded occurrence time.

Verified the syntax of these eight statements against a Dynatrace tenant on
26 November 2026. Each statement has a bounded timeframe. Synthetic values
remain placeholders for the adopter's data and field mappings. Use the actual
tenant results to decide whether a signal is searchable.

## Trace and release

Replace the service, version, environment and trace ID with the values observed on the candidate.

```dql
fetch spans, from: -15m, to: now()
| filter service.name == "example-profile" and service.version == "1.4.0"
    and deployment.environment.name == "preprod" and toString(trace.id) == "<trace-id>"
| fields start_time, trace.id, span.id, span.name, service.version
| limit 20
```

## Logs joined to a trace

Confirm the tenant's native log correlation field. The fallback handles an approved custom string field. Project identifiers and severity for the check.

```dql
fetch logs, from: -15m, to: now()
| filter service.name == "example-profile" and service.version == "1.4.0"
| fields log_time = timestamp, loglevel, trace_key = coalesce(toString(trace.id), toString(trace_id))
| filter trace_key == "<trace-id>"
| join [
    fetch spans, from: -15m, to: now()
    | filter service.name == "example-profile" and service.version == "1.4.0"
        and toString(trace.id) == "<trace-id>"
    | fields trace_key = toString(trace.id), span.id, span.name
  ], on: {trace_key}, kind: inner, fields: {span.id, span.name}
| limit 20
```

## One committed business event

Use the original CloudEvent ID and provider. Deduplicate the stable ID before aggregation. Count deliveries separately when investigating retries.

```dql
fetch bizevents, from: -15m, to: now()
| filter event.provider == "example.profile-api" and event.id == "<event-id>"
| fields timestamp, event.id, event.type, transaction.id
| dedup event.id, sort: {timestamp desc}
| limit 20
```

## Custom request counter

Replace the metric key and dimensions with ones actually exported. Check the returned timeseries values and units.

```dql
timeseries requests = sum(`example.profile.request.count`), from: -15m, to: now(), interval: 1m,
  filter: {service.name == "example-profile" and deployment.environment.name == "preprod"}
| limit 1
```

## RUM and backend join

Use an approved request ID property present on both the RUM event and server span. Filter to the intended frontend and environment where available. This join establishes application correlation. Verify native RUM-to-trace navigation separately.

```dql
fetch user.events, from: -15m, to: now()
| filter request.id == "<request-id>"
| fields rum_time = timestamp, request.id, event.type
| join [
    fetch spans, from: -15m, to: now()
    | filter service.name == "example-profile" and service.version == "1.4.0" and request.id == "<request-id>"
    | fields request.id, trace.id, span.id, span.name
  ], on: {request.id}, kind: inner, fields: {trace.id, span.id, span.name}
| limit 20
```

## Davis deployment annotation

Use the recorded deployment title and add the verified target or event identifier if it is available. Check the Events API receipt for per-result status.

```dql
fetch dt.davis.events, from: -15m, to: now()
| filter event.type == "CUSTOM_DEPLOYMENT" and event.name == "<deployment-title>"
| fields timestamp, event.id, event.name, event.type
| limit 20
```

## SDLC source event

Use the project's stable source ID field and expected source version. For a deployment, cross-check the deployment ID, outcome and field mapping from the ingested source.

```dql
fetch events, from: -15m, to: now()
| filter event.kind == "SDLC_EVENT" and sdlc.event.id == "<source-event-id>"
| fields timestamp, event.provider, event.type, event.status, sdlc.event.id, cicd.deployment.release_stage, vcs.ref.base.revision
| limit 20
```

## Smartscape service

Look up the service in Smartscape and use its returned ID to narrow subsequent queries.

```dql
smartscapeNodes "SERVICE", from: -15m, to: now()
| filter name == "example-profile"
| fields id, name, type
| limit 20
```

[Dynatrace DQL reference](https://docs.dynatrace.com/docs/platform/grail/dynatrace-query-language)
