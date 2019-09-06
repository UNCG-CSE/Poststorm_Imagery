import re
from typing import List

import requests
from requests import Response

from src.scraper.Tar import Tar

URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'

# Matches reference link to each storm (HTML)
URL_STORMS_REGEX_PATTERN_INDEX = "<a href=\"(.+/storms/([^/]+)/index\\.html)\">([^\\(]+)\\(([^\\)]+)\\)</a>"
# Groups: <storm_url>, <storm_id>, <storm_title>, <storm_year>


def get_http_response(url: str) -> Response:
    """Attempts to connect to the website via an HTTP request

    Args:
        url (str): The full url to connect to
    """

    # Declare variable to hold the HTTP request information
    r: Response

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


class ConnectionHandler:
    """An object that facilitates the connection between the user's computer and
    the NOAA website, reachable by HTTP(S)
    """

    from src.scraper.Storm import Storm

    # Declare variable to hold the HTTP request information
    r: Response

    storm_list: List[Storm] = list()
    storm_list_last_pattern: str = None

    tar_list: List[Tar] = list()

    def __init__(self):
        """Connect to the website and analyze the content"""
        self.r = get_http_response(URL_BASE)
        self.generate_storm_list()

    def generate_storm_list(self, search_re: str = '.*'):
        """Generates a list of tracked storms from the HTTP request

        Args:
            search_re (str): A regular expression to search all general storm
                data for. Search applies to storm name and year.
        """

        # Clear all existing storms
        self.storm_list = list()

        # Remember the search query
        self.storm_list_last_pattern = search_re

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for storm_url, storm_id, storm_name, storm_year in re.findall(URL_STORMS_REGEX_PATTERN_INDEX, self.r.text):

            # Search for the given pattern
            if re.search(search_re, storm_id) or re.search(search_re, storm_name) or re.search(search_re, storm_year):
                from src.scraper.Storm import Storm
                self.storm_list.append(Storm(storm_url, storm_id, storm_name, storm_year))

    def get_storm_list(self, search_re: str = '.*') -> List[Storm]:

        # If the user has already asked for a list with the same search expression (answer is not already known)
        """Retrieve a list of all storms that match a particular regular expression

        Args:
            search_re (str): A regular expression to search all general storm
                data for. Search applies to storm name and year.
        """
        if search_re != self.storm_list_last_pattern:

            # Generate the list of storms (clear old list if one exists)
            self.generate_storm_list(search_re)

        return self.storm_list

