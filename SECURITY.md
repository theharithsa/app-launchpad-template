# Security and privacy

Never commit secrets, customer exports, raw production logs, or private screenshots. Keep privileged configuration server-side and use the selected provider's secret store or supported short-lived identity. `.env.example` may contain names and safe examples only.

Do not publish security vulnerabilities in public issues. Use a verified private reporting channel agreed with the repository owner; none is configured by this template. Configure a project-specific reporting policy before accepting external reports.

Record auth/tenant boundaries, telemetry field allowlists, consent, retention, deletion and cost decisions before implementation. Session Replay requires separate approval. Tests use isolated synthetic data; production writes need explicit authorization.
