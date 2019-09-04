import re

import requests
from requests import Response

from src.tagger.Storm import Storm

URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'
URL_STORMS_REGEX_PATTERN = \
    "<a href=\"https://geodesy\\.noaa\\.gov/storm_archive/storms/([^/]+)/index\\.html\">([^\\(]+)\\(([^\\)]+)\\)</a>"

# Declare variable to hold the HTTP request information
r: Response

# Attempt to connect to the NOAA website
try:
    r = requests.get(URL_BASE)
    if r.status_code != requests.codes.ok:
        print('Connection refused! Returned code: ' + r.status_code)
        exit()

    print('Connection to website successful!\n')

    storm_list = list()

    for storm_id, storm_name, storm_year in re.findall(URL_STORMS_REGEX_PATTERN, r.text):

        storm_list.append(Storm(storm_id, storm_name, storm_year))

    # Present the storm as a number the user can reference quickly
    storm_number = 1

    for storm in storm_list:
        print(str(storm_number) + '.  \t' + str(storm))
        storm_number += 1

except Exception as e:
    print('Error occurred while trying to connect to ' + URL_BASE)
    print('Error: ' + str(e))
