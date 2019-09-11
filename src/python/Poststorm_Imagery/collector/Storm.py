import re
from typing import List

from requests import Response

# Matches .tar files for a given storm (Florence and newer)
from src.python.Poststorm_Imagery.collector.ConnectionHandler import get_http_response
from src.python.Poststorm_Imagery.collector.TarRef import TarRef

# Matches .tar files for most (if not all) formats
URL_STORMS_REGEX_PATTERN_TAR_GENERAL = "\"\\s*(http[^\"]+\\.tar)\\s*\""
# Groups: <tar_url>


class Storm:
    """An object that stores information about a particular storm"""

    storm_url: str  # The full url to the storm's index.html page
    storm_id: str  # The name given to the storm, located in the url to identify it in the list
    storm_title: str  # The full name of the storm as listed on the NOAA page
    storm_year: int  # The year that the storm occurred

    r: Response  # Holds the HTTP request information

    tar_list: List[TarRef] = list()  # A list of all tars associated with the storm (from the index.html)
    tar_list_last_pattern: str = None  # The last regular expression used to create the list of tar files

    def __init__(self, storm_url: str, storm_id: str, storm_title: str, storm_year: str or int):
        """Initializes the object with required information for a storm

        :param storm_url: The url to the index.html of the storm
        :param storm_id: The ID (from URL) of the storm
        :param storm_title: The name (link name) of the storm
        :param storm_year: The year the storm occurred
        """
        self.storm_url = storm_url
        self.storm_id = storm_id
        self.storm_title = storm_title
        self.storm_year = int(storm_year)

    def __str__(self):
        """Prints out the storm title and year in a human readable format"""
        return self.storm_title + '(' + str(self.storm_year) + ')'

    def generate_tar_list(self, search_re: str = '.*'):
        """Generates a list of archive (.tar) files from the given storm

        :param search_re: A regular expression to search all .tar files for
        """

        # Load the storm's index.html
        self.r = get_http_response(self.storm_url)

        # Clear all existing tar files
        self.tar_list = list()

        # Remember the search query
        self.tar_list_last_pattern = search_re

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for tar_url in re.findall(URL_STORMS_REGEX_PATTERN_TAR_GENERAL, self.r.text):
            if re.search(search_re, tar_url):

                exists = False

                for tar in self.tar_list:
                    if tar.tar_url == tar_url:
                        exists = True
                        break

                if exists is False:
                    self.tar_list.append(TarRef(tar_url=tar_url))

    """ DISABLED: Does not cover JPEG files reliably

        # Find all storm data by regex parsing of URLs
        for tar_date, tar_url, tar_label in re.findall(URL_STORMS_REGEX_PATTERN_TAR_1, self.r.text):

            # Search for the given pattern
            if re.search(search_re, tar_date) or re.search(search_re, tar_url) or re.search(search_re, tar_label):
                self.tar_list.append(TarRef(tar_url, tar_date, tar_label))
                
        for tar_url, tar_date, tar_label in re.findall(URL_STORMS_REGEX_PATTERN_TAR_2, self.r.text):
    
            # Search for the given pattern
            if re.search(search_re, tar_date) or re.search(search_re, tar_url) or re.search(search_re, tar_label):
                self.tar_list.append(TarRef(tar_url, tar_date, tar_label))
    
        if len(self.tar_list) == 0:
            for tar_url in re.findall(URL_STORMS_REGEX_PATTERN_TAR_FINAL, self.r.text):
                self.tar_list.append(TarRef(tar_url=tar_url))
    """

    def get_tar_list(self, search_re: str = '.*') -> List[TarRef]:
        """Get a list of all .tar objects with the associated regular expression

        :param search_re: The regular expression to search for. Applies to tar date, url, and label
        :returns: A list of tar references (information about tars from the website)
        """

        # If the user has already asked for a list with the same search expression (answer is not already known)
        if search_re != self.tar_list_last_pattern:
            # Generate the list of tar files (clear old list if one exists)
            self.generate_tar_list(search_re)

        return self.tar_list
