#!/usr/bin/env python3

################################################
# Define command-line parameters and arguments #
################################################
import os
import sys

from psic import h

SELF_PATH = os.path.dirname(os.path.abspath(__file__))

# r = argparse.ArgumentParser(add_help=False, prog='psic')
#
# r_subparsers = r.add_subparsers(title='operation', dest='module')
#
# r_subparsers += assign_parser()
#
# # p_assign = p_subparsers.add_parser(name='assign', help='JSON API for assigning images via the dashboard')
# # p_assign.add_argument('extras', nargs='*', default='--help', help='Operation specific parameters')
# # - '**/psic/assigner/assign.py'
# # - '**/psic/cataloging/catalog.py'
# # - '**/psic/collector/collect.py'
# # - '**/psic/resizer/resize.py'

paths = {
    'assign': '../assigner/assign.py',
    'catalog': '../cataloging/catalog.py',
    'collect': '../collector/collect.py',
    'resize': '../resizer/resize.py'
}

if len(sys.argv) > 1 and sys.argv[1] in paths.keys():
    script = h.validate_and_expand_path(os.path.join(SELF_PATH, paths[sys.argv[1]]))
    sys.argv.remove(sys.argv[1])
    sys.argv[0] = str(script)
    exec(open(sys.argv[0]).read())
else:
    h.print_error('Unknown sub-command "%s".'
                  '\nValid sub-commands are %s'
                  % (sys.argv[1], ', '.join(paths)))
