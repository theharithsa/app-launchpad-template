# Foundation tooling continuation

Inherited template tooling is ready for a local foundation check. The new repository's owner, CI results, ruleset and Project settings need their own evidence.

- Run sh scripts/check.sh on the current source. Confirm the required check and branch rules on GitHub if configured.
- Record the reviewer, source SHA, check links and any pending setup in this file. Set the service owner and status in the catalog after verification.
- Change tooling through an issue-linked PR. If service registration stops midway, inspect the working tree and active processes before recovering a stale catalog lock.
