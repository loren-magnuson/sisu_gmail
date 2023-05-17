QUERIES = {
    'FROM_ADDRESS': 'from:'
}


class NoNextPageToken(KeyError):
    pass


def next_page(resource, user_id, query, next_page_token, max_results=100):
    """Get next page of search results

    :param resource: Gmail API resource
    :param user_id: str, Gmail API userId
    :param query: str, Gmail API search query
    :param next_page_token: str, token for next page
    :param max_results: int, number of results per request
    :return: list, dicts of gmail message_id message_ids and thread message_ids
    """
    return resource.users().messages().list(
        userId=user_id,
        q=query,
        pageToken=next_page_token,
        maxResults=max_results
    ).execute()


def search(resource, user_id, query, max_results=100):
    """Return search results response for a Gmail API query

    :param resource: Gmail API resource
    :param user_id: str, Gmail API userId
    :param query: str, Gmail API search query
    :param max_results: int, number of results per request
    :return: Gmail API search response
    """
    return resource.users().messages().list(
        userId=user_id,
        q=query,
        maxResults=max_results
    ).execute()


def iter_messages(resource, user_id, query):
    """Generator to return search results

    :param resource: Gmail API resource
    :param user_id: str, Gmail API userId
    :param query: str, Gmail API search query
    :return: dict, gmail message_id message_ids and thread message_ids
    """

    do_next = True
    response = resource.users().messages().list(
        userId=user_id,
        q=query
    ).execute()
    while do_next:
        if 'messages' in response:
            print(len(response['messages']))
            for result in response['messages']:
                yield result
            if 'nextPageToken' in response:
                response = next_page(resource, user_id, query, response['nextPageToken'])
            else:
                do_next = False
        else:
            break


def search_by_address(resource, user_id, address):
    """Search gmail for messages by sender email address

    :param resource: Gmail API Resource
    :param user_id: str, Gmail API userId
    :param address: str, Gmail address
    :return: list, dict of Gmail message ids and thread ids:
    """
    return search(
        resource,
        user_id,
        f"{QUERIES['FROM_ADDRESS']}{address}"
    )
