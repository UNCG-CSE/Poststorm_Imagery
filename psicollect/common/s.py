"""A file that contains some commonly used values"""
from os import path

ROOT_CMD: str = 'pstorm'
DEFAULT_DEBUG: bool = False
DEFAULT_VERBOSITY: int = 1
FORMAT_TIME = '%B %d, %Y at %I:%M %p'

PROJECT_DIR = path.expanduser('~/psi/collect')

DATA_PATH = path.join(PROJECT_DIR, 'data')
ARCHIVE_CACHE_PATH = path.join(DATA_PATH, 'archives')

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
CATALOG_SCHEMA = 'v2'

# The base directory to store all new catalog files and read from existing catalog files (schema dependent)
CATALOG_DATA_PATH = path.join(DATA_PATH, 'catalogs/' + CATALOG_SCHEMA + '/')

# ${storm_id} is replaced with the storm's id (usually lower-cased storm name)
CATALOG_FILE = '${storm_id}.csv'

# If the storm_id cannot be parsed (e.g. scope starts in the 'data' folder, but not in any specific storm)
CATALOG_FILE_DEFAULT = 'default.csv'

# The catalog to store all storm data in when stacking
CATALOG_FILE_GLOBAL = 'global.csv'

# The fields to grab from the .geom file of images when assembling a catalog
DEFAULT_FIELDS = {'file', 'storm_id', 'archive', 'image',
                  'date', 'size', 'geom_checksum',
                  'll_lat', 'll_lon', 'lr_lat', 'lr_lon',
                  'ul_lat', 'ul_lon', 'ur_lat', 'ur_lon'}
