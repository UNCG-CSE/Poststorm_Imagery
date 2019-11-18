"""A file that contains some commonly used values"""

DEFAULT_DEBUG: bool = False
DEFAULT_VERBOSITY: int = 1
FORMAT_TIME = '%B %d, %Y at %I:%M %p'

DATA_PATH = '../../../../data/'
SMALL_PATH = '../../../../small/'
ARCHIVE_CACHE = 'archive_cache/'

LOCK_TOTAL_SIZE_BYTES_FIELD = 'total_size_bytes'
LOCK_PART_SIZE_BYTES_FIELD = 'size_bytes'
LOCK_SUFFIX = '.lock'

PART_SUFFIX = '.part'
URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'

# Matches reference link to each storm (HTML)
# Groups: <storm_url>, <storm_id>, <storm_title>, <storm_year>
URL_STORMS_REGEX_PATTERN_INDEX = '<a href=\"(.+/storms/([^/]+)/.*?index\\.html)\">([^\\(]+)\\(([^\\)]+)\\)</a>'

CATALOG_FILE_NAME = 'catalog'

# The fields to grab from the .geom file of images when assembling a catalog
DEFAULT_FIELDS = {'file', 'size', 'date',
                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}

RESIZE_SUB_FOLDER = '/small/'
