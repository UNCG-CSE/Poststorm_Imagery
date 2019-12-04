#!/usr/bin/env python3

import os
import sys

from psicollect.common import h

SELF_PATH = os.path.dirname(os.path.abspath(__file__))

paths = {
    'assign': '../assigner/assign.py',
    'catalog': '../cataloging/catalog.py',
    'collect': '../collector/collect.py',
    'resize': '../resizer/resize.py'
}

if len(sys.argv) >= 2 and sys.argv[1] in paths.keys():
    script = h.validate_and_expand_path(os.path.join(SELF_PATH, paths[sys.argv[1]]))
    sys.argv.remove(sys.argv[1])
    sys.argv[0] = str(script)
    exec(open(sys.argv[0]).read())
elif len(sys.argv) >= 2:
    print('Unknown sub-command "%s".'
          '\nValid sub-commands are %s'
          % (sys.argv[1], ', '.join(paths)))
else:
    print('Usage: %s [%s]'
          % (sys.argv[0], '|'.join(paths)))
