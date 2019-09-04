import re
from typing import List

import requests
from requests import Response

from src.tagger.Storm import Storm

URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'
URL_STORMS_REGEX_PATTERN = \
    "<a href=\"https://geodesy\\.noaa\\.gov/storm_archive/storms/([^/]+)" \
    "/index\\.html\">([^\\(]+)\\(([^\\)]+)\\)</a>"


class ConnectionHandler:

    # Declare variable to hold the HTTP request information
    r: Response

    storm_list: List[Storm] = list()

    def __init__(self):
        self.connect()
        self.generate_storm_list()

    def connect(self):
        """
        Attempt to connect to the website via an HTTP request
        """
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

    def generate_storm_list(self):

        self.storm_list = list()

        for storm_id, storm_name, storm_year in re.findall(URL_STORMS_REGEX_PATTERN, self.r.text):
            self.storm_list.append(Storm(storm_id, storm_name, storm_year))
