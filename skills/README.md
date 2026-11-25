# Skills catalog

Use [App Launchpad task routing](../.agents/skills/app-launchpad/SKILL.md#task-routing)
for the canonical workflow and its project checklist. Use the
[catalog](catalog.json) to find affected service skills, dependencies and
continuation records.

## Register a service

```sh
python3 scripts/add_service_skill.py --id SERVICE_ID --source-path ACTUAL_SOURCE_DIRECTORY --dry-run
python3 scripts/add_service_skill.py --id SERVICE_ID --source-path ACTUAL_SOURCE_DIRECTORY
```

Replace arguments with the actual architecture. The command creates a planned service skill, continuation and metadata; it does not create application code. Read the [owning service policy](../.agents/skills/app-launchpad/references/services.md) for required upkeep and the [tooling skill](service-foundation-tooling/SKILL.md) for mechanics/recovery.

## Contracts and examples

- [Catalog schema](../schemas/catalog.schema.json), [project schema](../schemas/project.schema.json), [evidence schema](../schemas/evidence.schema.json) own metadata fields; see [schema maintenance](../schemas/README.md).
- [Policy ownership map](../docs/policy-map.md) routes cross-cutting rules.
- [Synthetic examples](../examples/README.md) demonstrate completed shapes; they are not registered services or actual evidence.
- Run `sh scripts/check.sh`. See [checks](../docs/testing.md) and [inventory](../docs/services.md).
