import unittest
from time import sleep
from src.sisu_gmail import send, create, delete
from tests import helpers


class TestSend(helpers.GmailTestCase):

    def test_send_message(self):
        message = helpers.create_test_email(
            self.test_email_address,
            'sisu_gmail test_send_message',
            'sisu_gmail test_send_message'
        )
        response = send.send_message(
            self.resource,
            self.user_id,
            create.encode_multipart_message(message)
        )
        self.assertIn('id', response)
        self.assertIn('threadId', response)
        self.assertIn('labelIds', response)

        labels = response['labelIds']
        self.assertIn('UNREAD', labels)
        self.assertIn('SENT', labels)
        self.assertIn('INBOX', labels)

        # Just trying to prevent operating on "non-existent" emails
        sleep(5)
        delete.delete_message(self.resource, self.user_id, response['id'])


if __name__ == '__main__':
    unittest.main()
