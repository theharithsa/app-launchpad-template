# Foundation checks

Python 3.11+ and a POSIX shell (Git Bash or WSL on Windows); standard library only.
Git is needed for revision diagnostics and their tests. The required `foundation`
check aggregates Linux and Windows jobs; both must pass. Each job runs with
default-encoding warnings treated as errors.

```sh
sh scripts/check.sh
# Windows Git Bash, when Python is installed as python rather than python3:
PYTHON=python sh scripts/check.sh
# Strict encoding audit (use python instead of python3 on Windows):
python3 -X warn_default_encoding -W error::EncodingWarning -m unittest discover -s tests
python3 scripts/check_foundation.py --json
python3 scripts/check_foundation.py --ready --json
```

The shared entrypoint validates metadata, versions, skills, local Markdown links, the public documentation build and its HTML links, and unit tests. In PR CI it also requires a documentation impact decision in the PR body. README, catalog and CI use the same entrypoint. Foundation validator JSON includes `ok`, deterministic `errors`, and `ready` (whether discovery checks were requested). Failures exit nonzero.

The [schemas](../schemas/README.md) own field shapes. The Python gate adds internal-path/reference/dependency checks and ready/active semantics. Tests cover multi-error diagnostics, malformed structures, schema/constant parity, SemVer, service generation and rollback, link failures, CI command agreement and ruleset dry-run behavior.

For actual application suites follow the [test contract](../.agents/skills/app-launchpad/references/testing.md) and [evidence rules](../.agents/skills/app-launchpad/references/evidence.md). Record real commands/prerequisites in the relevant service skill after stack selection. `examples/` is synthetic reference material and never execution proof or a cataloged service. Raw local artifacts remain ignored under `qa/local/` or `qa/raw/`.

`PYTHON` selects one executable (a quoted path may contain spaces), not a command
plus arguments. On Windows, use `py -3` to locate/install Python if needed, then
set `PYTHON` to that executable; `PYTHON="py -3"` is not supported. UTF-8 mode is
not required. Symlink tests skip only when the platform denies or lacks symlink
creation; path, collision and lock tests still run. Missing review commits produce
a warning when Git history is available; fetch history or review and refresh the
continuation. Source archives can validate without Git history.
