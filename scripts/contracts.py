"""Shared contract constants; schemas and tests track changes together."""
SCHEMA_VERSION = 1
DECISIONS = ('product', 'stack', 'hosting', 'privacy', 'observability', 'license')
DECISION_STATUSES = ('needs-user-input', 'proposed', 'approved', 'not-applicable')
SERVICE_STATUSES = ('planned', 'active', 'retired')
CHECK_STATUSES = ('passed', 'failed', 'skipped', 'not-run', 'blocked')
PROJECT_REQUIRED = ('schemaVersion', 'name', 'template', 'decisions')
CATALOG_REQUIRED = ('schemaVersion', 'skills', 'services')
EVIDENCE_REQUIRED = ('schemaVersion', 'application', 'revision', 'release', 'checks', 'limits', 'lifecycle')
SKILL_REQUIRED = ('id', 'kind', 'path', 'description', 'dependsOn')
SERVICE_REQUIRED = ('id', 'skillId', 'sourcePaths', 'entrypoints', 'owner', 'status', 'dependsOn',
                    'contracts', 'testCommands', 'continuation', 'lastReviewedRevision')
CHECK_REQUIRED = ('id', 'status', 'revision', 'command', 'observedAt', 'environment', 'artifact')
SEMVER_PATTERN = r'^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-((?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*)(?:\.(?:0|[1-9][0-9]*|[0-9]*[A-Za-z-][0-9A-Za-z-]*))*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$'
