import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import test_foundation  # noqa: F401 - make repository scripts importable

from template_upgrade import report


class UpgradeTests(unittest.TestCase):
    def test_report_flags_local_edits_and_creates_no_changes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            def git(*args):
                return subprocess.check_output(['git', *args], cwd=root, encoding='utf-8').strip()

            def write(name, text):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text, encoding='utf-8', newline='\n')

            def commit(label):
                git('add', '-A')
                git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.test',
                    '-c', 'commit.gpgsign=false', 'commit', '-qm', label)
                return git('rev-parse', 'HEAD')

            git('init', '-q')
            write('TEMPLATE_VERSION', '1.9.0\n')
            write('docs/delivery.md', 'Initial delivery.\n')
            previous = commit('Published snapshot')
            write('TEMPLATE_VERSION', '1.14.3\n')
            write('docs/delivery.md', 'Changed template delivery.\n')
            write('docs/upgrading.md', 'New instructions.\n')
            write('src/app.py', 'Template-independent code.\n')
            target = commit('Target template')
            git('update-ref', 'refs/app-launchpad/v1.14.3', target)
            git('switch', '--detach', previous)
            write('project.json', json.dumps({'template': {'version': '1.9.0', 'revision': previous}}))
            write('docs/delivery.md', 'Adopter delivery customization.\n')
            write('docs/upgrading.md', 'Untracked local notes.\n')
            before = git('status', '--porcelain=v1')
            planned = report(root, 'v1.14.3')
            self.assertEqual(planned['to']['revision'], target)
            changes = {row['path']: row for row in planned['changes']}
            self.assertTrue(changes['docs/delivery.md']['localChanges'])
            self.assertTrue(changes['docs/upgrading.md']['localChanges'])
            self.assertFalse(changes['TEMPLATE_VERSION']['localChanges'])
            self.assertNotIn('src/app.py', changes)
            self.assertEqual(git('status', '--porcelain=v1'), before)
            with self.assertRaisesRegex(ValueError, 'unavailable locally'):
                report(root, 'v2.0.0')
