import json
from pathlib import Path
import subprocess
import sys
import unittest
import test_foundation as fixtures
ROOT = fixtures.ROOT
from skill_catalog import validate_catalog

class CatalogTests(unittest.TestCase):
    setUp = fixtures.FoundationTests.setUp
    fixture = fixtures.FoundationTests.fixture

    def catalog(self, root, change):
        file = root / 'skills/catalog.json'
        data = json.loads(file.read_text())
        change(data)
        file.write_text(json.dumps(data))

    def generate(self, root, *args):
        return subprocess.run([sys.executable, str(ROOT / 'scripts/add_service_skill.py'),
                               '--root', str(root), *args], capture_output=True, text=True)

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
        original = skill.read_text()
        skill.unlink()
        self.assertTrue(validate_catalog(root))
        skill.write_text(original.replace('name: project-design', 'name: mismatched'))
        self.assertTrue(validate_catalog(root))
        skill.write_text(original)
        extra = root / 'skills/uncataloged/SKILL.md'
        extra.parent.mkdir()
        extra.write_text(original)
        self.assertTrue(validate_catalog(root))

    def test_rejects_cycles_duplicates_or_service_without_skill(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_text()
        changes = [lambda d: d['skills'].append(d['skills'][0]),
                   lambda d: d['skills'][0].update(dependsOn=['project-design']),
                   lambda d: d['skills'][0].update(dependsOn=['missing']),
                   lambda d: d['services'][0].update(skillId='missing'),
                   lambda d: d['services'].clear()]
        for change in changes:
            (root / 'skills/catalog.json').write_text(before)
            self.catalog(root, change)
            self.assertTrue(validate_catalog(root))

    def test_active_service_requires_real_paths_owner_and_commands(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_text()
        self.assertEqual(validate_catalog(root), [])
        changes = [{'owner': None}, {'testCommands': []}, {'entrypoints': []},
                   {'sourcePaths': ['nonexistent']}, {'entrypoints': ['missing.py']},
                   {'continuation': 'missing.md'}, {'lastReviewedRevision': 'fake'}]
        for change in changes:
            (root / 'skills/catalog.json').write_text(before)
            self.catalog(root, lambda d: d['services'][0].update(change))
            self.assertTrue(validate_catalog(root))

    def test_generation_rejects_unsafe_paths_symlinks_existing_output_and_lock(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_bytes()
        for value in ('../outside', '/absolute'):
            result = self.generate(root, '--id', 'synthetic', '--source-path', value)
            self.assertNotEqual(result.returncode, 0)
        external = self.base / 'external'
        external.mkdir()
        link = root / 'linked'
        link.symlink_to(external, target_is_directory=True)
        self.assertNotEqual(self.generate(root, '--id', 'synthetic', '--source-path', 'linked/code').returncode, 0)
        destination = root / 'skills/service-synthetic'
        destination.mkdir()
        keep = destination / 'keep.txt'
        keep.write_text('preserve')
        self.assertNotEqual(self.generate(root, '--id', 'synthetic', '--source-path', 'src').returncode, 0)
        self.assertEqual(keep.read_text(), 'preserve')
        lock = root / 'skills/.catalog.lock'
        lock.write_text('other process')
        self.assertNotEqual(self.generate(root, '--id', 'other', '--source-path', 'src').returncode, 0)
        self.assertEqual(lock.read_text(), 'other process')
        self.assertFalse((root / 'skills/service-other').exists())
        self.assertEqual((root / 'skills/catalog.json').read_bytes(), before)

    def test_generation_rolls_back_on_catalog_temp_collision(self):
        root = self.fixture()
        before = (root / 'skills/catalog.json').read_bytes()
        temporary = root / 'skills/.catalog.next'
        temporary.write_text('preserve external work')
        self.assertNotEqual(self.generate(root, '--id', 'synthetic', '--source-path', 'src').returncode, 0)
        self.assertFalse((root / 'skills/service-synthetic').exists())
        self.assertFalse((root / 'skills/.catalog.lock').exists())
        self.assertEqual(temporary.read_text(), 'preserve external work')
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
        file.write_text('---\nname: example-only\ndescription: Synthetic fixture.\n---\n')
        self.assertEqual(validate_catalog(root), [])
