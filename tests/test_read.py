import unittest
from time import sleep
from src.sisu_gmail import read, send, create, delete
from tests import helpers


class TestRead(helpers.GmailTestCase):

    def test_download_message(self):
        message = helpers.create_test_email(
            self.test_email_address,
            'sisu_gmail test_download_message',
            'sisu_gmail test_download_message'
        )
        sent = send.send_message(
            self.resource,
            self.user_id,
            create.encode_multipart_message(message)
        )

        self.assertIn('id', sent)
        retrieved = read.download_message(self.resource, sent['id'])
        self.assertIn('id', retrieved)
        self.assertEqual(retrieved['id'], sent['id'])

        # Just trying to prevent operating on "non-existent" emails
        sleep(3)
        delete.delete_message(self.resource, self.user_id, retrieved['id'])


if __name__ == '__main__':
    unittest.main()
