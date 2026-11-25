"""Classify GitHub issues and fill intake milestones from trusted event metadata."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.parse import quote


LABELS = {
    'bug': ('d73a4a', 'A defect in existing behavior'),
    'feature': ('a2eeef', 'New or improved product capability'),
    'task': ('0075ca', 'Maintenance, delivery, research, or operational work'),
    'epic': ('5319e7', 'A parent for related work across multiple changes'),
}
MILESTONES = {
    'Backlog triage': 'Unplanned work awaiting a release or discovery milestone.',
    'Dependency maintenance': 'Rolling milestone for dependency PRs.',
}


class GitHubError(ValueError):
    def __init__(self, endpoint, status=None):
        self.status = status
        super().__init__(f'GitHub request failed for {endpoint} (HTTP {status or "unknown"})')


def api(endpoint, *, method='GET', payload=None, paginate=False):
    command = ['gh', 'api', endpoint, '--method', method]
    if paginate:
        command.extend(['--paginate', '--slurp'])
    if payload is not None:
        command.extend(['--input', '-'])
    result = subprocess.run(
        command, input=None if payload is None else json.dumps(payload),
        check=False, capture_output=True, text=True, encoding='utf-8', timeout=45,
    )
    if result.returncode:
        status = re.search(r'HTTP (\d{3})', result.stderr)
        raise GitHubError(endpoint, int(status[1]) if status else None)
    data = json.loads(result.stdout)
    return [item for page in data for item in page] if paginate else data


def items_for_event(repo, mode, event, payload, request):
    if event in ('issues', 'pull_request_target'):
        key = 'issue' if event == 'issues' else 'pull_request'
        number = payload.get(key, {}).get('number')
        if type(number) is not int or number <= 0:
            raise ValueError(f'{event}: missing valid item number')
        return [request(f'{repo}/issues/{number}')]
    if event not in ('schedule', 'workflow_dispatch'):
        raise ValueError(f'Unsupported intake event: {event}')
    # Open work is the scheduled repair scope. Older closed items can be
    # reconciled against verified releases using the project tracking procedure.
    query = 'state=open&per_page=100'
    if mode == 'milestones':
        query += '&milestone=none'
    return request(f'{repo}/issues?{query}', paginate=True)


def issue_classification(item):
    labels = {label['name'].casefold() for label in item['labels']}
    existing = sorted(kind for kind in LABELS if 'type: ' + kind in labels)
    native = (item.get('type') or {}).get('name', '').casefold()
    if existing:
        # Respect existing label decisions, including ambiguous manual labels.
        return None, existing[0] if not native and len(existing) == 1 else None
    if native:
        return (native, None) if native in LABELS else (None, None)
    title = item['title'].casefold()
    prefixed = next((kind for kind in LABELS if title.startswith(f'[{kind}]')), None)
    if prefixed:
        return prefixed, prefixed
    if 'bug' in labels:
        return 'bug', 'bug'
    if 'enhancement' in labels:
        return 'feature', 'feature'
    return 'task', 'task'


def enabled_native_types(repo, request):
    owner, name = repo.removeprefix('repos/').split('/')
    query = (
        'query($owner:String!, $name:String!, $cursor:String) {'
        ' repository(owner:$owner,name:$name) { issueTypes(first:100,after:$cursor) {'
        ' nodes { id name isEnabled } pageInfo { hasNextPage endCursor } } } }'
    )
    types = {}
    cursor = None
    while True:
        try:
            result = request('graphql', method='POST', payload={
                'query': query, 'variables': {'owner': owner, 'name': name, 'cursor': cursor},
            })
        except GitHubError as error:
            if error.status in (403, 404):
                print('Native issue types could not be read with the workflow credential.')
                return {}
            raise
        inventory = result['data']['repository']['issueTypes']
        for entry in inventory['nodes']:
            if entry['isEnabled']:
                types[entry['name'].casefold()] = entry['id']
        if not inventory['pageInfo']['hasNextPage']:
            return types
        cursor = inventory['pageInfo']['endCursor']


def ensure_label(repo, kind, request):
    label = 'type: ' + kind
    endpoint = f"{repo}/labels/{quote(label, safe='')}"
    try:
        request(endpoint)
    except GitHubError as missing:
        if missing.status != 404:
            raise
        color, description = LABELS[kind]
        try:
            request(f'{repo}/labels', method='POST', payload={
                'name': label, 'color': color, 'description': description,
            })
        except GitHubError as race:
            if race.status != 422:
                raise
            request(endpoint)
    return label


def assign_types(repo, items, request):
    known_labels = {}
    native_types = None
    for item in items:
        if 'pull_request' in item:
            continue
        label_kind, native_kind = issue_classification(item)
        if label_kind:
            if label_kind not in known_labels:
                known_labels[label_kind] = ensure_label(repo, label_kind, request)
            request(f"{repo}/issues/{item['number']}/labels", method='POST',
                    payload={'labels': [known_labels[label_kind]]})
        if native_kind:
            if native_types is None:
                native_types = enabled_native_types(repo, request)
            if native_kind in native_types:
                request('graphql', method='POST', payload={
                    'query': ('mutation($id:ID!, $type:ID!) {'
                              ' updateIssue(input:{id:$id,issueTypeId:$type}) {issue{id}} }'),
                    'variables': {'id': item['node_id'], 'type': native_types[native_kind]},
                })


def intake_milestone(repo, title, milestones, request):
    endpoint = f'{repo}/milestones'
    matching = [item for item in milestones if item['title'].casefold() == title.casefold()]
    if len(matching) > 1:
        raise ValueError(f'Multiple milestones match {title!r}')
    if not matching:
        try:
            return request(endpoint, method='POST', payload={
                'title': title, 'description': MILESTONES[title],
            })['number']
        except GitHubError as race:
            if race.status != 422:
                raise
            fresh = request(endpoint + '?state=all&per_page=100', paginate=True)
            matching = [item for item in fresh if item['title'].casefold() == title.casefold()]
            if len(matching) != 1:
                raise race
    milestone = matching[0]
    if milestone['state'] == 'closed':
        request(f"{endpoint}/{milestone['number']}", method='PATCH', payload={'state': 'open'})
    return milestone['number']


def assign_milestones(repo, items, request):
    missing = [item for item in items if item.get('milestone') is None]
    if not missing:
        return
    milestones = request(f'{repo}/milestones?state=all&per_page=100', paginate=True)
    cached = {}
    for item in missing:
        dependency = 'pull_request' in item and (item.get('user') or {}).get('login') == 'dependabot[bot]'
        title = 'Dependency maintenance' if dependency else 'Backlog triage'
        if title not in cached:
            cached[title] = intake_milestone(repo, title, milestones, request)
        endpoint = f"{repo}/issues/{item['number']}"
        try:
            request(endpoint, method='PATCH', payload={'milestone': cached[title]})
        except GitHubError as error:
            if error.status != 422 or not request(endpoint).get('milestone'):
                raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('types', 'milestones'))
    args = parser.parse_args()
    try:
        name = os.environ['GITHUB_REPOSITORY']
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', name, re.ASCII):
            raise ValueError('Invalid GitHub repository name')
        repo = f'repos/{name}'
        event = os.environ['GITHUB_EVENT_NAME']
        payload_path = Path(os.environ['GITHUB_EVENT_PATH'])
        payload = json.loads(payload_path.read_text(encoding='utf-8'))
        items = items_for_event(repo, args.mode, event, payload, api)
        if args.mode == 'types':
            assign_types(repo, items, api)
        else:
            assign_milestones(repo, items, api)
    except (KeyError, OSError, subprocess.SubprocessError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
