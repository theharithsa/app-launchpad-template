---
name: project-testing
description: Choose and run risk-based checks for project and service changes. Use when verifying a candidate or reproducing a behavior in a controlled test. Do not use to approve production promotion.
---

# Project Testing

- Read the service prerequisites and real test commands. [Service context](../../.agents/skills/app-launchpad/references/services.md).
- Choose unit/API/integration/browser/telemetry/release coverage for risk. [Test contract](../../.agents/skills/app-launchpad/references/testing.md).
- Record actual revision, execution, results and safe artifacts. [Evidence](../../.agents/skills/app-launchpad/references/evidence.md).
- For this foundation run `sh scripts/check.sh`; app checks are separate. [Local tooling](../../docs/testing.md).
