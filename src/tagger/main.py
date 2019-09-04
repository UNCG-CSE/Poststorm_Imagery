import re
import requests

URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'

try:
    r = requests.get(URL_BASE)
    if r.status_code == requests.codes.ok:
        print('Connection successful!')

        list_storms = dict()

        for storm_id, storm_name in re.findall("<a href=\"https://geodesy\\.noaa\\.gov/storm_archive/storms/([^/]+)/index\\.html\">(.*)</a>", r.text):
            list_storms[storm_id] = storm_name

        print()
        for storm in list_storms:
            print(list_storms[storm])
    else:
        print('Connection failed! Returned code: ' + r.status_code)
except Exception as e:
    print('Error occurred while trying to connect to ' + URL_BASE)
    print('Error: ' + str(e))