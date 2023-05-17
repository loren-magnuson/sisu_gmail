import logging
import sys
import unittest
import json
import sisu_email.create
import src.sisu_gmail.auth
from time import sleep
from json import JSONDecodeError
from src import sisu_gmail
from src.sisu_gmail import send, create, delete
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
    token = None
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
        finally:
            if token is None:
                token = load_json_file(settings.TEST_USER_TOKEN)
            return app_creds, token


def load_test_resource(user_token):
    """Try to load an authenticated resource for testing

    :param user_token:
    :return: Gmail API resource
    """
    credentials = sisu_gmail.auth.creds_from_json(user_token)
    return sisu_gmail.auth.authorize_resource(credentials)


def create_test_email(address, subject, text):
    """Create multipart message_id for testing

    :param address:
    :param subject:
    :param text:
    :return: id of created email
    """
    message = sisu_email.create.create_multipart_message(
        address,
        address,
        subject,
        text
    )
    return message


def send_test_emails(resource, user_id, sender, subject, text, count=1):
    """Send a batch of test emails

    :param resource: Gmail API resource
    :param user_id: Gmail API userId
    :param sender: sender Gmail address
    :param subject: subject line
    :param text: tex for body of email
    :param count: number to send
    :return: count of emails sent
    """
    messages = []
    for i in range(0, count):
        message = create_test_email(sender, subject, text)
        response = send.send_message(
            resource,
            user_id,
            create.encode_multipart_message(message)
        )
        if 'id' in response:
            messages.append(response)
        else:
            raise KeyError('Test email failed to send')
        sleep(1)
    else:
        sleep(3)
        return messages


class GmailTestCase(unittest.TestCase):
    """Setups up the resources to test facets of sisu_gmail"""
    def __init__(self, *args, **kwargs):
        super(GmailTestCase, self).__init__(*args, **kwargs)
        self.app_creds, self.user_token = get_app_creds_and_user_token()
        self.resource = load_test_resource(self.user_token)
        self.query = settings.TEST_SEARCH_QUERY
        self.user_id = 'me'
        self.test_email_address = self.set_test_email_address()
        self.test_emails = []

    def tearDown(self):
        pass
        # Just trying to prevent operating on "non-existent" emails
        # sleep(3)
        # if len(self.test_emails) > 0:
        #     delete.batch_delete(
        #         self.resource,
        #         self.user_id,
        #         message_ids=self.test_emails
        #     )

    def set_test_email_address(self):
        self.test_email_address = sisu_gmail.user.get_profile(
            self.resource,
            self.user_id
        )['emailAddress']
        return self.test_email_address
