# Sampling, masking, retention and cost

## Choose and verify sampling

For consistent head sampling, use an SDK parent-based ratio policy where
supported. Choose a root ratio by volume and follow the accepted parent
sampled flag at downstream services. Decide which trace behavior is
appropriate at untrusted boundaries. Record the actual SDK configuration and
test both retained and dropped traces.

Tail sampling in a Collector can consider completed traces, errors and
latency. Route all spans of a trace to the same decision point and size the
buffer, decision delay and memory for expected traffic. A head sampler that
dropped a trace upstream makes it unavailable to tail sampling. Measure
collector drops and retained trace shape. Use a known retained synthetic trace
for verification and report missing stored spans independently of transport.

Metrics and authoritative business records have their own collection and
deduplication policies. Do not apply a trace sampling percentage to their
totals.

## Estimate and review usage

| Signal | Measure to establish the budget |
| --- | --- |
| Traces | Request rate, spans per trace, sampled fraction, stored bytes and query scope |
| Logs | Events and bytes ingested, stored duration, and query scan volume |
| Metrics | Number of instrument series, attribute cardinality, emission interval and metric data points |
| Events | Domain/lifecycle event rate, duplicate/retry rate, payload size, retention and query usage |
| RUM | Monitored sessions, enabled capabilities, page/action volume and replay volume |

Use the tenant's actual subscription, capability allowances and rate card.
Estimate with observed volume, then compare in pre-production and after an
approved release. Record sampling configuration, volume, cost owner, budget
and alert thresholds. [Dynatrace subscription and usage](https://docs.dynatrace.com/docs/license)

## Mask and retain

Apply the allowlist and masking at production or SDK capture before export.
Use an authorized OpenPipeline processing step as a second layer for residual
sensitive fields. Test input, processing, forwarding and the resulting stored
record on synthetic cases. Confirm raw credentials, private values and
unapproved identifiers are absent from stored and forwarded data.

Choose the existing bucket when its ownership, retention and access policies
fit. Add a dedicated bucket only when its storage and access boundaries are
needed and approved. Record retention duration, data class, read access,
deletion behavior and query impact. Verify routing with one bounded query
before scaling. [OpenPipeline processing](https://docs.dynatrace.com/docs/platform/openpipeline/concepts/processing)
