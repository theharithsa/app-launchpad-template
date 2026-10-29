import json
from pathlib import Path
import unittest
from unittest.mock import patch
import test_foundation as fixtures
from contracts import *
from schema_validation import validate_shape, validate_record
from check_links import check_links
import repository_ruleset

ROOT = fixtures.ROOT

class ContractTests(unittest.TestCase):
    setUp = fixtures.FoundationTests.setUp

    def test_schema_keys_statuses_and_patterns_match_constants(self):
        schema = lambda name: json.loads((ROOT/'schemas'/f'{name}.schema.json').read_text())
        project, catalog, evidence = (schema(name) for name in ('project','catalog','evidence'))
        for document, required in ((project,PROJECT_REQUIRED),(catalog,CATALOG_REQUIRED),(evidence,EVIDENCE_REQUIRED)):
            self.assertEqual(document['properties']['schemaVersion']['const'],SCHEMA_VERSION)
            self.assertEqual(document['required'],list(required))
        self.assertEqual(project['properties']['template']['properties']['version']['pattern'],SEMVER_PATTERN)
        self.assertEqual(project['properties']['decisions']['required'],list(DECISIONS))
        self.assertEqual(project['$defs']['decision']['properties']['status']['enum'],list(DECISION_STATUSES))
        self.assertTrue(all(item == {'$ref':'#/$defs/decision'} for item in project['properties']['decisions']['properties'].values()))
        service=catalog['properties']['services']['items'];skill=catalog['properties']['skills']['items']
        self.assertEqual(service['required'],list(SERVICE_REQUIRED))
        self.assertEqual(skill['required'],list(SKILL_REQUIRED))
        self.assertEqual(service['properties']['status']['enum'],list(SERVICE_STATUSES))
        check=evidence['properties']['checks']['items']
        self.assertEqual(check['required'],list(CHECK_REQUIRED))
        self.assertEqual(check['properties']['status']['enum'],list(CHECK_STATUSES))

    def test_shape_constraints_accumulate_and_reject_wrong_types(self):
        record={'schemaVersion':True,'application':'','checks':[{'status':'imaginary'}], 'lifecycle':[]}
        errors=validate_record(ROOT,'evidence',record)
        self.assertGreater(len(errors),5)
        self.assertTrue(any('schemaVersion' in e for e in errors))
        self.assertTrue(any('checks[0].status' in e for e in errors))
        self.assertTrue(any('lifecycle' in e for e in errors))
        self.assertTrue(validate_shape('2026-02-31T12:00:00Z',{'format':'date-time'}))
        self.assertTrue(validate_shape(-1,{'type':'number','minimum':0}))
        self.assertEqual(validate_shape(1.0,{'type':'integer','const':1}),[])
        self.assertTrue(validate_shape(True,{'type':'integer','const':1}))
        self.assertTrue(validate_shape(float('nan'),{'type':'number'}))
        self.assertEqual(validate_shape(10**1000,{'type':'number','minimum':0}),[])

    def test_synthetic_evidence_and_sample_schema_pointers(self):
        value=json.loads((ROOT/'examples/evidence.json').read_text())
        self.assertEqual(validate_record(ROOT,'evidence',value),[])
        self.assertIn('SYNTHETIC',value['application'])
        for name in ('project.json','skills/catalog.json','qa/evidence.json','examples/evidence.json'):
            file=ROOT/name
            pointer=json.loads(file.read_text())['$schema']
            self.assertTrue((file.parent/pointer).is_file(),name)

    def test_links_check_hidden_files_spaces_references_and_code_fences(self):
        root=self.base/'links';(root/'.github').mkdir(parents=True)
        (root/'with space.md').write_text('# Target')
        file=root/'.github/instructions.md'
        file.write_text('[ok](../with%20space.md)\n[bad][x]\n[x]: ../missing.md\n```sh\n[example](../not-real.md)\n```\n')
        errors=check_links(root)
        self.assertEqual(len(errors),1,errors)
        self.assertIn('missing.md',errors[0])
        (root/'missing.md').write_text('resolved')
        self.assertEqual(check_links(root),[])

    def test_ci_and_catalog_share_the_check_entrypoint(self):
        data=json.loads((ROOT/'skills/catalog.json').read_text())
        service=next(s for s in data['services'] if s['id']=='foundation-tooling')
        import re
        executed=re.findall(r'^\s+run:\s*(.+)$',(ROOT/'.github/workflows/foundation.yml').read_text(),re.MULTILINE)
        self.assertEqual(service['testCommands'],executed)
        self.assertEqual(executed,['sh scripts/check.sh'])
        # Exercise the entrypoint's execution/early-exit contract without recursively running tests.
        import os,subprocess
        bin_dir=self.base/'bin';bin_dir.mkdir();calls=self.base/'calls'
        fake=bin_dir/'python3'
        fake.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$CHECK_CALLS"\ncase "$*" in *check_links*) exit "${CHECK_LINK_EXIT:-0}";; esac\n')
        fake.chmod(0o755)
        env={**os.environ,'PATH':str(bin_dir)+os.pathsep+os.environ['PATH'],'CHECK_CALLS':str(calls)}
        good=subprocess.run(['sh',str(ROOT/'scripts/check.sh')],env=env,capture_output=True)
        self.assertEqual(good.returncode,0)
        self.assertEqual(calls.read_text().splitlines(),['scripts/check_foundation.py','scripts/check_links.py','-m unittest discover -s tests -v'])
        calls.write_text('');env['CHECK_LINK_EXIT']='3'
        bad=subprocess.run(['sh',str(ROOT/'scripts/check.sh')],env=env,capture_output=True)
        self.assertEqual(bad.returncode,3)
        self.assertEqual(len(calls.read_text().splitlines()),2)

    def test_ruleset_default_preview_never_calls_github(self):
        import contextlib,io
        output=io.StringIO()
        with patch.object(repository_ruleset,'gh_json',side_effect=AssertionError('Network in dry-run')),contextlib.redirect_stdout(output):
            repository_ruleset.main(['--repo','example-owner/example-project'])
        plan=json.loads(output.getvalue())
        self.assertTrue(plan['dryRun'])
        self.assertEqual(plan['payload']['bypass_actors'],[])
        self.assertEqual({rule['type'] for rule in plan['payload']['rules']},{'deletion','non_fast_forward','pull_request','required_status_checks'})
        checks=next(rule for rule in plan['payload']['rules'] if rule['type']=='required_status_checks')
        self.assertEqual(checks['parameters']['required_status_checks'],[{'context':'foundation'}])

    def test_ruleset_apply_updates_by_name_and_verifies(self):
        import contextlib,io
        payload=repository_ruleset.build_ruleset()
        calls=[]
        def fake(arguments,value=None):
            calls.append((arguments,value))
            if '--paginate' in arguments:return [[{'id':7,'name':repository_ruleset.NAME}]]
            return {'id':7,**payload}
        with patch.object(repository_ruleset,'gh_json',side_effect=fake),contextlib.redirect_stdout(io.StringIO()):
            repository_ruleset.main(['--repo','example-owner/example-project','--apply'])
        self.assertIn('PUT',calls[1][0])
        self.assertEqual(calls[1][1],payload)
        self.assertEqual(calls[2][0],['repos/example-owner/example-project/rulesets/7'])
