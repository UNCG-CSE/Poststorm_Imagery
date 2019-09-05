import re
from typing import List

import requests
from requests import Response

from src.tagger.Storm import Storm

URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'
URL_STORMS_REGEX_PATTERN = \
    "<a href=\"(.+/storms/([^/]+)/index\\.html)\">([^\\(]+)\\(([^\\)]+)\\)</a>"


class ConnectionHandler:
    """An object that facilitates the connection between the user's computer and
    the NOAA website, reachable by HTTP(S)
    """

    # Declare variable to hold the HTTP request information
    r: Response

    storm_list: List[Storm] = list()

    def __init__(self, **kwargs):
        """Connect to the website and analyze the content

        Args:
            **kwargs: Arguments passed to the storm list generation function
        """
        self.connect()
        self.generate_storm_list(**kwargs)

    def connect(self):
        """Attempts to connect to the website via an HTTP request"""
        storm_list = list()

        try:
            self.r = requests.get(URL_BASE)
            if self.r.status_code != requests.codes.ok:
                print('Connection refused! Returned code: ' + self.r.status_code)
                exit()

            print('Connection to website successful!\n')

        except Exception as e:
            print('Error occurred while trying to connect to ' + URL_BASE)
            print('Error: ' + str(e))

    def generate_storm_list(self, search_re: str = '.*'):
        """Generates a list of tracked storms from the HTTP request

        Args:
            search_re (str): A regular expression to search all general storm
                data for. Search applies to storm name and year.
        """
        self.storm_list = list()

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for storm_id, storm_name, storm_year in re.findall(URL_STORMS_REGEX_PATTERN, self.r.text):

            # Search for the given pattern
            if re.search(search_re, storm_id) or re.search(search_re, storm_name) or re.search(search_re, storm_year):
                self.storm_list.append(Storm(storm_id, storm_name, storm_year))
