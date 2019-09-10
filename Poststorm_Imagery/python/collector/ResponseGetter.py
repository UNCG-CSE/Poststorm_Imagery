import requests
from requests import Response


def get_http_response(url: str) -> Response:
    """Attempts to connect to the website via an HTTP request

    :param url: The full url to connect to
    :returns: The response received from the url
    """

    # Declare variable to hold the HTTP request information
    r: Response = None

    try:
        r = requests.get(url)
        if r.status_code == requests.codes.ok:
            return r
        else:
            print('Connection refused! Returned code: ' + r.status_code)
            exit()

    except Exception as e:
        print('Error occurred while trying to connect to ' + url)
        print('Error: ' + str(e))
