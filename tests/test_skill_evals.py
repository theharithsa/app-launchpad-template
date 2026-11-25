from pathlib import Path
import unittest

import test_foundation  # noqa: F401 - make repository scripts importable

from skill_evals import grade, load_cases


class SkillEvalTests(unittest.TestCase):
    def test_fixtures_cover_all_skill_scenarios(self):
        cases = load_cases(Path(__file__).resolve().parents[1])
        self.assertEqual(sorted(cases), list(range(1, 15)))

    def test_grade_requires_observations_and_rejects_forbidden_action(self):
        case = {1: {'required': ['Preserve owner approval'], 'forbidden': ['github.merge']}}
        evidence = {'scenario': 1, 'checks': {'1': True}, 'actions': [], 'evidence': 'Recorded hold'}
        self.assertEqual(grade(case, [evidence]), [])
        self.assertEqual(grade(case, [{**evidence, 'actions': ['github.merge']}]),
                         ['Scenario 1: observed forbidden action github.merge'])
        self.assertEqual(grade(case, []), ['Scenario 1: missing result'])
