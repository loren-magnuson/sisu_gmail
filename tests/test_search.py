import unittest
from src.sisu_gmail import search
from src.sisu_gmail.search import NoNextPageToken
from tests import helpers


class TestSearch(helpers.GmailTestCase):

    def setUp(self):
        self.test_emails += helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            'sisu_gmail TestSearch',
            'sisu_gmail TestSearch',
            count=2
        )

    def test_search(self):
        response = search.search(self.resource, self.query)
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 2)

        response = search.search(self.resource, self.query, max_results=1)
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 1)

    def test_next_page(self):
        # raise type error on non-dict
        response = 'this-is-not-a-dict'
        with self.assertRaises(TypeError):
            search.next_page(
                self.resource,
                self.query,
                response
            )

        # raise NoNextPageToken if we don't have a page token
        response = {'theres-no-next-page-token-in-here': ''}
        with self.assertRaises(NoNextPageToken):
            search.next_page(
                self.resource,
                self.query,
                response
            )

        # We should get 1 result here
        response = search.search(self.resource, self.query, max_results=1)
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 1)

        # We should get 1 more result on the next page
        response = search.next_page(
            self.resource,
            self.query,
            response,
            max_results=1
        )
        self.assertIn('messages', response)
        self.assertEqual(len(response['messages']), 1)

    def test_iter_messages(self):
        messages = [
            msg for msg in search.iter_messages(
                self.resource,
                self.query
            )
        ]
        self.assertEqual(len(messages), 2)


if __name__ == '__main__':
    unittest.main()
