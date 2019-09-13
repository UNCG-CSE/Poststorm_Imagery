"""A file that contains some commonly used strings (constants)"""

FORMAT_TIME = '%B %d, %Y at %I:%M %p'

DATA_PATH = '../../data/'
TAR_CACHE = 'tar_cache/'
TAR_SUFFIX = '.tar'

LOCK_TOTAL_SIZE_BYTES_FIELD = 'total_size_bytes'
LOCK_PART_SIZE_BYTES_FIELD = 'size_bytes'
LOCK_SUFFIX = '.lock'

PART_SUFFIX = '.part'
URL_BASE = 'https://storms.ngs.noaa.gov/'
URL_STORMS = URL_BASE + 'storms/'
URL_STORMS_REGEX_PATTERN_INDEX = '<a href=\"(.+/storms/([^/]+)/index\\.html)\">([^\\(]+)\\(([^\\)]+)\\)</a>'
