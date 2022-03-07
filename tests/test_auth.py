import unittest
import src.sisu_gmail.auth
from json import JSONDecodeError
from google.auth.credentials import Credentials
from googleapiclient.discovery import Resource
from tests import helpers, settings


class TestAuth(helpers.GmailTestCase):

    def test_start_auth_flow(self):
        try:
            helpers.load_json_file(settings.TEST_USER_TOKEN)
        except JSONDecodeError:
            self.fail('Could not load test app credentials')
        else:
            path_to_token = src.sisu_gmail.auth.start_auth_flow(
                settings.TEST_APP_CREDS,
                settings.TEST_USER_TOKEN,
                scopes=settings.TEST_AUTH_SCOPES
            )
            self.assertEqual(None, path_to_token)

    def test_creds_from_json(self):
        credentials = src.sisu_gmail.auth.creds_from_json(self.user_token)
        self.assertIsInstance(credentials, Credentials)

    def test_authorize_resource(self):
        credentials = src.sisu_gmail.auth.creds_from_json(self.user_token)
        resource = src.sisu_gmail.auth.authorize_resource(credentials)
        self.assertIsInstance(resource, Resource)

    def test_refresh_token(self):
        credentials = src.sisu_gmail.auth.creds_from_json(self.user_token)
        old_expirty = credentials.__dict__['expiry']
        new_expiry = src.sisu_gmail.auth.refresh_token(credentials).__dict__['expiry']
        self.assertNotEqual(old_expirty, new_expiry)


if __name__ == '__main__':
    unittest.main()
