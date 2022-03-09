import inspect
import unittest
from src.sisu_gmail import label as labeller
from tests import helpers


class TestLabel(helpers.GmailTestCase):

    def test_get_labels(self):
        response = labeller.get_labels(self.resource, self.user_id)
        self.assertIn('labels', response)

        labels = response['labels']
        self.assertGreater(len(labels), 0)

        filtered = [
            label for label in labels
            if label['id'] == 'STARRED'
        ]
        self.assertEqual(len(filtered), 1)
        starred = filtered[0]
        self.assertIn('type', starred)
        self.assertEqual(starred['type'], 'system')

    def test_add_label(self):
        emails = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            inspect.stack()[0][3],
            inspect.stack()[0][3],
            count=1
        )
        self.test_emails += emails

        message_id = emails[0]['id']

        labels = labeller.get_labels(self.resource, self.user_id)['labels']
        label_id = [
            label for label in labels
            if label['id'] == 'STARRED'
        ][0]['id']

        # lists only for labels arg
        with self.assertRaises(ValueError):
            labeller.add_labels(
                self.resource,
                self.user_id,
                message_id,
                label_id
            )

        response = labeller.add_labels(
            self.resource,
            self.user_id,
            message_id,
            [label_id]
        )
        self.assertIn('id', response)
        self.assertIn('labelIds', response)
        self.assertEqual(response['id'], message_id)
        self.assertIn(label_id, response['labelIds'])

    def test_get_label_by_name(self):
        search_for_label_name = 'STARRED'
        label = labeller.get_label_by_name(
            self.resource,
            self.user_id,
            search_for_label_name
        )
        self.assertIn('id', label)
        self.assertEqual(label['id'], 'STARRED')

        # Should be case insensitive
        search_for_label_name_lowercase = 'starred'
        label = labeller.get_label_by_name(
            self.resource,
            self.user_id,
            search_for_label_name_lowercase
        )
        self.assertIn('id', label)
        self.assertEqual(label['id'], 'STARRED')

        # Should return None if None label is not found
        search_for_nonexistent_label_name = 'impossibletofindlabel'
        label = labeller.get_label_by_name(
            self.resource,
            self.user_id,
            search_for_nonexistent_label_name
        )
        self.assertEqual(None, label)

    def test_remove_labels(self):
        emails = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            inspect.stack()[0][3],
            inspect.stack()[0][3],
            count=1
        )
        self.test_emails += emails

        message_id = emails[0]['id']

        label_to_add = 'STARRED'
        label = labeller.get_label_by_name(
            self.resource,
            self.user_id,
            label_to_add
        )
        self.assertIn('id', label)
        self.assertEqual(label['id'], 'STARRED')

        # We need to add and confirm the label wa added
        label_to_remove_id = label['id']
        response = labeller.add_labels(
            self.resource,
            self.user_id,
            message_id,
            [label_to_remove_id]
        )
        self.assertIn('id', response)
        self.assertIn('labelIds', response)
        self.assertEqual(response['id'], message_id)
        self.assertIn(label_to_remove_id, response['labelIds'])

        # lists only for labels arg
        with self.assertRaises(ValueError):
            labeller.add_labels(
                self.resource,
                self.user_id,
                message_id,
                label_to_remove_id
            )

        response = labeller.remove_labels(
            self.resource,
            self.user_id,
            message_id,
            [label_to_remove_id]
        )
        self.assertIn('id', response)
        self.assertIn('labelIds', response)
        self.assertEqual(response['id'], message_id)
        self.assertNotIn(label_to_remove_id, response['labelIds'])


if __name__ == '__main__':
    unittest.main()
