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
