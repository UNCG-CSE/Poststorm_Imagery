#!/usr/bin/env python3

import os
import sys

from psic import h

SELF_PATH = os.path.dirname(os.path.abspath(__file__))

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
