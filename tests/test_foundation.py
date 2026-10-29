import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('foundation', ROOT / 'scripts/check_foundation.py')
foundation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foundation)

class FoundationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()

    def fixture(self):
        root = self.base / 'repo'
        for name in (*foundation.REQUIRED, 'project.json'):
            output = root / name
            output.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, output)
        for name in ('scripts', 'skills', '.agents', 'schemas', 'docs'):
            shutil.copytree(ROOT / name, root / name, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__'))
        return root

    def test_discovery_gate_requires_decisions_and_provenance(self):
        root = self.fixture()
        self.assertEqual(foundation.validate(root), [])
        self.assertTrue(foundation.validate(root, ready=True))
        project = json.loads((root / 'project.json').read_text())
        project['name'] = 'Synthetic app'
        project['template']['revision'] = 'a' * 40
        for key in foundation.DECISIONS:
            project['decisions'][key] = {'status': 'approved', 'value': 'Synthetic choice', 'approval': 'Test fixture'}
        (root / 'project.json').write_text(json.dumps(project))
        self.assertEqual(foundation.validate(root, ready=True), [])
        project['decisions']['hosting']['approval'] = None
        (root / 'project.json').write_text(json.dumps(project))
        self.assertTrue(foundation.validate(root, ready=True))

    def test_malformed_configuration_and_missing_files_fail(self):
        root = self.fixture()
        for invalid in ('[]', '{broken', '{"schemaVersion":1,"decisions":[]}'):
            (root / 'project.json').write_text(invalid)
            self.assertTrue(foundation.validate(root))
        (root / 'AGENTS.md').unlink()
        (root / 'qa/evidence.json').write_text('[]')
        self.assertTrue(any('Missing required' in error for error in foundation.validate(root)))
        self.assertTrue(any('evidence' in error for error in foundation.validate(root)))

    def test_version_metadata_and_release_notes_must_agree(self):
        root = self.fixture()
        (root / 'CHANGELOG.md').write_text('# Application changelog\n\n## [7.0.0]')
        self.assertEqual(foundation.validate(root), [])
        for name, replacement in [('TEMPLATE_VERSION', '1.09.0'), ('README.md', 'stale version'),
                                  ('docs/template-changelog.md', '# Template changelog\n\n## [0.0.0]')]:
            file = root / name
            before = file.read_text()
            file.write_text(replacement)
            self.assertTrue(foundation.validate(root), name)
            file.write_text(before)
        project = json.loads((root / 'project.json').read_text())
        project['template']['version'] = '0.0.0'
        (root / 'project.json').write_text(json.dumps(project))
        self.assertTrue(foundation.validate(root))

    def test_non_json_numeric_constants_are_rejected(self):
        root = self.fixture()
        project = json.loads((root/'project.json').read_text())
        project['extra'] = float('nan')
        (root/'project.json').write_text(json.dumps(project))
        errors = foundation.validate(root)
        self.assertTrue(any('Invalid JSON numeric constant' in error for error in errors), errors)

    def test_semver_identifiers(self):
        from contracts import SEMVER_PATTERN
        for good in ('0.0.0','1.9.0','1.10.0','1.9.0-rc.1','1.9.0+build.09'):
            self.assertIsNotNone(re.fullmatch(SEMVER_PATTERN, good), good)
        for bad in ('01.9.0','1.09.0','1.9.00','1.9.0-01','1.9','v1.9.0','1.9.0-'):
            self.assertIsNone(re.fullmatch(SEMVER_PATTERN, bad), bad)

    def test_json_output_and_failure_exit_status(self):
        command = [sys.executable, str(ROOT/'scripts/check_foundation.py'), '--root', str(ROOT), '--json']
        result = subprocess.run(command, capture_output=True, text=True)
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(payload, {'ok': True, 'errors': [], 'ready': False})
        result = subprocess.run(command+['--ready'], capture_output=True, text=True)
        payload = json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(payload['ok'])
        self.assertTrue(payload['ready'])
        self.assertEqual(payload['errors'], sorted(set(payload['errors'])))
