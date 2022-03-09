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

    def test_label_message(self):
        emails = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            'sisu_gmail test_label_message',
            'sisu_gmail test_label_message',
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
            response = labeller.label_message(
                self.resource,
                message_id,
                label_id
            )

        response = labeller.label_message(
            self.resource,
            message_id,
            [label_id]
        )
        self.assertIn('id', response)
        self.assertIn('labelIds', response)
        self.assertEqual(response['id'], message_id)
        self.assertIn(label_id, response['labelIds'], )


if __name__ == '__main__':
    unittest.main()
