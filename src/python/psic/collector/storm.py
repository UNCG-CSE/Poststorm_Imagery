import re
from typing import List

from requests import Response

from psic.collector.archive import Archive
# Matches archive files for a given storm (Florence and newer)
from psic.collector.connection_handler import get_http_response

# Matches archive files for most (if not all) formats
URL_STORMS_REGEX_PATTERN_ARCHIVE_GENERAL = "[\"\']\\s*(https?[^\"]+\\.tar)\\s*[\"\']"
# Groups: <archive_url>


class Storm:
    """An object that stores information about a particular storm"""

    storm_url: str  # The full url to the storm's index.html page
    storm_id: str  # The name given to the storm, located in the url to identify it in the list
    storm_title: str  # The full name of the storm as listed on the NOAA page
    storm_year: int  # The year that the storm occurred

    r: Response  # Holds the HTTP request information

    archive_list: List[Archive] = list()  # A list of all tars associated with the storm (from the index.html)
    archive_list_last_pattern: str = None  # The last regular expression used to create the list of archive files

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

    def generate_archive_list(self, search_re: str = '.*'):
        """Generates a list of archive files from the given storm

        :param search_re: A regular expression to search all archive files for
        """

        # Load the storm's index.html
        self.r = get_http_response(self.storm_url)

        # Clear all existing archive files
        self.archive_list = list()

        # Remember the search query
        self.archive_list_last_pattern = search_re

        # Make search pattern case-insensitive
        search_re = re.compile(search_re, re.IGNORECASE)

        # Find all storm data by regex parsing of URLs
        for archive_url in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_GENERAL, self.r.text):
            if re.search(search_re, archive_url):

                exists = False

                for archive in self.archive_list:
                    if archive.archive_url == archive_url:
                        exists = True
                        break

                if exists is False:
                    self.archive_list.append(Archive(archive_url=archive_url))

    """ DISABLED: Does not cover JPEG files reliably

        # Find all storm data by regex parsing of URLs
        for archive_date, archive_url, archive_label in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_1, self.r.text):

            # Search for the given pattern
            if re.search(search_re, archive_date) or re.search(search_re, archive_url) or re.search(search_re, archive_label):
                self.archive_list.append(Archive(archive_url, archive_date, archive_label))

        for archive_url, archive_date, archive_label in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_2, self.r.text):

            # Search for the given pattern
            if re.search(search_re, archive_date) or re.search(search_re, archive_url) or re.search(search_re, archive_label):
                self.archive_list.append(Archive(archive_url, archive_date, archive_label))

        if len(self.archive_list) == 0:
            for archive_url in re.findall(URL_STORMS_REGEX_PATTERN_ARCHIVE_FINAL, self.r.text):
                self.archive_list.append(Archive(archive_url=archive_url))
    """

    def get_archive_list(self, search_re: str = '.*') -> List[Archive]:
        """Get a list of all archive objects with the associated regular expression

        :param search_re: The regular expression to search for. Applies to archive date, url, and label
        :returns: A list of archive references (information about tars from the website)
        """

        # If the user has already asked for a list with the same search expression (answer is not already known)
        if search_re != self.archive_list_last_pattern:
            # Generate the list of archive files (clear old list if one exists)
            self.generate_archive_list(search_re)

        return self.archive_list
