import json
import errno
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import warnings
import test_foundation as fixtures
ROOT = fixtures.ROOT
from skill_catalog import safe_path, validate_catalog, warn_unavailable_revision

class CatalogTests(unittest.TestCase):
    setUp = fixtures.FoundationTests.setUp
    fixture = fixtures.FoundationTests.fixture

    def catalog(self, root, change):
        file = root / 'skills/catalog.json'
        data = json.loads(file.read_text(encoding='utf-8'))
        change(data)
        file.write_text(json.dumps(data), encoding='utf-8', newline='\n')

    def generate(self, root, *args):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/add_service_skill.py'),
                               '--root', str(root), *args], capture_output=True, text=True, timeout=10, encoding='utf-8')

    def test_registration_dry_run_round_trip_and_duplicate_preservation(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_bytes()
        args = ('--id', 'synthetic-api', '--source-path', 'src/api')
        dry = self.generate(root, *args, '--dry-run')
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual((root / 'skills/catalog.json').read_bytes(), before)
        self.assertFalse((root / 'skills/service-synthetic-api').exists())
        result = self.generate(root, *args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(validate_catalog(root), [])
        generated = (root / 'skills/service-synthetic-api/SKILL.md').read_bytes()
        updated = (root / 'skills/catalog.json').read_bytes()
        self.assertNotEqual(self.generate(root, *args).returncode, 0)
        self.assertEqual((root / 'skills/catalog.json').read_bytes(), updated)
        self.assertEqual((root / 'skills/service-synthetic-api/SKILL.md').read_bytes(), generated)
        self.assertFalse((root / 'src').exists())

    def test_rejects_missing_skill_or_uncataloged_skill(self):
        root = self.fixture()
        skill = root / 'skills/project-design/SKILL.md'
        original = skill.read_text(encoding='utf-8')
        skill.unlink()
        self.assertTrue(validate_catalog(root))
        skill.write_text(original.replace('name: project-design', 'name: mismatched'), encoding='utf-8', newline='\n')
        self.assertTrue(validate_catalog(root))
        skill.write_text(original, encoding='utf-8', newline='\n')
        extra = root / 'skills/uncataloged/SKILL.md'
        extra.parent.mkdir()
        extra.write_text(original, encoding='utf-8', newline='\n')
        self.assertTrue(validate_catalog(root))

    def test_rejects_cycles_duplicates_or_service_without_skill(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_text(encoding='utf-8')
        changes = [lambda d: d['skills'].append(d['skills'][0]),
                   lambda d: d['skills'][0].update(dependsOn=['project-design']),
                   lambda d: d['skills'][0].update(dependsOn=['missing']),
                   lambda d: d['services'][0].update(skillId='missing'),
                   lambda d: d['services'].clear()]
        for change in changes:
            (root / 'skills/catalog.json').write_text(before, encoding='utf-8', newline='\n')
            self.catalog(root, change)
            self.assertTrue(validate_catalog(root))

    def test_active_service_requires_real_paths_owner_and_commands(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_text(encoding='utf-8')
        self.assertEqual(validate_catalog(root), [])
        changes = [{'owner': None}, {'testCommands': []}, {'entrypoints': []},
                   {'sourcePaths': ['nonexistent']}, {'entrypoints': ['missing.py']},
                   {'continuation': 'missing.md'}, {'lastReviewedRevision': 'fake'}]
        for change in changes:
            (root / 'skills/catalog.json').write_text(before, encoding='utf-8', newline='\n')
            self.catalog(root, lambda d: d['services'][0].update(change))
            self.assertTrue(validate_catalog(root))

    def test_generation_rejects_unsafe_paths_existing_output_and_lock(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_bytes()
        for value in ('../outside', '/absolute', 'C:x', 'C:/absolute', '\\rooted', '//host/share'):
            result = self.generate(root, '--id', 'synthetic', '--source-path', value)
            self.assertNotEqual(result.returncode, 0)
        destination = root / 'skills/service-synthetic'
        destination.mkdir()
        keep = destination / 'keep.txt'
        keep.write_text('preserve', encoding='utf-8', newline='\n')
        self.assertNotEqual(self.generate(root, '--id', 'synthetic', '--source-path', 'src').returncode, 0)
        self.assertEqual(keep.read_text(encoding='utf-8'), 'preserve')
        lock = root / 'skills/.catalog.lock'
        lock.write_text('other process', encoding='utf-8', newline='\n')
        self.assertNotEqual(self.generate(root, '--id', 'other', '--source-path', 'src').returncode, 0)
        self.assertEqual(lock.read_text(encoding='utf-8'), 'other process')
        self.assertFalse((root / 'skills/service-other').exists())
        self.assertEqual((root / 'skills/catalog.json').read_bytes(), before)

    def create_symlink_or_skip(self, link, target):
        try:
            link.symlink_to(target, target_is_directory=True)
        except OSError as error:
            if error.errno in (errno.EPERM, errno.EACCES, errno.ENOSYS, errno.EOPNOTSUPP) or getattr(error, 'winerror', None) == 1314:
                self.skipTest('Platform cannot create symlinks: ' + str(error))
            raise

    def test_generation_rejects_symlink_ancestry(self):
        root = self.fixture()
        external = self.base / 'external'
        external.mkdir()
        self.create_symlink_or_skip(root / 'linked', external)
        result = self.generate(root, '--id', 'synthetic', '--source-path', 'linked/code')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Symlink path is not allowed', result.stderr)

    def test_symlink_permission_failure_skips_instead_of_erroring(self):
        with patch.object(Path, 'symlink_to', side_effect=PermissionError(errno.EPERM, 'No symlink privilege')):
            with self.assertRaises(unittest.SkipTest):
                self.create_symlink_or_skip(self.base / 'link', self.base)

    def test_safe_paths_reject_other_platform_roots_and_allow_nested_paths(self):
        for value in ('/x', 'C:x', 'C:/x', '\\x', '//server/share', '../x', 'a/../../x'):
            with self.subTest(path=value), self.assertRaisesRegex(ValueError, 'safe repository-relative path'):
                safe_path(self.base, value)
        self.assertEqual(safe_path(self.base, 'src/nested'), self.base / 'src/nested')

    def test_revision_warning_uses_real_git_history_and_preserves_archive_support(self):
        root = self.base / 'history'
        root.mkdir()
        def git(*args):
            return subprocess.run(['git', *args], cwd=root, capture_output=True, text=True,
                                  encoding='utf-8', timeout=10, check=True)
        git('init')
        git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
            '-c', 'commit.gpgsign=false', 'commit', '--allow-empty', '-m', 'Synthetic history')
        revision = git('rev-parse', 'HEAD').stdout.strip()
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            warn_unavailable_revision(root, 'synthetic', revision)
            self.assertEqual(caught, [])
        with self.assertWarnsRegex(RuntimeWarning, 'lastReviewedRevision .* does not resolve locally'):
            warn_unavailable_revision(root, 'synthetic', 'f' * 40)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter('always')
            warn_unavailable_revision(self.base, 'archive', 'f' * 40)
            with patch('skill_catalog.subprocess.run', side_effect=FileNotFoundError):
                warn_unavailable_revision(root, 'no-git', 'f' * 40)
            self.assertEqual(caught, [])

    def test_unicode_paths_and_lf_generation(self):
        root = self.fixture()
        result = self.generate(root, '--id', 'unicode', '--source-path', 'src/café-東京')
        self.assertEqual(result.returncode, 0, result.stderr)
        catalog = (root / 'skills/catalog.json').read_bytes()
        skill = (root / 'skills/service-unicode/SKILL.md').read_bytes()
        self.assertIn('café-東京', skill.decode('utf-8'))
        self.assertNotIn(b'\r\n', catalog)
        self.assertNotIn(b'\r\n', skill)
        self.assertFalse((root / 'skills/.catalog.lock').exists())

    def test_generation_rolls_back_on_catalog_temp_collision(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_bytes()
        temporary = root / 'skills/.catalog.next'
        temporary.write_text('preserve external work', encoding='utf-8', newline='\n')
        self.assertNotEqual(self.generate(root, '--id', 'synthetic', '--source-path', 'src').returncode, 0)
        self.assertFalse((root / 'skills/service-synthetic').exists())
        self.assertFalse((root / 'skills/.catalog.lock').exists())
        self.assertEqual(temporary.read_text(encoding='utf-8'), 'preserve external work')
        self.assertEqual((root / 'skills/catalog.json').read_bytes(), before)

    def test_multiple_errors_are_reported_together_in_stable_order(self):
        root = self.fixture()
        self.catalog(root, lambda d: (d['skills'][0].update(dependsOn=['missing-one']),
                                     d['services'][0].update(owner=None, entrypoints=['missing-entrypoint.py'],
                                                             continuation='missing-continuation.md')))
        errors = validate_catalog(root)
        self.assertEqual(errors, sorted(set(errors)))
        for marker in ('missing-one', 'owner', 'missing-entrypoint.py', 'missing-continuation.md'):
            self.assertTrue(any(marker in error for error in errors), (marker, errors))
        self.assertEqual(errors, validate_catalog(root))
        self.catalog(root, lambda d: d['skills'][0].update(id=None, path='missing-skill.md'))
        errors = validate_catalog(root)
        self.assertTrue(any('missing-skill.md' in error for error in errors), errors)
        self.assertTrue(any('skills[0].id' in error for error in errors), errors)

    def test_examples_are_not_discovered_as_live_skills(self):
        root = self.fixture()
        file = root / 'examples/web/SKILL.md'
        file.parent.mkdir(parents=True)
        file.write_text('---\nname: example-only\ndescription: Synthetic fixture.\n---\n', encoding='utf-8', newline='\n')
        self.assertEqual(validate_catalog(root), [])
