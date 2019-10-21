"""A file that contains some commonly used strings (constants)"""
from os import path

SELF_PATH = path.dirname(path.abspath(__file__))
DATA_PATH = path.join(SELF_PATH, '../../../../data')
SMALL_PATH = path.join(SELF_PATH, '../../../../small/')

DEFAULT_DEBUG: bool = False
DEFAULT_VERBOSITY: int = 1
FORMAT_TIME = '%B %d, %Y at %I:%M %p'

TAR_CACHE = 'tar_cache/'
TAR_SUFFIX = '.tar'

LOCK_TOTAL_SIZE_BYTES_FIELD = 'total_size_bytes'
LOCK_PART_SIZE_BYTES_FIELD = 'size_bytes'
LOCK_SUFFIX = '.lock'

PART_SUFFIX = '.part'
URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'

# Matches reference link to each storm (HTML)
# Groups: <storm_url>, <storm_id>, <storm_title>, <storm_year>
URL_STORMS_REGEX_PATTERN_INDEX = '<a href=\"(.+/storms/([^/]+)/.*?index\\.html)\">([^\\(]+)\\(([^\\)]+)\\)</a>'

# This should only be changed if the format of the catalog is changed to where old versions aren't compatible
CATALOG_SCHEMA = 'v1'

# The base directory to store all new catalog files and read from existing catalog files (schema dependent)
CATALOG_DATA_PATH = path.join(DATA_PATH, 'catalogs/' + CATALOG_SCHEMA + '/')

# '${storm_id}' is replaced with the storm's id (usually lower-cased storm name)
CATALOG_FILE_NAME = '${storm_id}'

# The fields to grab from the .geom file of images when assembling a catalog
DEFAULT_FIELDS = {'file', 'size', 'date',
                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}

RESIZE_SUB_FOLDER = '/small/'
