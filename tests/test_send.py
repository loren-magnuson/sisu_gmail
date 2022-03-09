import inspect
import unittest
from tests import helpers


class TestSend(helpers.GmailTestCase):

    def test_send_message(self):
        emails = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            inspect.stack()[0][3],
            inspect.stack()[0][3]
        )
        self.test_emails += emails
        response = emails[0]
        self.assertIn('id', response)
        self.assertIn('threadId', response)
        self.assertIn('labelIds', response)

        labels = response['labelIds']
        self.assertIn('UNREAD', labels)
        self.assertIn('SENT', labels)
        self.assertIn('INBOX', labels)


if __name__ == '__main__':
    unittest.main()
