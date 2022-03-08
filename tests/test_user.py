import unittest
from src.sisu_gmail import user
from tests import helpers


class TestUser(helpers.GmailTestCase):

    def test_get_profile(self):
        response = user.get_profile(
            self.resource,
            'me'
        )
        self.assertIn('emailAddress', response)
        self.assertIn('historyId', response)
        self.assertIn('messagesTotal', response)
        self.assertIn('threadsTotal', response)


if __name__ == '__main__':
    unittest.main()
