# Service and module inventory

The machine-readable inventory is `skills/catalog.json` → `services`. The template includes one real module, `foundation-tooling`, with its own service skill. It has no implemented application services. Before implementing each real service or independently maintained module, register it with `scripts/add_service_skill.py` and maintain its skill and continuation file.

For an existing application, inspect the actual source/runtime/deployment topology first and enumerate every service here or in the catalog. Review that inventory against the architecture on each PR. CI verifies declared mappings and catches uncataloged skill files; it cannot infer that undeclared source code is a service.

Keep dependencies, source paths, entrypoints, contract links, ownership, actual test commands and lifecycle state current in the catalog. Update service-specific design, policy/data, deploy/rollback, observability and handoff details alongside code changes. Use planned/active/retired deliberately; do not leave implemented services marked planned to avoid checks.
