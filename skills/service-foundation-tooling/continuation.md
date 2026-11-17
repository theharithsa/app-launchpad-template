# Foundation tooling continuation

- Scope: Iteration 2 issues #46, #47, #52, #53, #58 and #74; Windows portability, encoding, version consistency and reviewed tooling inventory.
- Source reviewed: the full `origin/main` commit recorded as `lastReviewedRevision` in [catalog](../catalog.json), the v1.14.1 baseline. It is an inspected source pointer, not proof of this candidate's CI.
- Implemented: cross-platform relative-path rejection and bounded traversal; lock handle closed before deletion; explicit UTF-8/LF I/O; configurable Python executable; bounded test subprocesses; isolated privilege-sensitive symlink test; root changelog version guard; Git-backed review-revision warnings.
- CI: Linux and Windows run the shared check command with encoding warnings as errors. The required `foundation` gate waits for both jobs. PR evidence must identify the checked head and actual run; inspect it before merge.
- Verification: local candidate checks and remote CI are recorded in the implementing PR. A passing foundation gate covers repository tooling and curated docs, not a generated application's behavior or runtime telemetry.
- Delivery: issue-linked implementation PR; merge, release and any resulting Pages publication are separate evidence states. No application runtime, database migration, ingestion credentials or tenant writes are involved.
- Recovery: revert the implementing commit through a PR. After interrupted generation inspect active processes, catalog and output before removing a stale `.catalog.lock` or `.catalog.next`. Never delete another process's lock or existing output.
- Remaining: the later CI/lint expansion (#54), validator/link-checker hardening and skill-quality epics remain outside this patch. Consumer projects adopt selected updates through reviewed PRs and preserve their own configuration.
- Next action: check the implementing PR's current-head Windows/Linux results, then perform the authorized merge/release procedure. Do not infer publication from a local check or an open PR.
