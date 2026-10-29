# Template versioning

`TEMPLATE_VERSION` is the authoritative version of the reusable template foundation. The current requested label is **1.09.0**. README, `project.json` → `template.version`, and the newest versioned `docs/template-changelog.md` section must agree with that file; foundation CI checks consistency.

## Version policy

This template uses a three-part numeric release label `major.minor.patch`, preserving the requested `1.09.0` spelling. It is not strict SemVer because the minor component has a leading zero. Do not pass it to tooling that requires strict SemVer without an explicitly agreed mapping. The label's three numeric components communicate compatibility:

- Patch: compatible fixes/documentation adjustments, for example `1.09.1`.
- Minor: compatible new foundation capabilities, for example `1.10.0`.
- Major: incompatible metadata/schema/workflow changes requiring consumer migration, for example `2.0.0`.

Record compatibility and migration impact in the changelog. The initial recorded version is 1.09.0; earlier unversioned commits remain historical facts, not invented past releases. Bundled third-party skill versions and licenses remain independent.

## Update and release

1. Create/reuse the issue and work through a PR. Choose the next label based on compatibility and user direction; update TEMPLATE_VERSION, README, project template metadata and the newest template changelog section together.
2. Run foundation validation, relevant tests, skill and link checks. Document actual results and current-head CI. Preserve the last reviewed source revision and continuation pointers separately from the template version.
3. Merge only when authorized and checks/review pass. A versioned source merge is not automatically a published GitHub release, deployed application or verified tenant signal.
4. When tag/release publication is requested or otherwise authorized, create a new immutable tag `v<LABEL>` at the verified merge revision and publish reviewed release notes. Verify the remote tag/commit and release URL. Never move or reuse a published tag. This change records version 1.09.0 in source; tag/release publication is a separate state.

## Generated projects and upgrades

On generation record the source template version and exact source commit in `project.json`. TEMPLATE_VERSION tracks the copied foundation; application package versions, release tags and API contract versions have their own approved policies. Generated applications may keep their own release history in root CHANGELOG.md; foundation checks read the separate docs/template-changelog.md to avoid mixing those histories. Do not overwrite the template provenance with an app version.

Template updates do not automatically synchronize consumers. Apply selected changes through an issue-linked PR, preserve product/service-specific instructions, record migrations, and update template version/provenance only after adoption. Keep README/changelog provenance consistent with the copied foundation. Use `docs/release-plan.md` and each service's continuation to distinguish source adoption from app deployment.
