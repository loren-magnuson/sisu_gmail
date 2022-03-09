import unittest
from time import sleep
from src.sisu_gmail import delete, search
from tests import helpers


class TestDelete(helpers.GmailTestCase):

    def test_batch_delete(self):
        helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            'sisu_gmail test_batch_delete',
            'sisu_gmail test_batch_delete',
            count=2
        )

        response = search.search(self.resource, self.query)
        self.assertIn('messages', response)
        messages = response['messages']
        self.assertEqual(len(messages), 2)

        response = delete.batch_delete(
            self.resource,
            self.user_id,
            messages
        )

        # Let Gmail catch up to avoid concurrency issues
        sleep(3)

        # If successful, the response body is empty.
        # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/batchDelete
        self.assertEqual(response, '')

        response = search.search(self.resource, self.query)
        self.assertIn('resultSizeEstimate', response)
        self.assertEqual(response['resultSizeEstimate'], 0)

    def test_delete_message(self):
        message_id = helpers.send_test_emails(
            self.resource,
            self.user_id,
            self.test_email_address,
            'sisu_gmail test_delete_message',
            'sisu_gmail test_delete_message',
            count=1
        )[0]['id']
        response = delete.delete_message(
            self.resource,
            self.user_id,
            message_id
        )

        # Let Gmail catch up to avoid concurrency issues
        sleep(3)

        # If successful, the response body is empty.
        # https://developers.google.com/gmail/api/reference/rest/v1/users.messages/delete
        self.assertEqual(response, '')

        response = search.search(self.resource, self.query)
        self.assertIn('resultSizeEstimate', response)
        self.assertEqual(response['resultSizeEstimate'], 0)


if __name__ == '__main__':
    unittest.main()
