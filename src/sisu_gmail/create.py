import sisu_email.create


def encode_multipart_message(message):
    """Encode multipart message as urlsafe base64 string

    :return: dict, {'raw': base64_string_of_message}
    """
    return {
        'raw': sisu_email.create.encode_multipart_message(message)
    }

