#!/usr/bin/env python3

import os
import sys

from psicollect.common import h, s

SELF_PATH = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    'catalog': '../cataloging/catalog.py',
    'collect': '../collector/collect.py'
}


def main():
    if len(sys.argv) >= 2 and sys.argv[1] in PATHS.keys():
        script = h.validate_and_expand_path(os.path.join(SELF_PATH, PATHS[sys.argv[1]]))
        sys.argv.remove(sys.argv[1])
        sys.argv[0] = str(script)
        exec(open(sys.argv[0]).read())
    elif len(sys.argv) >= 2 and (sys.argv[1] != ('--help' or '-h')):
        print('Unknown sub-command "%s".'
              '\nValid sub-commands are %s'
              % (sys.argv[1], ', '.join(PATHS)))
    else:
        print('Usage: %s [%s]'
              % (s.ROOT_CMD, '|'.join(PATHS)))


if __name__ == 'main':
    main()
