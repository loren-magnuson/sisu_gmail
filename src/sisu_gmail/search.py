def next_search_page(resource, response, query):
    """

    :param resource: Gmail API resource
    :param response: response from a gmail api search query
    :param query: str, Gmail API search query
    :return: list, dicts of gmail message ids and thread ids
    """
    page_token = response['nextPageToken']
    return resource.users().messages().list(
        userId='me',
        q=query,
        pageToken=page_token
    ).execute()


def search(resource, query):
    """Return search results response for a Gmail API query

    :param resource: Gmail API resource
    :param query: str, Gmail API search query
    :return: Gmail API search response
    """
    return resource.users().messages().list(
        userId='me',
        q=query
    ).execute()


def iter_messages(resource, query):
    """Generator to return search results

    :param resource: Gmail API resource
    :param query: str, Gmail API search query
    :return: dict, gmail message ids and thread ids
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
            next_search_page(resource, response, query)
