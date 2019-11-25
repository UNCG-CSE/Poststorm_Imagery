#!/usr/bin/env python3

import argparse

from psic import s
from psic.resizer.generate import ResizeImages

################################################
# Define command-line parameters and arguments #
################################################

parser = argparse.ArgumentParser(prog='resize')

parser.add_argument('--path', '-p', default=s.DATA_PATH,
                    help='The path on your system to set the scope of file search to (Default: %(default)s).')

parser.add_argument('--output_path', '-o', default=s.SMALL_PATH,
                    help='The path on your system to set the output of resized images (Default: %(default)s).')

parser.add_argument('--scale', '-s', type=float, default=0.15,
                    help='The resolution in comparison to the original image to shrink the original image to. '
                         '1 = 100% of original size, 0.15 = 15% of original size, etc. (Default: %(default)s)')

parser.add_argument('--debug', '-d', action='store_true',
                    help='If included, the program will print info throughout the process (Default: %(default)s).')

# Add custom OPTIONS to the script when running command-line
OPTIONS: argparse.Namespace = parser.parse_args()

ResizeImages.resize_all_images(path=OPTIONS.path,
                               output_path=OPTIONS.output_path,
                               scale=OPTIONS.scale,
                               debug=OPTIONS.debug)
