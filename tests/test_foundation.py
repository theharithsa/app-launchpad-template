import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('foundation', ROOT / 'scripts/check_foundation.py')
foundation = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foundation)
BOOTSTRAP = ROOT / '.agents/skills/app-launchpad/scripts/bootstrap.py'

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
        return root

    def bootstrap(self, target, name='Synthetic app', *flags):
        return subprocess.run([sys.executable, str(BOOTSTRAP), '--target', str(target),
                               '--name', name, *flags], capture_output=True, text=True)

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

    def test_bootstrap_dry_run_and_json_escaping(self):
        target = self.base / 'new'
        self.assertEqual(self.bootstrap(target, 'App "quoted" \\ example', '--dry-run').returncode, 0)
        self.assertFalse(target.exists())
        result = self.bootstrap(target, 'App "quoted" \\ example')
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads((target / 'qa/evidence.json').read_text())
        self.assertEqual(evidence['application'], 'App "quoted" \\ example')
        self.assertEqual(evidence['checks'], [])
        self.assertIsNone(evidence['lifecycle']['mergeSha'])

    def test_bootstrap_collision_preserves_existing_work(self):
        target = self.base / 'existing'
        (target / 'qa').mkdir(parents=True)
        existing = target / 'qa/evidence.json'
        existing.write_text('keep this')
        self.assertNotEqual(self.bootstrap(target).returncode, 0)
        self.assertEqual(existing.read_text(), 'keep this')
        self.assertFalse((target / 'AGENTS.md').exists())

    def test_bootstrap_refuses_symlink_ancestry_and_empty_name(self):
        real = self.base / 'real'
        real.mkdir()
        link = self.base / 'link'
        link.symlink_to(real, target_is_directory=True)
        self.assertNotEqual(self.bootstrap(link / 'child').returncode, 0)
        self.assertEqual(list(real.iterdir()), [])
        self.assertNotEqual(self.bootstrap(self.base / 'empty', ' ').returncode, 0)

if __name__ == '__main__':
    unittest.main()
