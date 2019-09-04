URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'

import requests

try:
    r = requests.get(URL_BASE)
    if r.status_code == requests.codes.ok:
        print('Connection successful!')
    else:
        print('Connection failed! Returned code: ' + r.status_code)
except:
    print('Error occurred while trying to connect to ' + URL_BASE)
LIST_STORMS = {''}