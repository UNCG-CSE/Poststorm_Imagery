#!/usr/bin/env python3

import argparse
from os import getcwd
from typing import Set

from psicollect.cataloging.make_catalog import Cataloging, CatalogNoEntriesException, PathParsingException
from psicollect.common import s, h

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog=(s.ROOT_CMD + ' catalog'))

parser.add_argument('--extension', '-e', default='jpg',
                    help='The file extension to restrict the search to (Default: %(default)s).')

parser.add_argument('--fields', '-f', type=Set, default=s.DEFAULT_FIELDS.copy(),
                    help='The various fields listed within a python set to grab from the .geom file as well as '
                         'optional fields "size" and "date" for the size of the image and the date taken respectively '
                         '(Default: %(default)s).')

parser.add_argument('--silent', '-s', action='store_true', default=False,
                    help='If included, the program will only print out errors (Default: %(default)s).')

parser.add_argument('--verbosity', '-v', type=int, default=s.DEFAULT_VERBOSITY,
                    help='Changes the log / debug message verbosity. Not all functions may be affected by this '
                         'value! Possible values are ... '
                         '0 = only errors, '
                         '1 = low, '
                         '2 = medium, '
                         '3 = high '
                         '(Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

try:
    Cataloging.generate_index_from_scope(scope_path=getcwd(),
                                         file_extension=OPTIONS.extension,
                                         fields_needed=OPTIONS.fields,
                                         debug=(not OPTIONS.silent) or OPTIONS.debug,
                                         verbosity=OPTIONS.verbosity)

    # Return that cataloging was successful
    exit(0)

except (CatalogNoEntriesException, PathParsingException) as e:
    h.print_error(e)
except KeyboardInterrupt:
    h.print_error('\nCataloging was prematurely ended.')

# If there was an exception return code 1 (error)
exit(1)
