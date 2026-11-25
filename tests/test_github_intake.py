import unittest
from unittest.mock import Mock

import test_foundation  # noqa: F401 - make repository scripts importable

from github_intake import GitHubError, assign_milestones, assign_types, issue_classification, items_for_event


class IntakeTests(unittest.TestCase):
    def test_existing_label_and_native_type_take_precedence(self):
        self.assertEqual(issue_classification({
            'labels': [{'name': 'type: feature'}], 'type': {'name': 'Bug'}, 'title': '[Bug] hi',
        }), (None, None))
        self.assertEqual(issue_classification({
            'labels': [], 'type': {'name': 'Epic'}, 'title': '[Task] hi',
        }), ('epic', None))
        self.assertEqual(issue_classification({
            'labels': [], 'type': {'name': 'Bug'}, 'title': '[Task] hi',
        }), ('bug', None))
        self.assertEqual(issue_classification({
            'labels': [{'name': 'type: epic'}], 'type': None, 'title': 'Discovery',
        }), (None, 'epic'))

    def test_event_reads_only_its_item(self):
        api = Mock(return_value={'number': 42})
        data = items_for_event('repos/org/app', 'types', 'issues', {'issue': {'number': 42}}, api)
        self.assertEqual(data, [{'number': 42}])
        api.assert_called_once_with('repos/org/app/issues/42')
        with self.assertRaisesRegex(ValueError, 'missing valid item number'):
            items_for_event('repos/org/app', 'types', 'issues', {'issue': {'number': '../../'}}, api)

    def test_board_epic_gets_label_without_native_replacement(self):
        api = Mock(return_value={})
        assign_types('repos/org/app', [{'number': 42, 'labels': [], 'type': {'name': 'Epic'}}], api)
        self.assertEqual(api.call_count, 2)
        api.assert_called_with('repos/org/app/issues/42/labels', method='POST', payload={'labels': ['type: epic']})

    def test_untyped_item_uses_repository_native_type_when_enabled(self):
        types = {'data': {'repository': {'issueTypes': {
            'nodes': [{'name': 'Bug', 'id': 'type-id', 'isEnabled': True}],
            'pageInfo': {'hasNextPage': False},
        }}}}
        api = Mock(side_effect=[{}, {}, types, {}])
        assign_types('repos/org/app', [{'number': 42, 'node_id': 'issue-id', 'labels': [], 'title': '[Bug] hi'}], api)
        self.assertEqual(api.call_args.kwargs['payload']['variables'], {'id': 'issue-id', 'type': 'type-id'})

    def test_closed_intake_milestone_reopens_and_scan_does_not_refetch(self):
        api = Mock(side_effect=[[{'title': 'Backlog triage', 'state': 'closed', 'number': 3}], {}, {}, {}])
        assign_milestones('repos/org/app', [{'number': 1}, {'number': 2}, {'number': 4, 'milestone': {'number': 9}}], api)
        self.assertEqual(api.call_count, 4)
        self.assertEqual(api.call_args_list[1].args, ('repos/org/app/milestones/3',))
        self.assertEqual(api.call_args_list[1].kwargs['payload'], {'state': 'open'})
        self.assertEqual(api.call_args.kwargs['payload'], {'milestone': 3})

    def test_milestone_422_requires_confirmed_concurrent_assignment(self):
        repo = 'repos/org/app'
        active = [{'title': 'Backlog triage', 'state': 'open', 'number': 3}]
        race = GitHubError(f'{repo}/issues/12', 422)
        api = Mock(side_effect=[active, race, {'milestone': {'number': 8}}])
        assign_milestones(repo, [{'number': 12}], api)
        api.assert_called_with(f'{repo}/issues/12')
        api = Mock(side_effect=[active, race, {'milestone': None}])
        with self.assertRaises(GitHubError):
            assign_milestones(repo, [{'number': 12}], api)

    def test_repair_scopes_to_open_unassigned_items(self):
        api = Mock(return_value=[])
        items_for_event('repos/org/app', 'milestones', 'schedule', {}, api)
        api.assert_called_once_with('repos/org/app/issues?state=open&per_page=100&milestone=none', paginate=True)
