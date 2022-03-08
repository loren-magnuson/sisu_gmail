import logging
import sys
import unittest
import json
import sisu_email.create
import src.sisu_gmail.auth
from json import JSONDecodeError
from src import sisu_gmail
from tests import settings


def load_json_file(path):
    with open(path) as infile:
        return json.loads(infile.read())


def get_app_creds_and_user_token():
    """Tries to load saved test app creds and user token
    If there are no app creds this cannot continue
    If there is no user token we try to get one using the app creds

    :return: tuple, dict of app creds, dict of user token
    """
    try:
        app_creds = load_json_file(settings.TEST_APP_CREDS)
    except JSONDecodeError:
        logging.error('Add app_creds json to app_creds.json')
        sys.exit(0)
    else:
        try:
            token = load_json_file(settings.TEST_USER_TOKEN)
        except FileNotFoundError:
            src.sisu_gmail.auth.start_auth_flow(
                settings.TEST_APP_CREDS,
                settings.TEST_USER_TOKEN,
                settings.TEST_AUTH_SCOPES
            )
        else:
            return app_creds, token


def load_test_resource(user_token):
    """Try to load an authenticated resource for testing

    :param user_token:
    :return: Gmail API resource
    """
    credentials = sisu_gmail.auth.creds_from_json(user_token)
    return sisu_gmail.auth.authorize_resource(credentials)


def insert_test_email(resource):
    """Insert email with text and image, excel, pdf attachments

    :param resource: Gmail API Resource
    :return: id of created email
    """
    pass
    # sisu_email.create.create_multipart_message()


class GmailTestCase(unittest.TestCase):
    """Setups up the resources to test facets of sisu_gmail"""
    def __init__(self, *args, **kwargs):
        super(GmailTestCase, self).__init__(*args, **kwargs)
        self.app_creds, self.user_token = get_app_creds_and_user_token()
        self.resource = load_test_resource(self.user_token)
        self.query = settings.TEST_SEARCH_QUERY
