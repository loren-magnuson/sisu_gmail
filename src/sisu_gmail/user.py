def get_profile(resource, user_id):
    """Fetch profile data for a given Gmail userId

    :param resource: Gmail API resource
    :param user_id: str, Gmail API userId
    :return: Gmail API response
    """
    return resource.users().getProfile(
        userId=user_id,
    ).execute()
