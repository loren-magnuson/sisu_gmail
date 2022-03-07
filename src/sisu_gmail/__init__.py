import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES = "https://mail.google.com/"


def start_auth_flow(path, token_path):
    """Start the google auth flow using credentials at path

    :param path: path to a credentials.json file
    :param token_path: path to store resulting auth credentials
    :return: path to the credentials if created else None
    """
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

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
    """Create google.oauth2.credentials from token_json

    :param token_json: dict: Gmail API token json loaded as dict
    :return: google.oauth2.credentials.Credentials
    """
    return Credentials.from_authorized_user_info(token_json)
