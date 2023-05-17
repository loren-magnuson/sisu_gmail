import inspect
import unittest
from src.sisu_gmail import search
from src.sisu_gmail.search import NoNextPageToken
from tests import helpers


TEST_EMAIL_COUNT = 105


class TestSearch(helpers.GmailTestCase):

    def setUp(self):
        pass
        # self.test_emails += helpers.send_test_emails(
        #     self.resource,
        #     self.user_id,
        #     self.test_email_address,
        #     f'TestSearch {inspect.stack()[0][3]}',
        #     f'TestSearch {inspect.stack()[0][3]}',
        #     count=TEST_EMAIL_COUNT
        # )

    def test_search(self):
        response = search.search(self.resource, self.user_id, self.query)
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), TEST_EMAIL_COUNT)

        response = search.search(
            self.resource,
            self.user_id,
            self.query,
            max_results=1
        )
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 1)

    def test_next_page(self):
        # We should get 100 results here
        response = search.search(
            self.resource,
            self.user_id,
            self.query,
            max_results=100
        )
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), TEST_EMAIL_COUNT - 5)
        total = len(response['messages'])

        # We should get 104 results on the next page
        response = search.next_page(
            self.resource,
            self.user_id,
            self.query,
            response['nextPageToken'],
            max_results=100
        )
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 5)
        total += len(response['messages'])
        self.assertEqual(total, TEST_EMAIL_COUNT)

    def test_iter_messages(self):
        messages = [
            msg for msg in search.iter_messages(
                self.resource,
                self.user_id,
                self.query
            )
        ]
        self.assertEqual(len(messages), TEST_EMAIL_COUNT)

    def test_search_by_address(self):
        messages = search.search_by_address(
            self.resource,
            self.user_id,
            self.test_email_address
        )
        self.assertEqual(len(messages), 2)


if __name__ == '__main__':
    unittest.main()
