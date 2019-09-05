import re
import tarfile
from typing import List

from requests import Response
from src.tagger.ConnectionHandler import get_http_response
from src.tagger.Tar import Tar

# Matches .tar files for a given storm
URL_STORMS_REGEX_PATTERN_TAR = "&nbsp;([^<;]+)</a><a href=\"(.+)\"\\(([^\\)]+)\\)</a>"
# Groups: <tar_date>, <tar_url>, <tar_label>


class Storm:
    """An object that stores information about a particular storm"""

    storm_url: str
    storm_id: str
    storm_title: str
    storm_year: int

    # Declare variable to hold the HTTP request information
    r: Response

    tar_list: List[Tar] = None

    def __init__(self, storm_url: str, storm_id: str, storm_title: str, storm_year: str or int):
        """Initializes the object with required information for a storm

        Args:
            storm_url (str): The url to the index.html of the storm
            storm_id (str): The ID (from URL) of the storm
            storm_title (str): The name (link name) of the storm
            storm_year (str or int): The year the storm occurred
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

        Args:
            search_re (str): A regular expression to search all .tar files for.
        """

        # Load the storm's index.html
        self.r = get_http_response(self.storm_url)

        self.tar_list = list()

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for tar_date, tar_url, tar_label in re.findall(URL_STORMS_REGEX_PATTERN_TAR, self.r.text):

            # Search for the given pattern
            if re.search(search_re, tar_date) or re.search(search_re, tar_url) or re.search(search_re, tar_label):
                self.tar_list.append(Tar(tar_date, tar_url, tar_label))
