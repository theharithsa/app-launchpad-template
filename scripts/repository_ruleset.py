#!/usr/bin/env python3
"""Preview a main-branch ruleset; --apply explicitly changes the named repository."""
import argparse
import json
import re
import subprocess

NAME = 'app-launchpad-main'


def build_ruleset(branch='main'):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._/-]*', branch) or '..' in branch:
        raise ValueError('Invalid branch name')
    return {
        'name': NAME, 'target': 'branch', 'enforcement': 'active', 'bypass_actors': [],
        'conditions': {'ref_name': {'include': ['refs/heads/' + branch], 'exclude': []}},
        'rules': [
            {'type': 'deletion'}, {'type': 'non_fast_forward'},
            {'type': 'pull_request', 'parameters': {
                'required_approving_review_count': 0, 'dismiss_stale_reviews_on_push': False,
                'require_code_owner_review': False, 'require_last_push_approval': False,
                'required_review_thread_resolution': True}},
            {'type': 'required_status_checks', 'parameters': {
                'required_status_checks': [{'context': 'foundation'}],
                'strict_required_status_checks_policy': True}}
        ]}


def gh_json(arguments, payload=None):
    result = subprocess.run(['gh', 'api', *arguments], input=None if payload is None else json.dumps(payload),
                            text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def contains(actual, expected):
    if isinstance(expected, dict):
        return isinstance(actual, dict) and all(key in actual and contains(actual[key], value) for key, value in expected.items())
    if isinstance(expected, list):
        return isinstance(actual, list) and len(actual) == len(expected) and all(
            any(contains(item, wanted) for item in actual) for wanted in expected)
    return actual == expected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, help='Explicit owner/repository target')
    parser.add_argument('--branch', default='main')
    parser.add_argument('--apply', action='store_true', help='Authorized settings mutation (default: local preview only)')
    args = parser.parse_args(argv)
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9][A-Za-z0-9_.-]*', args.repo):
        parser.error('Expected explicit owner/repository')
    try:
        payload = build_ruleset(args.branch)
        endpoint = f'repos/{args.repo}/rulesets'
        if not args.apply:
            print(json.dumps({'dryRun': True, 'repository': args.repo, 'operation': 'upsert-by-name',
                              'endpoint': endpoint, 'payload': payload}, indent=2))
            return
        pages = gh_json(['--paginate', '--slurp', endpoint + '?per_page=100'])
        matches = [item for page in pages for item in page if item.get('name') == NAME]
        if len(matches) > 1:
            raise ValueError('Multiple matching rulesets; resolve them manually')
        target = endpoint + ('/' + str(matches[0]['id']) if matches else '')
        receipt = gh_json(['--method', 'PUT' if matches else 'POST', target, '--input', '-'], payload)
        verified = gh_json([endpoint + '/' + str(receipt['id'])])
        if not contains(verified, payload):
            raise ValueError('Ruleset saved but verification differs; inspect settings before retrying')
        print(json.dumps({'dryRun': False, 'repository': args.repo, 'id': receipt['id'],
                          'verified': True, 'ruleset': verified}, indent=2))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f'Ruleset operation failed: {error}\n')

if __name__ == '__main__':
    main()
