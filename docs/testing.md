# Tests and evidence

Foundation checks (Python 3.11+; standard library):

```sh
python3 scripts/check_foundation.py
python3 -m unittest discover -s tests -v
python3 scripts/check_foundation.py --ready
```

The first two are template checks. `--ready` is an intentionally stricter discovery gate and fails on the unconfigured template. None establishes application correctness, deployment or tenant searchability.

After stack selection, document actual commands, dependencies and coverage here and add executable CI jobs. Cover domain/policy, real API denial/conflict/retry, isolated integration services and primary browser journeys as applicable. Do not use an echo job as a passing test. Keep test plans separate from execution evidence. See [testing reference](../.agents/skills/app-launchpad/references/testing.md).

`qa/evidence.json` starts empty. Add actual timestamped command/tool, source revision, environment, status and safe artifact references; no template test may pre-populate app successes. Raw evidence stays ignored under `qa/local` or `qa/raw`; review synthetic assets before publication.

Catalog checks are included in foundation validation: unique skill/service IDs, matching skill frontmatter, catalog completeness, internal references, dependency graphs and active service prerequisites. Generator tests exercise safe registration, dry run, duplicate preservation, path/symlink refusal, catalog locks and rollback. These checks do not infer undeclared services or certify that instructions match application behavior; review those against the service inventory in each PR.

Template version checks enforce a three-part numeric label and agreement between TEMPLATE_VERSION, README, project template provenance and the newest template changelog version (docs/template-changelog.md). Root application changelogs are independent. This allows the explicitly chosen 1.09.0 label without claiming strict SemVer. Tests exercise malformed version data and independently stale copies.
