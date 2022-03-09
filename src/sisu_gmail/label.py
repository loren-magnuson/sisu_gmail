def get_labels(resource, user_id):
    """Get a list of message labels for user_id
    
    :param resource: Gmail API Resource
    :param user_id: sender Gmail API userId
    :return: Gmail API response
    """
    response = resource.users().labels().list(
        userId=user_id
    ).execute()
    return response


def label_message(resource, message_id, labels):
    """Apply a list of labels to a Gmail message

    :param resource: Gmail API resource
    :param message_id: str, Gmail message id
    :param labels: list, str, labels to apply to message
    :return: Gmail API response
    """
    if not type(labels) is list:
        raise ValueError(
            'label_message requires a list of label ids for labels arg'
        )
    response = resource.users().messages().modify(
        userId='me',
        id=message_id,
        body={'addLabelIds': labels}
    ).execute()
    return response
