# Machine-readable contracts

| Record | JSON Schema |
| --- | --- |
| Project/discovery and template provenance | [project.schema.json](project.schema.json) |
| Workflow/service routing and ownership | [catalog.schema.json](catalog.schema.json) |
| Actual execution evidence | [evidence.schema.json](evidence.schema.json) |

All contracts fix schemaVersion at 1 and use JSON Schema 2020-12. Sample `$schema` pointers are relative; the gate ignores instance-supplied schema URIs and never fetches remote content.

Schemas own field shapes. `scripts/schema_validation.py` executes the used subset with the standard library (type, required/properties, const/enum, pattern/minLength, items/minItems, minimum, allOf/if/then, local $ref and timestamp format). Python domain checks add filesystem safety, unique identities, graph/reference integrity and discovery readiness. No jsonschema runtime package is required.

When changing a field, enum, required key or validator behavior, update schema, Python constants/domain checks, tests and examples together. Standard-library parity tests compare required keys/statuses/patterns; behavior tests exercise malformed inputs and domain semantics. New schema keywords need evaluator support and tests before use. Additional metadata keys remain allowed for compatible extension.
