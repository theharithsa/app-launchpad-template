"""Prepare and grade recorded App Launchpad skill walkthroughs."""

import argparse
import json
from pathlib import Path
import re


def load_cases(root):
    reference = root / '.agents/skills/app-launchpad/references/scenarios.md'
    numbers = [int(number) for number in re.findall(r'(?m)^(\d+)\. ', reference.read_text(encoding='utf-8'))]
    cases = {}
    for file in sorted((root / 'evals/app-launchpad').glob('*.json')):
        data = json.loads(file.read_text(encoding='utf-8'))
        number = data.get('scenario')
        if type(number) is not int or number in cases:
            raise ValueError(f'{file.name}: invalid or duplicate scenario number')
        for key in ('prompt', 'fixture'):
            if not isinstance(data.get(key), str) or not data[key].strip():
                raise ValueError(f'{file.name}: missing {key}')
        for key in ('required', 'forbidden'):
            values = data.get(key)
            if (not isinstance(values, list) or not values
                    or any(not isinstance(value, str) or not value.strip() for value in values)):
                raise ValueError(f'{file.name}: missing {key} criteria')
        cases[number] = data
    if not numbers or sorted(cases) != numbers:
        raise ValueError('Evaluation fixtures must cover every numbered scenario exactly once')
    return cases


def grade(cases, results):
    if not isinstance(results, list):
        return ['Expected an array of recorded results']
    observed = set()
    errors = []
    for result in results:
        number = result.get('scenario') if isinstance(result, dict) else None
        if type(number) is not int or number not in cases or number in observed:
            errors.append(f'Unexpected or duplicate result for scenario {number!r}')
            continue
        observed.add(number)
        case = cases[number]
        checks = result.get('checks')
        expected = {str(index) for index in range(1, len(case['required']) + 1)}
        if not isinstance(checks, dict) or set(checks) != expected:
            errors.append(f'Scenario {number}: incomplete rubric')
        else:
            for key in sorted(expected):
                if checks[key] is not True:
                    errors.append(f'Scenario {number}: required behavior {key} did not pass')
        actions = result.get('actions')
        if not isinstance(actions, list) or any(not isinstance(action, str) for action in actions):
            errors.append(f'Scenario {number}: missing action record')
        else:
            for action in sorted(set(actions).intersection(case['forbidden'])):
                errors.append(f'Scenario {number}: observed forbidden action {action}')
        if not isinstance(result.get('evidence'), str) or not result['evidence'].strip():
            errors.append(f'Scenario {number}: missing observed evidence')
    for number in sorted(cases.keys() - observed):
        errors.append(f'Scenario {number}: missing result')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--case', type=int)
    mode.add_argument('--results', type=Path)
    parser.add_argument('--rubric', action='store_true')
    args = parser.parse_args()
    try:
        cases = load_cases(Path(__file__).resolve().parents[1])
        if args.case is not None:
            case = dict(cases[args.case])
            if not args.rubric:
                case.pop('required')
                case.pop('forbidden')
            print(json.dumps(case, indent=2))
            return
        results = json.loads(args.results.read_text(encoding='utf-8'))
        errors = grade(cases, results)
        for error in errors:
            print(f'ERROR: {error}')
        if errors:
            raise SystemExit(1)
        print(f'{len(cases)} recorded skill evaluations passed their rubrics.')
    except (KeyError, OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
