# Baseline repository protection

This is an opt-in repository administration change under the [authorization policy](../.agents/skills/app-launchpad/references/safety.md). Template generation and CI never execute it.

Preview the exact target and payload locally (no GitHub request):

```sh
python3 scripts/repository_ruleset.py --repo OWNER/REPOSITORY
```

After the owner authorizes that settings change, apply and verify with the connected `gh` account:

```sh
python3 scripts/repository_ruleset.py --repo OWNER/REPOSITORY --apply
```

The baseline protects main (`--branch` selects another actual branch): PR required, the **foundation** status context required with an up-to-date base, resolved review threads, no force pushes and no branch deletion. No bypass actors are granted. The workflow title is Foundation checks, but the required check context is foundation.

Zero mandatory approvals supports the sole-owner repository; CODEOWNERS identifies ownership but does not manufacture an independent reviewer. Teams should agree their review count/code-owner requirements separately. Application checks are additional project-specific requirements, not covered by the foundation check.

The script finds only its named `app-launchpad-main` ruleset, creates it or updates it idempotently, and reads it back to verify the submitted constraints. It does not alter unrelated rulesets. Multiple matching names or verification failure stop for inspection. Authorization must cover an update to an existing named ruleset. Read-only verification:

```sh
gh api repos/OWNER/REPOSITORY/rules/branches/main
```

The [GitHub rulesets API](https://docs.github.com/en/rest/repos/rules) is the platform contract. Required settings are verified through GitHub state, not inferred from green CI.
