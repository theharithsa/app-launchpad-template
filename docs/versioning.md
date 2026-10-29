# Template versioning

`TEMPLATE_VERSION` is authoritative. README, project template metadata and the newest [template changelog](template-changelog.md) section agree with it under CI. Application/API and bundled upstream skill versions are independent.

## SemVer

Use [SemVer 2.0.0](https://semver.org/): patch for compatible fixes, minor for compatible additions, major for incompatible contracts requiring migration. Numeric identifiers have no leading zeros. Prerelease/build syntax is supported by the validator.

The first valid template release is **1.9.0**. Earlier source carried the explicitly requested custom label `1.09.0`; issue #18 replaces that convention. No tag/release was published under the old label. Record that correction without inventing historical releases.

## Update and release

- Follow the [delivery owner](../.agents/skills/app-launchpad/references/github-release.md) and [authorization owner](../.agents/skills/app-launchpad/references/safety.md).
- Update TEMPLATE_VERSION, README, project template metadata and the newest template changelog together; record compatibility/migration impact.
- Run `sh scripts/check.sh`, relevant app checks and current-head CI. Record inspected source revision and continuation evidence independently of version.
- After an authorized verified merge, publish a new immutable tag `v<VERSION>` at that merge. Verify remote tag/commit and any separately requested release publication; never move/reuse a published tag.

## Consumer migration

- Record source template version/commit on generation; retain provenance when app versions change.
- Adopt selected template updates through a reviewed PR, preserving product/service-specific decisions, data and skill content. Update provenance only for changes actually adopted.
- Root CHANGELOG.md may become the app history; retain template history separately in docs/template-changelog.md.
- This baseline removes `.agents/skills/app-launchpad/scripts/bootstrap.py` and its partial assets. Replace old callers with GitHub template generation or explicitly pending adoption. Other metadata stays schemaVersion 1 with published schemas; no application deployment or data migration is implied.
