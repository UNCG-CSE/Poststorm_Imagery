import re
from typing import List

from psicollect.collector.response_getter import get_http_response
from psicollect.collector.storm import Storm
from psicollect.common import s


class ConnectionHandler:
    """An object that facilitates the connection between the user's computer and
    the NOAA website, reachable by HTTP(S)
    """

    html_text: str  # Declare variable to hold the HTML file text

    storm_list: List[Storm] = list()
    storm_list_last_pattern: str = None

    def __init__(self, html_text: str = get_http_response(s.URL_BASE).text):
        """Connect to the website and analyze the content"""
        self.html_text = html_text
        self.generate_storm_list()

    def generate_storm_list(self, search_re: str = '.*') -> List[Storm]:
        """Generates a list of tracked storms from the HTTP request

        :param search_re: A regular expression to search all general storm data for. Search applies to storm name and year.
        """

        # Clear all existing storms
        self.storm_list = list()

        # Remember the search query
        self.storm_list_last_pattern = search_re

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for storm_url, storm_id, storm_name, storm_year in re.findall(s.URL_STORMS_REGEX_PATTERN_INDEX, self.html_text):

            # Search for the given pattern
            if re.search(search_re, storm_id) or re.search(search_re, storm_name) or re.search(search_re, storm_year):
                self.storm_list.append(Storm(storm_url, storm_id, storm_name, storm_year))

        return self.storm_list

    def get_storm_list(self, search_re: str = '.*') -> List[Storm]:
        """Retrieve a list of all storms that match a particular regular expression

        :param search_re: A regular expression to search all general storm data for. Search applies to storm name and year.
        :returns: A list of storms as Storm objects
        """

        # If the user has already asked for a list with the same search expression (answer is not already known)
        if search_re != self.storm_list_last_pattern:
            # Generate the list of storms (clear old list if one exists)
            self.generate_storm_list(search_re)

        return self.storm_list
