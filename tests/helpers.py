import logging
import sys
import unittest
import json
from json import JSONDecodeError
from src import sisu_gmail
from tests import settings


def load_json_file(path):
    with open(path) as infile:
        return json.loads(infile.read())


def get_app_creds_and_user_token():
    try:
        app_creds = load_json_file(settings.TEST_APP_CREDS)
    except JSONDecodeError:
        logging.error('Add app_creds json to app_creds.json')
        sys.exit(0)
    else:
        try:
            token = load_json_file(settings.TEST_USER_TOKEN)
        except FileNotFoundError:
            sisu_gmail.start_auth_flow(
                settings.TEST_APP_CREDS,
                settings.TEST_USER_TOKEN
            )
        else:
            return app_creds, token


class GmailTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(GmailTestCase, self).__init__(*args, **kwargs)
        self.app_creds, self.user_token = get_app_creds_and_user_token()
