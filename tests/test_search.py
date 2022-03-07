import unittest
from src.sisu_gmail import search
from tests import helpers


class TestAuth(helpers.GmailTestCase):

    def test_search(self):
        response = search.search(
            self.resource,
            self.query
        )
        self.assertIn(response, 'messages')

    def test_iter_messages(self):
        messages = [
            msg for msg in search.iter_messages(
                self.resource,
                self.query
            )
        ]
        self.assertEqual(len(messages), 3)

    def test_next_search_page(self):
        response = search.search(
            self.resource,
            self.query
        )
        messages = search.next_search_page(
            self.resource,
            self.query,
            response
        )
        self.assertEqual(len(messages), 3)


if __name__ == '__main__':
    unittest.main()
