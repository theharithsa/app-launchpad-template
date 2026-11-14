#!/usr/bin/env python3
"""Verify that a pull request records its documentation decision."""
import json
import os
from pathlib import Path
import re


def has_decision(body):
    body = body.replace('\r\n', '\n')
    visible_body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
    visible_body = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1[ \t]*$', '', visible_body,
                          flags=re.MULTILINE | re.DOTALL)
    section = re.search(
        r'^## Documentation impact[ \t]*\n(.*?)(?=^#{1,2} |\Z)',
        visible_body,
        flags=re.MULTILINE | re.DOTALL,
    )
    return section is not None and re.search(
        r'^(?:Updated|No change):[ \t]+\S.*$', section[1], flags=re.MULTILINE
    ) is not None


if __name__ == '__main__':
    if os.getenv('GITHUB_EVENT_NAME') != 'pull_request':
        print('Documentation impact is checked on pull requests.')
    else:
        event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
        body = event['pull_request']['body'] or ''
        if not has_decision(body):
            raise SystemExit(
                'Add a Documentation impact section with '
                '"Updated: <affected guides>" or "No change: <reason>".'
            )
        print('The PR records a documentation decision. Review the explanation and affected guides.')
