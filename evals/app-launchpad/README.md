# App Launchpad skill evaluations

Each numbered fixture mirrors a scenario in the [skill walkthroughs](../../.agents/skills/app-launchpad/references/scenarios.md). Use a disposable repository, mocked remote state and a reviewer who can inspect the actual response and actions. Run the assistant with the proposed skill and the fixture only.

1. Run `python3 scripts/skill_evals.py --case 1` to get the prompt and environment facts.
2. Capture the response and tool calls. Use `--case 1 --rubric` after the run to inspect the required outcomes and prohibited action identifiers.
3. Record a JSON array with one result per case. Each result has `scenario`, `checks` keyed by the rubric's numbered identifiers, `actions` with normalized action identifiers from the trace, and `evidence` describing the observed result. Mark a check true only when the trace or response demonstrates it.
4. Run `python3 scripts/skill_evals.py --results path/to/results.json`. Missing cases, failed checks and observed forbidden actions fail the run. Record the checked skill revision, model, fixture scope and actual outcomes in the skill-changing PR or release evidence.

Example result for one case:

```json
{
  "scenario": 1,
  "checks": {"1": true, "2": true},
  "actions": ["local.read"],
  "evidence": "The response asked who can book and whether payment is required, then offered stack options."
}
```

The foundation suite validates coverage and the results parser. A fixture check
does not establish model behavior. Keep actual evaluation results with their
review evidence.
