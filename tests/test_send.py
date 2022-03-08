import unittest
from src.sisu_gmail import send
from tests import helpers


class TestSend(helpers.GmailTestCase):

    def test_send_message(self):
        message = helpers.send_test_email(
            self.resource,
            self.user_id,
            self.test_email_address,
            self.test_email_address,
            'sisu_gmail test_send_message'
        )
        response = send.send_message(
            self.resource,
            self.user_id,
            message
        )
        print(response)


if __name__ == '__main__':
    unittest.main()
