import base64
import unittest
import sisu_email.create
from src.sisu_gmail import create
from tests import helpers


class TestCreate(helpers.GmailTestCase):

    def test_encode_multipart_message(self):
        """Encode multipart message as urlsafe base64 string

        :return: dict, {'raw': base64_string_of_message}
        """
        message = sisu_email.create.create_multipart_message(
            self.test_email_address,
            self.test_email_address,
            'sisu_gmail test_encode_multipart_message',
            'sisu_gmail test_encode_multipart_message'
        )
        text_repr = str(message)
        encoded = create.encode_multipart_message(message)
        self.assertIn('raw', encoded)
        self.assertIs(str, type(encoded['raw']))
        self.assertEqual(
            text_repr,
            base64.urlsafe_b64decode(encoded['raw']).decode()
        )


if __name__ == '__main__':
    unittest.main()
