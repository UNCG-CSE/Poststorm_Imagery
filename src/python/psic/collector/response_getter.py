import requests
from requests import Response


def get_http_response(url: str) -> Response:
    """Attempts to connect to the website via an HTTP request

    :param url: The full url to connect to
    :returns: The response received from the url
    """

    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r
        else:
            raise ConnectionError('Connection refused! Returned code: ' + str(r.status_code))

    except Exception as e:
        raise ConnectionError('Error occurred while trying to connect to %s (%s)' % (url, e))


def get_full_content_length(url: str) -> int:

    try:
        # Ask the server for head
        head = requests.head(url, stream=True, allow_redirects=True)

        if head.headers.get('Content-Length') is None:  # pragma: no cover
            raise ConnectionError('Content-Length is 0! The website returned back response code ' + str(
                head.status_code) + ' for ' + url)

        # Ask the server how big its' package is
        full_length = int(head.headers.get('Content-Length'))

        # Stop talking to the server about this
        head.close()

        return full_length

    except (OSError, ConnectionError):  # pragma: no cover
        return 0
