import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = 'https://mail.google.com/'


def start_auth_flow(path, token_path, scopes=SCOPES):
    """Start the google auth flow using app_creds at path

    :param path: path to a app_creds.json file
    :param token_path: path to store resulting auth app_creds
    :param scopes: Gmail API permission scope to request
    :return: path to the app_creds if created else None
    """
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())
            return token_path


def authorize_resource(credentials):
    """Create an authorized Gmail API resource

    :param credentials:
    :return: googleapiclient.discovery.Resource
    """
    return build('gmail', 'v1', credentials=credentials)


def creds_from_json(token_json):
    """Create google.oauth2.app_creds from token_json

    :param token_json: dict: Gmail API user_token json loaded as dict
    :return: google.oauth2.app_creds.Credentials
    """
    return Credentials.from_authorized_user_info(token_json)
