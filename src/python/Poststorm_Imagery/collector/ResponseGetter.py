import requests
from requests import Response

from src.python.Poststorm_Imagery.collector import h


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
            print('Connection refused! Returned code: ' + str(r.status_code))
            exit()

    except Exception as e:
        h.print_error('Error occurred while trying to connect to ' + url)
        h.print_error('Error: ' + str(e))
        exit()


def get_full_content_length(url: str) -> int:

    # Ask the server for head
    head = requests.head(url, stream=True)

    # Ask the server how big its' package is
    full_length = int(head.headers.get('Content-Length'))

    # Stop talking to the server about this
    head.close()

    return full_length
