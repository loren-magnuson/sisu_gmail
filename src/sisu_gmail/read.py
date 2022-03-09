def download_message(resource, message_id):
    """Download a message by id

    :param resource: Gmail API Resource
    :param message_id: str, Gmail message id
    :return: dict of message contents
    """
    return resource.users().messages().get(
        userId='me',
        id=message_id
    ).execute()
