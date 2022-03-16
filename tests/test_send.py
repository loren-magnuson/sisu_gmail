import inspect
import unittest
import sisu_email.create
from src.sisu_gmail import send, create
from tests import helpers


class TestSend(helpers.GmailTestCase):

    def test_send_message(self):
        message = sisu_email.create.create_multipart_message(
            self.test_email_address,
            self.test_email_address,
            inspect.stack()[0][3],
            inspect.stack()[0][3],
        )
        email = send.send_message(
            self.resource,
            self.user_id,
            create.encode_multipart_message(message)
        )
        self.assertIn('id', email)
        self.test_emails += [email]

    def test_send_message_with_xls_attachment(self):
        message = sisu_email.create.create_multipart_message(
            self.test_email_address,
            self.test_email_address,
            inspect.stack()[0][3],
            inspect.stack()[0][3],
        )

        with open('./fixtures/test_xls.xls', 'rb') as infile:
            sisu_email.create.attach_file(infile, message)

        message = create.encode_multipart_message(message)

        response = send.send_message(
            self.resource,
            self.user_id,
            message
        )

        self.assertIn('id', response)
        self.test_emails += [response]


if __name__ == '__main__':
    unittest.main()
