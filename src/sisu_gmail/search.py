class NoNextPageToken(KeyError):
    pass


def next_page(resource, query, response, max_results=100):
    """Get next page of search results

    :param resource: Gmail API resource
    :param query: str, Gmail API search query
    :param response: dict, Gmail API search query response
    :param max_results: int, number of results per request
    :return: list, dicts of gmail message message_ids and thread message_ids
    """
    if not type(response) is dict:
        raise TypeError(
            'next_search_page requires dict as response param'
        )
    elif 'nextPageToken' not in response:
        raise NoNextPageToken(
            'next_search_page requires dict with nextPageToken key'
        )

    page_token = response['nextPageToken']
    return resource.users().messages().list(
        userId='me',
        q=query,
        pageToken=page_token,
        maxResults=max_results
    ).execute()


def search(resource, query, max_results=100):
    """Return search results response for a Gmail API query

    :param resource: Gmail API resource
    :param query: str, Gmail API search query
    :param max_results: int, number of results per request
    :return: Gmail API search response
    """
    return resource.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()


def iter_messages(resource, query):
    """Generator to return search results

    :param resource: Gmail API resource
    :param query: str, Gmail API search query
    :return: dict, gmail message message_ids and thread message_ids
    """
    response = resource.users().messages().list(
        userId='me',
        q=query
    ).execute()

    if 'messages' not in response:
        raise StopIteration

    part = response['messages']
    for index, result in enumerate(part, start=1):
        yield result
        if len(part) == index and 'nextPageToken' in response:
            next_page(resource, response, query)
