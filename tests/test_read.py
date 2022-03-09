import unittest
from time import sleep
from src.sisu_gmail import read, send, create, delete
from tests import helpers


class TestRead(helpers.GmailTestCase):

    def test_download_message(self):
        emails = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            'sisu_gmail test_label_message',
            'sisu_gmail test_label_message',
            count=1
        )
        self.test_emails += emails
        sent = emails[0]
        self.assertIn('id', sent)
        retrieved = read.download_message(self.resource, sent['id'])
        self.assertIn('id', retrieved)
        self.assertEqual(retrieved['id'], sent['id'])


if __name__ == '__main__':
    unittest.main()
