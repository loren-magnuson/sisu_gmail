import logging
import sys
import unittest
import json
import vcr
from json import JSONDecodeError
from google.auth.credentials import Credentials
from googleapiclient.discovery import Resource
from src import sisu_gmail


TEST_CREDENTIALS_PATH = 'credentials.json'


TEST_TOKEN_PATH = 'token.json'


def load_json_file(path):
    with open(path) as infile:
        return json.loads(infile.read())


class TestSisuGmail(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestSisuGmail, self).__init__(*args, **kwargs)
        try:
            self.credentials = load_json_file(TEST_CREDENTIALS_PATH)
        except JSONDecodeError:
            logging.error('Add credentials json to credentials.json')
            sys.exit(0)

        try:
            self.token = load_json_file(TEST_TOKEN_PATH)
        except FileNotFoundError:
            sisu_gmail.start_auth_flow(
                TEST_CREDENTIALS_PATH,
                TEST_TOKEN_PATH
            )

    def test_start_auth_flow(self):
        try:
            load_json_file(TEST_TOKEN_PATH)
        except JSONDecodeError:
            self.fail('Could not load test credentials')
        else:
            result = sisu_gmail.start_auth_flow(
                TEST_CREDENTIALS_PATH,
                TEST_TOKEN_PATH
            )
            self.assertEqual(None, result)

    def test_creds_from_json(self):
        credentials = sisu_gmail.creds_from_json(self.token)
        self.assertIsInstance(credentials, Credentials)

    def test_authorize_resource(self):
        credentials = sisu_gmail.creds_from_json(self.token)
        resource = sisu_gmail.authorize_resource(credentials)
        self.assertIsInstance(resource, Resource)


if __name__ == '__main__':
    unittest.main()
