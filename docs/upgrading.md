# Upgrade an existing App Launchpad project

A generated repository owns its application code and decisions. Compare the
template versions, choose the pieces to adopt, and review them in the app's
own PR. Start with a clean worktree.

## Walkthrough from v1.12.0 to v1.14.3

Use the versions recorded in your project's metadata and the release you plan
to adopt. This example uses two published versions. Namespaced refs keep the
app's own version tags independent.

```sh
git switch -c upgrade-app-launchpad
git remote add app-launchpad https://github.com/theharithsa/app-launchpad-template.git
git fetch --no-tags app-launchpad \
  refs/tags/v1.12.0:refs/app-launchpad/v1.12.0 \
  refs/tags/v1.14.3:refs/app-launchpad/v1.14.3
git diff --stat refs/app-launchpad/v1.12.0 refs/app-launchpad/v1.14.3
git diff refs/app-launchpad/v1.12.0 refs/app-launchpad/v1.14.3 -- \
  .agents/skills scripts schemas tests .github/workflows docs
git rev-parse 'refs/app-launchpad/v1.14.3^{commit}'
```

If the remote already exists, verify its URL with
`git remote get-url app-launchpad` and continue with fetch. Check the target
commit against the [published v1.14.3 release](https://github.com/theharithsa/app-launchpad-template/releases/tag/v1.14.3).

| Changed paths | Action when adopting |
| --- | --- |
| `.agents/skills/`, `skills/catalog.json`, `scripts/`, `schemas/`, `tests/` | Keep compatible skill, catalog, validator and test changes together. Merge local skill and service entries. |
| `.github/workflows/foundation.yml` and `.github/pull_request_template.md` | Adopt the shared checks and PR documentation decision where the project uses this workflow. Verify required-check names in the app's own settings. |
| `docs/` and `TEMPLATE_VERSION` | Apply the relevant workflow guidance. Keep the app's own decisions, changelog, owners and evidence. |
| `site/`, `docs/public-guides.json` and `.github/workflows/product-pages.yml` | Optional product site starter. Merge it only when the app wants this Pages workflow. Preserve its existing content and deploy target. |

Review each file's diff against the app. If a selected file is unchanged from
the old template, you can restore just that file from the target revision.
Use a three-way review for edited files. Here is a command for the unmodified
foundation workflow after inspecting its diff:

```sh
git diff refs/app-launchpad/v1.12.0 -- .github/workflows/foundation.yml
git restore --source refs/app-launchpad/v1.14.3 -- .github/workflows/foundation.yml
```

For a full foundation upgrade, synchronize the target template version in
`TEMPLATE_VERSION`, README, `project.json.template.version`, the bundled App
Launchpad skill and template changelog. Set `project.json.template.revision`
to the peeled commit shown above. Merge the catalog entries and upstream
skill versions for the selected bundle. Keep the app's name, decisions and
service inventory.

For a partial adoption, record the adopted paths, upstream version and
commit in [delivery](delivery.md). Retain accurate baseline provenance.
Run `sh scripts/check.sh`, the app's relevant tests and any affected
deployment workflow checks. Record the result and open the app's PR.

For a read-only list of upstream changes and local overlap, run `python3 scripts/template_upgrade.py --to v1.14.3` after fetching the refs above. The command reads your recorded source commit and existing Git refs. Review each reported overlap in your adoption PR.

The [template changelog](template-changelog.md) describes versioned changes.
Use the tag-to-tag diff for the exact paths in older releases.
