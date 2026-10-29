# Evidence and authority

- Plans/catalogs describe coverage, never execution. Record passed, failed, skipped, not-run and blocked distinctly with timestamp, exact revision, command/tool, environment and safe artifact reference.
- Source merge, release publication, deployed configuration, HTTP/ingest acceptance (including partial rejection), tenant searchability, cross-signal joins and native RUM-to-trace navigation are separate states. A printed ID/202 or custom string join cannot prove later stages.
- GitHub owns repository transitions; runners own actual test/check execution; deployment systems own artifact/environment facts; application commits own durable business outcomes; RUM is client-observed.
- Preserve originating run/attempt/revision, real leaf-case statuses and stable retry IDs. Test results also record start/end/duration and tool/browser, independently of planned case catalogs. Reporting spans describe reporting, not fabricated historical execution. Retain failed, cancelled, skipped, timed-out, partial, closed-unmerged, reopened and rollback facts.
- When application deployment succeeds and reporting fails, preserve that success and retry reporting with original identities; do not repeat successful customer operations or deployment.
- Verify stored handoff claims against current code/Git/CI/provider/tenant evidence. Unknown or unavailable stages remain pending; historical captures retain their original version/time.
- Keep raw local evidence ignored and safe CI artifacts bounded by known retention/expiry. Synthetic screenshots need review, viewport/browser/zoom, version, file hash and asset inventory. Browser emulation does not certify physical devices, Safari, IME or production writes.

Detailed signal verification: [Dynatrace](observability.md). Execution records: the project's `schemas/evidence.schema.json`. Release checks: [delivery](github-release.md).
